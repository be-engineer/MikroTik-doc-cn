# Description

RouterOS allows to create multiple Virtual Routing and Forwarding instances on a single router. This is useful for BGP-based MPLS VPNs. Unlike BGP VPLS, which is OSI Layer 2 technology, BGP VRF VPNs work in Layer 3 and as such exchange IP prefixes between routers. VRFs solve the problem of overlapping IP prefixes and provide the required privacy (via separated routing for different VPNs).

It is possible to set up vrf-lite setups or use multi-protocol BGP with VPNv4 address family to distribute routes from VRF routing tables - not only to other routers, but also to different routing tables in the router itself.

# Configuration

VRF table is created in **`/ip vrf`** menu. After the VRF config is created routing table mapping is added (a dynamic table with the same name is created). Each active VRF will always have a mapped routing table.

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@arm-bgp] </code><code class="ros constants">/ip/vrf&gt; </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled; * - builtin</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp; * </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"main"</code> <code class="ros value">interfaces</code><code class="ros plain">=all</code>&nbsp;</div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">[admin@arm-bgp] </code><code class="ros constants">/routing/table&gt; </code><code class="ros functions">print</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: D - dynamic; X - disabled, I - invalid; U - used</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0 D&nbsp;&nbsp; </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"main"</code> <code class="ros plain">fib</code></div></div></td></tr></tbody></table>

Note that the order of the added VRFs is significant. To properly match which interface will belong to the VRF care must be taken to place VRFs in the correct order (matching is done starting from the top entry, just like firewall rules).

Since each VRF has mapped routing table, count of max unique VRFs is also limited to 4096.

  

Let's look at the following example:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@arm-bgp] </code><code class="ros constants">/ip/vrf&gt; </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled; * - builtin</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp; * </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"main"</code> <code class="ros value">interfaces</code><code class="ros plain">=all</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1&nbsp;&nbsp;&nbsp; </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"myVrf"</code> <code class="ros value">interfaces</code><code class="ros plain">=lo_vrf</code></div></div></td></tr></tbody></table>

Since the first entry is matching all the interfaces, the second VRF will not have any interfaces added. To fix the problem order of the entries must be changed.

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@arm-bgp] </code><code class="ros constants">/ip/vrf&gt; </code><code class="ros functions">move </code><code class="ros plain">1 0</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@arm-bgp] </code><code class="ros constants">/ip/vrf&gt; </code><code class="ros functions">print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled; * - builtin</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;&nbsp;&nbsp; </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"myVrf"</code> <code class="ros value">interfaces</code><code class="ros plain">=lo_vrf</code>&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1&nbsp; * </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"main"</code> <code class="ros value">interfaces</code><code class="ros plain">=all</code></div></div></td></tr></tbody></table>

Connected routes from the interfaces assigned to the VRF will be installed in the right routing table automatically.

When the interface is assigned to the VRF as well as connected routes it does not mean that RouterOS services will magically know which VRF to use just by specifying the IP address in the configuration. Each service needs VRF support to be added and explicit configuration. Whether the service has VRF support and has VRF configuration options refer to appropriate service documentation.

For example, let's make an SSH service to listen for connections on the interfaces belonging to the VRF:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@arm-bgp] </code><code class="ros constants">/ip/service&gt; </code><code class="ros functions">set </code><code class="ros plain">ssh </code><code class="ros value">vrf</code><code class="ros plain">=myVrf</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@arm-bgp] </code><code class="ros constants">/ip/service&gt; </code><code class="ros functions">print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X, I - INVALID</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NAME, PORT, CERTIFICATE, VRF</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros comments">#&nbsp;&nbsp; NAME&nbsp;&nbsp;&nbsp;&nbsp; PORT&nbsp; CERTIFICATE&nbsp; VRF&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">0&nbsp;&nbsp; telnet&nbsp;&nbsp;&nbsp;&nbsp; 23&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; main&nbsp;&nbsp;&nbsp;</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">1&nbsp;&nbsp; ftp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 21&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">2&nbsp;&nbsp; www&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 80&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; main&nbsp;&nbsp;&nbsp;</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">3&nbsp;&nbsp; ssh&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 22&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; myVrf</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">4 X www-ssl&nbsp;&nbsp; 443&nbsp; none&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; main&nbsp;&nbsp;&nbsp;</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">5&nbsp;&nbsp; api&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 8728&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; main&nbsp;&nbsp;&nbsp;</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">6&nbsp;&nbsp; winbox&nbsp;&nbsp; 8291&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; main&nbsp;&nbsp;&nbsp;</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros plain">7&nbsp;&nbsp; api-ssl&nbsp; 8729&nbsp; none&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; main</code></div></div></td></tr></tbody></table>

Adding routes to the VRF is as simple as specifying the routing-table parameter when adding the route and specifying in which routing table to resolve the gateway by specifying @name after the gateway IP:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip route </code><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=192.168.1.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=172.16.1.1@myVrf</code> <code class="ros value">routing-table</code><code class="ros plain">=myVrf</code></div></div></td></tr></tbody></table>

Traffic leaking between VRFs is possible if the gateway is explicitly set to be resolved in another VRF, for example:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros comments"># add route in the myVrf, but resolve the gateway in the main table</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/ip route </code><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=192.168.1.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=172.16.1.1@main</code> <code class="ros value">routing-table</code><code class="ros plain">=myVrf</code></div><div class="line number3 index2 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments"># add route in the main table, but resolve the gateway in the myVrf</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/ip route </code><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=192.168.1.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=172.16.1.1@myVrf</code></div></div></td></tr></tbody></table>

If the gateway configuration does not have an explicitly configured table to be resolved in, then it is considered, that gateway should be resolved in the "main" table.

# Supported features

Different services can be placed in specific VRF on which the service is listening for incoming or creating outgoing connections. By default, all services are using the `main` table, but it can be changed with a separate `vrf` parameter or by specifying the VRF name separated by "@" at the end of the IP address.

Below is the list of supported services.

| 
Feature



 | 

Support



 | 

Comment



 |
| --- | --- | --- |
| 

Feature



 | 

Support



 | 

Comment



 |
