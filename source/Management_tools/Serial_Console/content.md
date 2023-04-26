# Overview

The Serial Console and Terminal are tools, used to communicate with devices and other systems that are interconnected via the serial port. The serial terminal may be used to monitor and configure many devices - including modems, network devices (including MikroTik routers), and any device that can be connected to a serial (asynchronous) port.

The Serial Console feature is for configuring direct-access configuration facilities (monitor/keyboard and serial port) that are mostly used for initial or recovery configuration. A special null-modem cable is needed to connect two hosts (like two PCs, or two routers; not modems). Note that a terminal emulation program (e.g., HyperTerminal on Windows or minicom on Linux) is required to access the serial console from another computer. Default settings of the router's serial port are 115200 bits/s (for x86 default is 9600 bits/s), 8 data bits, 1 stop bit, no parity, hardware (RTS/CTS) flow control. 

Several customers have described situations where the Serial Terminal (managing side) feature would be useful:

-   on a mountaintop, where a MikroTik wireless installation sits next to equipment (including switches and Cisco routers) that can not be managed in-band (by telnet through an IP network)
-   monitoring weather-reporting equipment through a serial port
-   connection to a high-speed microwave modem that needed to be monitored and managed by a serial connection

With the serial-terminal feature of the MikroTik, up to 132 (and, maybe, even more) devices can be monitored and controlled.

# Serial Console Connections

Serial communications between devices are done with RS232, it is one of the oldest and most widely spread communication methods in the computer world. It was used for communication with the modems or other peripheral devices DTE/DCE. In the modern world, the main use of serial communication is DTE/DTE communication (Data Terminal Equipment) e.g. using a null-modem cable. There are several types of null modem cables and some of them may not work with RouterBoards at all.

## Null Modem Without Handshake

This cable does not utilize handshake pins at all:

| 
Side1 (DB9f)

 | 

Side2 (DB9f)

 | 

Function

 |     |
 | --- |  |  |
 |     |

Side1 (DB9f)

 | 

Side2 (DB9f)

 | 

Function

 |     |
 | --- | --- |  |
 | 2   | 3   |

Rx ← Tx

 |
| 3 | 2 | Tx → Rx |
| 5 | 5 | GND |

It allows data-only traffic on the cross-connected Rx/Tx lines. Hardware flow control is not possible with this type of cable. The only way to perform flow control is with software flow control using the XOFF and XON characters.

## Null Modem With LoopBack Handshake

The problem with the first cable is when connected to a device on which hardware flow control is enabled software may hang when checking modem signal lines. 

Null modem cable with loop back handshake fixes the problem, its main purpose is to fool well-defined software into thinking there is handshaking available:

| 
Side1 (DB9f)

 | 

Side2 (DB9f)

 | 

Function

 |     |
 | --- |  |  |
 |     |

Side1 (DB9f)

 | 

Side2 (DB9f)

 | 

Function

 |     |
 | --- | --- |  |
 | 2   | 3   |

Rx ← Tx

 |
| 3 | 2 | Tx → Rx |
| 5 | 5 | 

GND

 |
| 1+4+6 | \- | DTR → CD + DSR |
| \- | 1+4+6 | DTR → CD + DSR |
| 7+8 | \- | RTS → CTS |
| \- | 7+8 | RTS → CTS |

Hardware flow control is not possible with this cable. Also if remote software does not send its own ready signal to DTR output communication will hang.

## Null Modem With Partial Handshake

This cable can be used when flow control enabled without being incompatible with the original way flow control was used with DTE/DCE communication.

This type of cable is not recommended for use with RouterOS.

| 
Side1 (DB9f)

 | 

Side2 (DB9f)

 | 

Function

 |     |
 | --- |  |  |
 |     |

Side1 (DB9f)

 | 

Side2 (DB9f)

 | 

Function

 |     |
 | --- | --- |  |
 | 1   | 7+8 |

RTS2 → CTS2 + CD1

 |
| 2 | 3 | Rx ← Tx |
| 3 | 2 | 

