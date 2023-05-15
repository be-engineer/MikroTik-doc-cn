# Overview

The WifiWave2 package contains software for managing compatible 802.11ax and 802.11ac wave 2 wireless interfaces.  
Builds for x86, ppc, mmips and tile architectures contain the configuration utilities needed to centrally manage interfaces (as a CAPsMAN controller). Builds for arm and arm64 also contain interface drivers and firmware.

The package can be downloaded as part of the ['Extra Packages' archive](https://mikrotik.com/download).

The WifiWave2 package in RouterOS adds certain Wave2 features, and 802.11ax devices require it. Some products which ship with the standard 'wireless' package, can replace it with wifiwave2, for more details, please see this [section](https://help.mikrotik.com/docs/display/ROS/WifiWave2#WifiWave2-Replacingstockwireless).

Configuration in the command line is done under /interface/wifiwave2/, when using a graphical configuration tool (WinBox or WebFig), wifiwave2 interfaces can be configured using either the 'Wireless' or 'QuickSet' tabs.

# WifiWave2 Terminology

Before we move on let's familiarise ourselves with terms important for understanding the operation of the WifiWave2. These terms will be used throughout the article.

-   **Profile** - refers to the configuration preset created under one of this WifiWave2 sub-menus: **aaa**, **channel**, **security**, **datapath**, or **interworking**. 
-   **Configuration** **profile** - configuration preset defined under /interface/wifiwave2/configuration, it can reference various profiles.
-   **Station** - wireless client.

# Basic Configuration:

**Basic password-protected AP**

[?](https://help.mikrotik.com/docs/display/ROS/WifiWave2#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wifiwave2</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">wifi1 </code><code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">configuration.country</code><code class="ros plain">=Latvia</code> <code class="ros value">configuration.ssid</code><code class="ros plain">=MikroTik</code> <code class="ros value">security.authentication-types</code><code class="ros plain">=wpa2-psk,wpa3-psk</code> <code class="ros value">security.passphrase</code><code class="ros plain">=8-63_characters</code></div></div></td></tr></tbody></table>

  

**Open AP with OWE transition mode**

Opportunistic wireless encryption (OWE) allows the creation of wireless networks that do not require the knowledge of a password to connect, but still offer the benefits of traffic encryption and management frame protection. It is an improvement on regular open access points.

However, since a network cannot be simultaneously encrypted and unencrypted, 2 separate interface configurations are required to offer connectivity to older devices that do not support OWE and offer the benefits of OWE to devices that do.

This configuration is referred to as OWE transition mode.

[?](https://help.mikrotik.com/docs/display/ROS/WifiWave2#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wifiwave2</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">master-interface</code><code class="ros plain">=wifi1</code> <code class="ros value">name</code><code class="ros plain">=wifi1_owe</code> <code class="ros value">configuration.ssid</code><code class="ros plain">=MikroTik_OWE</code> <code class="ros value">security.authentication-types</code><code class="ros plain">=owe</code> <code class="ros value">security.owe-transition-interface</code><code class="ros plain">=wifi1</code> <code class="ros value">configuration.hide-ssid</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">wifi1 </code><code class="ros value">configuration.country</code><code class="ros plain">=Latvia</code> <code class="ros value">configuration.ssid</code><code class="ros plain">=MikroTik</code> <code class="ros value">security.authentication-types</code><code class="ros plain">=</code><code class="ros string">""</code> <code class="ros value">security.owe-transition-interface</code><code class="ros plain">=wifi1_owe</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">enable </code><code class="ros plain">wifi1,wifi1_owe</code></div></div></td></tr></tbody></table>

Client devices that support OWE will prefer the OWE interface. If you don't see any devices in your registration table that are associating with the regular open AP, you may want to move on from running a transition mode setup to a single OWE-encrypted interface.

**Resetting configuration**

WifiWave2 interface configurations can be reset by using the 'reset' command.

[?](https://help.mikrotik.com/docs/display/ROS/WifiWave2#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wifiwave2 </code><code class="ros functions">reset </code><code class="ros plain">wifi1</code></div></div></td></tr></tbody></table>

# Configuration profiles

One of the new WifiWave2 additions is configuration profiles, you can create various presets, that can be assigned to interfaces as needed. Configuration settings for WifiWave2 are grouped in **profiles** according to the parameter sections found at end of this page - **aaa**, **channel**, **configuration**, **datapath**, **interworking**, and **security**, and can then be assigned to interfaces. **Configuration** **profiles** can include other profiles as well as separate parameters from other categories.

This optional flexibility is meant to allow each user to arrange their configuration in a way that makes the most sense for them, but it also means that each parameter may have different values assigned to it in different sections of the configuration.

The following priority determines, which value is used:

1.  Value in interface settings
2.  Value in a profile assigned to interface
3.  Value in configuration profile assigned to interface
4.  Value in a profile assigned to configuration profile (which in turn is assigned to interface).

If you are at any point unsure of which parameter value will be used for an interface, consult the **actual-configuration** menu. For an example of configuration profile usage, see the following example.

**Example for dual-band home AP**

[?](https://help.mikrotik.com/docs/display/ROS/WifiWave2#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros comments"># Creating a security profile, which will be common for both interfaces</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface wifiwave2 security</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=common-auth</code> <code class="ros value">authentication-types</code><code class="ros plain">=wpa2-psk,wpa3-psk</code> <code class="ros value">passphrase</code><code class="ros plain">=</code><code class="ros string">"diceware makes good passwords"</code> <code class="ros value">wps</code><code class="ros plain">=disable</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments"># Creating a common configuration profile and linking the security profile to it</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/interface wifiwave2 configuration</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=common-conf</code> <code class="ros value">ssid</code><code class="ros plain">=MikroTik</code> <code class="ros value">country</code><code class="ros plain">=Latvia</code> <code class="ros value">security</code><code class="ros plain">=common-auth</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros comments"># Creating separate channel configurations for each band</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros constants">/interface wifiwave2 channel</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ch-2ghz</code> <code class="ros value">frequency</code><code class="ros plain">=2412,2432,2472</code> <code class="ros value">width</code><code class="ros plain">=20mhz</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ch-5ghz</code> <code class="ros value">frequency</code><code class="ros plain">=5180,5260,5500</code> <code class="ros value">width</code><code class="ros plain">=20/40/80mhz</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros comments"># Assigning to each interface the common profile as well as band-specific channel profile</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros constants">/interface wifiwave2</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">wifi1 </code><code class="ros value">channel</code><code class="ros plain">=ch-2ghz</code> <code class="ros value">configuration</code><code class="ros plain">=common-conf</code> <code class="ros value">disabled</code><code class="ros plain">=no</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">wifi2 </code><code class="ros value">channel</code><code class="ros plain">=ch-5ghz</code> <code class="ros value">configuration</code><code class="ros plain">=common-conf</code> <code class="ros value">disabled</code><code class="ros plain">=no</code></div><div class="line number15 index14 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros constants">/interface/wifiwave2/actual-configuration </code><code class="ros plain">print</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0 </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"wifi1"</code> <code class="ros value">mac-address</code><code class="ros plain">=74:4D:28:94:22:9A</code> <code class="ros value">arp-timeout</code><code class="ros plain">=auto</code> <code class="ros value">radio-mac</code><code class="ros plain">=74:4D:28:94:22:9A</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros value">configuration.ssid</code><code class="ros plain">=</code><code class="ros string">"MikroTik"</code> <code class="ros plain">.</code><code class="ros value">country</code><code class="ros plain">=Latvia</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros value">security.authentication-types</code><code class="ros plain">=wpa2-psk,wpa3-psk</code> <code class="ros plain">.</code><code class="ros value">passphrase</code><code class="ros plain">=</code><code class="ros string">"diceware makes good passwords"</code> <code class="ros plain">.</code><code class="ros value">wps</code><code class="ros plain">=disable</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros value">channel.frequency</code><code class="ros plain">=2412,2432,2472</code> <code class="ros plain">.</code><code class="ros value">width</code><code class="ros plain">=20mhz</code></div><div class="line number21 index20 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1 </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"wifi2"</code> <code class="ros value">mac-address</code><code class="ros plain">=74:4D:28:94:22:9B</code> <code class="ros value">arp-timeout</code><code class="ros plain">=auto</code> <code class="ros value">radio-mac</code><code class="ros plain">=74:4D:28:94:22:9B</code>&nbsp;&nbsp;</div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros value">configuration.ssid</code><code class="ros plain">=</code><code class="ros string">"MikroTik"</code> <code class="ros plain">.</code><code class="ros value">country</code><code class="ros plain">=Latvia</code></div><div class="line number24 index23 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros value">security.authentication-types</code><code class="ros plain">=wpa2-psk,wpa3-psk</code> <code class="ros plain">.</code><code class="ros value">passphrase</code><code class="ros plain">=</code><code class="ros string">"diceware makes good passwords"</code> <code class="ros plain">.</code><code class="ros value">wps</code><code class="ros plain">=disable</code></div><div class="line number25 index24 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros value">channel.frequency</code><code class="ros plain">=5180,5260,5500</code> <code class="ros plain">.</code><code class="ros value">width</code><code class="ros plain">=20/40/80mhz</code></div></div></td></tr></tbody></table>

# Access List

The access list provides multiple ways of filtering and managing wireless connections.

RouterOS will check each new connection to see if its parameters match the parameters specified in any access list rule.

The rules are checked in the order they appear in the list. Only management actions specified in the first matching rule are applied to each connection.

Connections, which have been accepted by an access list rule, will be periodically checked, to see if they remain within the permitted **time** and **signal-range**. If they do not, they will be terminated.

Take care when writing access list rules which reject clients. After being repeatedly rejected by an AP, a client device may start avoiding it.

The access list has two kinds of parameters - [filtering](https://help.mikrotik.com/docs/display/ROS/WifiWave2#WifiWave2-filtering), and [action](https://help.mikrotik.com/docs/display/ROS/WifiWave2#WifiWave2-action). Filtering properties are only used for matching clients, to whom the access list rule should be applied to. Action parameters can change connection parameters for that specific client and potentially overriding its default connection parameters with ones specified in the access list rule.

## MAC address authentication

Implemented through the **query-radius** action, MAC address authentication is a way to implement a centralized whitelist of client MAC addresses using a RADIUS server.

When a client device tries to associate with an AP, which is configured to perform MAC address authentication, the AP will send an access-request message to a RADIUS server with the device's MAC address as the user name and an empty password. If the RADIUS server answers with access-accept to such a request, the AP proceeds with whatever regular authentication procedure (passphrase or EAP authentication) is configured for the interface.

## Access rule examples

Only accept connections to guest network from nearby devices during business hours

[?](https://help.mikrotik.com/docs/display/ROS/WifiWave2#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wifiwave2/access-list/</code><code class="ros functions">print </code><code class="ros plain">detail</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disab</code><code class="ros plain">led</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;&nbsp; </code><code class="ros value">signal-range</code><code class="ros plain">=-60..0</code> <code class="ros value">allow-signal-out-of-range</code><code class="ros plain">=5m</code> <code class="ros value">ssid-regexp</code><code class="ros plain">=</code><code class="ros string">"MikroTik Guest"</code> <code class="ros value">time</code><code class="ros plain">=7h-19h,mon,tue,wed,thu,fri</code> <code class="ros value">action</code><code class="ros plain">=accept</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1&nbsp;&nbsp; </code><code class="ros value">ssid-regexp</code><code class="ros plain">=</code><code class="ros string">"MikroTik Guest"</code> <code class="ros value">action</code><code class="ros plain">=reject</code></div></div></td></tr></tbody></table>

Reject connections from locally-administered ('anonymous'/'randomized') MAC addresses

[?](https://help.mikrotik.com/docs/display/ROS/WifiWave2#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wifiwave2/access-list/</code><code class="ros functions">print </code><code class="ros plain">detail</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disab</code><code class="ros plain">led</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;&nbsp; </code><code class="ros value">mac-address</code><code class="ros plain">=02:00:00:00:00:00</code> <code class="ros value">mac-address-mask</code><code class="ros plain">=02:00:00:00:00:00</code> <code class="ros value">action</code><code class="ros plain">=reject</code></div></div></td></tr></tbody></table>

Assigning a different passphrase for a specific client can be useful, if you need to provide wireless access to a client, but don't want to share your wireless password, or don't want to create a separate SSID. When the matching client will connect to this network, instead of using the password defined in the interface configuration, the access list will make that client use a different password. Just make that the specific client doesn't get matched by a more generic access list rule first.

[?](https://help.mikrotik.com/docs/display/ROS/WifiWave2#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface wifiwave2 access-list</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">mac-address</code><code class="ros plain">=22:F9:70:E5:D2:8E</code> <code class="ros value">interface</code><code class="ros plain">=wifi1</code> <code class="ros value">passphrase</code><code class="ros plain">=StrongPassword</code></div></div></td></tr></tbody></table>

# Frequency scan

The '/interface/wifiwave2/frequency-scan wifi1' command provides information about RF conditions on available channels that can be obtained by running the frequency-scan command. Used to approximate the spectrum usage, it can be useful to find less crowded frequencies.

![](https://help.mikrotik.com/docs/download/attachments/46759946/image-2023-3-10_18-6-37.png?version=1&modificationDate=1678464582039&api=v2)

Running a frequency scan will disconnect all connected clients, or if the interface is in station mode, it will disconnect from AP.

# Scan command

The '/interface wifiwave2 scan' command will scan for access points and print out information about any APs it detects. It doesn't show the frequency usage, per channel, but it will reveal all access points that are transmitting. You can use the "connect" button, to initiate a connection to a specific AP.

The scan command takes all the same parameters as the frequency-scan command.

![](https://help.mikrotik.com/docs/download/attachments/46759946/image-2023-3-10_18-16-42.png?version=1&modificationDate=1678465186656&api=v2)

# Sniffer

The sniffer command enables monitor mode on a wireless interface. This turns the interface into a passive receiver for all WiFi transmissions.  
The command continuously prints out information on received packets and can save them locally to a pcap file or stream them using the TZSP protocol.

The sniffer will operate on whichever channel is configured for the chosen interface.

![](https://help.mikrotik.com/docs/download/attachments/46759946/wave2_sniffer.png?version=2&modificationDate=1679904643347&api=v2)

# WPS

## WPS client

The wps-client command enables obtaining authentication information from a WPS-enabled AP.

[?](https://help.mikrotik.com/docs/display/ROS/WifiWave2#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wifiwave2/</code><code class="ros functions">wps-client </code><code class="ros plain">wifi1</code></div></div></td></tr></tbody></table>

## WPS server

An AP can be made to accept WPS authentication by a client device for 2 minutes by running the following command.

[?](https://help.mikrotik.com/docs/display/ROS/WifiWave2#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wifiwave2 </code><code class="ros functions">wps-push-button </code><code class="ros plain">wifi1</code></div></div></td></tr></tbody></table>

# Radios

Information about the capabilities of each radio can be gained by running the \`/interface/wifiwave2/radio print detail\` command.  It can be useful to see what bands are supported by the interface and what channels can be selected. The country profile that is applied to the interface will influence the results.

[?](https://help.mikrotik.com/docs/display/ROS/WifiWave2#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">interface</code><code class="ros constants">/wifiwave2/radio/</code><code class="ros functions">print </code><code class="ros functions">detail</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: L - </code><code class="ros functions">local</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0 L </code><code class="ros value">radio-mac</code><code class="ros plain">=48:A9:8A:0B:F7:4A</code> <code class="ros value">phy-id</code><code class="ros plain">=0</code> <code class="ros value">tx-chains</code><code class="ros plain">=0,1</code> <code class="ros value">rx-chains</code><code class="ros plain">=0,1</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">bands</code><code class="ros plain">=5ghz-a:20mhz,5ghz-n:20mhz,20/40mhz,5ghz-ac:20mhz,20/40mhz,20/40/80mhz,5ghz-ax:20mhz,</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">20</code><code class="ros constants">/40mhz,20/40/80mhz</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">ciphers</code><code class="ros plain">=tkip,ccmp,gcmp,ccmp-256,gcmp-256,cmac,gmac,cmac-256,gmac-256</code> <code class="ros value">countries</code><code class="ros plain">=all</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">5g-channels</code><code class="ros plain">=5180,5200,5220,5240,5260,5280,5300,5320,5500,5520,5540,5560,5580,5600,5620,5640,5660,</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">5680,5700,5720,5745,5765,5785,5805,5825</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">max-vlans</code><code class="ros plain">=128</code> <code class="ros value">max-interfaces</code><code class="ros plain">=16</code> <code class="ros value">max-station-interfaces</code><code class="ros plain">=3</code> <code class="ros value">max-peers</code><code class="ros plain">=120</code> <code class="ros value">hw-type</code><code class="ros plain">=</code><code class="ros string">"QCA6018"</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">hw-caps</code><code class="ros plain">=sniffer</code> <code class="ros value">interface</code><code class="ros plain">=wifi1</code> <code class="ros value">current-country</code><code class="ros plain">=Latvia</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">current-channels</code><code class="ros plain">=5180/a,5180/n,5180/n/Ce,5180/ac,5180/ac/Ce,5180/ac/Ceee,5180/ax,5180/ax/Ce,</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">5180</code><code class="ros constants">/ax/Ceee,5200/a,5200/n,5200/n/eC,5200/ac,5200/ac/eC,5200/ac/eCee,5200/ax...</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">...5680</code><code class="ros constants">/n/eC,5680/ac,5680/ac/eC,5680/ax,5680/ax/eC,5700/a,5700/n,5700/ac,5700/ax</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">current-gopclasses</code><code class="ros plain">=115,116,128,117,118,119,120,121,122,123</code> <code class="ros value">current-max-reg-power</code><code class="ros plain">=30</code></div></div></td></tr></tbody></table>

While Radio information gives us information about supported channel width, it is also possible to deduce this information from the product page, to do so you need to check the following parameters: **number of chains**, **max data rate**. Once you know these parameters, you need to check the modulation and coding scheme (MCS) table, for example, here: [https://mcsindex.com/](https://mcsindex.com/).

If we take hAP ax<sup>2</sup>, as an example, we can see that number of chains is 2, and the max data rate is 1200 - 1201 in the MCS table. In the MCS table we need to find entry for 2 spatial streams - chains, and the respective data rate, which in this case shows us that 80MHz is the maximum supported channel width.

# Registration table

'/interface/wifiwave2/registration-table/' displays a list of connected wireless clients and detailed information about them.

![](https://help.mikrotik.com/docs/download/attachments/46759946/image-2023-3-10_18-29-11.png?version=1&modificationDate=1678465935336&api=v2)

## De-authentication

Wireless peers can be manually de-authenticated (forcing re-association) by removing them from the registration table.

[?](https://help.mikrotik.com/docs/display/ROS/WifiWave2#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wifiwave2/registration-table </code><code class="ros functions">remove </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros plain">where </code><code class="ros value">mac-address</code><code class="ros plain">=02:01:02:03:04:05]</code></div></div></td></tr></tbody></table>

# WifiWave2 CAPsMAN

WifiWave2 CAPsMAN allows applying wireless settings to multiple MikroTik WifiWave2 AP devices from a central configuration interface.

More specifically, the Controlled Access Point system Manager (CAPsMAN) allows the centralization of wireless network management. When using the CAPsMAN feature, the network will consist of a number of 'Controlled Access Points' (CAP) that provide wireless connectivity and a 'system Manager' (CAPsMAN) that manages the configuration of the APs, it also takes care of client authentication.

WifiWave2 CAPsMAN only passes wireless configuration to the CAP, all forwarding decisions are left to the CAP itself - there is no CAPsMAN forwarding mode.

Requirements:

-   Any RouterOS device, that supports the WifiWave2 package, can be a controlled wireless access point (CAP) as long as it has at least a Level 4 RouterOS license.
-   WifiWave2 CAPsMAN server can be installed on any RouterOS device that supports the WifiWave2 package, even if the device itself does not have a wireless interface
-   Unlimited CAPs (access points) supported by CAPsMAN

WifiWave2 CAPsMAN can only control WifiWave2 interfaces, and WifiWave2 CAPs can join only WifiWave2 CAPsMAN, similarly, regular CAPsMAN only supports non-WifiWave2 caps.

## CAPsMAN - CAP configuration example:

CAPsMAN in WifiWave2 uses the same menu as a regular WifiWave2 interface, meaning when you pass configuration to CAPs, you have to use the same configuration, security, channel configuration, etc. as you would for regular WifiWave2 interfaces.

You can configure sub configuration menus, directly under "/interface/wifiwave2/configuration" or reference previously created profiles in the main configuration profile

CAPsMAN:

[?](https://help.mikrotik.com/docs/display/ROS/WifiWave2#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros comments">#create a security profile</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface wifiwave2 security</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">authentication-types</code><code class="ros plain">=wpa3-psk</code> <code class="ros value">name</code><code class="ros plain">=sec1</code> <code class="ros value">passphrase</code><code class="ros plain">=HaveAg00dDay</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros comments">#create configuraiton profiles to use for provisioning</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/interface wifiwave2 configuration</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">country</code><code class="ros plain">=Latvia</code> <code class="ros value">name</code><code class="ros plain">=5ghz</code> <code class="ros value">security</code><code class="ros plain">=sec1</code> <code class="ros value">ssid</code><code class="ros plain">=CAPsMAN_5</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=2ghz</code> <code class="ros value">security</code><code class="ros plain">=sec1</code> <code class="ros value">ssid</code><code class="ros plain">=CAPsMAN2</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">country</code><code class="ros plain">=Latvia</code> <code class="ros value">name</code><code class="ros plain">=5ghz_v</code> <code class="ros value">security</code><code class="ros plain">=sec1</code> <code class="ros value">ssid</code><code class="ros plain">=CAPsMAN5_v</code></div><div class="line number10 index9 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros comments">#configure provisioning rules, configure band matching as needed</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros constants">/interface wifiwave2 provisioning</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=create-dynamic-enabled</code> <code class="ros value">master-configuration</code><code class="ros plain">=5ghz</code> <code class="ros value">slave-configurations</code><code class="ros plain">=5ghz_v</code> <code class="ros value">supported-bands</code><code class="ros plain">=\</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">5ghz-n</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=create-enabled</code> <code class="ros value">master-configuration</code><code class="ros plain">=2ghz</code> <code class="ros value">supported-bands</code><code class="ros plain">=2ghz-n</code></div><div class="line number16 index15 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros comments">#enable CAPsMAN service</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros constants">/interface wifiwave2 capsman</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">ca-certificate</code><code class="ros plain">=auto</code> <code class="ros value">enabled</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

CAP:

[?](https://help.mikrotik.com/docs/display/ROS/WifiWave2#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros comments">#enable CAP service, in this case CAPsMAN is on same LAN, but you can also specify "caps-man-addresses=x.x.x.x" here</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/interface/wifiwave2/cap </code><code class="ros functions">set </code><code class="ros value">enabled</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments">#set configuration.manager= on the WifiWave2 interface that should act as CAP</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wifiwave2/</code><code class="ros functions">set </code><code class="ros plain">wifi1,wifi2 </code><code class="ros value">configuration.manager</code><code class="ros plain">=capsman-or-local</code></div></div></td></tr></tbody></table>

If the CAP is hAP ax<sup>2</sup> or hAP ax<sup>3</sup>, it is strongly recommended to enable RSTP in the bridge configuration, on the CAP

configuration.manager should only be set on the CAP device itself, don't pass it to the CAP vai configuration profile that you provision.

The interface that should act as CAP needs additional configuration under "interface/wifiwave2/set wifiX configuration.manager="

# Advanced examples

[Enterprise wireless security with User Manager v5](https://help.mikrotik.com/docs/display/ROS/Enterprise+wireless+security+with+User+Manager+v5)

Assigning VLAN tags to wireless traffic can be achieved by following the [generic VLAN configuration example here](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-VLANExample-TrunkandAccessPorts).

# Replacing stock wireless

The wifiwave2 package can be installed on some products, which ship with the bundled 'wireless' package, replacing it.

Installing the wifiwave2 package disables other means of configuring wireless interfaces. Before installation, make sure to back up any wireless and regular CAPsMAN configuration you may want to retain.  

## Compatibility

Due to storage, RAM, and architecture requirements, only the following products can replace their bundled wireless software package with wifiwave2:

-   hAP ac³ (non-LTE)
-   Audience and Audience LTE6 kit
-   RB4011iGS+5HacQ2HnD\*

\* The 2.4GHz wireless interface on the RB4011iGS+5HacQ2HnD is not compatible with the wifiwave2 package. It will not be usable with the package installed.

## Benefits

-   WPA3 authentication and OWE (opportunistic wireless encryption)
-   802.11w standard management frame protection
-   802.11r/k
-   MU-MIMO and beamforming
-   400Mb/s maximum data rate in the 2.4GHz band for IPQ4019 interfaces
-   OFDMA

## Lost features

The following notable features of the bundled wireless package do not yet have equivalents in the wifiwave2 package

-   Station-bridging or other 4-address modes
-   Nstreme and Nv2 wireless protocols

# Property Reference

## AAA properties

Properties in this category configure an access point's interaction with AAA (RADIUS) servers.

Certain parameters in the table below take _format-string_ as their value. In a _format-string_, certain characters are interpreted in the following way:

| 
Character

 | 

Interpretation

|     |
| --- |  |
|     |

Character

 | 

Interpretation

|                 |
| --------------- | ----------------------------------------------------------------------------------- |
| a               | Hexadecimal character making up the MAC address of the client device in lower case  |
| A               | Hexadecimal character making up the MAC address of the client device in upper case  |
| i               | Hexadecimal character making up the MAC address of the AP's interface in lower case |
| I (capital 'i') | Hexadecimal character making up the MAC address of the AP's interface in upper case |
| N               | The entire name of the AP's interface (e.g. 'wifi1')                                |
| S               | The entire SSID                                                                     |

All other characters are used without interpreting them in any way. For examples, see default values.

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



|                                     |
| ----------------------------------- |  |
| **called-format** (_format-string_) |

Format for the value of the Called-Station-Id RADIUS attribute, in AP's messages to RADIUS servers. Default: II-II-II-II-II-II:S

 |
| **calling-format** (_format-string_) | Format for the value of the Calling-Station-Id RADIUS attribute, in AP's messages to RADIUS servers. Default: AA-AA-AA-AA-AA-AA |
| **interim-update** (_time interval)_ | Interval at which to send interim updates about traffic accounting to the RADIUS server. Default: 5m |
| **mac-caching** (_time interval_ | _'disabled'_) | 

Length of time to cache RADIUS server replies, when MAC address authentication is enabled.  
This resolves issues with client device authentication timing out due to (comparatively high latency of RADIUS server replies.

Default value: disabled.

 |
| **name** (_string_) | A unique name for the AAA profile. No default value. |
| **nas-identifier** (_string_) |  Value of the NAS-Identifier attribute, in AP's messages to RADIUS servers. Defaults to the host name of the device (/system/identity). |
| **password-format** (_format-string_) | 

Format for value to use in calculating the value of the User-Password attribute in AP's messages to RADIUS servers when performing MAC address authentication.

Default value: "" (an empty string).

 |
| **username-format** (_format-string_) | 

Format for the value of the User-Name attribute in APs messages to RADIUS servers when performing MAC address authentication.

Default value : `AA:AA:AA:AA:AA:AA`

 |

## Channel properties

Properties in this category specify the desired radio channel.

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

|                    |
| ------------------ | -------- |
| **band** (_2ghz-g_ | _2ghz-n_ | _2ghz-ax_ | _5ghz-a_ | _5ghz-ac_ | _5ghz-an_ | _5ghz-ax_) |

Supported frequency band and wireless standard. Defaults to newest supported standard.  
**Note that band support is limited by radio capabilities.**



 |
| **frequency** (_list of integers or integer ranges_) | 

For an interface in AP mode, specifies frequencies (in MHz) to consider when picking control channel center frequency.

For an interface in station mode, specifies frequencies on which to scan for APs.

Leave unset (default) to consider all frequencies supported by the radio and permitted by the applicable regulatory profille.

The parameter can contain 1 or more comma-separated values of integers or, optionally, ranges of integers denoted using the syntax RangeBeginning-RangeEnd:RangeStep

Examples of valid channel.frequency values:

-   2412
-   2412,2432,2472
-   5180-5240:20,5500-5580:20



 |
| **secondary-frequency** (_list of integers_ | 'disabled')  | 

Frequency (in MHz) to use for the center of the secondary part of a split 80+80MHz channel.

Only [official 80MHz channels](https://en.wikipedia.org/wiki/List_of_WLAN_channels#5_GHz_(802.11a/h/j/n/ac/ax)) (5210, 5290, 5530, 5610, 5690, 5775) are supported.

Leave unset (default) for automatic selection of secondary channel frequency.

 |
| **skip-dfs-channels**  (_10min-cac_ | _all_ | _disabled_) | 

Whether to avoid using channels, on which channel availability check (listening for presence of radar signals) is required.

-   _10min-cac_ - interface will avoid using channels, on which 10 minute long CAC is required
-   _all_ \- interface will avoid using all channels, on which CAC is required
-   _disabled_ (default) - interface may select any supported channel, regardless of CAC requirements

 |
| **width** ( _20mhz_ | _20/40mhz_ | _20/40mhz-Ce_ | _20/40mhz-eC_ | _20/40/80mhz_ | _20/40/80+80mhz_ |  _20/40/80/160mhz_) | 

Width of radio channel. Defaults to widest channel supported by the radio hardware.

 |

## Configuration properties

This section includes properties relating to the operation of the interface and the associated radio.

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

**antenna-gain** (_integer 0..30_)

 | 

Overrides the default antenna gain. The _master_ interface of each radio sets the antenna gain for every interface which uses the same radio.

This setting cannot override the antenna gain to be lower than the minimum antenna gain of a radio.  
No default value.



 |
| 

**beacon-interval** (_time interval 100ms..1s_)

 | 

Interval between beacon frames of an AP. Default: 100ms.

The 802.11 standard defines beacon interval in terms of _time units_ (1 TU = 1.024 ms). The actual interval between beacons will be 1 TU for every 1 ms configured.

Every AP running on the same radio (i.e. a master AP and all its 'virtual'/'slave' APs) must use the same beacon interval.







 |
| 

**chains** (_list of integer 0..7_ )

 | 

[Radio chains](https://en.wikipedia.org/wiki/RF_chain) to use for receiving signals. Defaults to all chains available to the corresponding radio hardware.

 |
| 

**country** (_name of a country_)

 | 

Determines, which regulatory domain restrictions are applied to an interface. Defaults to "United States".

It is important to set this value correctly to comply with local regulations and ensure interoperability with other devices.







 |
| 

**dtim-period** (_integer 1..255_)

 | 

Period at which to transmit multicast traffic, when there are client devices in power save mode connected to the AP. Expressed as a multiple of the beacon interval.

Higher values enable client devices to save more energy, but increase network latency.

Default: 1

 |
| 

**hide-ssid** (_no_ | _yes_)

 | 

-   _yes_ - AP does not include its SSID in beacon frames, and does not reply to probe requests that have broadcast SSID.
    
-   _no_ - AP includes its SSID in the beacon frames, and replies to probe requests that have broadcast SSID.
    

Default: no

 |
| **mode** (_ap_ | _station_) | 

Interface operation mode

-   _ap_ (default) - interface operates as an access point
-   _station_ - interface acts as a client device, scanning for access points advertising the configured SSID

 |
| **rrm** (_no_ | _yes_) | 

-   yes - enable support for 802.11k radio resource measurement
-   no - disable  support for 802.11k radio resource measurement

Default: yes

 |
| **ssid** (_string_) | The name of the wireless network, aka the (E)SSID. No default value. |
| **tx-chains** (_list of integer 0..7_) | [Radio chains](https://en.wikipedia.org/wiki/RF_chain) to use for transmitting signals. Defaults to all chains available to the corresponding radio hardware. |
| **tx-power** (_integer 0..40_) | A limit on the transmit power (in dBm) of the interface. Can not be used to set power above limits imposed by the regulatory profile. Unset by default. |
| **manager** (_capsman_ _|_ _capsman-or-local_ _| local)_ | 

capsman - the interface will act as CAP only, this option should **not** be passed via provisioning rules to the CAP

capsman-or-local - the interface will get configuration via CAPsMAN or use its own, if /interface/wifiwave2/cap is not enabled.

local - interface won't contact CAPsMAN in order to get configuration.

 |

## Datapath properties

Parameters relating to forwarding packets to and from wireless client devices.

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
| ------------------------------- | ------------------------------------------------------------------------- |
| **bridge** (_bridge interface_) | Bridge interface to add interface to, as a bridge port. No default value. |
| **bridge-cost** (_integer_)     | Bridge port cost to use when adding as bridge port. Default: 10           |
| **bridge-horizon** (_none_      | _integer)_                                                                | Bridge horizon to use when adding as bridge port Default: none.                                              |
| **client-isolation**  (_no_     | _yes_)                                                                    | Determines whether client devices connecting to this interface are (by default) isolated from others or not. |
This policy can be overridden on a per-client basis using access list rules, so a an AP can have a mixture of isolated and non-isolated clients.  
Traffic from an isolated client will not be forwarded to other clients and unicast traffic from a non-isolated client will not be forwarded to an isolated one.  
Default: no |
| **interface-list** (_interface list_) | List to which add the interface as a member. No default value. |
| **openflow-switch** (_interface_) | OpenFlow switch to add interface to, as port when enabled. No default value |
| **vlan-id** (_none_ | _integer_ 1..4095) | 

Default VLAN ID to assign to client devices connecting to this interface (only relevant to interfaces in AP mode).  
When a client is assigned a VLAN ID, traffic coming from the client is automatically tagged with the ID and only packets tagged with with this ID are forwarded to the client.  
Default: none

802.11n/ac interfaces do not support this type of VLAN tagging under the wifiwave2 package, but they can be [configured](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-VLANExample-TrunkandAccessPorts) as VLAN access ports in bridge settings.







 |

## Security Properties

Parameters relating to authentication.

| Property | Description |
| -------- | ----------- |
| Property | Description |
| ---      | ---         |
|          |
**authentication-types** (_list of wpa-psk, wpa2-psk, wpa-eap, wpa2-eap, wpa3-psk, owe, wpa3-eap, wpa3-eap-192_)

 | 

Authentication types to enable on the interface.

The default value is an empty list (no authenticaion, an open network).

Configuring a passphrase, adds to the default list the _wpa2-psk_ authentication method (if the interface is an AP) or both _wpa-psk_ and _wpa2-psk_ (if the interface is a station).

Configuring an _eap-username_ and an _eap-password_ adds to the default list _wpa-eap and wpa2-eap_ authentication methods.

 |
| **dh-groups** (_list of 19, 20, 21_) | 

Identifiers of [elliptic curve cryptography groups](http://www.iana.org/assignments/ipsec-registry/ipsec-registry.xhtml#ipsec-registry-10) to use in SAE (WPA3) authentication.

 |
| **disable-pmkid** (_no_ | _yes_) | For interfaces in AP mode, disables inclusion of a PMKID in EAPOL frames. Disabling PMKID can cause compatibility issues with client devices which make use of it.

-   _yes_ - Do not include PMKID in EAPOL frames.
-   _no_ (default) - include PMKID in EAPOL frames.

 |
| **eap-accounting** (_no_ | _yes_) | Send accounting information to RADIUS server for EAP-authenticated peers. Default: no. |
| 

Properties related to EAP, are only relevant to interfaces in station mode. APs delegate EAP authentication to the RADIUS server.





 |
| **eap-anonymous-identity** (_string_) | Optional anonymous identity for EAP outer authentication. No default value. |
| **eap-certificate-mode** (_dont-verify-certificate_ | _no-certificates_ | _verify-certificate_ | _verify-certificate-with-crl_) | 

Policy for handling the TLS certificate of the RADIUS server.

-   verify-certificate - require server to have a valid certificate. Check that it is signed by a trusted certificate authority.
-   dont-verify-certificate (default) - Do not perform any checks on the certificate.
-   no-certificates - Attempt to establish the TLS tunnel by performing anonymous Diffie-Hellman key exchange. To be used if the RADIUS server has no certificate at all.
-   verify-certificate-with-crl - Same as _verify-certificate,_ but also checks if the certificate is valid by checking the Certificate Revocation List.

 |
| **eap-methods** (_list of_ _peap, tls, ttls_) | EAP methods to consider for authentication. Defaults to all supported methods. |
| **eap-password** (_string_) | Password to use, when the chosen EAP method requires one. No default value. |
| **eap-tls-certificate** (_certificate_) | Name or id of a certificate in the device's certificate store to use, when the chosen EAP authentication method requires one. No default value. |
| **eap-username** (_string_) | Username to use when the chosen EAP method requires one. No default value. |
| 

Take care when configuring encryption ciphers.

All client devices MUST support the group encryption cipher used by the AP to connect, and some client devices (notably, Intel® 8260) will also fail to connect if the list of unicast ciphers includes any they don't support.







 |
| **encryption** (_list of  ccmp, ccmp-256, gcmp, gcmp-256, tkip_) | 

A list of ciphers to support for encrypting unicast traffic.

Defaults to _ccmp_.

 |
| 

Properties related to 802.11r fast BSS transition only apply to interfaces in AP mode. Wifiwave2 interfaces in station mode do not support 802.11r.

For a client device to successfully roam between 2 APs, the APs need to be managed by the same instance of RouterOS. For information on how to centrally manage multiple APs, see [CAPsMAN](https://help.mikrotik.com/docs/display/ROS/WifiWave2#WifiWave2-WifiWave2CAPsMAN)







 |
| **ft** (_no | yes_) | 

Whether to enable 802.11r fast BSS transitions ( roaming). Default: no.

 |
| **ft-mobility-domain** (_integer 0..65535_)  | 

The fast BSS transition mobility domain ID. Default: 44484 (0xADC4).

 |
| **ft-nas-identifier** (string of _2..96 hex characters_) | 

Fast BSS transition PMK-R0 key holder identifier. Default: MAC address of the interface.

 |
| **ft-over-ds** (_no_ | _yes_ )  | 

 Whether to enable fast BSS transitions over DS (distributed system). Default: no.

 |
| **ft-preserve-vlanid** (_no_ | _yes_ ) | 

-   no - when a client connects to this AP via 802.11r fast BSS transition, it is assigned a VLAN ID according to the access and/or interface settings
-   yes (default) - when a client connects to this AP via 802.11r fast BSS transition, it retains the VLAN ID, which it was assigned during initial authentication

The default behavior is essential when relying on a RADIUS server to assign VLAN IDs to users, since a RADIUS server is only used for initial authentication.

 |
| **ft-r0-key-lifetime** (_time interval 1s..6w3d12h15m_) | 

Lifetime of the fast BSS transition PMK-R0 encryption key. Default: 600000s (~7 days)

 |
| **ft-reassociation-deadline** (_time interval 0..70s_)  | 

Fast BSS transition reassociation deadline. Default: 20s.

 |
| **group-encryption** (_ccmp_ | _ccmp-256_ | _gcmp_ | _gcmp-256_ | _tkip_) | 

Cipher to use for encrypting multicast traffic.

Defaults to _ccmp_.

 |
| **group-key-update** (_time interval_) | 

Interval at which the group temporal key (key for encrypting broadcast traffic) is renewed. Defaults to 24 hours.

 |
| **management-encryption** (_cmac_ | _cmac-256_ | _gmac_ | _gmac-256_) | 

Cipher to use for encrypting protected management frames. Defaults to _cmac_.

 |
| 

**management-protection** (_allowed_ | _disabled_ | _required_)

 | 

Whether to use 802.11w management frame protection. **I****ncompatible with management frame protection in standard wireless package**.

Default value depends on value of selected authentication type. WPA2 allows use of management protection, WPA3 requires it.

 |
| 

**owe-transition-interface** (_i__nterface_)

 | 

Name or internal id of an interface whose MAC address and SSID to advertise as the matching AP when running in OWE transition mode.

Required for setting up open APs that offer OWE, but also work with older devices that don't support the standard. See [configuration example below](https://help.mikrotik.com/docs/display/ROS/WifiWave2#WifiWave2-owe-transition-mode).

 |
| **passphrase** (_string of up to 63 characters_) | 

Passphrase to use for PSK authentication types. Defaults to an empty string - "".

WPA-PSK and WPA2-PSK authentication requires a minimum of 8 chars, while WPA3-PSK does not have minimum passphrase length.

 |
| **sae-anti-clogging-threshold** (_'disabled'_ | _integer_) | 

Due to SAE (WPA3) associations being CPU resource intensive, overwhelming an AP with bogus authentication requests makes for a feasible denial-of-service attack.

This parameter provides a way to mitigate such attacks by specifying a threshold of in-progress SAE authentications, at which the AP will start requesting that client devices include a cookie bound to their MAC address in their authentication requests. It will then only process authentication requests which contain valid cookies.

Default: 5.

 |
| **sae-max-failure-rate** (_'__d__isabled'_ | _integer_) | Rate of failed SAE (WPA3) associations per minute, at which the AP will stop processing new association requests. Default: 40. |
| **sae-pwe** (_both_ | _hash-to-element_ | _hunting-and-pecking_) | Methods to support for deriving SAE password element. Default: both. |
| **wps** (_disabled_ | _push-button_) | 

-   _push-button_ (default) - AP will accept WPS authentication for 2 minutes after 'wps-push-button' command is called. Physical WPS button functionality not yet implemented.
-   _disabled_ \- AP will not accept WPS authentication

 |

## Miscellaneous properties

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

|                     |
| ------------------- | --------- |
| **arp** (_disabled_ | _enabled_ | _local-proxy-arp_ | _proxy-arp_ | _reply-only)_ | Address Resolution Protocol mode: |

-   _disabled_ - the interface will not use ARP
-   _enabled_ - the interface will use ARP (default)
-   _local-proxy-arp_ - the router performs proxy ARP on the interface and sends replies to the same interface
-   _proxy-arp_ - the router performs proxy ARP on the interface and sends replies to other interfaces
-   _reply-only_ - the interface will only reply to requests originated from matching IP address/MAC address combinations which are entered as static entries in the [ARP](https://wiki.mikrotik.com/wiki/Manual:IP/ARP "Manual:IP/ARP") table. No dynamic entries will be automatically stored in the ARP table. Therefore for communications to be successful, a valid static entry must already exist.

 |
| **arp-timeout** (_time interval_ | _'auto'_) | Determines how long a dynamically added ARP table entry is considered valid since the last packet was received from the respective IP address.  
Value _auto_ equals to the value of _arp-timeout_ in _/ip settings_, which defaults to 30s. |
| **disable-running-check** _(no_ | _yes_) | 

-   _yes_ - interface's _r__unning_ property will be true whenever the interface is not disabled
    
-   _no_ (default) - interface's _running_ property will only be true when it has established a link to another device
    

 |
| 

**disabled** (_no_ | _yes_) (X)

 | 

Hardware interfaces are disabled by default. Virtual interfaces are not.

 |
| 

**mac-address** (_MAC_)

 | 

MAC address (BSSID) to use for an interface.

Hardware interfaces default to the MAC address of the associated radio interface.

Default MAC addresses for virtual interfaces are generated by

1.  Taking the MAC address of the associated master interface
    
2.  Setting the second-least-significant bit of the first octet to 1, resulting in a [locally administered MAC address](https://en.wikipedia.org/wiki/MAC_address#Universal_vs._local)
    
3.  If needed, incrementing the last octet of the address to ensure it doesn't overlap with the address of another interface on the device
    

 |
| 

**master-interface** (_i__nterface_)

 | 

Multiple interface configurations can be run simultaneously on every wireless radio.

Only one of them determines the radio's state (whether it is enabled, what frequency it's using, etc). This  'master' interface, is _bound_  to a radio with the corresponding _radio-mac._

To create additional ('virtual') interface configurations on a radio, they need to be _bound_ to the corresponding master interface.

No default value.

 |
| 

**name** (_string_)

 | 

A name for the interface. Defaults to _wifiN_, where _N_ is the lowest integer that has not yet been used for naming an interface.

 |

## Read-only properties

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

|                           |
| ------------------------- |  |
| **bound** (_boolean_) (B) |

Always true for _master_ interfaces (configurations linked to radio hardware).

True for a virtual interface (configurations linked to a master interface) when both the interface itself and its master interface are not disabled.

 |
| **default-name** (_string_) | The default name for an interface. |
| **inactive** (_boolean_) (I) | 

False for interfaces in AP mode when they've selected a channel for operation (i.e. configuration has been successfully applied).

False for interfaces in station mode when they've connected to an AP (i.e. configuration has been successfully applied, an with AP with matching settings has been found).

True otherwise.

 |
| **master** (_boolean_) (M) | True for interface configurations, which are _bound_ to radio hardware. False for virtual interfaces. |
| **radio-mac** (_MAC_) | The MAC address of the associated radio. |
| **running** (_boolean_) (R) | 

True, when an interface has established a link to another device.

If _disable-running-check_ is set to 'yes', true whenever the interface is not disabled.

 |

## Access List

| 
Filtering parameters



|                                      |
| ------------------------------------ |
| Parameter                            | Description                                                                 |
| **interface** (_interface_           | _interface-list_                                                            | _'any'_) | Match if connection takes place on the specified interface or interface belonging to specified list. Default: any. |
| **mac-address** (_MAC address_)      | Match if the client device has the specified MAC address. No default value. |
| **mac-address-mask** (_MAC address_) |

Modifies the **mac-address** parameter to match if it is equal to the result of performing bit-wise AND operation on the client MAC address and the given address mask.

Default: FF:FF:FF:FF:FF:FF (i.e. client's MAC address must match value of **mac-address** exactly)

 |
| **signal-range** (_min..max_) | Match if the strength of received signal from the client device is within the given range. Default: '-120..120' |
| **ssid-regexp** (_regex_) | Match if the given regular expression matches the SSID. |
| **time** (_start-end,days_) | Match during the specified time of day and (optionally) days of week. Default: 0s-1d |

  

| 
Action parameters



|                                              |
| -------------------------------------------- |
| Parameter                                    | Description |
| **allow-signal-out-of-range** (_time period_ | 'always')   |

The length of time which a connected peer's signal strength is allowed to be outside the range required by the **signal-range** parameter, before it is disconnected.

If the value is set to 'always', peer signal strength is only checked during association.

Default: 0s.

 |
| **action** (_accept_ | _reject_ | _query-radius_) | 

Whether to authorize a connection

-   _accept_ - connection is allowed
-   _reject_ - connection is not allowed
-   _query-radius_ -  connection is allowed if MAC address authentication of the client's MAC address succeeds

Default: _accept_

 |
| **client-isolation** (_no_ | _yes_) | 

Whether to [isolate](https://help.mikrotik.com/docs/display/ROS/WifiWave2#WifiWave2-Datapathproperties) the client from others connected to the same AP. No default value.

 |
| **passphrase** (_string_) | Override the default passphrase with given value. No default value. |
| **radius-accounting** (_no_ | _yes_) | Override the default RADIUS accounting policy with given value. No default value. |
| **vlan-id** ( _none_ | _integer 1..4095_ ) | Assign the given [VLAN ID](https://help.mikrotik.com/docs/display/ROS/WifiWave2#WifiWave2-Datapathproperties) to matched clients. No default value. |

## Frequency scan

Information about RF conditions on available channels can be obtained by running the frequency-scan command.

| Command parameters                           |
| -------------------------------------------- |
| Parameter                                    | Description                                                                                                                                                                                                                 |
| **duration** (_time interval)_               | Length of time to perform the scan for before exiting. Useful for non-interactive use. Not set by default.                                                                                                                  |
| **freeze-frame-interval** (_time interval)_  | Time interval at which to update command output. Default: 1s.                                                                                                                                                               |
| **frequency** (_list of frequencies/ranges)_ | Frequencies to perform the scan on. See [channel.frequency parameter syntax](https://help.mikrotik.com/docs/display/ROS/WifiWave2#WifiWave2-frequency-syntax) above for more detail. Defaults to all supported frequencies. |
| **numbers** (_string)_                       | Either the name or internal id of the interface to perform the scan with. Required. Not set by default.                                                                                                                     |
| **rounds** (_integer)_                       | Number of times to go through list of scannable frequencies before exiting. Useful for non-interactive use. Not set by default.                                                                                             |
| **save-file** (string)                       | Name of file to save output to. Not set by default.                                                                                                                                                                         |

  

| Output parameters        |
| ------------------------ |
| Parameter                | Description                                |
| **channel** (_integer)_  | Frequency (in MHz) of the channel scanned. |
| **networks** (_integer)_ |
Number of access points detected on the channel.

 |
| **load** (integer_)_ | Percentage of time the channel was busy during the scan. |
| **nf** (integer) | Noise floor (in dBm) of the channel. |
| **max-signal** (_integer_) | Maximum signal strength (in dBm) of APs detected in the channel. |
| **min-signal** (_integer_) | Minimum signal strength (in dBm) of APs detected in the channel. |
| **primary** (_boolean_) (P) | Channel is in use as the primary (control) channel by an AP. |
| **secondary** (boolean) (S) | Channel is in use as a secondary (extension) channel by an AP. |

## Scan command

The '/interface wifiwave2 scan' command will scan for access points and print out information about any APs it detects.

The scan command takes all the same parameters as the frequency-scan command.

| Output parameters          |
| -------------------------- |
| Parameter                  | Description                                                                                                          |
| **active** (_boolean_) (A) | Signifies that beacons from the AP have been received in the last 30 seconds.                                        |
| **address** (_MAC_)        | The MAC address (BSSID) of the AP.                                                                                   |
| **channel** (_string_)     | The control channel frequency used by the AP, its supported wireless standards and control/extension channel layout. |
|                            |
**security** (_string_)

 | 

Authentication methods supported by the AP.

 |
| **signal** (_integer_) | Signal strength of the AP's beacons (in dBm). |
| **ssid** (_string_) | The extended service set identifier of the AP. |
| **sta-count** (_integer_) | The number of client devices associated with the AP. Only available if the AP includes this information in its beacons. |

## Sniffer

| Command parameters             |
| ------------------------------ |
| Parameter                      | Description                                                                                |
| **duration** (_time interval_) | Automatically interrupt the sniffer after the specified time has passed. No default value. |
|                                |
**number** (_interface_)



 | Interface to use for sniffing. |
| **pcap-file** (_string__)_ | Save captured frames to a file with the given name. No default value (captured frames are not saved to a file by default). |
| **pcap-size-limit** (_integer_) | File size limit (in bytes) when storing captured frames locally.  
When this limit has been reached, no new frames are added to the capture file. No default value. |
| **stream-address** (IP address) | Stream captured packets via the TZSP protocol to the given address. No default value (captured packets are not streamed anywhere by default). |
| **stream-rate** (_integer_) | Limit on the rate (in packets per second) at which captured frames are streamed via TZSP. |

## WPS

interface/wifiwave2/wps-client wifi

| Command parameters             |
| ------------------------------ |
| Parameter                      | Description                                                                                   |
| **duration** (_time interval_) | Length of time after which the command will time out if no AP is found. Unlimited by default. |
| **interval** (_time interval_) | Time interval at which to update command output. Default: 1s.                                 |
| **mac-address** (_MAC_)        | Only attempt connecting to AP with the specified MAC (BSSID). Not set by default.             |
| **numbers** (_string_)         | Name or internal id of the interface with which to attempt connection. Not set by default.    |
| **ssid** (_string_)            | Only attempt to connect to APs with the specified SSID. Not set by default.                   |

## Radios

Information about the capabilities of each radio can be gained by running the \`/interface/wifiwave2/radio print detail\` command.

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
| -------------------------------------- | ----------------------------------------------------------------- |
| **2g-channels** (_list of_ _integers_) | Frequencies supported in the 2.4GHz band.                         |
| **5g-channels** (_list of integers_)   | Frequencies supported in the 5GHz band.                           |
| **bands** (_list of strings_)          | Supported frequency bands, wireless standards and channel widths. |
| **ciphers** (_list of strings_)        | Supported encryption ciphers.                                     |
| **countries** (_list of strings_)      | Regulatory domains supported by the interface.                    |
| **min-antenna-gain** (_integer_)       | Minimum antenna gain permitted for the interface.                 |
| **phy-id** (_string_)                  |

A unique identifier.

 |
| **radio-mac** (_MAC_) | MAC address of the radio interface. Can be used to match radios to interface configurations. |
| **rx-chains** (_list of integers_) | IDs for radio chains available for receiving radio signals. |
| **tx-chains** (_list of integers_) | IDs for radio chains available for transmitting radio signals. |

## Registration table

The registration table contains read-only information about associated wireless devices.

| 
Parameter

 | 

Description

|     |
| --- |  |
|     |

Parameter

 | 

Description

|                                  |
| -------------------------------- | ---------------------------------------------------------------------- |
| **authorized** (_boolean_) (A)   | True when the peer has successfully authenticated.                     |
| **bytes** (_list of integers_)   | Number of bytes in packets transmitted to a peer and received from it. |
| **interface** (_string_)         | Name of the interface, which was used to associate with the peer.      |
| **mac-address** (_MAC_)          | The MAC address of the peer.                                           |
| **packets** (_list of integers_) | Number of packets transmitted to a peer and received from it.          |
| **rx-rate** _(string)_           | Bitrate of received transmissions from peer.                           |
| **signal** (_integer)_           |

Strength of signal received from the peer (in dBm).

 |
| **tx-rate** (_string)_ | Bitrate used for transmitting to the peer. |
| **uptime** (_time interval)_ | Time since association. |

## CAPsMAN Global Configuration

Menu: /interface/wifiwave2/capsman

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

|                            |
| -------------------------- | ---------------------- |
| **ca-certificate** _(auto_ | _certificate name_ _)_ | Device CA certificate, CAPsMAN server requires a certificate, certificate on CAP is optional. |
| **certificate** (_auto     | certificate name       | none_; Default: **none**)                                                                     | Device certificate |
| **enabled** _(no_          | _yes_)                 |

Disable or enable CAPsMAN functionality

 |
| 

**package-path** (_string |_; Default: )

 | Folder location for the RouterOS packages. For example, use "/upgrade" to specify the upgrade folder from the files section. If an empty string is set, CAPsMAN can use built-in RouterOS packages, note that in this case only CAPs with the same architecture as CAPsMAN will be upgraded. |
| 

**require-peer-certificate** (_yes | no_; Default: **no**)

 | 

Require all connecting CAPs to have a valid certificate

 |
| 

**upgrade-policy** (_none | require-same-version | suggest-same-upgrade_; Default: **none**)

 | 

Upgrade policy options

-   none - do not perform upgrade
-   require-same-version - CAPsMAN suggest to upgrade the CAP RouterOS version and, if it fails it will not provision the CAP. (Manual provision is still possible)
-   suggest-same-version - CAPsMAN suggests to upgrade the CAP RouterOS version and if it fails it will still be provisioned

 |
| **interfaces** _(all | interface name | none; Default: **all**)_ | Interfaces on which CAPsMAN will listen for CAP connections |

## CAPsMAN Provisioning

Provisioning rules for matching radios are configured in **/interface/wifiwave2/provisioning/** menu:

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

|                              |
| ---------------------------- | -------------- |
| **action** (_create-disabled | create-enabled | create-dynamic-enabled | none_; Default: **none**) | Action to take if rule matches are specified by the following settings: |

-   **create-disabled** \- create disabled static interfaces for radio. I.e., the interfaces will be bound to the radio, but the radio will not be operational until the interface is manually enabled;
-   **create-enabled** \- create enabled static interfaces. I.e., the interfaces will be bound to the radio and the radio will be operational;
-   **create-dynamic-enabled** \- create enabled dynamic interfaces. I.e., the interfaces will be bound to the radio, and the radio will be operational;
-   **none** \- do nothing, leaves radio in the non-provisioned state;

 |
| **comment** (_string_; Default: ) | Short description of the Provisioning rule |
| **common-name-regexp** (_string_; Default: ) | Regular expression to match radios by common name. Each CAP's common name identifier can be found under "/interface/wifiwave2/radio" as value "REMOTE-CAP-NAME" |
| **supported-bands** (_2ghz-ax | 2ghz-g | 2ghz-n | 5ghz-a | 5ghz-ac | 5ghz-ax | 5ghz-n_; Default: ) | Match radios by supported wireless modes |
| **identity-regexp** (_string_; Default: ) | Regular expression to match radios by router identity |
| **address-ranges** (_IpAddressRange\[,IpAddressRanges\] max 100x_; Default: **""**) | Match CAPs with IPs within configured address range. |
| **master-configuration** (_string_; Default: ) | If **action** specifies to create interfaces, then a new master interface with its configuration set to this configuration profile will be created |
| **name-format** (_cap | identity_ ; Default: **cap**) | specify the syntax of the CAP interface name creation

-   "example1-**%I**" - cap identity
-   "example2-**%C** "- cap common name

 |
| **name-prefix** (_string_; Default: ) | name prefix which can be used in the name-format for creating the CAP interface names |
| **radio-mac** (_MAC address_; Default: **00:00:00:00:00:00**) | MAC address of radio to be matched, empty MAC (00:00:00:00:00:00) means match all MAC addresses |
| **slave-configurations** (_string_; Default: ) | 

If **action** specifies to create interfaces, then a new slave interface for each configuration profile in this list is created.

 |
| **disabled** (_yes_ _| no_; Default: **no**)  | 

Specifies if the provision rule is disabled.

 |

## CAP configuration

Menu: /interface/wifiwave2/cap

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

|                                                                     |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **caps-man-addresses** _(list of IP addresses; Default: **empty**)_ | List of Manager IP addresses that CAP will attempt to contact during discovery                                 |
| **caps-man-names** ()                                               | An ordered list of CAPs Manager names that the CAP will connect to, if empty - CAP does not check Manager name |
| **discovery-interfaces** (_list of interfaces_;)                    | List of interfaces over which CAP should attempt to discover Manager                                           |
|                                                                     |

**lock-to-caps-man** (_no_ | _yes;_ Default: **no**)

 | Sets, if CAP should lock to the first CAPsMAN it connects to |
| 

**slaves-static** ()

 |   
 |
| 

**caps-man-certificate-common-names** ()

 | List of Manager certificate CommonNames that CAP will connect to, if empty - CAP does not check Manager certificate CommonName |
| **certificate** () | Certificate to use for authenticating |
| **enabled** (_yes | no_; Default: **no**) | Disable or enable the CAP feature |
| **slaves-datapath** () |   
 |