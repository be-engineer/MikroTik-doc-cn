## Summary

MikroTik RouterOS implements RIP version 2 (RFC 2453). Version 1 (RFC 1058) is not supported.

RIP enables routers in an autonomous system to exchange routing information. It always uses the best path (the path with the fewest number of hops (i.e. routers)) available.

  

## General

**Sub-menu:** `/routing rip instance`

  

<table class="wrapped confluenceTable" style="margin-left: 14.4318px;"><colgroup><col><col></colgroup><tbody><tr><th class="confluenceTh">Property</th><th class="confluenceTh">Description</th></tr><tr><td class="confluenceTd"><strong>name</strong><span>&nbsp;</span></td><td class="confluenceTd">name of the instance</td></tr><tr><td class="confluenceTd"><strong>vrf</strong><span>&nbsp;</span>(&nbsp;Default:<span> <strong>main</strong></span>)</td><td class="confluenceTd">which <a href="https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206" rel="nofollow">VRF</a> to use</td></tr><tr><td class="confluenceTd"><strong>afi</strong><span>&nbsp;</span>(<em>ipv4 | ipv6</em>; Default:<span> </span>)</td><td class="confluenceTd">specifies which afi to use.</td></tr><tr><td class="confluenceTd"><span><strong>in-filter-chain</strong> </span>(Default:<span>&nbsp;</span>)</td><td class="confluenceTd">input filter chain</td></tr><tr><td class="confluenceTd"><strong>out-filter-chain</strong> (Default:<span> </span>)</td><td class="confluenceTd">output filter chain</td></tr><tr><td class="confluenceTd"><span><strong>out-filter-select</strong> </span>(Default:<span>&nbsp;</span>)</td><td class="confluenceTd">output filter select rule chain</td></tr><tr><td class="confluenceTd"><span><strong>redistribute</strong> </span>(<em>bgp, bgp-mpls-vpn, connected, dhcp, fantasy, modem, ospf, rip, static, vpn</em>; Default:<span> </span>)</td><td class="confluenceTd">which routes to redistribute</td></tr><tr><td class="confluenceTd"><span><strong>originate-default</strong> </span>( Default:)</td><td class="confluenceTd">whether to originate default route</td></tr><tr><td class="confluenceTd"><span><strong>routing-table</strong> </span>( Default: main)</td><td class="confluenceTd"><span style="color: rgb(32,33,34);">in which routing table the routes will be added</span></td></tr><tr><td class="confluenceTd"><span><strong>route-timeout</strong> </span>(Default:<span>&nbsp;</span>)</td><td class="confluenceTd">route timeout</td></tr><tr><td class="confluenceTd"><strong>route-gc-timeout</strong> &nbsp;(Default:<span> </span>)</td><td class="confluenceTd"><br></td></tr><tr><td class="confluenceTd"><strong>update-interval</strong> (<em>time</em>; Default:<span> </span>)</td><td class="confluenceTd">specifies time interval after which the route is considered invalid</td></tr></tbody></table>

  

**Note:** The maximum metric of RIP route is 15. Metric higher than 15 is considered 'infinity' and routes with such metric are considered unreachable. Thus RIP cannot be used on networks with more than 15 hops between any two routers, and using redistribute metrics larger that 1 further reduces this maximum hop count.

  
  

## Interface

**Sub-menu:** `/routing rip interface-template`

  

<table class="wrapped confluenceTable" style="margin-left: 14.4318px;"><colgroup class=""><col class=""><col class=""></colgroup><tbody class=""><tr class=""><th class="confluenceTh">Property</th><th class="confluenceTh">Description</th></tr><tr class=""><td class="confluenceTd"><strong>name</strong><span>&nbsp;</span></td><td class="confluenceTd">name of the instance</td></tr><tr class=""><td class="confluenceTd"><strong>instance</strong></td><td class="confluenceTd">which <a href="https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328206" rel="nofollow">VRF</a> to use</td></tr><tr class=""><td class="confluenceTd"><span><strong>interfaces</strong>&nbsp;</span></td><td class="confluenceTd">specifies which afi to use.</td></tr><tr class=""><td class="confluenceTd"><strong>source-addresses&nbsp;</strong></td><td class="confluenceTd">input filter chain</td></tr><tr><td class="confluenceTd"><strong>cost</strong> (Default:<span> </span>)</td><td class="confluenceTd">output filter chain</td></tr><tr><td class="confluenceTd"><strong>split-horizon </strong>(<em>no</em><em>| yes</em> )</td><td class="confluenceTd"><br></td></tr><tr><td class="confluenceTd"><strong>poison-reverse </strong>(<em>no</em><em>| yes</em> )</td><td class="confluenceTd"><br></td></tr><tr><td class="confluenceTd"><strong>mode </strong>(<em>passive| strict</em>)</td><td class="confluenceTd"><br></td></tr><tr><td class="confluenceTd"><strong>key-chain </strong>(<em>name</em>)</td><td class="confluenceTd">name of key-chain</td></tr><tr><td class="confluenceTd"><strong>password&nbsp;</strong></td><td class="confluenceTd">password</td></tr></tbody></table>

  

  

