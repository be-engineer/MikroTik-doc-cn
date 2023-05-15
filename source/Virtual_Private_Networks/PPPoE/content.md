# Overview

  
Point to Point over Ethernet (PPPoE) is simply a method of encapsulating PPP packets into Ethernet frames. PPPoE is an extension of the standard Point to Point Protocol (PPP) and it the successor of PPPoA. PPPoE standard is defined in [RFC 2516](https://tools.ietf.org/html/rfc2516). The PPPoE client and server work over any Layer2 Ethernet level interface on the router, for example, Wireless, Ethernet, EoIP, etc. Generally speaking, PPPoE is used to hand out IP addresses to clients based on authentication by username (and also if required, by workstation) as opposed to workstation only authentication where static IP addresses or DHCP are used. It is advised not to use static IP addresses or DHCP on the same interfaces as PPPoE for obvious security reasons.

# Introduction

PPPoE provides the ability to connect a network of hosts over a simple bridging access device to a remote Access Concentrator.  

Supported connections:

-   MikroTik RouterOS PPPoE client to any PPPoE server;
-   MikroTik RouterOS server (access concentrator) to multiple PPPoE clients (clients are available for almost all operating systems and most routers);

# PPPoE Operation

PPPoE has two distinct stages(phases):

1.  Discovery phase;
2.  Session phase;

## Discovery phase

There are four steps to the Discovery stage. When it completes, both peers know the PPPoE _SESSION\_ID_ and the peer's Ethernet address, which together define the PPPoE session uniquely:

1.   **PPPoE Active Discovery Initialization (PADI) -** The PPPoE client sends out a _PADI_ packet to the broadcast address. This packet can also populate the "service-name" field if a service name has been entered in the dial-up networking properties of the PPPoE client. If a service name has not been entered, this field is not populated
2.  **PPPoE Active Discovery Offer (PADO) -** The PPPoE server, or Access Concentrator, should respond to the _PADI_ with a _PADO_ if the Access Concentrator is able to service the "service-name" field that had been listed in the _PADI_ packet. If no "service-name" field had been listed, the Access Concentrator will respond with a _PADO_ packet that has the "service-name" field populated with the service names that the Access Concentrator can service. The _PADO_ packet is sent to the unicast address of the PPPoE client
3.  **PPPoE Active Discovery Request (PADR) -** When a _PADO_ packet is received, the PPPoE client responds with a _PADR_ packet. This packet is sent to the unicast address of the Access Concentrator. The client may receive multiple _PADO_ packets, but the client responds to the first valid _PADO_ that the client received. If the initial _PADI_ packet had a blank "service-name" field filed, the client populates the "service-name" field of the _PADR_ packet with the first service name that had been returned in the _PADO_ packet.
4.  **PPPoE Active Discovery Session Confirmation (PADS) -** When the _PADR_ is received, the Access Concentrator generates a unique session identification (ID) for the Point-to-Point Protocol (PPP) session and returns this ID to the PPPoE client in the _PADS_ packet. This packet is sent to the unicast address of the client.
    

PPPoE session termination:

-   **PPPoE Active Discovery Terminate (PADT) -** Can be sent anytime after a session is established to indicate that a PPPoE session terminated. It can be sent by either server or client.

## Session phase

When the discovery stage is completed, both peers know _PPPoE Session ID_ and other peer's _Ethernet (MAC) address_ which together defines the PPPoE session. PPP frames are encapsulated in PPPoE session frames, which have Ethernet frame type **0x8864**.  
When a server sends confirmation and a client receives it, PPP Session is started that consists of the following stages:

1.  **LCP negotiation** stage
2.  **Authentication (CHAP/PAP)** stage
3.  **IPCP negotiation** stage - where the client is assigned an IP address.

If any process fails, the LCP negotiation establishment phase is started again.

  
PPPoE server sends _Echo-Request_ packets to the client to determine the state of the session, otherwise, the server will not be able to determine that session is terminated in cases when a client terminates session without sending _Terminate-Request_ packet.

# MTU

Typically, the largest Ethernet frame that can be transmitted without fragmentation is 1500 bytes. PPPoE adds another 6 bytes of overhead and the PPP field adds two more bytes, leaving 1492 bytes for IP datagram. Therefore max PPPoE MRU and MTU values must not be larger than 1492.

TCP stacks try to avoid fragmentation, so they use an MSS (Maximum Segment Size). By default, MSS is chosen as MTU of the outgoing interface minus the usual size of the TCP and IP headers (40 bytes), which results in 1460 bytes for an Ethernet interface. Unfortunately, there may be intermediate links with lower MTU which will cause fragmentation. In such a case TCP stack performs path MTU discovery. Routers that cannot forward the datagram without fragmentation are supposed to drop the packet and send _ICMP-Fragmentation-Required_ to originating host. When a host receives such an ICMP packet, it tries to lower the MTU. This should work in the ideal world, however in the real world many routers do not generate fragmentation-required datagrams, also many firewalls drop all ICMP datagrams.

The workaround for this problem is to [adjust MSS](https://help.mikrotik.com/docs/display/ROS/Mangle#Mangle-ChangeMSS) if it is too big. 

# PPPoE Client

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
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **ac-name** (_string_; Default: **""**)                       | Access Concentrator name, this may be left blank and the client will connect to any access concentrator on the broadcast domain |
| **add-default-route** (_yes                                   | no_; Default: **no**)                                                                                                           | Enable/Disable whether to add default route automatically                                                                                                                                                  |
| **allow** (_mschap2                                           | mschap1                                                                                                                         | chap                                                                                                                                                                                                       | pap_; Default: **mschap2,mschap1,chap,pap**) | allowed authentication methods, by default all methods are allowed |
| **default-route-distance** (_byte \[0..255\]_; Default:**1**) | sets distance value applied to auto created default route, if add-default-route is also selected                                |
| **dial-on-demand** (_yes                                      | no_; Default: **no**)                                                                                                           | connects to AC only when outbound traffic is generated. If selected, then route with gateway address from 10.112.112.0/24 network will be added while connection is not established.                       |
| **interface** (_string_; Default: )                           | interface name on which client will run                                                                                         |
| **keepalive-timeout** (_integer_; Default:**60**)             | Sets keepalive timeout in seconds.                                                                                              |
| **max-mru** (_integer_; Default: **1460**)                    | Maximum Receive Unit                                                                                                            |
| **max-mtu** (_integer_; Default: **1460**)                    | Maximum Transmission Unit                                                                                                       |
| **mrru** (_integer: 512..65535                                | disabled_; Default: **disabled**)                                                                                               | maximum packet size that can be received on the link. If a packet is bigger than tunnel MTU, it will be split into multiple packets, allowing full size IP or Ethernet packets to be sent over the tunnel. |
| **name** (_string_; Default: **pppoe-out\[i\]**)              | name of the PPPoE interface, generated by RouterOS if not specified                                                             |
| **password** (_string_; Default: )                            | password used to authenticate                                                                                                   |
| **profile** (_string_; Default: **default**)                  | Specifies which PPP profile configuration will be used when establishing the tunnel.                                            |
| **service-name** (_string_; Default: **""**)                  | specifies the service name set on the access concentrator, can be left blank to connect to any PPPoE server                     |
| **use-peer-dns** (_yes                                        | no_; Default: **no**)                                                                                                           | enable/disable getting DNS settings from the peer                                                                                                                                                          |
| **user** (_string_; Default: **""**)                          |

username used for authentication

 |

## Status

Command `/interface pppoe-client monitor` will display current PPPoE status.

Available read only properties:

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
| --------------------------------- | ----------------------------------------------------------------------------------------- |
| **ac-mac** (_MAC address_)        | MAC address of the access concentrator (AC) the client is connected to                    |
| **ac-name** (_string_)            | name of the Access Concentrator                                                           |
| **active-links** (_integer_)      | Number of bonded MLPPP connections, ('1' if not using MLPPP)                              |
| **encoding** (_string_)           | encryption and encoding (if asymmetric, separated with '/') being used in this connection |
| **local-address** (_IP Address_)  | IP Address allocated to client                                                            |
| **remote-address** (_IP Address_) | Remote IP Address allocated to server (ie gateway address)                                |
| **mru** (_integer_)               | effective MRU of the link                                                                 |
| **mtu** (_integer_)               | effective MTU of the link                                                                 |
| **service-name** (_string_)       | used service name                                                                         |
| **status** (_string_)             | current link status. Available values are:                                                |

-   dialing,
-   verifying password...,
-   connected,
-   disconnected.

 |
| **uptime** (_time_) | connection time displayed in days, hours, minutes and seconds |

## Scanner

PPPoE Scanner allows scanning all active PPPoE servers in the layer2 broadcast domain. Command to run scanner is as follows:

[?](https://help.mikrotik.com/docs/display/ROS/PPPoE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface pppoe-client </code><code class="ros functions">scan </code><code class="ros plain">[interface]</code></div></div></td></tr></tbody></table>

Available read only properties: 

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

|                         |
| ----------------------- | --------------------------------- |
| **service** (_string_)  | Service name configured on server |
| **mac-address** (_MAC_) | Mac address of detected server    |
| **ac-name** (_string_)  | name of the Access Concentrator   |

For Windows, some connection instructions may use the form where the "phone number", such as "MikroTik\_AC\\mt1", is specified to indicate that "MikroTik\_AC" is the access concentrator name and "mt1" is the service name.

Specifying MRRU means enabling MP (Multilink PPP) over a single link. This protocol is used to split big packets into smaller ones. Under Windows, it can be enabled in the Networking tab, Settings button, "Negotiate multi-link for single link connections". MRRU is hardcoded to 1614 on Windows. This setting is useful to overcome PathMTU discovery failures. The MP setting should be enabled on both peers.

# PPPoE Server

There are two types of interface (tunnel) items in PPPoE server configuration - static users and dynamic connections. An interface is created for each tunnel established to the given server. Static interfaces are added administratively if there is a need to reference the particular interface name (in firewall rules or elsewhere) created for the particular user. Dynamic interfaces are added to this list automatically whenever a user is connected and its username does not match any existing static entry (or in case the entry is active already, as there can not be two separate tunnel interfaces referenced by the same name - set _one-session-per-host_ value if this is a problem). Dynamic interfaces appear when a user connects and disappear once the user disconnects, so it is impossible to reference the tunnel created for that use in router configuration (for example, in firewall), so if you need a persistent rule for that user, create a static entry for him/her. Otherwise, it is safe to use a dynamic configuration. 

In both cases PPP users must be configured properly - static entries do not replace PPP configuration.

## Access concentrator 

[?](https://help.mikrotik.com/docs/display/ROS/PPPoE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface pppoe-server server</code></div></div></td></tr></tbody></table>

### Properties

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

|                                                        |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **authentication** ( _mschap2                          | mschap1                                                                                                                                                                                                                                                                               | chap                                                                                                                                                                                                       | pap_; Default: **"mschap2, mschap1, chap, pap"**) | Authentication algorithm |
| **default-profile** (_string_; Default: **"default"**) |
|                                                        |
| **interface** (_string_; Default: **""**)              | Interface that the clients are connected to                                                                                                                                                                                                                                           |
| **keepalive-timeout** (_time_; Default: **"10"**)      | Defines the time period (in seconds) after which the router is starting to send keepalive packets every second. If there is no traffic and no keepalive responses arrive for that period of time (i.e. 2 \* keepalive-timeout), the non responding client is proclaimed disconnected. |
| **max-mru** (_integer_; Default: **"1480"**)           | Maximum Receive Unit. The optimal value is the MTU of the interface the tunnel is working over reduced by 20 (so, for 1500-byte Ethernet link, set the MTU to 1480 to avoid fragmentation of packets)                                                                                 |
| **max-mtu** (_integer_; Default: **"1480"**)           | Maximum Transmission Unit. The optimal value is the MTU of the interface the tunnel is working over reduced by 20 (so, for 1500-byte Ethernet link, set the MTU to 1480 to avoid fragmentation of packets)                                                                            |
| **max-sessions** (_integer_; Default: **"0"**)         | Maximum number of clients that the AC can serve. '0' = no limitations.                                                                                                                                                                                                                |
| **mrru** (_integer: 512..65535                         | disabled_; Default: **"disabled"**)                                                                                                                                                                                                                                                   | Maximum packet size that can be received on the link. If a packet is bigger than tunnel MTU, it will be split into multiple packets, allowing full size IP or Ethernet packets to be sent over the tunnel. |
| **one-session-per-host** (_yes                         | no_; Default: **"no"**)                                                                                                                                                                                                                                                               | Allow only one session per host (determined by MAC address). If a host tries to establish a new session, the old one will be closed.                                                                       |
| **service-name** (_string_; Default: **""**)           | The PPPoE service name. Server will accept clients which sends PADI message with service-names that matches this setting or if service-name field in PADI message is not set.                                                                                                         |

The PPPoE server (access concentrator) supports multiple servers for each interface - with differing service names. The access concentrator name and PPPoE service name are used by clients to identify the access concentrator to register with. The access concentrator name is the same as the identity of the router displayed before the command prompt. The identity may be set within the _/system identity_ submenu.

Do not assign an IP address to the interface you will be receiving the PPPoE requests on.

  
Specifying MRRU means enabling MP (Multilink PPP) over a single link. This protocol is used to split big packets into smaller ones.  Their MRRU is hardcoded to 1614. This setting is useful to overcome PathMTU discovery failures. The MP setting should be enabled on both peers.

The default _keepalive-timeout_ value of 10s is OK in most cases. If you set it to 0, the router will not disconnect clients until they explicitly log out or the router is restarted. To resolve this problem, the one-session-per-host property can be used.

# Quick Example

![](https://help.mikrotik.com/docs/download/attachments/2031625/Untitled%20Diagram.jpg?version=1&modificationDate=1571812332084&api=v2)

## PPPoE Client

To configure MikroTik RouterOS to be a PPPoE client, just add a PPPoE-client with the following parameters as in the example:

[?](https://help.mikrotik.com/docs/display/ROS/PPPoE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; interface pppoe-client </code><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">password</code><code class="ros plain">=StrongPass</code> <code class="ros value">service-name</code><code class="ros plain">=pppoeservice</code> <code class="ros value">name</code><code class="ros plain">=PPPoE-Out</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">user</code><code class="ros plain">=MT-User</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; interface pppoe-client print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - invalid, R - running</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp; R </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"PPPoE-Out"</code> <code class="ros value">max-mtu</code><code class="ros plain">=auto</code> <code class="ros value">max-mru</code><code class="ros plain">=auto</code> <code class="ros value">mrru</code><code class="ros plain">=disabled</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">user</code><code class="ros plain">=</code><code class="ros string">"MT-User"</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">password</code><code class="ros plain">=</code><code class="ros string">"StrongPass"</code> <code class="ros value">profile</code><code class="ros plain">=default</code> <code class="ros value">keepalive-timeout</code><code class="ros plain">=10</code> <code class="ros value">service-name</code><code class="ros plain">=</code><code class="ros string">"pppoeservice"</code> <code class="ros value">ac-name</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">add-default-route</code><code class="ros plain">=no</code> <code class="ros value">dial-on-demand</code><code class="ros plain">=no</code> <code class="ros value">use-peer-dns</code><code class="ros plain">=no</code> <code class="ros value">allow</code><code class="ros plain">=pap,chap,mschap1,mschap2</code></div></div></td></tr></tbody></table>

## PPPoE Server

To configure MikroTik RouterOS to be an Access Concentrator (PPPoE Server):

-   add an IP address pool for the clients from 10.0.0.2-10.0.0.5;
-   add PPP profile;
-   add PPP secret (username/password);
-   add the PPPoE server itself;

[?](https://help.mikrotik.com/docs/display/ROS/PPPoE#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/ip pool</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=pppoe-pool</code> <code class="ros value">ranges</code><code class="ros plain">=10.0.0.2-10.0.0.5</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/ppp pro</code><code class="ros plain">file</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">local-address</code><code class="ros plain">=10.0.0.1</code> <code class="ros value">name</code><code class="ros plain">=for-pppoe</code> <code class="ros value">remote-address</code><code class="ros plain">=pppoe-pool</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/ppp secret</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=MT-User</code> <code class="ros value">password</code><code class="ros plain">=StrongPass</code> <code class="ros value">profile</code><code class="ros plain">=for-pppoe</code> <code class="ros value">service</code><code class="ros plain">=pppoe</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface pppoe-server server</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">default-profile</code><code class="ros plain">=for-pppoe</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">interface</code><code class="ros plain">=ether3</code> <code class="ros value">service-name</code><code class="ros plain">=pppoeservice</code></div></div></td></tr></tbody></table>