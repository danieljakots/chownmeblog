Title: Routing traffic with multiple OpenVPN
Date: 2017-11-21
Category: Tech


## [Why OpenVPN?](#openvpn) {: #openvpn }

For [my dayjob](https://evolix.ca/en) we access the servers we manage
through OpenVPN. Of course it's not the only security measure, it's
yet another layer and it helps to cut a part of the
[IBN](https://en.wikipedia.org/wiki/Internet_background_noise). All of
our servers are registered in
[LDAP](https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol)
and from this system we create some routes that the OpenVPN server
pushes to the OpenVPN clients.

## [What did I need?](#needs) {: #needs }

### [Follow the pushed routes, not always and not for all the hosts](#pushedroutes) {: #pushedroutes }

I work sometimes from home (for on-call or just remote work). I have a
IP phone which needs the VPN but of course I can't setup OpenVPN on
the phone directly, so the VPN has to go on my router. But let's say
some android phone (without security updates) connects to my wifi, I
don't want its traffic to go through the VPN.

But I also have my own desktop that I don't want any of its traffic to
go through the VPN, but sometimes I want it to use the routes if I
want to quickly check something on a server.

### [Default route sometimes, sometimes not](#default) {: #default }

By default, clients don't set the gateway to the vpn, because we
have the routes. But sometimes, we need to access a host through the
VPN without having a route to it being pushed by the server. Hence I
need to be able to route all the traffic through the vpn if
needed. But not always because the vpn endpoint is 105ms away and
browsing with this increased latency is obviously a bit slower.

### [Even with a default route, bypassing the VPN for some servers](#bypass) {: #bypass }

I have a VM in Montreal, 10ms away, and there's no reason that the
traffic should go through the VPN. Same goes for my OpenBSD mirror.

### [Multiple VPN](#multiplevpns) {: #multiplevpns }

I also have another VPN which endpoints is in Montreal and I may want
to route some host from my lan through it. It must independant from
the other VPN.

### [Don't touch the server side](#serveragnosticism) {: #serveragnoticism }

My coworkers use the VPN as well so I can't change the server
configuration just to suit my own need.

## [Suiting all the needs \o/](#suitneeds) {: #suitneeds }

I will only talk about the client as there's nothing special on the
server side

### [OpenVPN infrastructure](#ovpninfra) {: #ovpninfra }

~~~
danj@pancake:/etc/openvpn$ ls
client-ca.conf  client-fr.conf  private-stuff/
~~~

Config files are as usual, the only special thing is that I force
the tun device used by the VPN (so I can use it in pf.conf):

~~~
danj@pancake:/etc/openvpn$ grep dev *.conf
client-ca.conf:dev tun1
client-fr.conf:dev tun0
~~~

In `rc.conf.local`, I set the correct config file:

~~~
openvpn_fr_flags="--config /etc/openvpn/client-fr.conf"
openvpn_ca_flags="--config /etc/openvpn/client-ca.conf"
~~~

now I can `rcctl start openvpn_fr` and `rcctl start openvpn_ca`

### [routing](#routing) {: #routing }

Spoiler alert, everything is done with pf.

I won't put my whole pf.conf but only the needed parts. First let's
describe the interface.

~~~
vpnfr_if = "tun0"
vpnca_if = "tun1"
~~~

I have vlan-capable switch and wifi AP, so I have multiple networks.

~~~
lan_net = $lan_if:network
wifilap_net = $wifilap_if:network
wifitel_net = $wifitel_if:network
windows_net = $windows_if:network
tel_net = $tel_if:network
~~~

I need some tables (don't worry, you'll understand later what purpose
they have).

~~~
table <softvpnfr> { 10.20.20.20 } persist
table <vpnfr> { $phone } persist
table <vpnca> { 10.10.10.60 } persist
table <bypassfr> { 129.128.197.20, 129.128.5.191, 185.19.29.62, 167.114.216.84 } persist
table <forcevpnfr> { $mrs-fw2 }
table <nousautres> { 10.0.0.0/8, $home_ip } persist
~~~

Now we can see the ruleset. I let everything from the lan, that doesn't
go on the router itself or to another lan (so the traffic will need
another rules to be allowed) come through.

~~~
pass in     on $lan_if     from $lan_net     to ! <nousautres>
pass in     on $wifilap_if from $wifilap_net to ! <nousautres>
pass in     on $wifitel_if from $wifitel_net to ! <nousautres>
pass in     on $tel_if     from $tel         to ! <nousautres>
pass in log on $windows_if proto { tcp, udp } from $windows_net to ! <nousautres>
~~~

I let everything going out

~~~
pass out log on $ext_if proto { tcp, udp } all modulate state
pass out on $vpnfr_if proto { tcp, udp } all modulate state
pass out on $vpnca_if proto { tcp, udp } all modulate state
~~~

Now's the fun part.

* `<softvpn>` is the hosts that can you the routes pushed by the VPN but
it doesn't use the VPN as the gw
* `<vpnfr>` and `<vpnca>` everything from the hosts in it goes through
the VPN (French or Canadian)
* `<bypassfr>` any traffic to host in the table won't go through the VPN
* `<forcevpnfr>` host that must be accessed through the VPN


~~~
# disable the use of the routes if you're not in <softvpn>
pass in on { $lan_if, $wifilap_if, $wifitel_if, $atlas_if } \
     from !<softvpnfr> to ! <nousautres>  route-to ($ext_if $home_ip)

# force traffic through the French VPN
pass in on { $lan_if, $wifilap_if, $wifitel_if, $tel_if } \
     from <vpnfr> to ! <nousautres> route-to ($vpnfr_if 192.168.125.61)

# traffic to hosts in <bypass> must not go through the VPN
pass in on { $lan_if, $wifilap_if, $wifitel_if, $tel_if } \
     from <vpnfr> to <bypassfr> route-to ($ext_if $home_ip)

# force traffic through the Canadian VPN
pass in on { $lan_if, $wifilap_if, $wifitel_if, $tel_if } \
     from <vpnca> to ! <nousautres> route-to ($vpnca_if 192.168.251.10)

# traffic from <softvpnfr> to hosts in <forcevpnfr> should really go through the VPN
pass in on { $lan_if, $wifilap_if, $wifitel_if } \
     from <softvpnfr> to <forcevpnfr> route-to ($vpnfr_if 192.168.125.61)

~~~

But the real magic with pf, is that I can **very easily** change the
routing for any host :

~~~
# if I want everything to go through the Canadian VPN
root@pancake:~# pfctl -t vpnca -Ta 10.1.2.3
# or not
root@pancake:~# pfctl -t vpnca -Td 10.1.2.3
# through the French VPN
root@pancake:~# pfctl -t vpnfr -Ta 10.1.2.3
# ok not everything, just use the route pushed by the VPN
root@pancake:~# pfctl -t vpnfr -Td 10.1.2.3
root@pancake:~# pfctl -t softvpn -Ta 10.1.2.3
~~~

That's all! Of course, if anything goes wrong, I have
[Jean Canard's Advanced Paws System (APS)](https://static.chown.me/pub/iota/pics/IMG_0551.JPG)
that checks for anything.
