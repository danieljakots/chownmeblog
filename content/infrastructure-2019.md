Title: My infrastructure as of 2019
Date: 2020-03-06
Category: Tech

I've wanted to write about my infrastructure for a while, but I kept thinking,
"I'll wait until after I've done $next_thing_on_my_todo." Of course this cycle
never ends, so I decided to write about its state at the end of 2019. Maybe
I'll write an update on it in a couple of moons; who knows?

## [Goal for this infrastructure](#goal) {: #goal }

The goal for my infrastructure is to run the services I need. While a lot of
people in the homelab community experiment and play with software for its own
sake, I actively use the stuff I host. When I stop, I kill the service (though
I'm not as proficient at this as [Google](https://killedbygoogle.com/)).  These
are my production systems, and when one of them is down, I do miss it.

I kind of enjoy working on this infrastructure, but not that much (I used to
enjoy it more), so I'm careful with the software I choose. I want to spend time
on it when *I want to*, not because *I have to* (e.g. because something broke).
Consequently, I do my best to pick reliable, boring and easy software. Those
are my kinks.

Why do I host this myself? Mostly trust issues, and the fact that I care about
sovereignty.

I tend to lock down services as much as I can, either cutting them off
completely from the Internet (e.g. for *imap*) or running them on a
non-standard port and [enabling 2FA](./2FA-with-ssh-on-OpenBSD.html). I don't
use a VPN (mostly because I haven't come up with a nice, clean option yet), so
I restrict access to my services in different ways.

For most things, I'm the only user, which is both sad (as it's a waste of
resources) and great (as I can be more nimble). A notable exception is my
mastodon instance which is also used by [my
cat](https://awoo.chown.me/@jeancanard).

## [Machines](#machines) {: #machines }

My machines are hosted in 3 different places. First is at
[Exoscale](https://www.exoscale.com/), second is
[Vultr](https://www.vultr.com/) and the third is... my flat.

All of them run either OpenBSD on its -current branch, or the latest version of
Ubuntu. At this time, that's Ubuntu 19.10. After a couple of years working on
OpenBSD ports (i.e. packaging), I believe fresh software is better,
security-wise.

They're managed with Ansible. I began my Ansible repository 4 years ago and it
has about 1500 commits in it. I wrote the Ansible to fit my needs rather than
making generic (and therefore reusable) roles, so it's not public.

I update the OpenBSD machines regularly to a newer OpenBSD snapshot (so of
course the process has been
[automated](./upgrading-openbsd-with-ansible.html)). For Ubuntu, I prefer to
reinstall them, since they're managed by Ansible and they don't have any data
on them. Reinstalling machines regularly helps spot missing pieces in Ansible.
:P

All the three sites are as
[standalone](https://en.wikipedia.org/wiki/Loose_coupling) as possible. This is
both so that in the case that one gets pwned it won't help the attacker to
[move laterally](https://en.wikipedia.org/wiki/Network_Lateral_Movement), and
so that if one is unavailable it shouldn't impact anything else.

### [ns3.chown.me (OpenBSD)](#ns3) {: #ns3 }

It's my secondary name server and as you can guess, it replaced ns2. It's the
only machine that I don't back up, since I can replace it with my Ansible
without losing data.

It's hosted by *Vultr*. I mostly picked them because they offer OpenBSD
hosting. This virtual machine is in Toronto and has 1 CPU and 512M of ram.
(Disk space is not relevant here).

I wanted a different hosting provider/AS than my main name server for obvious
reasons of resiliency. Every now and then I think about using another name
server (whether instead of this machine or in addition to it, I don't know)
provided by my registrar (Gandi), but it has a low priority on my todo list.

The name server I use is *NSD*. I could use another one (like *knot*) as my
main name server also uses *NSD*, but the issues related to running the same
software on both aren't that serious in my case.

Since this machine doesn't do much otherwise, it's running
[mownitoring](https://github.com/danieljakots/mownitoring) to check that
everything works.

### [virtie.chown.me (OpenBSD)](#virtie) {: #virtie }

This virtual machine is the main one in my infrastructure. A moment ago your
browser connected to it to get this page. :)

It's hosted by Exoscale (with whom my experiences have been nothing less than
perfect). It's my oldest VM (4 or 5 years old). It has 1 CPU, 1G of ram and 50G
of disk space.

To host my blog I use OpenBSD's httpd which is fronted by *HAProxy*. While I
could remove *HAProxy*, I like this software and I trust it [more
than](https://ftp.openbsd.org/pub/OpenBSD/patches/5.6/common/022_httpd.patch.sig)
[httpd](https://github.com/openbsd/src/commit/49b1a9b154081c713af219b2422adaf51ca2584d).

In addition to hosting my blog, it hosts my email. I switched to *postfix* in
the beginning of 2019 after a couple of years running *OpenSMTPD*. Since I
switched to *postfix* I also dropped *spamd* (the OpenBSD greylisting daemon).
I enabled [FCrDNS](https://en.wikipedia.org/wiki/Forward-confirmed_reverse_DNS)
on *postfix* when I switched (at the time it was not available on *OpenSMTPD*)
and I didn't notice more spam. I use *Dovecot* for imap with only my IP
allowed. I can easily allow another IP address with `pfctl -t imap_allowed -Ta
203.0.113.47`.

I've never really had deliverability problems (except with Microsoft, but who
can say they haven't?) I assume my IP has a good reputation, which is why this
VM is the oldest, as I've been reluctant to lose it.

This machine also hosts a *gitolite* for a couple of different internal git
repositories.

### [pancake.chown.me (OpenBSD)](#pancake) {: #pancake }

This machine is an [APU2](https://pcengines.ch/apu2.htm). It acts as a router
for my flat. Since it's way more powerful than necessary for this task, I put
some other stuff on it. It's a trade-off between increasing the attack surface
of a critical machine and leaving a lot of CPU/RAM/SSD unused.

I collect [flows](https://en.wikipedia.org/wiki/NetFlow) on it, which in my
opinion are super cool!

It also hosts influxdb + grafana and some machines send their metrics with
collectd ([which allow signing/encrypting the network
traffic](https://collectd.org/wiki/index.php/Networking_introduction#Cryptographic_setup)).
This doesn't work well for a couple of reasons, so it's waiting to be replaced.

### [kvm1, and sometimes kvm2 (Ubuntu)](#kvm) {: #kvm }

These machines are hosted at home. kvm1 is the main machine, and kvm2 is the
machine I use to play Windows games on another SSD. I boot on the Ubuntu SSD
whenever I want to do something on kvm1 and then I live-migrate guests on it so
I don't experience any downtime. I use full disk encryption on the guests, so
live-migrating (instead of rebooting them) allows me to avoid having to
manually unlock each guest. I encrypt the guests and not the kvm because in the
event of a power outage, machines may come back on, in which case I don't want
them to wait for the passphrase if I'm away. Some hacks could be done to
encrypt them as well, but I'm not willing to do them since they're overkill for
my threat model.

Both machines have an i5-4590. kvm2 has 4x4G of ram with a 256G SSD (which is
enough for the kvm system and all the guests). kvm1 also has a 256G SSD but
while its ram layout would make anyone sensible cringe, it amounts to 20G of
ram! I don't use RAID. kvm0 (the machine they replaced) used to and I wasn't
sure it would work (and I couldn't test it safely since it was my only
machine).

To manage this part of the infrastructure I wrote a [python
script](https://github.com/danieljakots/uv). This script is kind of a wrapper
around libvirt, which itself is kind of a wrapper around qemu, which itself
[wrangles turtles](https://en.wikipedia.org/wiki/Turtles_all_the_way_down).
Contrary to what other people run, I think, a guest disk isn't a qcow2/raw
file. I don't want to pile filesystems on one another, so I manage guests'
disks on the hypervisor with LVM directly. I tend to have multiple disks to
bring more flexibility to the disk layout/partitioning than OpenBSD would,
thanks to LVM.

It hosts all the following virtual machines:

### [manicouagan1 (OpenBSD)](#manicouagan1) {: #manicouagan1 }

This machine's name dates from back when I used names from Québec to name my
machines.  The name comes from the [Manicouagan
Reservoir](https://en.wikipedia.org/wiki/Manicouagan_Reservoir), as this
machine is where I put my backups.

My backups are in three different places:
- locally, i.e. each machine stores its backup on itself
- *manicouagan* copies all the backups onto itself
- *manicouagan* ships the backups to an s3-like provider

I use *BorgBackup* for the backup, *rsync* to copy them onto *manicouagan* and
*s3cmd* to ship them away. I tried to use *rclone* but it used more ram.  Once,
I was away from my place for a long time, and my whole infra there became
unreachable, so I decided to temporarily host stuff on the cloud in the
meantime. I had to restore those backups and it went so nicely that I'm not
looking to change anything. Borg is awesome!

This machine is also a syslog server to which all my OpenBSD machines ship
their logs. Thanks to OpenBSD syslogd (bluhm@ <3), it uses TCP+TLS with a
private PKI. This is mostly in case one machine gets hacked, to help with
[forensics](https://en.wikipedia.org/wiki/Forensic_science).

I wrote a short script that shows me the largest data transfers on my router. I
use this to check that the backups are alive (I receive emails if the
*BorgBackup* script fails, but isn't that less fun? :))

### [db1 (OpenBSD)](#db1) {: #db1 }

This machine hosts postgresql and redis. Two boring pieces of software which I
love. Redis requires so little care that when I moved from db0, I forgot I had
it!

### [web1 (OpenBSD)](#web1) {: #web1 }

This machine runs nginx for my whole web presence excluding my blog. It hosts
*nextcloud*, *tt-rss*, *shaarli* and pics.chown.me (whose content I should
update).

Have you ever thought, "naah I'm too much paranoid"? Yeah, me neither. A few
months ago, I restricted all the non-static websites (with the exception of
Mastodon) behind an *htpasswd*. There was some value in having them publicly
accessible, but at the time I thought it was not worth the risk. The php-fpm
pools should be secure (they have their own users, they're chrooted and so on)
but I'm not entirely sure I'm doing this stuff properly and it is such a pain
to get it working that I'm not willing to look into it more than that.

Nginx also acts as a reverse proxy for the docker containers that run on
another machine. Finally, it hosts *minio* for *mastodon*.

### [docker2 (Ubuntu, obviously)](#docker2) {: #docker2 }

This machine runs a few docker containers through *docker-compose*:

* 3 containers for *mastodon* (*ruby on rails* stuff, a node api and *sidekiq*)
* container running the code I wrote for api.chown.me; it's a *flask*
  application
* registry:v2 that I have simply to ease the transfer of docker images

I build all the docker images I run myself (except for the registry one).

My policy regarding those containers is that they must not store any data
locally (i.e. they don't have a *docker volume*). This allows me not to care
about backups. The *docker-compose.yml* is tracked in my personal git, so I can
trash the VM any time.

api.chown.me is for now mostly a way to sync a list of IPs to block on my whole
infra. This way, if an IP is acting badly on one machine, it doesn't get to try
its luck on another of my machines. This list is also supplemented by public
lists of threats.

## [That's it for now](#end) {: #end }

Currently, my infrastructure is good at meeting my needs. It's not perfect, of
course, and it's a perpetual work in progress. But it's stable, and usually the
most I need to do is quickly patch some security vulnerabilities.  Since most
of the resources I use come from reused computers hosted at my place, I'm able
to keep the cost (both financial and ecological) really low.