**Sub-menu:** `/routing rip interface`

_Read-only properties:_

<table class="wrapped relative-table confluenceTable" style="margin-left: 14.4318px;width: 38.4213%;"><colgroup><col style="width: 58.9054%;"><col style="width: 41.0494%;"></colgroup><tbody><tr><th class="confluenceTh">Property</th><th class="confluenceTh">Description</th></tr><tr><td class="confluenceTd"><strong>instance </strong>(<em>name</em>)</td><td class="confluenceTd">name of the instance</td></tr><tr><td class="confluenceTd"><strong>address</strong><span>&nbsp;</span>(<em>address%interface </em>)</td><td class="confluenceTd">IP address and interface name</td></tr></tbody></table>

  

## Neighbor

**Sub-menu:** `/routing rip neighbor`

  

This submenu is used to define a neighboring routers to exchange routing information with. Normally there is no need to add the neighbors, if multicasting is working properly within the network. If there are problems with exchanging routing information, neighbor routers can be added to the list. It will force the router to exchange the routing information with the neighbor using regular unicast packets.

  

Read-only properties:

<table class="wrapped confluenceTable" style="margin-left: 14.4318px;"><colgroup class=""><col class=""><col class=""></colgroup><tbody class=""><tr class=""><th class="confluenceTh">Property</th><th class="confluenceTh">Description</th></tr><tr class=""><td class="confluenceTd"><strong>address</strong><span>&nbsp;</span>(<em>IP address</em>)</td><td class="confluenceTd">IP address of neighboring router</td></tr><tr><td class="confluenceTd"><strong>routes</strong></td><td class="confluenceTd">amount of routes</td></tr><tr><td class="confluenceTd"><strong>packets-total</strong></td><td class="confluenceTd">amount of all packets</td></tr><tr><td class="confluenceTd"><strong>packets-bad</strong></td><td class="confluenceTd">amount of bad packets</td></tr><tr><td class="confluenceTd"><strong>entries-bad</strong></td><td class="confluenceTd">amount of bad entries</td></tr><tr><td class="confluenceTd"><strong>last-update </strong>(<em>time</em>)</td><td class="confluenceTd">time from last update</td></tr></tbody></table>

  

**Sub-menu:** `/routing rip static-neighbor`

<table class="wrapped confluenceTable" style="margin-left: 14.4318px;"><colgroup class=""><col class=""><col class=""></colgroup><tbody class=""><tr class=""><th class="confluenceTh">Property</th><th class="confluenceTh">Description</th></tr><tr class=""><td class="confluenceTd"><strong>instance</strong> (name)</td><td class="confluenceTd">name of used instance</td></tr><tr class=""><td class="confluenceTd"><strong>address</strong><span>&nbsp;</span>(<em>IP address</em>)</td><td class="confluenceTd">IP address of neighboring router</td></tr></tbody></table>

## Keys

**Sub-menu:** `/routing rip keys`

  

MD5 authentication key chains.

  

| Property                                                                   | Description                                                                                                                                                |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **chain** (_string_; Default: **""**)                                      | chain name to place this key in.                                                                                                                           |
| **key** (_string_; Default: **""**)                                        | authentication key. Maximal length 16 characters                                                                                                           |
| **key-id** (_integer:0..255_; Default: )                                   | key identifier. This number is included in MD5 authenticated RIP messages, and determines witch key to use to check authentication for a specific message. |
| **valid-from** (_date and time_; Default: today's date and time: 00:00:00) | key is valid from this date and time                                                                                                                       |
| **valid-till** (_date and time_; Default: today's date and time: 00:00:00) | key is valid until this date and time                                                                                                                      |