Tx → Rx

 |
| 4 | 6 | DTR → DSR |
| 5 | 5 | GND |
| 6 | 4 | DSR ← DTR |
| 7+8 | 1 | RTS1 → CTS1 + CD2 |

## Null Modem With Full Handshake

Used with special software and should not be used with RouterOS.

| 
Side1 (DB9f)

 | 

Side2 (DB9f)

 | 

Function

 |     |
 | --- |  |  |
 |     |

Side1 (DB9f)

 | 

Side2 (DB9f)

 | 

Function

 |     |
 | --- | --- | ------- |
 | 2   | 3   | Rx ← Tx |
 | 3   | 2   |

Tx → Rx

 |
| 4 | 6 | DTR → DSR |
| 5 | 5 | GND |
| 6 | 4 | DSR ← DTR |
| 7 | 8 | RTS → CTS |
| 8 | 7 | CTS ← RTS |

## Null Modem Compatibility

Summary tables below will allow you to choose the proper cable for your application.

| 
  


 | 

No handshake

 | 

Loopback  
handshake



 | 

Partial  
handshake



 | 

Full  
handshake

 |     |
 | --- |  |  |  |  |
 |     |

  


 | 

No handshake

 | 

Loopback  
handshake



 | 

Partial  
handshake



 | 

Full  
handshake

 |                                 |
 | ------------------------------- | --- | --- | --- | --- |
 | RouterBoards                    |
 | with limited port functionality | Y   | Y   | N\* | N   |
 | RouterBoards                    |
 | with full functionality         | Y   | Y   | Y   | N   |

\* - may work only when hardware flow control is disabled

  

| 
  


 | 

No handshake

 | 

Loopback  
handshake



 | 

Partial  
handshake



 | 

Full  
handshake

 |     |
 | --- |  |  |  |  |
 |     |

  


 | 

No handshake

 | 

Loopback  
handshake



 | 

Partial  
handshake



 | 

Full  
handshake

 |                               |
 | ----------------------------- | --- | --- | ----- | ----- |
 | Software flow                 |
 | control only                  | Y   | Y\* | Y\*\* | Y\*\* |
 | Low-speed DTE/DCE compatible  |
 | hardware flow control         | N   | Y   | Y\*   | N     |
 | High-speed DTE/DCE compatible |
 | hardware flow control         | N   | Y   | Y\*\* | N     |
 | High speed                    |
communication  
using special software | N | N | Y\* | Y |

\* - will work as an alternative

\*\* - will work but not recommended

## RJ45 Type Serial Port

This type of port is used on RouterBOARD 2011, 3011, 4011, CCR1072, CCR1036 r2, CCR2xxx and CRS series devices, sometimes called "Cisco style" serial port.

RJ45 to DB9 Cable Pinout:

![](https://help.mikrotik.com/docs/download/attachments/328139/Rj45-pinout.gif.png?version=1&modificationDate=1570702738344&api=v2)  
  

| 
Signal

 | 

Console Port (DTE)  
RJ-45

 | 

RJ-45 Rolled Cable  
RJ-45 Pin

 | 

Adapter DB-9 Pin

 | 

Adapter DB-25 Pin

 | 

Signal

 |     |
 | --- |  |  |  |  |  |
 |     |

Signal

 | 

Console Port (DTE)  
RJ-45

 | 

RJ-45 Rolled Cable  
RJ-45 Pin

 | 

Adapter DB-9 Pin

 | 

Adapter DB-25 Pin

 | 

Signal

 |        |
 | ------ | --- | --- | --- | --- | ------ |
 | RTS    | 1   | 8   | 8   | 5   | CTS    |
 | DTR    | 2   | 7   | 6   | 6   | DSR    |
 | TxD    | 3   | 6   | 2   | 3   | RxD    |
 | Ground | 4   | 5   | 5   | 7   | Ground |
 | Ground | 5   | 4   | 5   | 7   | Ground |
 | RxD    | 6   | 3   | 3   | 2   | TxD    |
 | DSR    | 7   | 2   | 4   | 20  | DTR    |
 | CTS    | 8   | 1   | 7   | 4   | RTS    |

## RB M33G Additional Serial Header

For RBM33G additional serial header can be attached on GPIO pins U3\_RXD, GND, U3\_TXD, and 3V3

RouterOS 6.45.1+ and firmware are required!

  

## CCR Serial Header

The Cloud Core Router series devices have a serial header on the PCB board, called J402 or 100

Here is the pin-out of that connector:

![](https://help.mikrotik.com/docs/download/attachments/328139/J402.png?version=1&modificationDate=1570702787676&api=v2)

# Serial Terminal Usage

RouterOS allows to communicate with devices and other systems that are connected to the router via the serial port using a `/system serial-terminal`  command. All keyboard input will be forwarded to the serial port and all data from the port is output to the connected device.

First, you have to have a free serial port, if the device has only one serial port (like all RouterBoards, WRAP/ALIX boards, etc.) you will have to disable the system console on this serial port to be able to use it as **Serial Terminal** for connection to other equipment (switches, modems, etc):

[?](https://help.mikrotik.com/docs/display/ROS/Serial+Console#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system console </code><code class="ros functions">disable </code><code class="ros plain">0</code></div></div></td></tr></tbody></table>

Be sure to just disable the console rather than removing it, as RouterOS will recreate the console after the next reboot when you really remove it.

**Note that there are some caveats you should be aware of! Take your time understanding those limits to avoid strange things to happen when connecting a device to a serial port on a RouterBoard:**

-   By re-configuring port Serial0 on a RouterBoard as seen above, you will lose your serial console access to RouterOS. This means, that if you cannot access your RouterBoard over the network anymore, you might even have to reset the whole configuration of it to gain access again.
-   When rebooting a RouterBoard the boot loader (RouterBOOT) will always use the serial console (Serial0 on RouterBoards) to send out some startup messages and offer access to the RouterBOOT menu.
    
    Having text coming out of the serial port to the connected device might confuse your attached device. Furthermore, in the standard config, you can enter the RouterBOOT menu by pressing **ANY** key. So if your serial device sends any character to the serial port of your RouterBoard during boot time, the RouterBoard will enter the RouterBOOT menu and will **NOT** boot RouterOS unless you manually intervene!
    
    You can reconfigure RouterBOOT to enter the RouterBOOT menu only when a **DEL** character is received - use this to reduce the chance to get a router that's stuck when rebooting!
    
    Or if newer versions are used ["Silent boot"](https://wiki.mikrotik.com/wiki/Silent_boot "Silent boot") feature can be used to suppress any output on the serial interface, including removal of booting sounds.
    

  

  

Next, you will have to configure your serial port according to the serial port settings of the connected device. Using the following command you will set your serial port to 19200 Baud 8N1. What settings you need to use depends on the device you connect:

[?](https://help.mikrotik.com/docs/display/ROS/Serial+Console#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/port </code><code class="ros functions">set </code><code class="ros plain">serial0 </code><code class="ros value">baud-rate</code><code class="ros plain">=19200</code> <code class="ros value">data-bits</code><code class="ros plain">=8</code> <code class="ros value">parity</code><code class="ros plain">=none</code> <code class="ros value">stop-bits</code><code class="ros plain">=1</code></div></div></td></tr></tbody></table>

You can also try to let RouterOS guess the needed baud rate by setting

[?](https://help.mikrotik.com/docs/display/ROS/Serial+Console#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/port </code><code class="ros functions">set </code><code class="ros plain">serial0 </code><code class="ros value">baud-rate</code><code class="ros plain">=auto</code></div></div></td></tr></tbody></table>

Now's the time to connect your device if not already done. Usually, you will have to use a [null modem cable](https://help.mikrotik.com/docs/display/ROS/Serial+Console#SerialConsole-NullModemWithoutHandshake) (the same thing as a cross-over-cable for Ethernet). Now we're ready to go:

[?](https://help.mikrotik.com/docs/display/ROS/Serial+Console#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system serial-terminal serial0</code></div></div></td></tr></tbody></table>

This will give you access to the device you connected to port Serial0. **_Ctrl-A_** is the prefix key, which means that you will enter a small "menu". If you need to send the **_Ctrl-A_** character to a remote device, press **_Ctrl-A_** twice.

If you want to exit the connection to the serial device type **_Ctrl-A_**, then **_Q_**. This will return you to your RouterOS console.

Do not connect to devices at an incorrect speed and avoid dumping binary data.

# Special Login

Special login can be used to access another device (like a switch, for example) that is connected through a serial cable by opening a telnet/ssh session that will get you directly on this device (without having to login to RouterOS first). 

For demonstration we will use two RouterBoards and one PC. 

![](https://help.mikrotik.com/docs/download/attachments/328139/Special-login-setup.jpg?version=2&modificationDate=1657265964296&api=v2)

Routers R1 and R2 are connected with serial cable and PC is connected to R1 via ethernet. Lets say we want to access router R2 via serial cable from our PC. To do this you have to set up serial interface proxy on R1. It can be done by feature called **special-login**.

By default console is bound to serial port. 

First task is to unbind console from serial simply by disabling entry in /system console menu:

[?](https://help.mikrotik.com/docs/display/ROS/Serial+Console#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/system console&gt; </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, U - used, F - free</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments">#&nbsp;&nbsp; PORT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TERM</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0 X serial0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; vt102</code></div></div></td></tr></tbody></table>

Next step is to add new user, in this case _serial_, and bind it to the serial port

[?](https://help.mikrotik.com/docs/display/ROS/Serial+Console#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/user </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=serial</code> <code class="ros value">group</code><code class="ros plain">=full</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/special-login </code><code class="ros functions">add </code><code class="ros value">user</code><code class="ros plain">=serial</code> <code class="ros value">port</code><code class="ros plain">=serial0</code> <code class="ros value">disabled</code><code class="ros plain">=no</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/special-login </code><code class="ros plain">print</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disab</code><code class="ros plain">led</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments">#&nbsp;&nbsp; USER&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PORT</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;&nbsp; serial&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; serial0</code></div></div></td></tr></tbody></table>

Now we are ready to access R2 from our PC.

[?](https://help.mikrotik.com/docs/display/ROS/Serial+Console#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">maris@bumba</code><code class="ros constants">:/$ ssh serial@10.1.101.146</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[Ctrl-A is the prefix key]</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">R2 4.0beta4</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">R2 Login</code><code class="ros constants">:</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">[admin@R2] &gt;</code></div></div></td></tr></tbody></table>

To exit special login mode press Ctrl+A and Q

[?](https://help.mikrotik.com/docs/display/ROS/Serial+Console#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt;</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[Q - </code><code class="ros functions">quit </code><code class="ros plain">connection]&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [B - </code><code class="ros functions">send </code><code class="ros plain">break]</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[A - </code><code class="ros functions">send </code><code class="ros plain">Ctrl-A prefix]&nbsp;&nbsp; [R - autoconfigure rate]</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">Connection to 10.1.101.146 closed.</code></div></div></td></tr></tbody></table>

  

After router reboot and serial cable attached router may stuck at Bootloader main menu

To fix this problem you need to allow access bootloader main menu from <any> key to <delete>:

-   enter bootloader menu
-   press 'k' for boot key options
-   press '2' to change key to <delete>

```
What do you want to configure?                                                   
d - boot delay                                                                
k - boot key                                                                  
s - serial console                                                            
n - silent boot                                                              
o - boot device                                                               
u - cpu mode                                                                 
f - cpu frequency                                                             
r - reset booter configuration                                                 
e - format nand                                                               
g - upgrade firmware                                                         
i - board info                                                                
p - boot protocol                                                            
b - booter options                                                            
t - call debug code                                                           
l - erase license                                                             
x - exit setup                         
your choice: k - boot key

Select key which will enter setup on boot:
 * 1 - any key
   2 - <Delete> key only

your chaoice: 2
```