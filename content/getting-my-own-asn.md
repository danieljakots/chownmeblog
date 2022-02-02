Title: Why and how I got my own ASN!
Date: 2022-02-01
Category: Tech

## [Intro](#intro) {: #intro }

In this article, I'll explain how, and why I acquired an [Autonomous System
Number](https://en.wikipedia.org/wiki/Autonomous_system_(Internet)) and some
IPv6 addresses.

## [Getting some IPv6 cravings again](#cravings) {: #cravings }

In late 2020, I read
[https://blog.dave.tf/post/new-kubernetes/](https://blog.dave.tf/post/new-kubernetes/).
In this post, the author said if they were to build something new, they would
focus on "IPv6 only, mostly". This post got me to thinking about having some
IPv6 connectivity again.

Before I got to Montreal, I used to have access to IPv6 Internet. I can't
remember for sure, but I think it was through a [Hurricane
Electric](https://tunnelbroker.net/) tunnel.

## [No Native IPv6](#native) {: #native }

My Internet Service Provider (ISP) is a small ISP. They don't own the [last
mile](https://en.wikipedia.org/wiki/Last_mile). They provide native IPv6 for
some other subscription of theirs, where they can. However, on the service I'm
subscribed to, the last mile owner is still *in the process of deploying IPv6*
(*always-have-been-meme.png*).

No native IPv6 means I'll need to setup some tunnels, one way or another.

### [Using a tunnel providers](#tunnels) {: #tunnels }

The first thing I looked at was Hurrincane Electric, since it was the only
provider I knew at the time. Unfortunately, they only offer
[GRE](https://en.wikipedia.org/wiki/Generic_Routing_Encapsulation) tunnels,
which means no encryption. One could argue that in 2020+, with HTTPS and
[DoT](https://en.wikipedia.org/wiki/DNS_over_TLS)/[DoH](https://en.wikipedia.org/wiki/DNS_over_HTTPS),
there is little unencrypted traffic, but to that I'll reply "meh".

### [Creating my own tunnel](#hosters) {: #hosters }

I thought I could rent a virtual machine (preferably, since tunnels require
little resources and VMs are way cheaper than dedicated servers) and run my own
tunnel with the IPv6 it provides.

As mentioned in [my infrastructure blog post](./infrastructure-2020), I
have multiple networks (VLAN) at home. Because I didn't want to do some
*unholy* things, I needed to have a /64 per network, meaning multiple /64s for
my home.

I went on the hunt for a provider that offers something like a /56 (or the
option to get multiple /64s). Unfortunately, I didn't find anything reasonable.
I eventually found some high end servers that came with a /48 but since they
cost nearly as much as my rent, I'll pass. Most providers give at best a /64,
but it can also be a /128 (lol) or nothing (yeah who cares about IPv6).

### [It will be more complicated](#other) {: #other }

I asked a network engineer friend if he knew any hosting services providing
more than a /64 with a cheap machine and -well- he gave a network-engineer type
of answer "just get your IPv6 addresses and announce them".

After inquiring more detail, he kindly answered and I decided to proceed with
this.

### [Some context though](#context) {: #context }

While I don't qualify as a network engineer, I'm not completely ignorant
network-wise. I used to work for a [network operator](http://as197696.net/) (so
I'm no stranger to BGP) and I used to be a volunteer for [a
couple](https://www.ffdn.org/) [of non-profit](https://www.franciliens.net/)
[ISPs](https://gitoyen.net/) back in France.

## [Getting some resources](#resources) {: #resources }

**Disclaimer**: Keep in mind what follows is my own interpretation. Go read the
relevant parties' websites and agreements to make your own opinion.

Following my friend's advice, I set out to get some IPv6 addresses and an ASN
to announce them. I could then create my own (encrypted of course) tunnels to
get IPv6 at home.

I would also be able to achieve what I had wanted for years: play with
[anycast](https://en.wikipedia.org/wiki/Anycast).

## [Picking a RIR](#RIR) {: #RIR }

IP addresses and an ASN can be obtained through a
[RIR](https://en.wikipedia.org/wiki/Regional_Internet_registry).

Because of my personal situation (which I won't get into), there are two RIRs I
could ask: ARIN and the RIPE.

### [ARIN](#arin) {: #arin }

[ARIN](https://en.wikipedia.org/wiki/American_Registry_for_Internet_Numbers) is
the RIR for Corporatist America. If you're not a corporation, well you're not
going to go very far.

I considered creating my own, but the cost exceeded what I was ready to spend
on the project. As affordable as it would have been for a corporation, it would
not be for me.

### [RIPE](#ripe) {: #ripe }

[RIPE](https://en.wikipedia.org/wiki/RIPE_NCC) is the RIR for Socialist Europe.
You're an individual and you want some resources? That's totally fine, go ask
for some. Well, not directly. RIPE doesn't talk to peasants, you'll have to ask
a
[LIR](https://en.wikipedia.org/wiki/Regional_Internet_registry#Local_Internet_registry).
If they can provide it directly, they do.  Otherwise, they act as a proxy
between you and the RIPE.

I went for this option. From my time volunteering, I know quite a lot of people
in quite a lot of LIRs.

### [Grifon](#grifon) {: #grifon }

I chose [Grifon](https://grifon.fr/) for no particular reason.

## [Obtaining the resources](#obtaining) {: #obtaining }

My initial plan was to get a /48 to get IPv6 at home and a /48 to play with
anycast (because it is the smallest network you can announce on the Internet).
I couldn't do anything else with the /48 I would anycast, by design.

So after completing my membership, I requested a /48 IPv6 from the RIPE
(through my LIR, as explained). A few days after the request and with some
follow-up questions, I got [my first
prefix](https://bgp.he.net/net/2001:67c:291c::/48). Now that I had some address
space, I could justify the need for an ASN. I made the request and got
[it](https://bgp.he.net/AS211935).

So I requested a /48 to my LIR from its own resources.
[Alarig](https://www.swordarmor.fr/) kindly carved [my second
/48](https://bgp.he.net/net/2a0e:f43::/48) out of the LIR reserved address
space for this purpose.

(For the readers not versed in the RIPE-world technicalities, [the first /48 is
a PI, the second is a
PA](https://www.ripe.net/participate/member-support/copy_of_faqs/isp-related-questions/pa-pi)).

### [Getting a third /48](#feda) {: #feda }

Shortly after I setup IPv6 at home, I noticed Google believed I was in France.
[Given that even huge networks struggle to fix
problems](https://www.iucc.ac.il/en/blog/2021-05-google-geo-location/), I had
no hope for myself. I thought that maybe using a netblock from ARIN would solve
my issue.

At first, I went to ask [a non-profit I contribute to](https://igwan.net/), but
it didn't work because we hit a technical limitation from a common provider.

Then, I found the [Nato Internet Service](https://internet.nat.moe/). They
provide a /48 (or more if you can justify the need) out of a netblock called
feda (because it comes from `2602:feda::/36`).

Unfortunately, this didn't solve my geolocation problem with Google. I even had
a new problem, my FEDA block was geolocated in China, but I easily fixed it in
maxmind db, and it seems to have been enough.

However, as the quote says ["Everybody has a testing netblock. Some people are
lucky enough enough to have a totally separate netblock to run production
in."](https://twitter.com/stahnma/status/634849376343429120), I had now a /48 I
could use to test stuff for anycast.

### [Using an IPAM](#IPAM) {: #IPAM }

*Are you into IPAM porn? Because if you're into IPAM porn, you're in for a
treat!*

Now that I had 3 netblocks that I was going to cut into smaller networks, I
would need a [tool to track
usage](https://en.wikipedia.org/wiki/IP_address_management). Nowadays, most
people use [NetBox](https://github.com/netbox-community/netbox). I thought I
was going to use it, but I read a
[couple](https://lobste.rs/s/95hsvw/stupid_light_software#c_1n5zrk) of
[times](https://lobste.rs/s/lrphxy/designing_low_upkeep_software#c_pjyzfd) the
author of sidekiq and it made me realize I didn't need such a complex tool.

#### [IPAM v1](#IPAM1) {: #IPAM1 }

For shits and giggles, I initially thought "wouldn't it be nice to use tree(1)
to see everything??". I created directories for blocks, and files for
addresses. Here's what it looked like:

~~~
~/git/git.chown.me/ipam/ipv6 (master=)$ tree
.
├── 2001:67c:291c::-48
│   └── 2001:67c:291c::1
└── 2a0e:f43::-48
    ├── 2a0e:f43:0:100:-56
    │   └── NEXT-ONE
    ├── 2a0e:f43:0:fd00::-56
    │   ├── 2a0e:f43:0:fd00::1
    │   └── INTERCO-WG1
    ├── 2a0e:f43:0:fe00::-56
    │   ├── 2a0e:f43:0:fe00::254
    │   └── INTERCO-WG0
    ├── 2a0e:f43:0:ff00::-56
    │   └── 2a0e:f43:0:ff00::1
    └── 2a0e:f43::-56
        ├── 2a0e:f43:0:10::-64
        │   └── 2a0e:f43:0:10::1
        ├── 2a0e:f43:0:40::-64
        │   └── 2a0e:f43:0:40::1
        ├── 2a0e:f43:0:60::-64
        │   └── 2a0e:f43:0:60::1
        ├── 2a0e:f43:0:70::-64
        │   └── 2a0e:f43:0:70::1
        └── 2a0e:f43:0:80::-64
            └── 2a0e:f43:0:80::1
~~~

Note: This predates the move to the feda netblock.

However in the end, editing files was not easy because I had to escape all the
`:` in my shell. I had a lot of fun creating this arborescence, but it was time
to move on to something more practical.

#### [IPAM v2](#IPAM2) {: #IPAM2 }

I went for a single text file in a json-inspired format. Here's what it looks
like:

~~~
$ head -n 30 ipam.txt
ANNOUNCED BY BGP-YYZ
2001:67c:291c::/48 {
	2001:67c:291c::1 {
		anycast.chown.me
	}
}

ANNOUNCED BY BGP-YYZ, NS4
2602:feda:b8e::/48 {
	ANNOUNCED BY pancake
	2602:feda:b8e::/56 {
		2602:feda:b8e:10::/64 {
			LAN
			2602:feda:b8e:10::1 { pancake:vlan10 }
		}
		2602:feda:b8e:40::/64 {
			PHONE
			2602:feda:b8e:40::1 { pancake:vlan40 }
		}
		2602:feda:b8e:60::/64 {
			WINDOWS
			2602:feda:b8e:60::1 { pancake:vlan60 }
		}
		2602:feda:b8e:80::/64 {
			RTBH
			2602:feda:b8e:80::1 { pancake:vlan80 }
		}
	}
[...]
~~~

Note that here RTBH is **only** how I named the network, it's not related to
actual RTBH.

I manage the file with vim and I can easily (un)fold any level whether I want
an overview or a detailed view. Also this may not be entirely up to date haha.

## [The infrastructure](#infrastructure) {: #infrastructure }

### [For anycast](#anycast) {: #anycast }

My initial plan was to get some VMs around the world and announce the /48 on
each.  Easier said than done, because my requirements are to find a provider
which:

* offers a cheap and small VM (i.e. 1cpu, 1G of ram, 20G of disk)
* is willing to setup a BGP session so I can announce my IP addresses
* allows me to install OpenBSD
* provides basic hosting stuff, like setting a PTR on provided IP addresses

I thought "anycast is easy, you just announce your IP everywhere, and done".
Well, yes, but actually no. At least if you don't want to abide by [RFC
7511](https://datatracker.ietf.org/doc/html/rfc7511). Proper routing requires a
lot of work.

I currently have 4 VMs in this anycast network:

* bgp-dus in Düsseldorf, Germany
* bgp-mrs in Marseille, France
* bgp-yyz in Toronto, Canada
* ns4 also in Toronto, Canada

This is a work in progress that probably deserves its own blog post when it's
fully done, so I won't go further into details.

### [For my IPv6 at home](#athome) {: #athome }

As you just read, I have two VMs in Toronto. I wish I could have a provider in
Montreal to reduce latency, unfortunately I've not been able to find one quite
yet.

I had to choose some tunnelling technology. I picked up WireGuard® because it
had recently made it into OpenBSD kernels (see
[wg(4)](https://man.openbsd.org/wg)) and my experience with ipsec is as "good"
as the next person.

My current setup is:

~~~
~/git/git.chown.me/ipam (master=)$ cat schema.txt 
Upstream 1        Upstream 2
   |                 |
   |                 |
   R1------ wg ------R2
   |                 |
   wg                wg
   |                 |
   -------- R3 -------
~~~

R1 and R2 are my VMs in Toronto, and R3 is my router at home. Yes, my router at
home uses BGP, both to announce its own netblock over BGP and to choose the
best route between R1+Upstream 1 and R2+Upstream 2. Isn't that super cool??! :D

R1 and R2 both announce my /48 to their provider. They do so with my public
ASN.

They have a wg link between each other. The goal is twofold:

1. if the session with their upstream fails, the traffic will flow to the other
2. if wg between R3 and R1 or R2 dies. Traffic will flow through the remaining
   wg link

Case 1 isn't actually a problem. Once the session with the upstream fails, it
won't get the [full
view](https://www.bgp.us/routing-table/full-bgp-table-benefits-and-dangers/)
anymore, which means R3 won't get the full view from that router, and it will
*send* traffic only to the other. Traffic *to me* will switch automatically
provided the upstream stops announcing my route (it should, but [sometimes it
doesn't](https://blog.cloudflare.com/analysis-of-todays-centurylink-level-3-outage/))

I prepend that path with my ASN 15 times (picked by "should be good enough
lol") to avoid using it in normal condition.

This simple link was actually quite a big change because until then, R1 and R2
used to do some stateful firewalling (in addition to the one done on R3).
However, this change meant traffic could flow asymmetrically, so I had to
switch to stateless firewall (which I restricted to the specific network, the
rest of the traffic is still checked by [pf(4)](https://man.openbsd.org/pf)
with stateful rules).

R3 announces the /56 I have at home over BGP to R1 and R2. "But this is inter
AS, why didn't you use an IGP???". Well wg(4) doesn't support multicast, and
[ospf6d](https://man.openbsd.org/ospf6d) (and even
[eigrpd](https://man.openbsd.org/eigrpd)) needs it. You can do without
buuuut... I tried and struggled with ospf6d, so sticking with
[bgpd](https://man.openbsd.org/bgpd) was way easier.

Fun fact: I even began to write my own igpd, but I quickly realized I was just
reimplementing bgpd poorly so I aborted.

I actually use a private ASN to announce the /56. I picked 4200211935, so it's
obviously both "it's my ASN", and "it's not *my ASN*":

~~~
danj@bgp-yyz:~$ bgpctl sh
Neighbor                   AS    MsgRcvd    MsgSent  OutQ Up/Down  State/PrfRcvd
pancake-6          4200211935      17289    2134334     0 5d22h44m      1
ns4-6                  211935    1213381    1930550     0 5d23h30m 134718
xenyth-6                62513    1945805      17297     0 6d00h06m 138770
~~~

Of course since I announce a /56 and a private ASN, I needed to stop checking
RPKI for this particular host. Fortunately, bgpd's rules system is really easy
to work with.

### [Software](#software) {: #software }

Of course everything runs OpenBSD! It has a lovely
[bgpd](https://www.openbgpd.org/) in base. OpenBSD ships
[rpki-client](https://rpki-client.org/) which one can use to validate ROA
("improve the routing security" in layman's terms).

OpenBSD developers changed OpenBGPD config since last I used it. The thing I
worry the most about is messing what I announce to my peers. They must have
filters, but I don't want to be *that guy*. OpenBGPD's config file is set in a
way that it's hard to mess up, thanks to sane defaults and a nice logic.

It ships with an excellent example config file making easy to start using it!
For that reason, I'm not going to detail mine.

OpenBGPD uses little memory:

~~~
danj@ns4:~$ bgpctl show rib nei vultr-6 in | wc -l
  135254
danj@ns4:~$ bgpctl show rib nei bgp-yyz-6 in | wc -l
  139312
danj@ns4:~$ bgpctl show rib memory
RDE memory statistics
    139583 IPv6 unicast network entries using 7.5M of memory
    279161 rib entries using 17.0M of memory
    823926 prefix entries using 101M of memory
    156446 BGP path attribute entries using 10.7M of memory
	   and holding 823926 references
    138180 BGP AS-PATH attribute entries using 11.6M of memory
	   and holding 156446 references
       819 entries for 6470 BGP communities using 178K of memory
	   and holding 823926 references
      6803 BGP attributes entries using 266K of memory
	   and holding 41980 references
      6802 BGP attributes using 54.1K of memory
    306537 as-set elements in 280152 tables using 10.9M of memory
    511038 prefix-set elements using 21.6M of memory
RIB using 148M of memory
Sets using 32.5M of memory

RDE hash statistics
	path hash: size 131072, 156446 entries
	    min 0 max 8 avg/std-dev = 1.194/0.759
	aspath hash: size 131072, 138180 entries
	    min 0 max 8 avg/std-dev = 1.054/0.943
	comm hash: size 16384, 819 entries
	    min 0 max 3 avg/std-dev = 0.050/0.000
	attr hash: size 16384, 6803 entries
	    min 0 max 5 avg/std-dev = 0.415/0.000
~~~

Most VMs have only 1G of ram and 1 cpu.

~~~
danj@ns4:~$ top -b -ores
load averages:  0.01,  0.05,  0.02    ns4.chown.me 20:35:57
65 processes: 1 running, 63 idle, 1 on processor  up 13 days,  3:58
CPU states:  2.9% user,  0.0% nice,  2.1% sys,  0.0% spin,  0.1% intr, 94.9% idle
Memory: Real: 411M/713M act/tot Free: 256M Cache: 152M Swap: 192M/512M

PID USERNAME PRI NICE  SIZE   RES STATE     WAIT      TIME    CPU COMMAND
90287 _bgpd      2    0  231M  238M sleep     poll     36:22  0.00% bgpd
88230 _bgpd      2    0   26M   30M idle      poll      8:29  0.00% bgpd
61228 root       2    0   20M   22M sleep     poll     16:59  0.00% bgpd
[...]
~~~

[markdown comment to unfuck vim __ ]: <> (This is a comment, it will not be included)


### [RPKI](#rpki) {: #rpki }

I didn't want to run [rpki-client](https://man.openbsd.org/rpki-client) on each
and every router. I couldn't either because it uses a truckload of inodes and
my /var/ partitions couldn't afford it.

I considered using [RTR](https://datatracker.ietf.org/doc/html/rfc8210),
however it meant running more software (e.g.
[gortr](https://github.com/cloudflare/gortr)/[stayrtr](https://github.com/bgp/stayrtr)).

Also bgpd doesn't support (yet?) encrypted RTR so it would have meant either
doing RTR unecrypted (yuck), or run even more software.

What I ended up doing is running rpki-client on my web server (on which I added
a special partion with way more inodes).

~~~
42 * * * * -n rpki-client -v && \
	cp /var/db/rpki-client/openbgpd /var/www/static.chown.me/pub/rpki/openbgpd && \
	gzip -f /var/www/static.chown.me/pub/rpki/openbgpd
~~~

And on my bgpd routers

~~~
57 * * * * -n ftp -o /var/db/rpki-client/openbgpd.gz https://static.chown.me/pub/rpki/openbgpd.gz && \
	gunzip -f /var/db/rpki-client/openbgpd.gz && \
	bgpd -n && bgpctl reload
~~~

15 minutes ought to be enough, it used to run in 5 minutes, but apparently it
now runs in around 8 minutes, I guess I should setup some monitoring haha.

## [OpenBSD Contributions](#contributions) {: #contributions }

Of course, I found some improvements for the software I use through this
project. Here are some fixes that made it into the OpenBSD trees because of my
playing around:

* [fixed a basic cosmetic problem](https://github.com/openbsd/src/commit/d5980c09d2040665450fb05dc517f02f9059b40f)
* [improved the bgpd.conf example](https://github.com/openbsd/src/commit/7d9b2f2f77bea0095e5af3377fe49c9b1ba47384)
* [fixed a man page](https://github.com/openbsd/src/commit/25b45e4dc40bdb93a2214908573405fd6d7e5dc5)
* [fixed another man page](https://github.com/openbsd/src/commit/f2c1f8a9d7d9a1bd6d0f1bd24202767c14a55827)
* [updated afresh1's bgpd nrpe check](https://github.com/openbsd/ports/commit/824909a45fdb9566129f108c664aacfa148d71ca)
* [got someone to fix a panic when destroying a wg(4) interface](https://github.com/openbsd/src/commit/40192866049d58ca33971afdcb144fab8b38563c)

## [Cost](#cost) {: #cost }

Of course this weird hobby of mine costs money. I'm however very happy of how
low I could keep my expenses.

### [Administrative costs](#admincost) {: #admincost }

Here's what I paid Grifon:

* 15€/y for membership fees
* 90€/y for administrative fees to get the ASN/IPv6 resources

### [Hosting costs](#hostingcost) {: #hostingcost }

Out of 4 VMs I run BGP on, I've been using one for other things, so I'm not
counting it since I would pay for it regardless of this project.

Here's what I pay for the host:

* bgp-mrs: 0€ (thanks [Evolix](https://evolix.com/)! <3)
* bgp-dus: 9€/month
* bgp-yyz: 8.50US$/month

## [Misc resources](#resources) {: #resouces }

### [Traffic engineering](#te) {: #te }

Even if I messed around with BGP before, I hadn't really gone deeper than the
surface. Since I had a lot to learn network engineering-wise, I read a lot of
stuff. Among everything, I highly recommend the [BGP For All
playlist](https://www.youtube.com/watch?v=1pi18uNqsO4&list=PLjVwd8FlHBAQk5U2ScrjpeRJujGTCaMfR)
from [NSRC](https://nsrc.org/)

### [Finding hosters](#findinghosters) {: #findinghosters }

The Google Docs [Providers that offer BGP sessions](http://bgp.services) was
incredibly helpful.

## [Should you do it?](#shouldyoudoit) {: #shouldyoudoit }

Probably no.

While the resources I'm using are plentiful (32-bit ASNs, 128-bit IP
addresses), people's routers
[TCAM](https://en.wikipedia.org/wiki/Content-addressable_memory#Ternary_CAMs)
are not.

My 'experiment' is 3 netblocks out of the ~130k in the
[DFZ](https://en.wikipedia.org/wiki/Default-free_zone).

Note that I'm definitely not the first person to get an ASN for personal use.
Once you begin looking into ASN, there are plenty.

If you really want to play with BGP, you can look into
[dn42](https://dn42.eu/Home)!

## [Outro](#outro) {: #outro }

I've been doing this project for a bit over a year now.

There were some boring tasks (the perpetual quest to find hosters who don't
suck, administrative things to get the resources, etc), but overall, this
project has been incredibly fun!

Yeah sex is good, but have you tried running mtr(8), while shutting a BGP
session, or [remotely triggering a black
hole](https://en.wikipedia.org/wiki/Black_hole_(networking)#Black_hole_filtering)
and watch the traffic change?
