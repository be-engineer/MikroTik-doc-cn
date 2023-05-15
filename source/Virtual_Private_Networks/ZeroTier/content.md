# Introduction

The [ZeroTier](https://www.zerotier.com/manual/) network hypervisor is a self-contained network virtualization engine that implements an Ethernet virtualization layer similar to [VXLAN](https://en.wikipedia.org/wiki/Virtual_Extensible_LAN) built atop a cryptographically secure global peer-to-peer network. It provides advanced network virtualization and management capabilities on par with an enterprise SDN switch, but across both local and wide area networks and connecting almost any kind of app or device.

MikroTik has added ZeroTier to RouterOS v7.1rc2 as a separate package for the **ARM/ARM64** architecture. 

Wait, so what can I use it for?

-   Hosting a game server at home (useful for LAN only games) or simply creating a LAN party with your friends;
-   Accessing LAN devices behind NAT directly;
-   Accessing LAN devices via SSH without opening port to the Internet;
-   Using your local Pi-Hole setup from anywhere via the Internet;

## Video tutorial

-   [ZeroTier](https://youtu.be/60uIlyF8Z5s)

# Required Network Configuration

## What ports does ZeroTier use?

It listens on three 3 UDP ports:

-   9993 - The default
-   A random, high numbered port derived from your ZeroTier address  
    
-   A random, high numbered port for use with UPnP/NAT-PMP mappings

That means your _peers_ could be listening on any port. To talk with them directly, you need to be able to send them to any port.

## Recommended Local Network and Internet Gateway Configuration

These ZeroTier recommended guidelines are consistent with the vast majority of typical deployments using commodity gateways and access points:

-   Don't restrict outbound UDP traffic.
-   Supporting either UPnP or NAT-PMP on your network can greatly improve performance by allowing ZeroTier endpoints to map external ports and avoid NAT traversal entirely.
-   IPv6 is recommended and can greatly improve direct connection reliability if supported on both ends of a direct link. If present it should be implemented without NAT (NAT is wholly unnecessary with IPv6 and only adds complexity) and with a stateful firewall that permits bidirectional UDP conversations.
-   Don't use "symmetric" NAT. Use "full cone" or "port restricted cone" NAT. Symmetric NAT is extremely hostile to peer-to-peer traffic and will degrade VoIP, video chat, games, WebRTC, and many other protocols as well as ZeroTier.
-   No more than one layer of NAT should be present between ZeroTier endpoints and the Internet. Multiple layers of NAT introduce connection instability due to chaotic interactions between states and behaviors at different levels. **No Double NAT.**
-   NATs should have a port mapping or connection timeout no shorter than 60 seconds.
-   Place no more than about 16,000 devices behind each NAT-managed external IP address to ensure that each device can map a sufficient number of ports.
-   Switches and wireless access points should allow direct local traffic between local devices. Turn off any "local isolation" features. Some switches might allow finer-grained control, and on these, it would be sufficient to allow local UDP traffic to/from 9993 (or in general).

# Configuration example

![](https://help.mikrotik.com/docs/download/attachments/83755083/ZeroTier_ilustracija.png?version=1&modificationDate=1640071414044&api=v2)

By default, ZeroTier is designed to be zero-configuration. A user can start a new ZeroTier node without having to write configuration files or provide the IP addresses of other nodes. It’s also designed to be fast. Any two devices in the world should be able to locate each other and communicate almost instantly so the following example will enable ZeroTier on RouterOS device and connect one mobile phone using the ZeroTier application.

  

1.  Register on [my.zerotier.com](https://my.zerotier.com/) and **Create A Network**, obtain the _Network ID_, in this example: _1d71939404912b40_;  
    ![](https://help.mikrotik.com/docs/download/attachments/83755083/network.jpg.png?version=1&modificationDate=1640071063702&api=v2)
2.  [Download](https://mikrotik.com/download) and Install ZeroTier NPK package in RouterOS, you can find under in the "Extra packages", upload package on the device and reboot the unit;
3.  Enable the default (official) ZeroTier instance:
    
    [?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)
    
    <table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@mikrotik] &gt; zerotier</code><code class="ros constants">/</code><code class="ros functions">enable </code><code class="ros plain">zt1</code></div></div></td></tr></tbody></table>
    
4.  Add a new network, specifying the network ID you created in the ZeroTier cloud console:
    
    [?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)
    
    <table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@mikrotik] zerotier</code><code class="ros constants">/interface/</code><code class="ros functions">add </code><code class="ros value">network</code><code class="ros plain">=1d71939404912b40</code> <code class="ros value">instance</code><code class="ros plain">=zt1</code></div></div></td></tr></tbody></table>
    
5.  Verify ZeroTier configuration:
    
    [?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)
    
    <table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; zerotier</code><code class="ros constants">/interface/</code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: R - RUNNING</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NAME, MAC-ADDRESS, NETWORK, NETWORK-NAME, STATUS</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments">#&nbsp;&nbsp; NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; MAC-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NETWORK&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NETWORK-NAME&nbsp;&nbsp;&nbsp;&nbsp; STATUS</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0 R zerotier1&nbsp; 42</code><code class="ros constants">:AC:0D:0F:C6:F6&nbsp; 1d71939404912b40&nbsp; modest_metcalfe&nbsp; OK</code></div></div></td></tr></tbody></table>
    
6.  Now you might need to allow connections from the ZeroTier interface to your router, and **optionally**, to your other LAN interfaces: 
    
    [?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)
    
    <table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall filter </code><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">in-interface</code><code class="ros plain">=zerotier1</code> <code class="ros value">place-before</code><code class="ros plain">=0</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/ip firewall filter </code><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">in-interface</code><code class="ros plain">=zerotier1</code> <code class="ros value">place-before</code><code class="ros plain">=0</code></div></div></td></tr></tbody></table>
    
7.  Install a ZeroTier client on your smartphone or computer, follow the ZeroTier manual on how to connect to the same network from there.
8.  If **"****Access Control"** is set to **"Private"**, you must authorize nodes before they become members:  
    ![](https://help.mikrotik.com/docs/download/attachments/83755083/Screenshot_2.png?version=1&modificationDate=1640071629089&api=v2)
9.  [?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)
    
    <table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; ip</code><code class="ros constants">/address/</code><code class="ros functions">print </code><code class="ros plain">where interface~</code><code class="ros string">"zero"</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: D - DYNAMIC</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: ADDRESS, NETWORK, INTERFACE</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments">#&nbsp;&nbsp; ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NETWORK&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; INTERFACE</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">3 D </code><code class="ros color1">192.168.192.105/24</code>&nbsp; <code class="ros plain">192.168.192.0&nbsp; zerotier1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros functions">ping </code><code class="ros plain">192.168.192.252 </code><code class="ros value">count</code><code class="ros plain">=3</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">SEQ HOST&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; SIZE TTL TIME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; STATUS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">0 192.168.192.252 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;56&nbsp; 64 407us&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">1 192.168.192.252 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;56&nbsp; 64 452us&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">2 192.168.192.252 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;56&nbsp; 64 451us&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros value">sent</code><code class="ros plain">=3</code> <code class="ros value">received</code><code class="ros plain">=3</code> <code class="ros value">packet-loss</code><code class="ros plain">=0%</code> <code class="ros value">min-rtt</code><code class="ros plain">=407us</code> <code class="ros value">avg-rtt</code><code class="ros plain">=436us</code> <code class="ros value">max-rtt</code><code class="ros plain">=452us</code></div></div></td></tr></tbody></table>
    

You should specify routes to specific internal subnets in the [ZeroTier cloud console](https://my.zerotier.com/), to make sure you can access those networks when connecting from other devices. 

### Peer

[?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">zerotier</code><code class="ros constants">/peer/</code></div></div></td></tr></tbody></table>

ZeroTier\`s peer is an informative section with a list of nodes that your node knows about. Nodes can not talk to each other unless they are joined and authorized on the same network.

[?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@Home] &gt; zerotier</code><code class="ros constants">/peer/</code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: INSTANCE, ZT-ADDRESS, LATENCY, ROLE, PATH</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros comments"># INSTANCE&nbsp; ZT-ADDRESS&nbsp; LATENCY&nbsp; ROLE&nbsp;&nbsp;&nbsp; PATH&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">0 zt1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 61d294b9cb&nbsp; 186ms&nbsp;&nbsp;&nbsp; PLANET&nbsp; active,preferred,</code><code class="ros color1">50.7.73.34/999</code><code class="ros plain">3,recvd:4s526ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">1 zt1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 62f865ae71&nbsp; 270ms&nbsp;&nbsp;&nbsp; PLANET&nbsp; active,preferred,</code><code class="ros color1">50.7.252.138/999</code><code class="ros plain">3,recvd:4s440ms,sent:9s766ms&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">2 zt1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 778cde7190&nbsp; 132ms&nbsp;&nbsp;&nbsp; PLANET&nbsp; active,preferred,</code><code class="ros color1">103.195.103.66/999</code><code class="ros plain">3,recvd:4s579ms,sent:9s766ms</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">3 zt1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 992fcf1db7&nbsp; 34ms&nbsp;&nbsp;&nbsp;&nbsp; PLANET&nbsp; active,preferred,</code><code class="ros color1">195.181.173.159/999</code><code class="ros plain">3,recvd:4s675ms,sent:4s712ms</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">4 zt1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 159924d630&nbsp; 130ms&nbsp;&nbsp;&nbsp; LEAF&nbsp;&nbsp;&nbsp; active,preferred,34.121.192.xx</code><code class="ros constants">/21002,recvd:3s990ms,sent:3s990ms</code></div></div></td></tr></tbody></table>

# Parameters

[?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; zerotier</code><code class="ros constants">/</code></div></div></td></tr></tbody></table>

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

|                                              |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **name** (s_tring_; default: **zt1**)        | Instance name.                                                                                              |
| **port** (_number;_ default: **9993**)       | Port number the instance listen to.                                                                         |
| **identity** (_string_; default)             | Instance 40-bit unique address.                                                                             |
| **interface** (string; default: **all)**     | List of interfaces that are used in order to discover ZeroTier peers, by using ARP and IP type connections. |
| **route-distance** (number; default: **1** ) | Route distance for routes obtained from planet/moon servers.                                                |

[?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; zerotier</code><code class="ros constants">/interface/</code></div></div></td></tr></tbody></table>

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
| ---------------------------------------------- | ------------------------------------------------- |
| **allow-default** (_string; yes                | no)_                                              | A network can override the systems default route (force VPN mode). |
| **allow-global** (_string; yes                 | no)_                                              | ZeroTier IP addresses and routes can overlap public IP space.      |
| **allow-managed** (_string; yes                | no)_                                              | ZeroTier managed IP addresses and routes are assigned.             |
| **arp-timeout** ( _number_; default: **auto**) | ARP timeouts value.                               |
| **comment** (_string_; Default: )              | Descriptive comment for the interfaces.           |
| **copy-from**                                  | Allows copying existing interfaces configuration. |
| **disable-running-check** (_string; yes        | no)_                                              | Force interface in "running" state.                                |
| **instance** (_string_; Default: **zt1**)      | ZeroTier instance name.                           |
| **name** (s_tring_; default: **zerotier1**)    | A short name.                                     |
| **network** (_string_; Default)                | 16-digit network ID.                              |

# Controller

  

RouterOS implements ZeroTier functionality in the role of a node where most of the network configuration must be done on the ZeroTier webpage dashboard. However, in situations where you would prefer to do all the configuration on your own device, RouterOS offers to host your own controller

A common misunderstanding is to conflate network controllers with root servers (planet and moons). Root servers are connection facilitators that operate at the **[VL1 level](https://docs.zerotier.com/zerotier/manual/#2networkhypervisoroverviewaname2a)**. Network controllers are configuration managers and certificate authorities that belong to the **[VL2 level](https://docs.zerotier.com/zerotier/manual/#22vl2theethernetvirtualizationlayeraname2_2a).** Generally, root servers don’t join or control virtual networks and network controllers are not root servers, though it is possible to have a node do both.

[?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/zerotier/controller/</code></div></div></td></tr></tbody></table>

Every ZeroTier instance has a self-hosting network controller that can be used to host virtual networks. A controller is responsible for admitting members to the network, and issuing default configuration information including certificates. Controllers can in theory host up to 2^24 networks and serve many millions of devices (or more), but we recommend spreading large numbers of networks across many controllers for load balancing and fault tolerance reasons.

## Parameters

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
| --------------------------------- | --------------------------------------- |
| **broadcast**  _( yes             | no; Default: **yes**)_                  | Allow receiving broadcast (_FF:FF:FF:FF:FF:FF_) packets. |
| **comment** (_string_; Default: ) | Descriptive comment for the controller. |
|                                   |

**copy-from** (_string_; Default: )



 | Copies an existing item. It takes default values of a new item's properties from another item. If you do not want to make an exact copy, you can specify new values for some properties. When copying items that have names, you will usually have to give a new name to a copy. |
| **instance** (_string_; Default: **zt1**) | ZeroTier instance name.  
 |
| **ip-range** (_IP_; Default: ) | IP range, _for example, 172.16.16.1-172.16.16.254._ |
|  **ip6-6plane** _( yes | no; Default: **no**)_ | An option gives every member a /80 within a /40 network but uses NDP emulation to route _all_ IPs under that /80 to their owner. The `6plane` mode is great for use cases like Docker since it allows every member to assign IPv6 addresses within its /80 that just work instantly and globally across the network. |
| **ip6-rfc4193** _( yes | no; Default: **no**)_ | The _rfc4193_ mode gives every member a /128 on a /88 network. |
| **ip6-range** (_IPv6_; Default: ) | IPv6 range, _for example fd00:feed:feed:beef::-fd00:feed:feed:beef:ffff:ffff:ffff:ffff._ |
| **mtu** _(integer;_ Default: **2800**) | Network MTU. |
| **multicast-limit** (_integer_: Default: **32**) | Maximum recipients for a multicast packet. |
| **name** (_string_; Default: ) | A short name for this controller. |
| **network** (_string_; Default) | 16-digit network ID. |
| **private** _( yes | no; Default: **yes**)_ | Enables access control. |
| **routes** (_IP@GW_; Default: ) | Push routes in the following format:  
_Routes ::= Route\[,Routes\]_  
  _Route ::= Dst\[@Gw\]_ |

## Configuration example

In the following example, we will use RouterOS built-in ZeroTier controller to send our new network hosts appropriate certificates, credentials, and configuration information. The controller will operate from the "RouterOS Home" device and we will join in our network 3 units: mobile phone, laptop, RouterOS Office device, but theoretically, you can join up to 100 devices in one network.

![](https://help.mikrotik.com/docs/download/attachments/83755083/ZeroTier_ilustracija_2.png?version=1&modificationDate=1649918837632&api=v2)

### RouterOS Home

First, we enable the default instance which operates at the **VL1** level :

[?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@Home] </code><code class="ros constants">/zerotier&gt; </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NAME, PORT, IDENTITY.PUBLIC</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros comments"># NAME&nbsp; PORT&nbsp; IDENTITY.PUBLIC&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">;;; ZeroTier Central controller - https</code><code class="ros constants">://my.zerotier.com/</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0 zt1&nbsp;&nbsp; 9993 &nbsp;879c0b5265</code><code class="ros constants">:0:d5fd2d17805e011d9b93ce8779385e427c8f405e520eea9284809d8444de0335a817xxb21aa4ba153bfbc229ca34d94e08de96d925a4aaa19b252da546693a28</code></div></div></td></tr></tbody></table>

Now we create a new network via the controller section which will operate at the **VL2** level. Each network has its own controller and each network ID is generated from the controller address and controller ID combination.

Note that we use the **_private=yes_** option for a more secure network:

[?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@Home] </code><code class="ros constants">/zerotier&gt; controller/</code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ZT-private</code> <code class="ros value">instance</code><code class="ros plain">=zt1</code> <code class="ros value">ip-range</code><code class="ros plain">=172.27.27.10-172.27.27.20</code> <code class="ros value">private</code><code class="ros plain">=yes</code> <code class="ros value">routes</code><code class="ros plain">=172.27.27.0/24</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@Home] </code><code class="ros constants">/zerotier&gt; controller/</code><code class="ros plain">print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: INSTANCE, NAME, NETWORK, PRIVATE</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments"># INSTANCE&nbsp; NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NETWORK&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PRIVATE</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0 zt1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ZT-private&nbsp; 879c0b5265a99e4b&nbsp; yes</code></div></div></td></tr></tbody></table>

Add our new network under the interface section:

[?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@Home] </code><code class="ros constants">/zerotier&gt; interface/</code><code class="ros functions">add </code><code class="ros value">network</code><code class="ros plain">=879c0b5265a99e4b</code> <code class="ros value">name</code><code class="ros plain">=myZeroTier</code> <code class="ros value">instance</code><code class="ros plain">=zt1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@Home] </code><code class="ros constants">/zerotier&gt; interface/</code><code class="ros functions">print </code><code class="ros value">interval</code><code class="ros plain">=1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NAME, MAC-ADDRESS, NETWORK, STATUS</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments"># NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; MAC-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NETWORK&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; STATUS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0 myZeroTier&nbsp; 4A</code><code class="ros constants">:19:35:6E:00:6E&nbsp; 879c0b5265a99e4b&nbsp; ACCESS_DENIED</code></div></div></td></tr></tbody></table>

Each new peer asks for a controller to join the network, in this situation, we have _ACCESS\_DENIED_ status and we have to authorize a new peer, that is because we used the **private=yes** option.

After authorization, each member in the network receives information from the controller about new peers and approval they can exchange packets with them:

[?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@Home] </code><code class="ros constants">/zerotier&gt; controller/member/</code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NETWORK, ZT-ADDRESS</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros comments">#&nbsp; NETWORK&nbsp;&nbsp;&nbsp;&nbsp; ZT-ADDRESS</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">0&nbsp; ZT-private&nbsp; 879a0b5265</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">[admin@Home] </code><code class="ros constants">/zerotier&gt; controller/member/</code><code class="ros functions">set </code><code class="ros plain">0 </code><code class="ros value">authorized</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Verify newly configured IP address and route:

[?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@Home] </code><code class="ros constants">/zerotier&gt; /ip/address/</code><code class="ros functions">print </code><code class="ros plain">where interface~</code><code class="ros string">"Zero"</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: D - DYNAMIC</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: ADDRESS, NETWORK, INTERFACE</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments">#&nbsp;&nbsp; ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NETWORK&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; INTERFACE</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">4 D </code><code class="ros color1">172.27.27.15/24</code>&nbsp; <code class="ros plain">172.27.27.0&nbsp; myZeroTier</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">[admin@Home] </code><code class="ros constants">/zerotier&gt; /ip/route/pr where gateway~"Zero"</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: D - DYNAMIC; A - ACTIVE; c, y - COPY</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: DST-ADDRESS, GATEWAY, DISTANCE</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">DST-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp; GATEWAY&nbsp;&nbsp;&nbsp;&nbsp; DISTANCE</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">DAc </code><code class="ros color1">172.27.27.0/24</code>&nbsp; <code class="ros plain">myZeroTier&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div></div></td></tr></tbody></table>

### RouterOS Office

Configuration on the Office device. We will enable the default instance and ask a controller to join the _879c0b5265a99e4b_ network:

[?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@office] </code><code class="ros constants">/zerotier&gt; interface/</code><code class="ros functions">add </code><code class="ros value">network</code><code class="ros plain">=879c0b5265a99e4b</code> <code class="ros value">instance</code><code class="ros plain">=zt1</code> <code class="ros value">name</code><code class="ros plain">=ZT-interface</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@office] </code><code class="ros constants">/zerotier&gt; interface/</code><code class="ros functions">print </code><code class="ros value">interval</code><code class="ros plain">=1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NAME, MAC-ADDRESS, NETWORK, STATUS</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments"># NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; MAC-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NETWORK&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; STATUS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0 ZT-interface&nbsp; 4A</code><code class="ros constants">:40:1C:38:97:BA&nbsp; 879c0b5265a99e4b&nbsp; ACCESS_DENIED</code></div></div></td></tr></tbody></table>

As previously, because our network is private, we have to authorize a new peer via "RouterOS home device". After that verify from controller received IP address and route:

[?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@Home] </code><code class="ros constants">/zerotier&gt; controller/member/</code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: A - AUTHORIZED</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NETWORK, ZT-ADDRESS, IP-ADDRESS, LAST-SEEN</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments">#&nbsp;&nbsp;&nbsp; NETWORK&nbsp;&nbsp;&nbsp;&nbsp; ZT-ADDRESS&nbsp; IP-ADDRESS&nbsp;&nbsp;&nbsp; LAST-SEEN</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0 A&nbsp; ZT-private&nbsp; 879a0b5265&nbsp; 172.27.27.15&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">1 A&nbsp; ZT-private&nbsp; 554a914c7f&nbsp; 172.27.27.17&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">2 A&nbsp; ZT-private&nbsp; a83ac6032a&nbsp; 172.27.27.10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">3&nbsp;&nbsp;&nbsp; ZT-private&nbsp; deba5dc5b1&nbsp; 172.27.27.13&nbsp; 3s348ms&nbsp;</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">[admin@Home] </code><code class="ros constants">/zerotier&gt; controller/member/</code><code class="ros functions">set </code><code class="ros plain">3 </code><code class="ros value">authorized</code><code class="ros plain">=yes</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">[admin@Home] </code><code class="ros constants">/zerotier&gt; controller/member/</code><code class="ros functions">print </code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: A - AUTHORIZED</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NETWORK, ZT-ADDRESS, IP-ADDRESS, LAST-SEEN</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros comments">#&nbsp;&nbsp;&nbsp; NETWORK&nbsp;&nbsp;&nbsp;&nbsp; ZT-ADDRESS&nbsp; IP-ADDRESS&nbsp;&nbsp;&nbsp; LAST-SEEN</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros plain">0 A&nbsp; ZT-private&nbsp; 879a0b5265&nbsp; 172.27.27.15&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros plain">1 A&nbsp; ZT-private&nbsp; 554a914c7f&nbsp; 172.27.27.17&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros plain">2 A&nbsp; ZT-private&nbsp; a83ac6032a&nbsp; 172.27.27.10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros plain">3 A&nbsp; ZT-private&nbsp; deba5dc5b1&nbsp; 172.27.27.13&nbsp; 4s55ms</code></div></div></td></tr></tbody></table>

Verify via ZeroTier obtained IP address and route:

[?](https://help.mikrotik.com/docs/display/ROS/ZeroTier#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@office] </code><code class="ros constants">/zerotier&gt; /ip/address/</code><code class="ros functions">print </code><code class="ros plain">where interface~</code><code class="ros string">"ZT"</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: D - DYNAMIC</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: ADDRESS, NETWORK, INTERFACE</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments">#&nbsp;&nbsp; ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NETWORK&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; INTERFACE&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0 D </code><code class="ros color1">172.27.27.13/24</code>&nbsp; <code class="ros plain">172.27.27.0&nbsp; ZT-interface</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">[admin@office] </code><code class="ros constants">/zerotier&gt; /ip/route/</code><code class="ros functions">print </code><code class="ros plain">where gateway~</code><code class="ros string">"ZT"</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: D - DYNAMIC; A - ACTIVE; c, y - COPY</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: DST-ADDRESS, GATEWAY, DISTANCE</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">DST-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp; GATEWAY&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DISTANCE</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">DAc </code><code class="ros color1">172.27.27.0/24</code>&nbsp; <code class="ros plain">ZT-interface&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div></div></td></tr></tbody></table>

### Other devices

  
[Download the ZeroTier app](https://www.zerotier.com/download/) for your mobile phone or computer and join your newly created network:

1) Via our Laptop ZeroTier application we join the _879c0b5265a99e4b_ network;

2) User Zerotier mobile app to join the _879c0b5265a99e4b_ network;

Also all other new hosts you have to authorize under the _/zerotier/controller/member/_ section.

![](https://help.mikrotik.com/docs/download/attachments/83755083/Screenshot_7.png?version=1&modificationDate=1649918837933&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/83755083/ztAPP%20%282%29.png?version=1&modificationDate=1650365184697&api=v2)