Title: Locking OpenBSD when it's sleeping
Date: 2018-10-08
Category: Tech

I frequent the #openbsd IRC channel in order to help people. A question
commonly asked is how to automatically lock your machine when
putting it to sleep with zzz(1). I answered this question in a
previous article (which was actually written four years ago; time flies!) but
it was written in French, so here's a new one, also covering additional related topics.

## [Locking the machine when it is put to sleep](#locking) {: #locking }

If you read [apmd(8)](https://man.openbsd.org/apmd.8):

~~~
FILES
     /etc/apm/suspend
     /etc/apm/hibernate
     /etc/apm/standby
     /etc/apm/resume
     /etc/apm/powerup
     /etc/apm/powerdown    These files contain the host's customized actions.
                           Each file must be an executable binary or shell
                           script.  A single program or script can be used to
                           control all transitions by examining the name by
                           which it was called, which is one of suspend,
                           hibernate, standby, resume, powerup, or powerdown.
~~~

The trick is to write a script for 'etc/apm/suspend' to run when zzz is called
(either directly or by [closing the
lid](https://github.com/openbsd/src/blob/master/etc/etc.amd64/sysctl.conf#L3)).
For instance, the script I'm using is:

~~~
#!/bin/sh
doas -u danj env DISPLAY=:0 XAUTHORITY=/home/danj/.Xauthority xlock &
~~~

It requires:

- configuring doas, *left as an exercise to the reader* ;)
- running apmd (hashtag rcctl)
- an executable script

## [Locking it further](#lockingfurther) {: #lockingfurther }

This is off to a good start, but if you are a *startx* user (versus using xenodm), be sure to run `exec startx` and not just `startx`. Otherwise, it is possible to kill X and then access the shell.

If you don't set a maximum lifetime for your `ssh-agent`, you should clear your identities using `ssh-add -D`. You should also revoke any `sudo` permissions with `sudo -K`. `doas` doesn't work the same way, so `doas -L` won't help you much. (You have elevated permissions only in the current shell, not account-wide).

You might want to clear your clipboards, as well. Use something like: `xsel -c -p; xsel -c -s; xsel -c -b`.

Of course, if you use other authentication mechanisms (GNOME keyring, ssh's
Control\*, etc.), you should handle those as well.

## [Beware of the cat](#cat) {: #cat }

Now that I have a [Captive Advanced
Threat](https://awoo.chown.me/@jeancanard), I feel the need to automatically lock the screen after it has been idle for a short while. You can achieve this using `xidle`. The [man
page](https://man.openbsd.org/xidle.1) is sufficiently descriptive that I won't talk about that further.


<br/>

*Thanks [semarie](https://maly.io/@semarie) for the technical proof-reading and [Pamela](https://bsd.network/@pamela) for the English proof-reading!*
