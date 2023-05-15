# Overview

MikroTik RouterOS implements Label Distribution Protocol (RFC 3036, RFC 5036, and RFC 7552) for IPv4 and IPv6 address families. LDP is a protocol that performs the set of procedures and exchange messages by which Label Switched Routers (LSRs) establish Label Switched Paths (LSPs) through a network by mapping network-layer routing information directly to data-link layer switched paths.

# Prerequisites for MPLS

## "Loopback" IP address

Although not a strict requirement, it is advisable to configure routers participating in the MPLS network with "loopback" IP addresses (not attached to any real network interface) to be used by LDP to establish sessions.

This serves 2 purposes:

-   as there is only one LDP session between any 2 routers, no matter how many links connect them, the loopback IP address ensures that the LDP session is not affected by interface state or address changes
-   use of loopback address as LDP transport address ensures proper penultimate hop popping behavior when multiple labels are attached to the packet as in the case of VPLS

In RouterOS "loopback" IP address can be configured by creating a dummy bridge interface without any ports and adding the address to it. For example:

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=lo</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/ip address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=255.255.255.1/32</code> <code class="ros value">interface</code><code class="ros plain">=lo</code></div></div></td></tr></tbody></table>

  

  

## IP connectivity

As LDP distributes labels for active routes, the essential requirement is properly configured IP routing. LDP by default distributes labels for active IGP routes (that is - connected, static, and routing protocol learned routes, except BGP).

For instructions on how to set up properly IGP refer to appropriate documentation sections:

