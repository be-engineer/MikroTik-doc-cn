# Overview

Wireless interface in any of _station_ modes will search for acceptable access point (AP) and connect to it. The connection between station and AP will behave in slightly different way depending on type of _station_ mode used, so correct mode must be chosen for given application and equipment. This article attempts to describe differences between available _station_ modes.

Primary difference between _station_ modes is in how L2 addresses are processed and forwarded across wireless link. This directly affects the ability of wireless link to be part of L2 bridged infrastructure.

If L2 bridging over wireless link is not necessary - as in case of routed or MPLS switched network, basic **mode=station** setup is suggested and will provide highest efficiency.

Availability of particular _station_ mode depends on **wireless-protocol** that is used in wireless network. Please refer to [applicability matrix](https://help.mikrotik.com/docs/display/ROS/Wireless+Station+Modes#WirelessStationModes-ApplicabilityMatrix) for information on mode support in protocols. It is possible that connection between station and AP will be established even if particular mode is not supported for given protocol. Beware that such connection will not behave as expected with respect to L2 bridging.

# 802.11 limitations for L2 bridging

Historically 802.11 AP devices were supposed to be able to bridge frames between wired network segment and wireless, but station device was not supposed to do L2 bridging.

Consider the following network:

```
[X]---[AP]-(     )-[STA]---[Y]

```

where X-to-AP and STA-to-Y are ethernet links, but AP-to-STA are connected wirelessly. According to 802.11, AP can transparently bridge traffic between X and STA, but it is not possible to bridge traffic between AP and Y, or X and Y.

802.11 standard specifies that frames between station and AP device must be transmitted in so called _3 address_ frame format, meaning that header of frame contains 3 MAC addresses. Frame transmitted from AP to station has the following addresses:

-   destination address - address of station device, also radio receiver address
-   radio transmitter address - address of AP
-   source address - address of originator of particular frame

Frame transmitted from station to AP has the following addresses:

-   radio receiver address - address of AP
-   source address - address of station device, also radio transmitter address
-   destination address

Considering that every frame must include radio transmitter and receiver address, it is clear that _3 address_ frame format is not suitable for transparent L2 bridging over station, because station can not send frame with source address different from its address - e.g. frame from Y, and at the same time AP can not format frame in a way that would include address of Y.

802.11 includes additional frame format, so called _4 address_ frame format, intended for "wireless distribution system" (WDS) - a system to interconnect APs wirelessly. In this format additional address is added, producing header that contains the following addresses:

-   radio receiver address
-   radio transmitter address
-   destination address
-   source address

This frame format includes all necessary information for transparent L2 bridging over wireless link. Unluckily 802.11 does not specify how WDS connections should be established and managed, therefore any usage of _4 address_ frame format (and WDS) is implementation specific.

Different _station_ modes attempt to solve shortcomings of standard station mode to provide support for L2 bridging.

# Applicability Matrix

The following matrix specifies _station_ modes available for each **wireless-protocol**. Note that there are 2 columns for 802.11 protocol: **802.11** specifies availability of mode in "pure" 802.11 network (when connecting to any vendor AP) and **ROS 802.11** specifies availability of mode when connecting to RouterOS AP that implements necessary proprietary extensions for mode to work.

_Table applies to RouterOS v5rc11 and above:_

| 
  


 | 

802.11

 | 

ROS 802.11

 | 

nstreme

 | 

nv2

|     |
| --- |  |  |  |  |
|     |

  


 | 

802.11

 | 

ROS 802.11

 | 

nstreme

 | 

nv2

|                                |
| ------------------------------ | --- | --- | --- | --- |
| **station**                    | V   | V   | V   | V   |
| **station-wds**                |
| V                              | V   | V   |
| **station-pseudobridge**       | V   | V   | V   |
|                                |
| **station-pseudobridge-clone** | V   | V   | V   |
|                                |
| **station-bridge**             |
| V                              | V   | V   |

# Mode _station_

This is standard mode that does not support L2 bridging on station - attempts to put wireless interface in bridge will not produce expected results. On the other hand this mode can be considered the most efficient and therefore should be used if L2 bridging on station is not necessary - as in case of routed or MPLS switched network. This mode is supported for all wireless protocols.

# Mode _station-wds_

This mode works only with RouterOS APs. As a result of negotiating connection, separate WDS interface is created on AP for given station. This interface can be thought of point-to-point connection between AP and given station - whatever is sent out WDS interface is delivered to station (and only to particular station) and whatever station sends to AP is received from WDS interface (and not subject to forwarding between AP clients), preserving L2 addresses.

This mode is supported for all wireless protocols except when 802.11 protocol is used in connection to non-RouterOS device. Mode uses _4 address_ frame format when used with 802.11 protocol, for other protocols (such as nstreme or nv2), protocol internal means are used.

This mode is safe to use for L2 bridging and gives most administrative control on AP by means of separate WDS interface, for example use of bridge firewall, RSTP for loop detection and avoidance, etc.

With station-wds mode, it is not possible to connect to CAPsMAN controlled CAP.

# Mode _station-pseudobridge_

From the wireless connection point of view, this mode is the same as standard station mode. It has limited support for L2 bridging by means of some services implemented in station:

-   MAC address translation for IPv4 packets - station maintains IPv4-to-MAC mapping table and replaces source MAC address with its own address when sending frame to AP (in order to be able to use _3 address_ frame format), and replaces destination MAC address with address from mapping table for frames received from AP. IPv4-to-MAC mappings are built also for VLAN encapsulated frames.
-   single MAC address translation for the rest of protocols - station learns source MAC address from first forwarded non-IPv4 frame and uses it as default for reverse translation - this MAC address is used to replace destination MAC address for frames received from AP if IPv4-to-MAC mapping can not be performed (e.g. - non-IPv4 frame or missing mapping).

This mode is limited to complete L2 bridging of data to single device connected to station (by means of single MAC address translation) and some support for IPv4 frame bridging - bridging of non-IP protocols to more than one device will not work. Also MAC address translation limits access to station device from AP side to IPv4 based access - the rest of protocols will be translated by single MAC address translation and will not be received by station itself.

This mode is available for all protocols except nv2 and **should be avoided when possible**. The usage of this mode can only be justified if AP does not support better mode for L2 bridging (e.g. when non-RouterOS AP is used) or if only one end-user device must be connected to network by means of station device.

# Mode _station-pseudobridge-clone_

This mode is the same as _station-pseudobridge_ mode, except that it connects to AP using "cloned" MAC address - that is either address configured in **station-bridge-clone-mac** parameter (if configured) or source address of first forwarded frame. This essentially appears on AP as if end-user device connected to station connected to AP.

# Mode _station-bridge_

This mode works only with RouterOS APs and provides support for transparent protocol-independent L2 bridging on the station device. RouterOS AP accepts clients in _station-bridge_ mode when enabled using **bridge-mode** parameter. In this mode, the AP maintains a forwarding table with information on which MAC addresses are reachable over which station device.

This mode is MikroTik proprietary and cannot be used to connect to other brands of devices.

This mode is safe to use for L2 bridging and is the preferred mode unless there are specific reasons to use _station-wds_ mode. With station-bridge mode, it is not possible to connect to CAPsMAN controlled CAP.