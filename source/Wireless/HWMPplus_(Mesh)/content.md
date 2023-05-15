# Summary

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=8978441#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface mesh</code></div></div></td></tr></tbody></table>

HWMP+ is a MikroTik specific layer-2 routing protocol for wireless mesh networks. It is based on Hybrid Wireless Mesh Protocol (HWMP) from IEEE 802.11s draft standard. It can be used instead of (Rapid) Spanning Tree protocols in mesh setups to ensure loop-free optimal routing.

The HWMP+ protocol however is not compatible with HWMP from IEEE 802.11s draft standard.

Note that the distribution system you use for your network need not be a Wireless Distribution System (WDS). HWMP+ mesh routing supports not only WDS interfaces but also Ethernet interfaces inside the mesh. So you can use a simple Ethernet-based distribution system, or you can combine both WDS and Ethernet links!

 Prerequisites for this article: you understand what WDS is and why to use it!

# Properties

## Mesh

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

|                                                               |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **admin-mac** (_MAC address_; **Default: 00:00:00:00:00:00)** | Administratively assigned MAC address, used when the **auto-mac** setting is disabled                                                                                                                                                                                            |
| **arp** (_disabled                                            | enabled                                                                                                                                                                                                                                                                          | proxy-arp | reply-only_; Default: **enabled**) | Address Resolution Protocol setting |
| **auto-mac** (_boolean_; Default: **no**)                     | If disabled, then the value from **admin-mac** will be used as the MAC address of the mesh interface; else address of some port will be used if ports are present                                                                                                                |
| **hwmp-default-hoplimit** (_integer: 1..255_; Default: )      | Maximum hop count for generated routing protocol packets; after an HWMP+ packet is forwarded "hoplimit" times, it is dropped                                                                                                                                                     |
| **hwmp-prep-lifetime** (_time_; Default: **5m**)              | Lifetime for routes created from received PREP or PREQ messages                                                                                                                                                                                                                  |
| **hwmp-preq-destination-only** (_boolean_; Default: **yes**)  | Whether the only destination can respond to HWMP+ PREQ message                                                                                                                                                                                                                   |
| **hwmp-preq-reply-and-forward** (_boolean_; Default: **yes**) | Whether intermediate nodes should forward HWMP+ PREQ message after responding to it. Useful only when **hwmp-preq-destination-only** is disabled                                                                                                                                 |
| **hwmp-preq-retries** (_integer_; Default: **2**)             | How many times to retry a route discovery to a specific MAC address before the address is considered unreachable                                                                                                                                                                 |
| **hwmp-preq-waiting-time** (_time_; Default: **4s**)          | How long to wait for a response to the first PREQ message. Note that for subsequent PREQs the waiting time is increased exponentially                                                                                                                                            |
| **hwmp-rann-interval** (_time_; Default: **10s**)             | How often to send out HWMP+ RANN messages                                                                                                                                                                                                                                        |
| **hwmp-rann-lifetime** (_time_; Default: **1s**)              | Lifetime for routes created from received RANN messages                                                                                                                                                                                                                          |
| **hwmp-rann-propagation-delay** (_number_; Default: **0.5**)  | How long to wait before propagating a RANN message. Value in seconds                                                                                                                                                                                                             |
| **mesh-portal** (_boolean_; Default: **no**)                  | Whether this interface is a portal in the mesh network                                                                                                                                                                                                                           |
| **mtu** (_number_; Default: **1500**)                         | Maximum transmission unit size                                                                                                                                                                                                                                                   |
| **name** (_string_; Default: )                                | Interface name                                                                                                                                                                                                                                                                   |
| **reoptimize-paths** (_boolean_; Default: **no**)             | Whether to send out periodic PREQ messages asking for known MAC addresses. Turning on this setting is useful if the network topology is changing often. Note that if no reply is received to a re-optimization PREQ, the existing path is kept anyway (until it timeouts itself) |

## Port

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

|                                                      |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| **active-port-type** (_read-only: wireless           | WDS                                                                                              | ethernet-mesh | ethernet-bridge       | ethernet-mixed_; Default: ) | port type and state actually used |
| **hello-interval** (_time_; Default: **10s**)        | the maximum interval between sending out HWMP+ Hello messages. Used only for Ethernet type ports |
| **interface** (_interface name_; Default: )          | interface name, which is to be included in a mesh                                                |
| **mesh** (_interface name_; Default: )               | mesh interface this port belongs to                                                              |
| **path-cost** (_integer: 0..65535_; Default: **10**) | path cost to the interface, used by routing protocol to determine the 'best' path                |
| **port-type** (_WDS                                  | auto                                                                                             | ethernet      | wireless_; Default: ) | port type to use            |

