# Introduction

`/ip firewall connection`

There are several ways to see what connections are making their way through the router.

In the Winbox Firewall window, you can switch to the Connections tab, to see current connections to/from/through your router. It looks like this:

![](https://help.mikrotik.com/docs/download/attachments/130220087/Screenshot_1.png?version=1&modificationDate=1653993869514&api=v2)

## Properties

All properties in the connection list are read-only

| 属性                                   | 说明                                                                                                    |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **assured** (_yes                      | no_)                                                                                                    | Indicates that this connection is assured and that it will not be erased if the maximum possible tracked connection count is reached. |
| **confirmed** (_yes                    | no_)                                                                                                    | Connection is confirmed and a packet is sent out from the device.                                                                     |
| **connection-mark** (_string_)         | Connection mark that was set by mangle rule.                                                            |
| **connection-type** (_pptp             | ftp_)                                                                                                   | Type of connection, the 属性 is empty if connection tracking is unable to determine a predefined connection type.                     |
| **dst-address** (_ip\[:port\]_)        | Destination address and port (if a protocol is port-based).                                             |
| **dstnat** (_yes                       | no_)                                                                                                    | A connection has gone through DST-NAT (for example, port forwarding).                                                                 |
| **dying** (_yes                        | no_)                                                                                                    | The connection is dying due to connection timeout.                                                                                    |
| **expected** (_yes                     | no_)                                                                                                    | Connection is set up using connection helpers (pre-defined service rules).                                                            |
| **fasttrack** (_yes                    | no_)                                                                                                    | Whether the connection is FastTracked.                                                                                                |
| **gre-key** (_integer_)                | Contents of the GRE Key field.                                                                          |
| **gre-protocol** (_string_)            | Protocol of the encapsulated payload.                                                                   |
| **gre-version** (_string_)             | A version of the GRE protocol was used in the connection.                                               |
| **icmp-code** (_string_)               | ICMP Code Field                                                                                         |
| **icmp-id** (_integer_)                | Contains the ICMP ID                                                                                    |
| **icmp-type** (_integer_)              | ICMP Type Number                                                                                        |
| **orig-bytes** (_integer_)             | Amount of bytes sent out from the source address using the specific connection.                         |
| **orig-fasttrack-bytes** (_integer_)   | Amount of FastTracked bytes sent out from the source address using the specific connection.             |
| **orig-fasttrack-packets** (_integer_) | Amount of FastTracked packets sent out from the source address using the specific connection.           |
| **orig-packets** (_integer_)           | Amount of packets sent out from the source address using the specific connection.                       |
| **orig-rate** (_integer_)              | The data rate at which packets are sent out from the source address using the specific connection.      |
| **protocol** (_string_)                | IP protocol type                                                                                        |
| **repl-bytes** (_integer_)             | Amount of bytes received from the destination address using the specific connection.                    |
| **repl-fasttrack-bytes** (_string_)    | Amount of FastTracked bytes received from the destination address using the specific connection.        |
| **repl-fasttrack-packets** (_integer_) | Amount of FastTracked packets received from the destination address using the specific connection.      |
| **repl-packets** (_integer_)           | Amount of packets received from the destination address using the specific connection.                  |
| **repl-rate** (_string_)               | The data rate at which packets are received from the destination address using the specific connection. |
| **reply-dst-address** (_ip\[:port\]_)  | Destination address (and port) expected of return packets. Usually the same as "src-address: port"      |
| **reply-src-address** (_ip\[:port\]_)  | Source address (and port) expected of return packets. Usually the same as "dst-address: port"           |
| **seen-reply** (_yes                   | no_)                                                                                                    | The destination address has replied to the source address.                                                                            |
| **src-address** (_ip\[:port\]_)        | The source address and port (if a protocol is port-based).                                              |
| **srcnat** (_yes                       | no_)                                                                                                    | Connection is going through SRC-NAT, including packets that were masqueraded through NAT.                                             |
| **tcp-state** (_string_)               | The current state of TCP connection :                                                                   |
- "established"
- "time-wait"
- "close"
- "syn-sent"
- "syn-received" |
| **timeout** (_time_) | Time after connection will be removed from the connection list. |

# Connection tracking settings

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall connection tracking</code></div></div></td></tr></tbody></table>

### Properties


| 属性                                                   | 说明                                                                              |
| ------------------------------------------------------ | --------------------------------------------------------------------------------- |
| **enabled** (_yes                                      | no                                                                                | auto_; Default: **auto**) | Allows to disable or enable connection tracking. Disabling connection tracking will cause several firewall features to stop working. See the [list](https://wiki.mikrotik.com/wiki/Manual:IP/Firewall/Connection_tracking#Features_affected_by_connection_tracking) of affected features. Starting from v6.0rc2 default value is auto. This means that connection tracing is disabled until at least one firewall rule is added. |
| **loose-tcp-tracking** (_yes_; Default: **yes**)       | Disable picking up already established connections                                |
| **tcp-syn-sent-timeout** (_time_; Default: **5s**)     | TCP SYN timeout.                                                                  |
| **tcp-syn-received-timeout** (_time_; Default: **5s**) | TCP SYN timeout.                                                                  |
| **tcp-established-timeout** (_time_; Default: **1d**)  | Time when established TCP connection times out.                                   |
| **tcp-fin-wait-timeout** (_time_; Default: **10s**)    |
|                                                        |
| **tcp-close-wait-timeout** (_time_; Default: **10s**)  |
|                                                        |
| **tcp-last-ack-timeout** (_time_; Default: **10s**)    |
|                                                        |
| **tcp-time-wait-timeout** (_time_; Default: **10s**)   |
|                                                        |
| **tcp-close-timeout** (_time_; Default: **10s**)       |
|                                                        |
| **udp-timeout** (_time_; Default: **10s**)             | Specifies the timeout for UDP connections that have seen packets in one direction |
| **udp-stream-timeout** (_time_; Default: **3m**)       | Specifies the timeout of UDP connections that has seen packets in both directions |
| **icmp-timeout** (_time_; Default: **10s**)            | ICMP connection timeout                                                           |
| **generic-timeout** (_time_; Default: **10m**)         | Timeout for all other connection entries                                          |
  
**Read-only properties**

| 属性                                                           | 说明                                                                                                                                                                                                                                                                                                                          |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **max-entries** (_integer_)                                    | Max amount of entries that the connection tracking table can hold. This value depends on the installed amount of RAM. Note that the system does not create a maximum size connection tracking table when it starts, the maximum entry amount can increase if the situation demands it and the router still has free ram left. |
| **total-entries** (_integer_)                                  |
| Amount of connections that the current connection table holds. |
