Routing stats.

  

# /routing/stats/origin

  

# /routing/stats/process

This menu allows to monitor debugging information of all the routing processes.

[?](https://help.mikrotik.com/docs/display/ROS/Routing+Debugging+Tools#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@rack1_b35_CCR1036] /routing/stats/process&gt; print interval=1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Columns: TASKS, PRIVATE-MEM-BLOCKS, SHARED-MEM-BLOCKS, PSS, RSS, VMS, RETIRED, ID, PID, RPID, PROCESS-TIME, KERNEL-TIME, CUR-BUSY, MAX-BUSY, CUR-CALC, MAX-CALC</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain"># TASKS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PRIVATE-&nbsp; SHARED-ME&nbsp; PSS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; RSS&nbsp;&nbsp;&nbsp;&nbsp; VMS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; RETIRED&nbsp; ID&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PID&nbsp; RPID&nbsp; PROCESS&nbsp; KERNEL-TIME&nbsp; CUR-BUSY&nbsp; MAX-BUSY&nbsp; CUR-CALC&nbsp; MAX-CALC</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">0 routing tables&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 768.0KiB&nbsp; 1792.0KiB&nbsp; 2399.0KiB&nbsp; 6.4MiB&nbsp; 22.1MiB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 34&nbsp; main&nbsp;&nbsp;&nbsp;&nbsp; 317&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp; 2s260ms&nbsp; 1s940ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 170ms&nbsp;&nbsp;&nbsp;&nbsp; 20ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1s210ms</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;</code><code class="text plain">rib&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">1 fib&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2263.0KiB&nbsp; 6.2MiB&nbsp; 22.3MiB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; fib&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 351&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 250ms&nbsp;&nbsp;&nbsp; 1s720ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1s210ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1s210ms</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">2 ospf&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 256.0KiB&nbsp; 256.0KiB&nbsp;&nbsp; 2559.0KiB&nbsp; 6.6MiB&nbsp; 22.3MiB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ospf&nbsp;&nbsp;&nbsp;&nbsp; 384&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 4s710ms&nbsp; 5s210ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 20ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 20ms&nbsp;&nbsp;&nbsp;</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">3 pimsm&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 256.0KiB&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2252.0KiB&nbsp; 5.8MiB&nbsp; 22.3MiB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; pim&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 386&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 200ms&nbsp;&nbsp;&nbsp; 450ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">4 fantasy&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2031.0KiB&nbsp; 5.1MiB&nbsp; 22.3MiB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; fantasy&nbsp; 388&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 270ms&nbsp;&nbsp;&nbsp; 390ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">5 configuration and reporting&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 512.0KiB&nbsp;&nbsp; 2351.0KiB&nbsp; 6.4MiB&nbsp; 22.3MiB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; static&nbsp;&nbsp; 389&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 310ms&nbsp;&nbsp;&nbsp; 430ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">6 ldp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 256.0KiB&nbsp; 256.0KiB&nbsp;&nbsp; 2455.0KiB&nbsp; 6.4MiB&nbsp; 22.3MiB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; mpls&nbsp;&nbsp;&nbsp;&nbsp; 387&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 340ms&nbsp;&nbsp;&nbsp; 350ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 40ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 40ms&nbsp;&nbsp;&nbsp;</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;</code><code class="text plain">Copy&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">7 rip&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 256.0KiB&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2230.0KiB&nbsp; 5.7MiB&nbsp; 22.3MiB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; rip&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 377&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 230ms&nbsp;&nbsp;&nbsp; 380ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">8 routing policy configuration&nbsp; 512.0KiB&nbsp; 512.0KiB&nbsp;&nbsp; 2355.0KiB&nbsp; 5.6MiB&nbsp; 22.3MiB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; policy&nbsp;&nbsp; 358&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 240ms&nbsp;&nbsp;&nbsp; 390ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">9 BGP service&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 512.0KiB&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2592.0KiB&nbsp; 6.3MiB&nbsp; 22.3MiB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bgp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 364&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 360ms&nbsp;&nbsp;&nbsp; 600ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="text plain">10 BFD service&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 256.0KiB&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2206.0KiB&nbsp; 5.7MiB&nbsp; 22.3MiB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 12&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 371&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 230ms&nbsp;&nbsp;&nbsp; 370ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="text plain">11 BGP Input 111.11.0.1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 512.0KiB&nbsp; 512.0KiB&nbsp;&nbsp; 2560.0KiB&nbsp; 6.4MiB&nbsp; 22.3MiB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 22&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 679&nbsp;&nbsp;&nbsp;&nbsp; 1&nbsp; 140ms&nbsp;&nbsp;&nbsp; 350ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp;</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;</code><code class="text plain">BGP Output 111.11.0.1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="text plain">12 Global memory&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 256.0KiB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; global&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div></div></td></tr></tbody></table>

   

# /routing/stats/step

# /routing/fantasy

Fantasy menu is a fancy way to generate large amount of routes for testing purposes. Main benefits of this approach compared to script is the generation speed and simplicity. It is easy to remove all fantasy generated routes just by disabling fantasy rule.

Fantasy uses random generator from hashed route sequence number, seed and other parameters. 

### **Configuration Options**

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
| **comment** (_string_) |   
 |
| **count** (_integer:\[0..4294967295\]_) | How many routes to generate. |
| **dealer-id** (_start-\[end\]:: integer:\[0..4294967295\]_) |   
 |
| **disabled** (_yes | no_) | ID reference is not used. |
| **dst-address**(_Prefix_) | Prefix from which route will be generated.  |
| **gateway** (string) |   
 |
| **instance-id** (_start-\[end\]:: integer:\[0..4294967295\]_) |   
 |
| **name** (_string_) | Reference name |
| **offset** (_integer:\[0..4294967295\]_) | Route sequence number offset |
| **prefix-length** (start-\[end\]:: _integer:\[0..4294967295\]_ ) | Prefix length for generated route (can be specified as integer range). For example dst-address 192.168.0.0/16 and prefix-length 24 will generate /24 routes from 192.168.0.0/16 subnet. |
| **priv-offset** (_start-\[end\]:: integer: \[0..4294967295\]_) |   
 |
| **priv-size** (_start-\[end\]:: integer: \[0..100000\]_) |   
 |
| **scope** (_start-\[end\]::_ _integer: \[0..255\]_) | Scope to be set, can be set as range |
| **seed** (_string_) | Random generator seed |
| **target-scope** (_start-\[end\]::_ _integer: \[0..255\]_) | Target scope to be set, can be set as range |
| **use-hold** (_yes | no_) |   
 |

 A read-only table that lists routes from all the address families as well as all filtered routes with all possible route attributes.

  

Default example output of the table with various route types:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=59965493#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@MikroTik] /routing/route&gt; print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: A - ACTIVE; c, s, a, l, y - COPY; H - HW-OFFLOADED</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Columns: DST-ADDRESS, GATEWAY, AFI, DISTANCE, SCOPE, TARGET-SCOPE, IMMEDIATE-GW</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">DST-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GATEWAY&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; AFI&nbsp;&nbsp; D&nbsp; SCOPE&nbsp; TA&nbsp; IMMEDIATE-GW&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">lH 10.0.0.0/8&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ip4&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text plain">;;; defconf</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain">As&nbsp; 10.0.0.0/8&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10.155.130.1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ip4&nbsp;&nbsp; 1&nbsp;&nbsp;&nbsp;&nbsp; 30&nbsp; 10&nbsp; 10.155.130.1%ether1</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">lH 10.155.130.0/25&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ip4&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text plain">Ac&nbsp; 10.155.130.0/25&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ip4&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">aH 10.155.130.12/32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ip4&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">lH 111.13.0.0/24&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ip4&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="text plain">Ac&nbsp; 111.13.0.0/24&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ip4&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">aH 111.13.0.1/32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ip4&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="text plain">Ac&nbsp; 111.111.111.2/32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; loopback@vrfTest&nbsp; ip4&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; loopback&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="text plain">Ac&nbsp; 2111:4::/64&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ip6&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="text plain">Ac&nbsp; fe80::%ether1/64&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ip6&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="text plain">Ac&nbsp; fe80::%ether2/64&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ip6&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="text plain">Ac&nbsp; fe80::%ether3/64&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ip6&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="text plain">Ac&nbsp; fe80::%ether4/64&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ip6&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="text plain">Ac&nbsp; 3333::2/128&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; loopback@vrfTest&nbsp; ip6&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; loopback&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="text plain">Ac&nbsp; fe80::%loopback/64&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; loopback@vrfTest&nbsp; ip6&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; loopback&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="text plain">Ay&nbsp; 111.111.111.2/32&amp;65530:100&nbsp; loopback@vrfTest&nbsp; vpn4&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp; 5&nbsp; loopback&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="text plain">Ay&nbsp; 3333::2/128&amp;65530:100&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; loopback@vrfTest&nbsp; vpn6&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; 10&nbsp;&nbsp; 5&nbsp; loopback&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number24 index23 alt1" data-bidi-marker="true"><code class="text plain">A H ether1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; link&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number25 index24 alt2" data-bidi-marker="true"><code class="text plain">A H ether2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; link&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number26 index25 alt1" data-bidi-marker="true"><code class="text plain">A H ether3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; link&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number27 index26 alt2" data-bidi-marker="true"><code class="text plain">A H ether4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; link&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number28 index27 alt1" data-bidi-marker="true"><code class="text plain">A H loopback&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; link&nbsp; 0</code></div></div></td></tr></tbody></table>

  

Detailed example output with some BGP, OSPF, and other routes:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=59965493#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@MikroTik] /routing/route&gt; print detail</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: X - disabled, F - filtered, U - unreachable, A - active;</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">c - connect, s - static, r - rip, b - bgp, o - ospf, d - dhcp, v - vpn, m - modem, a - ldp-address, l - ldp-mapping, y - copy; H - hw-offloaded;</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">+ - ecmp, B - blackhole</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;</code><code class="text plain">o&nbsp;&nbsp; afi=ip4 contribution=best-candidate dst-address=0.0.0.0/0 routing-table=main gateway=10.155.101.1%ether1 immediate-gw=10.155.101.1%ether1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">distance=110 scope=20 target-scope=10 belongs-to="OSPF route"</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">ospf.metric=2 .tag=111 .type=ext-type-1</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">debug.fwp-ptr=0x203425A0</code></div><div class="line number9 index8 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">Ad + afi=ip4 contribution=active dst-address=0.0.0.0/0 routing-table=main pref-src="" gateway=10.155.101.1 immediate-gw=10.155.101.1%ether1</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">distance=1 scope=30 target-scope=10 vrf-interface=ether1 belongs-to="DHCP route"</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">debug.fwp-ptr=0x20342060</code></div><div class="line number13 index12 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">As + afi=ip4 contribution=active dst-address=0.0.0.0/0 routing-table=main pref-src="" gateway=10.155.101.1 immediate-gw=10.155.101.1%ether1</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">distance=1 scope=30 target-scope=10 belongs-to="Static route"</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">debug.fwp-ptr=0x20342060</code></div><div class="line number17 index16 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">Fb&nbsp;&nbsp; afi=ip4 contribution=filtered dst-address=1.0.0.0/24 routing-table=main gateway=10.155.101.1 immediate-gw=10.155.101.1%ether1 distance=20</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">scope=40 target-scope=10 belongs-to="BGP IP routes from 10.155.101.217" rpki=valid</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">bgp.peer-cache-id=*B000002 .aggregator="13335:172.68.180.1" .as-path="65530,100,9002,13335" .atomic-aggregate=yes .origin=igp</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">debug.fwp-ptr=0x20342960</code></div></div></td></tr></tbody></table>

  

  

| Property | Description |
| --- | --- |
| Property | Description |
| --- | --- |
| **active** (_yes | no_) | A flag indicates whether the route is elected as Active and eligible to be added to the FIB. |
| **afi** (_ip4 | ip6 | link_) | Address family this route belongs to. |
| **belongs-to** (_string_) | Descriptive info showing from where the route was received. |
| **bgp** (_yes | no_) | A flag indicates whether this route was added by the [BGP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328220) protocol. |
| **bgp -** a group of parameters associated with the [BGP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328220) protocol |
|  | **.as-path**(_string_) | value of the AS\_PATH [BGP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328220) attribute |
|  | **.aggregator** (_string)_ |   
 |
|  | **.atomic-aggregate** (_yes | no_) |   
 |
|  | **.cluster-list** (_string_) |   
 |
|  | **.communities** (_string_) | value of the COMMUNITIES BGP attribute |
|  | **.ext-communities** (_string_) | value of the EXTENDED\_COMMUNITIES BGP attribute |
|  | **.igp-metric**(_string_) | value of the IGP\_METRIC BGP attribute |
|  | **.large-communities** (_string_) | value of the LARGE\_COMMUNITIES BGP attribute |
|  | **.local-pref** (_string_) | value of the LOCAL\_PREF BGP attribute |
|  | **.med** (_string_) | value of the MED BGP attribute |
|  | **.nexthop** (_string_) |   
 |
|  | **.origin** (_string_) |   
 |
|  | **.originator-id** (_string_) |   
 |
|  | **.out-nexthop**(_string_) |   
 |
|  | **.peer-cache-id** (_string_) | The ID of the [BGP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328220) session that installed the route. See `/routing/bgp/session` menu. |
|  | **.unknown** (_string_) | hex blob of unknown [BGP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328220) attributes |
|  | **.weight** (_string_) |   
 |
| **blackhole** (_yes | no_) | A flag indicates whether it is a blackhole route |
| **check-gateway** (_ping | arp | bfd_) | Currently used check-gateway option. |
| **comment** (_string_) |   
 |
| **connect** (_yes | no_) | A flag indicates whether it is a connected network route. |
| **contribution** (_string_) | Shows the route status contributing to the election process, e.g "filtered, active, candidate" |
| **copy** (_yes | no_) | A flag indicates a copy of the route to be redistributed as the L3VPN route. VPNv4/6 related attributes are attached to this "copy" route. |
| **create-time** (_string_) |   
 |
| **debug -** a group of debugging parameters |
|   
 |   
 |   
 |
| **dhcp** (_yes | no_) | A flag indicates whether the route was added by the DHCP service. |
| **disabled** (_yes | no_) | A flag indicates whether the route is disabled. |
| **distance** (_integer_) |   
 |
| **dst-address** (_prefix_) | Route destination. |
| **ecmp** (_yes | no_) | A flag indicates whether the route is added as an Equal-Cost Multi-Path route in the FIB. [Read more>>](https://help.mikrotik.com/docs/display/ROS/How+Packets+Are+Routed#HowPacketsAreRouted-Multipath(ECMP)routes) |
| **filtered** (_yes | no_) | A flag indicates whether the route was filtered by routing filters and excluded from being used as the best route. |
| **gateway** (_string_) | Configured gateway, for the actually resolved gateway, see `immediate-gw` parameter. |
| **hw-offloaded** (_yes | no_) | Indicates whether the route is eligible to be hardware offloaded on supported hardware. |
| **immediate-gw** (_string_) | Shows actual (resolved) gateway and interface that will be used for packet forwarding. Displayed in format `[ip%interface]`. |
| **label** (_integer_) |   
 |
| **ldp-address** (_yes | no_) | A flag indicates whether the route entry is an LDP address. |
| **ldp-mapping** (_yes | no_) | A flag indicates whether the route entry is the LDP mapping |
| **ldp** - a group of parameters associated with the LDP protocol |
|   
 | **.label** (_integer_) | LDP mapped MPLS label. |
|   
 | **.peer-id** () |   
 |
| **local-address** (_IP_) | Local IP address of the connected network. |
| **modem** (_yes | no_) | A flag indicates whether the route is added by the LTE or 3g modems. |
| **mpls** - group of generic parameters associated with the MPLS |
|   
 | **.in-label** () | Mapped MPLS ingress label |
|   
 | **.labels** () |   
 |
|   
 | **.out-label** () | Mapped MPLS egress label |
| **nexthop-id** () |   
 |
| **ospf** (_yes | no_) | A flag indicates whether the route was added by the [OSPF](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=328218) routing protocol. |
| **ospf** - group of parameters associated with the OSPF protocol |
|   
 | **.metric** (_integer_) |   
 |
|   
 | **.type** (_string_) |   
 |
| **pref-src** () |   
 |
| **received-from** () |   
 |
| **rip** (_yes | no_) | A flag indicates whether the route was added by the RIP routing protocol |
| **rip** - group of parameters associated with the RIP protocol |
|   
 | **.metric** () |   
 |
|   
 | **.route-tag** () |   
 |
| **route-cost** () |   
 |
| **routing-table** () | Routing table this route belongs to. |
| **rpki** _(valid | invalid | unknown)_ | Current status of the prefix from the [RPKI](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=59277471) validation process. |
| **scope** (_integer_) | Scope used in the next-hop lookup process. [Read more>>](https://help.mikrotik.com/docs/display/ROS/How+Packets+Are+Routed#HowPacketsAreRouted-RouteSelection) |
| **static** (_yes | no_) | A flag indicates statically added routes. |
| **target-scope** (_integer_) | Target scope used in next-hop lookup process. [Read more>>](https://help.mikrotik.com/docs/display/ROS/How+Packets+Are+Routed#HowPacketsAreRouted-RouteSelection) |
| **te-tunnel-id** () | Traffic Engineering tunnel ID |
| **total-cost** () |   
 |
| **unreachable** (_yes | no_) | A flag indicates whether the route next-hop is unreachable. |
| **update-time** () |   
 |
|   
 | ve-block-offset |   
 |
|   
 | ve-block-size |   
 |
|   
 | ve-id |   
 |
| **vpn** (_yes | no_) | A flag indicates whether the route was added by one of the VPN protocols (PPPoE, L2TP, SSTP, etc.) |
| **vrf-interface** () | Internal use only parameter which allows identifying to which VRF route should be added. Used by services that add routes dynamically, for example, DHCP client. Shown for debugging purposes. |