-   [OSPF](https://help.mikrotik.com/docs/display/ROS/OSPF)
-   [Static Routing](https://help.mikrotik.com/docs/display/ROS/IP+Routing)
-   etc

LDP supports ECMP routes.

You should be able to reach any loopback address from any location of your network before continuing with the LDP configuration. Connectivity can be verified with the ping tool running from loopback address to loopback address.

# Example Setup

Let's consider that we have already existing four routers setup, with working IP connectivity.

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">(lo</code><code class="ros constants">:111.111.111.1)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (lo:111.111.111.2)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (lo:111.111.111.3)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (lo:111.111.111.4)</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">|---------R1-----(</code><code class="ros color1">111.11.0.0/24</code><code class="ros plain">)-----R2-----(</code><code class="ros color1">111.12.0.0/24</code><code class="ros plain">)-----R3-----(</code><code class="ros color1">111.13.0.0/24</code><code class="ros plain">)-----R4---------|</code></div></div></td></tr></tbody></table>

  

## Ip Reachability

Not going deep into routing setup here is the quit export of the IP and OSPF configurations:

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros comments">#R1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=loopback</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=111.11.0.1/24</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=111.111.111.1</code> <code class="ros value">interface</code><code class="ros plain">=loopback</code></div><div class="line number7 index6 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros constants">/routing ospf instance</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=default_ip4</code> <code class="ros value">router-id</code><code class="ros plain">=111.111.111.1</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros constants">/routing ospf area</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">instance</code><code class="ros plain">=default_ip4</code> <code class="ros value">name</code><code class="ros plain">=backbone_ip4</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros constants">/routing ospf interface-template</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">area</code><code class="ros plain">=backbone_ip4</code> <code class="ros value">dead-interval</code><code class="ros plain">=10s</code> <code class="ros value">hello-interval</code><code class="ros plain">=1s</code> <code class="ros value">networks</code><code class="ros plain">=111.111.111.1</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">area</code><code class="ros plain">=backbone_ip4</code> <code class="ros value">dead-interval</code><code class="ros plain">=10s</code> <code class="ros value">hello-interval</code><code class="ros plain">=1s</code> <code class="ros value">networks</code><code class="ros plain">=111.11.0.0/24</code></div><div class="line number15 index14 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number16 index15 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros comments">#R2</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=loopback</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=111.11.0.2/24</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=111.12.0.1/24</code> <code class="ros value">interface</code><code class="ros plain">=ether3</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=111.111.111.2</code> <code class="ros value">interface</code><code class="ros plain">=loopback</code></div><div class="line number24 index23 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number25 index24 alt2" data-bidi-marker="true"><code class="ros constants">/routing ospf instance</code></div><div class="line number26 index25 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=default_ip4</code> <code class="ros value">router-id</code><code class="ros plain">=111.111.111.2</code></div><div class="line number27 index26 alt2" data-bidi-marker="true"><code class="ros constants">/routing ospf area</code></div><div class="line number28 index27 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">instance</code><code class="ros plain">=default_ip4</code> <code class="ros value">name</code><code class="ros plain">=backbone_ip4</code></div><div class="line number29 index28 alt2" data-bidi-marker="true"><code class="ros constants">/routing ospf interface-template</code></div><div class="line number30 index29 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">area</code><code class="ros plain">=backbone_ip4</code> <code class="ros value">dead-interval</code><code class="ros plain">=10s</code> <code class="ros value">hello-interval</code><code class="ros plain">=1s</code> <code class="ros value">networks</code><code class="ros plain">=111.111.111.2</code></div><div class="line number31 index30 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">area</code><code class="ros plain">=backbone_ip4</code> <code class="ros value">dead-interval</code><code class="ros plain">=10s</code> <code class="ros value">hello-interval</code><code class="ros plain">=1s</code> <code class="ros value">networks</code><code class="ros plain">=111.11.0.0/24</code></div><div class="line number32 index31 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">area</code><code class="ros plain">=backbone_ip4</code> <code class="ros value">dead-interval</code><code class="ros plain">=10s</code> <code class="ros value">hello-interval</code><code class="ros plain">=1s</code> <code class="ros value">networks</code><code class="ros plain">=111.12.0.0/24</code></div><div class="line number33 index32 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number34 index33 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number35 index34 alt2" data-bidi-marker="true"><code class="ros comments">#R3</code></div><div class="line number36 index35 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number37 index36 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=loopback</code></div><div class="line number38 index37 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number39 index38 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number40 index39 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=111.12.0.2/24</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number41 index40 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=111.13.0.1/24</code> <code class="ros value">interface</code><code class="ros plain">=ether3</code></div><div class="line number42 index41 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=111.111.111.3</code> <code class="ros value">interface</code><code class="ros plain">=loopback</code></div><div class="line number43 index42 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number44 index43 alt1" data-bidi-marker="true"><code class="ros constants">/routing ospf instance</code></div><div class="line number45 index44 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=default_ip4</code> <code class="ros value">router-id</code><code class="ros plain">=111.111.111.3</code></div><div class="line number46 index45 alt1" data-bidi-marker="true"><code class="ros constants">/routing ospf area</code></div><div class="line number47 index46 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">instance</code><code class="ros plain">=default_ip4</code> <code class="ros value">name</code><code class="ros plain">=backbone_ip4</code></div><div class="line number48 index47 alt1" data-bidi-marker="true"><code class="ros constants">/routing ospf interface-template</code></div><div class="line number49 index48 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">area</code><code class="ros plain">=backbone_ip4</code> <code class="ros value">dead-interval</code><code class="ros plain">=10s</code> <code class="ros value">hello-interval</code><code class="ros plain">=1s</code> <code class="ros value">networks</code><code class="ros plain">=111.111.111.3</code></div><div class="line number50 index49 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">area</code><code class="ros plain">=backbone_ip4</code> <code class="ros value">dead-interval</code><code class="ros plain">=10s</code> <code class="ros value">hello-interval</code><code class="ros plain">=1s</code> <code class="ros value">networks</code><code class="ros plain">=111.12.0.0/24</code></div><div class="line number51 index50 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">area</code><code class="ros plain">=backbone_ip4</code> <code class="ros value">dead-interval</code><code class="ros plain">=10s</code> <code class="ros value">hello-interval</code><code class="ros plain">=1s</code> <code class="ros value">networks</code><code class="ros plain">=111.13.0.0/24</code></div><div class="line number52 index51 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number53 index52 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number54 index53 alt1" data-bidi-marker="true"><code class="ros comments">#R4</code></div><div class="line number55 index54 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number56 index55 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=loopback</code></div><div class="line number57 index56 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number58 index57 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=111.13.0.2/24</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number59 index58 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=111.111.111.4</code> <code class="ros value">interface</code><code class="ros plain">=loopback</code></div><div class="line number60 index59 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number61 index60 alt2" data-bidi-marker="true"><code class="ros constants">/routing ospf instance</code></div><div class="line number62 index61 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=default_ip4</code> <code class="ros value">router-id</code><code class="ros plain">=111.111.111.4</code></div><div class="line number63 index62 alt2" data-bidi-marker="true"><code class="ros constants">/routing ospf area</code></div><div class="line number64 index63 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">instance</code><code class="ros plain">=default_ip4</code> <code class="ros value">name</code><code class="ros plain">=backbone_ip4</code></div><div class="line number65 index64 alt2" data-bidi-marker="true"><code class="ros constants">/routing ospf interface-template</code></div><div class="line number66 index65 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">area</code><code class="ros plain">=backbone_ip4</code> <code class="ros value">dead-interval</code><code class="ros plain">=10s</code> <code class="ros value">hello-interval</code><code class="ros plain">=1s</code> <code class="ros value">networks</code><code class="ros plain">=111.111.111.4</code></div><div class="line number67 index66 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">area</code><code class="ros plain">=backbone_ip4</code> <code class="ros value">dead-interval</code><code class="ros plain">=10s</code> <code class="ros value">hello-interval</code><code class="ros plain">=1s</code> <code class="ros value">networks</code><code class="ros plain">=111.13.0.0/24</code></div></div></td></tr></tbody></table>

  

Verify that IP connectivity and routing are working properly

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@R4] /ip/address&gt; /tool traceroute 111.111.111.1 src-address=111.111.111.4</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Columns: ADDRESS, LOSS, SENT, LAST, AVG, BEST, WORST, STD-DEV</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">#&nbsp; ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; LOSS&nbsp; SENT&nbsp; LAST&nbsp;&nbsp; AVG&nbsp; BEST&nbsp; WORST&nbsp; STD-DEV</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">1&nbsp; 111.13.0.1&nbsp;&nbsp;&nbsp;&nbsp; 0%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 4&nbsp; 0.6ms&nbsp; 0.6&nbsp; 0.6&nbsp;&nbsp; 0.6&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">2&nbsp; 111.12.0.1&nbsp;&nbsp;&nbsp;&nbsp; 0%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 4&nbsp; 0.5ms&nbsp; 0.6&nbsp; 0.5&nbsp;&nbsp; 0.6&nbsp;&nbsp;&nbsp; 0.1&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text plain">3&nbsp; 111.111.111.1&nbsp; 0%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 4&nbsp; 0.6ms&nbsp; 0.6&nbsp; 0.6&nbsp;&nbsp; 0.6&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div></div></td></tr></tbody></table>

  

## LDP Setup

In order to start distributing labels, LDP is enabled on interfaces that connect other LDP routers and not enabled on interfaces that connect customer networks.

On R1 it will look like this:

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/mpls ldp</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">afi</code><code class="ros plain">=ip</code> <code class="ros value">lsr-id</code><code class="ros plain">=111.111.111.1</code> <code class="ros value">transport-addresses</code><code class="ros plain">=111.111.111.1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/mpls ldp interface</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> &nbsp; &nbsp;</div></div></td></tr></tbody></table>

Note that the transport address gets set to 111.111.111.1. This makes the router originate LDP session connections with this address and also advertise this address as a transport address to LDP neighbors.

  

Other routers are set up similarly.

R2:

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/mpls ldp</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">afi</code><code class="ros plain">=ip</code> <code class="ros value">lsr-id</code><code class="ros plain">=111.111.111.2</code> <code class="ros value">transport-addresses</code><code class="ros plain">=111.111.111.2</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/mpls ldp interface</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> &nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether3</code> &nbsp;</div></div></td></tr></tbody></table>

On R3:

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/mpls ldp</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">afi</code><code class="ros plain">=ip</code> <code class="ros value">lsr-id</code><code class="ros plain">=111.111.111.3</code> <code class="ros value">transport-addresses</code><code class="ros plain">=111.111.111.3</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/mpls ldp interface</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> &nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether3</code> &nbsp;</div></div></td></tr></tbody></table>

On R4:

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/mpls ldp</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">afi</code><code class="ros plain">=ip</code> <code class="ros value">lsr-id</code><code class="ros plain">=111.111.111.4</code> <code class="ros value">transport-addresses</code><code class="ros plain">=111.111.111.4</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/mpls ldp interface</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> &nbsp;</div></div></td></tr></tbody></table>

  

  

After LDP sessions are established, R2 should have two LDP neighbors:

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@R2] /mpls/ldp/neighbor&gt; print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: D, I - INACTIVE; O, T - THROTTLED; p - PASSIVE</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Columns: TRANSPORT, LOCAL-TRANSPORT, PEER, ADDRESSES</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">#&nbsp;&nbsp;&nbsp;&nbsp; TRANSPORT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; LOCAL-TRANSPORT&nbsp; PEER&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ADDRESSES&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">0 DO&nbsp; 111.111.111.1&nbsp; 111.111.111.2&nbsp;&nbsp;&nbsp; 111.111.111.1:0&nbsp; 111.11.0.1&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">111.111.111.1</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain">1 DOp 111.111.111.3&nbsp; 111.111.111.2&nbsp;&nbsp;&nbsp; 111.111.111.3:0&nbsp; 111.12.0.2&nbsp;&nbsp;</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">111.13.0.1&nbsp;&nbsp;</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">111.111.111.3</code></div></div></td></tr></tbody></table>

  

