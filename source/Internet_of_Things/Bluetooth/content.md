# Summary

Bluetooth is a short-range wireless technology that allows broadcasting the data over specific Bluetooth channels. 

There are 40 unique bands (channels) and each band has a 2 MHz separation. 37, 38, and 39 channels are used for primary advertising, and 0-36 are used for data transmission.

During the advertising process, the BLE advertising packet is broadcasted. This packet contains the Preamble, Access Address, PDU and CRS fields.

The Preamble and Access Address fields help the receiver detect frames. CRS field is used to check errors. PDU consists of PDU Header and PDU Payload. PDU defines the packet itself.

PDU Header contains information about the PDU type. Based on the type, the payload fields may differ.

For example, when PDU type is ADV\_NONCONN\_IND → PDU Payload consists of "AdvA" (a field that contains information about the advertiser's address) and "AdvData" (a field that contains data information) fields:

1 octet = 1 byte = 8 bits

<table class="relative-table wrapped confluenceTable" style="width: 41.1958%;"><colgroup><col style="width: 24.2667%;"><col style="width: 75.7333%;"></colgroup><tbody><tr><td class="confluenceTd">Preamble</td><td class="confluenceTd">1 octet</td></tr><tr><td class="confluenceTd">Access-Address</td><td class="confluenceTd">4 octets</td></tr><tr><td class="confluenceTd">PDU</td><td class="confluenceTd"><ul><li>PDU Header = 2 octets</li><li>PDU Payload = AdvA (6 octets)+AdvData (0...31 octets)</li></ul></td></tr><tr><td colspan="1" class="confluenceTd">CRS</td><td colspan="1" class="confluenceTd">3 octets</td></tr></tbody></table>

There are different PDU types:

-   ADV\_IND (where payload consists of AdvA \[6octets\] + AdvData \[0-31 octets\] and which is used for connectable, scannable undirected advertising);
-   ADV\_NOCONN\_IND (where payload consists of AdvA \[6octets\] + AdvData \[0-31 octets\] and which is used for non-connectable, non-scannable undirected advertising);
-   ADV\_SCAN\_IND (where payload consists of AdvA \[6octets\] + AdvData \[0-31 octets\] and which is used for scannable, undirected advertising);
-   SCAN\_REQ (where payload consists of ScanA \[6octets\] + AdvA \[6octets\], where ScanA field contains scanner's address and AdvA contains advertiser's address, and which is used for requesting SCAN\_RSP response);
-   SCAN\_RSP (where payload consists of AdvA \[6octets\] + ScanRspData \[0-31 octets\], where ScanRspData can contain any data from the advertiser's host and which is used to respond to a SCAN\_REQ request);
-   ADV\_DIRECT\_IND (where payload consists of AdvA \[6octets\] + TargetA \[6octets\], where TargetA is the device address field to which the PDU is addressed, and which is used for connectable, directed advertising);
-   etc

You can find more information about the packet structure over [here](https://www.bluetooth.com/specifications/specs/core-specification/) (Bluetooth specifications).

The main application for the Bluetooth interface in RouterOS is to monitor Bluetooth advertising packets (scanner feature) that are broadcasted by other devices (like for example, [Bluetooth tags](https://help.mikrotik.com/docs/display/UM/TG-BT5-IN)) or broadcast advertising packets (advertiser feature).

# Configuration

**Sub-menu:** `/iot bluetooth`

_**note**:_ **iot** package is required.

_**note**:_ Check your device's specifications page to make sure that the Bluetooth is supported by the unit.

IoT package is available with RouterOS version 6.48.3. You can get it from our [download page](https://mikrotik.com/download) - under "Extra packages".

## Devices

In this menu you can check and set general Bluetooth chip parameters:

[?](https://help.mikrotik.com/docs/display/ROS/Bluetooth#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; iot bluetooth print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NAME, PUBLIC-ADDRESS, RANDOM-STATIC-ADDRESS, ANTENNA</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros comments">#&nbsp; NAM&nbsp; PUBLIC-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp; RANDOM-STATIC-ADD&nbsp; ANTENNA</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">0&nbsp; bt1&nbsp; 00</code><code class="ros constants">:00:00:00:00:00&nbsp; F4:4E:E8:04:77:3A&nbsp; internal</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot bluetooth </code><code class="ros functions">set</code></div></div></td></tr></tbody></table>

_**note**:_ Public address is the IEEE registered, permanent address. This address can not be changed. In the "print" example above, the device does not have a public address assigned (all octets are set to 0).

Configurable settings are shown below:

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

 |                                           |
 | ----------------------------------------- | ------------------------------------------------------------------ |
 | **antenna** (_string_; Default: internal) | Choose whether to use an internal or an external Bluetooth antenna |
 | **name** (_string_; Default: )            | Descriptive name of Bluetooth chip/interface                       |
 |                                           |

**random-static-address** (_MAC address_; Default: )

 | A user-configurable address for the Bluetooth chip |

You can monitor chip stats with the command:

[?](https://help.mikrotik.com/docs/display/ROS/Bluetooth#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot bluetooth </code><code class="ros functions">print </code><code class="ros plain">stats</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NAME, RX-BYTES, TX-BYTES, RX-ERRORS, TX-ERRORS, RX-EVT, TX-CMD, RX-ACL, TX-ACL</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros comments">#&nbsp; NAM&nbsp; RX-BYTE&nbsp; TX-&nbsp; R&nbsp; T&nbsp; RX-EV&nbsp; TX&nbsp; R&nbsp; T</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">0&nbsp; bt1&nbsp; 1857835&nbsp; 235&nbsp; 0&nbsp; 0&nbsp; 46677&nbsp; 45&nbsp; 0&nbsp; 0</code></div></div></td></tr></tbody></table>

## Advertisers

In this menu, it is possible to set up the Bluetooth chip to broadcast advertising packets. You can check and set advertiser settings with the commands:

[?](https://help.mikrotik.com/docs/display/ROS/Bluetooth#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; iot bluetooth advertisers print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - DISABLED</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: DEVICE, MIN-INTERVAL, MAX-INTERVAL, OWN-ADDRESS-TYPE, CHANNEL-MAP, AD-SIZE</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments">#&nbsp;&nbsp; DEVICE&nbsp; MIN-INTERVAL&nbsp; MAX-INTERVAL&nbsp; OWN-ADDRESS-TYPE&nbsp; CHANNEL-MAP&nbsp; AD-SIZE</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0 X bt1&nbsp;&nbsp;&nbsp;&nbsp; 1280ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2560ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; random-static&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 37&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">38&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">39&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot bluetooth advertisers </code><code class="ros functions">set</code></div></div></td></tr></tbody></table>

Configurable settings are shown below:

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

 |                                         |
 | --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
 | **ad-structures** (_string_; Default: ) | Choose a pre-configured structure for the advertisement packets. For more information see the "AD structures" section. |
 | **channel-map** (_37                    | 38                                                                                                                     | 39_; Default: 37, 38, 39) | Channels used for advertising. |
 |                                         |

**disabled** (_yes | no_; Default: **yes**)

 | An option to disable or enable the Bluetooth chip to broadcast advertising packets. |
| 

**max-interval** (_integer:_20..10240;__ Default: **2560** **ms**)

 | The maximal interval for broadcasting advertising packets. |
| 

**min-interval** (_integer:_20..10240;__ Default: **1280 ms**)

 | The minimal interval for broadcasting advertising packets. |
| 

**own-address-type** (_public | random-static | rpa-fallback-to-public | rpa-fallback-to-random_; Default: **random-static**)

 | 

The MAC address that is going to be used in the advertising packet's payload:

-   public →  To use the IEEE registered, permanent address.
-   random-static →  To use user-configurable address (will be changed on the next power-cycle).
-   rpa-fallback-to-public → To use Resolvable Random Private Address (RPA) that can only be resolved if the receiver has our Identity Resolving Key (IRK). If RPA can not be generated, the public address will be used instead.
-   rpa-fallback-to-random → Same as "rpa-fallback-to-public" but if RPA can not be generated, the random-static address will be used instead.

 |

_**note**:_ Advertising packets will be broadcasted each _min-interval_ <= **X** <= _max-interval_ milliseconds.

## AD structures

This section allows you to define the payload for the advertising packets that are going to be broadcasted by the Bluetooth chip.

Currently, only 3 types are supported: 0x08 "Shortened Local Name"; 0x09 "Complete Local Name"; 0xFF "Manufacturer Specific Data".

You can check and set "AD structures" settings with the commands:

[?](https://help.mikrotik.com/docs/display/ROS/Bluetooth#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; iot bluetooth advertisers ad-structures print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NAME, TYPE, DATA</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros comments">#&nbsp; NAME&nbsp; TYPE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DATA</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">0&nbsp; test&nbsp; short-local-name&nbsp; TEST</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; iot bluetooth advertisers ad-structures </code><code class="ros functions">set</code></div></div></td></tr></tbody></table>

Configurable properties are shown below:

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

 |                                |
 | ------------------------------ | ------------------------------------------------------- |
 | **data** (_string_; Default: ) | Define advertising packet's AdvData part of the payload |
 | **name** (_string_; Default: ) | Descriptive name of AD structure                        |
 |                                |

**type** (complete-local-name | manufacturer-data | short-local-name; Default: )

 | 

An option to set AD structure's type:

-   0x08 "Shortened Local Name"
-   0x09 "Complete Local Name"
-   0xFF "Manufacturer Specific Data"

 |

If, for example, the "Shortened Local Name" type is chosen and the "data" field is configured with "TEST" → AdvData part of the payload is going to look like this:

05 08 54 45 53 54 (hexadecimal format)

, where the first octet (05) shows the number of bytes to follow (5 bytes) and the second octet (08) shows the type (Shortened Local Name). 3d, 4th, 5th and 6th (and etc) octets are the "data" \[54 (hex)=**T** (ASCII), 45 (hex)=**E** (ASCII), 53 (hex)=**S** (ASCII), 54 (hex)=**T** (ASCII)\].

The same applies to the "Complete Local Name" type. Only the second octet in the AdvData payload is going to differ and will be set to 09.

For the "Manufacturer Specific Data" type, you will need to configure the "data" field in the hexadecimal format. The second octet for this type is going to be set to FF.

## Scanners

In this menu, you can set up the scanner settings for the Bluetooth chip. When disabled, the device is no longer able to receive advertising reports. When enabled, you can monitor advertising reports in the "Advertising reports" tab (which will be explained later in the guide). You can check and set scanner settings with the commands:

[?](https://help.mikrotik.com/docs/display/ROS/Bluetooth#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; iot bluetooth scanners print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - DISABLED</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: DEVICE, TYPE, INTERVAL, WINDOW, OWN-ADDRESS-TYPE, FILTER-POLICY, FILTER-DUPL</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">ICATES</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros comments">#&nbsp;&nbsp; DEVICE&nbsp; TYPE&nbsp;&nbsp;&nbsp;&nbsp; INTERVAL&nbsp; WINDOW&nbsp; OWN-ADDRESS-TYPE&nbsp; FILTER-POLICY&nbsp; FIL</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">0 X bt1&nbsp;&nbsp;&nbsp;&nbsp; passive&nbsp; 10ms&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10ms&nbsp;&nbsp;&nbsp; random-static&nbsp;&nbsp;&nbsp;&nbsp; default&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; off</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot bluetooth scanners </code><code class="ros functions">set</code></div></div></td></tr></tbody></table>

Configurable properties are shown below:

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

 |                                    |
 | ---------------------------------- | --------------------- |
 | **disabled** (_yes                 | no_; Default: **no**) | An option to disable or enable the Bluetooth chip to receive advertising reports. |
 | **filter-duplicates** (keep-newest | keep-oldest           | off; Default: **off**)                                                            |

An option to discard duplicate advertisements from the same advertiser:

-   keep-newest → Keeps the newest report (discards the oldest). Only the newest PDU from a single AdvA will be kept.
-   keep-oldest → Keeps the oldest report (discards the newest). Only the oldest PDU from a single AdvA will be kept. This type of PDU filtering happens at the controller level and as such it's the most efficient (energy/bandwidth-wise) method of duplicate filtering.
-   off → Duplicates are not discarded. All PDUs with the same AdvA will be kept.

A duplicate advertising report is an advertising report sent from the same device address. The actual data ("AdvData" part of the payload) may change/differ and it is not considered significant when determining duplicate advertising reports. Meaning that, for example, if the Bluetooth interface receives 10 payloads (payload after payload with a 1-second interval) from the same tag:

-   if you are using the "keep-oldest" setting → Bluetooth interface will only display the first payload received (9 follow-up payloads will be filtered out) from that tag.  
    
-   if you are using the "keep-newest" setting → Bluetooth interface will only display the last payload received (each follow-up payload will rewrite the previous one) from that tag.







 |
| 

**filter-policy** (default | whitelist _| no_; Default: **default**)

 | 

An option to set up a filtering policy (controller-level advertisement filtering):

-   default → When this policy is enabled, the scanner will only accept ADV\_IND, ADV\_NOCONN\_IND, ADV\_SCAN\_IND, SCAN\_RSP, and ADV\_DIRECT\_IND (where TargetA is the scanner's own Bluetooth address) PDU types.
-   whitelist → When this policy is enabled, the scanner will only accept ADV\_IND, ADV\_NOCONN\_IND, ADV\_SCAN\_IND, SCAN\_RSP PDU types that are broadcasted by the advertiser, whose address is configured in the "Whitelist" section, and ADV\_DIRECT\_IND type PDU (where TargetA is the scanner's own Bluetooth address).

 |
| 

**interval** (_integer:3..10240_;__ Default: **10 ms**)

 | Time after which scanner will start scanning the next advertisement channel. |
| 

**own-address-type** (_public | random-static | rpa-fallback-to-public | rpa-fallback-to-random_; Default: **random-static**)

 | 

Address type used in scan requests (if active scanning type is used):

-   public →  To use the IEEE registered, permanent address.
-   random-static →  To use user-configurable address (will be changed on the next power-cycle).
-   rpa-fallback-to-public → To use Resolvable Random Private Address (RPA) that can only be resolved with our Identity Resolving Key (IRK). If RPA can not be generated, the public address will be used instead.
-   rpa-fallback-to-random → Same as "rpa-fallback-to-public" but if RPA can not be generated, the random-static address will be used instead.

 |
| 

**type** (_active | passive;_ Default: **passive**)

 | 

Defines the scanner's type:

-   active → Scanner can send scan requests if it receives a scannable advertisement. The scanner can send a SCAN\_REQ in order to acquire a SCAN\_RSP response.
-   passive → Scanner will only listen for advertisements, no data (e.g. scan requests) will be sent.

 |
| **window** (_integer:3..10240;_ Default: **10 ms**) | The time that the scanner will spend scanning a single advertisement channel. |

For example, if the scanner interval is set to 20ms, it means that only after 20ms, the device will begin scanning the next channel in line. If the scanner window is set to 10ms, it means that the device will scan each channel only during that 10ms window. Meaning, it will scan channel 37 for 10ms (window time) and begin scanning the next channel after 10 more ms (20ms\[interval\]-10ms\[window\]). It will take 10ms to scan channel 38, and after 10 more ms, the device will begin scanning channel 39.

## Advertising reports

In this section, it is possible to monitor Bluetooth advertising reports (from the nearby broadcasters). You can monitor advertising reports with the command:

[?](https://help.mikrotik.com/docs/display/ROS/Bluetooth#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; iot bluetooth scanners advertisements </code><code class="ros functions">print </code>&nbsp;&nbsp;&nbsp;&nbsp;</div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: DEVICE, PDU-TYPE, TIME, ADDRESS-TYPE, ADDRESS, RSSI</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments">#&nbsp; DEV&nbsp; PDU-TYPE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TIME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ADDRES&nbsp; ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; RSSI&nbsp;</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp; bt1&nbsp; adv-noconn-ind&nbsp; jul</code><code class="ros constants">/28/2021 09:30:56&nbsp; public&nbsp; 2C:C8:1B:93:16:49&nbsp; -24dBm</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1&nbsp; bt1&nbsp; adv-noconn-ind&nbsp; jul</code><code class="ros constants">/28/2021 09:30:56&nbsp; random&nbsp; 0B:16:17:9E:7B:EF&nbsp; -60dBm</code></div></div></td></tr></tbody></table>

It is possible to set up a filter for the reports with the command:

[?](https://help.mikrotik.com/docs/display/ROS/Bluetooth#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; iot bluetooth scanners advertisements </code><code class="ros functions">print </code><code class="ros plain">where</code></div></div></td></tr></tbody></table>

For example, to print reports that are broadcasted by a specific Bluetooth address, use the command:

[?](https://help.mikrotik.com/docs/display/ROS/Bluetooth#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; iot bluetooth scanners advertisements </code><code class="ros functions">print </code><code class="ros plain">where </code><code class="ros value">address</code><code class="ros plain">=XX:XX:XX:XX:XX:XX</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments"># DEVICE&nbsp;&nbsp;&nbsp; PDU-TYPE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TIME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ADD... ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; RSSI&nbsp;&nbsp;&nbsp;&nbsp; LENGTH DATA&nbsp;&nbsp;&nbsp;</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">79 bt1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; adv-noconn-ind jul</code><code class="ros constants">/28/2021 09:46:38 public XX:XX:XX:XX:XX:XX &nbsp; &nbsp; &nbsp; &nbsp;-70dBm&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 30 02010...</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">80 bt1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; adv-noconn-ind jul</code><code class="ros constants">/28/2021 09:46:43 public XX:XX:XX:XX:XX:XX &nbsp; &nbsp; &nbsp; &nbsp;-67dBm&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 30 02010...</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">81 bt1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; adv-noconn-ind jul</code><code class="ros constants">/28/2021 09:46:44 public XX:XX:XX:XX:XX:XX &nbsp; &nbsp; &nbsp; &nbsp;-70dBm&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 28 1bff0...</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">82 bt1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; adv-noconn-ind jul</code><code class="ros constants">/28/2021 09:46:48 public XX:XX:XX:XX:XX:XX &nbsp; &nbsp; &nbsp; &nbsp;-75dBm&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 30 02010...</code></div></div></td></tr></tbody></table>

To show only advertising reports that have RSSI stronger than -30 dBm, use the command:

[?](https://help.mikrotik.com/docs/display/ROS/Bluetooth#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; iot bluetooth scanners advertisements </code><code class="ros functions">print </code><code class="ros plain">where rssi &gt; -30</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments"># DEVICE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PDU-TYPE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TIME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ADDRESS-TYPE ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; RSSI&nbsp;&nbsp;&nbsp;&nbsp; LENGTH DATA&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">307 bt1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; adv-noconn-ind jul</code><code class="ros constants">/29/2021 10:11:31 public&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2C:C8:1B:93:16:49&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -24dBm&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 22 15ff4f09.&gt;</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">308 bt1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; adv-noconn-ind jul</code><code class="ros constants">/29/2021 10:11:31 public&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2C:C8:1B:93:16:49&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -26dBm&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 22 15ff4f09.&gt;</code></div></div></td></tr></tbody></table>

Possible filters (you can filter the list of advertising reports with the help of the following parameters):

| 
Filter

 | 

Description

 |     |
 | --- |  |
 |     |

Filter

 | 

Description

 |                  |
 | ---------------- | -------------------------------------------------------- |
 | **address**      | Bluetooth advertisers address                            |
 | **address-type** | Advertisers address type (for example, public or random) |
 |                  |

**data**

 | Advertisement data in hex format (AdvData payload) |
| **device** | Bluetooth chip/interface name |
| **epoch** | Milliseconds since Unix Epoch |
| **filter-comment** | Comment of the matching whitelist filter |
| **length** | Advertisement data length |
| **pdu-type** | Advertisement PDU type |
| **rssi** | Signal strength |
| **time** | Time of the advertisement packet reception |

## Whitelist

In this tab, it is possible to configure a whitelist that is going to be used in the filter policy in the "Scanners" section. In other words, an option to specify which Bluetooth addresses are going to be scanned (displayed in the "Advertising reports").

You can view the whitelisted entries with the command:

[?](https://help.mikrotik.com/docs/display/ROS/Bluetooth#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; iot bluetooth whitelist print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: DEVICE, ADDRESS-TYPE, ADDRESS</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros comments"># DEVICE&nbsp; ADDRESS-TYPE&nbsp; ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">0 bt1&nbsp;&nbsp;&nbsp;&nbsp; public&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 08</code><code class="ros constants">:55:31:CF:F3:9C</code></div></div></td></tr></tbody></table>

You can add a new whitelist entry with the command:

[?](https://help.mikrotik.com/docs/display/ROS/Bluetooth#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; iot bluetooth whitelist </code><code class="ros functions">add</code></div></div></td></tr></tbody></table>

Configurable properties:

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
 | -------------------------------------- | -------------------- |
 | **address** (_MAC address_; Default: ) | Advertiser's address |
 | **address-type** (_public              | random_; Default: )  | Advertiser's address type |
 |                                        |

**comment** (_string_; Default: )

 | Short description of the whitelisted entry |
| **copy-from** | An option to copy an entry - for more information check the [console documentation](https://wiki.mikrotik.com/wiki/Manual:Console#General_Commands) |
| **device** (_bt1_; Default: ) | Select the Bluetooth interface/chip name |
| **disabled** (_yes | no_; Default: ) | An option to disable or to enable the entry |

Only 8 whitelisted entries can be added.
