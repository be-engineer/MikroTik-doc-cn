# Summary

Precision Time Protocol is used to synchronize clocks throughout the network. On a local area network, it achieves clock accuracy in the sub-microsecond range, making it suitable for measurement and control systems. RouterOS supports IEEE 1588-2008, PTPv2. Support is hardware dependant, please see the supported device list below.

Supported features:

-   Boundary/Ordinary clock
-   E2E delay mode
-   PTP delay mode
-   UDP over IPv4 multicast transport mode
-   L2 transport mode
-   priority1 can be configured to decide master/slave
-   PTP clock IS NOT synced with the system clock

# General properties

**Sub-menu:** `/system ptp`

  

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

|                                   |
| --------------------------------- | -------------------------------------------------------------------- |
| **port**                          | Sub-menu used for adding, removing, or viewing assigned ports        |
| **status**                        | Sub-menu that shows PTP ports, their state, and delay on slave ports |
| **comment** (_string_; Default: ) |

Short description of the PTP profile

 |
| **name** (_string_; Default: ) | Name of the PTP profile |
| **delay-mode** (_auto | e2e | ptp_; Default: **auto**) | Configures delay mode for PTP profile

-   -   _auto_ \- selects delay mode automatically
    -   _e2e_ \- use the delay request-response mechanism
    -   _ptp_ \- use the peer delay mechanism

 |
| **priority1** (_integer \[0..255\]_; auto; Default: **auto**) | the priority value for influencing grandmaster election |
| **profile** (_802.1as; default; g8275.1;_ Default: **default**) | 

IEEE 1588-2008 includes a _profile_ concept defining PTP operating parameters and options. 

IEEE 802.1AS is an adaptation of PTP for use with Audio Video Bridging and Time-Sensitive Networking. Uses delay-mode=p2p, transport-mode=l2; recommends using priority1=auto.

g8275.1 profile is for frequency and phase synchronization in a fully PTP-aware network. Only allows priority1=auto (128), priority2=128, domain=24, delay-mode=e2e, transport=l2.

default profile, PTPv2 default configuration, allows for more configuration options than other profiles, but default values with auto settings correspond to: priority1=128. priority2=128, domain=0,transport=ipv4, delay-mode=e2e

 |
| **transport** (_auto; ipv4;  l2;_ Default: **auto**) | transport protocol to be used: IPv4 or layer2 |

  

For more details regarding Precision Time Protocol please see the following standards IEEE 1588 and IEEE 802.1as.

We strongly recommend keeping default/auto values, as there are different requirements between profiles. And assigning them manually can result in misconfiguration.

# Configuration

To configure the device to participate in PTP you first need to create a PTP profile:

