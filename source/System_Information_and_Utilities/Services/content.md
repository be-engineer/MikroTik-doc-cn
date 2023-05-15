# Summary

___

This page lists protocols and ports used by various MikroTik RouterOS services. It helps you to determine why your MikroTik router listens to certain ports, and what you need to block/allow in case you want to prevent or grant access to certain services. Please see the relevant sections of the Manual for more explanations.

The default services are:

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

|             |
| ----------- | ------------------------------------------------------------------------------------ |
| **telnet**  | Telnet service                                                                       |
| **ftp**     | FTP service                                                                          |
| **www**     | Webfig HTTP service                                                                  |
| **ssh**     | SSH service                                                                          |
| **www-ssl** | Webfig HTTPS service                                                                 |
| **api**     | API service                                                                          |
| **winbox**  | Responsible for Winbox tool access, as well as Tik-App smartphone app and Dude probe |
| **api-ssl** | API over SSL service                                                                 |

# Properties

___

Note that it is not possible to add new services, only existing service modifications are allowed.

**Sub-menu:** `/ip service`

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

|                                             |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_IP address/netmask            | IPv6/0..128_; Default: )                                                                                                                | List of IP/IPv6 prefixes from which the service is accessible |
| **certificate** (_name_; Default: **none**) | The name of the certificate used by a particular service. Applicable only for services that depend on certificates (_www-ssl, api-ssl_) |
| **name** (_name_; Default: **none**)        | Service name                                                                                                                            |
| **port** (_integer: 1..65535_; Default: )   | The port particular service listens on                                                                                                  |
| **_tls-version_** (_any_                    | _only-1.2_; Default: **any**)                                                                                                           | Specifies which TLS versions to allow by a particular service |
| **vrf** (_name_; Default: **main**)         | Specify which VRF instance to use by a particular service                                                                               |

## Example

For example, allow API only from a specific IP/IPv6 address range

