## Feature Status

N/A - Feature not yet available

OK - Initial tests successful

NOK - initial tests not successful

Highlight Colors:

-   Yellow - partially working
-   Green - Working
-   Red - Not working at the moment

| 
Feature



 | 

v7.1

 | 

v7.2

 | 

v7.3

 | 

v7.6

 | 

v7.7

 | 

v7.10

 |
| --- | --- | --- | --- | --- | --- | --- |
| 

Feature



 | 

v7.1

 | 

v7.2

 | 

v7.3

 | 

v7.6

 | 

v7.7

 | 

v7.10

 |
| --- | --- | --- | --- | --- | --- | --- |
| **_Winbox_** |  |  |  |  |  |  |
| BGP support |   
 |   
 |   
 |   
 |   
 |   
 |
| OSPF support |   
 |   
 |   
 |   
 |   
 |   
 |
| RIP support |   
 |   
 |   
 |   
 |   
 |   
 |
| Router ID support |   
 |   
 |   
 |   
 |   
 |   
 |
| Routing filter support |   
 |   
 |   
 |   
 |   
 |   
 |
|   
 |   
 |   
 |   
 |   
 |   
 |   
 |
| _**Generic**_ |  |  |  |  |  |  |
| /31 address support | N/A |   
 | Routed traffic does not work to odd address. |   
 |   
 |   
 |
| Convert route rules after upgrade from v6.x |   
 |   
 |   
 |   
 |   
 |   
 |
| Static IPv6 upgrade from ROS v6 |   
 |   
 |   
 |   
 |   
 |   
 |
| IPv4 Route Rules |   
 |   
 |   
 |   
 |   
 |   
 |
| IPv6 Route Rules |   
 |   
 |   
 |   
 |   
 |   
 |
| ECMP flags |   
 |   
 |   
 |   
 |   
 |   
 |
| dst@table |   
 |   
 |   
 |   
 |   
 |   
 |
| gateway@table |   
 |   
 |   
 |   
 |   
 |   
 |
| gateway%interface |   
 |   
 |   
 |   
 |   
 |   
 |
| recursive route over ipv6 LL address |   
 |   
 |   
 |   
 |   
 |   
 |
| 3 level recursive gateway with ECMP  |   
 |   
 |   
 |   
 |   
 |   
 |
| IPV6 ECMP |   
 |   
 |   
 |   
 |   
 |   
 |
| IPv6 connected ECMP |   
 |   
 |   
 |   
 |   
 |   
 |
| Addresses from same subnet to multiple interfaces | N/A |   
 |   
 |   
 |   
 |   
 |
| Show time when route was last updated | N/A |   
 |   
 |   
 |   
 |   
 |
| Check Gateway | BFD not ready |   
 |   
 |   
 |   
 |   
 |
| Scope and target scope |   
 |   
 |   
 |   
 |   
 |   
 |
| IPv4 Mangle routing-mark |   
 |   
 |   
 |   
 |   
 |   
 |
| IPv6 Mangle routing-mark |   
 |   
 |   
 |   
 |   
 |   
 |
| Packet SRC address | Does not work correctly with /32 addresses |   
 |   
 |   
 |   
 |   
 |
| Routing-table parameter for ping and telnet |   
 |   
 |   
 |   
 |   
 |   
 |
| Show if route is hardware accelerated | Shows if route is candidate for HW acceleration |   
 |   
 |   
 |   
 |   
 |
| Custom route selection policy  |   
 |   
 |   
 |   
 |   
 |   
 |
| IPv4 with IPv6 nexthops for RFC5549 |   
 |   
 |   
 |   
 |   
 |   
 |
|   
 |   
 |   
 |   
 |   
 |   
 |   
 |
| Routing id |   
 |   
 |   
 |   
 |   
 |   
 |
| VRF |   
 |   
 |   
 |   
 |   
 |   
 |
| Management services support for VRFs  | telnet, ssh, api, www services can be set to listen on specific VRF |   
 |   
 |   
 |   
 |   
 |
| Some kind of mechanism to import/export routes from one vrf to another within same router | N/A |   
 |   
 |   
 |   
 |   
 |
| BFD | N/A |   
 |   
 |   
 |   
 |   
 |
|   
 |   
 |   
 |   
 |   
 |   
 |   
 |
| _**OSPF**_ |  |  |  |  |  |  |
| Convert OSPF config from v6 to v7 after upgrade | 

Known conversion problems:

-   NBMA neighbors place in backbone
-   ospf-v2 networks + interface may have issues
    