The local mappings table shows what label is assigned to what route and peers the router have distributed labels to.

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@R2] /mpls/ldp/local-mapping&gt; print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: I - INACTIVE; D - DYNAMIC; E - EGRESS; G - GATEWAY; L - LOCAL</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Columns: VRF, DST-ADDRESS, LABEL, PEERS</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; VRF&nbsp;&nbsp; DST-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; LABEL&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PEERS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">0&nbsp; D G&nbsp; main&nbsp; 10.0.0.0/8&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 16&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.1:0</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">111.111.111.3:0</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain">1 IDE L main&nbsp; 10.155.130.0/25&nbsp; impl-null&nbsp; 111.111.111.1:0</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">111.111.111.3:0</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text plain">2 IDE L main&nbsp; 111.11.0.0/24&nbsp;&nbsp;&nbsp; impl-null&nbsp; 111.111.111.1:0</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">111.111.111.3:0</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="text plain">3 IDE L main&nbsp; 111.12.0.0/24&nbsp;&nbsp;&nbsp; impl-null&nbsp; 111.111.111.1:0</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">111.111.111.3:0</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="text plain">4 IDE L main&nbsp; 111.111.111.2&nbsp;&nbsp;&nbsp; impl-null&nbsp; 111.111.111.1:0</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">111.111.111.3:0</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="text plain">5&nbsp; D G&nbsp; main&nbsp; 111.111.111.1&nbsp;&nbsp;&nbsp; 17&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.1:0</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">111.111.111.3:0</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="text plain">6&nbsp; D G&nbsp; main&nbsp; 111.111.111.3&nbsp;&nbsp;&nbsp; 18&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.1:0</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">111.111.111.3:0</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="text plain">7&nbsp; D G&nbsp; main&nbsp; 111.111.111.4&nbsp;&nbsp;&nbsp; 19&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.1:0</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">111.111.111.3:0</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="text plain">8&nbsp; D G&nbsp; main&nbsp; 111.13.0.0/24&nbsp;&nbsp;&nbsp; 20&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.1:0</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">111.111.111.3:0</code></div></div></td></tr></tbody></table>

  

  

Remote mappings table on the other hand shows labels that are allocated for routes by neighboring LDP routers and advertised to this router:

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@R2] /mpls/ldp/remote-mapping&gt; print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: I - INACTIVE; D - DYNAMIC</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Columns: VRF, DST-ADDRESS, NEXTHOP, LABEL, PEER</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">#&nbsp;&nbsp;&nbsp; VRF&nbsp;&nbsp; DST-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NEXTHOP&nbsp;&nbsp;&nbsp;&nbsp; LABEL&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PEER&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">0 ID main&nbsp; 10.0.0.0/8&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 16&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.1:0</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">1 ID main&nbsp; 10.155.130.0/25&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; impl-null&nbsp; 111.111.111.1:0</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">2 ID main&nbsp; 111.11.0.0/24&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; impl-null&nbsp; 111.111.111.1:0</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">3 ID main&nbsp; 111.12.0.0/24&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 17&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.1:0</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">4&nbsp; D main&nbsp; 111.111.111.1&nbsp;&nbsp;&nbsp; 111.11.0.1&nbsp; impl-null&nbsp; 111.111.111.1:0</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">5 ID main&nbsp; 111.111.111.2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 19&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.1:0</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">6 ID main&nbsp; 111.111.111.3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 20&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.1:0</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">7 ID main&nbsp; 111.111.111.4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 21&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.1:0</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">8 ID main&nbsp; 111.13.0.0/24&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 18&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.1:0</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">9 ID main&nbsp; 0.0.0.0/0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; impl-null&nbsp; 111.111.111.3:0</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="text plain">10 ID main&nbsp; 111.111.111.2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 16&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.3:0</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="text plain">11 ID main&nbsp; 111.111.111.1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 18&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.3:0</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="text plain">12&nbsp; D main&nbsp; 111.111.111.3&nbsp;&nbsp;&nbsp; 111.12.0.2&nbsp; impl-null&nbsp; 111.111.111.3:0</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="text plain">13&nbsp; D main&nbsp; 111.111.111.4&nbsp;&nbsp;&nbsp; 111.12.0.2&nbsp; 19&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.3:0</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="text plain">14 ID main&nbsp; 10.155.130.0/25&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; impl-null&nbsp; 111.111.111.3:0</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="text plain">15 ID main&nbsp; 111.11.0.0/24&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 17&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.3:0</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="text plain">16 ID main&nbsp; 111.12.0.0/24&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; impl-null&nbsp; 111.111.111.3:0</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="text plain">17&nbsp; D main&nbsp; 111.13.0.0/24&nbsp;&nbsp;&nbsp; 111.12.0.2&nbsp; impl-null&nbsp; 111.111.111.3:0</code></div></div></td></tr></tbody></table>

  