[?](https://help.mikrotik.com/docs/display/ROS/Precision+Time+Protocol#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system ptp </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ptp1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros comments">#to view the created profile use</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/system ptp </code><code class="ros functions">print</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: I - inactive, X - disab</code><code class="ros plain">led</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0 </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"ptp1"</code> <code class="ros value">priority1</code><code class="ros plain">=auto</code> <code class="ros value">delay-mode</code><code class="ros plain">=auto</code> <code class="ros value">transport</code><code class="ros plain">=auto</code> <code class="ros value">profile</code><code class="ros plain">=default</code></div></div></td></tr></tbody></table>

Note

Only 1 PTP profile is supported per device

  

After creating a PTP profile, you need to assign ports to it:

[?](https://help.mikrotik.com/docs/display/ROS/Precision+Time+Protocol#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system ptp port </code><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">ptp</code><code class="ros plain">=ptp1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros comments">#to view assigned ports use</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/system ptp port </code><code class="ros functions">print</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: I - inactive</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0 </code><code class="ros value">ptp</code><code class="ros plain">=ptp1</code> <code class="ros value">interface</code><code class="ros plain">=ether8</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">1 </code><code class="ros value">ptp</code><code class="ros plain">=ptp1</code> <code class="ros value">interface</code><code class="ros plain">=ether22</code></div></div></td></tr></tbody></table>

To monitor the PTP profile, use the monitor command:

[?](https://help.mikrotik.com/docs/display/ROS/Precision+Time+Protocol#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros comments">#on grandmaster device</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@grandmaster] &gt; system ptp </code><code class="ros functions">monitor </code><code class="ros value">numbers</code><code class="ros plain">=0</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">name</code><code class="ros constants">: test</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">clock-id</code><code class="ros constants">: 64:D1:54:FF:FE:EB:AE:C3</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">priority1</code><code class="ros constants">: 30</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">priority2</code><code class="ros constants">: 128</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">i-am-gm</code><code class="ros constants">: yes</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros comments">#on non-grandmaster device</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">[admin@328] </code><code class="ros constants">/system ptp </code><code class="ros functions">monitor </code><code class="ros plain">0</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">name</code><code class="ros constants">: ptp1</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">clock-id</code><code class="ros constants">: 64:D1:54:FF:FE:EB:AD:C7</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros plain">priority1</code><code class="ros constants">: 128</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros plain">priority2</code><code class="ros constants">: 128</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros plain">i-am-gm</code><code class="ros constants">: no</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros plain">gm-clock-id</code><code class="ros constants">: 64:D1:54:FF:FE:EB:AE:C3</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros plain">gm-priority1</code><code class="ros constants">: 30</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros plain">gm-priority2</code><code class="ros constants">: 128</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros plain">master-clock-id</code><code class="ros constants">: 64:D1:54:FF:FE:EB:AE:C3</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros plain">slave-port</code><code class="ros constants">: ether8</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros plain">freq-drift</code><code class="ros constants">: 2147483647 ppb</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros plain">offset</code><code class="ros constants">: 1396202830 ns</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros plain">hw-offset</code><code class="ros constants">: 1306201921 ns</code></div><div class="line number24 index23 alt1" data-bidi-marker="true"><code class="ros plain">slave-port-delay</code><code class="ros constants">: 2075668440 ns</code></div></div></td></tr></tbody></table>

## Monitor properties

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

|                       |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **clock-id:**         | local clock ID                                                                                                                                                                        |
| **priority1:**        | priority1 value, depending on the PTP profile selected, an adjustable value used to influence the grandmaster election.                                                               |
| **priority2:**        | priority2 value, non-adjustable in RouterOS                                                                                                                                           |
| **i-am-gm:** yes      | no                                                                                                                                                                                    | shows if the device is a grandmaster clock |
| **gm-clock-id:**      | grandmaster clock ID - Within a domain, a clock that is the ultimate source of time for clock synchronization using the protocol.                                                     |
| **gm-priority1:**     | grandmaster priority1                                                                                                                                                                 |
| **gm-priority2:**     | grandmaster priority2                                                                                                                                                                 |
| **master-clock-id:**  | master clock ID - In the context of a single Precision Time Protocol (PTP) communication path, a clock that is the source of time to which all other clocks on that path synchronize. |
| **slave-port:**       | shows which port is going towards the master or grandmaster clock                                                                                                                     |
| **freq-drift:**       | frequency drift in PPB (parts per billion) - time that would be lost every second in relation to the master clock, IF there was no synchronization.                                   |
| **offset:**           | difference between clock values                                                                                                                                                       |
| **hw-offset:**        | offset difference from the hardware clock                                                                                                                                             |
| **slave-port-delay:** | the time it takes for a packet to be delivered to a directly connected device                                                                                                         |

# Device support

### Supported on:

-   CRS326-24G-2S+ supported only on Gigabit Ethernet ports
-   CRS328-24P-4S+ supported only on Gigabit Ethernet ports
-   CRS317-1G-16S+ supported on all ports
-   CRS326-24S+2Q+ supported on SFP+ and QSFP+ interfaces
-   CRS312-4C+8XG supported on all ports
-   CRS318-16P-2S+ supported only on Gigabit Ethernet ports

### Not supported on:

-   CRS305-1G-4S+
-   CRS309-1G-8S+
-   CRS328-4C-20S-4S+
-   CRS354-48G-4S+2Q+
-   CRS354-48P-4S+2Q+