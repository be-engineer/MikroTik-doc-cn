-   [RouterOS version 6](https://help.mikrotik.com/docs/display/ROS/NTP#NTP-RouterOSversion6)
    -   1.1[SNTP Client properties:](https://help.mikrotik.com/docs/display/ROS/NTP#NTP-SNTPClientproperties:)
    -   1.2[Client settings example:](https://help.mikrotik.com/docs/display/ROS/NTP#NTP-Clientsettingsexample:) 
    -   1.3[NTP Server settings:](https://help.mikrotik.com/docs/display/ROS/NTP#NTP-NTPServersettings:)
-   2[RouterOS version 7](https://help.mikrotik.com/docs/display/ROS/NTP#NTP-RouterOSversion7)
    -   2.1[NTP Client properties:](https://help.mikrotik.com/docs/display/ROS/NTP#NTP-NTPClientproperties:)
    -   2.2[NTP Server settings:](https://help.mikrotik.com/docs/display/ROS/NTP#NTP-NTPServersettings:.1)
-   3[Log messages](https://help.mikrotik.com/docs/display/ROS/NTP#NTP-Logmessages)

RouterOS v6 implements the SNTP protocol defined in RFC4330, manycast mode is not supported. SNTP client is included in the _system_ package. To use an NTP server, _ntp_ package must be [installed and enabled](https://help.mikrotik.com/docs/display/ROS/Packages).

RouterOS v7 main package includes NTP client and server functionality, which is based on RFC5905.

The client configuration is located in the **/system ntp client** console path, and the **_"System > SNTP Client"_** (RouterOS version 6), **_"System > NTP Client"_** (RouterOS version 7) WinBox window. This configuration is shared by the SNTP client implementation in the _system_ package and the NTP client implementation in the _ntp_ package. When _ntp_ package is installed and enabled, the SNTP client is disabled automatically.

# RouterOS version 6

## SNTP Client properties:

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

|                                                     |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **enabled** (_yes, no default: no_)                 | Enable SNTP client for time synchronization                                                                                                                                                                                 |
| **mode** (_broadcast, unicast, filed is read-only_) | Mode that the SNTP client will operate in. If no NTP servers are configured _broadcast_ mode will be used. If there is a dynamic or static NTP server IP address or FQDN used it will automatically switch to unicast mode. |
| **primary-ntp** (_IP address default: 0.0.0.0_)     |

IP address of the NTP server that has to be used for time synchronization. If both values are non-zero, then the SNTP client will alternate between the two server addresses, switching to the other when the request to the current server times out or when the "KoD" packet is received, indicating that the server is not willing to respond to requests from this client.

The following formats are accepted:

_\- ipv4_  
_\- ipv6_

 |
| **secondary-ntp** (_IP address default: 0.0.0.0_) | see **primary-ntp** |
| **server-dns-names** (_Comma separated domain name list default:_ ) | To set the NTP server using its domain name. The domain name will be resolved each time an NTP request is sent. Router has to have _/ip dns_ configured. |

**Status**

-   **active-server** (IP address; read-only property) : Currently selected NTP server address. This value is equal to **primary-ntp** or **secondary-ntp**.
-   **poll-interval** (Time interval; read-only property) : Current interval between requests sent to the active server. The initial value is 16 seconds, and it is increased by doubling to 15 minutes.

**Last received packet information**

Values of the following properties are reset when the SNTP client is stopped or restarted, either because of a configuration change, or because of a network error.

-   **last-update-from** (IP address; read-only property) : Source IP address of the last received NTP server packed that was successfully processed.
-   **last-update-before** (Time interval; read-only property) : Time since the last successfully received server message.
-   **last-adjustment** (Time interval; read-only property) : Amount of clock adjustment that was calculated from the last successfully received NTP server message.
-   **last-bad-packet-from** (IP address; read-only property) : Source IP address of last received SNTP packed that was not successfully processed. Reason of the failure and time since this packet was received is available in the next two properties.
-   **last-bad-packet-before** (Time interval; read-only property) : Time since the last receive failure.
-   **last-bad-packet-reason** (Text; read-only property) : Text that describes the reason of the last receive failure. Possible values are:
    -   _bad-packet-length_ \- Packet length is not in the acceptable range.
    -   _server-not-synchronized_ \- Leap Indicator field is set to "alarm condition" value, which means that clock on the server has not been synchronized yet.
    -   _zero-transmit-timestamp_ \- Transmit Timestamp field value is 0.
    -   _bad-mode_ \- Value of the Mode field is neither 'server' nor 'broadcast'.
    -   _kod-ABCD_ \- Received "KoD" (Kiss-o'-Death) response. _ABCD_ is the short "kiss code" text from the Reference Identifier field.
    -   _broadcast_ \- Received proadcast message, but **mode**\=_unicast_.
    -   _non-broadcast_ \- Received packed was server reply, but **mode**\=_broadcast_.
    -   _server-ip-mismatch_ \- Received response from address that is not **active-server**.
    -   _originate-timestamp-mismatch_ \- Originate Timestamp field in the server response message is not the same as the one included in the last request.
    -   _roundtrip-too-long_ \- request/response roundtrip exceeded 1 second.

## Client settings example: 

To check the status of the NTP client in CLI, use the "print" command

[?](https://help.mikrotik.com/docs/display/ROS/NTP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@ntp-example_v6] &gt; </code><code class="ros constants">/system ntp client </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">enabled</code><code class="ros constants">: no</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">primary-ntp</code><code class="ros constants">: 0.0.0.0</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">secondary-ntp</code><code class="ros constants">: 0.0.0.0</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">server-dns-names</code><code class="ros constants">:</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">mode</code><code class="ros constants">: unicast</code></div></div></td></tr></tbody></table>

To enable the NTP client and set IP addresses or FQDN of the NTP servers:

[?](https://help.mikrotik.com/docs/display/ROS/NTP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@ntp-example_v6] &gt; </code><code class="ros constants">/system ntp client </code><code class="ros functions">set </code><code class="ros value">enabled</code><code class="ros plain">=yes</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@ntp-example_v6] &gt; </code><code class="ros constants">/system ntp client </code><code class="ros functions">print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">enabled</code><code class="ros constants">: yes</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">primary-ntp</code><code class="ros constants">: 0.0.0.0</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">secondary-ntp</code><code class="ros constants">: 0.0.0.0</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">server-dns-names</code><code class="ros constants">:</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">mode</code><code class="ros constants">: unicast</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">dynamic-servers</code><code class="ros constants">: x.x.x.x, x.x.x.x</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">poll-interval</code><code class="ros constants">: 15s</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">active-server</code><code class="ros constants">: x.x.x.x</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">last-update-from</code><code class="ros constants">: x.x.x.x</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">last-update-before</code><code class="ros constants">: 6s570ms</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">last-adjustment</code><code class="ros constants">: -1ms786us</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros plain">[admin@ntp-example_v6] &gt; </code><code class="ros constants">/system ntp client </code><code class="ros functions">set </code><code class="ros value">primary-ntp</code><code class="ros plain">=162.159.200.123</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros plain">[admin@ntp-example_v6] &gt; </code><code class="ros constants">/system ntp client </code><code class="ros functions">print</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">enabled</code><code class="ros constants">: yes</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">primary-ntp</code><code class="ros constants">: 162.159.200.123</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">secondary-ntp</code><code class="ros constants">: 0.0.0.0</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">server-dns-names</code><code class="ros constants">:</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">mode</code><code class="ros constants">: unicast</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">dynamic-servers</code><code class="ros constants">: x.x.x.x, x.x.x.x</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">poll-interval</code><code class="ros constants">: 16s</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">active-server</code><code class="ros constants">: x.x.x.x</code></div></div></td></tr></tbody></table>

## NTP Server settings:

Server configuration is located in **/system ntp server**

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

|     |
| --- |  |
|     |

**enabled** (_yes_ or _no_; default value: _no_)

 | Enable  NTP server |
| 

**broadcast** (_yes_ or _no_; default value: _no_)

 | Enable certain NTP server mode, for this mode to work you have to set up broadcast-addresses field |
| 

**multicast** (_yes_ or _no_; default value: _no_)

 | Enable certain NTP server mode |
| 

**manycast** (_yes_ or _no_; default value: _no_)

 | Enable certain NTP server mode |
| 

**broadcast-addresses** (_IP address_; default value: )

 | Set broadcast address to use for NTP server broadcast mode |

_**Example:**_

Set up an NTP server for the local network that is 192.168.88.0/24

[?](https://help.mikrotik.com/docs/display/ROS/NTP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system ntp server </code><code class="ros functions">set </code><code class="ros value">broadcast</code><code class="ros plain">=yes</code> <code class="ros value">broadcast-addresses</code><code class="ros plain">=192.168.88.255</code> <code class="ros value">enabled</code><code class="ros plain">=yes</code> <code class="ros value">manycast</code><code class="ros plain">=no</code></div></div></td></tr></tbody></table>

# RouterOS version 7

## NTP Client properties:

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

|                                                      |
| ---------------------------------------------------- | ------------------------------------------ |
| **enabled** (_yes, no default: no_)                  | Enable NTP client for time synchronization |
| **mode** (_broadcast, manycast, multicast, unicast_) | Mode that the NTP client will operate in   |
|                                                      |

**NTP servers**

 | 

The list of NTP servers. It is possible to add static entries.

The following formats are accepted:

\- _FQDN ("Resolved Address" will appear in the "Servers"- window in an appropriate column if the address is resolved) or IP address can be used. If DHCP-Client property **use-peer-ntp=yes** - the dynamic entries advertised by [DHCP](https://help.mikrotik.com/docs/display/ROS/DHCP)_  
_\- _ipv4_  
\- _ipv4_`@`_vrf_  
\- _ipv6_  
\- _ipv6_`@`_vrf_  
\- _ipv6-linklocal_`%`_interface__

 |
| **vrf** (_default: main_) | Virtual Routing and Forwarding |
| **Servers** (_Button/Section_) | 

A detailed table of dynamically and statically added NTP servers (Address, Resolved address, Min Poll, Max Poll, iBurst, Auth. Key)

To set the NTP server using its FQDN. The domain name will be resolved each time an NTP request is sent. Router has to have _/ip/dns_ configured.

 |
| 

**Peers**

 | 

Current parameter values

[?](https://help.mikrotik.com/docs/display/ROS/NTP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@ntp-example_v7] &gt; </code><code class="ros constants">/system/ntp/monitor-peers</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros value">type</code><code class="ros plain">=</code><code class="ros string">"ucast-client"</code> <code class="ros value">address</code><code class="ros plain">=x.x.x.x</code> <code class="ros value">refid</code><code class="ros plain">=</code><code class="ros string">"y.y.y.y"</code> <code class="ros value">stratum</code><code class="ros plain">=3</code> <code class="ros value">hpoll</code><code class="ros plain">=10</code> <code class="ros value">ppoll</code><code class="ros plain">=10</code> <code class="ros value">root-delay</code><code class="ros plain">=28.869</code> <code class="ros plain">ms </code><code class="ros value">root-disp</code><code class="ros plain">=50.994</code> <code class="ros plain">ms</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros value">offset</code><code class="ros plain">=-0.973</code> <code class="ros plain">ms </code><code class="ros value">delay</code><code class="ros plain">=0.522</code> <code class="ros plain">ms </code><code class="ros value">disp</code><code class="ros plain">=15.032</code> <code class="ros plain">ms </code><code class="ros value">jitter</code><code class="ros plain">=0.521</code> <code class="ros plain">ms</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">-- [Q quit|D dump|C-z pause]</code></div></div></td></tr></tbody></table>











 |
| 

**Keys**

 | 

NTP symmetric keys, used for authentication between the NTP client and server. Key Identifier (Key ID) - an integer identifying the cryptographic key used to generate the message-authentication code.



 |

**Status**

-   **synchronized, stopped, waiting, using-local-clock** \- Current status of the NTP client
-   **Frequency drift** - The fractional frequency drift per unit time.
-   **synced-server** - The IP address of the NTP Server.
-   **synced-stratum** - The accuracy of each server is defined by a number called the stratum, with the topmost level (primary servers) assigned as one and each level downwards (secondary servers) in the hierarchy assigned as one greater than the preceding level.
-   **system-offset** - This is a signed, fixed-point number indicating the offset of the NTP server's clock relative to the local clock, in seconds.

## NTP Server settings:

Server configuration is located in **/system ntp server**

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

|                                                  |
| ------------------------------------------------ | ----------------- |
| **enabled** (_yes_ or _no_; default value: _no_) | Enable NTP server |
|                                                  |

**broadcast** (_yes_ or _no_; default value: _no_)

 | Enable certain NTP server mode, for this mode to work you have to set up broadcast-addresses field |
| 

**multicast** (_yes_ or _no_; default value: _no)_

 | Enable certain NTP server mode |
| 

**manycast** (_yes_ or _no_; default value: _no)_

 | Enable certain NTP server mode |
| 

**broadcast-addresses** (_IP address_; default value: )

 | Set broadcast address to use for NTP server broadcast mode |
| 

**vrf** (_default: main_)

 | Virtual Routing and Forwarding |
| 

**use-local-clock** (_yes_ or _no_; default value: _no_)

 | The server will supply its local system time as valid if others are not available. |
| 

**local-clock-stratum**

 | Manually set stratum if **use-local-clock=yes** |
| 

**auth-key** (default value: _none_)

 | NTP symmetric key, used for authentication between the NTP client and server. Key Identifier (Key ID) - an integer identifying the cryptographic key used to generate the message-authentication code. |

# Log messages

SNTP client can produce the following log messages. See the article "[log](https://wiki.mikrotik.com/wiki/Log "Log")" on how to set up logging and how to inspect logs.

-   **ntp**,**debug** gradually adjust by _OFFS_
-   **ntp**,**debug** instantly adjust by _OFFS_
-   **ntp**,**debug** Wait for _N_ seconds before sending the next message
-   **ntp**,**debug** Wait for _N_ seconds before restarting
-   **ntp**,**debug**,**packet** packet receive an error, restarting
-   **ntp**,**debug**,**packet** received _PKT_
-   **ntp**,**debug**,**packet** ignoring received _PKT_
-   **ntp**,**debug**,**packet** error sending to _IP_, restarting
-   **ntp**,**debug**,**packet** sending to _IP_ _PKT_

Explanation of log message fields

-   _OFFS_ \- difference of two NTP timestamp values, in hexadecimal.
-   _PKT_ \- dump of NTP packet. If the packet is shorter than the minimum 48 bytes, it is dumped as a hexadecimal string. Otherwise, the packet is dumped as a list of field names and values, one per log line. Names of fields follow RFC4330.
-   _IP_ \- remote IP address.

**NOTE**: the above logging rules work only with the built-in SNTP client, the separate NTP package doesn't have any logging facilities.