# Introduction

Network Address Translation is an Internet standard that allows hosts on local area networks to use one set of IP addresses for internal communications and another set of IP addresses for external communications. A LAN that uses NAT is ascribed as a _natted_ network. For NAT to function, there should be a NAT gateway in each _natted_ network. The NAT gateway (NAT router) performs IP address rewriting on the way packet travel from/to LAN.

Nat matches only the first packet of the connection, connection tracking remembers the action and performs on all other packets belonging to the same connection.

Whenever NAT rules are changed or added, the connection tracking table should be cleared otherwise NAT rules may seem to be not functioning correctly until connection entry expires.

## Types of NAT:

![](https://help.mikrotik.com/docs/download/attachments/3211299/nats.png?version=2&modificationDate=1644848864680&api=v2)

-   **source NAT or srcnat.** This type of NAT is performed on packets that are originated from a natted network. A NAT router replaces the private source address of an IP packet with a new public IP address as it travels through the router. A reverse operation is applied to the reply packets traveling in the other direction.
-   **destination NAT or dstnat.** This type of NAT is performed on packets that are destined for the natted network. It is most commonly used to make hosts on a private network to be accessible from the Internet. A NAT router performing dstnat replaces the destination IP address of an IP packet as it travels through the router towards a private network.

Since RouterOS v7 the firewall NAT has two new _INPUT_ and _OUTPUT_ chains which are traversed for packets delivered to and sent from applications running on the local machine:

-   **input** \- used to process packets entering the router through one of the interfaces with the destination IP address which is one of the router's addresses. Packets passing through the router are not processed against the rules of the input chain.
-   **output** \- used to process packets that originated from the router and leave it through one of the interfaces. Packets passing through the router are not processed against the rules of the output chain.

### Destination NAT

![](https://help.mikrotik.com/docs/download/attachments/3211299/NAT-setup.jpg?version=3&modificationDate=1572338061900&api=v2)

Network address translation works by modifying network address information in the packets IP header. Let\`s take a look at the common setup where a network administrator wants to access an office server from the internet.

We want to allow connections from the internet to the office server whose local IP is 10.0.0.3. In this case, we have to configure a destination address translation rule on the office gateway router:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall nat </code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=dstnat</code> <code class="ros value">action</code><code class="ros plain">=dst-nat</code> <code class="ros value">dst-address</code><code class="ros plain">=172.16.16.1</code> <code class="ros value">dst-port</code><code class="ros plain">=22</code> <code class="ros value">to-addresses</code><code class="ros plain">=10.0.0.3</code> <code class="ros value">protocol</code><code class="ros plain">=tcp</code></div></div></td></tr></tbody></table>

The rule above translates: when an incoming connection requests TCP port 22 with destination address 172.16.16.1, use the _dst-nat_ action and depart packets to the device with local IP address 10.0.0.3 and port 22.

To allow access only from the PC at home, we can improve our _dst-nat_ rule with _"src-address=192.168.88.1"_ which is a Home\`s PC public (this example) IP address. It is also considered to be more secure!

### Source NAT

If you want to hide your local devices behind your public IP address received from ISP, you should configure the source network address translation (masquerading) feature of the MikroTik router.   
Let\`s assume you want to hide both office computer and server behind the public IP 172.16.16.1, the rule will look like the following one:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall nat </code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">src-address</code><code class="ros plain">=10.0.0.0/24</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">to-addresses</code><code class="ros plain">=172.16.16.1</code> <code class="ros value">out-interface</code><code class="ros plain">=WAN</code></div></div></td></tr></tbody></table>

Now your ISP will see all the requests coming with IP 172.16.16.1 and they will not see your LAN network IP addresses.

#### Masquerade

Firewall NAT _action=masquerade_ is a unique subversion of _action=srcnat,_ it was designed for specific use in situations when public IP can randomly change, for example, DHCP server change assigned IP or PPPoE tunnel after disconnect gets different IP, in short - **when public IP is dynamic**.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall nat </code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">src-address</code><code class="ros plain">=10.0.0.0/24</code> <code class="ros value">action</code><code class="ros plain">=masquarade</code> <code class="ros value">out-interface</code><code class="ros plain">=WAN</code></div></div></td></tr></tbody></table>

Every time when interface disconnects and/or its IP address changes, the router will clear all masqueraded connection tracking entries related to the interface, this way improving system recovery time after public IP change. If _srcnat_ is used instead of _masquerade,_ connection tracking entries remain and connections can simply resume after a link failure.

Unfortunately, this can lead to some issues with unstable links when the connection gets routed over different links after the primary link goes down. In such a scenario following things can happen:

-   on disconnect, all related connection tracking entries are purged;
-   next packet from every purged (previously masqueraded) connection will come into the firewall as _new_, and, if a primary interface is not back, a packet will be routed out via an alternative route (if you have any) thus creating a new masqueraded connection;
-   the primary link comes back, routing is restored over the primary link, so packets that belong to existing connections are sent over the primary interface without being masqueraded, that way leaking local IPs to a public network.

To work around this situation **blackhole** route can be created as an alternative to the route that might disappear on disconnect.

Hosts behind a NAT-enabled router do not have true end-to-end connectivity. Therefore some Internet protocols might not work in scenarios with NAT. Services that require the initiation of TCP connection from outside the private network or stateless protocols such as UDP, can be disrupted. 

To overcome these limitations RouterOS includes a number of so-called NAT helpers, that enable NAT traversal for various protocols. When _action=srcnat_ is used instead, connection tracking entries remain and connections can simply resume.

Though Source NAT and masquerading perform the same fundamental function: mapping one address space into another one, the details differ slightly. Most noticeably, masquerading chooses the source IP address for the outbound packet from the IP bound to the interface through which the packet will exit.

#### CGNAT (NAT444)

![](https://help.mikrotik.com/docs/download/attachments/3211299/Cgnat.png?version=1&modificationDate=1630400169782&api=v2)

To combat IPv4 address exhaustion, a new RFC 6598 was deployed. The idea is to use shared 100.64.0.0/10 address space inside the carrier's network and perform NAT on the carrier's edge router to a single public IP or public IP range.

Because of the nature of such setup, it is also called NAT444, as opposed to a NAT44 network for a 'normal' NAT environment, three different IPv4 address spaces are involved.

CGNAT configuration on RouterOS does not differ from any other regular source NAT configuration:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall nat</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=src-nat</code> <code class="ros value">action</code><code class="ros plain">=srcnat</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.0.0/10</code> <code class="ros value">to-address</code><code class="ros plain">=2.2.2.2</code> <code class="ros value">out-interface</code><code class="ros plain">=&lt;</code><code class="ros plain">;public_if&gt;</code></div></div></td></tr></tbody></table>

Where:

-   2.2.2.2 - public IP address,
-   public\_if - interface on providers edge router connected to the internet

The advantage of NAT444 is obvious, fewer public IPv4 addresses are used. But this technique comes with major drawbacks:

-   The service provider router performing CGNAT needs to maintain a state table for all the address translations: this requires a lot of memory and CPU resources.
-   Console gaming problems. Some games fail when two subscribers using the same outside public IPv4 address try to connect to each other.
-   Tracking users for legal reasons means extra logging, as multiple households go behind one public address.
-   Anything requiring incoming connections is broken. While this already was the case with regular NAT, end-users could usually still set up port forwarding on their NAT router. CGNAT makes this impossible. This means no web servers can be hosted here, and IP Phones cannot receive incoming calls by default either.
-   Some web servers only allow a maximum number of connections from the same public IP address, as a means to counter DoS attacks like SYN floods. Using CGNAT this limit is reached more often and some services may be of poor quality.
-   6to4 requires globally reachable addresses and will not work in networks that employ addresses with a limited topological span.

  

Packets with Shared Address Space source or destination addresses MUST NOT be forwarded across Service Provider boundaries. Service Providers MUST filter such packets on ingress links. In RouterOS this can be easily done with firewall filters on edge routers:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall filter</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.0.0/10</code> <code class="ros value">action</code><code class="ros plain">=drop</code> <code class="ros value">in-interface</code><code class="ros plain">=&lt;</code><code class="ros plain">;public_if&gt;</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=output</code> <code class="ros value">dst-address</code><code class="ros plain">=100.64.0.0/10</code> <code class="ros value">action</code><code class="ros plain">=drop</code> <code class="ros value">out-interface</code><code class="ros plain">=&lt;</code><code class="ros plain">;public_if&gt;</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.0.0/10</code> <code class="ros value">action</code><code class="ros plain">=drop</code> <code class="ros value">in-interface</code><code class="ros plain">=&lt;</code><code class="ros plain">;public_if&gt;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.0.0/10</code> <code class="ros value">action</code><code class="ros plain">=drop</code> <code class="ros value">out-interface</code><code class="ros plain">=&lt;</code><code class="ros plain">;public_if&gt;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">dst-address</code><code class="ros plain">=100.64.0.0/10</code> <code class="ros value">action</code><code class="ros plain">=drop</code> <code class="ros value">out-interface</code><code class="ros plain">=&lt;</code><code class="ros plain">;public_if&gt;</code></div></div></td></tr></tbody></table>

Service providers may be required to log of MAPed addresses, in a large CGN deployed network that may be a problem. Fortunately, RFC 7422 suggests a way to manage CGN translations in such a way as to significantly reduce the amount of logging required while providing traceability for abuse response.

RFC states that instead of logging each connection, CGNs could deterministically map customer private addresses (received on the customer-facing interface of the CGN, a.k.a., internal side) to public addresses extended with port ranges.

In RouterOS described algorithm can be done with few script functions. Let's take an example:

<table class="wrapped confluenceTable" style="text-align: left;" resolved=""><colgroup><col><col></colgroup><tbody><tr><td class="confluenceTd"><strong>Inside IP</strong></td><td class="confluenceTd"><strong>Outside IP/Port range</strong></td></tr><tr><td class="confluenceTd">100.64.1.1</td><td class="confluenceTd">2.2.2.2:2000-2099</td></tr><tr><td class="confluenceTd">100.64.1.2</td><td class="confluenceTd">2.2.2.2:2100-2199</td></tr><tr><td class="confluenceTd">100.64.1.3</td><td class="confluenceTd">2.2.2.2:2200-2299</td></tr><tr><td class="confluenceTd">100.64.1.4</td><td class="confluenceTd">2.2.2.2:2300-2399</td></tr><tr><td class="confluenceTd">100.64.1.5</td><td class="confluenceTd">2.2.2.2:2400-2499</td></tr><tr><td class="confluenceTd">100.64.1.6</td><td class="confluenceTd">2.2.2.2:2500-2599</td></tr></tbody></table>

Instead of writing NAT mappings by hand, we could write a function that adds such rules automatically.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">:</code><code class="ros functions">global </code><code class="ros plain">sqrt </code><code class="ros value">do</code><code class="ros plain">=</code><code class="ros plain">{</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros constants">:</code><code class="ros functions">for </code><code class="ros plain">i </code><code class="ros value">from</code><code class="ros plain">=0</code> <code class="ros value">to</code><code class="ros plain">=$1</code> <code class="ros value">do</code><code class="ros plain">=</code><code class="ros plain">{</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros constants">:</code><code class="ros functions">if </code><code class="ros plain">(i * i &gt; </code><code class="ros keyword">$1</code><code class="ros plain">) </code><code class="ros value">do</code><code class="ros plain">=</code><code class="ros plain">{ </code><code class="ros constants">:</code><code class="ros functions">return </code><code class="ros plain">(</code><code class="ros keyword">$i</code> <code class="ros plain">- 1) }</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">}</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">}</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros constants">:</code><code class="ros functions">global </code><code class="ros plain">addNatRules </code><code class="ros value">do</code><code class="ros plain">=</code><code class="ros plain">{</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros constants">/ip firewall nat </code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">action</code><code class="ros plain">=jump</code> <code class="ros value">jump-target</code><code class="ros plain">=xxx</code> <code class="ros plain">\</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">src-address</code><code class="ros plain">=</code><code class="ros string">"$($srcStart)-$($srcStart + $count - 1)"</code></div><div class="line number10 index9 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros constants">:</code><code class="ros functions">local </code><code class="ros plain">x [</code><code class="ros keyword">$sqrt</code> <code class="ros keyword">$count</code><code class="ros plain">]</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros constants">:</code><code class="ros functions">local </code><code class="ros plain">y </code><code class="ros keyword">$x</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros constants">:</code><code class="ros functions">if </code><code class="ros plain">(</code><code class="ros keyword">$x</code> <code class="ros plain">* </code><code class="ros keyword">$x</code> <code class="ros plain">=</code> <code class="ros keyword">$count</code><code class="ros plain">) </code><code class="ros value">do</code><code class="ros plain">=</code><code class="ros plain">{ </code><code class="ros constants">:</code><code class="ros functions">set </code><code class="ros plain">y (</code><code class="ros keyword">$x</code> <code class="ros plain">+ 1) }</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros constants">:</code><code class="ros functions">for </code><code class="ros plain">i </code><code class="ros value">from</code><code class="ros plain">=0</code> <code class="ros value">to</code><code class="ros plain">=$x</code> <code class="ros value">do</code><code class="ros plain">=</code><code class="ros plain">{</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros constants">/ip firewall nat </code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=xxx</code> <code class="ros value">action</code><code class="ros plain">=jump</code> <code class="ros value">jump-target</code><code class="ros plain">=</code><code class="ros string">"xxx-$($i)"</code> <code class="ros plain">\</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">src-address</code><code class="ros plain">=</code><code class="ros string">"$($srcStart + ($x * $i))-$($srcStart + ($x * ($i + 1) - 1))"</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">}</code></div><div class="line number18 index17 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros constants">:</code><code class="ros functions">for </code><code class="ros plain">i </code><code class="ros value">from</code><code class="ros plain">=0</code> <code class="ros value">to</code><code class="ros plain">=($count</code> <code class="ros plain">- 1) </code><code class="ros value">do</code><code class="ros plain">=</code><code class="ros plain">{</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros constants">:</code><code class="ros functions">local </code><code class="ros plain">prange </code><code class="ros string">"$($portStart + ($i * $portsPerAddr))-$($portStart + (($i + 1) * $portsPerAddr) - 1)"</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros constants">/ip firewall nat </code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=</code><code class="ros string">"xxx-$($i / $x)"</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">protocol</code><code class="ros plain">=tcp</code> <code class="ros value">src-address</code><code class="ros plain">=($srcStart</code> <code class="ros plain">+ </code><code class="ros keyword">$i</code><code class="ros plain">) \</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">to-address</code><code class="ros plain">=$toAddr</code> <code class="ros value">to-ports</code><code class="ros plain">=$prange</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros constants">/ip firewall nat </code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=</code><code class="ros string">"xxx-$($i / $x)"</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">src-address</code><code class="ros plain">=($srcStart</code> <code class="ros plain">+ </code><code class="ros keyword">$i</code><code class="ros plain">) \</code></div><div class="line number24 index23 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">to-address</code><code class="ros plain">=$toAddr</code> <code class="ros value">to-ports</code><code class="ros plain">=$prange</code></div><div class="line number25 index24 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">}</code></div><div class="line number26 index25 alt1" data-bidi-marker="true"><code class="ros plain">}</code></div></div></td></tr></tbody></table>

After pasting the above script in the terminal function "addNatRules" is available. If we take our example, we need to map 6 shared network addresses to be mapped to 2.2.2.2 and each address uses a range of 100 ports starting from 2000. So we run our function:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros keyword">$addNatRules</code> <code class="ros value">count</code><code class="ros plain">=6</code> <code class="ros value">srcStart</code><code class="ros plain">=100.64.1.1</code> <code class="ros value">toAddr</code><code class="ros plain">=2.2.2.2</code> <code class="ros value">portStart</code><code class="ros plain">=2000</code> <code class="ros value">portsPerAddr</code><code class="ros plain">=100</code></div></div></td></tr></tbody></table>

Now you should be able to get a set of rules:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@rack1_b18_450] </code><code class="ros constants">/ip firewall nat&gt; </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - invalid, D - dynamic</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">action</code><code class="ros plain">=jump</code> <code class="ros value">jump-target</code><code class="ros plain">=xxx</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.1.1-100.64.1.6</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1&nbsp;&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=xxx</code> <code class="ros value">action</code><code class="ros plain">=jump</code> <code class="ros value">jump-target</code><code class="ros plain">=xxx-0</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.1.1-100.64.1.2</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">2&nbsp;&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=xxx</code> <code class="ros value">action</code><code class="ros plain">=jump</code> <code class="ros value">jump-target</code><code class="ros plain">=xxx-1</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.1.3-100.64.1.4</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">3&nbsp;&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=xxx</code> <code class="ros value">action</code><code class="ros plain">=jump</code> <code class="ros value">jump-target</code><code class="ros plain">=xxx-2</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.1.5-100.64.1.6</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number10 index9 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">4&nbsp;&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=xxx-0</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">to-addresses</code><code class="ros plain">=2.2.2.2</code> <code class="ros value">to-ports</code><code class="ros plain">=2000-2099</code> <code class="ros value">protocol</code><code class="ros plain">=tcp</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.1.1</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number12 index11 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">5&nbsp;&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=xxx-0</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">to-addresses</code><code class="ros plain">=2.2.2.2</code> <code class="ros value">to-ports</code><code class="ros plain">=2000-2099</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.1.1</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number14 index13 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">6&nbsp;&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=xxx-0</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">to-addresses</code><code class="ros plain">=2.2.2.2</code> <code class="ros value">to-ports</code><code class="ros plain">=2100-2199</code> <code class="ros value">protocol</code><code class="ros plain">=tcp</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.1.2</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number16 index15 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">7&nbsp;&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=xxx-0</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">to-addresses</code><code class="ros plain">=2.2.2.2</code> <code class="ros value">to-ports</code><code class="ros plain">=2100-2199</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.1.2</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number18 index17 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">8&nbsp;&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=xxx-1</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">to-addresses</code><code class="ros plain">=2.2.2.2</code> <code class="ros value">to-ports</code><code class="ros plain">=2200-2299</code> <code class="ros value">protocol</code><code class="ros plain">=tcp</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.1.3</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number20 index19 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">9&nbsp;&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=xxx-1</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">to-addresses</code><code class="ros plain">=2.2.2.2</code> <code class="ros value">to-ports</code><code class="ros plain">=2200-2299</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.1.3</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number22 index21 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros plain">10&nbsp;&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=xxx-1</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">to-addresses</code><code class="ros plain">=2.2.2.2</code> <code class="ros value">to-ports</code><code class="ros plain">=2300-2399</code> <code class="ros value">protocol</code><code class="ros plain">=tcp</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.1.4</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number24 index23 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number25 index24 alt2" data-bidi-marker="true"><code class="ros plain">11&nbsp;&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=xxx-1</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">to-addresses</code><code class="ros plain">=2.2.2.2</code> <code class="ros value">to-ports</code><code class="ros plain">=2300-2399</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.1.4</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number26 index25 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number27 index26 alt2" data-bidi-marker="true"><code class="ros plain">12&nbsp;&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=xxx-2</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">to-addresses</code><code class="ros plain">=2.2.2.2</code> <code class="ros value">to-ports</code><code class="ros plain">=2400-2499</code> <code class="ros value">protocol</code><code class="ros plain">=tcp</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.1.5</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number28 index27 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number29 index28 alt2" data-bidi-marker="true"><code class="ros plain">13&nbsp;&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=xxx-2</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">to-addresses</code><code class="ros plain">=2.2.2.2</code> <code class="ros value">to-ports</code><code class="ros plain">=2400-2499</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.1.5</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number30 index29 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number31 index30 alt2" data-bidi-marker="true"><code class="ros plain">14&nbsp;&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=xxx-2</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">to-addresses</code><code class="ros plain">=2.2.2.2</code> <code class="ros value">to-ports</code><code class="ros plain">=2500-2599</code> <code class="ros value">protocol</code><code class="ros plain">=tcp</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.1.6</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number32 index31 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number33 index32 alt2" data-bidi-marker="true"><code class="ros plain">15&nbsp;&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=xxx-2</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">to-addresses</code><code class="ros plain">=2.2.2.2</code> <code class="ros value">to-ports</code><code class="ros plain">=2500-2599</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">src-address</code><code class="ros plain">=100.64.1.6</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div></div></td></tr></tbody></table>

#### Hairpin NAT

Hairpin network address translation (_NAT Loopback_) is where the device on the LAN is able to access another machine on the LAN via the public IP address of the gateway router. 

  

![](https://help.mikrotik.com/docs/download/attachments/3211299/NAT-setup.jpg?version=3&modificationDate=1572338061900&api=v2)

  

In the above example the gateway router has the following _dst-nat_ configuration rule:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall nat </code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=dstnat</code> <code class="ros value">action</code><code class="ros plain">=dst-nat</code> <code class="ros value">dst-address</code><code class="ros plain">=172.16.16.1</code> <code class="ros value">dst-port</code><code class="ros plain">=443</code> <code class="ros value">to-addresses</code><code class="ros plain">=10.0.0.3</code> <code class="ros value">to-ports</code><code class="ros plain">=443</code> <code class="ros value">protocol</code><code class="ros plain">=tcp</code></div></div></td></tr></tbody></table>

When a user from the PC at home establishes a connection to the webserver, the router performs DST NAT as configured:

1.  the client sends a packet with a source IP address of 192.168.88.1 to a destination IP address of 172.16.16.1 on port 443 to request some web resources;
2.  the router destination NAT\`s the packet to 10.0.0.3 and replaces the destination IP address in the packet accordingly. The source IP address stays the same: 192.168.88.1;
3.  the server replies to the client's request and the reply packet have a source IP address of 10.0.0.3 and a destination IP address of 192.168.88.1.
4.  the router determines that the packet is part of a previous connection and undoes the destination NAT, and puts the original destination IP address into the source IP address field. The destination IP address is 192.168.88.1, and the source IP address is 172.16.16.1;
5.  The client receives the reply packet it expects, and the connection is established;

  

![](https://help.mikrotik.com/docs/download/attachments/3211299/Hairpin-NAT-setup.jpg?version=2&modificationDate=1572338092573&api=v2)

But, there will be a **problem**, when a client on the same network as the webserver requests a connection to the web server's **public** IP address: 

1.  the client sends a packet with a source IP address of 10.0.0.2 to a destination IP address of 172.16.16.1 on port 443 to request some web resources;
2.  the router destination NATs the packet to 10.0.0.3 and replaces the destination IP address in the packet accordingly. The source IP address stays the same: 10.0.0.2;
3.  the server replies to the client's request. However, the source IP address of the request is on the same subnet as the webserver. The web server does not send the reply back to the router but sends it back directly to 10.0.0.2 with a source IP address in the reply of 10.0.0.3;
4.  The client receives the reply packet, but it discards it because it expects a packet back from 172.16.16.1, and not from 10.0.0.3;

To resolve this issue, we will configure a new _src-nat_ rule (the hairpin NAT rule) as follows:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall nat</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=masquerade</code> <code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">dst-address</code><code class="ros plain">=10.0.0.3</code> <code class="ros value">out-interface</code><code class="ros plain">=LAN</code> <code class="ros value">protocol</code><code class="ros plain">=tcp</code> <code class="ros value">src-address</code><code class="ros plain">=10.0.0.0/24</code></div></div></td></tr></tbody></table>

After configuring the rule above:

1.  the client sends a packet with a source IP address of 10.0.0.2 to a destination IP address of 172.16.16.1 on port 443 to request some web resources;
2.  the router destination NATs the packet to 10.0.0.3 and replaces the destination IP address in the packet accordingly. It also source NATs the packet and replaces the source IP address in the packet with the IP address on its LAN interface. The destination IP address is 10.0.0.3, and the source IP address is 10.0.0.1;
3.  the web server replies to the request and sends the reply with a source IP address of 10.0.0.3 back to the router's LAN interface IP address of 10.0.0.1;
4.  the router determines that the packet is part of a previous connection and undoes both the source and destination NAT, and puts the original destination IP address of 10.0.0.3 into the source IP address field, and the original source IP address of 172.16.16.1 into the destination IP address field

## IPv4

### Properties


| 属性                                            | 说明                                               |
| ----------------------------------------------- | -------------------------------------------------- |
| **action** (_action name_; Default: **accept**) | Action to take if a packet is matched by the rule: |

-   accept \- accept the packet. A packet is not passed to the next NAT rule.
-   add-dst-to-address-list \- add the destination address to the address list specified by `address-list` parameter
-   add-src-to-address-list \- add the source address to the address list specified by `address-list` parameter
-   dst-nat \- replaces destination address and/or port of an IP packet to values specified by `to-addresses` and `to-ports` parameters
-   jump \- jump to the user-defined chain specified by the value of `jump-target` parameter
-   log \- add a message to the system log containing the following data: in-interface, out-interface, src-mac, protocol, src-ip:port->dst-ip:port and length of the packet. After a packet is matched it is passed to the next rule in the list, similar as `passthrough`
-   masquerade \- replaces the source port of an IP packet with one specified by `to-ports` parameter and replace the source address of an IP packet to IP determined by the routing facility. 
-   netmap \- creates a static 1:1 mapping of one set of IP addresses to another one. Often used to distribute public IP addresses to hosts on private networks
-   passthrough \- if a packet is matched by the rule, increase the counter and go to the next rule (useful for statistics).
-   redirect \- replaces the destination port of an IP packet with one specified by `to-ports` parameter and destination address to one of the router's local addresses
-   return \- passes control back to the chain from where the jump took place
-   same \- gives a particular client the same source/destination IP address from a supplied range for each connection. This is most frequently used for services that expect the same client address for multiple connections from the same client
-   src-nat \- replaces the source address of an IP packet with values specified by `to-addresses` and `to-ports` parameters

 |
| **address-list** (_string_; Default: ) | Name of the address list to be used. Applicable if action is `add-dst-to-address-list` or `add-src-to-address-list` |
| **address-list-timeout** (_none-dynamic | none-static | time_; Default: **none-dynamic**) | Time interval after which the address will be removed from the address list specified by `address-list` parameter. Used in conjunction with `add-dst-to-address-list` or `add-src-to-address-list` actions  

-   Value of none-dynamic (`00:00:00`) will leave the address in the address list till reboot
-   Value of none-static will leave the address in the address list forever and will be included in configuration export/backup

 |
| **chain** (_name_; Default: ) | Specifies to which chain rule will be added. If the input does not match the name of an already defined chain, a new chain will be created |
| **comment** (_string_; Default: ) | Descriptive comment for the rule |
| **connection-bytes** (_integer-integer_; Default: ) | Matches packets only if a given amount of bytes has been transferred through the particular connection. 0 - means infinity, for example `connection-bytes=2000000-0` means that the rule matches if more than 2MB has been transferred through the relevant connection |
| **connection-limit** (_integer,netmask_; Default: ) | Matches connections per address or address block after a given value is reached |
| **connection-mark** (_no-mark | string_; Default: ) | Matches packets marked via mangle facility with particular connection mark. If **no-mark** is set, the rule will match any unmarked connection |
| **connection-rate** (_Integer 0..4294967295_; Default: ) | Connection Rate is a firewall matcher that allows capturing traffic based on the present speed of the connection |
| **connection-type** (_ftp | h323 | irc | pptp | quake3 | sip | tftp_; Default: ) | Matches packets from related connections based on information from their connection tracking helpers. A relevant connection helper must be enabled under /ip firewall service-port |
| **content** (_string_; Default: ) | Match packets that contain specified text |
| **dscp** (_integer: 0..63_; Default: ) | Matches DSCP IP header field. |
| **dst-address** (_IP/netmask | IP range_; Default: ) | Matches packets whose destination is equal to specified IP or falls into a specified IP range. |
| **dst-address-list** (_name_; Default: ) | Matches destination address of a packet against user-defined address list |
| **dst-address-type** (_unicast | local | broadcast | multicast_; Default: ) | Matches destination address type:

-   unicast \- IP address used for point-to-point transmission
-   local \- if dst-address is assigned to one of the router's interfaces
-   broadcast \- packet is sent to all devices in a subnet
-   multicast \- packet is forwarded to a defined group of devices

 |
| **dst-limit** (_integer\[/time\],integer,dst-address | dst-port | src-address\[/time\]_; Default: ) | Matches packets until a given PPS limit is exceeded. As opposed to the limit matcher, every destination IP address/destination port has its own limit. Parameters are written in the following format: `count[/time],burst,mode[/expire]`.

-   **count** \- maximum average packet rate measured in packets per `time` interval
-   **time** \- specifies the time interval in which the packet rate is measured (optional)
-   **burst** \- number of packets that are not counted by packet rate
-   **mode** \- the classifier for packet rate limiting
-   **expire** \- specifies interval after which recorded IP address /port will be deleted (optional)

 |
| **dst-port** (_integer\[-integer\]: 0..65535_; Default: ) | List of destination port numbers or port number ranges in format _Range\[,Port\]_, for example, _dst-port=123-345,456-678_ |
| **fragment** (_yes|no_; Default: ) | Matches fragmented packets. The first (starting) fragment does not count. If connection tracking is enabled there will be no fragments as the system automatically assembles every packet |
| **hotspot** (_auth | from-client | http | local-dst | to-client_; Default: ) | Matches packets received from HotSpot clients against various HotSpot matchers.

-   auth \- matches authenticated HotSpot client packets
-   from-client \- matches packets that are coming from the HotSpot client
-   http \- matches HTTP requests sent to the HotSpot server
-   local-dst \- matches packets that are destined to the HotSpot server
-   to-client \- matches packets that are sent to the HotSpot client

 |
| **icmp-options** (_integer:integer_; Default: ) | Matches ICMP type: code fields |
| **in-bridge-port** (_name_; Default: ) | Actual interface the packet has entered the router if the incoming interface is a bridge |
| **in-interface** (_name_; Default: ) | Interface the packet has entered the router |
| **ingress-priority** (_integer: 0..63_; Default: ) | Matches ingress the priority of the packet. Priority may be derived from VLAN, WMM or MPLS EXP bit.  |
| **ipsec-policy** (_in | out, ipsec | none_; Default: ) | Matches the policy used by IPSec. Value is written in the following format: `**direction, policy**`. The direction is Used to select whether to match the policy used for decapsulation or the policy that will be used for encapsulation.

-   in \- valid in the PREROUTING, INPUT, and FORWARD chains
-   out \- valid in the POSTROUTING, OUTPUT, and FORWARD chains

-   ipsec \- matches if the packet is subject to IPsec processing;
-   none \- matches packet that is not subject to IPsec processing (for example, IPSec transport packet).

For example, if a router receives an IPsec encapsulated Gre packet, then rule `ipsec-policy=in,ipsec` will match Gre packet, but the rule `ipsec-policy=in,none` will match the ESP packet.

 |
| **ipv4-options** (_any | loose-source-routing | no-record-route | no-router-alert | no-source-routing | no-timestamp | none | record-route | router-alert | strict-source-routing | timestamp_; Default: ) | Matches IPv4 header options.

-   any \- match packet with at least one of the ipv4 options
-   loose-source-routing \- match packets with a loose source routing option. This option is used to route the internet datagram based on information supplied by the source
-   no-record-route \- match packets with no record route option. This option is used to route the internet datagram based on information supplied by the source
-   no-router-alert \- match packets with no router alter option
-   no-source-routing \- match packets with no source routing option
-   no-timestamp \- match packets with no timestamp option
-   record-route \- match packets with record route option
-   router-alert \- match packets with router alter option
-   strict-source-routing \- match packets with a strict source routing option
-   timestamp \- match packets with a timestamp

 |
| **jump-target** (_name_; Default: ) | Name of the target chain to jump to. Applicable only if `action=jump` |
| **layer7-protocol** (_name_; Default: ) | Layer7 filter name defined in layer7 protocol menu. |
| **limit** (_integer,time,integer_; Default: ) | Matches packets until a given PPS limit is exceeded. Parameters are written in the following format: `count[/time],burst`.

-   **count** \- maximum average packet rate measured in packets per `time` interval
-   **time** \- specifies the time interval in which the packet rate is measured (optional, 1s will be used if not specified)
-   **burst** \- number of packets that are not counted by packet rate

 |
| **log** (_yes | no; Default:_ **no**) | Add a message to the system log containing the following data: in-interface, out-interface, src-mac, protocol, src-ip:port->dst-ip:port, and length of the packet. |
| **log-prefix** (_string_; Default: ) | Adds specified text at the beginning of every log message. Applicable if _action=log_ or _log=yes_ configured. |
| **out-bridge-port** (_name_; Default: ) | Actual interface the packet is leaving the router if the outgoing interface is a bridge |
| **out-interface** (; Default: ) | Interface the packet is leaving the router |
| **packet-mark** (_no-mark | string_; Default: ) | Matches packets marked via mangle facility with particular packet mark. If **no-mark** is set, the rule will match any unmarked packet |
| **packet-size** (_integer\[-integer\]:0..65535_; Default: ) | Matches packets of specified size or size range in bytes |
| **per-connection-classifier** (_ValuesToHash:Denominator/Remainder_; Default: ) | PCC matcher allows dividing traffic into equal streams with the ability to keep packets with a specific set of options in one particular stream |
| **port** (_integer\[-integer\]: 0..65535_; Default: ) | Matches if any (source or destination) port matches the specified list of ports or port ranges. Applicable only if `protocol` is TCP or UDP |
| **protocol** (_name or protocol ID_; Default: **tcp**) | Matches particular IP protocol specified by protocol name or number |
| **psd** (_integer,time,integer,integer_; Default: ) | Attempts to detect TCP and UDP scans. Parameters are in the following format `WeightThreshold, DelayThreshold, LowPortWeight, HighPortWeight`

-   **WeightThreshold** \- total weight of the latest TCP/UDP packets with different destination ports coming from the same host to be treated as port scan sequence
-   **DelayThreshold** \- delay for the packets with different destination ports coming from the same host to be treated as possible port scan subsequence
-   **LowPortWeight** \- the weight of the packets with privileged (<1024) destination port
-   **HighPortWeight** \- the weight of the packet with a non-privileged destination port

 |
| **random** (_integer: 1..99_; Default: ) | Matches packets randomly with a given probability |
| **routing-mark** (_string_; Default: ) | Matches packets marked by mangle facility with particular routing mark |
| **same-not-by-dst** (_yes | no_; Default: ) | Specifies whether to take into account or not destination IP address when selecting a new source IP address. Applicable if `action=same` |
| **src-address** (_Ip/Netmaks, Ip range_; Default: ) | Matches packets whose source is equal to specified IP or falls into a specified IP range. |
| **src-address-list** (_name_; Default: ) | Matches source address of a packet against user-defined address list |
| **src-address-type** (_unicast | local | broadcast | multicast_; Default: ) | 

Matches source address type:

-   unicast \- IP address used for point-to-point transmission
-   local \- if an address is assigned to one of the router's interfaces
-   broadcast \- packet is sent to all devices in a subnet
-   multicast \- packet is forwarded to a defined group of devices

 |
| **src-port** (_integer\[-integer\]: 0..65535_; Default: ) | List of source ports and ranges of source ports. Applicable only if a protocol is TCP or UDP. |
| **src-mac-address** (_MAC address_; Default: ) | Matches source MAC address of the packet |
| **tcp-mss** (_integer\[-integer\]: 0..65535_; Default: ) | Matches TCP MSS value of an IP packet |
| **time** (_time-time,sat | fri | thu | wed | tue | mon | sun_; Default: ) | Allows to create a filter based on the packets' arrival time and date or, for locally generated packets, departure time and date |
| **to-addresses** (_IP address\[-IP address\]_; Default: **0.0.0.0**) | Replace the original address with the specified one. Applicable if action is dst-nat, netmap, same, src-nat |
| **to-ports** (_integer\[-integer\]: 0..65535_; Default: ) | Replace the original port with the specified one. Applicable if action is dst-nat, redirect, masquerade, netmap, same, src-nat |
| **ttl** (_integer: 0..255_; Default: ) | Matches packets TTL value |

### Stats


| 属性                    | 说明                                            |
| ----------------------- | ----------------------------------------------- |
| **bytes** (_integer_)   | The total amount of bytes matched by the rule   |
| **packets** (_integer_) | The total amount of packets matched by the rule |

To show additional _read-only_ properties:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; ip firewall nat </code><code class="ros functions">print </code><code class="ros plain">stats </code><code class="ros variable">all</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - invalid, D - dynamic</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros comments"># CHAIN ACTION BYTES PACKETS</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">0 srcnat masquerade 265 659 987</code></div></div></td></tr></tbody></table>

## IPv6

NAT66 is supported since RouterOS v7.1.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">ipv6</code><code class="ros constants">/firewall/nat/</code></div></div></td></tr></tbody></table>

### Properties


| 属性                                            | 说明                                               |
| ----------------------------------------------- | -------------------------------------------------- |
| **action** (_action name_; Default: **accept**) | Action to take if a packet is matched by the rule: |

-   accept \- accept the packet. A packet is not passed to the next NAT rule.
-   add-dst-to-address-list \- add the destination address to the address list specified by `address-list` parameter
-   add-src-to-address-list \- add the source address to the address list specified by `address-list` parameter
-   dst-nat \- replaces destination address and/or port of an IP packet to values specified by `to-addresses` and `to-ports` parameters
-   jump \- jump to the user-defined chain specified by the value of `jump-target` parameter
-   log \- add a message to the system log containing the following data: in-interface, out-interface, src-mac, protocol, src-ip:port->dst-ip:port and length of the packet. After a packet is matched it is passed to the next rule in the list, similar as `passthrough`
-   masquerade \- replaces the source port of an IP packet with one specified by `to-ports` parameter and replace the source address of an IP packet to IP determined by the routing facility. 
-   netmap \- creates a static 1:1 mapping of one set of IP addresses to another one. Often used to distribute public IP addresses to hosts on private networks
-   passthrough \- if a packet is matched by the rule, increase the counter and go to the next rule (useful for statistics).
-   redirect \- replaces the destination port of an IP packet with one specified by `to-ports` parameter and destination address to one of the router's local addresses
-   return \- passes control back to the chain from where the jump took place
-   src-nat \- replaces the source address of an IP packet with values specified by `to-addresses` and `to-ports` parameters

 |
| **address-list** (_string_; Default: ) | Name of the address list to be used. Applicable if action is `add-dst-to-address-list` or `add-src-to-address-list` |
| **address-list-timeout** (_none-dynamic | none-static | time_; Default: **none-dynamic**) | Time interval after which the address will be removed from the address list specified by `address-list` parameter. Used in conjunction with `add-dst-to-address-list` or `add-src-to-address-list` actions  

-   Value of none-dynamic (`00:00:00`) will leave the address in the address list till reboot
-   Value of none-static will leave the address in the address list forever and will be included in configuration export/backup

 |
| **chain** (_name_; Default: ) | Specifies to which chain rule will be added. If the input does not match the name of an already defined chain, a new chain will be created |
| **comment** (_string_; Default: ) | Descriptive comment for the rule |
| **connection-bytes** (_integer-integer_; Default: ) | Matches packets only if a given amount of bytes has been transferred through the particular connection. 0 - means infinity, for example `connection-bytes=2000000-0` means that the rule matches if more than 2MB has been transferred through the relevant connection |
| **connection-limit** (_integer,netmask_; Default: ) | Matches connections per address or address block after a given value is reached |
| **connection-mark** (_no-mark | string_; Default: ) | Matches packets marked via mangle facility with particular connection mark. If **no-mark** is set, the rule will match any unmarked connection |
| **connection-rate** (_Integer 0..4294967295_; Default: ) | Connection Rate is a firewall matcher that allows capturing traffic based on the present speed of the connection |
| **connection-state** (_established | invalid | new | related | untracked_; Default: ) | Interprets the connection tracking analytics data for a particular packet:

-   established \- a packet that belongs to an existing connection
-   invalid \- a packet that does not have a determined state in connection tracking (usually - severe out-of-order packets, packets with wrong sequence/ack number, or in case of a resource over usage on the router), for this reason, an invalid packet will not participate in NAT (as only connection-state=new packets do), and will still contain original source IP address when routed. We strongly suggest dropping all _connection-state=invalid_ packets in firewall filter forward and input chains
-   new \- the packet has started a new connection, or is otherwise associated with a connection that has not seen packets in both directions.
-   related \- a packet that is related to, but not parts of an existing connection, such as ICMP errors or a packet that begins FTP data connection
-   an untracked \- packet which was set to bypass connection tracking in firewall [RAW](https://wiki.mikrotik.com/wiki/Manual:IP/Firewall/Raw "Manual:IP/Firewall/Raw") tables.

 |
| **connection-type** (_ftp | h323 | irc | pptp | quake3 | sip | tftp_; Default: ) | Matches packets from related connections based on information from their connection tracking helpers. A relevant connection helper must be enabled under /ip firewall service-port |
| **content** (_string_; Default: ) | Match packets that contain specified text |
| **dscp** (_integer: 0..63_; Default: ) | Matches DSCP IP header field. |
| **dst-address** (_IP/netmask | IP range_; Default: ) | Matches packets whose destination is equal to specified IP or falls into a specified IP range. |
| **dst-address-list** (_name_; Default: ) | Matches destination address of a packet against user-defined address list |
| **dst-address-type** (_unicast | local | broadcast | multicast_; Default: ) | Matches destination address type:

-   unicast \- IP address used for point-to-point transmission
-   local \- if dst-address is assigned to one of the router's interfaces
-   broadcast \- packet is sent to all devices in a subnet
-   multicast \- packet is forwarded to a defined group of devices

 |
| **dst-limit** (_integer\[/time\],integer,dst-address | dst-port | src-address\[/time\]_; Default: ) | Matches packets until a given PPS limit is exceeded. As opposed to the limit matcher, every destination IP address/destination port has its own limit. Parameters are written in the following format: `count[/time],burst,mode[/expire]`.

-   **count** \- maximum average packet rate measured in packets per `time` interval
-   **time** \- specifies the time interval in which the packet rate is measured (optional)
-   **burst** \- number of packets that are not counted by packet rate
-   **mode** \- the classifier for packet rate limiting
-   **expire** \- specifies interval after which recorded IP address /port will be deleted (optional)

 |
| **dst-port** (_integer\[-integer\]: 0..65535_; Default: ) | List of destination port numbers or port number ranges in format _Range\[,Port\]_, for example, _dst-port=123-345,456-678_ |
| **icmp-options** (_integer:integer_; Default: ) | Matches ICMP type: code fields |
| **in-bridge-port** (_name_; Default: ) | Actual interface the packet has entered the router if the incoming interface is a bridge |
| **in-bridge-port-list** (_name_; Default: ) | Set of interfaces defined in interface list. Works the same as in-bridge-port |
| **in-interface** (_name_; Default: ) | Interface the packet has entered the router |
| **in-interface-list** (_name_; Default: ) | Set of interfaces defined in interface list. Works the same as in-interface |
| **ingress-priority** (_integer: 0..63_; Default: ) | Matches ingress the priority of the packet. Priority may be derived from VLAN, WMM or MPLS EXP bit.  |
| **ipsec-policy** (_in | out, ipsec | none_; Default: ) | Matches the policy used by IPSec. Value is written in the following format: `**direction, policy**`. The direction is Used to select whether to match the policy used for decapsulation or the policy that will be used for encapsulation.

-   in \- valid in the PREROUTING, INPUT, and FORWARD chains
-   out \- valid in the POSTROUTING, OUTPUT, and FORWARD chains

-   ipsec \- matches if the packet is subject to IPsec processing;
-   none \- matches packet that is not subject to IPsec processing (for example, IPSec transport packet).

For example, if a router receives an IPsec encapsulated Gre packet, then rule `ipsec-policy=in,ipsec` will match Gre packet, but the rule `ipsec-policy=in,none` will match the ESP packet.

 |
| **jump-target** (_name_; Default: ) | Name of the target chain to jump to. Applicable only if `action=jump` |
| **layer7-protocol** (_name_; Default: ) | Layer7 filter name defined in layer7 protocol menu. |
| **limit** (_integer,time,integer_; Default: ) | Matches packets until a given PPS limit is exceeded. Parameters are written in the following format: `count[/time],burst`.

-   **count** \- maximum average packet rate measured in packets per `time` interval
-   **time** \- specifies the time interval in which the packet rate is measured (optional, 1s will be used if not specified)
-   **burst** \- number of packets that are not counted by packet rate

 |
| **log** (_yes | no; Default:_ **no**) | Add a message to the system log containing the following data: in-interface, out-interface, src-mac, protocol, src-ip:port->dst-ip:port, and length of the packet. |
| **log-prefix** (_string_; Default: ) | Adds specified text at the beginning of every log message. Applicable if _action=log_ or _log=yes_ configured. |
| **out-bridge-port** (_name_; Default: ) | Actual interface the packet is leaving the router if the outgoing interface is a bridge |
| **out-bridge-port-list** (_name_; Default: ) | Set of interfaces defined in interface list. Works the same as out-bridge-port |
| **out-interface** (; Default: ) | Interface the packet is leaving the router |
| **out-interface-list** (_name_; Default: ) | Set of interfaces defined in interface list. Works the same as out-interface |
| **packet-mark** (_no-mark | string_; Default: ) | Matches packets marked via mangle facility with particular packet mark. If **no-mark** is set, the rule will match any unmarked packet |
| **packet-size** (_integer\[-integer\]:0..65535_; Default: ) | Matches packets of specified size or size range in bytes |
| **per-connection-classifier** (_ValuesToHash:Denominator/Remainder_; Default: ) | PCC matcher allows dividing traffic into equal streams with the ability to keep packets with a specific set of options in one particular stream |
| **port** (_integer\[-integer\]: 0..65535_; Default: ) | Matches if any (source or destination) port matches the specified list of ports or port ranges. Applicable only if `protocol` is TCP or UDP |
| **protocol** (_name or protocol ID_; Default: **tcp**) | Matches particular IP protocol specified by protocol name or number |
| **priority** (_integer: 0..63_; Default:) | Matches the packet's priority after a new priority has been set. Priority may be derived from VLAN, WMM, DSCP, MPLS EXP bit, or from the priority that has been set using the set-priority action. |
| **random** (_integer: 1..99_; Default: ) | Matches packets randomly with a given probability |
| **routing-mark** (_string_; Default: ) | Matches packets marked by mangle facility with particular routing mark |
| **src-address** (_Ip/Netmaks, Ip range_; Default: ) | Matches packets whose source is equal to specified IP or falls into a specified IP range. |
| **src-address-list** (_name_; Default: ) | Matches source address of a packet against user-defined address list |
| **src-address-type** (_unicast | local | broadcast | multicast_; Default: ) | 

Matches source address type:

-   unicast \- IP address used for point-to-point transmission
-   local \- if an address is assigned to one of the router's interfaces
-   broadcast \- packet is sent to all devices in a subnet
-   multicast \- packet is forwarded to a defined group of devices |
| **src-port** (_integer\[-integer\]: 0..65535_; Default: ) | List of source ports and ranges of source ports. Applicable only if a protocol is TCP or UDP. |
| **tcp-flags** (_ack | cwr | ece | fin | psh | rst | syn | urg_; Default: ) | Matches specified TCP flags
-   ack \- acknowledging data
-   cwr \- congestion window reduced
-   ece \- ECN-echo flag (explicit congestion notification)
-   fin \- close connection
-   psh \- push function
-   rst \- drop connection
-   syn \- new connection
-   urg \- urgent data |
| **src-mac-address** (_MAC address_; Default: ) | Matches source MAC address of the packet |
| **tcp-mss** (_integer\[-integer\]: 0..65535_; Default: ) | Matches TCP MSS value of an IP packet |
| **time** (_time-time,sat | fri | thu | wed | tue | mon | sun_; Default: ) | Allows to create a filter based on the packets' arrival time and date or, for locally generated packets, departure time and date |
| **to-addresses** (_IP address\[-IP address\]_; Default: **0.0.0.0**) | Replace the original address with the specified one. Applicable if action is dst-nat, netmap, same, src-nat |
| **to-ports** (_integer\[-integer\]: 0..65535_; Default: ) | Replace the original port with the specified one. Applicable if action is dst-nat, redirect, masquerade, netmap, same, src-nat |

### 统计信息


| 属性                    | 说明                 |
| ----------------------- | -------------------- |
| **bytes** (_integer_)   | 该规则匹配的字节总数 |
| **packets** (_integer_) | 规则匹配的数据包总量 |

显示额外的 _只读_ 属性:

`ipv6/firewall/nat/print stats`
