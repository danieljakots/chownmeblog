Title: My infrastructure as of 2020
Date: 2021-04-27
Category: Tech

Last year, I wrote about my infrastructure as of 2019. Here's
the update for 2020! I would advise that you first (re)read
last year's article, since this one will be more like a
[diff](https://en.wikipedia.org/wiki/Diff).

## [Goal for this infrastructure](#goal) {: #goal }

Goals stayed the same.

## [Machines](#machines) {: #machines }

My machines are still hosted in the same 3 different places. The first is
[Exoscale](https://www.exoscale.com/), the second is
[Vultr](https://www.vultr.com/) and the third is... my flat.

My choice for OS didn't change, as in I still use the last LTS-or-not Ubuntu,
which at the end of the year was Ubuntu 20.10. And OpenBSD -current, of course.

I made 446 commits during 2020 in my Ansible repository, according to `git
rev-list --count HEAD --since="Jan 1 2020" --before="Jan 1 2021"` (I'm giving
the command mostly for my next-year self). But keep in mind I really care about
commits doing one thing, and one thing only. While this number may seem high,
I'm sure some people would have been fine with making only one commit
:trollface:.

Infrastructure-wise, I added a system to share blocked IP addresses among
my machines. You can read more about it in [its dedicated
article](https://chown.me/blog/acacia).

### [ns4.chown.me (OpenBSD)](#ns4) {: #ns4 }

This used to be ns3. I wanted to get more use out of this machine, so I needed
to repartition (i.e. reinstall) the OS. I could have gone with ns2, but I
planned to move my irc client from virtie to this one. Latency over ssh is
annoying, and ns4 is 30ms away while virtie is 130ms away. The reverse of the
IP address (i.e. the DNS PTR record) appears on irc, so I wanted to trick
people into thinking I have at least four nameservers :D

Since my irc logs (and more) are on it, I'm now backing up this machine.

I implemented a VPN. Initially it was IPSEC with
[ipsec.conf(5)](https://man.openbsd.org/ipsec.conf.5) and
[npppd(8)](https://man.openbsd.org/npppd.8). I'm surprised I didn't mention it
in my article from last year because I've had this VPN since 2017, I think.
During 2020, I moved to Wireguard® with its [kernel
implementation](https://man.openbsd.org/wg.4).

### [virtie.chown.me (OpenBSD)](#virtie) {: #virtie }

A couple times I thought about dropping the HAProxy + httpd setup and moving
all my web presence to web1 with its nginx. Out of laziness, I didn't do it.

The only thing that changed for this machine is my irc client, which moved to
ns4.

### [pancake.chown.me (OpenBSD)](#pancake) {: #pancake }

I'm using VLANs again on my home infrastructure. I've been using VLANs for a
few years to limit interactions between my devices. At the end of 2019, the
[power flickered](https://en.wikipedia.org/wiki/Power-line_flicker), and I had
troubles with my "manageable" switch. For a few months after that, I used a
"simple" switch so everything was on the same network. I wrote last year's
article during this time, which is why I didn't mention the VLANs.

After a few months, I tried the switch one last time, and this time it worked,
so I went back to using VLANs. I've since bought an "APC Back-UPS BE600M1"
to protect my home infrastructure.  The switch I have is a TP-LINK TL-SG3216. I
have a TL-WA901ND, a VLAN-capable Wifi Access Point, so I can create up
to 4 SSIDs, and each is on a given VLAN.

As mentioned, I use many VLANs to restrict how devices can interact with each
other. For instance, if I were to share my Internet uplink with my neighbor (I
don't, because I assume my ISP's Terms of Service forbid it), she would have
her own SSID on her own VLAN so her devices wouldn't interact with mine.

I use [aggr(4)](https://man.openbsd.org/aggr.4), which is a modern LACP driver.
I doubt this improves the forwarding performance of the router, but I like the
look of the three cables plugged into the switch, and I don't have to figure
out which interface on the apu is em0 or em2 (em1 obviously being the one in
the middle).

### [kvm1, and sometimes kvm2 (Ubuntu)](#kvm) {: #kvm }

No change on the KVM side, other than that they're now running Ubuntu 20.10.

I further automated the post-reinstall step. Reinstalling them frequently is
always nice, allowing me to find things I did manually and forgot to add to my
ansible repository.

The virtual machines it hosts are the same four as before:

#### [manicouagan1 (OpenBSD)](#manicouagan1) {: #manicouagan1 }

This machine doesn't actually hold the backups any longer. I set up a NAS, so I
moved the backup system there. The only role of this machine now is to receive
all the logs via syslogd.

#### [db1 (OpenBSD)](#db1) {: #db1 }

Other than the usual updates, nothing changed.

#### [web1 (OpenBSD)](#web1) {: #web1 }

Very little change here. I've only added <https://px.chown.me> to it.

#### [docker4 (Ubuntu, obviously)](#docker4) {: #docker4 }

In the previous article, it was docker2 (Ubuntu 19.10). I recreated this as
docker3 (Ubuntu 20.04), and now as docker4 (Ubuntu 20.10).

This machine still runs containers through *docker-compose*. I'm still running
docker registry, mastodon and my API. In addition to these, I now have:

* etherpad
* two containers for [nitter](https://github.com/zedeus/nitter) (nitter itself and redis)
* [openbsd-commits-to-mastodon](https://github.com/danieljakots/openbsd-commits-to-mastodon)

My policy about not having data on the machine didn't change. The redis used by
nitter is just for caching.

A few days ago, I accidentally broke the booting system of the machine, and I
chose to reinstall it rather than trying to fix it. This was a good test, since
I still don't have backups for this one. Other than the short period of
unavailability, it went fine.

I considered switching to k3s, but since this setup works fine, I didn't
bother.

### [zfs1 (Ubuntu)](#zfs1) {: #zfs1 }

As briefly mentioned in my article from last year, kvm1 and 2 replaced a
machine called kvm0. Since I still had the hardware around, I decided to use it
as a NAS. I'm using Ubuntu installed on an SSD. Contrary to the other Ubuntu
machines, this one stayed at 20.04. I didn't know if I wanted to switch to
20.10, and doing nothing was the easier path.

A NAS is obviously nothing without storage, and I bought two 4TB Iron Wolf hard
drives. I have a plan to buy two more disks and to change it from a mirror to a
striped mirror. The current computer case and motherboard don't support 5 disks
(4 disks for zfs, and the SSD for the OS). However, I want to reuse hardware
rather than buying, which requires me to do some shuffling with the hardware I
have. This complicates things so it hasn't happened yet (and the remaining
space on the current system is not critically low, so I'm slacking).

The ZFS disks are encrypted through LUKS. While zfs added support for
encryption, I wasn't sure about the details. I'm used to LUKS so this was the
easier path.

As mentioned in the manicouagan part, this machine is now the one fetching the
backups from the other machines and uploading them to the Cloud™.

With the previous setup, my backups were at risk of deletion. Let's say someone
broke into my database server. They could rm -rf the backups. Then my server
would "synchronize" the directory, which would delete everything. Then it would
"synchronize" with the Cloud™, which would remove the data there as well. The
attacker could then rm the data, or encrypt it for a ransom, and there would be
nothing I could do.

Now, I'm taking zfs snapshots every hour. If the backups directory on the
server disappears, rsync will remove it on zfs1 as well. But I will still have
the data in the snapshots.

I had been reluctant to get a NAS because I thought the machine would do
nothing most of the time. With this machine, it's clearly the case.

## [That's it for now](#end) {: #end }

As I said in the introduction, there were no major changes. This is not a
surprise since this setup works well.
