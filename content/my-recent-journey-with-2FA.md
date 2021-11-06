Title: My recent journey with 2FA
Date: 2017-02-26
Category: Tech

## [2FA](#2FA) {: #2FA }

Of course by 2FA I mean
[two-factor authentication](https://en.wikipedia.org/wiki/Multi-factor_authentication).

I've been using that for a long time for ssh with
[my yubikey on OpenBSD](./yubikey-en.html) but I've never enabled 2FA
on the online services I use. The main reason for not doing it before was
that I thought that my phone had to play a central role (which in fact
is not much the case). While it's the most critical device I have, my
phone is the device I trust the least.

However, yesterday I saw a comment on lobste.rs asking about
[how to use TOTP on OpenBSD](https://lobste.rs/s/1cyltz/two_factor_authentication_now_available/comments/a9xvvg#c_a9xvvg).
In addition to that, I guess seeing
[what happened to cloudflare](https://blog.cloudflare.com/incident-report-on-memory-leak-caused-by-cloudflare-parser-bug/)
and everything what's happening if you want to cross the US border
made me more interested in 2FA than before.

So I began to look into how it works.

## [How it works](#how) {: #how }

The concept of 2FA is that you may lose your password (or your ssh
key) and in that case the person who takes control of it can
successfully impersonate you. The goal is that a login system will
require something else to verify that it's really you.

One way to achieve this is to use SMS but that sucks: [circumventing it
is not even restricted to Nation State Actors](http://www.baltimoresun.com/features/baltimore-insider-blog/bal-black-lives-matter-activist-deray-mckesson-s-twitter-hacked-friday-morning-20160610-story.html).

Another can be something biometric but then users need to access to a
scanner which is quite impractical in every day life. Even if iPhones
have a fingerprint reader, it's not usable by third parties.

It must be something that keeps changing otherwise it's both
subject to replay attack and it's just another password.

Here comes the OTP.

## [One Time Password](#OTP) {: #OTP }

One Time Password was defined in
[RFC2289](https://tools.ietf.org/html/rfc2289) (which is quite old:
February 1998). Then they made HOTP (H is for *HMAC-Based*) in
[RFC4226](https://tools.ietf.org/html/rfc4226) and finally the TOTP (T
is for *Time-Based*) in [RFC](https://tools.ietf.org/html/rfc6238)
which is an extension of the HOTP to support the time-based moving
factor.

To understand in more details you can either read in the RFC4226
[5.4.  Example of HOTP Computation for Digit = 6](https://tools.ietf.org/html/rfc4226#page-7)
and then the short RFC6238 or you can just read this [random blog
article on the Internet which explains clearly the same thing](https://pthree.org/2014/04/15/time-based-one-time-passwords-how-it-works/).

### [tl;dr](#tldr) {: #tldr }

There's a secret shared and then you compute the HMAC-SHA1 of the
shared secret and epoch.

### [Wait, did you just say sha1?!?1?](#sha1) {: #sha1 }

Even if there's now a sha1 collision, it's not really a problem. To
quote Schneier: "[collision] pretty much puts a bullet into
SHA-1 as a hash function for digital signatures (although it doesn't
affect applications such as HMAC where collisions aren't important)."
([source](https://www.schneier.com/blog/archives/2005/02/sha1_broken.html))

And for a more complete answer, see this
[answer](http://crypto.stackexchange.com/questions/26510/why-is-hmac-sha1-still-considered-secure).

## [How to use it](#howuse) {: #howuse }

### [Don't be locked out](#lockedout) {: #lockedout }

I wanted to use my phone (something distinct that my computer to
compartment things a bit). Obviously the goal is to secure your
account without losing it so that means that losing your phone
shouldn't prevent you to retrieve access to your accounts. Unusable
security is unusable.

If you read about 2FA, you'll see that some services that provide it,
give you some backup code to not to be locked out. But I don't want to
locked out from services don't provide backup codes either.

So my phone must not be a single point of failure.

We saw earlier that {T,H}OTP are based on a shared secret so let's
backup it.

### [Backuping shared secrets and backup codes](#backups) {: #backups }

For my regular passwords, I use keepassx which is shared/backuped across my
different computers. I created another database to store those. Of
course you shouldn't use the same database to keep your passwords and the
other secrets in case of you leak one of the two database's password.

### [Clients](#clients) {: #clients }

#### [Android phone](#android) {: #android }

Now that I'm ready to activate 2FA, let's see how to use it. The plan
is to use my android phone. On the
[Time-based One-time Password Algorithm Wikipedia page](https://en.wikipedia.org/wiki/Time-based_One-time_Password_Algorithm)
there was a list of clients but sadly it was deleted.
You can still find it
[in the history](https://en.wikipedia.org/w/index.php?title=Time-based_One-time_Password_Algorithm&oldid=724156353#Client_implementations).

I wanted a FOSS application and Google Authenticator is now closed
source so I went with FreeOTP which is not completely dead compared to
others (but it's not thriving either), so far it works good.

#### [OpenBSD](#OpenBSD) {: #OpenBSD }

In the case I don't have a phone, I still want to be able to
log in my different accounts. In the lobste.rs' link that I gave at the
beginning of this article, someone mentioned oath-toolkit which works
very easily:

    $ oathtool --totp -b deafcafe
	405723

(with deafcafe being the shared secret).

## [Activating it](#activation) {: #activation }

Now that we're ready to use it, let's do it. So where to activate
it? Actually, there's [a cool site](https://2fa.directory/) that
lists services that provide or not (and then you can shame them on
twitter) 2FA with a link to the service's documentation.

### [My Feedback](#feedback) {: #feedback }

So far I activated 2FA on about half a dozen of website. The first one was
the [RIPE NCC](https://www.ripe.net/) (if you don't want people to
steal your precious IP addresses and/or your atlas credit) and it was
actually a good one to try it.

To activate it usually the website gives you a qrcode which is in fact
just a URL looking like:

    otpauth://totp/Example:foo@example.com?secret=DEAFCAFE&issuer=Example

which is fine for my phone but sadly my eyes can't decode qrcode and I
need the shared secret to put it my keepassx. Most of the time
websites gives you by default the qrcode but also gives you the
possibility to access the shared secret.

For now, everything works fine, I use my phone to unlock my different
accounts and if anything happens to it, I can just unlock my second
keepassx database and use oathtool (or use a backup code) to get my
account back.
