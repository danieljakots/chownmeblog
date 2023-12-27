Title: Upgrading OpenBSD with Ansible
Date: 2018-10-19
Category: Tech

This article is best enjoyed with basic knowledge of [OpenBSD
autoinstall](https://man.openbsd.org/autoinstall) and [Ansible](https://www.ansible.com/)

## [My router runs OpenBSD -current](#router) {: #router }

A few months ago, I needed software that had just hit the ports tree. I didn't
want to wait for the next release, so I upgraded my router to use -current.
Since then, I've continued running -current, which means upgrading to a newer
snapshot every so often. Running -current is great, but the process of updating
to a newer snapshot was cumbersome.  Initially, I had to plug in a serial cable
and then reboot into *bsd.rd*, hit enter ten times, then reboot, run `sysmerge`
and update packages.

I eventually switched to [upobsd](https://github.com/semarie/upobsd) to be
able to upgrade without the need for a serial connection. The process was
better, but still tiresome. Usually, I would prepare the special version of
*bsd.rd*, boot on *bsd.rd*, and do something like wash the dishes in the
meantime. After about ten minutes, I would dry my hands and then go back to my
workstation to see whether the *bsd.rd* part had finished so I could run
`sysmerge` and `pkg_add`, and then return to the dishes while it upgraded
packages.

Out of laziness, I thought: "I should automate this," but what happened instead
is that I simply didn't upgrade that machine very often. (Yes, laziness).  With
my router out of commission, life is very dull, because it is my gateway to the
Internet. Even services hosted at my place (like my Mastodon instance) are not
reachable when the router is down because I use multiple VLANs (so I need the
router to *jump* across VLANs).

## [Ansible Reboot Module](#ansiblereboot) {: #ansiblereboot }

I recently got a new job, and one of my first tasks was auditing the *Ansible*
roles written by my predecessors. In one role, the machine rebooted and they
used the
[*wait_for_connection*](https://docs.ansible.com/ansible/2.5/modules/wait_for_module.html)
module to wait for it to come back up. That sounded quite hackish to me, so out
of curiosity, I tried to determine whether there was a better way. I also
thought I might be able to use something similar to further automate my OpenBSD
upgrades, and wanted to assess the cleanliness of this method. ;-)

I learned that with the then-upcoming 2.7 Ansible release, a proper *reboot*
module would be included. I went to the docs, which stated that for a certain
parameter:

~~~
- On Linux and macOS, this is converted to minutes and
  rounded down. If less than 60, it will be set to 0.
- On Solaris and FreeBSD, this will be seconds.
~~~

I took this to mean that there was no support for OpenBSD. I looked at the code
and, indeed, there was not. However, I believed that it wouldn't be too hard
to add it. I added the missing pieces for OpenBSD, tested it on my poor Pine64
and then submitted it upstream. After a quick back and forth, the module's
author [merged it into
devel](https://github.com/ansible/ansible/commit/2769a4e2cc3aadbf91e7f4f83ef57b7ebe43442a)
(having a friend working at Red Hat helped the process, merci Cyril !) A couple
days later, the release engineer [merged it into
stable-2.7](https://github.com/ansible/ansible/commit/26de4f97493adeb388c1c8fad7a266bb7652bac6).

I proceeded to actually write the playbook, and then I hit a bug. The parameter
*reboot_timeout* was not recognized by Ansible. This feature would definitely
be useful on a slow machine (such as the Pine64 and its dying SD card). Again,
my fix was [merged into
master](https://github.com/ansible/ansible/commit/0105b4aeadb94dd12b921ed6c427b21cd31182fa)
by the module's author and then [merged into
stable-2.7](https://github.com/ansible/ansible/commit/a0f38bdab5ae0e183cb960fe9e964bf1edf7c326).
2.7.1 will be the first release to feature these fixes, but if you use OpenBSD
-current, you already have access to them. I backported the patches when I
[updated
ansible](https://marc.info/?l=openbsd-ports-cvs&m=153994960724056&w=2).

Fun fact about Ansible and reboots: "The win_reboot module was [...] included
with Ansible 2.1," while for unix systems it wasn't added until 2.7. :D For
more details, you can read the [module's author blog
article](http://samdoran.com/ansible-reboot-plugin/).

## [The Playbook](#playbook) {: #playbook }

Initially, my playbook did the upgrade as usual (i.e., it fetched the sets in
*bsd.rd*). During this process, of course, my machine is not performing its
function as a router. My Internet access is not super great, so fetching the
sets takes awhile. I got frustrated while I was testing it and looked into
lessening the amount of time spent inside *bsd.rd*.

To speed up the process, I wrote [a basic shell
shttps://chown.me/iota/cript](https://static.chown.me/pub/iota/blog/fetch-sets) to fetch the sets **before**
rebooting into *bsd.rd*. It enabled me to remove some *tasks* I had to do in
order to get working Internet access in *bsd.rd*. (This is specific to my
case).

### [The playbook itself](#playbookitself) {: #playbookitself }

~~~
---
- name: Upgrade OpenBSD
  hosts: apu-root
  vars:
    arch: amd64
    date: "{{ lookup('pipe', 'date +%Y-%m-%d') }}"
    disk: "sd0"
    mirror: "fastly.cdn.openbsd.org"
    path_sets: "/home/danj/sets"

  tasks:
    - name: fetch sets
      command: /home/danj/bin/fetch-sets
      when: path_sets is defined
    - name: create answer file for upobsd
      template:
        src: answer.j2
        dest: answer
      delegate_to: localhost
    - name: create kernel with upobsd
      command: "upobsd -v -a {{ arch }} -u ./answer -m https://{{ mirror }}/pub/OpenBSD -V snapshots"
      delegate_to: localhost
    - name: copy bsd.rd created by upobsd
      copy:
        src: bsd.rd
        dest: /bsd
    - name: reboot host
      reboot:
        msg: "rebooting into bsd.rd to upgrade"
        reboot_timeout: 900
    - name: archive kernel
      copy:
        src: "/bsd"
        dest: "/bsd-{{ date }}"
        mode: 0700
        remote_src: "yes"
    - name: upgrade all packages
      command: "pkg_add -u -Dsnap"
~~~

### [The answer file](#answerfile) {: #answerfile }

The answer file is automatically [mailed to root at the end of the
upgrade](https://github.com/openbsd/src/blob/master/distrib/miniroot/install.sub#L2811-L2812),
so it's easy to get it!

In my case, the answer file transformed into a jinja2 template is:

~~~
Which disk is the root disk = sd0
Force checking of clean non-root filesystems = no
{% if path_sets is defined %}
Location of sets = disk
Is the disk partition already mounted = yes
Pathname to the sets = {{ path_sets }}
{% else %}
Location of sets = http
HTTP proxy URL = none
HTTP Server = {{ mirror }}
Server directory = pub/OpenBSD/snapshots/{{ arch }}
{% endif %}
Set name(s) = done
Location of sets = done
~~~

### [The explanations](#explanations) {: #explanations }

Ansible runs my script on the remote host to fetch the sets. It creates an
answer file from the template and then gives it to *upobsd*. Once *upobsd* has
created the kernel, Ansible copies it in place of `/bsd` on the host. The
router reboots and boots on `/bsd`, which is upobsd's *bsd.rd*. The *installer*
runs in *auto_update* mode. Once it comes back from *bsd.rd* land, it archives
the kernel and finishes by upgrading all the packages.

It also supports upgrading without fetching the sets ahead of time. For
instance, I upgrade this way on my Pine64 because if I cared about speed, I
wouldn't use this weak computer with its dying SD card. For this case, I just
comment out the *path_sets* variable and Ansible instead creates an answer file
that will instruct the installer to fetch the sets from the designated mirror.

I've been archiving my kernels for a few years. It's a nice way to <strike>fill
up /</strike> keep a history of my upgrades. If I spot a regression, I can
try a previous kernel ... which may not work with the then-desynchronized
*userland*, but that's another story.

`sysmerge` already runs with
[rc.sysmerge](https://github.com/openbsd/src/blob/master/etc/rc#L579-L580) in
batch mode and sends the result by email. I don't think there's merit to
running it again in the playbook. The only perk would be discovering **in the
terminal** whether any files need to be manually merged, rather than reading
exactly the same output in the email.

Initially, I used the *openbsd_pkg* module, but it doesn't work on -current
just **before** a release because `pkg_add` automatically looks for
*pub/OpenBSD/${release}/packages/${arch}* (which is empty). I wrote and tested
this playbook while 6.4 was around the corner, so I switched to *command* to be
able to pass the `-Dsnap` parameter.

## [The result](#result) {: #result }

I'm very happy with the playbook! It performs the upgrade with as little
intervention as possible and minimal downtime. \o/

<br/>

*Thanks [Pamela](https://bsd.network/@pamela) for the proof-reading!*

