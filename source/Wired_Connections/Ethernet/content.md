-   [Summary](https://help.mikrotik.com/docs/display/ROS/Ethernet#Ethernet-Summary)
-   2[Properties](https://help.mikrotik.com/docs/display/ROS/Ethernet#Ethernet-Properties)
-   3[Menu specific commands](https://help.mikrotik.com/docs/display/ROS/Ethernet#Ethernet-Menuspecificcommands)
-   4[Monitor](https://help.mikrotik.com/docs/display/ROS/Ethernet#Ethernet-Monitor)
-   5[Detect Cable Problems](https://help.mikrotik.com/docs/display/ROS/Ethernet#Ethernet-DetectCableProblems)
-   6[Stats](https://help.mikrotik.com/docs/display/ROS/Ethernet#Ethernet-Stats)

  

**Sub-menu:** `/interface ethernet`  
**Standards:** `[IEEE 802.3](http://grouper.ieee.org/groups/802/3/)`

# Summary

MikroTik RouterOS supports various types of Ethernet interfaces - ranging from 10Mbps to 10Gbps Ethernet over copper twisted pair, 1Gbps and 10Gbps SFP/SFP+ interfaces and 40Gbps QSFP interface. Certain RouterBoard devices are equipped with a combo interface that simultaneously contains two interface types (e.g. 1Gbps Ethernet over twisted pair and SFP interface) allowing to select the most suitable option or creating a physical link failover. Through RouterOS, it is possible to control different Ethernet related properties like link speed, auto-negotiation, duplex mode, etc, monitor a transceiver diagnostic information and see a wide range of Ethernet related statistics.

# Properties

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

|                          |
| ------------------------ | -------- |
| **advertise** (_10M-full | 10M-half | 100M-full       | 100M-half | 1000M-full                         | 1000M-half                        | 2500M-full | 5000M-full | 10000M-full_; Default: ) | Advertised speed and duplex modes for Ethernet interfaces over twisted pair, only applies when auto-negotiation is enabled. Advertising higher speeds than the actual interface supported speed will have no effect, multiple options are allowed. |
| **arp** (_disabled       | enabled  | local-proxy-arp | proxy-arp | reply-only_; Default: **enabled**) | Address Resolution Protocol mode: |

-   disabled \- the interface will not use ARP
-   enabled \- the interface will use ARP
-   local-proxy-arp \- the router performs proxy ARP on the interface and sends replies to the same interface
-   proxy-arp \- the router performs proxy ARP on the interface and sends replies to other interfaces
-   reply-only \- the interface will only reply to requests originated from matching IP address/MAC address combinations which are entered as static entries in the [ARP](https://wiki.mikrotik.com/wiki/Manual:IP/ARP "Manual:IP/ARP") table. No dynamic entries will be automatically stored in the ARP table. Therefore for communications to be successful, a valid static entry must already exist.

 |
| **auto-negotiation** (_yes | no_; Default: **yes**) | When enabled, the interface "advertises" its maximum capabilities to achieve the best connection possible.

-   **Note1:** Auto-negotiation should not be disabled on one end only, otherwise Ethernet Interfaces may not work properly.
-   **Note2:** Gigabit Ethernet and NBASE-T Ethernet links cannot work with auto-negotiation disabled.

 |
| **bandwidth** (_integer/integer_; Default: **unlimited/unlimited**) | Sets max rx/tx bandwidth in kbps that will be handled by an interface. TX limit is supported on all Atheros [switch-chip](https://wiki.mikrotik.com/wiki/Manual:Switch_Chip_Features "Manual:Switch Chip Features") ports. RX limit is supported only on Atheros8327/QCA8337 switch-chip ports. |
| **cable-setting** (_default | short | standard_; Default: **default**) | Changes the cable length setting (only applicable to NS DP83815/6 cards) |
| **combo-mode** (_auto | copper | sfp_; Default: **auto**) | When auto mode is selected, the port that was first connected will establish the link. In case this link fails, the other port will try to establish a new link. If both ports are connected at the same time (e.g. after reboot), the priority will be the SFP/SFP+ port. When sfp mode is selected, the interface will only work through SFP/SFP+ cage. When copper mode is selected, the interface will only work through RJ45 Ethernet port. |
| **comment** (_string_; Default: ) | Descriptive name of an item |
| **disable-running-check** (_yes | no_; Default: **yes**) | Disable running check. If this value is set to 'no', the router automatically detects whether the NIC is connected with a device in the network or not. Default value is 'yes' because older NICs do not support it. (only applicable to x86) |
| **tx-flow-control** (_on | off | auto_; Default: **off**) | When set to on, the port will generate pause frames to the upstream device to temporarily stop the packet transmission. Pause frames are only generated when some routers output interface is congested and packets cannot be transmitted anymore. **auto** is the same as **on** except when auto-negotiation=yes flow control status is resolved by taking into account what other end advertises. |
| **rx-flow-control** (_on | off | auto_; Default: **off**) | When set to on, the port will process received pause frames and suspend transmission if required. **auto** is the same as **on** except when auto-negotiation=yes flow control status is resolved by taking into account what other end advertises. |
| **full-duplex** (_yes | no_; Default: **yes**) | Defines whether the transmission of data appears in two directions simultaneously, only applies when auto-negotiation is disabled. |
| **l2mtu** (_integer \[0..65536\]_; Default: ) | Layer2 Maximum transmission unit. [Read more>>](https://wiki.mikrotik.com/wiki/Maximum_Transmission_Unit_on_RouterBoards "Maximum Transmission Unit on RouterBoards") |
| **mac-address** (_MAC_; Default: ) | Media Access Control number of an interface. |
| **master-port** (_name_; Default: **none**) | Outdated property, more details about this property can be found in the [Master-port](https://wiki.mikrotik.com/wiki/Manual:Master-port "Manual:Master-port") page. |
| **mdix-enable** (_yes | no_; Default: **yes**) | Whether the MDI/X auto cross over cable correction feature is enabled for the port (Hardware specific, e.g. ether1 on RB500 can be set to yes/no. Fixed to 'yes' on other hardware.) |
| **mtu** (_integer \[0..65536\]_; Default: **1500**) | Layer3 Maximum transmission unit |
| **name** (_string_; Default: ) | Name of an interface |
| **orig-mac-address** (_read-only: MAC_; Default: ) | Original Media Access Control number of an interface. |
| **poe-out** (_auto-on | forced-on | off_; Default: **off**) | Poe Out settings. [`Read more >>`](https://wiki.mikrotik.com/wiki/Manual:PoE-Out "Manual:PoE-Out") |
| **poe-priority** (_integer \[0..99\]_; Default: ) | Poe Out settings. [`Read more >>`](https://wiki.mikrotik.com/wiki/Manual:PoE-Out "Manual:PoE-Out") |
| **sfp-shutdown-temperature** (_integer_; Default: **95** | **80**) | The temperature in Celsius at which the interface will be temporarily turned off due to too high detected SFP module temperature (introduced v6.48). The default value for SFP/SFP+/SFP28 interfaces is 95, and for QSFP+/QSFP28 interfaces 80 (introduced v7.6). |
| **speed** (_10Mbps | 10Gbps | 100Mbps | 1Gbps_; Default: ) | Sets interface data transmission speed which takes effect only when auto-negotiation is disabled. |

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

|                        |
| ---------------------- | --------------------------------------------- |
| **running** (_yes      | no_)                                          | Whether interface is running. Note that some interface does not have running check and they are always reported as "running"              |
| **slave** (_yes        | no_)                                          | Whether interface is configured as a slave of another interface (for example [Bonding](https://wiki.mikrotik.com/wiki/Bonding "Bonding")) |
| **switch** (_integer_) | ID to which switch chip interface belongs to. |

# Menu specific commands

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

|                                        |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **blink** (_\[id, name\]_)             | Blink Ethernet leds                                                                                                                        |
| **monitor** (_\[id, name\]_)           | Monitor ethernet status. [Read more>>](https://wiki.mikrotik.com/wiki/Manual:Interface/Ethernet#Monitor)                                   |
| **reset-counters** (_\[id, name\]_)    | Reset stats counters. [Read more>>](https://wiki.mikrotik.com/wiki/Manual:Interface/Ethernet#Stats)                                        |
| **reset-mac-address** (_\[id, name\]_) | Reset MAC address to manufacturers default.                                                                                                |
| **cable-test** (_string_)              | Shows detected problems with cable pairs. [`Read More >>`](https://wiki.mikrotik.com/wiki/Manual:Interface/Ethernet#Detect_Cable_Problems) |

# Monitor

To print out a current link rate, duplex mode, and other Ethernet related properties or to see detailed diagnostics information for transceivers, use `/interface ethernet monitor` command. The provided information can differ for different interface types (e.g. Ethernet over twisted pair or SFP interface) or for different transceivers (e.g. SFP and QSFP).

**Properties**

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
| ------------------------------- | -------- |
| **advertising** (_10M-full      | 10M-half | 100M-full | 100M-half    | 1000M-full                       | 1000M-half | 2500M-full | 5000M-full | 10000M-full_) | Advertised speeds and duplex modes for Ethernet interfaces over twisted pair, only applies when auto-negotiation is enabled |
| **auto-negotiation** (_disabled | done     | failed    | incomplete_) | Current auto negotiation status: |

-   disabled \- negotiation disabled
-   done \- negotiation completed
-   failed \- negotiation failed
-   incomplete \- negotiation not completed yet

 |
| **default-cable-settings** (_short | standard_) | Default cable length setting (only applicable to NS DP83815/6 cards)

-   short \- support short cables
-   standard \- support standard cables

 |
| **full-duplex** (_yes | no_) | Whether transmission of data occurs in two directions simultaneously |
| **link-partner-advertising** (_10M-full | 10M-half | 100M-full | 100M-half | 1000M-full | 1000M-half | 2500M-full | 5000M-full | 10000M-full_) | Link partner advertised speeds and duplex modes for Ethernet interfaces over twisted pair, only applies when auto-negotiation is enabled |
| **rate** (_10Mbps | 100Mbps | 1Gbps | 2.5Gbps | 5Gbps | 10Gbps | 40Gbps |_) | Actual data rate of the connection. |
| **status** (_link-ok | no-link | unknown_) | Current link status of an interface

-   link-ok \- the card is connected to the network
-   no-link \- the card is not connected to the network
-   unknown \- the connection is not recognized (if the card does not report connection status)

 |
| **tx-flow-control** (_yes | no_) | Whether TX flow control is used |
| **rx-flow-control** (_yes | no_) | Whether RX flow control is used |
| **combo-state** (_copper | sfp_) | Used combo-mode for combo interfaces |
| **sfp-module-present** (_yes | no_) | Whether a transceiver is in cage |
| **sfp-rx-lose** (_yes | no_) | Whether a receiver signal is lost |
| **sfp-tx-fault** (_yes | no_) | Whether a transceiver transmitter is in fault state |
| **sfp-type** (_SFP-or-SFP+ | DWDM-SFP | QSFP+_) | Used transceiver type |
| **sfp-connector-type** (_SC | LC | optical-pigtail | copper-pigtail | multifiber-parallel-optic-1x12 | no-separable-connector | RJ45_) | Used transceiver connector type |
| **sfp-link-length-9um** (_m_) | Transceiver supported link length for single mode 9/125um fiber |
| **sfp-link-length-50um** (_m_) | Transceiver supported link length for multi mode 50/125um fiber (OM2) |
| **sfp-link-length-62um** (_m_) | Transceiver supported link length for multi mode 62.5/125um fiber (OM1) |
| **sfp-link-length-copper** (_m_) | Supported link length of copper transceiver |
| **sfp-vendor-name** (_string_) | Transceiver manufacturer |
| **sfp-vendor-part-number** (_string_) | Transceiver part number |
| **sfp-vendor-revision** (_string_) | Transceiver revision number |
| **sfp-vendor-serial** (_string_) | Transceiver serial number |
| **sfp-manufacturing-date** (_date_) | Transceiver manufacturing date |
| **sfp-wavelength** (_nm_) | Transceiver transmitter optical signal wavelength |
| **sfp-temperature** (_C_) | Transceiver temperature |
| **sfp-supply-voltage** (_V_) | Transceiver supply voltage |
| **sfp-tx-bias-current** (_mA_) | Transceiver Tx bias current |
| **sfp-tx-power** (_dBm_) | Transceiver transmitted optical power |
| **sfp-rx-power** (_dBm_) | Transceiver received optical power |
| **eeprom-checksum** (_good | bad_) | Whether EEPROM checksum is correct |
| **eeprom** (_hex dump_) | Raw EEPROM of the transceiver |

Example output of an Ethernet status:

[?](https://help.mikrotik.com/docs/display/ROS/Ethernet#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface ethernet </code><code class="ros functions">monitor </code><code class="ros plain">ether1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">name</code><code class="ros constants">: ether1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">status</code><code class="ros constants">: link-ok</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">auto-negotiation</code><code class="ros constants">: done</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">rate</code><code class="ros constants">: 1Gbps</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">full-duplex</code><code class="ros constants">: yes</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">tx-flow-control</code><code class="ros constants">: no</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">rx-flow-control</code><code class="ros constants">: no</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">advertising</code><code class="ros constants">: 10M-half,10M-full,100M-half,100M-full,1000M-half,1000M-full</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">link-partner-advertising</code><code class="ros constants">: 10M-half,10M-full,100M-half,100M-full,1000M-full</code></div></div></td></tr></tbody></table>

Example output of an SFP status:

[?](https://help.mikrotik.com/docs/display/ROS/Ethernet#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface ethernet </code><code class="ros functions">monitor </code><code class="ros plain">sfp-sfpplus24</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">name</code><code class="ros constants">: sfp-sfpplus24</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">status</code><code class="ros constants">: link-ok</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">auto-negotiation</code><code class="ros constants">: done</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">rate</code><code class="ros constants">: 10Gbps</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">full-duplex</code><code class="ros constants">: yes</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">tx-flow-control</code><code class="ros constants">: no</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">rx-flow-control</code><code class="ros constants">: no</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">advertising</code><code class="ros constants">:</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">link-partner-advertising</code><code class="ros constants">:</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">sfp-module-present</code><code class="ros constants">: yes</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">sfp-rx-loss</code><code class="ros constants">: no</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros plain">sfp-tx-fault</code><code class="ros constants">: no</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros plain">sfp-type</code><code class="ros constants">: SFP-or-SFP+</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros plain">sfp-connector-type</code><code class="ros constants">: LC</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros plain">sfp-link-length-50um</code><code class="ros constants">: 80m</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros plain">sfp-link-length-62um</code><code class="ros constants">: 30m</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros plain">sfp-vendor-name</code><code class="ros constants">: Mikrotik</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros plain">sfp-vendor-part-number</code><code class="ros constants">: S+85DLC03D</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros plain">sfp-vendor-revision</code><code class="ros constants">: A</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros plain">sfp-vendor-serial</code><code class="ros constants">: STST85S84700155</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros plain">sfp-manufacturing-date</code><code class="ros constants">: 18-12-07</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros plain">sfp-wavelength</code><code class="ros constants">: 850nm</code></div><div class="line number24 index23 alt1" data-bidi-marker="true"><code class="ros plain">sfp-temperature</code><code class="ros constants">: 33C</code></div><div class="line number25 index24 alt2" data-bidi-marker="true"><code class="ros plain">sfp-supply-voltage</code><code class="ros constants">: 3.251V</code></div><div class="line number26 index25 alt1" data-bidi-marker="true"><code class="ros plain">sfp-tx-bias-current</code><code class="ros constants">: 6mA</code></div><div class="line number27 index26 alt2" data-bidi-marker="true"><code class="ros plain">sfp-tx-power</code><code class="ros constants">: -2.843dBm</code></div><div class="line number28 index27 alt1" data-bidi-marker="true"><code class="ros plain">sfp-rx-power</code><code class="ros constants">: -1.203dBm</code></div><div class="line number29 index28 alt2" data-bidi-marker="true"><code class="ros plain">eeprom-checksum</code><code class="ros constants">: good</code></div><div class="line number30 index29 alt1" data-bidi-marker="true"><code class="ros plain">eeprom</code><code class="ros constants">: 0000: 03 04 07 10 00 00 00 20 40 0c c0 06 67 00 00 00 ....... @...g...</code></div><div class="line number31 index30 alt2" data-bidi-marker="true"><code class="ros plain">0010</code><code class="ros constants">: 08 03 00 1e 4d 69 6b 72 6f 74 69 6b 20 20 20 20 ....Mikr otik</code></div><div class="line number32 index31 alt1" data-bidi-marker="true"><code class="ros plain">0020</code><code class="ros constants">: 20 20 20 20 00 00 00 00 53 2b 38 35 44 4c 43 30 .... S+85DLC0</code></div><div class="line number33 index32 alt2" data-bidi-marker="true"><code class="ros plain">0030</code><code class="ros constants">: 33 44 20 20 20 20 20 20 41 20 20 20 03 52 00 45 3D A .R.E</code></div><div class="line number34 index33 alt1" data-bidi-marker="true"><code class="ros plain">0040</code><code class="ros constants">: 00 1a 00 00 53 54 53 54 38 35 53 38 34 37 30 30 ....STST 85S84700</code></div><div class="line number35 index34 alt2" data-bidi-marker="true"><code class="ros plain">0050</code><code class="ros constants">: 31 35 35 20 31 38 31 32 30 37 20 20 68 f0 05 b6 155 1812 07 h...</code></div><div class="line number36 index35 alt1" data-bidi-marker="true"><code class="ros plain">0060</code><code class="ros constants">: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ........ ........</code></div><div class="line number37 index36 alt2" data-bidi-marker="true"><code class="ros plain">0070</code><code class="ros constants">: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ........ ........</code></div><div class="line number38 index37 alt1" data-bidi-marker="true"><code class="ros plain">0080</code><code class="ros constants">: 64 00 d8 00 5f 00 dd 00 8c a0 6d 60 88 b8 71 48 d..._... ..m`..qH</code></div><div class="line number39 index38 alt2" data-bidi-marker="true"><code class="ros plain">0090</code><code class="ros constants">: 1d 4c 00 fa 17 70 01 f4 31 2d 04 ea 27 10 06 30 .L...p.. 1-..'..0</code></div><div class="line number40 index39 alt1" data-bidi-marker="true"><code class="ros plain">00a0</code><code class="ros constants">: 31 2d 01 3c 27 10 01 8e 00 00 00 00 00 00 00 00 1-.&lt;'... ........</code></div><div class="line number41 index40 alt2" data-bidi-marker="true"><code class="ros plain">00b0</code><code class="ros constants">: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ........ ........</code></div><div class="line number42 index41 alt1" data-bidi-marker="true"><code class="ros plain">00c0</code><code class="ros constants">: 00 00 00 00 3f 80 00 00 00 00 00 00 01 00 00 00 ....?... ........</code></div><div class="line number43 index42 alt2" data-bidi-marker="true"><code class="ros plain">00d0</code><code class="ros constants">: 01 00 00 00 01 00 00 00 01 00 00 00 00 00 00 26 ........ .......&amp;</code></div><div class="line number44 index43 alt1" data-bidi-marker="true"><code class="ros plain">00e0</code><code class="ros constants">: 21 8a 7f 00 0c cd 14 4c 1d 9c 00 00 00 00 00 00 !......L ........</code></div><div class="line number45 index44 alt2" data-bidi-marker="true"><code class="ros plain">00f0</code><code class="ros constants">: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ........ ........</code></div></div></td></tr></tbody></table>

# Detect Cable Problems

A cable test can detect problems or measure the approximate cable length if the cable is unplugged on the other end and there is, therefore, "no-link". RouterOS will show:

-   which cable pair is damaged
-   the distance to the problem
-   how exactly the cable is broken - short-circuited or open-circuited

This also works if the other end is simply unplugged - in that case, the total cable length will be shown.

Here is an example output:

[?](https://help.mikrotik.com/docs/display/ROS/Ethernet#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@CCR] &gt; interface ethernet cable-test ether2</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">name</code><code class="ros constants">: ether2</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">status</code><code class="ros constants">: no-link</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">cable-pairs</code><code class="ros constants">: open:4,open:4,open:4,open:4</code></div></div></td></tr></tbody></table>

In the above example, the cable is not shorted but “open” at 4 meters distance, all cable pairs are equally faulty at the same distance from the switch chip.

Currently `cable-test` is implemented on the following devices:

-   CCR series devices
-   CRS1xx series devices
-   CRS2xx series devices
-   OmniTIK series devices
-   RB450G series devices
-   RB951 series devices
-   RB2011 series devices
-   RB4011 series devices
-   RB750Gr2
-   RB750UPr2
-   RB751U-2HnD
-   RB850Gx2
-   RB931-2nD
-   RB941-2nD
-   RB952Ui-5ac2nD
-   RB962UiGS-5HacT2HnT
-   RB1100AHx2
-   RB1100x4
-   RBD52G-5HacD2HnD
-   RBcAPGi-5acD2nD
-   RBmAP2n
-   RBmAP2nD
-   RBwsAP-5Hac2nD
-   RB3011UiAS-RM
-   RBMetal 2SHPn
-   RBDynaDishG-5HacD
-   RBLDFG-5acD
-   RBLHGG-5acD

  

Currently `cable-test` is not supported on Combo ports.

# Stats

Using `/interface ethernet print stats` command, it is possible to see a wide range of Ethernet-related statistics. The list of statistics can differ between RouterBoard devices due to different Ethernet drivers. The list below contains all available counters across all RouterBoard devices. Most of the Ethernet statistics can be remotely monitored using [SNMP](https://wiki.mikrotik.com/wiki/Manual:SNMP "Manual:SNMP") and MIKROTIK-MIB.

  

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

|                                             |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **driver-rx-byte** (_integer_)              | Total count of received bytes on device CPU                                                                                             |
| **driver-rx-packet** (_integer_)            | Total count of received packets on device CPU                                                                                           |
| **driver-tx-byte** (_integer_)              | Total count of transmitted bytes by device CPU                                                                                          |
| **driver-tx-packet** (_integer_)            | Total count of transmitted packets by device CPU                                                                                        |
| **rx-64** (_integer_)                       | Total count of received 64 byte frames                                                                                                  |
| **rx-65-127** (_integer_)                   | Total count of received 65 to 127 byte frames                                                                                           |
| **rx-128-255** (_integer_)                  | Total count of received 128 to 255 byte frames                                                                                          |
| **rx-256-511** (_integer_)                  | Total count of received 256 to 511 byte frames                                                                                          |
| **rx-512-1023** (_integer_)                 | Total count of received 512 to 1023 byte frames                                                                                         |
| **rx-1024-1518** (_integer_)                | Total count of received 1024 to 1518 byte frames                                                                                        |
| **rx-1519-max** (_integer_)                 | Total count of received frames larger than 1519 bytes                                                                                   |
| **rx-align-error** (_integer_)              | Total count of received align error events - packets where bits are not aligned along octet boundaries                                  |
| **rx-broadcast** (_integer_)                | Total count of received broadcast frames                                                                                                |
| **rx-bytes** (_integer_)                    | Total count of received bytes                                                                                                           |
| **rx-carrier-error** (_integer_)            | Total count of received frames with carrier sense error                                                                                 |
| **rx-code-error** (_integer_)               | Total count of received frames with code error                                                                                          |
| **rx-control** (_integer_)                  | Total count of received control or pause frames                                                                                         |
| **rx-error-events** (_integer_)             | Total count of received frames with the active error event                                                                              |
| **rx-fcs-error** (_integer_)                | Total count of received frames with incorrect checksum                                                                                  |
| **rx-fragment** (_integer_)                 | Total count of received fragmented frames (not related to IP fragmentation)                                                             |
| **rx-ip-header-checksum-error** (_integer_) | Total count of received frames with IP header checksum error                                                                            |
| **rx-jabber** (_integer_)                   | Total count of received jabbed packets - a packet that is transmitted longer than the maximum packet length                             |
| **rx-length-error** (_integer_)             | Total count of received frames with frame length error                                                                                  |
| **rx-multicast** (_integer_)                | Total count of received multicast frames                                                                                                |
| **rx-overflow** (_integer_)                 | Total count of received overflowed frames can be caused when device resources are insufficient to receive a certain frame               |
| **rx-pause** (_integer_)                    | Total count of received pause frames                                                                                                    |
| **rx-runt** (_integer_)                     | Total count of received frames shorter than the minimum 64 bytes, is usually caused by collisions                                       |
| **rx-tcp-checksum-error** (_integer_)       | Total count of received frames with TCP header checksum error                                                                           |
| **rx-too-long** (_integer_)                 | Total count of received frames that were larger than the maximum supported frame size by the network device, see the max-l2mtu property |
| **rx-too-short** (_integer_)                | Total count of the received frame shorter than the minimum 64 bytes                                                                     |
| **rx-udp-checksum-error** (_integer_)       | Total count of received frames with UDP header checksum error                                                                           |
| **rx-unicast** (_integer_)                  | Total count of received unicast frames                                                                                                  |
| **rx-unknown-op** (_integer_)               | Total count of received frames with unknown Ethernet protocol                                                                           |
| **tx-64** (_integer_)                       | Total count of transmitted 64 byte frames                                                                                               |
| **tx-65-127** (_integer_)                   | Total count of transmitted 65 to 127 byte frames                                                                                        |
| **tx-128-255** (_integer_)                  | Total count of transmitted 128 to 255 byte frames                                                                                       |
| **tx-256-511** (_integer_)                  | Total count of transmitted 256 to 511 byte frames                                                                                       |
| **tx-512-1023** (_integer_)                 | Total count of transmitted 512 to 1023 byte frames                                                                                      |
| **tx-1024-1518** (_integer_)                | Total count of transmitted 1024 to 1518 byte frames                                                                                     |
| **tx-1519-max** (_integer_)                 | Total count of transmitted frames larger than 1519 bytes                                                                                |
| **tx-align-error** (_integer_)              | Total count of transmitted align error events - packets where bits are not aligned along octet boundaries                               |
| **tx-broadcast** (_integer_)                | Total count of transmitted broadcast frames                                                                                             |
| **tx-bytes** (_integer_)                    | Total count of transmitted bytes                                                                                                        |
| **tx-collision** (_integer_)                | Total count of transmitted frames that made collisions                                                                                  |
| **tx-control** (_integer_)                  | Total count of transmitted control or pause frames                                                                                      |
| **tx-deferred** (_integer_)                 | Total count of transmitted frames that were delayed on its first transmit attempt due to already busy medium                            |
| **tx-drop** (_integer_)                     | Total count of transmitted frames that were dropped due to the already full output queue                                                |
| **tx-excessive-collision** (_integer_)      | Total count of transmitted frames that already made multiple collisions and never got successfully transmitted                          |
| **tx-excessive-deferred** (_integer_)       | Total count of transmitted frames that were deferred for an excessive period of time due to an already busy medium                      |
| **tx-fcs-error** (_integer_)                | Total count of transmitted frames with incorrect checksum                                                                               |
| **tx-fragment** (_integer_)                 | Total count of transmitted fragmented frames (not related to IP fragmentation)                                                          |
| **tx-carrier-sense-error** (_integer_)      | Total count of transmitted frames with carrier sense error                                                                              |
| **tx-late-collision** (_integer_)           | Total count of transmitted frames that made collision after being already halfway transmitted                                           |
| **tx-multicast** (_integer_)                | Total count of transmitted multicast frames                                                                                             |
| **tx-multiple-collision** (_integer_)       | Total count of transmitted frames that made more than one collision and subsequently transmitted successfully                           |
| **tx-overflow** (_integer_)                 | Total count of transmitted overflowed frames                                                                                            |
| **tx-pause** (_integer_)                    | Total count of transmitted pause frames                                                                                                 |
| **tx-all-queue-drop-byte** (_integer_)      | Total count of transmitted bytes dropped by all output queues                                                                           |
| **tx-all-queue-drop-packet** (_integer_)    | Total count of transmitted packets dropped by all output queues                                                                         |
| **tx-queueX-byte** (_integer_)              | Total count of transmitted bytes on a certain queue, the **X** should be replaced with a queue number                                   |
| **tx-queueX-packet** (_integer_)            | Total count of transmitted frames on a certain queue, the **X** should be replaced with a queue number                                  |
| **tx-runt** (_integer_)                     | Total count of transmitted frames shorter than the minimum 64 bytes, is usually caused by collisions                                    |
| **tx-too-short** (_integer_)                | Total count of transmitted frames shorter than the minimum 64 bytes                                                                     |
| **tx-rx-64** (_integer_)                    | Total count of transmitted and received 64 byte frames                                                                                  |
| **tx-rx-64-127** (_integer_)                | Total count of transmitted and received 64 to 127 byte frames                                                                           |
| **tx-rx-128-255** (_integer_)               | Total count of transmitted and received 128 to 255 byte frames                                                                          |
| **tx-rx-256-511** (_integer_)               | Total count of transmitted and received 256 to 511 byte frames                                                                          |
| **tx-rx-512-1023** (_integer_)              | Total count of transmitted and received 512 to 1023 byte frames                                                                         |
| **tx-rx-1024-max** (_integer_)              | Total count of transmitted and received frames larger than 1024 bytes                                                                   |
| **tx-single-collision** (_integer_)         | Total count of transmitted frames that made only a single collision and subsequently transmitted successfully                           |
| **tx-too-long** (_integer_)                 | Total count of transmitted packets that were larger than the maximum packet size                                                        |
| **tx-underrun** (_integer_)                 | Total count of transmitted underrun packets                                                                                             |
| **tx-unicast** (_integer_)                  | Total count of transmitted unicast frames                                                                                               |

For example, the output of Ethernet stats on the hAP ac2 device:

[?](https://help.mikrotik.com/docs/display/ROS/Ethernet#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface ethernet </code><code class="ros functions">print </code><code class="ros plain">stats</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">name</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether1 ether2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ether4 ether5</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">driver-rx-byte</code><code class="ros constants">:&nbsp; 182 334 805 898&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp; 5 836 927 820&nbsp;&nbsp;&nbsp; 24 895 692&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">driver-rx-packet</code><code class="ros constants">:&nbsp;&nbsp;&nbsp; 4 449 562 546&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp; 4 320 155 362&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 259 449&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">driver-tx-byte</code><code class="ros constants">:&nbsp;&nbsp; 15 881 099 971&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0 70 502 669 211&nbsp;&nbsp;&nbsp; 60 498 056&nbsp;&nbsp;&nbsp;&nbsp; 53</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">driver-tx-packet</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 52 724 428&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; 54 231 229&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 106 498&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-bytes</code><code class="ros constants">:&nbsp; 178 663 398 808&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp; 5 983 590 739 1 358 140 795&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-too-short</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-64</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 12 749 144&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 362 459&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 125 917&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-65-127</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 9 612 406&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; 20 366 513&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 292 189&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-128-255</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 6 259 883&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1 672 588&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 261 013&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-256-511</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2 950 578&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 211 380&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 278 147&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-512-1023</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3 992 258&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 185 666&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 163 241&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-1024-1518</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 119 034 611&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2 796 559&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 696 254&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-1519-max</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-too-long</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-broadcast</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 12 025 189&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1 006 377&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 64 178&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-pause</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-multicast</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 4 687 869&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 36 188&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 220 136&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-fcs-error</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-align-error</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-fragment</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">rx-overflow</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number24 index23 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-bytes</code><code class="ros constants">:&nbsp;&nbsp; 16 098 535 973&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0 72 066 425 886&nbsp;&nbsp; 225 001 772&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number25 index24 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-64</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1 063 375&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 924 855&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 37 877&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number26 index25 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-65-127</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 26 924 514&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2 442 200&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 959 209&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number27 index26 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-128-255</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 14 588 113&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 924 746&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 295 961&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number28 index27 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-256-511</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1 323 733&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1 036 515&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 33 252&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number29 index28 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-512-1023</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1 287 464&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2 281 554&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3 625&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number30 index29 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-1024-1518</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 7 537 154&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; 48 212 304&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 64 659&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number31 index30 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-1519-max</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number32 index31 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-too-long</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number33 index32 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-broadcast</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 590&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 145 800&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 823 038&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number34 index33 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-pause</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number35 index34 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-multicast</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1 039 243&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 41 716&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number36 index35 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-underrun</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number37 index36 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-collision</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number38 index37 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-excessive-collision</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number39 index38 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-multiple-collision</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number40 index39 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-single-collision</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number41 index40 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-excessive-deferred</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number42 index41 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-deferred</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number43 index42 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tx-late-collision</code><code class="ros constants">:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div></div></td></tr></tbody></table>