We can observe that router has received label bindings for all routes from both its neighbors - R1 and R3.

The remote mapping table will have active mappings only for the destinations that have direct next-hop, for example, let's take a closer look at 111.111.111.4 mappings. The routing table indicates that the network 111.111.111.4 is reachable via 111.12.0.2 (R3):

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@R2] /ip/route&gt; print where dst-address=111.111.111.4</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: D - DYNAMIC; A - ACTIVE; o, y - COPY</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Columns: DST-ADDRESS, GATEWAY, DISTANCE</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">DST-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GATEWAY&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DISTANCE</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">DAo 111.111.111.4/32&nbsp; 111.12.0.2%ether3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 110</code></div></div></td></tr></tbody></table>

And if we look again at the remote mapping table, the only active mapping is the one received from R3 with assigned label 19. This implies that when R2 when routing traffic to this network, will impose label 19.

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">17&nbsp; D main&nbsp; 111.111.111.4&nbsp;&nbsp;&nbsp; 111.12.0.2&nbsp; 19&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.3:0</code></div></div></td></tr></tbody></table>

  

  

Label switching rules can be seen in the forwarding table:

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@R2] /mpls/forwarding-table&gt; print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: L, V - VPLS</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Columns: LABEL, VRF, PREFIX, NEXTHOPS</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">#&nbsp;&nbsp; LABEL&nbsp; VRF&nbsp;&nbsp; PREFIX&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NEXTHOPS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">0 L&nbsp;&nbsp;&nbsp; 16&nbsp; main&nbsp; 10.0.0.0/8&nbsp;&nbsp;&nbsp;&nbsp; { nh=10.155.130.1; interface=ether1 }&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text plain">1 L&nbsp;&nbsp;&nbsp; 18&nbsp; main&nbsp; 111.111.111.3&nbsp; { label=impl-null; nh=111.12.0.2; interface=ether3 }</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain">2 L&nbsp;&nbsp;&nbsp; 19&nbsp; main&nbsp; 111.111.111.4&nbsp; { label=19; nh=111.12.0.2; interface=ether3 }&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text plain">3 L&nbsp;&nbsp;&nbsp; 20&nbsp; main&nbsp; 111.13.0.0/24&nbsp; { label=impl-null; nh=111.12.0.2; interface=ether3 }</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text plain">4 L&nbsp;&nbsp;&nbsp; 17&nbsp; main&nbsp; 111.111.111.1&nbsp; { label=impl-null; nh=111.11.0.1; interface=ether2 }</code></div></div></td></tr></tbody></table>

If we take a look at rule number 2, the rule says that when R2 received the packet with label 19, it will change the label to new label 19 (assigned by the R3).

As you can see from this example it is not mandatory that labels along the path should be unique.

  

Now if we look at the forwarding table of R3:

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@R3] /mpls/forwarding-table&gt; print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: L, V - VPLS</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Columns: LABEL, VRF, PREFIX, NEXTHOPS</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">#&nbsp;&nbsp; LA&nbsp; VRF&nbsp;&nbsp; PREFIX&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NEXTHOPS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">0 L 19&nbsp; main&nbsp; 111.111.111.4&nbsp; { label=impl-null; nh=111.13.0.2; interface=ether3 }</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text plain">1 L 17&nbsp; main&nbsp; 111.11.0.0/24&nbsp; { label=impl-null; nh=111.12.0.1; interface=ether2 }</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain">2 L 16&nbsp; main&nbsp; 111.111.111.2&nbsp; { label=impl-null; nh=111.12.0.1; interface=ether2 }</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text plain">3 L 18&nbsp; main&nbsp; 111.111.111.1&nbsp; { label=17; nh=111.12.0.1; interface=ether2 }</code></div></div></td></tr></tbody></table>

Rule number 0, shows that the out label is "**impl-null**". The reason for this is that R3 is the last hop before 111.111.111.4 will be reachable and there is no need to swap to any real label. It is known that R4 is the egress point for the 111.111.111.4 network (router is the egress point for directly connected networks because the next hop for traffic is not MPLS router), therefore it advertises the "implicit null" label for this route. This tells R3 to forward traffic for the destination 111.111.111.4/32 to R4 unlabelled, which is exactly what R3 forwarding table entry tells.

Action, when the label is not swapped to any real label, is called **Penultimate hop popping,** it ensures that routers do not have to do unnecessary label lookup when it is known in advance that the router will have to route the packet.

  

# Using traceroute in MPLS networks

RFC4950 introduces extensions to the ICMP protocol for MPLS. The basic idea is that some ICMP messages may carry an MPLS "label stack object" (a list of labels that were on the packet when it caused a particular ICMP message). ICMP messages of interest for MPLS are Time Exceeded and Need Fragment.

MPLS label carries not only label value, but also TTL field. When imposing a label on an IP packet, MPLS TTL is set to value in the IP header, when the last label is removed from the IP packet, IP TTL is set to value in MPLS TTL. Therefore MPLS switching network can be diagnosed by means of a traceroute tool that supports MPLS extension.

