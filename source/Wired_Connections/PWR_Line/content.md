# Summary

The PWR-Line series devices allow Ethernet-like connectivity between supported devices over regular power lines. When plugged into the same electrical circuit, the PWR-Line devices will establish connectivity by using the HomePlug AV standard. 

# Properties

<table class="wrapped confluenceTable"><colgroup><col><col></colgroup><tbody><tr><td class="confluenceTd"><strong>arp</strong> (<em>disabled | enabled | proxy-arp | reply-only</em>; Default: <strong>enabled</strong>)</td><td class="confluenceTd">Address Resolution Protocol mode:<ul><li>disabled - the interface will not use ARP</li><li>enabled - the interface will use ARP</li><li>proxy-arp - the interface will use the ARP proxy feature</li><li>reply-only - the interface will only reply to requests originating from matching IP address/MAC address combinations which are entered as static entries in the "/ip arp" table. No dynamic entries will be automatically stored in the ARP table. Therefore for communications to be successful, a valid static entry must already exist.</li></ul></td></tr><tr><td class="confluenceTd"><strong>bandwidth</strong> (<em>integer/integer</em>; Default: <strong>unlimited/unlimited</strong>)</td><td class="confluenceTd">Sets max rx/tx bandwidth in kbps that will be handled by an interface. TX limit is supported on all Atheros <a href="https://help.mikrotik.com/docs/display/ROS/Switch+Chip+Features" rel="nofollow">switch-chip</a> ports. RX limit is supported only on Atheros8327/QCA8337 switch-chip ports.</td></tr><tr><td class="confluenceTd"><strong>comment</strong> (<em>string</em>; Default: )</td><td class="confluenceTd">Descriptive name of an item</td></tr><tr><td class="confluenceTd"><strong>l2mtu</strong> (<em>integer [0..65536]</em>; Default: )</td><td class="confluenceTd">Layer2 Maximum transmission unit. <a href="https://help.mikrotik.com/docs/display/ROS/MTU+in+RouterOS">MTU in RouterOS</a></td></tr><tr><td class="confluenceTd"><strong>mac-address</strong> (<em>MAC</em>; Default: )</td><td class="confluenceTd">Media Access Control number of an interface.</td></tr><tr><td class="confluenceTd"><strong>mtu</strong> (<em>integer [0..65536]</em>; Default: <strong>1500</strong>)</td><td class="confluenceTd">Layer3 Maximum transmission unit</td></tr><tr><td class="confluenceTd"><strong>name</strong> (<em>string</em>; Default: )</td><td class="confluenceTd">Name of an interface</td></tr><tr><td class="confluenceTd"><strong>orig-mac-address</strong> (<em>MAC</em>; Default: )</td><td class="confluenceTd"><br></td></tr><tr><td class="confluenceTd"><strong>rx-flow-control</strong> (<em>on | off | auto</em>; Default: <strong>off</strong>)</td><td class="confluenceTd">When set to on, the port will process received pause frames and suspend transmission if required. <strong>auto</strong> is the same as <strong>on</strong> except when auto-negotiation=yes flow control status is resolved by taking into account what the other end advertises. The feature is supported on AR724x, AR9xxx, and QCA9xxx CPU ports, all CCR ports, and all Atheros switch chip ports.</td></tr><tr><td class="confluenceTd"><strong>tx-flow-control</strong> (<em>on | off | auto</em>; Default: <strong>off</strong>)</td><td class="confluenceTd">When set to on, the port will send pause frames when specific buffer usage thresholds are met. <strong>auto</strong> is the same as <strong>on</strong> except when auto-negotiation=yes flow control status is resolved by taking into account what the other end advertises. The feature is supported on AR724x, AR9xxx, and QCA9xxx CPU ports, all CCR ports, and all Atheros switch chip ports.</td></tr></tbody></table>

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

|                         |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **configure** ()        | The command configures the attached PWR-Line device's network-key, network-password, plc-cco-selection-mode.                                                               |
| **join** ()             | Initiates the pairing sequence which will look for other PWR-Line devices in the same electrical circuit that is also in the pairing mode. This mode lasts for 60 seconds. |
| **leave** ()            | Initiates the leaving sequence which essentially randomizes the device's network-key.                                                                                      |
| **monitor** ()          | Outputs PWR-Line-related statuses in real-time.                                                                                                                            |
| **upgrade-firmware** () | Upgrades the PWR-Line device with specified firmware-file and pib-file files.                                                                                              |

# Configuration example

For two or more devices to be able to connect with each other, they must share the same network-key value. The currently configured network-key can be seen using the monitor command as plc-actual-network-key.

