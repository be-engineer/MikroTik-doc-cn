The **device-mode** is a feature which sets specific limitations on a device, or limits access to specific configuration options.  
There are two available modes: _enterprise_ and _home_. By default, all devices use the mode _enterprise,_ which allows all functionality except _container_. The home mode disables the following features: _scheduler, socks, fetch, bandwidth-test, traffic-gen, sniffer, romon, proxy, hotspot, email, zerotier, container._

[?](https://help.mikrotik.com/docs/display/ROS/Device-mode#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; system</code><code class="ros constants">/device-mode/</code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">mode</code><code class="ros constants">: enterprise</code></div></div></td></tr></tbody></table>

The device mode can be changed by the user, but remote access to the device is not enough to change it. After changing the device-mode, you need to confirm it, by pressing a button on the device itself, or perform a "cold reboot" - that is, unplug the power.

[?](https://help.mikrotik.com/docs/display/ROS/Device-mode#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; system</code><code class="ros constants">/device-mode/update mode=home</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">update</code><code class="ros constants">: please activate by turning power off or pressing </code><code class="ros functions">reset </code><code class="ros variable">or</code> <code class="ros plain">mode button</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros variable">in</code> <code class="ros plain">5m00s</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">-- [Q quit|D dump|C-z pause]</code></div></div></td></tr></tbody></table>

If no power off or button press is performed within the specified time, the mode change is canceled. If another update command is run in parallel, both will be canceled. 

The following commands are available in the **system/device-mode/** menu: 

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

|     |
| --- |  |
|     |

get

 | 

Returns value that you can assign to variable or print on the screen.

 |
| print | Shows the active mode and its properties. |
| update | Applies changes to the specified properties, see below.  |

## List of available properties

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



|                                                                                                         |
| ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **container, fetch, scheduler, traffic-gen,                                                             |
| ipsec, pptp, smb, l2tp, proxy, sniffer, zerotier, bandwidth-test, email, hotspot, romon, socks.** (_yes | no_; Default: **yes**, for enterprise mode)                                                                                                                                                                          | The list of available features, which can be controlled with the **device-mode** option.                                                                                                                                                                                                                   |
| **activation-timeout** (default: **5m**);                                                               | The reset button or power off activation timeout can be set in range 00:00:10 .. 1d00:00:00. If the reset button is not pressed (or cold reboot is not performed) during this interval, the update will be canceled. |
| **flagging-enabled** (_yes                                                                              | no_; Default: **yes**)                                                                                                                                                                                               | Enable or disable the _flagged_ status. See below for a detailed description.                                                                                                                                                                                                                              |
| **flagged** (_yes                                                                                       | no_; Default: **no**)                                                                                                                                                                                                | RouterOS employs various mechanisms to detect tampering with it's system files. If the system has detected unauthorized access to RouterOS, the status "flagged" is set to yes. If "flagged" is set to yes, for your safety, certain limitations are put in place. See below chapter for more information. |
| **mode:** (home, enterprise; default: **enterprise**);                                                  | Allows choosing from available modes that will limit device functionality. In the future, various modes could be added.                                                                                              |

By default, **enterprise** mode allows all options except container. So to use the **container** feature, you will need to turn it on by performing a device-mode update.

By default, **home** mode disables the following features: **scheduler, socks, fetch, bandwidth-test, traffic-gen, sniffer, romon, proxy, hotspot, email, zerotier, container.**

 |

More specific control over the available features is possible. Each of the features controlled by device-mode can be specifically turned on or off, for example:

[?](https://help.mikrotik.com/docs/display/ROS/Device-mode#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; system</code><code class="ros constants">/device-mode/update mode=home email=yes</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; system</code><code class="ros constants">/device-mode/update mode=enterprise zerotier=no</code></div></div></td></tr></tbody></table>

If the update command specifies any of the mode parameters, this update replaces the entire device-mode configuration. In this case, all "per-feature" settings will be lost, except those specified with this command. For instance:

[?](https://help.mikrotik.com/docs/display/ROS/Device-mode#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; system</code><code class="ros constants">/device-mode/update mode=home email=yes fetch=yes</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; system</code><code class="ros constants">/device-mode/</code><code class="ros functions">print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">mode</code><code class="ros constants">: home</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">fetch</code><code class="ros constants">: yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">email</code><code class="ros constants">: yes</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; system</code><code class="ros constants">/device-mode/update mode=enterprise sniffer=no</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">-- reboot --</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; system</code><code class="ros constants">/device-mode/</code><code class="ros functions">print</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">mode</code><code class="ros constants">: enterprise</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">sniffer</code><code class="ros constants">: no</code></div></div></td></tr></tbody></table>

We see that fetch = yes and email = yes is missing, as they were overriden with the mode change. However, specifying only "per-feature" settings will change only those:

[?](https://help.mikrotik.com/docs/display/ROS/Device-mode#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; system</code><code class="ros constants">/device-mode/update hotspot=no</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">-- reboot --</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; system</code><code class="ros constants">/device-mode/</code><code class="ros functions">print</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">mode</code><code class="ros constants">: enterprise</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">sniffer</code><code class="ros constants">: no</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">hotspot</code><code class="ros constants">: no</code></div></div></td></tr></tbody></table>

If the feature is disabled, an error message is displayed for interactive commands:

[?](https://help.mikrotik.com/docs/display/ROS/Device-mode#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; system</code><code class="ros constants">/device-mode/</code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">mode</code><code class="ros constants">: enterprise</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">sniffer</code><code class="ros constants">: no</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">hotspot</code><code class="ros constants">: no</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; tool</code><code class="ros constants">/sniffer/quick</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">failure</code><code class="ros constants">: not allowed by device-mode</code></div></div></td></tr></tbody></table>

However, it is possible to add the configuration to a disabled feature, but there will be a comment showing the disabled feature in the device-mode:

[?](https://help.mikrotik.com/docs/display/ROS/Device-mode#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; ip hotspot</code><code class="ros constants">/</code><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; ip hotspot</code><code class="ros constants">/</code><code class="ros functions">print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X, S - HTTPS</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NAME, INTERFACE, PROFILE, IDLE-TIMEOUT</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros comments">#&nbsp;&nbsp; NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; INTERFACE&nbsp; PROFILE&nbsp; IDLE-TIMEOUT</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">;;; inactivated, not allowed by device-mode</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">0 X hotspot1&nbsp; ether1&nbsp;&nbsp;&nbsp;&nbsp; default&nbsp; 5m</code></div></div></td></tr></tbody></table>

# Flagged status

Along with the device-mode feature, RouterOS now can analyse the whole configuration at system startup, to determine if there are any signs of unauthorized access to your router. If suspicious configuration is detected, the suspicious configuration will be disabled and the **flagged** parameter will be set to "yes". The device has now a Flagged state and enforces certain limitations. 

[?](https://help.mikrotik.com/docs/display/ROS/Device-mode#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; system</code><code class="ros constants">/device-mode/</code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">mode</code><code class="ros constants">: enterprise</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">flagged</code><code class="ros constants">: yes</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">sniffer</code><code class="ros constants">: no</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">hotspot</code><code class="ros constants">: no</code></div></div></td></tr></tbody></table>

If the system has this flagged status, the current configuration works, but it is not possible to perform the following actions:   
  
bandwidth-test, traffic-generator, sniffer, as well as configuration actions that enable or create new configuration entries (it will still be possible to disable or delete them) for the following programs: _system scheduler, SOCKS proxy, pptp, l2tp, ipsec, proxy, smb_.  
  
When performing the aforementioned actions while the router has the flagged state, you will receive an error message:

[?](https://help.mikrotik.com/docs/display/ROS/Device-mode#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/tool sniffer/quick</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">failure</code><code class="ros constants">: configuration flagged, check all router configuration </code><code class="ros functions">for </code><code class="ros plain">unauthorized changes </code><code class="ros variable">and</code> <code class="ros plain">update device-mode</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/int l2tp-client/</code><code class="ros functions">add </code><code class="ros value">connect-to</code><code class="ros plain">=1.1.1.1</code> <code class="ros value">user</code><code class="ros plain">=user</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">failure</code><code class="ros constants">: configuration flagged, check all router configuration </code><code class="ros functions">for </code><code class="ros plain">unauthorized changes </code><code class="ros variable">and</code> <code class="ros plain">update device-mode</code></div></div></td></tr></tbody></table>

To exit the flagged state, you must perform the command "/system/device-mode/update flagged=no". The system will ask to either press a button, or issue a hard reboot (cut power physically or do a hard reboot of the virtual machine).   
  
**Important!** Although the system has disabled any malicious looking rules, which triggered the flagged state, it is crucial to inspect all of your configuration for other unknown things, before exiting the flagged state. If your system has been flagged, assume that your system has been compromised and do a full audit of all settings before re-enabling the system for use. After completing the audit, change all the system passwords and upgrade to the latest RouterOS version.