For example, the traceroute from R4 to R1 looks like this:

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@R1] /mpls/ldp/neighbor&gt; /tool traceroute 111.111.111.4 src-address=111.111.111.1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Columns: ADDRESS, LOSS, SENT, LAST, AVG, BEST, WORST, STD-DEV, STATUS</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">#&nbsp; ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; LOSS&nbsp; SENT&nbsp; LAST&nbsp;&nbsp; AVG&nbsp; BEST&nbsp; WORST&nbsp; STD-DEV&nbsp; STATUS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">1&nbsp; 111.11.0.2&nbsp;&nbsp;&nbsp;&nbsp; 0%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2&nbsp; 0.7ms&nbsp; 0.7&nbsp; 0.7&nbsp;&nbsp; 0.7&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp; &lt;MPLS:L=19,E=0&gt;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">2&nbsp; 111.12.0.2&nbsp;&nbsp;&nbsp;&nbsp; 0%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2&nbsp; 0.4ms&nbsp; 0.4&nbsp; 0.4&nbsp;&nbsp; 0.4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp; &lt;MPLS:L=19,E=0&gt;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text plain">3&nbsp; 111.111.111.4&nbsp; 0%&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2&nbsp; 0.5ms&nbsp; 0.5&nbsp; 0.5&nbsp;&nbsp; 0.5&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div></div></td></tr></tbody></table>

  

Traceroute results show MPLS labels on the packet when it produced ICMP Time Exceeded. The above means: that when R3 received a packet with MPLS TTL 1, it had label 18 on it. This match advertised label by R3 for 111.111.111.4. In the same way, R2 observed label 17 on the packet on the next traceroute iteration - R3 switched label 17 to label 17, as explained above. R1 received packet without labels - R2 did penultimate hop popping as explained above.

  

## Drawbacks of using traceroute in MPLS network

### Label switching ICMP errors

One of the drawbacks of using traceroute in MPLS networks is the way MPLS handles produced ICMP errors. In IP networks ICMP errors are simply routed back to the source of the packet that caused the error. In an MPLS network, it is possible that a router that produces an error message does not even have a route to the source of the IP packet (for example in the case of asymmetric label switching paths or some kind of MPLS tunneling, e.g. to transport MPLS VPN traffic).

Due to this produced ICMP errors are not routed to the source of the packet that caused the error but switched further along the label switching path, assuming that when the label switching path endpoint will receive an ICMP error, it will know how to properly route it back to the source.

This causes the situation, that traceroute in MPLS network can not be used the same way as in IP network - to determine failure point in the network. If the label switched path is broken anywhere in the middle, no ICMP replies will come back, because they will not make it to the far endpoint of the label switching path.

### Penultimate hop popping and traceroute source address

A thorough understanding of penultimate hop behavior and routing is necessary to understand and avoid problems that penultimate hop popping causes to traceroute.

In the example setup, a regular traceroute from R5 to R1 would yield the following results:

```
[admin@R5] > /tool traceroute 9.9.9.1
     ADDRESS                                    STATUS
   1         0.0.0.0 timeout timeout timeout
   2         2.2.2.2 37ms 4ms 4ms
                      mpls-label=17
   3         9.9.9.1 4ms 2ms 11ms

```

compared to:

```
[admin@R5] > /tool traceroute 9.9.9.1 src-address=9.9.9.5
     ADDRESS                                    STATUS
   1         4.4.4.3 15ms 5ms 5ms
                      mpls-label=17
   2         2.2.2.2 5ms 3ms 6ms
                      mpls-label=17
   3         9.9.9.1 6ms 3ms 3ms

```

The reason why the first traceroute does not get a response from R3 is that by default traceroute on R5 uses source address 4.4.4.5 for its probes because it is the preferred source for a route over which next-hop to 9.9.9.1/32 is reachable:

```
[admin@R5] > /ip route print
Flags: X - disabled, A - active, D - dynamic,
C - connect, S - static, r - rip, b - bgp, o - ospf, m - mme,
B - blackhole, U - unreachable, P - prohibit
 #      DST-ADDRESS        PREF-SRC        G GATEWAY         DISTANCE             INTERFACE
 ...
 3 ADC  4.4.4.0/24         4.4.4.5                           0                    ether1
 ...
 5 ADo  9.9.9.1/32                         r 4.4.4.3         110                  ether1
 ...

```

When the first traceroute probe is transmitted (source: 4.4.4.5, destination 9.9.9.1), R3 drops it and produces an ICMP error message (source 4.4.4.3 destination 4.4.4.5) that is switched all the way to R1. R1 then sends ICMP error back - it gets switched along the label switching path to 4.4.4.5.

R2 is the penultimate hop popping router for network 4.4.4.0/24 because 4.4.4.0/24 is directly connected to R3. Therefore R2 removes the last label and sends ICMP error to R3 unlabelled:

```
[admin@R2] > /mpls forwarding-table print
 # IN-LABEL             OUT-LABELS           DESTINATION        INTERFACE            NEXTHOP
 ...
 3 19                                        4.4.4.0/24         ether2               2.2.2.3
 ...

```

R3 drops the received IP packet because it receives a packet with its own address as a source address. ICMP errors produced by following probes come back correctly because R3 receives unlabelled packets with source addresses 2.2.2.2 and 9.9.9.1, which are acceptable to a route.

Command:

```
[admin@R5] > /tool traceroute 9.9.9.1 src-address=9.9.9.5
 ...

```

produces expected results, because the source address of traceroute probes is 9.9.9.5. When ICMP errors are traveling back from R1 to R5, the penultimate hop popping for the 9.9.9.5/32 network happens at R3, therefore it never gets to route packet with its own address as a source address.

# Optimizing label distribution

## Label binding filtering

