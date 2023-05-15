# Label Range and TTL

From the `/mpls settings` menu it is possible to assign specific dynamic label range and TTL propagation. If for some reason static label mapping is used then the dynamic range can be adjusted to exclude statically assigned label numbers from being dynamically assigned by any of the label distribution protocols.

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

|                                                                                      |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **dynamic-label-range** (_range of integer\[16..1048575\]_; Default: **16-1048575**) | Range of Label numbers used for dynamic allocation. The first 16 labels are reserved for special purposes (as defined in RFC). If you intend to configure labels statically then adjust the dynamic default range not to include numbers that will be used in a static configuration. |
| **propagate-ttl** (_yes                                                              | no_; Default: **yes**)                                                                                                                                                                                                                                                                | Whether to copy TTL values from IP header to MPLS header. If this option is set to **no** then hops inside the MPLS cloud will be invisible from traceroutes. |
| **allow-fast-path(**_yes                                                             | no_; Default: **yes)**                                                                                                                                                                                                                                                                | Enable/disable MPLS fast-path support.                                                                                                                        |

# MPLS MTU

Configuration of MPLS MTU (path MTU + MPLS tag size) is useful in cases when there is a large variety of possible MTUs along the path. Configuring MPLS MTU to a minimum value that can pass all the hops will ensure that the MPLS packet will not be silently dropped on the devices that do not support big enough MTU.

MPLS MTUs are configured from the `/mpls interface` menu.

[?](https://help.mikrotik.com/docs/display/ROS/MPLS+MTU%2C+Forwarding+and+Label+Bindings#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@rack1_b35_CCR1036] /mpls/interface&gt; print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: X - disabled; * - builtin</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">0&nbsp;&nbsp;&nbsp; ;;; router-test</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">interface=ether1 mpls-mtu=1580 input=yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">1&nbsp;&nbsp;&nbsp; ;;; router-test</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">interface=ether2 mpls-mtu=1580 input=yes</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">2&nbsp;&nbsp;&nbsp; interface=all mpls-mtu=1500</code></div></div></td></tr></tbody></table>

  

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

|                                                            |
| ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **comment** (_string_; Default: )                          | Short description of the interface                                                              |
| **disabled** (_yes                                         | no_; Default: **no**)                                                                           | If set to **yes** then this configuration is ignored. |
| **interface** (_name_; Default:)                           | Name of the interface or interface-list to match.                                               |
| **input** (_yes                                            | no_; Default: **yes**)                                                                          | Whether to allow MPLS input on the interface          |
| **mpls-mtu** (_integer \[512..65535\]_; Default: **1508**) | The option represents how big packets can be carried over the interface with added MPLS labels. |

  

Listed entries are ordered, and the first entry (iterating from the top to the bottom) that matches the interface will be used.

The order of the entries is important due to the possibility that different interface lists can contain the same interface and in addition, that interface can be referenced directly.

Selection of the MPLS MTU happens in the following manner:

-   If the interface matched the entry from this table, then try to use configured MPLS MTU value
-   If the interface does not match any entry then consider MPLS MTU equal to L2MTU
-   If the interface does not support L2MTU, then consider MPLS MTU equal to L3 MTU

On the MPLS ingress path, MTU is chosen by min(MPLS MTU - tagsize, l3mtu). This means that on interfaces that do not support L2MTU and default L3 MTU is set to 1500, max path MTU will be 1500 - tag size (the interface will not be able to pass full IP frame without fragmentation). In such scenarios, L3MTU must be increased by max observed tag size.

Read more on MTUs in the [MTU in RouterOS](https://help.mikrotik.com/docs/display/ROS/MTU+in+RouterOS) article.

  

## Forwarding Table

Entries in the `/mpls forwarding-table` menu show label bindings for specific routes that will be used in MPLS label switching. Properties in this menu are read-only.

[?](https://help.mikrotik.com/docs/display/ROS/MPLS+MTU%2C+Forwarding+and+Label+Bindings#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@rack1_b35_CCR1036] /mpls/forwarding-table&gt; print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: L, V - VPLS</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Columns: LABEL, VRF, PREFIX, NEXTHOPS</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">#&nbsp;&nbsp; LABEL&nbsp; VRF&nbsp;&nbsp; PREFIX&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; NEXTHOPS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">0 L&nbsp;&nbsp;&nbsp; 16&nbsp; main&nbsp; 10.0.0.0/8&nbsp;&nbsp;&nbsp;&nbsp; { nh=10.155.130.1; interface=ether12 }&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text plain">1 L&nbsp;&nbsp;&nbsp; 18&nbsp; main&nbsp; 111.111.111.3&nbsp; { label=impl-null; nh=111.12.0.1; interface=ether2 }</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain">2 L&nbsp;&nbsp;&nbsp; 17&nbsp; main&nbsp; 111.111.111.2&nbsp; { label=impl-null; nh=111.11.0.1; interface=ether1 }</code></div></div></td></tr></tbody></table>

  

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

|                        |
| ---------------------- | ------------------------------------------------ |
| **prefix** (_IP/Mask_) | Destination prefix for which labels are assigned |
| **label** (_integer_)  | Ingress MPLS label                               |
| **ldp** (_yes          | no_)                                             | Whether labels are [LDP](https://help.mikrotik.com/docs/display/ROS/LDP) signaled |
| **nexthops** ()        |

An array of the next-hops, each entry in the array represents one ECMP next-hop. Array entry can contain several parameters:

-   **label** - egress MPLS label
-   **nh** - out next-hop IP address
-   **interface** - out the interface

 |
| **out-label** (_integer_) | Label number which is added or switched to for outgoing packet. |
| **packets** (_integer_) | Number of packets matched by this entry |
| **te-sender** |   
 |
| **te-session**  |   
 |
| **traffic-eng**  | Shows whether the entry is signaled by RSVP-TE (Traffic Engineering) |
| **type** _(string)_ | Type of the entry, for example, "vpls", etc. |
| **vpls** (_yes | no_) | Shows whether the entry is used for [VPLS](https://help.mikrotik.com/docs/display/ROS/VPLS) tunnels. |
| **vpn** |   
 |
| **vrf** | Name of the VRF table this entry belongs to |