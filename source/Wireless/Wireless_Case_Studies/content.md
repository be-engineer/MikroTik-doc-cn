# Summary

The virtual Private Lan Service (VPLS) interface can be considered a tunnel interface just like the [EoIP](https://help.mikrotik.com/docs/display/ROS/EoIP) interface. To achieve transparent ethernet segment forwarding between customer sites.

Negotiation of VPLS tunnels can be done by LDP protocol or MP-BGP - both endpoints of tunnel exchange labels they are going to use for the tunnel.

Data forwarding in the tunnel happens by imposing 2 labels on packets: tunnel label and transport label - a label that ensures traffic delivery to the other endpoint of the tunnel.

  
MikroTik RouterOS implements the following VPLS features:

-   VPLS LDP signaling (RFC 4762)
-   Cisco style static VPLS pseudowires (RFC 4447 FEC type 0x80)
-   VPLS pseudowire fragmentation and reassembly (RFC 4623)
-   VPLS MP-BGP based autodiscovery and signaling (RFC 4761)
-   Cisco VPLS BGP-based auto-discovery (draft-ietf-l2vpn-signaling-08)
-   support for multiple import/export route-target extended communities for BGP based VPLS (both, RFC 4761 and draft-ietf-l2vpn-signaling-08)

  

# VPLS Prerequisities

For VPLS to be able to transport MPLS packets, one of the label distribution protocols should be already running on the backbone, it can be LDP, RSVP-TE, or static bindings.

Before moving forward, familiarize yourself with the [prerequisites required for LDP](https://help.mikrotik.com/docs/display/ROS/LDP#LDP-PrerequisitesforMPLS) and prerequisites for RSVP-TE.

In case, if BGP should be used as a VPLS discovery and signaling protocol, the backbone should be running iBGP preferably with route reflector/s.

  

# Example Setup

Let's consider that we already have a working LDP setup from the [LDP configuration example](https://help.mikrotik.com/docs/display/ROS/LDP#LDP-ExampleSetup).

Routers R1, R3, and R4 have connected Customer A sites, and routers R1 and R3 have connected Customer B sites. Customers require transparent L2 connectivity between the sites.

  

  

# Reference

## General

**Sub-menu:** `/interface vpls`

  
List of all VPLS interfaces. This menu shows also dynamically created BGP-based VPLS interfaces.

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

|                                                                   |
| ----------------------------------------------------------------- | ---------------------------------------- |
| **arp** (_disabled                                                | enabled                                  | proxy-arp                                                                                                                      | reply-only_; Default: **enabled**)                                                                                                                                                                                                                                       | Address Resolution Protocol |
| **arp-timeout** (_time interval                                   | auto_; Default: auto)                    |
|                                                                   |
| **bridge** (_name_; Default:)                                     |
|                                                                   |
| **bridge-cost** (_integer \[0..4294967295\]_; Default: **50**)    | Cost of the bridge port.                 |
| **bridge-horizon** (_none                                         | integer_; Default: **none**)             | If set to **none** bridge horizon will not be used.                                                                            |
| **cisco-static-id** (_integer \[0..4294967295\]_; Default: **0**) | Cisco-style VPLS tunnel ID.              |
| **comment** (_string_; Default: )                                 | Short description of the item            |
| **disable-running-check** (_yes                                   | no_; Default: **no**)                    | Specifies whether to detect if an interface is running or not. If set to **no** interface will always have the `running` flag. |
| **disabled** (_yes                                                | no_; Default: **yes**)                   | Defines whether an item is ignored or used. By default VPLS interface is disabled.                                             |
| **mac-address** (_MAC_; Default: )                                |
|                                                                   |
| **mtu** (_integer \[32..65536\]_; Default: **1500**)              |
|                                                                   |
| **name** (_string_; Default: )                                    | Name of the interface                    |
| **pw-l2mtu** (_integer \[0..65536\]_; Default: **1500**)          | L2MTU value advertised to a remote peer. |
| **pw-type** (_raw-ethernet                                        | tagged-ethernet                          | vpls_; Default: **raw-ethernet**)                                                                                              | Pseudowire type.                                                                                                                                                                                                                                                         |
| **peer** (_IP_; Default: )                                        | The IP address of the remote peer.       |
| **pw-control-word** (_disabled                                    | enabled                                  | default_; Default: **default**)                                                                                                | Enables/disables Control Word usage. Default values for regular and cisco style VPLS tunnels differ. Cisco style by default has control word usage disabled. Read more in the [VPLS Control Word](https://help.mikrotik.com/docs/display/ROS/VPLS+Control+Word) article. |
| **vpls-id** (_AsNum                                               | AsIp_; Default: )                        | A unique number that identifies the VPLS tunnel. Encoding is 2byte+4byte or 4byte+2byte number.                                |

  
**Read-only properties**

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

|                              |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **cisco-bgp-signaled** (_yes | no_)                                                                                                                                 |
|                              |
| **vpls** (_string_)          | name of the [bgp-vpls instance](https://wiki.mikrotik.com/wiki/Manual:Interface/VPLS#BGP_VPLS) used to create dynamic vpls interface |
| **bgp-signaled**             |
|                              |
| **bgp-vpls**                 |
|                              |
| **bgp-vpls-prfx**            |
|                              |
| **dynamic** (_yes            | no_)                                                                                                                                 |
|                              |
| **l2mtu** (integer)          |
|                              |
| **running** (_yes            | no_)                                                                                                                                 |
|                              |

### Monitoring

Command `/interface vpls monitor [id]` will display the current VPLS interface status

For example:

[?](https://help.mikrotik.com/docs/display/ROS/VPLS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@10.0.11.23] </code><code class="ros constants">/interface vpls&gt; </code><code class="ros functions">monitor </code><code class="ros plain">vpls2</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">remote-label</code><code class="ros constants">: 800000</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">local-label</code><code class="ros constants">: 43</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">remote-status</code><code class="ros constants">:</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">transport</code><code class="ros constants">: 10.255.11.201/32</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">transport-nexthop</code><code class="ros constants">: 10.0.11.201</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">imposed-labels</code><code class="ros constants">: 800000</code></div></div></td></tr></tbody></table>

Available read-only properties:

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

|                                     |
| ----------------------------------- | -------------------------------------------------------------------------------------------- |
| **imposed-label** (_integer_)       | VPLS imposed label                                                                           |
| **local-label** (_integer_)         | Local VPLS label                                                                             |
| **remote-group** ()                 |
|                                     |
| **remote-label** (_integer_)        | Remote VPLS label                                                                            |
| **remote-status** (_integer_)       |
|                                     |
| **transport-nexthop** (_IP prefix_) | Shows used transport address (typically Loopback address).                                   |
| **transport** (_string_)            | Name of the transport interface. Set if VPLS is running over the Traffic Engineering tunnel. |