[?](https://help.mikrotik.com/docs/display/ROS/PWR+Line#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/interface pwr-line </code><code class="ros functions">monitor </code><code class="ros plain">pwr-line1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">name</code><code class="ros constants">: pwr-line1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">connection-to-plc</code><code class="ros constants">: ok</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">tx-flow-control</code><code class="ros constants">: no</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">rx-flow-control</code><code class="ros constants">: no</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">plc-actual-network-key</code><code class="ros constants">: c973947c200e1540b0f84b571d92bebe</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">plc-hw-platform</code><code class="ros constants">: QCA7420</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">plc-sw-platform</code><code class="ros constants">: MAC</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">plc-fw-version</code><code class="ros constants">: 1.4.0(24-20180515-CS)</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">plc-line-freq</code><code class="ros constants">: 50Hz</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">plc-zero-crossing</code><code class="ros constants">: detected</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">plc-mac</code><code class="ros constants">: B8:69:F4:C4:34:68</code></div></div></td></tr></tbody></table>

## Method 1

There are two ways to set the same network-key on different devices. You can either use the network-key parameter which is a hashed version of network-password parameter. Or use the network-password parameter and let the router apply the hash on a human-readable string.

For example:

[?](https://help.mikrotik.com/docs/display/ROS/PWR+Line#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface pwr-line configure pwr-line1 network-password=mynetwork</code></div></div></td></tr></tbody></table>

is the same as: 

[?](https://help.mikrotik.com/docs/display/ROS/PWR+Line#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface pwr-line configure pwr-line1 network-key=cb01fcc6167bf3d1edb1433c2ebde4b3</code></div></div></td></tr></tbody></table>

You must set the same key or password on all devices you wish to communicate with each other. 

## Method 2

It is possible to use the join and leave commands and make the PWR-Line devices automatically synchronize the network-key value. It is advised to use the leave command before using the join command to make sure a new network-key is randomly generated and the device is not part of any old network.

[?](https://help.mikrotik.com/docs/display/ROS/PWR+Line#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface pwr-line leave pwr-line1</code></div></div></td></tr></tbody></table>

Then we can issue the join command. When doing so, the pairing sequence is enabled for 60 seconds, meaning you have to enable pairing mode on another device within 60 seconds for them to successfully pair.

[?](https://help.mikrotik.com/docs/display/ROS/PWR+Line#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface pwr-line join pwr-line1</code></div></div></td></tr></tbody></table>

## Method 3

It is also possible to set a specified role for the PWR-Line device (master or slave) with the plc-cco-selection-mode parameter.

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
| --------------------------------- | ------ |
| **plc-cco-selection-mode** (_auto | always | never_; Default: **auto**) | Sets PWR-Line device mode: |

-   auto - PWR-Line will automatically decide what role to take depending on the situation upon joining a PWR-Line network.
-   always - PWR-Line will always be forced to act as "central-coordinator" or master device.
-   never - PWR-Line will always be forced to act as a slave device.

 |

Example: 

[?](https://help.mikrotik.com/docs/display/ROS/PWR+Line#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface pwr-line configure pwr-line1 plc-cco-selection-mode=auto</code></div></div></td></tr></tbody></table>

[?](https://help.mikrotik.com/docs/display/ROS/PWR+Line#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface pwr-line configure pwr-line1 plc-cco-selection-mode=always</code></div></div></td></tr></tbody></table>

[?](https://help.mikrotik.com/docs/display/ROS/PWR+Line#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface pwr-line configure pwr-line1 plc-cco-selection-mode=never</code></div></div></td></tr></tbody></table>

# Sync Button usage

-   Hold 0.5 – 3 seconds to turn on sync mode. For 120 seconds will try to communicate with another PWR-LINE device. A blinking orange LED light indicates that it is in search mode. You have to also do the same on the other PWR-LINE device, so they can synchronize. Press the button again to cancel the search. You can also manually set the security keys in RouterOS settings.

-   Hold 5 – 8 seconds to generate a new security key. This is needed to remove a PWR-LINE device from an existing PWR-LINE network.

-   Hold 10 – 15 seconds to reset all PWR-LINE related settings.

# Supported Hardware

The device is fully compatible with our PWR-LINE AP and the newest revisions of products that have a MicroUSB port, such as hAP lite, hAP lite tower, hAP mini, mAP, and mAP lite have a pwr-line interface. A simple software upgrade to v6.44+ enables this feature (supported by the mentioned devices with serial numbers that end with /9xx). PWR-LINE functionality is also supported by some previously manufactured units - if you have a unit with a serial number that ends with /8xx, upgrade to 6.44+ and see if the pwr-line interface shows up).