During the implementation of the given example setup, it has become clear that not all label bindings are necessary. For example, there is no need to exchange IP route label bindings between R1 and R3 or R2 and R4, as there is no chance they will ever be used. Also, if the given network core is providing connectivity only for mentioned customer ethernet segments, there is no real use to distribute labels for networks that connect routers between themselves, the only routes that matter are /32 routes to endpoints or attached customer networks.

Label binding filtering can be used to distribute only specified sets of labels to reduce resource usage and network load.

There are 2 types of label binding filters:

-   which label bindings should be advertised to LDP neighbors, configured in the `/mpls ldp advertise-filter` menu
-   which label bindings should be accepted from LDP neighbors, configured in `/mpls ldp accept-filter` menu

Filters are organized in the ordered list, specifying prefixes that must include the prefix that is tested against the filter and neighbor (or wildcard).

In the given example setup all routers can be configured so that they advertise labels only for routes that allow reaching the endpoints of tunnels. For this 2 advertise filters need to be configured on all routers:

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/mpls ldp advertise-filter </code><code class="ros functions">add </code><code class="ros value">prefix</code><code class="ros plain">=111.111.111.0/24</code> <code class="ros value">advertise</code><code class="ros plain">=yes</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/mpls ldp advertise-filter </code><code class="ros functions">add </code><code class="ros value">prefix</code><code class="ros plain">=0.0.0.0/0</code> <code class="ros value">advertise</code><code class="ros plain">=no</code></div></div></td></tr></tbody></table>

  

  

This filter causes routers to advertise only bindings for routes that are included by the 111.111.111.0/24 prefix which covers loopbacks (111.111.111.1/32, 111.111.111.2/32, etc). The second rule is necessary because the default filter results when no rule matches are to allow the action in question.

In the given setup there is no need to set up accept filter because by convention introduced by 2 abovementioned rules no LDP router will distribute unnecessary bindings.

Note that filter changes do not affect existing mappings, so to take the filter into effect, connections between neighbors need to be reset. either by removing neighbors from the LDP neighbor table or by restarting the LDP instance.

So on R2, for example, we get:

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@R2] /mpls/ldp/remote-mapping&gt; print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: I - INACTIVE; D - DYNAMIC</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Columns: VRF, DST-ADDRESS, NEXTHOP, LABEL, PEER</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">#&nbsp;&nbsp;&nbsp; VRF&nbsp;&nbsp; DST-ADDRESS&nbsp;&nbsp;&nbsp; NEXTHOP&nbsp;&nbsp;&nbsp;&nbsp; LABEL&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PEER&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">0 ID main&nbsp; 111.111.111.2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 17&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.3:0</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text plain">1 ID main&nbsp; 111.111.111.1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 16&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.3:0</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain">2&nbsp; D main&nbsp; 111.111.111.3&nbsp; 111.12.0.2&nbsp; impl-null&nbsp; 111.111.111.3:0</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text plain">3&nbsp; D main&nbsp; 111.111.111.4&nbsp; 111.12.0.2&nbsp; 18&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.3:0</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text plain">4 ID main&nbsp; 111.111.111.2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 16&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.1:0</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text plain">5&nbsp; D main&nbsp; 111.111.111.1&nbsp; 111.11.0.1&nbsp; impl-null&nbsp; 111.111.111.1:0</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="text plain">6 ID main&nbsp; 111.111.111.3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 17&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.1:0</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="text plain">7 ID main&nbsp; 111.111.111.4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 18&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 111.111.111.1:0</code></div></div></td></tr></tbody></table>

  

# LDP on Ipv6 and Dual-Stack links

RouterOS implements RFC 7552 to support LDP on dual-stack links.

Supported AFIs can be selected by LDP instance, as well as explicitly configured per LDP interface.

