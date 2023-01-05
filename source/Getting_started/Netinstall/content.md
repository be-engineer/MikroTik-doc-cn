# Introduction

Netinstall is a tool for installing and reinstalling MikroTik devices running RouterOS. Always try using Netinstall if you suspect that your device is not working properly. The tool is available for Windows (with a graphical interface) and for Linux (as a command line tool). 

In short, the Netinstall procedure goes like this: Connect your PC directly to the **boot** port (Usually Ether1, the port labeled BOOT or as otherwise indicated in the product manual) of the device you will be reinstalling. Turn on the device while holding the **reset** button until it shows up in the Netinstall tool.

Careful. Netinstall re-formats the system's drive, all configuration and saved files will be lost. Netinstall does not erase the RouterOS license key, nor does it reset RouterBOOT related settings, for example, CPU frequency is not changed after reinstalling the device.

# Instructions for Windows  

-   Download **Netinstall** from the [downloads](https://mikrotik.com/download) page. If you are not sure which version you need, then you can always select the version that is marked as **Current** (stable);
-   Download the RouterOS **Main package** from the [downloads](https://mikrotik.com/download) page;
    
    You must choose a RouterOS version. You can always select the version that is marked as **Current**. You must also select the architecture (ARM, MIPS, SMIPS, TILE, etc...), but if you are not sure, then you can download the RouterOS package for **ALL** architectures, Netinstall will choose the right architecture for you.
    
-   Disconnect your computer from WiFi, Ethernet, LTE, or any other type of connection! Netinstall will only work on one active interface on your computer, it is highly recommended that you disconnect any other network interfaces in order to be sure that Netinstall will select the right network interface.
    
-   Configure a static IP address for your Ethernet interface, open **Start,** and select **Settings**:
    

![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_4.png?version=1&modificationDate=1587384029368&api=v2)

Netinstall can run also on a local network, in such case you could skip setting a static IP address, but it is highly recommended that you set a static IP address if you are not familiar with Netinstall.

-   Open **Network & Internet** and select **Change adapter options**

![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_5.png?version=1&modificationDate=1587384914250&api=v2)![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_6.png?version=1&modificationDate=1587385041755&api=v2)

-    Right-click on your Ethernet interface and select **Properties**

![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_7.png?version=1&modificationDate=1587385120369&api=v2)

-   Select **Internet Protocol Version 4 (TCP/IPv4)** and click **Properties**

**![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_8.png?version=1&modificationDate=1587385250640&api=v2)**

-   Check Use the following IP address and fill out the fields as shown in the image below

**![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_9.png?version=1&modificationDate=1587385330268&api=v2)**

If you have a working router, then you can use it and skip the setting up a static IP part of this tutorial, but it requires you to know your LAN address since you will need to specify an unused IP address in your network for the network boot server. For this reason, it is recommended to apply a static IP address and follow this guide precisely, if you are not sure how to get these parameters out of your network.

-   Open your Downloads folder (or wherever you saved the downloaded files) and extract the Netinstall .zip file to a convenient place

![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_1.png?version=1&modificationDate=1587385508581&api=v2)![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_2.png?version=1&modificationDate=1587385541664&api=v2)

-   Make sure that the Ethernet interface is running and launch Netinstall.exe. If you followed the guide precisely, then you should not have any Internet connection on your computer, Windows 10 wants to verify all apps that it runs, but will not be able to do it since lack of an Internet connection, for this reason, a warning might pop up, you should click **Run**.
    

![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_10.png?version=1&modificationDate=1587385638572&api=v2)

Netinstall requires administrator rights, there should be a window asking for permissions to run Netinstall, you must accept these permissions in order for Netinstall to work properly.

-   Allow access for Netinstall in **Public** networks and configure **Net booting** settings and fill out the required fields as shown in the image below

![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_11.png?version=2&modificationDate=1587385766358&api=v2)![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_12.png?version=1&modificationDate=1587385770397&api=v2)

The Client IP address must be unique! Don't use an existing IP address in your network, this also means that you should not use the computer's IP address as well. Use a completely different IP address from the same subnet.

-   Connect your device to your computer using an ethernet cable directly (without any other devices in-between), plug the Ethernet cable into your device's Etherboot port.
-   MikroTik devices are able to use Netinstall from their **first** port (Ether1), or from the port marked with "**BOOT**".
  
![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_18.png?version=1&modificationDate=1587385958852&api=v2)

Some computers have a network interface (especially USB Ethernet adapters) that tend to create an extra link flap, which is enough for Netinstall to fail to detect a device that is in Etherboot mode. In such a case you can use a switch between your device and your computer or a router in bridge mode to prevent this issue.

-   Power up your device and put it into etherboot mode

There are multiple ways how to put your device into Etherboot mode. Make sure you read the Etherboot manual before trying to put the device into this mode. Methods vary between different MikroTik devices.

-   Wait for the device to show up in Netinstall, select it and press **Browse.** Navigate to your **Downloads** folder (or wherever you saved your RouterOS packages) and press **OK**

**![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_13.png?version=1&modificationDate=1587387085890&api=v2)**![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_14.png?version=2&modificationDate=1587387136017&api=v2)

-   Select your desired RouterOS version and press **Install.** Wait for the installation to finish and press "**Reboot**" (Devices without serial console have to be rebooted manually)

If you downloaded RouterOS packages for multiple architectures, then Netinstall will only show the appropriate architecture packages for your device after you have selected it. All unsupported packages will not show up in this window after you have selected a device.

**![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_15.png?version=1&modificationDate=1587387289302&api=v2)![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_17.png?version=1&modificationDate=1587387292639&api=v2)**

If the installation does not start (progress bar is not moving or no status is shown), then you can try closing the Netinstall application and opening it up again or try to put the device into Etherboot mode again. If you are still unable to get Netinstall working, then you should try using it on a different computer since there might be an operating system's issue that is preventing Netinstall from working properly.

-   You are done! Remove the device from power, remove the Ethernet cable, place the device back in your network and your device should be running properly now!

After using Netinstall the device will be reset to defaults (unless you specified not to apply default configuration). Some devices are not accessible through **ether1** port with the default configuration for security reasons. Read more about [Default configuration](https://wiki.mikrotik.com/wiki/Manual:Default_Configurations "Manual:Default Configurations").

When using the **Configure script** option, it is suggested to introduce a [delay](https://wiki.mikrotik.com/wiki/Manual:Configuration_Management#Startup_delay) before configuration execution.

# Instructions for Linux

The Linux version is a command line tool, which offers nearly the same parameters as the Windows counterpart. 

Download the tool from our download page (links not literal): 

```
wget https://download.mikrotik.com/routeros/[VERSION]/netinstall-[VERSION].tar.gz
```

Extract it:

```
tar -xzf netinstall-[VERSION].tar.gz
```

Run the tool:

```
./netinstall-cli -a 192.168.0.1 routeros-arm64-[VERSION].npk
```

The tool requires privileged access and must be run as root, use sudo.

The available parameters are as follows: 

| Parameter      | Meaning                                                                                       |
| -------------- | --------------------------------------------------------------------------------------------- |
| \-r            | resets the configuration upon reinstallation procedure, optional                              |
| \-k keyfile    | provides the device with a license key (key file in .KEY format), optional                    |
| \-s userscript | preconfigures the device with the provided configuration (text file in .RSC format), optional |
|                |

\-a IP

 | uses a specific IP address that the Netinstall server will assign to the device, mandatory |
| PACKAGE | specify a list of RouterOS.NPK format packages that Netinstall will try to install on the device, mandatory |
| \-i | 

**_starting from Release 7.7beta8_**

allows you to specify an interface on which netinstall will work on the host, using multiple NICs. (sudo ./netinstall-cli -i <interface> -r -a 192.168.88.3 routeros-7.5-mipsbe.npk)

 |

First make sure you have set the IP on your computer's interface:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">admin@ubuntu:~$ sudo ifconfig &lt;interface&gt; 192.168.88.2/24</code></div></div></td></tr></tbody></table>

Then run the Netinstall version 6 (an example that resets the configuration upon reinstallation procedure):

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">admin@ubuntu:~$ sudo ./netinstall -r -a 192.168.88.3 routeros-mipsbe-6.48.1.npk</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Using server IP: 192.168.88.2</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Starting PXE server</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">Waiting for RouterBOARD...</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">PXE client: 01:23:45:67:89:10</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text plain">Sending image: mips</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain">Discovered RouterBOARD...</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text plain">Formatting...</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text plain">Sending package routeros-mipsbe-6.48.1.npk ...</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text plain">Ready for reboot...</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="text plain">Sent reboot command</code></div></div></td></tr></tbody></table>

Or run the Netinstall version 7 (an example that resets the configuration upon reinstallation procedure):

[?](https://help.mikrotik.com/docs/display/ROS/Netinstall#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">admin@ubuntu:~$ sudo ./netinstall-cli -r -a 192.168.88.3 routeros-7.5-mipsbe.npk</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Version: 7.5 (2022-08-30 09:34:59)</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Using server IP: 192.168.88.2</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">Use Netmask: 255.255.255.0</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">Starting PXE server</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text plain">Waiting for RouterBOARD...</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain">PXE client: C4:AD:34::89:10</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text plain">Sending image: mips</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text plain">Discovered RouterBOARD...</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text plain">Formatting...</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="text plain">Sending package routeros-mipsbe-7.5.npk ...</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="text plain">Ready for reboot...</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="text plain">Sent reboot command</code></div></div></td></tr></tbody></table>

# Etherboot

Etherboot mode is a special state for a MikroTik device that allows you to reinstall your device using [Netinstall](https://help.mikrotik.com/docs/display/ROS/Netinstall). There are several ways to put your device into Etherboot mode depending on the device you are using.

## Reset button

The **Reset** can be found on all MikroTik devices, this button can be used to put the device into Etherboot mode. An easy way to put a device into Etherboot mode using the **Reset** button is by powering off the device, hold the **Reset** button, power on the device while holding the **Reset** button and keep holding it until the device shows up in your **Netinstalll** window.

![](https://help.mikrotik.com/docs/download/attachments/24805390/262_hi_res.png?version=1&modificationDate=1587460761021&api=v2)

If you have set up a [Protected bootloader](https://help.mikrotik.com/docs/display/ROS/RouterBOARD#RouterBOARD-Protectedbootloader), then the reset button's behavior is changed. Make sure you remember the settings you used to set up the Protected bootloader, otherwise you will not be able to use Eterboot mode and will not be able to reset your device.

## RouterOS

If your device is able to boot up and you are able to log in, then you can easily put the device into Etherboot mode. To do so, just connect to your device and execute the following command:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system routerboard settings </code><code class="ros functions">set </code><code class="ros value">boot-device</code><code class="ros plain">=try-ethernet-once-then-nand</code></div></div></td></tr></tbody></table>

  
After that either reboot the device or do a power cycle on the device. Next time the device will boot up, then it will first try going into Etherboot mode. Note that after the first boot up, the device will not try going into Etherboot mode and will boot directly from NAND or from the storage type the device is using.

## Serial console

Some devices come with a serial console that can be used to put the device into Etherboot mode. To do so, make sure you configure your computer's serial console. The required parameters for all MikroTik devices (except for RouterBOARD 230 series) are as following:

[?](https://help.mikrotik.com/docs/display/ROS/Netinstall#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">115200bit</code><code class="ros constants">/s, 8 data bits, 1 stop bit, no parity, flow control=none by default.</code></div></div></td></tr></tbody></table>

For RouterBOARD 230 series devices the parameters are as following:

[?](https://help.mikrotik.com/docs/display/ROS/Netinstall#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">9600bit</code><code class="ros constants">/s, 8 data bits, 1 stop bit, no parity, hardware (RTS/CTS) flow control by default.</code></div></div></td></tr></tbody></table>

Make sure you are using a proper null modem cable, you can find the proper pinout [here](https://help.mikrotik.com/docs/display/ROS/Serial+Console). When the device is booting up, keep pressing **CTRL+E** on your keyboard until the device shows that it is **trying bootp protocol**:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">RouterBOOT booter 6.42.3</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">CRS125-24G-1S</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">CPU frequency</code><code class="ros constants">: 600 MHz</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">Memory speed</code><code class="ros constants">: 175 MHz</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">Memory size</code><code class="ros constants">: 128 MiB</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">NAND size</code><code class="ros constants">: 128 MiB</code></div><div class="line number9 index8 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">Press any key within 2 seconds to enter setup</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">Ethernet link absent...</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">trying bootp protocol.....................</code></div></div></td></tr></tbody></table>

At this point your device is in Etherboot mode, now the device should show up in your Netinstall window.