-   dynamic interfaces may have issues
    
-   MPLS PE CE features are not converted
    

 | 

  


 | 

  


 | 

  


 | 

  


 | 

  


 |
| OSPF neighbors in NSSA Area |   
 |   
 |   
 |   
 |   
 |   
 |
| OSPF in broadcast network |   
 |   
 |   
 |   
 |   
 |   
 |
| OSPF with routing filters |   
 |   
 |   
 |   
 |   
 |   
 |
| OSPF Virtual Link |   
 |   
 |   
 |   
 |   
 |   
 |
| OPSF input filtering |   
 |   
 |   
 |   
 |   
 |   
 |
| HMAC-SHA auth RFC5709 | N/A |   
 |   
 | Initial support |   
 |   
 |
| BGP and OSPF SNMP monitoring | N/A |   
 |   
 |   
 |   
 |   
 |
|   
 |   
 |   
 |   
 |   
 |   
 |   
 |
| _**BGP**_ |  |  |  |  |  |  |
| Convert BGP config from v6 to v7 after upgrade |   
 |   
 |   
 |   
 |   
 |   
 |
| BGP Templates and dynamic peers |   
 |   
 |   
 |   
 |   
 |   
 |
| BGP connect listen on a network |   
 |   
 |   
 |   
 |   
 |   
 |
| BGP guess remote.as |   
 |   
 |   
 |   
 |   
 |   
 |
| Show from which peer route received | OK ( /routing/route/print detail --> belongs-to) |   
 |   
 |   
 |   
 |   
 |
| BGP Address Families |   
 |   
 |   
 |   
 |   
 |   
 |
| BGP input.accept-\* |   
 |   
 |   
 |   
 |   
 |   
 |
| eBGP nexthop self |   
 |   
 |   
 |   
 |   
 |   
 |
| Input Filter |   
 |   
 |   
 |   
 |   
 |   
 |
| Output Filter |   
 |   
 |   
 |   
 |   
 |   
 |
| BGP Local address auto selection |   
 |   
 |   
 |   
 |   
 |   
 |
| BGP route reflect |   
 |   
 |   
 |   
 |   
 |   
 |
| BGP route server |   
 |   
 |   
 |   
 |   
 |   
 |
