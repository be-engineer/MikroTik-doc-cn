Global Router ID election configuration. ID can be configured explicitly or set to be elected from one of the Routers IP addresses.

For each VRF table RouterOS adds dynamic ID instance, that elects the ID from one of the IP addresses belonging to a particular VRF:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=59965506#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@rack1_b33_CCR1036] /routing/id&gt; print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: D - DYNAMIC, I - INACTIVE</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Columns: NAME, DYNAMIC-ID, SELECT-DYNAMIC-ID, SELECT-FROM-VRF</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">#&nbsp;&nbsp; NAME&nbsp;&nbsp; DYNAMIC-ID&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; SELECT-D&nbsp;&nbsp; SELE</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">0 D main&nbsp;&nbsp; 111.111.111.2&nbsp;&nbsp; only-vrf&nbsp;&nbsp; main</code></div></div></td></tr></tbody></table>

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
| **disabled** (_yes | no_) | ID reference is not used. |
| **id**(_IP_) | Parameter to explicitly set the Router ID. If ID is not explicitly specified, then it can be elected from one of the configured IP addresses on the router. See parameters select-dynamic-id and select-from-vrf. |
| **name** (_string_) | Reference name |
| **select-dynamic-id**(_any | lowest | only-active | only-loopback | only-static | only-vrf_) | States what IP addresses to use for the ID election:  

-   any - any address found on the router can be elected as the Router ID.
-   lowest - pick the lowest IP address.
-   only-active - pick an ID only from active IP addresses.
-   only-loopback - pick an ID only from loopback addresses.
-   only-vrf - pick an ID only from selected VRF. Works with select-from-vrf property.

 |
| **select-from-vrf** (_name_) | VRF from which to select IP addresses for the ID election. |

  

### **Read-only Properties**

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
| **dynamic** (_yes | no_) |   
 |
| **dynamic-id** (_IP_) | Currently selected ID. |
| **inactive** (_yes | no_) | If there was a problem to get a valid ID, then item can become inactive. |