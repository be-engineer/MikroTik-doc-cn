RouterBOOT is responsible for starting RouterOS in RouterBOARD devices.

## Main and Backup loaders

By default, the main loader is used, but RouterBOARD devices also have a secondary (backup) bootloader, which can be used in case the main doesn't work. It is possible to call the backup loader with a configuration setting in RouterOS:

[?](https://help.mikrotik.com/docs/display/ROS/RouterBOOT#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">system</code><code class="ros constants">/routerboard/settings/</code><code class="ros functions">set </code><code class="ros value">force-backup-booter</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

It is also possible to use the backup booter by turning on the device, with the RESET button pushed. It is only possible to upgrade the main RouterBOOT, so in case of failure, you can use the backup booter to start the device and downgrade the main loader. For upgrade instructions, follow the separate instructions in [RouterBOARD#UpgradingRouterBOOT](https://help.mikrotik.com/docs/display/ROS/RouterBOARD#RouterBOARD-UpgradingRouterBOOT)

## RouterBOARD reset button

RouterBOOT reset button has three functions:

-   Hold this button during boot time until the LED light starts flashing, release the button to reset the RouterOS configuration (total 5 seconds)
-   Keep holding for 5 more seconds, LED turns solid, release now to turn on CAPs mode (total 10 seconds)
-   Or Keep holding the button for 5 more seconds until LED turns off, then release it to make the RouterBOARD look for Netinstall servers (total of 15 seconds)

If you hold the button before applying power, backup RouterBOOT will be used in addition to all the above actions. To do the above actions without loading the backup loader, push the button right after applying power to the device.

  

[Reset the password](https://help.mikrotik.com/docs/display/RKB/Reset+the+password)

[https://www.youtube.com/watch?v=6Unz92rABs8](https://www.youtube.com/watch?v=6Unz92rABs8) 

## Configuration Reset For **Wireless Wire** kits

The reset button has the same functionality as on other devices, explained in detail [https://help.mikrotik.com/docs/display/ROS/Reset+Button](https://help.mikrotik.com/docs/display/ROS/Reset+Button)

5-second button hold on startup (USR LED light starts flashing) - resets to password-protected state.

10-second button hold on startup (USR LED turns solid after flashing) - completely removes configuration.

## Configuration

For RouterBOARD devices that feature a serial console connector, it is possible to access the RouterBOOT loader configuration menu. The required cable is described in the [Serial Console](https://help.mikrotik.com/docs/display/ROS/Serial+Console) manual. RouterBOARD serial port is configured to 115200bit/s, 8 data bits, 1 stop bit, and no parity. We suggest disabling the hardware flow control. 

This example shows the menu which is available in RouterBOOT 7.4beta4:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">RouterBOOT booter 7.4beta4</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">CRS328-24P-4S+</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">built by build at Jun</code><code class="ros constants">/15/2022 11:34:09 from revision 73B4521C</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">CPU frequency</code><code class="ros constants">: 800 MHz</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">Memory size</code><code class="ros constants">: 512 MiB</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">Storage size</code><code class="ros constants">:&nbsp; 16 MiB</code></div><div class="line number10 index9 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">Press Ctrl+E to enter etherboot mode</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">Press any key within 2 seconds to enter setup</code></div><div class="line number13 index12 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number14 index13 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros plain">RouterBOOT-7.4beta4</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros plain">What </code><code class="ros functions">do </code><code class="ros plain">you want to configure?</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">d - boot delay</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">k - boot key</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">s - serial console</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">n - silent boot</code></div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">o - boot device</code></div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">z - extra kernel parameters</code></div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">r - </code><code class="ros functions">reset </code><code class="ros plain">booter configuration</code></div><div class="line number24 index23 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">e - format storage</code></div><div class="line number25 index24 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">w - repartition nand</code></div><div class="line number26 index25 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">g - </code><code class="ros functions">upgrade </code><code class="ros plain">firmware</code></div><div class="line number27 index26 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">i - board info</code></div><div class="line number28 index27 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">p - boot protocol</code></div><div class="line number29 index28 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">b - booter options</code></div><div class="line number30 index29 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">j - boot os</code></div><div class="line number31 index30 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">t - hardware tests</code></div><div class="line number32 index31 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">l - erase license</code></div><div class="line number33 index32 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">x - exit setup</code></div><div class="line number34 index33 alt1" data-bidi-marker="true"><code class="ros plain">your choice</code><code class="ros constants">:</code></div></div></td></tr></tbody></table>

The options are self-explanatory.


| letter | description                | explanation                                                                                                                   |
| ------ | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| d      | boot delay                 | Delays starting of RouterOS to allow an interface to initialize                                                               |
| k      | boot key                   | The button that will open the configuration menu                                                                              |
| s      | serial console             | Sets the baud rate of the serial port                                                                                         |
| n      | silent boot                | Suppresses all output on the serial port, in case some device is connected to it (like a GPS device or a temperature monitor) |
| o      | boot device                | Allows to enable Netinstall booting                                                                                           |
| z      | extra kernel parameters    |
|        |
| r      | reset booter configuration | Resets the settings in this menu. **Warning, no confirmation!**                                                               |
| e      | format storage             | Destroys all data on the NAND, including RouterOS configuration and license                                                   |
| w      | repartition nand           | Refer to the [Partitions](https://help.mikrotik.com/docs/display/ROS/Partitions) document for more info                       |
| y      | active partition           | Choose an active partition from which to try to load RouterOS                                                                 |
| g      | upgrade firmware           | Allows upgrading RouterBOOT version through the network, or the XModem protocol                                               |
| i      | board info                 |
|        |
| p      | boot protocol              |
|        |
| b      | booter options             | Select which bootloader to use by default                                                                                     |
| t      | do memory testing          | booter options                                                                                                                |
| j      | boot os                    | do memory testing                                                                                                             |
| t      | hardware tests             |                                                                                                                               |
| l      | erase license              |                                                                                                                               |
| x      | exit setup                 |                                                                                                                               |

Hitting the appropriate keyboard letter will give you a list of further options, they are shown below:

```
# d - boot delay:

Select boot delay:
   1 - 1s
 * 2 - 2s
   3 - 3s
   4 - 4s
   5 - 5s
   6 - 6s
   7 - 7s
   8 - 8s
   9 - 9s

# k - boot key:

Select key which will enter setup on boot:
 * 1 - any key
   2 - <Delete> key only

# s - serial console:

Select baud rate for serial console:
 * 1 - 115200
   2 - 57600
   3 - 38400
   4 - 19200
   5 - 9600
   6 - 4800
   7 - 2400
   8 - 1200
   9 - off

# n - silent boot:

Silent boot:
   0 - off
 * 1 - on

# o - boot device:

Select boot device:
   e - boot over Ethernet
 * n - boot from NAND, if fail then Ethernet
   1 - boot Ethernet once, then NAND
   o - boot from NAND only
   b - boot chosen device
   f - boot Flash Configure Mode
   3 - boot Flash Configure Mode once, then NAND


# f - cpu frequency:

Select CPU frequency:
   a -  200MHz
   b -  400MHz
   c -  600MHz
   d -  800MHz
   e - 1000MHz
 * f - 1200MHz

# r - reset booter configuration:

# e - format nand:

Do you realy want to format your storage device?
that would result in losing all your data
type "yes" to confirm: 

# w - repartition nand:

Select parititon count:
   1 - partition
 * 2 - partitions
   3 - partitions
   4 - partitions

# y - active partition:

Select active partiton:
 * 0 - partition
   1 - partition

# g - upgrade firmware:

Upgrade firmware options:
   e - upgrade firmware over ethernet
   s - upgrade firmware over serial port

# i - board info:

Board Info:

        Board type: CCR1009-8G-1S-1S+
     Serial number: 48FF01DDE6FD
  Firmware version: 3.19
     CPU frequency: 1200 MHz
       Memory size: 2048 MiB
         NAND size: 128 MiB
        Build time: 2014-09-23 15:02:34
  eth1 MAC address: 00:0C:42:00:BE:4A
  eth2 MAC address: 00:0C:42:00:BE:4B
  eth3 MAC address: 00:0C:42:00:BE:4C
  eth4 MAC address: 00:0C:42:00:BE:4D
  eth5 MAC address: 00:0C:42:00:BE:4E
  eth6 MAC address: 00:0C:42:00:BE:4F
  eth7 MAC address: 00:0C:42:00:BE:50
  eth8 MAC address: 00:0C:42:00:BE:51
  eth9 MAC address: 00:0C:42:00:BE:52
 eth10 MAC address: 00:0C:42:00:BE:53

# p - boot protocol:

Choose which boot protocol to use:
 * 1 - bootp protocol
   2 - dhcp protocol

# b - booter options:

Select which booter you want to load:
 * 1 - load regular booter
   2 - force backup-booter loading

#t - do memory testing:

launches built in memory test!

# x - exit setup:

Exit bios configuration menu and continues with system startup.

```

  

## Simple Upgrade

RouterBOOT can be upgraded from RouterOS by:

-   Run command _/system routerboard upgrade_
-   Reboot your router to apply the upgrade (_/system reboot_)\]

[?](https://help.mikrotik.com/docs/display/ROS/RouterBOOT#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@admin] &gt; system</code><code class="ros constants">/routerboard/</code><code class="ros functions">upgrade</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Do you really want to </code><code class="ros functions">upgrade </code><code class="ros plain">firmware? [y</code><code class="ros constants">/n]</code></div></div></td></tr></tbody></table>

Every ROS version has a new RouterBoot version included in it, once you perform a ROS upgrade we always recommend upgrading RouterBoot also.

## Checking RouterBOOT version

This command shows the current RouterBOOT version of your device and available upgrade which is _either included in routerboard.npk package, or if you uploaded an FWF file_ corresponding to the device model:

[?](https://help.mikrotik.com/docs/display/ROS/RouterBOOT#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@admin] &gt;&nbsp; system</code><code class="ros constants">/routerboard/</code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">;;; Firmware upgraded successfully, please reboot </code><code class="ros functions">for </code><code class="ros plain">changes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">to take effect!</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">routerboard</code><code class="ros constants">: yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">board-name</code><code class="ros constants">: hAP ac</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">model</code><code class="ros constants">: RouterBOARD 962UiGS-5HacT2HnT</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">serial-number</code><code class="ros constants">: 6737057562DD</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">firmware-type</code><code class="ros constants">: qca9550L</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">factory-firmware</code><code class="ros constants">: 3.29</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">current-firmware</code><code class="ros constants">: 6.49.5</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">upgrade-firmware</code><code class="ros constants">: 7.4beta5</code></div></div></td></tr></tbody></table>

In this case, you see, there is **a newer version** of the Bootloader firmware available already inside your current RouterOS version and it has been updated and requires a reboot.

A downgrade is also possible by uploading \*.FWF file with an older version may be required for troubleshooting purposes when contacting MikroTik support.