[?](https://help.mikrotik.com/docs/display/ROS/LDP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/mpls ldp</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">afi</code><code class="ros plain">=ip,ipv6</code> <code class="ros value">lsr-id</code><code class="ros plain">=111.111.111.1</code> <code class="ros value">preferred-afi</code><code class="ros plain">=ipv6</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/mpls ldp interface</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">afi</code><code class="ros plain">=ip</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether3</code> <code class="ros value">afi</code><code class="ros plain">=ipv6</code></div></div></td></tr></tbody></table>

The example above enables LDP instance to use IPv4 and IPv6 address families and sets the preference to IPv6 with `preferred-afi` parameter. LDP interface configuration on the other hand explicitly sets that **ether2** supports only IPv4 and **ether3** supports only IPv6.

  

The main question occurs how AFI is selected when there are a mix of different AFIs and what if one of the supported AFIs flaps. 

The logic behind sending hellos is as follows:

-   if an interface has only one AFI:
    -   dual-stack element is not sent
    -   sends hello only if there is an IP address on the interface from the corresponding AFI.
-   If an interface has both AFIs:
    -   dual-stack element is always sent and contains the value from preferred-afi
    -   sends hellos on each AFI if a corresponding address is present on the interface.

  

From all received hellos peer determines which AFI to use for connection and for which AFIs to bind and send labels. For LDP to be able to use a specific AFI, receiving hello for that specific AFI is mandatory. Hello packet contains the transport address necessary for proper LDP operation. By comparing received AFI addresses, is determined active/passive role.

The logic behind receiving and processing hellos is as follows:

-   if the LDP instance has only one AFI (it means that all interfaces can have only that specific AFI operational):
    -   drop hellos from not supported AFI
    -   ignore/forget the dual-stack element for the hello packet
    -   the role is determined only for this one specific AFI
    -   labels are sent only for this one specific AFI
-   if the LDP instance has both AFIs (interfaces can have different combinations of supported AFIs):
    -   drop hellos from AFI that are not configured as supported on the interface.
    -   ignore/forget the dual-stack element (preference is not taken into account) for hello packets, if an interface has only one supported AFI.
    -   drop hello if received preference in dual-stack element does not match configured `preferred-afi`.

  

If there are changes in hello packets, the existing session is terminated only in case if address family used by labels is changed, otherwise, the session is preserved.

Dual-stack element in hello packets is set only if an interface is determined to be dual-stack compatible:

-   Normally such an interface should be able to receive hellos from both AFIs,
    -   Before proceeding LDP should wait for hello from the preferred AFI.
    -   if hello is received only from one AFI:
        -   if hello from preferred AFI is not received then it is considered an error. 
        -   otherwise, wait for missing hello for x seconds (x = 3 \* hello-interval)
            -   if missing hello appears within a time interval consider peer to be dual-stack
            -   if missing hello did not appear, then consider peer to be single-stack
            -   if missing hello appeared after the time interval then restart the session.
-   the dual-stack element indicates that LDP wants to distribute labels for both AFIs.

In summary, the following combinations of AFIs and dual-stack element (ds6) are possible assuming that preferred-afi=ipv6:

1.  ipv4 - wait X seconds, if no changes, then use the IPv4 LDP session and distribute IPv4 labels
2.  ipv4+ds6 - wait for IPv6 hello, dual-stack element indicates that there should be IPv6
3.  ipv6 - wait X seconds, if no changes, then use the IPv6 LDP session and distribute IPv6 labels
4.  ipv6+ds6 - use IPv6 LDP session and distribute IPv6 labels
5.  ipv4,ipv6 - use IPv6 LDP session and distribute IPv4 and IPv6 labels
6.  ipv4,ipv6+ds6 - use IPv6 LDP session and distribute IPv4 and IPv6 labels

# Property Reference

## LDP Instance

  

**Sub-menu:** `/mpls`

**Properties**

| 
Property

 | 

Description

|     |
| --- |  |
|     |

Property

 | 

Description

|                                                |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **afi (**_ip                                   | ipv6_**;** Default: **)**                                                                                                       | Determines supported address families by the instance.                                                                                               |
| **comments** (_string_; Default: )             | Short description of the entry                                                                                                  |
| **disabled** (_yes                             | no_; Default: **no**)                                                                                                           |
|                                                |
| **distribute-for-default** (_yes               | no_; Default: no)                                                                                                               | Defines whether to map label for the default route.                                                                                                  |
| **hop-limit** (_integer\[0..255\]_; Default: ) | Max hop limit used for loop detection. Works in combination with the **loop-detect** property.                                  |
| **loop-detect** (_yes                          | no_; Default: )                                                                                                                 | Defines whether to run LSP loop detection. Will not work correctly if not enabled on all LSRs. Should be used only on non-TTL networks such as ATMs. |
| **lsr-id** (_IP_; Default: )                   | Unique label switching router's ID.                                                                                             |
| **path-vector-limit** (_IP_; Default: )        | Max path vector limit used for loop detection. Works in combination with the **loop-detect** property.                          |
| **preferred-afi** (ip                          | ipv6; Default: **ipv6**)                                                                                                        | Determining which address family connection is preferred. Value is also set in dual-stack element (if used).                                         |
| **transport-addresses** (_IP_; Default: )      | Specifies LDP session connections origin addresses and also advertises these addresses as transport addresses to LDP neighbors. |
| **use-explicit-null** (_yes                    | no_; Default: no)                                                                                                               | Whether to distribute explicit-null label bindings.                                                                                                  |
| **vrf (**_name_; Default: main**)**            | Name of the VRF table this instance will operate on.                                                                            |

## Interface

**Sub-menu:** `/mpls ldp interface`

  

| 
Property

 | 

Description

|     |
| --- |  |
|     |

Property

 | 

Description

|                                                    |
| -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **afi (**_ip                                       | ipv6_**;** Default: **)**                                                                                                         | Determines interface address family. Only AFIs that are configured as supported by the instance is taken into account. If the value is not explicitly specified then it is considered to be equal to the instance-supported AFIs. |
| **accept-dynamic-neighbors** (_yes                 | no_; Default:)                                                                                                                    | Defines whether to discover neighbors dynamically or use only statically configured in [LDP neighbors menu](https://help.mikrotik.com/docs/display/ROS/LDP#LDP-Neighbors)                                                         |
| **comments** (_string_; Default: )                 | Short description of the entry                                                                                                    |
| **disabled** (_yes                                 | no_; Default: **no**)                                                                                                             |
|                                                    |
| **hello-interval** (_string_; Default: )           | The interval between hello packets that the router sends out on specified interface/s. The default value is 5s.                   |
| **hold-time** (_string_; Default: )                | Specifies the interval after which a neighbor discovered on the interface is declared as not reachable. The default value is 15s. |
| **interface** (_string_; Default: )                | Name of the interface or interface list where LDP will be listening.                                                              |
| **transport-addresses** (List of _IPs_; Default: ) | Used transport addresses if differs from LDP Instance settings.                                                                   |

  

## Neighbors

**Sub-menu:** `/mpls ldp neighbor`

List of discovered and statically configured LDP neighbors.

**Properties**

| 
Property

 | 

Description

|     |
| --- |  |
|     |

Property

 | 

Description

|                                    |
| ---------------------------------- | ------------------------------ |
| **comments** (_string_; Default: ) | Short description of the entry |
| **disabled** (_yes                 | no_; Default: **no**)          |
|                                    |
| **send-targeted** (_yes            | no_; Default: )                | Specifies whether to try to send targeted hellos, used for targeted (not directly connected) LDP sessions. |
| **transport** (_IP_; Default: )    | Remote transport address.      |

  

**Read-only Properties**

| 
Property

 | 

Description

|     |
| --- |  |
|     |

Property

 | 

Description

|                                   |
| --------------------------------- | -------------------------------------------- |
| **active-connect** (_yes          | no_)                                         |
|                                   |
| **addresses** (_list of IPs_)     | List of discovered addresses on the neighbor |
| **inactive** (_yes                | no_)                                         | Whether binding is active and can be selected as a candidate for forwarding. |
| **dynamic** (_yes                 | no_)                                         | Whether entry was dynamically added                                          |
| **local-transport** (_IP_)        | Selected local transport address.            |
| **on-demand** (_yes               | no_)                                         |
|                                   |
| **operational** (_yes             | no_)                                         | Indicates whether the peer is operational.                                   |
| **passive** (_yes                 | no_)                                         | Indicates whether the peer is in a passive role.                             |
| **passive-wait** (_yes            | no_)                                         |
|                                   |
| **path-vector-limit** (_integer_) |
|                                   |
| **peer** (_IP:integer_)           | LSR-ID and label space of the neighbor       |
| **sending-targeted-hello**(_yes   | no_)                                         | Whether targeted hellos are being sent to the neighbor.                      |
| **throttled** (_yes               | no_)                                         |
|                                   |
| **used-afi** (_yes                | no_)                                         | Used transport AFI                                                           |
| **vpls** (_yes                    | no_)                                         | Whether neighbor is used by VPLS tunnel                                      |

## Accept Filter

**Sub-menu:** `/mpls ldp accept-filter`

List of label bindings that should be accepted from LDP neighbors.

| 
Property

 | 

Description

|     |
| --- |  |
|     |

Property

 | 

Description

|                                    |
| ---------------------------------- | -------------------------------------- |
| **accept** (_yes                   | no_; Default: )                        | Whether to accept label bindings from the neighbors for the specified prefix. |
| **comments** (_string_; Default: ) | Short description of the entry         |
| **disabled** (_yes                 | no_; Default: **no**)                  |
|                                    |
| **neighbor**(_string_; Default: )  | Neighbor to which this filter applies. |
| **prefix** (_IP/mask_; Default: )  | Prefix to match.                       |
| **vrf** (name; Default: )          |
|                                    |

  

## Advertise Filter

**Sub-menu:** `/mpls ldp advertise-filter`

List of label bindings that should be advertised to LDP neighbors.

| 
Property

 | 

Description

|     |
| --- |  |
|     |

Property

 | 

Description

|                                    |
| ---------------------------------- | -------------------------------------- |
| **advertise** (_yes                | no_; Default: )                        | Whether to advertise label bindings to the neighbors for the specified prefix. |
| **comments** (_string_; Default: ) | Short description of the entry         |
| **disabled** (_yes                 | no_; Default: **no**)                  |
|                                    |
| **neighbor**(_string_; Default: )  | Neighbor to which this filter applies. |
| **prefix** (_IP/mask_; Default: )  | Prefix to match.                       |
| **vrf** (name; Default: )          |
|                                    |

## Local Mapping

**Sub-menu:** `/mpls local-mapping`

This sub-menu shows labels bound to the routes locally in the router. In this menu also static mappings can be configured if there is no intention to use LDP dynamically.

  
**Properties**

| 
Property

 | 

Description

|     |
| --- |  |
|     |

Property

 | 

Description

|                                        |
| -------------------------------------- | ---------------------------------------------- |
| **comments** (_string_; Default: )     | Short description of the entry                 |
| **disabled** (_yes                     | no_; Default: **no**)                          |
|                                        |
| **dst-address** (_IP/Mask_; Default: ) | Destination prefix the label is assigned to.   |
| **label** (_integer\[0..1048576\]      | alert                                          | expl-null | expl-null6 | impl-null | none_; Default: ) | Label number assigned to destination. |
| **vrf (**_name_; Default: main**)**    | Name of the VRF table this mapping belongs to. |

  
**Read-only Properties**

| 
Property

 | 

Description

|     |
| --- |  |
|     |

Property

 | 

Description

|                               |
| ----------------------------- | -------------------------------------------------------------------------- |
| **adv-path** ()               |
|                               |
| **inactive** (_yes            | no_)                                                                       | Whether binding is active and can be selected as a candidate for forwarding. |
| **dynamic** (_yes             | no_)                                                                       | Whether entry was dynamically added                                          |
| **egress** (_yes              | no_)                                                                       |
|                               |
| **gateway** (_yes             | no_)                                                                       | Whether the destination is reachable through the gateway.                    |
| **local** (_yes               | no_)                                                                       | Whether the destination is locally reachable on the router                   |
| **peers** (_IP:label\_space_) | IP address and label space of the peer to which this entry was advertised. |

## Remote Mapping

**Sub-menu:** `/mpls remote-mapping`

Sub-menu shows label bindings for routes received from other routers. Static mapping can be configured if there is no intention to use LDP dynamically. This table is used to build [Forwarding Table](https://help.mikrotik.com/docs/display/ROS/Mpls+Overview#MplsOverview-ForwardingTable)

**Properties**

| 
Property

 | 

Description

|     |
| --- |  |
|     |

Property

 | 

Description

|                                        |
| -------------------------------------- | ---------------------------------------------- |
| **comments** (_string_; Default: )     | Short description of the entry                 |
| **disabled** (_yes                     | no_; Default: **no**)                          |
|                                        |
| **dst-address** (_IP/Mask_; Default: ) | Destination prefix the label is assigned to.   |
| **label** (_integer\[0..1048576\]      | alert                                          | expl-null | expl-null6 | impl-null | none_; Default: ) | Label number assigned to destination. |
| **nexthop (**_IP_; Default:**)**       |
|                                        |
| **vrf (**_name_; Default: main**)**    | Name of the VRF table this mapping belongs to. |

  

**Read-only Properties**

| 
Property

 | 

Description

|     |
| --- |  |
|     |

Property

 | 

Description

|                     |
| ------------------- | ---- |
| **inactive** (_yes  | no_) | Whether binding is active and can be selected as a candidate for forwarding. |
| **dynamic** (_yes   | no_) | Whether entry was dynamically added                                          |
| **path** (_string_) |      |