[?](https://help.mikrotik.com/docs/display/ROS/Services#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@dzeltenais_burkaans] </code><code class="ros constants">/ip service&gt; </code><code class="ros functions">set </code><code class="ros plain">api </code><code class="ros value">address</code><code class="ros plain">=10.5.101.0/24,2001:db8:fade::/64</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@dzeltenais_burkaans] </code><code class="ros constants">/ip service&gt; </code><code class="ros functions">print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - invalid</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments">#&nbsp;&nbsp; NAME&nbsp;&nbsp;&nbsp;&nbsp; PORT&nbsp; ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; CERTIFICATE&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;&nbsp; telnet&nbsp;&nbsp; 23&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1&nbsp;&nbsp; ftp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 21&nbsp;&nbsp;</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">2&nbsp;&nbsp; www&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 80&nbsp;&nbsp;</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">3&nbsp;&nbsp; ssh&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 22&nbsp;&nbsp;</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">4 X www-ssl&nbsp; 443&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; none&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">5&nbsp;&nbsp; api&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 8728&nbsp; </code><code class="ros color1">10.5.101.0/24</code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">2001</code><code class="ros constants">:db8:fade::/64&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">6&nbsp;&nbsp; winbox&nbsp;&nbsp; 8291</code></div></div></td></tr></tbody></table>

# Service Ports

___

Hosts behind a NAT-enabled router do not have true end-to-end connectivity. Therefore some Internet protocols might not work in scenarios with NAT.

To overcome these limitations RouterOS includes a number of [NAT](https://help.mikrotik.com/docs/display/ROS/NAT) helpers, that enable NAT traversal for various protocols.

If connection tracking is not enabled then firewall service ports will be shown as inactive

**Sub-menu:** `/ip firewall service-port`

| 
Helper

 | 

Description

|     |
| --- |  |
|     |

Helper

 | 

Description

|             |
| ----------- | ------------------------------- |
| **FTP**     | FTP service helper              |
| **H323**    | H323 service helper             |
| **IRC**     | IRC service helper              |
| **PPTP**    | PPTP tunneling helper           |
| **UDPLITE** | UDP-Lite service helper         |
| **DCCP**    | DCCP service helper             |
| **SCTP**    | SCTP service helper             |
| **SIP**     | SIP helper. Additional options: |

-   **sip-direct-media** allows redirecting the RTP media stream to go directly from the caller to the callee. The default value is _yes_.
-   **sip-timeout** allows adjusting TTL of SIP UDP connections. Default: 1 hour. In some setups, you have to reduce that.

 |
| **TFTP** | TFTP service helper |
| **RSTP** | RTSP service helper |

**udplite**, **dccp**, and **sctp** are built-in services of the connection tracking. Since these are not separately loaded modules, they cannot be disabled separately, they got disabled together with the connection tracking.

  

# Protocols and ports

___

The table below shows the list of protocols and ports used by RouterOS.

| 
Proto/Port

 | 

Description

|     |
| --- |  |
|     |

Proto/Port

 | 

Description

|                       |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **20/tcp**            | FTP data connection                                                                                                     |
| **21/tcp**            | FTP control connection                                                                                                  |
| **22/tcp**            | Secure Shell (SSH) remote login protocol                                                                                |
| **23/tcp**            | Telnet protocol                                                                                                         |
| **53/tcp              |
| 53/udp**              | DNS                                                                                                                     |
| **67/udp**            | Bootstrap protocol or [DHCP Server](https://help.mikrotik.com/docs/display/ROS/DHCP#DHCP-DHCPServer)                    |
| **68/udp**            | Bootstrap protocol or [DHCP Client](https://help.mikrotik.com/docs/display/ROS/DHCP#DHCP-DHCPClient)                    |
| **80/tcp**            | World Wide Web HTTP                                                                                                     |
| **123/udp**           | Network Time Protocol ([NTP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=40992869))                     |
| **161/udp**           | Simple Network Management Protocol ([SNMP](https://help.mikrotik.com/docs/display/ROS/SNMP))                            |
| **179/tcp**           | Border Gateway Protocol ([BGP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328220))                     |
| **443/tcp**           | Secure Socket Layer (SSL) encrypted HTTP                                                                                |
| **500/udp**           | Internet Key Exchange (IKE) protocol                                                                                    |
| **520/udp             |
| 521/udp**             | [RIP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328211) routing protocol                              |
| **546/udp**           | [DHCPv6 Client](https://help.mikrotik.com/docs/display/ROS/DHCP-client) message                                         |
| **547/udp**           | [DHCPv6 Server](https://help.mikrotik.com/docs/display/ROS/DHCP+Server) message                                         |
| **646/tcp**           | [LDP](https://wiki.mikrotik.com/wiki/Manual:MPLS/LDP "Manual:MPLS/LDP") transport session                               |
| **646/udp**           | [LDP](https://wiki.mikrotik.com/wiki/Manual:MPLS/LDP "Manual:MPLS/LDP") hello protocol                                  |
| **1080/tcp**          | [SOCKS](https://help.mikrotik.com/docs/display/ROS/SOCKS) proxy protocol                                                |
| **1698/udp 1699/udp** | RSVP TE Tunnels                                                                                                         |
| **1701/udp**          | Layer 2 Tunnel Protocol ([L2TP](https://help.mikrotik.com/docs/display/ROS/L2TP))                                       |
| **1723/tcp**          | Point-To-Point Tunneling Protocol ([PPTP](https://help.mikrotik.com/docs/display/ROS/PPTP))                             |
| **1900/udp            |
| 2828/tcp**            | Universal Plug and Play ([uPnP](https://help.mikrotik.com/docs/display/ROS/UPnP))                                       |
| **1966/udp**          | MME originator message traffic                                                                                          |
| **1966/tcp**          | MME gateway protocol                                                                                                    |
| **2000/tcp**          | Bandwidth test server                                                                                                   |
| **5246,5247/udp**     | [CAPsMAN](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=1409149)                                          |
| **5678/udp**          | Mikrotik Neighbor Discovery Protocol                                                                                    |
| **6343/tcp**          | Default OpenFlow port                                                                                                   |
| **8080/tcp**          | HTTP Web Proxy                                                                                                          |
| **8291/tcp**          | [Winbox](https://help.mikrotik.com/docs/display/ROS/Winbox)                                                             |
| **8728/tcp**          | [API](https://help.mikrotik.com/docs/display/ROS/API)                                                                   |
| **8729/tcp**          | API-SSL                                                                                                                 |
| **20561/udp**         | MAC winbox                                                                                                              |
| **/1**                | ICMP                                                                                                                    |
| **/2**                | [Multicast                                                                                                              | IGMP](https://wiki.mikrotik.com/wiki/Manual:Routing "Manual:Routing") |
| **/4**                | [IPIP](https://help.mikrotik.com/docs/display/ROS/IPIP) encapsulation                                                   |
| **/41**               | IPv6 (encapsulation)                                                                                                    |
| **/46**               | RSVP TE tunnels                                                                                                         |
| **/47**               | General Routing Encapsulation (GRE) - used for PPTP and [EoIP](https://help.mikrotik.com/docs/display/ROS/EoIP) tunnels |
| **/50**               | Encapsulating Security Payload for IPv4 (ESP)                                                                           |
| **/51**               | Authentication Header for IPv4 (AH)                                                                                     |
| **/89**               | [OSPF](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328218) routing protocol                             |
| **/103**              | [Multicast                                                                                                              | PIM](https://wiki.mikrotik.com/wiki/Manual:Routing "Manual:Routing")  |
| **/112**              | [VRRP](https://help.mikrotik.com/docs/display/ROS/VRRP)                                                                 |