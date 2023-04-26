## Summary

**Quickset** is a simple configuration wizard page that prepares your router in a few clicks. It is the first screen a user sees, when opening the default IP address 192.168.88.1 in a web browser.

Quickset is available for all devices that have some sort of default configuration from factory. Devices that do not have configuration must be configured by hand. The most popular and recommended mode is the HomeAP (or HomeAP dual, depending on the device). This Quickset mode provides the simplest of terminology and the most common options for the home user.

## Modes

Depending on the router model, different Quickset modes might be available from the Quickset dropdown menu:

-   **CAP**: Controlled Access Point, an AP device, that will be managed by a centralised CAPsMAN server. Only use if you have already set up a CAPsMAN server.
-   **CPE**: Client device, which will connect to an Access Point (AP) device. Provides option to scan for AP devices in your area.
-   **HomeAP**: The default Access Point config page for most home users. Provides less options and simplified terminology.
-   **HomeAP dual**: Dual band devices (2GHz/5GHz). The default Access Point config page for most home users. Provides less options and simplified terminology.
-   **Home Mesh**: Made for making bigger WiFi networks. Enables the CAPsMAN server in the router, and places the local WiFi interfaces under CAPsMAN control. Just boot other MikroTik WiFi APs with the reset button pressed, and they will join this HomeMesh network (see their Quick guide for details)
-   **PTP Bridge AP**: When you need to transparently interconnect two remote locations together in the same network, set one device to this mode, and the other device to the next (PTP Bridge CPE) mode.
-   **PTP Bridge CPE**: When you need to transparently interconnect two remote locations together in the same network, set one device to this mode, and the other device to the previous (PTP Bridge AP) mode.
-   **WISP AP**: Similar to the HomeAP mode, but provides more advanced options and uses industry standard terminology, like SSID and WPA.

## HomeAP

This is the mode you should use if you would like to quickly configure a home access point.

### Wireless

Set up your wireless network in this section:

-   **Network Name**: How will your smartphone see your network? Set any name you like here. In HomeAP dual, you can set the 2GHz (legacy) and 5GHz (modern) networks to the same, or different names (see FAQ). Use any name you like, in any format.
-   **Frequency**: Normally you can leave "Auto", in this way, the router will scan the environment, and select the least occupied frequency channel (it will do this once). Use a custom selection if you need to experiment.
-   **Band**: Normally leave this to defaults (2GHz b/g/n and 5GHz A/N/AC).
-   **Use Access List (ACL)**: Enable this if you would like to restrict who can connect to your AP, based on the users MAC (hardware) address. To use this option, first you need to allow these clients to connect, and then use the below button "Copy to ACL". This will copy the selected client to the access list. After you have build an Access list (ACL), you can enable this option to forbid anyone else to attempt connections to your device. Normally you can leave this alone, as the Wireless password already provides the needed restrictions.
-   **WiFi Password**: The most important option here. Sets a secure password that also encrypts your wireless communications.
-   **WPS accept**: Use this button to grant access to a specific device that supports the WPS connection mode. Useful for printers and other peripherals where typing a password is difficult. First start WPS mode in your client device, then once click the WPS button here to allow said device. Button works for a few seconds and operates on a per-client basis.
-   **Guest network**: Useful for house guests who don't need to know your main WiFi password. Set a separate password for them in this option. Important! Guest users will not be able to access other devices in your LAN and other guest devices. This mode enabled Bridge filters to prevent this.
-   **Wireless clients**: This table shows the currently connected client devices (their MAC address, if they are in your Access List, their last used IP address, how long are they connected, their signal level in dBm and in a bar graph).

### Internet

-   **Port**: Select which port is connected to the ISP (internet) modem. Usually Eth1.
-   **Address Acquisition**: Select how the ISP is giving you the IP address. Ask your service provider about this and the other options (IP address, Netmask, Gateway).
-   **MAC address**: Normally should not be changed, unless your ISP has locked you to a specific MAC address and you have changed the router to a new one.
-   **Firewall router**: This enables secure firewall for your router and your network. Always make sure this box is selected, so that no access is possible to your devices from the internet port.
-   **MAC server / MAC Winbox**: Allows connection with the \[Winbox utility [https://mt.lv/winbox](https://mt.lv/winbox)\] from the LAN port side in MAC address mode. Useful for debugging and recovery, when IP mode is not available. Advanced use only.
-   **Discovery**: Allows the device to be identified by model name from other RouterOS devices.

### Local Network

-   **IP address**: Mostly can stay at the default 192.168.88.1 unless your router is behind another router. To avoid IP conflict, change to 192.168.89.1 or similar
-   **Netmask**: In most situations can leave 255.255.255.0
-   **Bridge all LAN ports**: Allows your devices to communicate to each other, even if, say, your TV is connected via ethernet LAN cable, but your PC is connected via WiFi.
-   **DHCP server**: Normally, you would want automatic IP address configuration in your home network, so leave the DHCP settings ON and on their defaults.
-   **NAT**: Turn this off ONLY if your ISP has provided a public IP address for both the router and also the local network. If not, leave NAT on.
-   **UPnP**: This option enables automatic port forwarding ("opening ports to the local network" as some call it) for supported programs and devices, like your NAS disks and peer-to-peer utilities. Use with care, as this option can sometimes expose internal devices to the internet without your knowledge. Enable only if specifically needed.

### VPN

If you want to access your local network (and your router) from the internet, use a secure VPN tunnel. This option gives you a domain name where to connect to, and enables PPTP and L2TP/IPsec (the second one is recommended). The username is 'vpn' and you can specify your own password. All you need to do is enable it here, and then provide the address, username and password in your laptop or phone, and when connected to the VPN, you will have a securely encrypted connection to your home network. Also useful when travelling - you will be able to browse the internet through a secure line, as if connecting from your home. This also helps to avoid geographical restrictions that are set up in some countries.

### System

-   **Check for updates**: Always make sure your device is up to date with this button. Checks if an updated RouterOS release is available, and installs it.
-   **Password**: Sets the password for the device config page itself. Make sure nobody can access your router config page and change the settings.

## FAQ

**Q: How is Quickset different from the Webfig tab, where a whole bunch of new menus appear?**

A: QuickSet is for new users who only need their device up and running in no time. It provides the most commonly used options in one place. If you need more options, do not use any Quickset settings at all, click on "Webfig" to open the advanced configuration interface. The full functionality is unlocked.

**Q: Can I use Quickset and Webfig together? While settings that are not conflicting can be configured this way, it is not recommended to mix up these menus.**

A: If you are going to use Quickset, use only Quickset and vice versa. What's is difference between Router and Bridge mode? Bridge mode adds all interfaces to the bridge allowing to forward Layer2 packets (acts as a hub/switch). In Router mode packets are forwarded in Layer3 by using IP addresses and IP routes (acts as a router).

**Q: In HomeAP mode, should the 2GHz and 5GHz network names be the same, or different?**

A: If you prefer that all your client devices, like TV, phones, game consoles, would automatically select the best preferred network, set the names identically. If you would like to force a client device to use the faster 5GHz 802.11ac connection, set the names unique.

**Q: Can I create an AP without security settings - no password or connect to such AP while using QuickSet?**

A: QuickSet uses WPA2 pre-shared key by default. It means that the minimal password length is 8 symbols and the device can only connect to WPA2 secured AP or serve as AP itself. For configurations with no security settings, you need to configure them manually using WinBox, Webfig, or console.