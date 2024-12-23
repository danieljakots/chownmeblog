Title: Synchronizing TLS certificates across machines
Date: 2024-12-23
Category: Tech

A while ago, I had the need to synchronize certificates across machines. I was
able to answer it using a perhaps uncommon trick which I thought might be worth
sharing.

Let's say you have one domain for which you want multiple machines answering
requests. Of course, you choose to provide that service over TLS (doesn't
matter whether it's http or another layer 7 protocol).

As usual, the first step is to create a private key and then obtain a
certificate either directly on that machine with the [ACME
protocol](https://en.wikipedia.org/wiki/Automatic_Certificate_Management_Environment),
or while jumping through hoops with a legacy certificate authority. All is
well, but you didn't accomplish the goal of having that service provided by
multiple machines.

So you copy the key and the certificates (plural since you most likely have an
intermediate certificate). Now that goal is accomplished until you have to
renew the certificate.

If you use a legacy certificate authority, it might work for a long time (if I
understand correctly the [CA/Brower forum
FAQ](https://cabforum.org/working-groups/server/baseline-requirements/faq/),
39 months is the longest available right now). If you use Let's Encrypt (or any
other alternative I assume), currently the certificate you'll receive is valid
for 90 days. However, they're now talking about providing certificates with a
[6-day validity period](https://letsencrypt.org/2024/12/11/eoy-letter-2024/).

Of course, with such a constraint, automating the certificate renewal is
unavoidable. Proving to the validation server that you control the domain for
which you have the certificate, while running the service on multiple machines
is not necessarily trivial, but this is outside the scope of this article.

Let's say you route the `.well-known/acme-challenge` path to a particular
machine, which will run your favourite ACME client (this obviously assumes you
use the `HTTP-01` [challenge](https://letsencrypt.org/docs/challenge-types/)).
Now you have a renewed certificate on one machine, but how do you synchronize
it with your other machines? By the way, I say certificate, but I should actually
use plural as the intermediate certificate changes from time to time. (Your
private key isn't likely to change unless you fucked something up — don't
worry, we all do).

There are a couple of ways to synchronize the certificates across the fleet:

* by hand, but it's error-prone, time-consuming, and boring.
* automated through rsync/scp, but it requires ssh access which may not end up being [the best thing](https://en.wikipedia.org/wiki/Lateral_movement_(cybersecurity))

So what's a better way to solve that? Well, [the certificates are actually sent
by the server during the negotiation
phase](https://en.wikipedia.org/wiki/Transport_Layer_Security#Basic_TLS_handshake)
(so you can validate it). You don't actually need any privileged access, you can
just do a basic TCP connection, followed by a TLS handshake.

When I wanted to do that, I attempted to use the `openssl(1)` command line
tool. After suffering a while because of its poor UX, I thought it would be less
frustrating and even funnier to actually write some code to do that.

The code is available on
[github](https://github.com/danieljakots/getCertificates). Basically you tell
the tool how to connect with TCP to the machine with the new certificates
(likely by specifying its IP since the DNS name is spread over the multiple
machines), and it writes down the certificates it got.

To be honest, I don't run it anymore as I stopped running my website over
multiple machines. I had it in my crontab for as long as I did though. Reading
the Let's Encrypt announcement about short-lived certificates reminded me about
this tool so I thought I would share it.
