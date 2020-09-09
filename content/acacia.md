Title: Firewall ban-sharing across machines
Date: 2020-09-15
Category: Tech

How can you block one IP simultaneously on multiple machines?

## [The goal](#goal) {: #goal }

As described in [My infrastructure as of 2019](./infrastructure-2019), my
machines are located in three different sites and are loosely coupled.
Nonetheless, I wanted to set things up so that if an IP address is acting
maliciously toward one machine, all my machines block that IP at once so the
meanie won't get to try one machine after another.

This isn't exactly new, with computers or even in
[nature](https://www.newscientist.com/article/mg12717361-200-antelope-activate-the-acacias-alarm-system/).
That's why I named this *acacia*.

One of multiple ways to achieve this goal would have used
[BGP](https://en.wikipedia.org/wiki/Border_Gateway_Protocol) and communities.
The problem with this approach is that I wanted all exchanges between my
machines to be encrypted. I could have met this requirement with a VPN, but I
would have had to set up too many sessions for my taste. And I wanted to
develop a REST API, just for its own sake.

## [The REST API](#rest) {: #rest }

I wanted some boring technology so I went with Flask and PostgreSQL. This
worked quite well and I enjoyed writing it. I also wrote a client in Python.
The client reads the locally blocked IP addresses, sends them to the API, and
then fetches the complete block list from the API and feeds it to
[pf(4)](https://man.openbsd.org/pf.4)

At the beginning, my code was very unoptimized. I definitely didn't want to run
the polling too frequently, so I set it to `*/5`. The new problem was that a
lot can happen in 5 minutes. I thought I could get closer to *real-time* with
some [Pubsub](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern).
And I wanted to play with Pubsub.

## [Pubsub](#pubsub) {: #pubsub }

I initially tried to use a light [MQTT](https://en.wikipedia.org/wiki/MQTT)
implementation. However I was only left with [an itch to
scratch](https://mosquitto.org/), as I couldn't get the examples to work.

While reviewing tb@'s work to update our [Redis port to the 6.x
branch](https://github.com/openbsd/ports/commit/e9670716ad4afb5aa92c9e35ed08fe526ad1a15c),
I noticed they had finally added TLS support. Well, that was great: I already
had a Redis instance running and I like the software, so much that [I went
through](https://university.redislabs.com/certificates/user/51165/course/course-v1:redislabs+RU101+2020_03)
their [RU101 online course](https://university.redislabs.com/courses/ru101/)
(and also, I had a lot of free time).

I got a proof of concept to work really easily (in Python as well). I made it
evolve into a simple daemon. It worked well... when it was correctly connected
to Redis.

The problem is that I often need to reboot my infra to
[upgrade](./upgrading-openbsd-with-ansible) it. That daemon didn't always
detect it had lost the connection to the Redis server. To make the problem
worse, I couldn't check at any given time whether the script was correctly
connected to Redis. Redis can tell me how many listeners a channel has, but
that may not reflect reality.

Only currently connected clients receive a Pubsub message. Therefore, I
couldn't ditch my API. Instead, I use the Pubsub system as a light and near
real-time system, and use the REST API to be confident no server misses any
data.


## [Rewriting the pubsub daemon in go](#go) {: #go }

Initially, what motivated me the most was to have a web status page so I could
check whether it was connected to Redis with any http client. Doing that in
Python would not have been simple. Based on what I had heard about Golang, I
thought that would be more accessible.

Indeed, I painlessly achieved what I wanted. The new daemon is much more
reliable (I haven't been able to disconnect it while it thinks it's connected)
and I have a `/status`  http endpoint to monitor it anyway.

I thought maybe people might want to do more stuff or other stuff with this
daemon so I made it generic. You can specify any number of channels, each with
an associated command you want it to execute.

## [How do I use it](#usage) {: #usage }

### [Infrastructure](#infra) {: #infra }

I recently published on Github one repository for the [API (+ the
client)](https://github.com/danieljakots/acacia_api) and another one for the
[Pubsub daemon](https://github.com/danieljakots/acacia_pubsub). Each has a
README, but here's how I use the whole:

I run the flask API under docker because I didn't find a way I liked under
OpenBSD. While Redis uses an internal PKI, for the API I just use Let's
Encrypt. For Redis' PKI, I use a basic shell wrapper based on
[shellpki](https://github.com/Evolix/shellpki).

Here's an excerpt of my `pf.conf`:

~~~
table <api_bans> persist file "/etc/pf.api"
table <bruteweb> persist
[...]
block drop in quick from <api_bans>
block drop in quick from <bruteweb>
[...]
pass in on vio0 proto tcp to port { www, https } keep state \
  (max-src-conn XXX, max-src-conn-rate YYY, \
  overload <bruteweb> flush global)
~~~

I use a table per protocol (e.g. *bruteweb*, *brutessh* and so on). This allows
me to identify why an IP has been banned.

I also have on each machine these two cron jobs:

~~~
#Ansible: acacia_client cron api
*/5 * * * * /usr/share/scripts/acacia_client -q cron --only-api
#Ansible: acacia_client cron pubsub
* * * * * /usr/share/scripts/acacia_client -q cron --only-pubsub
~~~

Let's dive into each of these two modes!

### [The REST API mode](#apimode) {: #apimode }

In API mode, the script gets the IP addresses from the *brute\** tables and
sends them to the API. Then it fetches the whole list of IP addresses and loads
it into pf. Finally, the script expires the IP addresses in *brute\** so it
doesn't process them eternally.

### [Pubsub Mode](#pubsubmode) {: #pubsub }

In pubsub mode, the script gets the IP addresses from the *brute\** tables and
shares them over Pubsub. Nothing more, to keep it light.

On each machine I also have a simple script that will ban a given IP address:

~~~
#!/usr/bin/env python3

import ipaddress
import subprocess
import sys


def main():
    ip = sys.argv[1]
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        print(f"{ip} is not valid", file=sys.stderr)
        sys.exit(1)
    subprocess.run(
        ["/sbin/pfctl", "-t", "api_bans", "-T", "add", ip],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
~~~

Since acacia_pubsub is dropping privileges, I need a
[doas(1)](https://man.openbsd.org/doas) rule:

~~~
permit nopass _acacia as root cmd /usr/share/scripts/acacia_ban
~~~

And then acacia_pubsub can call the script to ban it.

### [Cron job execution frequency](#frequency) {: #frequency }

Pubsub is lighter than doing the REST dance so it runs each minute. It's not
perfect but there is no way to get a "notification" from pf when an IP address
is banned. (Even using OpenBGPD, AFAIK, you can automatically fill a pf table
from a community but you can't get it to automatically update a community from
a pf table).


## [Conclusion](#conclusion) {: #conclusion }

With these different bricks, any IP that gets blocked by one machine will
automatically get blocked by my other machines, in near real-time. And all
traffic still benefits from TLS.
