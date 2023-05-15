# Overview

PPTP has many known security issues and we are not recommending to use it. However, this protocol is integrated into common operating systems and it is easy to set it up. PPTP can be useful in networks where security concerns are not considered.

PPTP traffic uses TCP port 1723 and IP protocol GRE (Generic Routing Encapsulation, IP protocol ID 47), as assigned by the Internet Assigned Numbers Authority (IANA). PPTP can be used with most firewalls and routers by enabling traffic destined for TCP port 1723 and protocol 47 traffic to be routed through the firewall or router.  PPTP includes PPP authentication and accounting for each PPTP connection. Full authentication and accounting of each connection may be done through a RADIUS client or locally.

# PPTP Client

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

|                                                                |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **add-default-route** (_yes                                    | no_; Default: **no**)                                                                                             | Whether to add PPTP remote address as a default route.                                                                                                                                                     |
| **allow** (_mschap2                                            | mschap1                                                                                                           | chap                                                                                                                                                                                                       | pap_; Default: **mschap2, mschap1, chap, pap**) | Allowed authentication methods. |
| **connect-to** (_IP_; Default: )                               | Remote address of PPTP server                                                                                     |
| **default-route-distance** (_byte \[0..255\]_; Default: **1**) | sets distance value applied to auto created default route, if add-default-route is also selected                  |
| **dial-on-demand** (_yes                                       | no_; Default: **no**)                                                                                             | connects to PPTP server only when outbound traffic is generated. If selected, then route with gateway address from 10.112.112.0/24 network will be added while connection is not established.              |
| **disabled** (_yes                                             | no_; Default: **yes**)                                                                                            | Whether interface is disabled or not. By default it is disabled                                                                                                                                            |
| **keepalive-timeout** (_integer_; Default: **60**)             | Sets keepalive timeout in seconds.                                                                                |
| **max-mru** (_integer_; Default: **1460**)                     | Maximum Receive Unit. Max packet size that PPTP interface will be able to receive without packet fragmentation.   |
| **max-mtu** (_integer_; Default: **1460**)                     | Maximum Transmission Unit. Max packet size that PPTP interface will be able to send without packet fragmentation. |
| **mrru** (_disabled                                            | integer_; Default: **disabled**)                                                                                  | Maximum packet size that can be received on the link. If a packet is bigger than tunnel MTU, it will be split into multiple packets, allowing full size IP or Ethernet packets to be sent over the tunnel. |
| **name** (_string_; Default: )                                 | Descriptive name of the interface.                                                                                |
| **password** (_string_; Default: **""**)                       | Password used for authentication.                                                                                 |
| **profile** (_name_; Default: **default-encryption**)          |
|                                                                |
| **user** (_string_; Default: )                                 | User name used for authentication.                                                                                |

# PPTP Server

