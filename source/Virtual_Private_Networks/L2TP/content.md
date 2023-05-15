# Overview

Layer Two Tunneling Protocol "L2TP" extends the PPP model by allowing the L2 and PPP endpoints to reside on different devices interconnected by a packet-switched network.  L2TP includes PPP authentication and accounting for each L2TP connection. Full authentication and accounting of each connection may be done through a RADIUS client or locally. L2TP traffic uses UDP protocol for both control and data packets. UDP port 1701 is used only for link establishment, further traffic is using any available UDP port (which may or may not be 1701). This means that L2TP can be used with most firewalls and routers (even with NAT) by enabling UDP traffic to be routed through the firewall or router.  L2TP standard is defined in [RFC 2661](https://tools.ietf.org/html/rfc2661).

# Introduction

It may be useful to use L2TP just as any other tunneling protocol with or without encryption. The L2TP standard says that the most secure way to encrypt data is using L2TP over IPsec (Note that it is the default mode for Microsoft L2TP client) as all L2TP control and data packets for a particular tunnel appear as homogeneous UDP/IP data packets to the IPsec system. 

Multilink PPP (MP) is supported in order to provide MRRU (the ability to transmit full-sized 1500 and larger packets) and bridging over PPP links (using Bridge Control Protocol (BCP) that allows sending raw Ethernet frames over PPP links). This way it is possible to setup bridging without EoIP. The bridge should either have an administratively set MAC address or an Ethernet-like interface in it, as PPP links do not have MAC addresses.

L2TP does not provide encryption mechanisms for tunneled traffic. IPsec can be used for additional security layers.

# L2TP Client

## Properties

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

|                                  |
| -------------------------------- | --------------------- |
| **add-default-route** (_yes      | no_; Default: **no**) | Whether to add L2TP remote address as a default route. |
| **allow** (_mschap2              | mschap1               | chap                                                   | pap_; Default: **mschap2, mschap1, chap, pap**) | Allowed authentication methods. |
| **connect-to** (_IP_; Default: ) |

Remote address of L2TP server (if the address is in VRF table,  VRF should be specified)

[?](https://help.mikrotik.com/docs/display/ROS/L2TP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface l2tp-client</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">add&nbsp;</code><code class="ros value">connect-to</code><code class="ros plain">=192.168.88.1@vrf1&nbsp;</code><code class="ros plain">;</code><code class="ros value">name</code><code class="ros plain">=l2tp-out1&nbsp;</code><code class="ros plain">;</code><code class="ros value">user</code><code class="ros plain">=l2tp-client)</code></div></div></td></tr></tbody></table>

  




 |
| **comment** (_string_; Default: ) | Short description of the tunnel. |
| **default-route-distance** (_byte_; Default: ) | Since v6.2, sets distance value applied to auto created default route, if add-default-route is also selected |
| **dial-on-demand** (_yes | no_; Default: **no**) | connects only when outbound traffic is generated. If selected, then route with gateway address from 10.112.112.0/24 network will be added while connection is not established. |
| **disabled** (_yes | no_; Default: **yes**) | Enables/disables tunnel. |
| **keepalive-timeout** (_integer \[1..4294967295\]_; Default: **60s**) | Since v6.0rc13, tunnel keepalive timeout in seconds. |
| **max-mru** (_integer_; Default: **1460**) | Maximum Receive Unit. Max packet size that L2TP interface will be able to receive without packet fragmentation. |
| **max-mtu** (_integer_; Default: **1460**) | Maximum Transmission Unit. Max packet size that L2TP interface will be able to send without packet fragmentation. |
| **mrru** (_disabled | integer_; Default: **disabled**) | Maximum packet size that can be received on the link. If a packet is bigger than tunnel MTU, it will be split into multiple packets, allowing full size IP or Ethernet packets to be sent over the tunnel. |
| **name** (_string_; Default: ) | Descriptive name of the interface. |
| **password** (_string_; Default: **""**) | Password used for authentication. |
| **profile** (_name_; Default: **default-encryption**) | Specifies which PPP profile configuration will be used when establishing the tunnel. |
| **user** (_string_; Default: ) | User name used for authentication. |
| **use-ipsec** (_yes | no_; Default: **no**) | When this option is enabled, dynamic IPSec peer configuration and policy is added to encapsulate L2TP connection into IPSec tunnel. |
| **ipsec-secret** (_string_; Default: ) | Preshared key used when use-ipsec is enabled. |

# L2TP Server

An interface is created for each tunnel established to the given server. There are two types of interfaces in the L2TP server's configuration

-   Static interfaces are added administratively if there is a need to reference the particular interface name (in firewall rules or elsewhere) created for the particular user;
-   Dynamic interfaces are added to this list automatically whenever a user is connected and its username does not match any existing static entry (or in case the entry is active already, as there can not be two separate tunnel interfaces referenced by the same name);

Dynamic interfaces appear when a user connects and disappear once the user disconnects, so it is impossible to reference the tunnel created for that use in router configuration (for example, in firewall), so if you need persistent rules for that user, create a static entry for him/her. Otherwise, it is safe to use a dynamic configuration.

in both cases PPP users must be configured properly - static entries do not replace PPP configuration.

## Properties

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

|                                                               |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **authentication** (_pap                                      | chap                                                                                                                                                                                                                                                                                                                              | mschap1                                                                                                                                                                                                    | mschap2_; Default: **mschap1,mschap2**)                                                                                                                                                                                                           | Authentication methods that server will accept. |
| **default-profile** (_name_; Default: **default-encryption**) | default profile to use                                                                                                                                                                                                                                                                                                            |
| **enabled** (_yes                                             | no_; Default: **no**)                                                                                                                                                                                                                                                                                                             | Defines whether L2TP server is enabled or not.                                                                                                                                                             |
| **max-mru** (_integer_; Default: **1450**)                    | Maximum Receive Unit. Max packet size that L2TP interface will be able to receive without packet fragmentation.                                                                                                                                                                                                                   |
| **keepalive-timeout** (_integer_; Default: **30**)            | If server during keepalive-timeout period does not receive any packets, it will send keepalive packets every second, five times. If the server still does not receive any response from the client, then the client will be disconnected after 5 seconds. Logs will show 5x "LCP missed echo reply" messages and then disconnect. |
| **max-mtu** (_integer_; Default: **1450**)                    | Maximum Transmission Unit. Max packet size that L2TP interface will be able to send without packet fragmentation.                                                                                                                                                                                                                 |
| **use-ipsec** (_no                                            | yes                                                                                                                                                                                                                                                                                                                               | require_; Default: **no**)                                                                                                                                                                                 | When this option is enabled, dynamic IPSec peer configuration is added to suite most of the L2TP road-warrior setups. When require is selected server will accept only those L2TP connection attempts that were encapsulated in the IPSec tunnel. |
| **ipsec-secret** (_string_; Default: )                        | Preshared key used when use-ipsec is enabled                                                                                                                                                                                                                                                                                      |
| **mrru** (_disabled                                           | integer_; Default: **disabled**)                                                                                                                                                                                                                                                                                                  | Maximum packet size that can be received on the link. If a packet is bigger than tunnel MTU, it will be split into multiple packets, allowing full size IP or Ethernet packets to be sent over the tunnel. |

# Quick Example

![](https://help.mikrotik.com/docs/download/attachments/2031631/Simple-l2tp-setup.jpg?version=2&modificationDate=1571748876898&api=v2)

## L2TP Server

On the servers side we will enable L2TP-server and create a PPP profile for a particular user:

[?](https://help.mikrotik.com/docs/display/ROS/L2TP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface l2tp-server server </code><code class="ros functions">set </code><code class="ros value">enabled</code><code class="ros plain">=yes</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/ppp secret </code><code class="ros functions">add </code><code class="ros value">local-address</code><code class="ros plain">=10.0.0.2</code> <code class="ros value">name</code><code class="ros plain">=MT-User</code> <code class="ros value">password</code><code class="ros plain">=StrongPass</code> <code class="ros value">profile</code><code class="ros plain">=default-encryption</code> <code class="ros value">remote-address</code><code class="ros plain">=10.0.0.1</code> <code class="ros value">service</code><code class="ros plain">=l2tp</code></div></div></td></tr></tbody></table>

## L2TP Client

L2TP client setup in the RouterOS is very simple.  In the following example, we already have a preconfigured 3 unit setup. We will take a look more detailed on how to set up L2TP client with username "MT-User", password "StrongPass" and server 192.168.51.3:

[?](https://help.mikrotik.com/docs/display/ROS/L2TP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface l2tp-client \</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">connect-to</code><code class="ros plain">=192.168.51.3</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">name</code><code class="ros plain">=MT-User</code> <code class="ros value">password</code><code class="ros plain">=StrongPass</code> <code class="ros value">user</code><code class="ros plain">=MT-User</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface l2tp-client </code><code class="ros functions">print</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, R - running</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0 R </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"MT-User"</code> <code class="ros value">max-mtu</code><code class="ros plain">=1450</code> <code class="ros value">max-mru</code><code class="ros plain">=1450</code> <code class="ros value">mrru</code><code class="ros plain">=disabled</code> <code class="ros value">connect-to</code><code class="ros plain">=192.168.51.3</code> <code class="ros value">user</code><code class="ros plain">=</code><code class="ros string">"MT-User"</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros value">password</code><code class="ros plain">=</code><code class="ros string">"StrongPass"</code> <code class="ros value">profile</code><code class="ros plain">=default-encryption</code> <code class="ros value">keepalive-timeout</code><code class="ros plain">=60</code> <code class="ros value">use-ipsec</code><code class="ros plain">=no</code> <code class="ros value">ipsec-secret</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros value">allow-fast-path</code><code class="ros plain">=no</code> <code class="ros value">add-default-route</code><code class="ros plain">=no</code> <code class="ros value">dial-on-demand</code><code class="ros plain">=no</code> <code class="ros value">allow</code><code class="ros plain">=pap,chap,mschap1,mschap2</code></div></div></td></tr></tbody></table>