-   auto - port type is determined automatically based on the underlying interface's type
-   WDS - a Wireless Distribution System interface. Remote MAC address is learned from wireless connection data
-   ethernet - Remote MAC addresses are learned either from HWMP+ Hello messages or from source MAC addresses in received or forwarded traffic
-   wireless - Remote MAC addresses are learned from wireless connection data

 |

## FDB Status

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

|                                 |
| ------------------------------- | ------------------------------------------------------- |
| **mac-address** (_MAC address_) | MAC address corresponding for this FDB entry            |
| **seq-number** (_integer_)      | sequence number used in routing protocol to avoid loops |
| **type** (_integer_)            | sequence number used in routing protocol to avoid loops |
| **interface** (_local           | outsider                                                | direct | mesh | neighbor | larval | unknown_) | type of this FDB entry |

-   local -- MAC address belongs to the local router itself
-   outsider -- MAC address belongs to a device external to the mesh network
-   direct -- MAC address belongs to a wireless client on an interface that is in the mesh network
-   mesh -- MAC address belongs to a device reachable over the mesh network; it can be either internal or external to the mesh network
-   neighbor -- MAC address belongs to a mesh router that is a direct neighbor to this router
-   larval -- MAC address belongs to an unknown device that is reachable over the mesh network
-   unknown -- MAC address belongs to an unknown device

 |
| **mesh** (_interface name_) | the mesh interface this FDB entry belongs to |
| **on-interface** (_interface name_) | mesh port used for traffic forwarding, kind of a next-hop value |
| **lifetime** (_time_) | time remaining to live if this entry is not used for traffic forwarding |
| **age** (_time_) | age of this FDB entry |
| **metric** (_integer_) | a metric value used by routing protocol to determine the 'best' path |

# Example