[?](https://help.mikrotik.com/docs/display/ROS/PPTP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface pptp-server</code></div></div></td></tr></tbody></table>

An interface is created for each tunnel established to the given server. There are two types of interfaces in the PPTP server's configuration:

-   Static interfaces are added administratively if there is a need to reference the particular interface name (in firewall rules or elsewhere) created for the particular user;
-   Dynamic interfaces are added to this list automatically whenever a user is connected and its username does not match any existing static entry (or in case the entry is active already, as there can not be two separate tunnel interfaces referenced by the same name);

Dynamic interfaces appear when a user connects and disappear once the user disconnects, so it is impossible to reference the tunnel created for that use in router configuration (for example, in firewall), so if you need persistent rules for that user, create a static entry for him/her. Otherwise, it is safe to use a dynamic configuration.

In both cases PPP users must be configured properly - static entries do not replace PPP configuration.

## _Properties_

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
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **authentication** (_pap                                      | chap                                                                                                                                                                                                                                                                                      | mschap1                                                                                                                                                                                                    | mschap2_; Default: **mschap1,mschap2**) | Authentication methods that server will accept. |
| **default-profile** (_name_; Default: **default-encryption**) |
|                                                               |
| **enabled** (_yes                                             | no_; Default: **no**)                                                                                                                                                                                                                                                                     | Defines whether PPTP server is enabled or not.                                                                                                                                                             |
| **keepalive-timeout** (_time_; Default: **30**)               | If server during keepalive period does not receive any packet, it will send keepalive packets every second five times. If the server does not receives response from the client, then disconnect after 5 seconds. Logs will show 5x "LCP missed echo reply" messages and then disconnect. |
| **max-mru** (_integer_; Default: **1460**)                    | Maximum Receive Unit. Max packet size that PPTP interface will be able to receive without packet fragmentation.                                                                                                                                                                           |
| **max-mtu** (_integer_; Default: **1460**)                    | Maximum Transmission Unit. Max packet size that PPTP interface will be able to send without packet fragmentation.                                                                                                                                                                         |
| **mrru** (_disabled                                           | integer_; Default: **disabled**)                                                                                                                                                                                                                                                          | Maximum packet size that can be received on the link. If a packet is bigger than tunnel MTU, it will be split into multiple packets, allowing full size IP or Ethernet packets to be sent over the tunnel. |

# Example

![](https://help.mikrotik.com/docs/download/attachments/2031638/pptp-setup.jpg?version=1&modificationDate=1571822551430&api=v2)

## PPTP Client

The following example demonstrates how to set up a PPTP client with username "MT-User", password "StrongPass" and server 192.168.62.2:

  

[?](https://help.mikrotik.com/docs/display/ROS/PPTP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; interface pptp-client </code><code class="ros functions">add </code><code class="ros value">connect-to</code><code class="ros plain">=192.168.62.2</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">name</code><code class="ros plain">=pptp-out1</code> <code class="ros value">password</code><code class="ros plain">=StrongPass</code> <code class="ros value">user</code><code class="ros plain">=MT-User</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; interface pptp-client </code><code class="ros functions">print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled; R - running</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp; R </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"pptp-out1"</code> <code class="ros value">max-mtu</code><code class="ros plain">=1450</code> <code class="ros value">max-mru</code><code class="ros plain">=1450</code> <code class="ros value">mrru</code><code class="ros plain">=disabled</code> <code class="ros value">connect-to</code><code class="ros plain">=192.168.62.2</code> <code class="ros value">user</code><code class="ros plain">=</code><code class="ros string">"MT-User"</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">password</code><code class="ros plain">=</code><code class="ros string">"StrongPass"</code> <code class="ros value">profile</code><code class="ros plain">=default-encryption</code> <code class="ros value">keepalive-timeout</code><code class="ros plain">=60</code> <code class="ros value">add-default-route</code><code class="ros plain">=no</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">dial-on-demand</code><code class="ros plain">=no</code> <code class="ros value">allow</code><code class="ros plain">=pap,chap,mschap1,mschap2</code></div></div></td></tr></tbody></table>

## PPTP Server

On the other side we simply enable the PPTP server and create a PPP secret for a particular user:

[?](https://help.mikrotik.com/docs/display/ROS/PPTP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt;&nbsp; interface pptp-server server </code><code class="ros functions">set </code><code class="ros value">enabled</code><code class="ros plain">=yes</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt;&nbsp; ppp secret </code><code class="ros functions">add </code><code class="ros value">local-address</code><code class="ros plain">=10.0.0.1</code> <code class="ros value">name</code><code class="ros plain">=MT-User</code> <code class="ros value">password</code><code class="ros plain">=StrongPass</code> <code class="ros value">profile</code><code class="ros plain">=default-encryption</code> <code class="ros value">remote-address</code><code class="ros plain">=10.0.0.5</code> <code class="ros value">service</code><code class="ros plain">=pptp</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt;&nbsp; interface pptp-server print</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: D - dynamic; R - running</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NAME, USER, MTU, CLIENT-ADDRESS, UPTIME, ENCODING</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros comments">#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; USER&nbsp;&nbsp;&nbsp;&nbsp; MTU&nbsp; CLIENT-ADDRESS&nbsp; UPTIM&nbsp; ENCODING&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">0&nbsp; DR&nbsp; &lt;pptp-MT-User&gt;&nbsp; MT-User&nbsp; 1450&nbsp; 192.168.51.3&nbsp;&nbsp; 44m8s&nbsp; MPPE128 stateless</code></div></div></td></tr></tbody></table>