| BGP Roles  
[https://datatracker.ietf.org/doc/draft-ietf-idr-bgp-open-policy/?include\_text=1](https://datatracker.ietf.org/doc/draft-ietf-idr-bgp-open-policy/?include_text=1) | rfc roles not fully implemented |   
 |   
 |   
 |   
 |   
 |
| BGP session uptime in "established" state |   
 |   
 |   
 |   
 |   
 |   
 |
| BGP session last established time |   
 |   
 |   
 |   
 |   
 |   
 |
|   
 |   
 |   
 |   
 |   
 |   
 |   
 |
| BGP Flow Spec | Flow spec attributes are forwarded |   
 |   
 |   
 |   
 |   
 |
| BGP Selection |   
 |   
 |   
 |   
 |   
 |   
 |
|   
 |   
 |   
 |   
 |   
 |   
 |   
 |
| BGP Selection (Multipath) | N/A |   
 |   
 |   
 |   
 |   
 |
| BGP Confederation |   
 |   
 |   
 |   
 |   
 |   
 |
| BGP Aggregation | N/A |   
 |   
 |   
 |   
 |   
 |
| BGP ORF | N/A |   
 |   
 |   
 |   
 |   
 |
| Discard prefix RTBH  RFC 6666 | N/A |   
 |   
 |   
 |   
 |   
 |
| AS-wide Unique BGP Identifier RFC 6286 | N/A |   
 |   
 |   
 |   
 |   
 |
| Exported PDU PCAP saver |   
 |   
 |   
 |   
 |   
 |   
 |
| Exported PDU PCAP loader |   
 |   
 |   
 |   
 |   
 |   
 |
| BGP Advertisement monitoring |   
 | Initial implementation by dumping to pcap |   
 | Advertisements rework |   
 |   
 |
| BGP Prefix limit |   
 |   
 | Initial support |   
 |   
 |   
 |
| BGP advertise IPv4 prefix with IPv6 nexthop (RFC5549) |   
 |   
 |   
 |   
 |   
 |   
 |
| BGP VPNv6 support |   
 |   
 |   
 |   
 |   
 | Prerequisites are made, need to add actual BGP Afi |
|   
 |   
 |   
 |   
 |   
 |   
 |   
 |
| _**MPLS**_ |  |  |  |  |  |  |
| Static label mapping |   
 |   
 |   
 |   
 |   
 |   
 |
| Static mapping upgrade from v6 |   
 |   
 |   
 |   
 |   
 |   
 |
| LDP IPv4 mapping |   
 |   
 |   
 |   
 |   
 |   
 |
| LDP IPv6 mapping |   
 |   
 |   
 |   
 |   
 |   
 |
| LDP signaled VPLS |   
 |   
 |   
 |   
 |   
 |   
 |
| LDP config upgrade from v6 |   
 |   
 |   
 |   
 |   
 |   
 |
| LDP Dual Stack |   
 |   
 |   
 |   
 |   
 |   
 |
| TE |   
 |   
 |   
 |   
 |   
 |   
 |
| TE Config upgrade from v6 |   
 |   
 |   
 |   
 |   
 |   
 |
| VPLS Encap to TE |   
 |   
 |   
 |   
 |   
 |   
 |
| BGP signaled VPLS |   
 |   
 |   
 |   
 |   
 |   
 |
| VPLS config upgrade from v6 |   
 |   
 |   
 |   
 |   
 |   
 |
| Fast reroute |   
 |   
 |   
 |   
 |   
 |   
 |
| MPLS ECMP |   
 |   
 |   
 |   
 |   
 |   
 |
| One label per VRF |   
 |   
 |   
 |   
 |   
 |   
 |
| Ability to use MPLS EXP-bit in Queues | N/A |   
 |   
 |   
 |   
 |   
 |
| MPLS Fast-Path | N/A |   
 |   
 |   
 |   
 |   
 |
|   
 |   
 |   
 |   
 |   
 |   
 |   
 |
| RPKI session |   
 |   
 |   
 |   
 |   
 |   
 |
| RPKI possibility to view received info of specific prefix |   
 |   
 |   
 |   
 |   
 |   
 |
| RPKI show connection status |   
 |   
 |   
 |   
 |   
 |   
 |
|   
 |   
 |   
 |   
 |   
 |   
 |   
 |
| _**Filters**_ |  |  |  |  |  |  |
| Convert routing filters after upgrade from v6.x |   
 |   
 |   
 |   
 |   
 |   
 |
| Syntax completion |   
 |   
 |   
 |   
 |   
 |   
 |
| Routing filter chain drop by default without rules |   
 |   
 |   
 |   
 |   
 |   
 |
| Routing filter prefix match |   
 |   
 |   
 |   
 |   
 |   
 |
| Routing filter protocol match |   
 |   
 |   
 |   
 |   
 |   
 |
| Routing filter append communities |   
 |   
 |   
 |   
 |   
 |   
 |
| Routing filter append large community |   
 |   
 |   
 |   
 |   
 |   
 |
| Routing filter set weight |   
 |   
 |   
 |   
 |   
 |   
 |
| Routing filter set local pref |   
 |   
 |   
 |   
 |   
 |   
 |
| Routing filter set MED |   
 |   
 |   
 |   
 |   
 |   
 |
| Routing filter set origin |   
 |   
 |   
 |   
 |   
 |   
 |
| Routing filter set igp metric from OSPF cost |   
 |   
 |   
 |   
 |   
 |   
 |
| Routing filter match prefix with address list |   
 |   
 |   
 |   
 |   
 |   
 |
| Routing filter match community/large community lists |   
 |   
 |   
 |   
 |   
 |   
 |
| Routing filter add a prefix to address list | N/A |   
 |   
 |   
 |   
 |   
 |
| Routing filter validate prefix with RPKI |   
 |   
 |   
 |   
 |   
 |   
 |
|   
 |   
 |   
 |   
 |   
 |   
 |   
 |
| _**Multicast**_ |  |  |  |  |  |  |
| IGMP-Proxy |   
 |   
 |   
 |   
 |   
 |   
 |
| PIM-SM | Initial support |   
 |   
 |   
 |   
 |   
 |

## Performance Status

  
Used hardware:

-   CCR1036, 16GB RAM (tile)
-   CCR2004(arm64)
-   CCR1100AHx4(arm)
-   Intel(R) Core(TM) i7-4790 CPU @ 3.60GHz 32GB RAM (as a host for CHRs)

  
The simulated upstream peer is a CHR router running ROSv6 with a copy of the global IPv4 routing table (585K routes loaded from MRT dump).

### One Peer Receive Only

![](https://help.mikrotik.com/docs/download/attachments/28606515/BGP_T1.png?version=1&modificationDate=1599129381563&api=v2)

DUT establishes a connection to simulated upstream peers, receives routes, and installs them in FIB.

| 
  


 | 

v6.44

 | 

v7.1beta3

 | 

v7.1rc7

 |
| --- | --- | --- | --- |
| 

  


 | 

v6.44

 | 

v7.1beta3

 | 

v7.1rc7

 |
| --- | --- | --- | --- |
| CCR | 0:40 - 2:12 | 0:46 |   
 |
| RB1100x4 1.4GHz | 0:32-0:38 | 0:23 |   
 |
| CCR2004 | 0:32 | 0:18 |   
 |
| x86 (CHR) | 0:20 |   
 |   
 |
| RB450G (in/out affinity=alone) | after trying for 9min - ran out of memory at 558K routes | 2:02 (121MB free) |   
 |
| RB450G (in/out affinity=main) | \- | 1:54 |   
 |
| RB450G (affinity in=alone out=input) | \- | 2:12 |   
 |

  

### Two Peers Receive Only

![](https://help.mikrotik.com/docs/download/attachments/28606515/BGP_T2.png?version=1&modificationDate=1599129407331&api=v2)

DUT establishes a connection to two simulated upstream peers, receives routes, picks the best route, and installs in FIB. On ROSv7 affinity settings are set to "alone".

| 
  


 | 

v6.44

 | 

FRR

 | 

v7.1beta3

 | 

v7.1rc7 (846k routes per peer)

 |
| --- | --- | --- | --- | --- |
| 

  


 | 

v6.44

 | 

FRR

 | 

v7.1beta3

 | 

v7.1rc7 (846k routes per peer)

 |
| --- | --- | --- | --- | --- |
| CCR | 1:01 - 2:45 |   
 | 1:11 |   
 |
| RB1100x4 1.4GHz | 0:51 |   
 | 0:30 |   
 |
| CCR2004 | 0:51 |   
 | 0:29 | 0:33 |
| router x |   
 |   
 |   
 | 0:40 |
| x86 (CHR) | 0:25 |   
 |   
 |   
 |
| x86 (virtual) |   
 | 0:26(4cores) |   
 |   
 |
|   
 |   
 | 0:46(2cores) |   
 |   
 |
|   
 |   
 | 0:30(2cores no LDP) |   
 |   
 |

  

### Multi-homing Sim

Two DUT devices establish eBGP sessions to simulated x86 upstream routers. Both DUTs are interconnected with the iBGP session. Each DUT receives routes from upstream and readvertises routes over iBGP. On ROSv7 affinity, settings are set to "alone" and early-cut disabled.

![](https://help.mikrotik.com/docs/download/attachments/28606515/BGP_MH.png?version=1&modificationDate=1599128813808&api=v2)

-   Route Provider: CHR (ROSv6)
-   DUT\_1: CCR1032
-   DUT\_2: CCR1032

<table class="wrapped confluenceTable"><colgroup><col><col></colgroup><tbody><tr><td class="confluenceTd">v7.1beta3</td><td class="confluenceTd">1:11</td></tr><tr><td class="confluenceTd">v7.1beta2</td><td class="confluenceTd">1:29</td></tr><tr><td class="confluenceTd">v6.xx</td><td class="confluenceTd">1:02 - 8:30</td></tr></tbody></table>

  

```

```

-   Route Provider: CHR (ROSv6)
-   DUT\_1: CCR2004
-   DUT\_2: RB1100AHx2

<table class="wrapped confluenceTable"><colgroup><col><col></colgroup><tbody><tr><td class="confluenceTd">v7.1beta3</td><td class="confluenceTd">0:36</td></tr><tr><td class="confluenceTd">v6.xx</td><td class="confluenceTd">0:59</td></tr></tbody></table>

### Memory Usage:

[?](https://help.mikrotik.com/docs/display/ROS/Routing+Protocol+Overview#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">Columns: TASKS, PRIVATE-MEM-BLOCKS, SHARED-MEM-BLOCKS, PSS, RSS, VMS, RETIRED, ID, PID, RPID, PROCESS-TIME, KERNEL-TIME, CUR-BUSY, MAX-BU&gt;</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;</code><code class="text plain">#&nbsp; TASKS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PRIVATE-M&nbsp; SHARED-M&nbsp; P&nbsp; R&nbsp; V&nbsp; RE&nbsp; ID&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PID&nbsp; R&nbsp; PROCESS-&nbsp; KERNEL-&nbsp; CUR&nbsp; MAX-BUS&nbsp; CUR&nbsp; MAX-CALC</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;</code><code class="text plain">0&nbsp; routing tables&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 12.0MiB&nbsp;&nbsp;&nbsp; 30.2MiB&nbsp;&nbsp; 0&nbsp; 0&nbsp; 0&nbsp; 12&nbsp; main&nbsp;&nbsp;&nbsp;&nbsp; 111&nbsp; 0&nbsp; 8s980ms&nbsp;&nbsp; 2s60ms&nbsp;&nbsp; 0ms&nbsp; 1s320ms&nbsp; 0ms&nbsp; 10s700ms</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">rib&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">connected networks&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;</code><code class="text plain">1&nbsp; fib&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2816.0KiB&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp; 0&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; fib&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 130&nbsp; 1&nbsp; 3s&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 4s660ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 7s220ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 7s220ms</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;</code><code class="text plain">2&nbsp; ospf&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 512.0KiB&nbsp;&nbsp; 256.0KiB&nbsp; 0&nbsp; 0&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ospf&nbsp;&nbsp;&nbsp;&nbsp; 137&nbsp; 1&nbsp; 1s220ms&nbsp;&nbsp; 130ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 980ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1s40ms&nbsp;</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">connected networks&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;</code><code class="text plain">3&nbsp; fantasy&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 256.0KiB&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp; 0&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; fantasy&nbsp; 138&nbsp; 1&nbsp; 60ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 80ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 40ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 40ms&nbsp;&nbsp;&nbsp;</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;</code><code class="text plain">4&nbsp; configuration and reporting&nbsp;&nbsp; 3840.0KiB&nbsp; 512.0KiB&nbsp; 0&nbsp; 0&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; static&nbsp;&nbsp; 139&nbsp; 1&nbsp; 1s270ms&nbsp;&nbsp; 110ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 260ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 260ms&nbsp;&nbsp;</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;</code><code class="text plain">5&nbsp; rip&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 512.0KiB&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp; 0&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; rip&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 136&nbsp; 1&nbsp; 120ms&nbsp;&nbsp;&nbsp;&nbsp; 70ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 60ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 120ms&nbsp;&nbsp;</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">connected networks&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;</code><code class="text plain">6&nbsp; routing policy configuration&nbsp; 768.0KiB&nbsp;&nbsp; 768.0KiB&nbsp; 0&nbsp; 0&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; policy&nbsp;&nbsp; 133&nbsp; 1&nbsp; 2s290ms&nbsp;&nbsp; 3s170ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 80ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 80ms&nbsp;&nbsp;&nbsp;</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;</code><code class="text plain">7&nbsp; BGP service&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 768.0KiB&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp; 0&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bgp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 134&nbsp; 1&nbsp; 2s760ms&nbsp;&nbsp; 5s480ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 20ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 60ms&nbsp;&nbsp;&nbsp;</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">connected networks&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;</code><code class="text plain">8&nbsp; BFD service&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 512.0KiB&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp; 0&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 12&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 135&nbsp; 1&nbsp; 100ms&nbsp;&nbsp;&nbsp;&nbsp; 90ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 40ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 120ms&nbsp;&nbsp;</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">connected networks&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;</code><code class="text plain">9&nbsp; BGP Input 10.155.101.186&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3072.0KiB&nbsp; 6.2MiB&nbsp;&nbsp;&nbsp; 0&nbsp; 0&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 20&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 183&nbsp; 1&nbsp; 1s350ms&nbsp;&nbsp; 1s190ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 20ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 20ms&nbsp;&nbsp;&nbsp;</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;</code><code class="text plain">10&nbsp; BGP Output 10.155.101.186&nbsp;&nbsp;&nbsp;&nbsp; 5.5MiB&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp; 0&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 21&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 184&nbsp; 1&nbsp; 5s400ms&nbsp;&nbsp; 500ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3s880ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3s880ms</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;</code><code class="text plain">11&nbsp; BGP Input 10.155.101.232&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3072.0KiB&nbsp; 6.2MiB&nbsp;&nbsp;&nbsp; 0&nbsp; 0&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 22&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 187&nbsp; 1&nbsp; 970ms&nbsp;&nbsp;&nbsp;&nbsp; 740ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 20ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 20ms&nbsp;&nbsp;&nbsp;</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;</code><code class="text plain">12&nbsp; BGP Output 10.155.101.232&nbsp;&nbsp;&nbsp;&nbsp; 8.2MiB&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp; 0&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 23&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 188&nbsp; 1&nbsp; 10s830ms&nbsp; 960ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 7s&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 7s&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;</code><code class="text plain">13&nbsp; Global memory&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 256.0KiB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; global&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp; 0</code></div></div></td></tr></tbody></table>