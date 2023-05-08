# Introduction

___

The Group Management Protocol allows any of the interfaces to become a receiver for the multicast stream. It allows testing the multicast routing and switching setups without using dedicated IGMP or MLD clients. The option is available since RouterOS v7.4 and it supports IGMP v1, v2, v3 and MLD v1, v2 protocols. 

Interfaces are using IGMP v3 and MLD v2 by default. In case IGMP v1, v2 or MLD v1 queries are received, the interfaces will fall back to the appropriate version. Once Group Management Protocol is created on the interface, it will send an unsolicited membership report (join) packet and respond to query messages. If the configuration is removed or disabled, the interface will send a leave message.

# Configuration options

___

This section describes the Group Management Protocol configuration options.

**Sub-menu:** `/routing gmp`

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
| **groups** (_IPv4 | IPv6_; Default: ) | The multicast group address to be used by the interface, multiple group addresses are supported. |
| **interfaces** (_name_; Default: ) | Name of the interface, multiple interfaces and interface lists are supported. |
| **exclude** (Default: ) | 

When `exclude` is set, the interface expects to reject multicast data from the configured `sources`. When this option is not used, the interfaces will emit source specific join for the configured `sources`.  


 |
| **sources** (_IPv4 | IPv6_; Default: ) | The source address list used by the interface, multiple source addresses are supported. This setting has an effect when IGMPv3 or MLDv2 protocols are active.  
 |

# Examples

___

This example shows how to configure a simple multicast listener on the interface.

First, add an IP address on the interface:

[?](https://help.mikrotik.com/docs/display/ROS/Group+Management+Protocol#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.10.10/24</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">network</code><code class="ros plain">=192.168.10.0</code></div></div></td></tr></tbody></table>

Then configure Group Management Protocol on the same interface:

[?](https://help.mikrotik.com/docs/display/ROS/Group+Management+Protocol#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/routing gmp</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">groups</code><code class="ros plain">=229.1.1.1</code> <code class="ros value">interfaces</code><code class="ros plain">=ether1</code></div></div></td></tr></tbody></table>

It is now possible to check your multicast network to see if routers or switches have created the appropriate multicast forwarding entries and whether multicast data is being received on the interface (see the interface stats, or use a [Packet Sniffer](https://help.mikrotik.com/docs/display/ROS/Packet+Sniffer) and [Torch](https://help.mikrotik.com/docs/display/ROS/Torch)).