![](https://help.mikrotik.com/docs/download/attachments/8978441/Mesh_ex1.jpg?version=2&modificationDate=1612788541366&api=v2)

This example uses static WDS links that are dynamically added as mesh ports when they become active. Two different frequencies are used: one for AP interconnections, and one for client connections to APs, so the AP must have at least two wireless interfaces. Of course, the same frequency for all connections also could be used, but that might not work as well because of potential interference issues.

Repeat this configuration on all APs:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=8978441#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface mesh </code><code class="ros functions">add </code><code class="ros value">disabled</code><code class="ros plain">=no</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface mesh port </code><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=wlan1</code> <code class="ros value">mesh</code><code class="ros plain">=mesh1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface mesh port </code><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=wlan2</code> <code class="ros value">mesh</code><code class="ros plain">=mesh1</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments"># interface used for AP interconnections</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface wireless </code><code class="ros functions">set </code><code class="ros plain">wlan1 </code><code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">ssid</code><code class="ros plain">=mesh</code> <code class="ros value">frequency</code><code class="ros plain">=2437</code> <code class="ros value">band</code><code class="ros plain">=2.4ghz-b/g/n</code> <code class="ros value">mode</code><code class="ros plain">=ap-bridge</code> <code class="ros plain">\</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros value">wds-mode</code><code class="ros plain">=static-mesh</code> <code class="ros value">wds-default-bridge</code><code class="ros plain">=mesh1</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros comments"># interface used for client connections</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros constants">/interface wireless </code><code class="ros functions">set </code><code class="ros plain">wlan2 </code><code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">ssid</code><code class="ros plain">=mesh-clients</code> <code class="ros value">frequency</code><code class="ros plain">=5180</code> <code class="ros value">band</code><code class="ros plain">=5ghz-a/n/ac</code> <code class="ros value">mode</code><code class="ros plain">=ap-bridge</code></div><div class="line number11 index10 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros comments"># a static WDS interface for each AP you want to connect to</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros constants">/interface wireless wds </code><code class="ros functions">add </code><code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">master-interface</code><code class="ros plain">=wlan1</code> <code class="ros value">name</code><code class="ros plain">=&lt;</code><code class="ros plain">;descriptive name of remote end&gt; \</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros value">wds-address</code><code class="ros plain">=&lt;</code><code class="ros plain">;MAC address of remote end&gt;</code></div></div></td></tr></tbody></table>

Here WDS interface is added manually because static WDS mode is used. If you are using **wds-mode**\=**dynamic-mesh**, all WDS interfaces will be created automatically. The **frequency** and **band** parameters are specified here only to produce valid example configuration; mesh protocol operations are by no means limited to or optimized for, these particular values.

You may want to increase the **disconnect-timeout** wireless interface option to make the protocol more stable.

In real-world setups you also should take care of securing the wireless connections, using **/interface wireless security-profile**. For simplicity, that configuration is not shown here.

Results on router A (there is one client connected to wlan2):

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=8978441#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@A] &gt; </code><code class="ros constants">/interface mesh </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, R - running</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">0 R </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"mesh1"</code> <code class="ros value">mtu</code><code class="ros plain">=1500</code> <code class="ros value">arp</code><code class="ros plain">=enabled</code> <code class="ros value">mac-address</code><code class="ros plain">=00:0C:42:0C:B5:A4</code> <code class="ros value">auto-mac</code><code class="ros plain">=yes</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros value">admin-mac</code><code class="ros plain">=00:00:00:00:00:00</code> <code class="ros value">mesh-portal</code><code class="ros plain">=no</code> <code class="ros value">hwmp-default-hoplimit</code><code class="ros plain">=32</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros value">hwmp-preq-waiting-time</code><code class="ros plain">=4s</code> <code class="ros value">hwmp-preq-retries</code><code class="ros plain">=2</code> <code class="ros value">hwmp-preq-destination-only</code><code class="ros plain">=yes</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros value">hwmp-preq-reply-and-forward</code><code class="ros plain">=yes</code> <code class="ros value">hwmp-prep-lifetime</code><code class="ros plain">=5m</code> <code class="ros value">hwmp-rann-interval</code><code class="ros plain">=10s</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros value">hwmp-rann-propagation-delay</code><code class="ros plain">=1s</code> <code class="ros value">hwmp-rann-lifetime</code><code class="ros plain">=22s</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">[admin@A] &gt; </code><code class="ros constants">/interface mesh port </code><code class="ros functions">print </code><code class="ros plain">detail</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - inactive, D - dynamic</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">0 </code><code class="ros value">interface</code><code class="ros plain">=wlan1</code> <code class="ros value">mesh</code><code class="ros plain">=mesh1</code> <code class="ros value">path-cost</code><code class="ros plain">=10</code> <code class="ros value">hello-interval</code><code class="ros plain">=10s</code> <code class="ros value">port-type</code><code class="ros plain">=auto</code> <code class="ros value">port-type-used</code><code class="ros plain">=wireless</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">1 </code><code class="ros value">interface</code><code class="ros plain">=wlan2</code> <code class="ros value">mesh</code><code class="ros plain">=mesh1</code> <code class="ros value">path-cost</code><code class="ros plain">=10</code> <code class="ros value">hello-interval</code><code class="ros plain">=10s</code> <code class="ros value">port-type</code><code class="ros plain">=auto</code> <code class="ros value">port-type-used</code><code class="ros plain">=wireless</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros plain">2 D </code><code class="ros value">interface</code><code class="ros plain">=router_B</code> <code class="ros value">mesh</code><code class="ros plain">=mesh1</code> <code class="ros value">path-cost</code><code class="ros plain">=105</code> <code class="ros value">hello-interval</code><code class="ros plain">=10s</code> <code class="ros value">port-type</code><code class="ros plain">=auto</code> <code class="ros value">port-type-used</code><code class="ros plain">=WDS</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros plain">3 D </code><code class="ros value">interface</code><code class="ros plain">=router_D</code> <code class="ros value">mesh</code><code class="ros plain">=mesh1</code> <code class="ros value">path-cost</code><code class="ros plain">=76</code> <code class="ros value">hello-interval</code><code class="ros plain">=10s</code> <code class="ros value">port-type</code><code class="ros plain">=auto</code> <code class="ros value">port-type-used</code><code class="ros plain">=WDS</code></div></div></td></tr></tbody></table>

The FDB (Forwarding Database) at the moment contains information only about local MAC addresses, non-mesh nodes reachable through a local interface, and direct mesh neighbors:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=8978441#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@A] </code><code class="ros constants">/interface mesh fdb </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: A - active, R - root</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">MESH TYPE MAC-ADDRESS ON-INTERFACE LIFETIME AGE</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">A mesh1 </code><code class="ros functions">local </code><code class="ros plain">00</code><code class="ros constants">:0C:42:00:00:AA 3m17s</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">A mesh1 neighbor 00</code><code class="ros constants">:0C:42:00:00:BB router_B 1m2s</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">A mesh1 neighbor 00</code><code class="ros constants">:0C:42:00:00:DD router_D 3m16s</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">A mesh1 direct 00</code><code class="ros constants">:0C:42:0C:7A:2B wlan2 2m56s</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">A mesh1 </code><code class="ros functions">local </code><code class="ros plain">00</code><code class="ros constants">:0C:42:0C:B5:A4 2m56s</code></div><div class="line number9 index8 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">[admin@A] </code><code class="ros constants">/interface mesh fdb </code><code class="ros functions">print </code><code class="ros plain">detail</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: A - active, R - root</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">A </code><code class="ros value">mac-address</code><code class="ros plain">=00:0C:42:00:00:AA</code> <code class="ros value">type</code><code class="ros plain">=local</code> <code class="ros value">age</code><code class="ros plain">=3m21s</code> <code class="ros value">mesh</code><code class="ros plain">=mesh1</code> <code class="ros value">metric</code><code class="ros plain">=0</code> <code class="ros value">seqnum</code><code class="ros plain">=4294967196</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros plain">A </code><code class="ros value">mac-address</code><code class="ros plain">=00:0C:42:00:00:BB</code> <code class="ros value">type</code><code class="ros plain">=neighbor</code> <code class="ros value">on-interface</code><code class="ros plain">=router_B</code> <code class="ros value">age</code><code class="ros plain">=1m6s</code> <code class="ros value">mesh</code><code class="ros plain">=mesh1</code> <code class="ros value">metric</code><code class="ros plain">=132</code> <code class="ros value">seqnum</code><code class="ros plain">=4294967196</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros plain">A </code><code class="ros value">mac-address</code><code class="ros plain">=00:0C:42:00:00:DD</code> <code class="ros value">type</code><code class="ros plain">=neighbor</code> <code class="ros value">on-interface</code><code class="ros plain">=router_D</code> <code class="ros value">age</code><code class="ros plain">=3m20s</code> <code class="ros value">mesh</code><code class="ros plain">=mesh1</code> <code class="ros value">metric</code><code class="ros plain">=79</code> <code class="ros value">seqnum</code><code class="ros plain">=4294967196</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros plain">A </code><code class="ros value">mac-address</code><code class="ros plain">=00:0C:42:0C:7A:2B</code> <code class="ros value">type</code><code class="ros plain">=direct</code> <code class="ros value">on-interface</code><code class="ros plain">=wlan2</code> <code class="ros value">age</code><code class="ros plain">=3m</code> <code class="ros value">mesh</code><code class="ros plain">=mesh1</code> <code class="ros value">metric</code><code class="ros plain">=10</code> <code class="ros value">seqnum</code><code class="ros plain">=0</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros plain">A </code><code class="ros value">mac-address</code><code class="ros plain">=00:0C:42:0C:B5:A4</code> <code class="ros value">type</code><code class="ros plain">=local</code> <code class="ros value">age</code><code class="ros plain">=3m</code> <code class="ros value">mesh</code><code class="ros plain">=mesh1</code> <code class="ros value">metric</code><code class="ros plain">=0</code> <code class="ros value">seqnum</code><code class="ros plain">=0</code></div></div></td></tr></tbody></table>

Test if ping works:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=8978441#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@A] &gt; </code><code class="ros constants">/</code><code class="ros functions">ping </code><code class="ros plain">00</code><code class="ros constants">:0C:42:00:00:CC</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">00</code><code class="ros constants">:0C:42:00:00:CC 64 byte </code><code class="ros functions">ping </code><code class="ros value">time</code><code class="ros plain">=108</code> <code class="ros plain">ms</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">00</code><code class="ros constants">:0C:42:00:00:CC 64 byte </code><code class="ros functions">ping </code><code class="ros value">time</code><code class="ros plain">=51</code> <code class="ros plain">ms</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">00</code><code class="ros constants">:0C:42:00:00:CC 64 byte </code><code class="ros functions">ping </code><code class="ros value">time</code><code class="ros plain">=39</code> <code class="ros plain">ms</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">00</code><code class="ros constants">:0C:42:00:00:CC 64 byte </code><code class="ros functions">ping </code><code class="ros value">time</code><code class="ros plain">=43</code> <code class="ros plain">ms</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">4 packets transmitted, 4 packets received, 0% packet loss</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">round-trip min</code><code class="ros constants">/avg/max = 39/60.2/108 ms</code></div></div></td></tr></tbody></table>

Router A had to discover a path to Router C first, hence the slightly larger time for the first ping. Now the FDB also contains an entry for 00:0C:42:00:00:CC, with type "mesh".

Also, test that ARP resolving works and so does IP level ping:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=8978441#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@A] &gt; </code><code class="ros constants">/</code><code class="ros functions">ping </code><code class="ros plain">10.4.0.3</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">10.4.0.3 64 byte ping</code><code class="ros constants">: ttl=64 time=163 ms</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">10.4.0.3 64 byte ping</code><code class="ros constants">: ttl=64 time=46 ms</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">10.4.0.3 64 byte ping</code><code class="ros constants">: ttl=64 time=48 ms</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">3 packets transmitted, 3 packets received, 0% packet loss</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">round-trip min</code><code class="ros constants">/avg/max = 46/85.6/163 ms</code></div></div></td></tr></tbody></table>

### Mesh traceroute

There is also a mesh traceroute command, that can help you to determine which paths are used for routing.

For example, for this network:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=8978441#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@1] </code><code class="ros constants">/interface mesh fdb </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: A - active, R - root</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">MESH TYPE MAC-ADDRESS ON-INTERFACE LIFETIME AGE</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">A mesh1 </code><code class="ros functions">local </code><code class="ros plain">00</code><code class="ros constants">:0C:42:00:00:01 7m1s</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">A mesh1 mesh 00</code><code class="ros constants">:0C:42:00:00:02 wds4 17s 4s</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">A mesh1 mesh 00</code><code class="ros constants">:0C:42:00:00:12 wds4 4m58s 1s</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">A mesh1 mesh 00</code><code class="ros constants">:0C:42:00:00:13 wds4 19s 2s</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">A mesh1 neighbor 00</code><code class="ros constants">:0C:42:00:00:16 wds4 7m1s</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">A mesh1 mesh 00</code><code class="ros constants">:0C:42:00:00:24 wds4 18s 3s</code></div></div></td></tr></tbody></table>

Traceroute to 00:0C:42:00:00:12 shows:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=8978441#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@1] </code><code class="ros constants">/interface mesh traceroute mesh1 00:0C:42:00:00:12</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">ADDRESS TIME STATUS</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">00</code><code class="ros constants">:0C:42:00:00:16 1ms ttl-exceeded</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">00</code><code class="ros constants">:0C:42:00:00:02 2ms ttl-exceeded</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">00</code><code class="ros constants">:0C:42:00:00:24 4ms ttl-exceeded</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">00</code><code class="ros constants">:0C:42:00:00:13 6ms ttl-exceeded</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">00</code><code class="ros constants">:0C:42:00:00:12 6ms success</code></div></div></td></tr></tbody></table>

# Protocol description

## Reactive mode

![](https://help.mikrotik.com/docs/download/attachments/8978441/520px-Hwmp_reactive_a.jpg?version=1&modificationDate=1612788675602&api=v2)  
Router A wants to discover a path to C

  
![](https://help.mikrotik.com/docs/download/attachments/8978441/520px-Hwmp_reactive_b.jpg?version=1&modificationDate=1612788683515&api=v2)

Router C sends a unicast response to A

In reactive mode, HWMP+ is very much like AODV (Ad-hoc On-demand Distance Vector). All paths are discovered on-demand, by flooding Path Request (PREQ) message in the network. The destination node or some router that has a path to the destination will reply with a Path Response (PREP). Note that if the destination address belongs to a client, the AP this client is connected to will serve as a proxy for him (i.e. reply to PREQs on his behalf).

This mode is best suited for mobile networks, and/or when most of the communication happens between intra-mesh nodes.

## Proactive mode

![](https://help.mikrotik.com/docs/download/attachments/8978441/Hwmp_proactive_a.jpg?version=1&modificationDate=1612788716474&api=v2)  
The root announces itself by flooding RANN

  

![](https://help.mikrotik.com/docs/download/attachments/8978441/Hwmp_proactive_b.jpg?version=1&modificationDate=1612788725360&api=v2)  
Internal nodes respond with PREGs

In proactive mode, there are some routers configured as portals. In general, being a portal means that the router has interfaces to some other network, i.e. it is an entry/exit point to the mesh network.

The portals will announce their presence by flooding the Root Announcement (RANN) message in the network. Internal nodes will reply with a Path Registration (PREG) message. The result of this process will be routing trees with roots in the portal.

Routes to portals will serve as a kind of default route. If an internal router does not know the path to a particular destination, it will forward all data to its closest portal. The portal will then discover the path on behalf of the router if needed. The data afterward will flow through the portal. This may lead to sub-optimal routing unless the data is addressed to the portal itself or some external network the portals have interfaces to.

A proactive mode is best suited when most of the traffic goes between internal mesh nodes and a few portal nodes.

## Topology change detection

![](https://help.mikrotik.com/docs/download/attachments/8978441/Hwmp_error_a.jpg?version=1&modificationDate=1612788766081&api=v2)  
Data flow path

![](https://help.mikrotik.com/docs/download/attachments/8978441/Hwmp_error_b.jpg?version=1&modificationDate=1612788772566&api=v2)  
After the link disappears, an error is propagated upstream

HWMP+ uses Path Error (PERR) message to notify that a link has disappeared. The message is propagated to all upstream nodes up to the data source. The source on PERR reception restarts the path discovery process.

# FAQ

**Q. How is this better than RSTP?**

A. It gives you optimal routing. RSTP is only for loop prevention.

**Q. How the route selection is done?**

A. The route with the best metric is always selected after the discovery process. There is also a configuration option to periodically reoptimize already known routes.

Route metric is calculated as the sum of individual link metrics.

Link metric is calculated in the same way as for (R)STP protocols:

-   For Ethernet links the metric is configured statically (same as for OSPF, for example).
-   For WDS links the metric is updated dynamically depending on actual link bandwidth, which in turn is influenced by wireless signal strength, and the selected data transfer rate.

Currently, the protocol does not take into account the amount of bandwidth being used on a link, but that might be also used in the future.

**Q. How is this better than OSPF/RIP/layer-3 routing in general?**

A. WDS networks usually are bridged, not routed. The ability to self-configure is important for mesh networks, and routing generally requires much more configuration than bridging. Of course, you can always run any L3 routing protocol over a bridged network, but for mesh networks that usually makes little sense. 

 Since optimized layer-2 multicast forwarding is not included in the mesh protocol, it is better to avoid forwarding any multicast traffic (including OSPF) over meshed networks. If you need OSPF, then you have to configure [OSPF NBMA](https://wiki.mikrotik.com/wiki/OSPF-reference#NBMA_Neighbor) neighbors that use unicast mode instead.

**Q. What about performance/CPU requirements?**

A. The protocol itself, when properly configured, will take much fewer resources than OSPF (for example) would. Data forwarding performance on an individual router should be close to that of bridging.

**Q. How does it work together with existing mesh setups that are using RSTP?**

A. The internal structure of an RSTP network is transparent to the mesh protocol (because mesh hello packets are forwarded inside the RSTP network). The mesh will see the path between two entry points in the RSTP network as a single segment. On the other hand, a mesh network is not transparent to the RSTP, since RSTP hello packets are not be forwarded inside the mesh network. _(This is the behavior since v3.26)_

  

Routing loops are possible if a mesh network is attached to an RSTP network in two or more points!

  

Note that if you have a WDS link between two access points, then both ends must have the same configuration (either as ports in a mesh on both ends or as ports in a bridge interface on both ends).

You can also put a bridge interface as a mesh port (to be able to use a bridge firewall, for example).

**Q. Can I have multiple entry/exit points to the network?**

A. If the entry/exit points are configured as portals (i.e. proactive mode is used), each router inside the mesh network will select its closest portal and forward all data to it. The portal will then discover a path on behalf of the router if needed.

**Q. How to control or filter mesh traffic?**

A. At the moment the only way is to use a bridge firewall. Create a bridge interface, put the WDS interfaces and/or Ethernets in that bridge, and put that bridge in a mesh interface. Then configure bridge firewall rules.

To match MAC protocol used for mesh traffic encapsulation, use MAC protocol number 0x9AAA, and to match mesh routing traffic, use MAC protocol number 0x9AAB. Example:

[?](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=8978441#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">interface bridge settings </code><code class="ros functions">set </code><code class="ros value">use-ip-firewall</code><code class="ros plain">=yes</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">interface bridge filter </code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">action</code><code class="ros plain">=log</code> <code class="ros value">mac-protocol</code><code class="ros plain">=0x9aaa</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">interface bridge filter </code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">action</code><code class="ros plain">=log</code> <code class="ros value">mac-protocol</code><code class="ros plain">=0x9aab</code></div></div></td></tr></tbody></table>

It is perfectly possible to create mixed mesh/bridge setups that will not work (e.g. _Problematic example 1_ with bridge instead of a switch). The recommended fail-safe way that will always work is to create a separate bridge interface per each of the physical interfaces; then add all these bridge interfaces as mesh ports.

# Advanced topics

We all know that it's easy to make problematic layer-2 bridging or routing setups and it can be hard to debug them. (Compared to layer-3 routing setups.) So here are a few bad configuration examples that could create problems for you. Avoid them!

## Problematic example 1: Ethernet switch inside a mesh

![](https://help.mikrotik.com/docs/download/attachments/8978441/Mesh_bad_ex1.jpg?version=2&modificationDate=1612788797211&api=v2)

_Router A is outside the mesh, all the rest of the routers are inside. For routers B, C, D all interfaces are added as mesh ports._

Router A will not be able to communicate reliably with router C. The problem manifests itself when D is the designated router for Ethernet; if B takes this role, everything is OK. The main cause of the problem is MAC address learning on Ethernet switch.

Consider what happens when router A wants to send something to C. We suppose router A either knows or floods data to all interfaces. Either way, data arrives at the switch. The switch, not knowing anything about the destination's MAC address, forwards the data to both B and D.

What happens now:

1.  B receives the packet on a mesh interface. Since the MAC address is not local for B and B knows that he is not the designated router for the Ethernet network, he simply ignores the packet.
2.  D receives the packet on a mesh interface. Since the MAC address is not local for B and D is the designated router for the Ethernet network, he initiates the path discovery process to C.

After path discovery is completed, D has information that C is reachable over B. Now D encapsulates the packet and forwards it back to the Ethernet network. The encapsulated packet is forwarded by the switch, received and forwarded by B, and received by C. So far everything is good.

Now C is likely to respond to the packet. Since B already knows where A is, he will decapsulate and forward the reply packet. But now the switch will learn that the MAC address of C is reachable through B! That means, next time when something arrives from A addressed to C, the switch will forward data _only_ to B (and B, of course, will silently ignore the packet)!

In contrast, if B took up the role of a designated router, everything would be OK, because traffic would not have to go through the Ethernet switch twice.

_**Troubleshooting**_: either avoid such setup or disable MAC address learning on the switch. Note that on many switches that is not possible.

Also note that there will be no problem, if either:

-   router A supports and is configured to use HWMP+;
-   or Ethernet switch is replaced with a router that supports HWMP+ and has Ethernet interfaces added as mesh ports.

## Problematic example 2: wireless modes

_Consider this (invalid) setup example_:

![](https://help.mikrotik.com/docs/download/attachments/8978441/Mesh_bad_ex2.jpg?version=2&modificationDate=1612788828215&api=v2)

_Routers A and B are inside the mesh, router C: outside. For routers A and B all interfaces are added as mesh ports._

It is not possible to bridge wlan1 and wlan2 on router B now. The reason for this is pretty obvious if you understand how WDS works. For WDS communications four address frames are used. This is because for wireless multihop forwarding you need to know both the addresses of the intermediate hops, as well as the original sender and final receiver. In contrast, non-WDS 802.11 communication includes only three MAC addresses in a frame. That's why it's not possible to do multi-hop forwarding in station mode.

_**Troubleshooting**_: depends on what you want to achieve:

1.  If you want router C to act as a repeater either for wireless or Ethernet traffic, configure the WDS link between router B and router C, and run mesh routing protocol on all nodes.
2.  In other cases configure wlan2 on router B in AP mode and WLAN on router C in station mode.