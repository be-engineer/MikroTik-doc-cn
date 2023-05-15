## Properties

**Sub-menu:** `/interface traffic-eng`

  

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

|                                                                 |
| --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **affinity-exclude** (_integer_; Default: **not set**)          | Do not use interface if [resource-class](https://wiki.mikrotik.com/wiki/Manual:MPLS/Traffic-eng#Interface "Manual:MPLS/Traffic-eng") matches any of specified bits.                                                                                  |
| **affinity-include-all** (_integer_; Default: **not set**)      | Use interface only if [resource-class](https://wiki.mikrotik.com/wiki/Manual:MPLS/Traffic-eng#Interface "Manual:MPLS/Traffic-eng") matches all of specified bits.                                                                                    |
| **affinity-include-any** (_integer_; Default: **not set**)      | Use interface if [resource-class](https://wiki.mikrotik.com/wiki/Manual:MPLS/Traffic-eng#Interface "Manual:MPLS/Traffic-eng") matches any of specified bits.                                                                                         |
| **auto-bandwidth-avg-interval** (_time_; Default: **5m**)       | Interval in which actual amount of data is measured, from which average bandwidth is calculated.                                                                                                                                                     |
| **auto-bandwidth-range** (_Disabled                             | Min\[bps\]\[-Max\[bps\]\]_; Default: **0bps**)                                                                                                                                                                                                       | Auto bandwidth adjustment range. [`Read more >>`](https://wiki.mikrotik.com/wiki/Manual:TE_tunnel_auto_bandwidth "Manual:TE tunnel auto bandwidth")                                                                                                       |
| **auto-bandwidth-reserve** (_integer\[%\]_; Default: **0%**)    | Specifies percentage of additional bandwidth to reserve. [`Read more >>`](https://wiki.mikrotik.com/wiki/Manual:TE_tunnel_auto_bandwidth "Manual:TE tunnel auto bandwidth")                                                                          |
| **auto-bandwidth-update-interval** (_time_; Default: **1h**)    | Interval during which tunnel keeps track of highest average rate.                                                                                                                                                                                    |
| **bandwidth** (_integer\[bps\]_; Default: **0bps**)             | How much bandwidth to reserve for TE tunnel. Value is in bits per second. [`Read more >>`](https://wiki.mikrotik.com/wiki/Manual:TE_tunnel_auto_bandwidth#Bandwidth_limitation "Manual:TE tunnel auto bandwidth")                                    |
| **bandwidth-limit** (_disabled                                  | integer\[%\]_; Default: **disabled**)                                                                                                                                                                                                                | Defines actual bandwidth limitation of TE tunnel. Limit is configured in percent of specified tunnel `bandwidth`. [`Read more >>`](https://wiki.mikrotik.com/wiki/Manual:TE_tunnel_auto_bandwidth#Bandwidth_limitation "Manual:TE tunnel auto bandwidth") |
| **comment** (_string_; Default: )                               | Short description of the item                                                                                                                                                                                                                        |
| **disable-running-check** (_yes                                 | no_; Default: **no**)                                                                                                                                                                                                                                | Specifies whether to detect if interface is running or not. If set to **no** interface will always have `running` flag.                                                                                                                                   |
| **disabled** (_yes                                              | no_; Default: **yes**)                                                                                                                                                                                                                               | Defines whether item is ignored or used.                                                                                                                                                                                                                  |
| **from-address** (_auto                                         | IP_; Default: **auto**)                                                                                                                                                                                                                              | Ingress address of the tunnel. If set to **auto** least IP address is picked.                                                                                                                                                                             |
| **holding-priority** (_integer \[0..7\]_; Default: **not set**) | Is used to decide whether this session can be preempted by another session. 0 sets the highest priority.                                                                                                                                             |
| **mtu** (_integer_; Default: **1500**)                          | Layer3 Maximum Transmission Unit                                                                                                                                                                                                                     |
| **name** (_string_; Default: )                                  | Name of the interface                                                                                                                                                                                                                                |
| **primary-path** (_string_; Default: )                          | Primary label switching paths defined in `[/mpls traffic-eng tunnel-path](https://wiki.mikrotik.com/wiki/Manual:MPLS/Traffic-eng#Tunnel_Path "Manual:MPLS/Traffic-eng")` menu.                                                                       |
| **primary-retry-interval** (_time_; Default: **1m**)            | Interval after which tunnel will try to use primary path.                                                                                                                                                                                            |
| **record-route** (_yes                                          | no_; Default: **not set**)                                                                                                                                                                                                                           | If enabled, the sender node will receive information about the actual route that the LSP tunnel traverses. Record Route is analogous to a path vector, and hence can be used for loop detection.                                                          |
| **reoptimize-interval** (_time_; Default: **not set**)          | Interval after which tunnel will re-optimize current path. If current path is not the best path then after optimization best path will be used. [`Read more >>`](https://wiki.mikrotik.com/wiki/Manual:Interface/Traffic_Engineering#Reoptimization) |
| **secondary-paths** (_string\[,string\]_; Default: )            | List of label switching paths used by TE tunnel if primary path fails. Paths are defined in `[/mpls traffic-eng tunnel-path](https://wiki.mikrotik.com/wiki/Manual:MPLS/Traffic-eng#Tunnel_Path "Manual:MPLS/Traffic-eng")` menu.                    |
| **setup-priority** (_integer\[0..7\]_; Default: **not set**)    | Parameter is used to decide whether this session can preempt another session. 0 sets the highest priority.                                                                                                                                           |
| **to-address** (_IP_; Default: **0.0.0.0**)                     | Remote end of TE tunnel.                                                                                                                                                                                                                             |

## Monitoring

To verify TE tunnel's status **`monitor`** command can be used.

[?](https://help.mikrotik.com/docs/display/ROS/Traffic+Eng#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface traffic-eng </code><code class="ros functions">monitor </code><code class="ros plain">0</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">tunnel-id</code><code class="ros constants">: 12</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">primary-path-state</code><code class="ros constants">: on-hold</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">secondary-path-state</code><code class="ros constants">: established</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">secondary-path</code><code class="ros constants">: static</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">active-path</code><code class="ros constants">: static</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">active-lspid</code><code class="ros constants">: 3</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">active-label</code><code class="ros constants">: 66</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">explicit-route</code><code class="ros constants">: "S:192.168.55.10/32,L:192.168.55.13/32,L:192.168.55.17/32"</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">recorded-route</code><code class="ros constants">: "192.168.55.13[66],192.168.55.17[59],192.168.55.18[3]"</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">reserved-bandwidth</code><code class="ros constants">: 5.0Mbps</code></div></div></td></tr></tbody></table>

  

## Reoptimization

Path can be re-optimized manually by entering the command `/interface traffic-eng reoptimize [id]` (where \[id\] is an item number or interface name). It allows network administrators to reoptimize the LSPs that have been established based on changes in bandwidth, traffic, management policy, or other factors.

Let's say TE tunnel chose another path after a link failure on best path. You can verify optimization by looking at **`explicit-route`** or **`recorded-route`** values if [record-route](https://wiki.mikrotik.com/wiki/Manual:MPLS/Traffic-eng#Tunnel_Path "Manual:MPLS/Traffic-eng") parameter is enabled.

[?](https://help.mikrotik.com/docs/display/ROS/Traffic+Eng#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface traffic-eng </code><code class="ros functions">monitor </code><code class="ros plain">0</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">tunnel-id</code><code class="ros constants">: 12</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">primary-path-state</code><code class="ros constants">: established</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">primary-path</code><code class="ros constants">: dyn</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">secondary-path-state</code><code class="ros constants">: not-necessary</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">active-path</code><code class="ros constants">: dyn active-lspid: 1</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">active-label</code><code class="ros constants">: 67</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">explicit-route</code><code class="ros constants">: "S:192.168.55.10/32,S:192.168.55.13/32,S:192.168.55.14/32,</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">S</code><code class="ros constants">:192.168.55.17/32,S:192.168.55.18/32"</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">recorded-route</code><code class="ros constants">: "192.168.55.13[67],192.168.55.17[60],192.168.55.18[3]"</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">reserved-bandwidth</code><code class="ros constants">: 5.0Mbps</code></div></div></td></tr></tbody></table>

  

Whenever the link comes back, TE tunnel will use the same path even it is not the best path (unless [reoptimize-interval](https://wiki.mikrotik.com/wiki/Manual:MPLS/Traffic-eng#Tunnel_Path "Manual:MPLS/Traffic-eng") is configured). To fix it we can manually reoptimize the tunnel path.

[?](https://help.mikrotik.com/docs/display/ROS/Traffic+Eng#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface traffic-eng reoptimize 0</code></div></div></td></tr></tbody></table>

  

[?](https://help.mikrotik.com/docs/display/ROS/Traffic+Eng#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface traffic-eng </code><code class="ros functions">monitor </code><code class="ros plain">0</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">tunnel-id</code><code class="ros constants">: 12</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">primary-path-state</code><code class="ros constants">: established</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">primary-path</code><code class="ros constants">: dyn</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">secondary-path-state</code><code class="ros constants">: not-necessary</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">active-path</code><code class="ros constants">: dyn</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">active-lspid</code><code class="ros constants">: 2 active-label: 81</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">explicit-route</code><code class="ros constants">: "S:192.168.55.5/32,S:192.168.55.2/32,S:192.168.55.1/32"</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">recorded-route</code><code class="ros constants">: "192.168.55.2[81],192.168.55.1[3]"</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">reserved-bandwidth</code><code class="ros constants">: 5.0Mbps</code></div></div></td></tr></tbody></table>

  

Notice how explicit-route and recorded-route changed to a shorter path.