| --- | --- | --- |
| **[BGP](https://help.mikrotik.com/docs/display/ROS/BGP)** | + | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/routing bgp template</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bgp-template1</code> <code class="ros value">vrf</code><code class="ros plain">=vrf1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/routing bgp vpls</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bgp-vpls1</code> <code class="ros value">site-id</code><code class="ros plain">=10</code> <code class="ros value">vrf</code><code class="ros plain">=vrf1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/routing bgp vpn</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">label-allocation-policy</code><code class="ros plain">=per-vrf</code> <code class="ros value">vrf</code><code class="ros plain">=vrf1</code></div></div></td></tr></tbody></table>











 |
| **[E-mail](https://help.mikrotik.com/docs/display/ROS/E-mail)** | + | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/tool e-mail</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">address</code><code class="ros plain">=192.168.88.1</code> <code class="ros value">vrf</code><code class="ros plain">=vrf1</code></div></div></td></tr></tbody></table>











 |
| **[IP Services](https://help.mikrotik.com/docs/display/ROS/Services)** | + | 

VRF is supported for `telnet`, `www`, `ssh`, `www-ssl`, `api`, `winbox`, `api-ssl` services. The `ftp` service does not support changing the VRF.

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip service</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">telnet </code><code class="ros value">vrf</code><code class="ros plain">=vrf1</code></div></div></td></tr></tbody></table>











 |
| **[L2TP Client](https://help.mikrotik.com/docs/display/ROS/L2TP)** | + | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface l2tp-client</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">connect-to</code><code class="ros plain">=192.168.88.1@vrf1</code> <code class="ros value">name</code><code class="ros plain">=l2tp-out1</code> <code class="ros value">user</code><code class="ros plain">=l2tp-client</code></div></div></td></tr></tbody></table>











 |
| **[MPLS](https://help.mikrotik.com/docs/display/ROS/Mpls+Overview)** | + | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/mpls ldp</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">vrf</code><code class="ros plain">=vrf1</code></div></div></td></tr></tbody></table>











 |
| **[Netwatch](https://help.mikrotik.com/docs/display/ROS/Netwatch)** | 

+

 | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/tool netwatch</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">host</code><code class="ros plain">=192.168.88.1@vrf1</code></div></div></td></tr></tbody></table>











 |
| **[NTP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=40992869)** | 

+

 | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system ntp client</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">vrf</code><code class="ros plain">=vrf1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/system ntp server</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">vrf</code><code class="ros plain">=vrf1</code></div></div></td></tr></tbody></table>











 |
| **[OSPF](https://help.mikrotik.com/docs/display/ROS/OSPF)** | 

+

 | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/routing ospf instance</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">name</code><code class="ros plain">=ospf-instance-1</code> <code class="ros value">vrf</code><code class="ros plain">=vrf1</code></div></div></td></tr></tbody></table>











 |
| **[ping](https://help.mikrotik.com/docs/display/ROS/Ping)** | 

+

 | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/</code><code class="ros functions">ping </code><code class="ros plain">192.168.88.1 </code><code class="ros value">vrf</code><code class="ros plain">=vrf1</code></div></div></td></tr></tbody></table>











 |
| **[RADIUS](https://help.mikrotik.com/docs/display/ROS/RADIUS)** | 

+

 | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/radius </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.88.1@vrf1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/radius incoming </code><code class="ros functions">set </code><code class="ros value">vrf</code><code class="ros plain">=vrf1</code></div></div></td></tr></tbody></table>











 |
| **[RIP](https://help.mikrotik.com/docs/display/ROS/RIP)** | 

+

 | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/routing rip instance</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=rip-instance-1</code> <code class="ros value">vrf</code><code class="ros plain">=vrf1</code></div></div></td></tr></tbody></table>











 |
| **[RPKI](https://help.mikrotik.com/docs/display/ROS/RPKI)** | 

+

 | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/routing rpki</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">vrf</code><code class="ros plain">=vrf1</code></div></div></td></tr></tbody></table>











 |
| **[SNMP](https://help.mikrotik.com/docs/display/ROS/SNMP)** | 

+

 | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/snmp</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">vrf</code><code class="ros plain">=vrf1</code></div></div></td></tr></tbody></table>











 |
| **[EoIP](https://help.mikrotik.com/docs/display/ROS/EoIP)** | 

+

 | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface eoip</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">remote-address</code><code class="ros plain">=192.168.1.1@vrf1</code></div></div></td></tr></tbody></table>











 |
| **[IPIP](https://help.mikrotik.com/docs/display/ROS/IPIP)** | 

+

 | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ipip</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">remote-address</code><code class="ros plain">=192.168.1.1@vrf1</code></div></div></td></tr></tbody></table>











 |
| **[GRE](https://help.mikrotik.com/docs/display/ROS/GRE)** | 

+

 | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface gre</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">remote-address</code><code class="ros plain">=192.168.1.1@vrf1</code></div></div></td></tr></tbody></table>











 |
| **[SSTP-client](https://help.mikrotik.com/docs/display/ROS/SSTP#SSTP-SSTPClient)** | 

+

 | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface sstp-client</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">connect-to</code><code class="ros plain">=192.168.1.1@vrf1</code></div></div></td></tr></tbody></table>











 |
| **[OVPN-client](https://help.mikrotik.com/docs/display/ROS/OpenVPN#OpenVPN-OVPNClient)** | 

+

 | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ovpn-client</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">connect-to</code><code class="ros plain">=192.168.1.1@vrf1</code></div></div></td></tr></tbody></table>











 |
| **L2TP-ether** | 

+

 | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface l2tp-ether</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">connect-to</code><code class="ros plain">=192.168.2.2@vrf</code></div></div></td></tr></tbody></table>











 |
| **[VXLAN](https://help.mikrotik.com/docs/display/ROS/VXLAN)** | 

+

 | 

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface vxlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">vni</code><code class="ros plain">=10</code> <code class="ros value">vrf</code><code class="ros plain">=vrf1</code></div></div></td></tr></tbody></table>











 |

# Examples

## Simple VRF-Lite setup

Let's consider a setup where we need two customer VRFs that require access to the internet:  

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=172.16.1.2/24</code> <code class="ros value">interface</code><code class="ros plain">=public</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.1.1/24</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.2.1/24</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number5 index4 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/ip route</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">gateway</code><code class="ros plain">=172.16.1.1</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros comments"># add VRF configuration</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros constants">/ip vrf</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=cust_a</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros plain">place-before 0</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=cust_b</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros plain">place-before 0</code></div><div class="line number13 index12 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros comments"># add vrf routes</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros constants">/ip route</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">gateway</code><code class="ros plain">=172.16.1.1@main</code> <code class="ros value">routing-table</code><code class="ros plain">=cust_a</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">gateway</code><code class="ros plain">=172.16.1.1@main</code> <code class="ros value">routing-table</code><code class="ros plain">=cust_b</code></div><div class="line number18 index17 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros comments"># masquerade local source</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros constants">/ip firewall nat </code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">out-interface</code><code class="ros plain">=public</code> <code class="ros value">action</code><code class="ros plain">=masquerade</code></div></div></td></tr></tbody></table>

It might be necessary to ensure that packets coming in the "public" interface can actually reach the correct VRF.   
This can be solved by marking new connections originated by the VRF customers and steering the traffic by routing marks of incoming packets on the "public" interface.

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros comments"># mark new customer connections</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/ip firewall mangle</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=mark-connection</code> <code class="ros value">chain</code><code class="ros plain">=prerouting</code> <code class="ros value">connection-state</code><code class="ros plain">=new</code> <code class="ros value">new-connection-mark</code><code class="ros plain">=\</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">cust_a_conn </code><code class="ros value">src-address</code><code class="ros plain">=192.168.1.0/24</code> <code class="ros value">passthrough</code><code class="ros plain">=no</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=mark-connection</code> <code class="ros value">chain</code><code class="ros plain">=prerouting</code> <code class="ros value">connection-state</code><code class="ros plain">=new</code> <code class="ros value">new-connection-mark</code><code class="ros plain">=\</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">cust_b_conn </code><code class="ros value">src-address</code><code class="ros plain">=192.168.2.0/24</code> <code class="ros value">passthrough</code><code class="ros plain">=no</code></div><div class="line number7 index6 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros comments"># mark routing</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall mangle&nbsp;</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=mark-routing</code> <code class="ros value">chain</code><code class="ros plain">=prerouting</code> <code class="ros value">connection-mark</code><code class="ros plain">=cust_a_conn</code> <code class="ros plain">\</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">in-interface</code><code class="ros plain">=public</code> <code class="ros value">new-routing-mark</code><code class="ros plain">=cust_a</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=mark-routing</code> <code class="ros value">chain</code><code class="ros plain">=prerouting</code> <code class="ros value">connection-mark</code><code class="ros plain">=cust_b_conn</code> <code class="ros plain">\</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">in-interface</code><code class="ros plain">=public</code> <code class="ros value">new-routing-mark</code><code class="ros plain">=cust_b</code></div></div></td></tr></tbody></table>

## Static inter-VRF routes

In general, it is recommended that all routes between VRF should be exchanged using BGP local import and export functionality. If that is not enough, static routes can be used to achieve this so-called route leaking.

There are two ways to install a route that has a gateway in a different routing table than the route itself.

The first way is to explicitly specify the routing table in the gateway field when adding a route. This is only possible when leaking a route and gateway from the "main" routing table to a different routing table (VRF). Example:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros comments"># add route to 5.5.5.0/24 in 'vrf1' routing table with gateway in the main routing table</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=5.5.5.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=10.3.0.1@main</code> <code class="ros value">routing-table</code><code class="ros plain">=vrf1</code></div></div></td></tr></tbody></table>

  

The second way is to explicitly specify the interface in the gateway field. The interface specified can belong to a VRF instance. Example:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros comments"># add route to 5.5.5.0/24 in the main routing table with gateway at 'ether2' VRF interface</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=5.5.5.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=10.3.0.1%ether2</code> <code class="ros value">routing-table</code><code class="ros plain">=main</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros comments"># add route to 5.5.5.0/24 in the main routing table with 'ptp-link-1' VRF interface as gateway</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=5.5.5.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=ptp-link-1</code> <code class="ros value">routing-table</code><code class="ros plain">=main</code></div></div></td></tr></tbody></table>

  

As can be observed, there are two variations possible - to specify gateway as _ip\_address%interface_ or to simply specify an _interface_. The first should be used for broadcast interfaces in most cases. The second should be used for point-to-point interfaces, and also for broadcast interfaces, if the route is a connected route in some VRF. For example, if you have an address `1.2.3.4/24` on interface _ether2_ that is put in a VRF, there will be a connected route to `1.2.3.0/24` in that VRF's routing table. It is acceptable to add a static route `1.2.3.0/24` in a different routing table with an interface-only gateway, even though _ether2_ is a broadcast interface:

  

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=1.2.3.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=ether2</code> <code class="ros value">routing-table</code><code class="ros plain">=main</code></div></div></td></tr></tbody></table>

## The simplest MPLS VPN setup

![](https://help.mikrotik.com/docs/download/attachments/328206/L3vpn-simple.png?version=2&modificationDate=1621329532209&api=v2)

In this example, a rudimentary MPLS backbone (consisting of two Provider Edge (PE) routers PE1 and PE2) is created and configured to forward traffic between Customer Edge (CE) routers CE1 and CE2 routers that belong to _cust-one_ VPN.

### CE1 Router

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.1.1.1/24</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros comments"># use static routing</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip route </code><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=10.3.3.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=10.1.1.2</code></div></div></td></tr></tbody></table>

  

### CE2 Router

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.3.3.4/24</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/ip route </code><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=10.1.1.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=10.3.3.3</code></div></div></td></tr></tbody></table>

  

### PE1 Router

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=lobridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/ip address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.1.1.2/24</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.2.2.2/24</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/ip address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.5.5.2/32</code> <code class="ros value">interface</code><code class="ros plain">=lobridge</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/ip vrf </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=cust-one</code> <code class="ros value">interfaces</code><code class="ros plain">=ether1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/mpls ldp </code><code class="ros functions">add </code><code class="ros value">enabled</code><code class="ros plain">=yes</code> <code class="ros value">transport-address</code><code class="ros plain">=10.5.5.2</code> <code class="ros value">lsr-id</code><code class="ros plain">=10.5.5.2</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros constants">/mpls ldp interface </code><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros constants">/routing bgp template </code><code class="ros functions">set </code><code class="ros plain">default </code><code class="ros value">as</code><code class="ros plain">=65000</code></div><div class="line number9 index8 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros constants">/routing bgp vpn</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">vrf</code><code class="ros plain">=cust-one</code> <code class="ros plain">\</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">route-distinguisher</code><code class="ros plain">=1.1.1.1:111</code> <code class="ros plain">\</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">import.route-targets</code><code class="ros plain">=1.1.1.1:111</code> <code class="ros plain">\</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">import.router-id</code><code class="ros plain">=cust-one</code> <code class="ros plain">\</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">export.redistribute</code><code class="ros plain">=connected</code> <code class="ros plain">\</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">export.route-targets</code><code class="ros plain">=1.1.1.1:111</code> <code class="ros plain">\</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">label-allocation-policy</code><code class="ros plain">=per-vrf</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros constants">/routing bgp connection</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">template</code><code class="ros plain">=default</code> <code class="ros value">remote.address</code><code class="ros plain">=10.5.5.3</code> <code class="ros value">address-families</code><code class="ros plain">=vpnv4</code> <code class="ros value">local.address</code><code class="ros plain">=10.5.5.2</code></div><div class="line number20 index19 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros comments"># add route to the remote BGP peer's loopback address</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros constants">/ip route </code><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=10.5.5.3/32</code> <code class="ros value">gateway</code><code class="ros plain">=10.2.2.3</code></div></div></td></tr></tbody></table>

  

  

### PE2 Router (Cisco)

  

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">ip vrf cust-one</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">rd 1.1.1.1</code><code class="ros constants">:111</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">route-target </code><code class="ros functions">export </code><code class="ros plain">1.1.1.1</code><code class="ros constants">:111</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">route-target </code><code class="ros functions">import </code><code class="ros plain">1.1.1.1</code><code class="ros constants">:111</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">exit</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">interface Loopback0</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">ip address 10.5.5.3 255.255.255.255</code></div><div class="line number9 index8 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">mpls ldp router-id Loopback0 force</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">mpls label protocol ldp</code></div><div class="line number12 index11 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros plain">interface FastEthernet0</code><code class="ros constants">/0</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros plain">ip address 10.2.2.3 255.255.255.0</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros plain">mpls ip</code></div><div class="line number16 index15 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros plain">interface FastEthernet1</code><code class="ros constants">/0</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros plain">ip vrf forwarding cust-one</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros plain">ip address 10.3.3.3 255.255.255.0</code></div><div class="line number20 index19 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros plain">router bgp 65000</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros plain">neighbor 10.5.5.2 remote-as 65000</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros plain">neighbor 10.5.5.2 update-source Loopback0</code></div><div class="line number24 index23 alt1" data-bidi-marker="true"><code class="ros plain">address-family vpnv4</code></div><div class="line number25 index24 alt2" data-bidi-marker="true"><code class="ros plain">neighbor 10.5.5.2 activate</code></div><div class="line number26 index25 alt1" data-bidi-marker="true"><code class="ros plain">neighbor 10.5.5.2 send-community both</code></div><div class="line number27 index26 alt2" data-bidi-marker="true"><code class="ros plain">exit-address-family</code></div><div class="line number28 index27 alt1" data-bidi-marker="true"><code class="ros plain">address-family ipv4 vrf cust-one</code></div><div class="line number29 index28 alt2" data-bidi-marker="true"><code class="ros plain">redistribute connected</code></div><div class="line number30 index29 alt1" data-bidi-marker="true"><code class="ros plain">exit-address-family</code></div><div class="line number31 index30 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number32 index31 alt1" data-bidi-marker="true"><code class="ros plain">ip route 10.5.5.2 255.255.255.255 10.2.2.2</code></div></div></td></tr></tbody></table>

Results

Check that VPNv4 route redistribution is working:

  

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@PE1] </code><code class="ros constants">/routing/route&gt; </code><code class="ros functions">print </code><code class="ros functions">detail </code><code class="ros plain">where </code><code class="ros value">afi</code><code class="ros plain">=</code><code class="ros string">"vpn4"</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, F - filtered, U - unreachable, A - active;</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">c - connect, s - static, r - rip, b - bgp, o - ospf, d - dhcp, v - vpn, m - modem, a - ldp-address, l - l</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">dp-mapping, g - slaac, y - bgp-mpls-vpn;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">H - hw-offloaded; + - ecmp, B - blackhole</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">Ab&nbsp;&nbsp; </code><code class="ros value">afi</code><code class="ros plain">=vpn4</code> <code class="ros value">contribution</code><code class="ros plain">=active</code> <code class="ros value">dst-address</code><code class="ros plain">=111.16.0.0/24&amp;</code><code class="ros plain">;1.1.1.1:111 </code><code class="ros value">routing-table</code><code class="ros plain">=main</code> <code class="ros value">label</code><code class="ros plain">=16</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">gateway</code><code class="ros plain">=111.111.111.4</code> <code class="ros value">immediate-gw</code><code class="ros plain">=111.13.0.2%ether9</code> <code class="ros value">distance</code><code class="ros plain">=200</code> <code class="ros value">scope</code><code class="ros plain">=40</code> <code class="ros value">target-scope</code><code class="ros plain">=30</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">belongs-to</code><code class="ros plain">=</code><code class="ros string">"bgp-VPN4-111.111.111.4"</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">bgp.peer-cache-id</code><code class="ros plain">=*2C00011</code> <code class="ros plain">.</code><code class="ros value">as-path</code><code class="ros plain">=</code><code class="ros string">"65511"</code> <code class="ros plain">.</code><code class="ros value">ext-communities</code><code class="ros plain">=rt:1.1.1.1:111</code> <code class="ros plain">.</code><code class="ros value">local-pref</code><code class="ros plain">=100</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">.</code><code class="ros value">atomic-aggregate</code><code class="ros plain">=yes</code> <code class="ros plain">.</code><code class="ros value">origin</code><code class="ros plain">=igp</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">debug.fwp-ptr</code><code class="ros plain">=0x202427E0</code></div><div class="line number12 index11 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros plain">[admin@PE1] </code><code class="ros constants">/routing/bgp/advertisements&gt; </code><code class="ros functions">print</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0 </code><code class="ros value">peer</code><code class="ros plain">=to-pe2-1</code> <code class="ros value">dst</code><code class="ros plain">=10.1.1.0/24</code> <code class="ros value">local-pref</code><code class="ros plain">=100</code> <code class="ros value">origin</code><code class="ros plain">=2</code> <code class="ros value">ext-communities</code><code class="ros plain">=rt:1.1.1.1:111</code> <code class="ros value">atomic-aggregate</code><code class="ros plain">=yes</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code>&nbsp;</div></div></td></tr></tbody></table>

Check that the 10.3.3.0 is installed in IP routes, in the cust-one route table:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@PE1] &gt; </code><code class="ros constants">/ip route </code><code class="ros functions">print </code><code class="ros plain">where </code><code class="ros value">routing-table</code><code class="ros plain">=</code><code class="ros string">"cust-one"</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: D - DYNAMIC; A - ACTIVE; c, b, y - BGP-MPLS-VPN</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: DST-ADDRESS, GATEWAY, DISTANCE</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments"># DST-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp; GATEWAY&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DISTANCE</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0 ADC </code><code class="ros color1">10.1.1.0/24</code> <code class="ros plain">ether1@cust-one&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">1 ADb </code><code class="ros color1">10.3.3.0/24</code> <code class="ros plain">10.5.5.3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 20</code></div></div></td></tr></tbody></table>

  

Let's take a closer look at IP routes in cust-one VRF. The 10.1.1.0/24 IP prefix is a connected route that belongs to an interface that was configured to belong to cust-one VRF. The 10.3.3.0/24 IP prefix was advertised via BGP as a VPNv4 route from PE2 and is imported in this VRF routing table, because our configured **import-route-targets** matched the BGP extended communities attribute it was advertised with.

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@PE1] </code><code class="ros constants">/routing/route&gt; </code><code class="ros functions">print </code><code class="ros functions">detail </code><code class="ros plain">where </code><code class="ros value">routing-table</code><code class="ros plain">=</code><code class="ros string">"cust-one"</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, F - filtered, U - unreachable, A - active;</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">c - connect, s - static, r - rip, b - bgp, o - ospf, d - dhcp, v - vpn, m - modem, a - ldp-address, l - l</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">dp-mapping, g - slaac, y - bgp-mpls-vpn;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">H - hw-offloaded; + - ecmp, B - blackhole</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">Ac&nbsp;&nbsp; </code><code class="ros value">afi</code><code class="ros plain">=ip4</code> <code class="ros value">contribution</code><code class="ros plain">=active</code> <code class="ros value">dst-address</code><code class="ros plain">=10.1.1.0/24</code> <code class="ros value">routing-table</code><code class="ros plain">=cust-one</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">gateway</code><code class="ros plain">=ether1@cust-one</code> <code class="ros value">immediate-gw</code><code class="ros plain">=ether1</code> <code class="ros value">distance</code><code class="ros plain">=0</code> <code class="ros value">scope</code><code class="ros plain">=10</code> <code class="ros value">belongs-to</code><code class="ros plain">=</code><code class="ros string">"connected"</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">local-address</code><code class="ros plain">=10.1.1.2%ether1@cust-one</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">debug.fwp-ptr</code><code class="ros plain">=0x202420C0</code></div><div class="line number10 index9 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">Ay&nbsp;&nbsp; </code><code class="ros value">afi</code><code class="ros plain">=ip4</code> <code class="ros value">contribution</code><code class="ros plain">=active</code> <code class="ros value">dst-address</code><code class="ros plain">=10.3.3.0/24</code> <code class="ros value">routing-table</code><code class="ros plain">=cust-one</code> <code class="ros value">label</code><code class="ros plain">=16</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">gateway</code><code class="ros plain">=10.5.5.3</code> <code class="ros value">immediate-gw</code><code class="ros plain">=10.2.2.3%ether2</code> <code class="ros value">distance</code><code class="ros plain">=20</code> <code class="ros value">scope</code><code class="ros plain">=40</code> <code class="ros value">target-scope</code><code class="ros plain">=30</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">belongs-to</code><code class="ros plain">=</code><code class="ros string">"bgp-mpls-vpn-1-bgp-VPN4-10.5.5.3-import"</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">bgp.peer-cache-id</code><code class="ros plain">=*2C00011</code> <code class="ros plain">.</code><code class="ros value">ext-communities</code><code class="ros plain">=rt:1.1.1.1:111</code> <code class="ros plain">.</code><code class="ros value">local-pref</code><code class="ros plain">=100</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">.</code><code class="ros value">atomic-aggregate</code><code class="ros plain">=yes</code> <code class="ros plain">.</code><code class="ros value">origin</code><code class="ros plain">=igp</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">debug.fwp-ptr</code><code class="ros plain">=0x20242840</code></div><div class="line number17 index16 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number18 index17 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros plain">[admin@PE1] </code><code class="ros constants">/routing/route&gt; </code><code class="ros functions">print </code><code class="ros functions">detail </code><code class="ros plain">where </code><code class="ros value">afi</code><code class="ros plain">=</code><code class="ros string">"vpn4"</code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, F - filtered, U - unreachable, A - active;</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros plain">c - connect, s - static, r - rip, b - bgp, o - ospf, d - dhcp, v - vpn, m - modem, a - ldp-address, l - l</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros plain">dp-mapping, g - slaac, y - bgp-mpls-vpn;</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros plain">H - hw-offloaded; + - ecmp, B - blackhole</code></div><div class="line number24 index23 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">Ay&nbsp;&nbsp; </code><code class="ros value">afi</code><code class="ros plain">=vpn4</code> <code class="ros value">contribution</code><code class="ros plain">=active</code> <code class="ros value">dst-address</code><code class="ros plain">=10.1.1.0/24&amp;</code><code class="ros plain">;1.1.1.1:111 </code><code class="ros value">routing-table</code><code class="ros plain">=main</code> <code class="ros value">label</code><code class="ros plain">=19</code></div><div class="line number25 index24 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">gateway</code><code class="ros plain">=ether1@cust-one</code> <code class="ros value">immediate-gw</code><code class="ros plain">=ether1</code> <code class="ros value">distance</code><code class="ros plain">=200</code> <code class="ros value">scope</code><code class="ros plain">=40</code> <code class="ros value">target-scope</code><code class="ros plain">=10</code></div><div class="line number26 index25 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">belongs-to</code><code class="ros plain">=</code><code class="ros string">"bgp-mpls-vpn-1-connected-export"</code></div><div class="line number27 index26 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">bgp.ext-communities</code><code class="ros plain">=rt:1.1.1.1:1111</code> <code class="ros plain">.</code><code class="ros value">atomic-aggregate</code><code class="ros plain">=no</code> <code class="ros plain">.</code><code class="ros value">origin</code><code class="ros plain">=incomplete</code></div><div class="line number28 index27 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">debug.fwp-ptr</code><code class="ros plain">=0x202426C0</code></div><div class="line number29 index28 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number30 index29 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">Ab&nbsp;&nbsp; </code><code class="ros value">afi</code><code class="ros plain">=vpn4</code> <code class="ros value">contribution</code><code class="ros plain">=active</code> <code class="ros value">dst-address</code><code class="ros plain">=10.3.3.0/24&amp;</code><code class="ros plain">;1.1.1.1:111 </code><code class="ros value">routing-table</code><code class="ros plain">=main</code> <code class="ros value">label</code><code class="ros plain">=16</code></div><div class="line number31 index30 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">gateway</code><code class="ros plain">=10.5.5.3</code> <code class="ros value">immediate-gw</code><code class="ros plain">=10.2.2.3%ether2</code> <code class="ros value">distance</code><code class="ros plain">=200</code> <code class="ros value">scope</code><code class="ros plain">=40</code> <code class="ros value">target-scope</code><code class="ros plain">=30</code></div><div class="line number32 index31 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">belongs-to</code><code class="ros plain">=</code><code class="ros string">"bgp-VPN4-10.5.5.3"</code></div><div class="line number33 index32 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">bgp.peer-cache-id</code><code class="ros plain">=*2C00011</code> <code class="ros plain">.</code><code class="ros value">ext-communities</code><code class="ros plain">=rt:1.1.1.1:111</code> <code class="ros plain">.</code><code class="ros value">local-pref</code><code class="ros plain">=100</code></div><div class="line number34 index33 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">.</code><code class="ros value">atomic-aggregate</code><code class="ros plain">=yes</code> <code class="ros plain">.</code><code class="ros value">origin</code><code class="ros plain">=igp</code></div><div class="line number35 index34 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">debug.fwp-ptr</code><code class="ros plain">=0x202427E0</code></div></div></td></tr></tbody></table>

  

The same for Cisco:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">PE2</code><code class="ros comments">#show ip bgp vpnv4 all</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">BGP table version is 5, </code><code class="ros functions">local </code><code class="ros plain">router ID is 10.5.5.3</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Status codes</code><code class="ros constants">: s suppressed, d damped, h history, * valid, &gt; best, i - internal,</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">r RIB-failure, S Stale</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">Origin codes</code><code class="ros constants">: i - IGP, e - EGP,&nbsp;? - incomplete</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">Network Next Hop Metric LocPrf Weight Path</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">Route Distinguisher</code><code class="ros constants">: 1.1.1.1:111 (default </code><code class="ros functions">for </code><code class="ros plain">vrf cust-one)</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">*&gt;i</code><code class="ros color1">10.1.1.0/24</code> <code class="ros plain">10.5.5.2 100 0&nbsp;?</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">*&gt; </code><code class="ros color1">10.3.3.0/24</code> <code class="ros plain">0.0.0.0 0 32768&nbsp;?</code></div><div class="line number10 index9 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">PE2</code><code class="ros comments">#show ip route vrf cust-one</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">Routing Table</code><code class="ros constants">: cust-one</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros plain">Codes</code><code class="ros constants">: C - connected, S - static, R - RIP, M - mobile, B - BGP</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros plain">D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros plain">N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros plain">E1 - OSPF external type 1, E2 - OSPF external type 2</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros plain">i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros plain">ia - IS-IS inter area, * - candidate default, U - per-user static route</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros plain">o - ODR, P - periodic downloaded static route</code></div><div class="line number20 index19 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros plain">Gateway of last resort is not </code><code class="ros functions">set</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros color1">10.0.0.0/24</code> <code class="ros plain">is subnetted, 1 subnets</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros plain">B 10.1.1.0 [200</code><code class="ros constants">/0] via 10.5.5.2, 00:05:33</code></div><div class="line number24 index23 alt1" data-bidi-marker="true"><code class="ros color1">10.0.0.0/24</code> <code class="ros plain">is subnetted, 1 subnets</code></div><div class="line number25 index24 alt2" data-bidi-marker="true"><code class="ros plain">C 10.3.3.0 is directly connected, FastEthernet1</code><code class="ros constants">/0</code></div></div></td></tr></tbody></table>

  

You should be able to ping from CE1 to CE2 and vice versa.

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@CE1] &gt; </code><code class="ros constants">/</code><code class="ros functions">ping </code><code class="ros plain">10.3.3.4</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">10.3.3.4 64 byte ping</code><code class="ros constants">: ttl=62 time=18 ms</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">10.3.3.4 64 byte ping</code><code class="ros constants">: ttl=62 time=13 ms</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">10.3.3.4 64 byte ping</code><code class="ros constants">: ttl=62 time=13 ms</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">10.3.3.4 64 byte ping</code><code class="ros constants">: ttl=62 time=14 ms</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">4 packets transmitted, 4 packets received, 0% packet loss</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">round-trip min</code><code class="ros constants">/avg/max = 13/14.5/18 ms</code></div></div></td></tr></tbody></table>

  

## A more complicated setup (changes only)

![](https://help.mikrotik.com/docs/download/attachments/328206/800px-L3vpn-two-customers.png?version=2&modificationDate=1621329573471&api=v2)

As opposed to the simplest setup, in this example, we have two customers: cust-one and cust-two.

We configure two VPNs for them, cust-one and cust-two respectively, and exchange all routes between them. (This is also called "route leaking").

Note that this could be not the most typical setup, because routes are usually not exchanged between different customers. In contrast, by default, it should not be possible to gain access from one VRF site to a different VRF site in another VPN. (This is the "Private" aspect of VPNs.) Separate routing is a way to provide privacy, and it is also required to solve the problem of overlapping IP network prefixes. Route exchange is in direct conflict with these two requirements but may sometimes be needed (e.g. temp. solution when two customers are migrating to a single network infrastructure).

### CE1 Router, _cust-one_

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip route </code><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=10.4.4.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=10.1.1.2</code></div></div></td></tr></tbody></table>

  

### CE2 Router, _cust-one_

  

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip route </code><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=10.4.4.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=10.3.3.3</code></div></div></td></tr></tbody></table>

CE1 Router,_cust-two_

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.4.4.5</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/ip route </code><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=10.1.1.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=10.3.3.3</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip route </code><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=10.3.3.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=10.3.3.3</code></div></div></td></tr></tbody></table>

  

### PE1 Router

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros comments"># replace the old BGP VPN with this:</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/routing bgp vpn</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">vrf</code><code class="ros plain">=cust-one</code> <code class="ros plain">\</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">export.redistribute</code><code class="ros plain">=connected</code> <code class="ros plain">\</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">route-distinguisher</code><code class="ros plain">=1.1.1.1:111</code> <code class="ros plain">\</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">import.route-targets</code><code class="ros plain">=1.1.1.1:111,2.2.2.2:222</code>&nbsp; <code class="ros plain">\</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">export.route-targets</code><code class="ros plain">=1.1.1.1:111</code></div></div></td></tr></tbody></table>

PE2 Router (Cisco)

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">ip vrf cust-one</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">rd 1.1.1.1</code><code class="ros constants">:111</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">route-target </code><code class="ros functions">export </code><code class="ros plain">1.1.1.1</code><code class="ros constants">:111</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">route-target </code><code class="ros functions">import </code><code class="ros plain">1.1.1.1</code><code class="ros constants">:111</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">route-target </code><code class="ros functions">import </code><code class="ros plain">2.2.2.2</code><code class="ros constants">:222</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">exit</code></div><div class="line number7 index6 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">ip vrf cust-two</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">rd 2.2.2.2</code><code class="ros constants">:222</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">route-target </code><code class="ros functions">export </code><code class="ros plain">2.2.2.2</code><code class="ros constants">:222</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">route-target </code><code class="ros functions">import </code><code class="ros plain">1.1.1.1</code><code class="ros constants">:111</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">route-target </code><code class="ros functions">import </code><code class="ros plain">2.2.2.2</code><code class="ros constants">:222</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros plain">exit</code></div><div class="line number14 index13 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros plain">interface FastEthernet2</code><code class="ros constants">/0</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros plain">ip vrf forwarding cust-two</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros plain">ip address 10.4.4.3 255.255.255.0</code></div><div class="line number18 index17 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros plain">router bgp 65000</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros plain">address-family ipv4 vrf cust-two</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros plain">redistribute connected</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros plain">exit-address-family</code></div></div></td></tr></tbody></table>

  

## Variation: replace the Cisco with another MT

### PE2 Mikrotik config

  

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=lobridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.2.2.3/24</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.3.3.3/24</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.4.4.3/24</code> <code class="ros value">interface</code><code class="ros plain">=ether3</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.5.5.3/32</code> <code class="ros value">interface</code><code class="ros plain">=lobridge</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros constants">/ip vrf</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=cust-one</code> <code class="ros value">interfaces</code><code class="ros plain">=ether2</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=cust-two</code> <code class="ros value">interfaces</code><code class="ros plain">=ether3</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros constants">/mpls ldp </code><code class="ros functions">add </code><code class="ros value">enabled</code><code class="ros plain">=yes</code> <code class="ros value">transport-address</code><code class="ros plain">=10.5.5.3</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros constants">/mpls ldp interface </code><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number12 index11 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros constants">/routing bgp template </code><code class="ros functions">set </code><code class="ros plain">default </code><code class="ros value">as</code><code class="ros plain">=65000</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros constants">/routing bgp vpn</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">vrf</code><code class="ros plain">=cust-one</code> <code class="ros plain">\</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">export.redistribute</code><code class="ros plain">=connected</code> <code class="ros plain">\</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">route-distinguisher</code><code class="ros plain">=1.1.1.1:111</code> <code class="ros plain">\</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">import.route-targets</code><code class="ros plain">=1.1.1.1:111,2.2.2.2:222</code> <code class="ros plain">\</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">export.route-targets</code><code class="ros plain">=1.1.1.1:111</code> <code class="ros plain">\</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">vrf</code><code class="ros plain">=cust-two</code> <code class="ros plain">\</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">export.redistribute</code><code class="ros plain">=connected</code> <code class="ros plain">\</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">route-distinguisher</code><code class="ros plain">=2.2.2.2:222</code> <code class="ros plain">\</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">import.route-targets</code><code class="ros plain">=1.1.1.1:111,2.2.2.2:222</code> <code class="ros plain">\</code></div><div class="line number24 index23 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros value">export.route-targets</code><code class="ros plain">=2.2.2.2:222</code> <code class="ros plain">\</code></div><div class="line number25 index24 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number26 index25 alt1" data-bidi-marker="true"><code class="ros constants">/routing bgp connection</code></div><div class="line number27 index26 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">template</code><code class="ros plain">=default</code> <code class="ros value">remote.address</code><code class="ros plain">=10.5.5.2</code> <code class="ros value">address-families</code><code class="ros plain">=vpnv4</code> <code class="ros value">local.address</code><code class="ros plain">=10.5.5.3</code></div><div class="line number28 index27 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number29 index28 alt2" data-bidi-marker="true"><code class="ros comments"># add route to the remote BGP peer's loopback address</code></div><div class="line number30 index29 alt1" data-bidi-marker="true"><code class="ros constants">/ip route </code><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=10.5.5.2/32</code> <code class="ros value">gateway</code><code class="ros plain">=10.2.2.2</code></div></div></td></tr></tbody></table>

Results

The output of **/ip route print** now is interesting enough to deserve detailed observation.

  

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@PE2] </code><code class="ros constants">/ip route&gt; </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, A - active, D - dynamic,</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">C - connect, S - static, r - rip, b - bgp, o - ospf, m - mme,</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">B - blackhole, U - unreachable, P - prohibit</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros comments"># DST-ADDRESS PREF-SRC GATEWAY DISTANCE</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">0 ADb </code><code class="ros color1">10.1.1.0/24</code> <code class="ros plain">10.5.5.2 recurs... 20</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">1 ADC </code><code class="ros color1">10.3.3.0/24</code> <code class="ros plain">10.3.3.3 ether2 0</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">2 ADb </code><code class="ros color1">10.4.4.0/24</code> <code class="ros plain">20</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">3 ADb </code><code class="ros color1">10.1.1.0/24</code> <code class="ros plain">10.5.5.2 recurs... 20</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">4 ADb </code><code class="ros color1">10.3.3.0/24</code> <code class="ros plain">20</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">5 ADC </code><code class="ros color1">10.4.4.0/24</code> <code class="ros plain">10.4.4.3 ether3 0</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">6 ADC </code><code class="ros color1">10.2.2.0/24</code> <code class="ros plain">10.2.2.3 ether1 0</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros plain">7 A S </code><code class="ros color1">10.5.5.2/32</code> <code class="ros plain">10.2.2.2 reacha... 1</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros plain">8 ADC </code><code class="ros color1">10.5.5.3/32</code> <code class="ros plain">10.5.5.3 lobridge 0</code></div></div></td></tr></tbody></table>

The route 10.1.1.0/24 was received from a remote BGP peer and is installed in both VRF routing tables.

The routes 10.3.3.0/24 and 10.4.4.0/24 are also installed in both VRF routing tables. Each is a connected route in one table and a BGP route in another table. This has nothing to do with their being advertised via BGP. They are simply being "advertised" to the local VPNv4 route table and locally reimported after that. Import and export **route-targets** determine in which tables they will end up.

This can be deduced from its attributes - they don't have the usual BGP properties. (Route 10.4.4.0/24.)

  

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@PE2] </code><code class="ros constants">/routing/route&gt; </code><code class="ros functions">print </code><code class="ros functions">detail </code><code class="ros plain">where </code><code class="ros value">routing-table</code><code class="ros plain">=cust-one</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">...</code></div></div></td></tr></tbody></table>

## Leaking routes between VRFs

Currently, there is no mechanism to leak routes from one VRF instance to another within the same router.

As a workaround, it is possible to create a tunnel between two locally configure loopback addresses and assign each tunnel endpoint to its own VRF. Then it is possible to run either dynamic routing protocols or set up static routes to leak between both VRFs.

The downside of this approach is that tunnel must be created between each VRF where routes should be leaked (create a full mesh), which significantly complicates configuration even if there are just several VRFs, not to mention more complicated setups.

For example, to leak routes between 5 VRFs it would require n \* ( n – 1) / 2 connections, which will lead to the setup with 20 tunnel endpoints and 20 OSPF instances on one router.

Example config with two VRFs of this method:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=dummy_custC</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=dummy_custB</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=lo1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=lo2</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=111.255.255.1</code> <code class="ros value">interface</code><code class="ros plain">=lo1</code> <code class="ros value">network</code><code class="ros plain">=111.255.255.1</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=111.255.255.2</code> <code class="ros value">interface</code><code class="ros plain">=lo2</code> <code class="ros value">network</code><code class="ros plain">=111.255.255.2</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=172.16.1.0/24</code> <code class="ros value">interface</code><code class="ros plain">=dummy_custC</code> <code class="ros value">network</code><code class="ros plain">=172.16.1.0</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=172.16.2.0/24</code> <code class="ros value">interface</code><code class="ros plain">=dummy_custB</code> <code class="ros value">network</code><code class="ros plain">=172.16.2.0</code></div><div class="line number12 index11 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros constants">/interface ipip</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">local-address</code><code class="ros plain">=111.255.255.1</code> <code class="ros value">name</code><code class="ros plain">=ipip-tunnel1</code> <code class="ros value">remote-address</code><code class="ros plain">=111.255.255.2</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">local-address</code><code class="ros plain">=111.255.255.2</code> <code class="ros value">name</code><code class="ros plain">=ipip-tunnel2</code> <code class="ros value">remote-address</code><code class="ros plain">=111.255.255.1</code></div><div class="line number16 index15 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.1.1/24</code> <code class="ros value">interface</code><code class="ros plain">=ipip-tunnel1</code> <code class="ros value">network</code><code class="ros plain">=192.168.1.0</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.1.2/24</code> <code class="ros value">interface</code><code class="ros plain">=ipip-tunnel2</code> <code class="ros value">network</code><code class="ros plain">=192.168.1.0</code></div><div class="line number20 index19 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros constants">/ip vrf</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interfaces</code><code class="ros plain">=ipip-tunnel1,dummy_custC</code> <code class="ros value">name</code><code class="ros plain">=custC</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interfaces</code><code class="ros plain">=ipip-tunnel2,dummy_custB</code> <code class="ros value">name</code><code class="ros plain">=custB</code></div><div class="line number24 index23 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number25 index24 alt2" data-bidi-marker="true"><code class="ros constants">/routing ospf instance</code></div><div class="line number26 index25 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">name</code><code class="ros plain">=i2_custB</code> <code class="ros value">redistribute</code><code class="ros plain">=connected,static,copy</code> <code class="ros value">router-id</code><code class="ros plain">=192.168.1.1</code> <code class="ros value">routing-table</code><code class="ros plain">=custB</code> <code class="ros value">vrf</code><code class="ros plain">=custB</code></div><div class="line number27 index26 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">name</code><code class="ros plain">=i2_custC</code> <code class="ros value">redistribute</code><code class="ros plain">=connected</code> <code class="ros value">router-id</code><code class="ros plain">=192.168.1.2</code> <code class="ros value">routing-table</code><code class="ros plain">=custC</code> <code class="ros value">vrf</code><code class="ros plain">=custC</code></div><div class="line number28 index27 alt1" data-bidi-marker="true"><code class="ros constants">/routing ospf area</code></div><div class="line number29 index28 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">instance</code><code class="ros plain">=i2_custB</code> <code class="ros value">name</code><code class="ros plain">=custB_bb</code></div><div class="line number30 index29 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">instance</code><code class="ros plain">=i2_custC</code> <code class="ros value">name</code><code class="ros plain">=custC_bb</code></div><div class="line number31 index30 alt2" data-bidi-marker="true"><code class="ros constants">/routing ospf interface-template</code></div><div class="line number32 index31 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">area</code><code class="ros plain">=custB_bb</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">networks</code><code class="ros plain">=192.168.1.0/24</code></div><div class="line number33 index32 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">area</code><code class="ros plain">=custC_bb</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">networks</code><code class="ros plain">=192.168.1.0/24</code></div></div></td></tr></tbody></table>

Result:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@rack1_b36_CCR1009] </code><code class="ros constants">/routing/ospf/neighbor&gt; </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: V - virtual; D - dynamic</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp; D </code><code class="ros value">instance</code><code class="ros plain">=i2_custB</code> <code class="ros value">area</code><code class="ros plain">=custB_bb</code> <code class="ros value">address</code><code class="ros plain">=192.168.1.1</code> <code class="ros value">priority</code><code class="ros plain">=128</code> <code class="ros value">router-id</code><code class="ros plain">=192.168.1.2</code> <code class="ros value">dr</code><code class="ros plain">=192.168.1.1</code> <code class="ros value">bdr</code><code class="ros plain">=192.168.1.2</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">state</code><code class="ros plain">=</code><code class="ros string">"Full"</code> <code class="ros value">state-changes</code><code class="ros plain">=6</code> <code class="ros value">adjacency</code><code class="ros plain">=41m28s</code> <code class="ros value">timeout</code><code class="ros plain">=33s</code></div><div class="line number5 index4 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1&nbsp; D </code><code class="ros value">instance</code><code class="ros plain">=i2_custC</code> <code class="ros value">area</code><code class="ros plain">=custC_bb</code> <code class="ros value">address</code><code class="ros plain">=192.168.1.2</code> <code class="ros value">priority</code><code class="ros plain">=128</code> <code class="ros value">router-id</code><code class="ros plain">=192.168.1.1</code> <code class="ros value">dr</code><code class="ros plain">=192.168.1.1</code> <code class="ros value">bdr</code><code class="ros plain">=192.168.1.2</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">state</code><code class="ros plain">=</code><code class="ros string">"Full"</code> <code class="ros value">state-changes</code><code class="ros plain">=6</code> <code class="ros value">adjacency</code><code class="ros plain">=41m28s</code> <code class="ros value">timeout</code><code class="ros plain">=33s</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">[admin@rack1_b36_CCR1009] </code><code class="ros constants">/ip/route&gt; </code><code class="ros functions">print </code><code class="ros plain">where </code><code class="ros value">routing-table</code><code class="ros plain">=custB</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: D - DYNAMIC; A - ACTIVE; c, s, o, y - COPY</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: DST-ADDRESS, GATEWAY, DISTANCE</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">DST-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GATEWAY&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DISTANCE</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">DAo </code><code class="ros color1">172.16.1.0/24</code>&nbsp;&nbsp;&nbsp;&nbsp; <code class="ros plain">192.168.1.1%ipip-tunnel2@custB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 110</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">DAc </code><code class="ros color1">172.16.2.0/24</code>&nbsp;&nbsp;&nbsp;&nbsp; <code class="ros plain">dummy_custB@custB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">DAc </code><code class="ros color1">192.168.1.0/24</code>&nbsp;&nbsp;&nbsp; <code class="ros plain">ipip-tunnel2@custB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number17 index16 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number18 index17 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros plain">[admin@rack1_b36_CCR1009] &gt; </code><code class="ros constants">/ip route/</code><code class="ros functions">print </code><code class="ros plain">where </code><code class="ros value">routing-table</code><code class="ros plain">=custC</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: D - DYNAMIC; A - ACTIVE; c, o, y - COPY</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: DST-ADDRESS, GATEWAY, DISTANCE</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">DST-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GATEWAY&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DISTANCE</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">DAc </code><code class="ros color1">172.16.1.0/24</code>&nbsp;&nbsp;&nbsp;&nbsp; <code class="ros plain">dummy_custC@custC&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number24 index23 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">DAo </code><code class="ros color1">172.16.2.0/24</code>&nbsp;&nbsp;&nbsp;&nbsp; <code class="ros plain">192.168.1.2%ipip-tunnel1@custC&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 110</code></div><div class="line number25 index24 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">DAc </code><code class="ros color1">192.168.1.0/24</code>&nbsp;&nbsp;&nbsp; <code class="ros plain">ipip-tunnel1@custC&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div></div></td></tr></tbody></table>

  

# References

[RFC 4364: BGP/MPLS IP Virtual Private Networks (VPNs)](http://www.ietf.org/rfc/rfc4364.txt)

MPLS Fundamentals, chapter 7, _Luc De Ghein_, Cisco Press 2006