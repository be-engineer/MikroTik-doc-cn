# Summary

___

Internet Group Management Protocol (IGMP) proxy can implement multicast routing. It is forwarding IGMP frames and is commonly used when there is no need for a more advanced protocol like PIM.

**IGMP proxy features:**

-   The simplest way how to do multicast routing;
-   Can be used in topologies where PIM-SM is not suitable for some reason;
-   It takes slightly less resources than PIM-SM;
-   Ease of configuration.

On the other hand, IGMP proxy is not well suited for complicated multicast routing setups. Compared to PIM-based solutions, IGMP proxy does not support more than one upstream interface and routing loops are not detected or avoided.

By default, IGMP proxy upstream interface will send IGMPv3 membership reports and it will detect what IGMP version the upstream device (e.g. multicast router) is using based on received queries. In case IGMPv1/v2 queries are received, the upstream port will fall back to the lower IGMP version. It will convert back to IGMPv3 when IGMPv1/v2 querier present timer (400s) expires. Downstream interfaces of IGMP proxy will only send IGMPv2 queries.

RouterOS v7 has IGMP proxy configuration available in the main **system** package. Older RouterOS versions need an additional **multicast** package installed in order to use IGMP proxy. See more details about [Packages](https://help.mikrotik.com/docs/display/ROS/Packages).

# Configuration options

___

General IGMP proxy configuration.

**Sub-menu:** `/routing igmp-proxy`

| 
Property



 | 

Description



 |
| --- | --- |
| 

Property



 | 

Description



 |
| --- | --- |
| **query-interval** (_time: 1s..1h_; Default: **2m5s**) | How often to send out IGMP Query messages over downstream interfaces. |
| **query-response-interval** (_time: 1s..1h_; Default: **10s**) | How long to wait for responses to an IGMP Query message. |
| **quick-leave** | Specifies action on IGMP Leave message. If quick-leave is on, then an IGMP Leave message is sent upstream as soon as a leave message is received from the first client on the downstream interface. Use **yes** only in case there is only one subscriber behind the proxy. |

Configure what interfaces will participate as IGMP proxy interfaces on the router. If an interface is not configured as an IGMP proxy interface, then all IGMP traffic received on it will be ignored.

**Sub-menu:** `/routing igmp-proxy interface`

| 
Property



 | 

Description



 |
| --- | --- |
| 

Property



 | 

Description



 |
| --- | --- |
| **alternative-subnets** (_IP/Mask_; Default: ) | By default, only packets from directly attached subnets are accepted. This parameter can be used to specify a list of alternative valid packet source subnets, both for data or IGMP packets. Has an effect only on the upstream interface. Should be used when the source of multicast data often is in a different IP network. |
| **interface** (_name_; Default: **all**) | Name of the interface. |
| **threshold**  (_integer: 0..4294967295_; Default: **1**) | Minimal TTL. Packets received with a lower TTL value are ignored |
| **upstream** (_yes | no_; Default: **no**) | The interface is called "upstream" if it's in the direction of the root of the multicast tree. An IGMP forwarding router must have exactly one upstream interface configured. The upstream interface is used to send out IGMP membership requests. |

It is possible to get detailed status information for each interface using the `print` `status` command.

[?](https://help.mikrotik.com/docs/display/ROS/IGMP+Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/routing igmp-proxy interface </code><code class="ros functions">print </code><code class="ros plain">status</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - inactive, D - dynamic; U - upstream</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp; U </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">threshold</code><code class="ros plain">=1</code> <code class="ros value">alternative-subnets</code><code class="ros plain">=</code><code class="ros string">""</code> <code class="ros value">upstream</code><code class="ros plain">=yes</code> <code class="ros value">source-ip-address</code><code class="ros plain">=192.168.10.10</code> <code class="ros value">rx-bytes</code><code class="ros plain">=3018487500</code> <code class="ros value">rx-packets</code><code class="ros plain">=2012325</code> <code class="ros value">tx-bytes</code><code class="ros plain">=0</code> <code class="ros value">tx-packets</code><code class="ros plain">=0</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1&nbsp;&nbsp;&nbsp; </code><code class="ros value">interface</code><code class="ros plain">=ether3</code> <code class="ros value">threshold</code><code class="ros plain">=1</code> <code class="ros value">alternative-subnets</code><code class="ros plain">=</code><code class="ros string">""</code> <code class="ros value">upstream</code><code class="ros plain">=no</code> <code class="ros value">querier</code><code class="ros plain">=yes</code> <code class="ros value">source-ip-address</code><code class="ros plain">=192.168.20.10</code> <code class="ros value">rx-bytes</code><code class="ros plain">=0</code> <code class="ros value">rx-packets</code><code class="ros plain">=0</code> <code class="ros value">tx-bytes</code><code class="ros plain">=2973486000</code> <code class="ros value">tx-packets</code><code class="ros plain">=1982324</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">2&nbsp;&nbsp;&nbsp; </code><code class="ros value">interface</code><code class="ros plain">=ether4</code> <code class="ros value">threshold</code><code class="ros plain">=1</code> <code class="ros value">alternative-subnets</code><code class="ros plain">=</code><code class="ros string">""</code> <code class="ros value">upstream</code><code class="ros plain">=no</code> <code class="ros value">querier</code><code class="ros plain">=yes</code> <code class="ros value">source-ip-address</code><code class="ros plain">=192.168.30.10</code> <code class="ros value">rx-bytes</code><code class="ros plain">=0</code> <code class="ros value">rx-packets</code><code class="ros plain">=0</code> <code class="ros value">tx-bytes</code><code class="ros plain">=152019000</code> <code class="ros value">tx-packets</code><code class="ros plain">=101346</code></div></div></td></tr></tbody></table>

| 
Property



 | 

Description



 |
| --- | --- |
| 

Property



 | 

Description



 |
| --- | --- |
| **querier** (_read-only; yes|no_) | Whether the interface is acting as an IGMP querier. |
| **source-ip-address**  (_read-only; IP address_) | The detected source IP for the interface. |
| **rx-bytes** (_read-only; integer_) | The total amount of received multicast traffic on the interface. |
| **rx-packet** (_read-only; integer_) | The total amount of received multicast packets on the interface. |
| **tx-bytes** (_read-only; integer_) | The total amount of transmitted multicast traffic on the interface. |
| **tx-packet** (_read-only; integer_) | The total amount of transmitted multicast packets on the interface. |

Multicast forwarding cache (MFC) status.

**Sub-menu:** `/routing igmp-proxy mfc`

| 
Property



 | 

Description



 |
| --- | --- |
| 

Property



 | 

Description



 |
| --- | --- |
| **active-downstream-interfaces** (_read-only: name_) | The packet stream is going out of the router through this interface. |
| **bytes** (_read-only: integer_) | The total amount of received multicast traffic. |
| **group** (_read-only: IP address_) | IGMP group address. |
| **packets** (_read-only: integer_) | The total amount of received multicast packets. |
| **source** (_read-only: IP address_) | The multicast data originator address. |
| **upstream-interface** (_read-only: name_) | The packet stream is coming into the router through this interface. |
| **wrong-packets** (_read-only: integer_) | 

The total amount of received multicast packets that arrived on a wrong interface, for example, a multicast stream that is received on a downstream interface instead of an upstream interface.

 |

RouterOS support static multicast forwarding rules for IGMP proxy. If a static rule is added, all dynamic rules for that group will be ignored. These rules will take effect only if IGMP-proxy interfaces are configured (upstream and downstream interfaces should be set) or these rules won't be active.

| 
Property



 | 

Description



 |
| --- | --- |
| 

Property



 | 

Description



 |
| --- | --- |
| **downstream-interfaces** (_name_; Default: ) | The received stream will be sent out to the listed interfaces only. |
| **group** (_read-only: IP address_) | The multicast group address this rule applies. |
| **source** (_read-only: IP address_) | The multicast data originator address. |
| **upstream-interface** (_read-only: name_) | The interface that is receiving stream data. |

# Examples

___

To forward all multicast data coming from the ether2 interface to the downstream bridge interface, where subscribers are connected, use the configuration below. Both interfaces should have an IP address.

[?](https://help.mikrotik.com/docs/display/ROS/IGMP+Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/routing igmp-proxy interface</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">upstream</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=bridge1</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/routing igmp-proxy interface </code><code class="ros plain">print</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: U - UPSTREAM</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: INTERFACE, THRESHOLD</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros comments">#&nbsp;&nbsp; INTERFACE&nbsp; THRESHOLD</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">0 U ether2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">1&nbsp;&nbsp; bridge1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1</code></div></div></td></tr></tbody></table>

You may also need to configure `alternative-subnets` on the upstream interface in case the multicast sender address is in an IP subnet that is not directly reachable from the local router:

[?](https://help.mikrotik.com/docs/display/ROS/IGMP+Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/routing igmp-proxy interface</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros value">upstream</code><code class="ros plain">=yes]</code> <code class="ros value">alternative-subnets</code><code class="ros plain">=192.168.50.0/24,192.168.60.0/24</code></div></div></td></tr></tbody></table>

To enable `quick-leave`, use the setting below:

[?](https://help.mikrotik.com/docs/display/ROS/IGMP+Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/routing igmp-proxy</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">quick-leave</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>