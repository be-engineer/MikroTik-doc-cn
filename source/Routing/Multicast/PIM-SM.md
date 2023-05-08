# Summary

Protocol Independent Multicast - Sparse Mode (PIM-SM or PIM) enables RouterOS to support multicast streaming over the network area. Several configured PIM routers will make a multicast cloud where client devices can use IGMP to manage stream subscriptions. PIM should be used when the network topology is complex or stream sources are connected to a multicast cloud. Continuous cloud must have configured a unique rendezvous point for multicast groups and other participants should know how to reach the rendezvous point. In a simple case where on the part of the network only potential clients may reside and there are no stream sources, then [IGMP proxy](https://help.mikrotik.com/docs/display/ROS/IGMP+Proxy) can be used instead to preserve resources.

The feature is not supported on SMIPS devices (hAP lite, hAP lite TC and hAP mini).

# Property Reference

## Instance

The instance menu defines the main PIM-SM settings. The instance is then used for all other PIM-related configurations like interface-template, static RP, and Bootstrap Router.

**Sub-menu:** `/routing pimsm instance`

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
| **afi** (_ipv4 | ipv6_; Default: **ipv4**) | Specifies address family for PIM. |
| **bsm-forward-back** (_yes | no_; Default: ) | Currently not implemented. |
| **crp-advertise-contained** (_yes | no_; Default: ) | 

Currently not implemented.

 |
| **name** (_text_; Default: ) | Name of the instance. |
| **rp-hash-mask-length** (_integer: 0..4294967295_; Default: **30** (IPv4), or **126** (IPv6)) | The hash mask allows changing how many groups to map to one of the matching RPs. |
| **rp-static-override** (_yes | no_; Default: **no**) | Changes the selection priority for static RP. When disabled, the bootstrap RP set has a higher priority. When enabled, static RP has a higher priority. |
| **ssm-range** (_IPv4 | IPv6_; Default: ) | Currently not implemented. |
| **switch-to-spt** (_yes | no_; Default: **yes**) | Whether to switch to Shortest Path Tree (SPT) if multicast data bandwidth threshold is reached. The router will not proceed from protocol phase one (register encapsulation) to native multicast traffic flow if this option is disabled. It is recommended to enable this option. |
| **switch-to-spt-bytes** (_integer: 0..4294967295_; Default: **0**) | Multicast data bandwidth threshold. Switching to Shortest Path Tree (SPT) happens if this threshold is reached in the specified time interval. If a value of 0 is configured, switching will happen immediately. |
| **switch-to-spt-interval** (_time_; Default: ) | Time interval in which to account for multicast data bandwidth, used in conjunction with `switch-to-spt-bytes` to determine if the switching threshold is reached. |
| **vrf** (_name_; Default: main) | Name of the VRF. |

## Interface template

The interface template menu defines which interfaces will participate in PIM and what per-interface configuration will be used.

**Sub-menu:** `/routing pimsm interface-template`

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
| **hello-delay** (_time_; Default: **5s**) | Randomized interval for the initial Hello message on interface startup or detecting new neighbor. |
| **hello-period** (_time_; Default: **30s**) | Periodic interval for Hello messages. |
| **instance** (_name_; Default: ) | Name of the PIM instance this interface template belongs to. |
| **interfaces** (_name_; Default: **all**) | List of interfaces that will participate in PIM. |
| **join-prune-period** (_time_; Default: **1m**) |   
 |
| **join-tracking-support** (_yes | no_; Default: **yes**) | 

Sets the value of a Tracking (T) bit in the LAN Prune Delay option in the Hello message. When enabled, a router advertises its willingness to disable Join suppression. it is possible for upstream routers to explicitly track the join membership of individual downstream routers if Join suppression is disabled. Unless all PIM routers on a link negotiate this capability, explicit tracking and the disabling of the Join suppression mechanism are not possible.

 |
| **override-interval** (_time_; Default: **2s500ms**) | Sets the maximum time period over which to randomize when scheduling a delayed override Join message on a network that has join suppression enabled. |
| **priority** (_integer: 0..4294967295_; Default: **1**) | The Designated Router (DR) priority. A single Designated Router is elected on each network. The priority is used only if all neighbors have advertised a priority option. Numerically largest priority is preferred. In case of a tie or if priority is not used - the numerically largest IP address is preferred. |
| **propagation-delay** (_time_; Default: **500ms**) | 

Sets the value for a prune pending timer. It is used by upstream routers to figure out how long they should wait for a Join override message before pruning an interface that has join suppression enabled.

 |
| **source-addresses** (_IPv4 | IPv6_; Default: ) |   
 |

## Interface

The interface menu shows all interfaces that are currently participating in PIM and their statuses. This menu contains dynamic and read-only entries that get created by defined interface templates.

**Sub-menu:** `/routing pimsm interface`

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
| **address** (_IP%interface@vrf_) | Shows IP address, interface, and VRF. |
| **designated-router** (_yes | no_) |   
 |
| **dr** (_yes | no_) |   
 |
| **dynamic** (_yes | no_) |   
 |
| **instance** (_name_) | Name of the PIM instance this interface template belongs to. |
| **join-tracking** (_yes | no_) | 

  


 |
| **override-interval** (_time_) |   
 |
| **priority** (_integer: 0..4294967295_) |   
 |
| **propagation-delay** (_time_) |   
 |

## Neighbor

The neighbor menu shows all detected neighbors that are running PIM and their statuses. This menu contains dynamic and read-only entries.

**Sub-menu:** `/routing pimsm neighbor`

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
| **address** (_IP%interface_) | Shows the neighbor's IP address and local interface the neighbor is detected on. |
| **designated-router** (_yes | no_) | 

Shows whether the neighbor is elected as Designated Router (DR).

 |
| **instance** (_name_) | Name of the PIM instance this neighbor is detected on. |
| **join-tracking** (_yes | no_) | 

Indicates the neighbor's value of a Tracking (T) bit in the LAN Prune Delay option in the Hello message.

 |
| **override-interval** (_time_) | Indicates the neighbor's value of the override interval in the LAN Prune Delay option in the Hello message. |
| **priority** (_integer: 0..4294967295_) | Indicates the neighbor's priority value. |
| **propagation-delay** (_time_) | Indicates the neighbor's value of the propagation delay in the LAN Prune Delay option in the Hello message. |
| **timeout** (_time_) | Shows the reminding time after the neighbor is removed from the list if no new Hello message is received. The hold time equals to neighbor's `hello-period` \* 3.5.  |

## Static RP

The static-rp menu allows manually defining the multicast group to RP mappings. Such a mechanism is not robust to failures but does at least provide a basic interoperability mechanism.

**Sub-menu:** `/routing pimsm static-rp`

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
| **address** (_IPv4 | IPv6_; Default: ) | The IP address of the static RP. |
| **group** (_IPv4 | IPv6_; Default: **224.0.0.0/4**) | The multicast group that belongs to a specific RP. |
| **instance** (_name_; Default: ) | Name of the PIM instance this static RP belongs to. |

## Upstream Information Base

The upstream information base menus show the any-source multicast (\*,G) and source-specific multicast (S,G) groups and their statuses. These menus contain only read-only entries.

**Sub-menu:** `/routing pimsm uib-g`

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
| **group** (_IPv4 | IPv6_) | The multicast group address. |
| **instance** (_name_) | Name of the PIM instance the multicast group is created on. |
| **rp** (_IPv4 | IPv6_) | 

The address of the Rendezvous Point for this group.

 |
| **rp-local** (_yes | no_) | Indicates whether the multicast router itself is RP. |
| **rpf** (_IP%interface_) | The Reverse Path Forwarding (RPF) indicates the router address and outgoing interface that a Join message for that group is directed to. |

**Sub-menu:** `/routing pimsm uib-sg`

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
| **group** (_IPv4 | IPv6_) | The multicast group address. |
| **instance** (_name_) | Name of the PIM instance the multicast group is created on. |
| **keepalive** (_yes | no_) |   
 |
| **register** (_join | join-pending | prune_) |   
 |
| **rpf** (_IP%interface_) | The Reverse Path Forwarding (RPF) indicates the router address and outgoing interface that a Join message for that group is directed to. |
| **source** (_IPv4 | IPv6_) | The source IP address of the multicast group. |
| **spt-bit** (_yes | no_) | 

The Shortest Path Tree (SPT) bit indicates whether forwarding is taking place on the (S,G) Shortest Path Tree or on the (\*,G) tree. A router can have an (S,G) state and still be forwarding on a (\*,G) state during the interval when the source-specific tree is being constructed. When SPT bit is false, only the (\*,G) forwarding state is used to forward packets from S to G. When SPT bit is true, both (\*,G) and (S,G) forwarding states are used.

 |