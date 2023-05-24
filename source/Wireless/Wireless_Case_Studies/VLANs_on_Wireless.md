# Summary

VLANs provide the possibility to isolate devices into different Layer2 segments while still using the same Layer1 medium. This is very useful in setups where you want to separate different types of devices of users. This feature is also very useful for Wireless setups since you can isolate different Virtual APs and restricting access to certain services or networks by using Firewall. Below is an example with a setup with two Access Points on the same device that isolates them into saparate VLANs. This kind of scenario is very common when you have a **Guest AP** and **Work AP**.

# Example

![](https://help.mikrotik.com/docs/download/attachments/122388507/Vlan-wlan1.jpg?version=1&modificationDate=1650965266847&api=v2)

[Bridge VLAN Filtering](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeVLANFiltering) since RouterOS v6.41 provides VLAN aware Layer2 forwarding and VLAN tag modifications within the bridge.

**R1:**

-   Add necessary VLAN interfaces on ethernet interface to make it a VLAN trunk port. Add ip addresses on VLAN interfaces.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@R1] &gt;</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface vlan</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">name</code><code class="ros plain">=vlan111</code> <code class="ros value">vlan-id</code><code class="ros plain">=111</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">name</code><code class="ros plain">=vlan222</code> <code class="ros value">vlan-id</code><code class="ros plain">=222</code></div><div class="line number5 index4 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.1.1/24</code> <code class="ros value">interface</code><code class="ros plain">=vlan111</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.2.1/24</code> <code class="ros value">interface</code><code class="ros plain">=vlan222</code></div></div></td></tr></tbody></table>

  

**R2:**

-   Add VirtualAP under wlan1 interface and create wireless security-profiles for wlan1 and wlan2

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@R2] &gt;</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface wireless</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[ </code><code class="ros functions">find </code><code class="ros value">default-name</code><code class="ros plain">=wlan1</code> <code class="ros plain">] </code><code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">mode</code><code class="ros plain">=ap-bridge</code> <code class="ros value">security-profile</code><code class="ros plain">=vlan111</code> <code class="ros value">ssid</code><code class="ros plain">=vlan111</code> <code class="ros value">vlan-id</code><code class="ros plain">=111</code> <code class="ros value">vlan-mode</code><code class="ros plain">=use-tag</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">master-interface</code><code class="ros plain">=wlan1</code> <code class="ros value">name</code><code class="ros plain">=wlan2</code> <code class="ros value">security-profile</code><code class="ros plain">=vlan222</code> <code class="ros value">ssid</code><code class="ros plain">=vlan222</code> <code class="ros value">vlan-id</code><code class="ros plain">=222</code> <code class="ros value">vlan-mode</code><code class="ros plain">=use-tag</code></div></div></td></tr></tbody></table>

  

It is important to set wlan1,wlan2 vlan-mode to "use-tag".

  

-   Create bridge with _vlan-filtering=yes_
-   Add necessary bridge ports
-   Add _tagged_ interfaces under _interface bridge vlan_ section with correct _vlan-ids_

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@R2] &gt;</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">fast-forward</code><code class="ros plain">=no</code> <code class="ros value">name</code><code class="ros plain">=bridge1</code> <code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=wlan1</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=wlan2</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether2,wlan1</code> <code class="ros value">vlan-ids</code><code class="ros plain">=111</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether2,wlan2</code> <code class="ros value">vlan-ids</code><code class="ros plain">=222</code></div></div></td></tr></tbody></table>

  

Some devices have a built-in switch chip that can switch packets between Ethernet ports with wire-speed performance. Bridge VLAN filtering disables hardware offloading (except on CRS3xx series switches), which will prevent packets from being switched, this does not affect Wireless interfaces as traffic through them cannot be offloaded to the switch chip either way.

  
  

VLAN filtering is not required in this setup, but is highly recommended due to security reasons. Without VLAN filtering it is possible to forward unknown VLAN IDs in certain scenarios. Disabling VLAN filtering does have performance benefits.

  

**R3:**

-   Add IP address on wlan1 interface.
-   Create wireless security-profile compatible with R2 wlan1.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@R3] &gt;</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.1.3/24</code> <code class="ros value">interface</code><code class="ros plain">=wlan1</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/interface wireless</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[ </code><code class="ros functions">find </code><code class="ros value">default-name</code><code class="ros plain">=wlan1</code> <code class="ros plain">] </code><code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">security-profile</code><code class="ros plain">=vlan111</code></div></div></td></tr></tbody></table>

**R4:**

-   Add IP address on wlan1 interface.
-   Create wireless security-profile compatible with R2 wlan2.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@R4] &gt;</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.2.4/24</code> <code class="ros value">interface</code><code class="ros plain">=wlan1</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/interface wireless</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[ </code><code class="ros functions">find </code><code class="ros value">default-name</code><code class="ros plain">=wlan1</code> <code class="ros plain">] </code><code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">security-profile</code><code class="ros plain">=vlan222</code></div></div></td></tr></tbody></table>