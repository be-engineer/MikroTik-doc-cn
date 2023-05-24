## Summary



This example shows how to configure automatic fail-over (bonding) 5Ghz link in combination with 60Ghz devices in GUI.  
When a connection between 60Ghz wireless is lost, it will automatically use the bonded interface.  
Example is done from empty configuration state with [[WinBox](https://mikrotik.com/download) utility

## Connect to the device



After configuration reset - only mac-telnet is possible. In main WinBox screen press on Neighbours, choose your devices MAC address and press Connect:

1.  Select correct device **MAC Address;**
2.  Login by default is "**admin**" and no password is set;
3.  Press **Connect.**

![](https://help.mikrotik.com/docs/download/attachments/43843592/connect_To_device.png?version=1&modificationDate=1622190419447&api=v2)

## Configure bridge  



Add new bridge.

1.  Open Bridge sub-menu;
2.  Press on "+" to add new bridge;
3.  Apply your changes.

![](https://help.mikrotik.com/docs/download/attachments/43843592/winbox_bridge_screen.png?version=1&modificationDate=1604312525470&api=v2)

_Later in the instructions it requires to assign bridge members to it. This will allow to pass traffic from Ethernet to W60G interface without routing._

## Set up 60Ghz wireless connection



All previously explained steps are identical to **bridge** and **station** devices. Different modes needs to be used when configuring wireless interfaces.

Configure **bridge** device as follows:

1.  Open Interface menu;
2.  Double click on wlan60-1 interface;
3.  Press on Wireless sub-menu and set mode to **bridge (**or **ap-bridge** for PtmP);
4.  Set SSID and password and region;
5.  Select previously created bridge under "Put Stations In Bridge";
6.  Apply your changes;
7.  Press enable to start transmitting.

![](https://help.mikrotik.com/docs/download/attachments/43843592/60Ghz_connection_bridge.png?version=1&modificationDate=1622183751843&api=v2)

Configure **station** device as follows:

1.  Open Interface menu;
2.  Double click on wlan60-1 interface;
3.  Press on Wireless sub-menu and set mode to **station bridge;**
4.  Set SSID and password;
5.  Apply your changes;
6.  Press enable to start transmitting.

![](https://help.mikrotik.com/docs/download/attachments/43843592/60Ghz_station.png?version=1&modificationDate=1622184307117&api=v2)

## Set up 5Ghz wireless connection

___

**Choose Security Profile for your devices -**

1.  Choose **Wireless** menu
2.  Choose **Security Profiles** sub-menu
3.  Add new profile with "**+**" sign
4.  Choose **name**, **mode**, **authentication type** and a secure password.
5.  **Apply** the configuration.

**![](https://help.mikrotik.com/docs/download/attachments/43843592/5Ghz_security_profile.png?version=1&modificationDate=1622186103507&api=v2)**

_**For bridge device -**_

1.  Open **Interfaces** menu;
2.  Double click on **wlan1** interface;
3.  Press on **Wireless** sub-menu and set mode to **bridge** (or **ap-bridge** for PtmP);
4.  Set **SSID**, **password** and **country.**
5.  Press on **Advanced Mode.**

![](https://help.mikrotik.com/docs/download/attachments/43843592/5ghz_bridge1.png?version=1&modificationDate=1622186905895&api=v2)

1.  Choose your **Security Profile**;
2.  **Apply** your changes;
3.  Press **enable** to start transmitting.

![](https://help.mikrotik.com/docs/download/attachments/43843592/5ghz_bridge2.png?version=1&modificationDate=1622187051362&api=v2)

**_For station device -_**

1.  Open **Interfaces** menu;
2.  Double click on **wlan1** interface;
3.  Press on **Wireless** sub-menu and set mode to **station-bridge**;
4.  Set **SSID**, **password** and **country**;
5.  Press on **advanced** mode ( similar to bridge device\* );
6.  Choose **Security Profile**;
7.  **Apply** your changes;
8.  Press **enable** to start transmitting.

![](https://help.mikrotik.com/docs/download/attachments/43843592/5ghz_station.png?version=1&modificationDate=1622187363087&api=v2)

_If everything is done correctly - running (R) flags should appear as shown in the screenshot -_  
![](https://help.mikrotik.com/docs/download/attachments/43843592/R_flags.png?version=1&modificationDate=1622187671524&api=v2)

## Configure bonding  

___

_Configure bonding and assign slave interfaces in this setup it is selected as built in wlan1 interface, but it can be also ether interface in other kind of setups._

_**For bridge device -**_

1.  Press on **Bonding** sub-menu;
2.   Add new member with "**+**";
3.  Add interface members (**wlan1** and **wlan60-station-1**) to **bonding** interface as **Slaves;**
4.  Add interface member **wlan60-station-1** as **Primary** interface;
5.  Choose Mode as **active backup**;
6.  **Apply** configuration.

![](https://help.mikrotik.com/docs/download/attachments/43843592/Bridge_bonding.png?version=1&modificationDate=1622188481448&api=v2)

_**For station device -**_

1.  Press on **Bonding** sub-menu;
2.   Add new member with "**+**";
3.  Add interface members (**wlan1** and **wlan60-1**) to **bonding** interface as **Slaves;**
4.  Add interface member **wlan60-1** as **Primary** interface;
5.  Choose Mode as **active backup**;
6.  **Apply** configuration.

![](https://help.mikrotik.com/docs/download/attachments/43843592/Station_bonding.png?version=1&modificationDate=1622188982907&api=v2)

## Configure bridge  



_Configuring bridge settings including the bonding interface is mandatory for the active-backup to work on used devices ( In this case bridge and station devices settings are the same ).  
_

1.  Press on **Bridge** sub-menu;
2.  Add new member with "**+**";
3.  Add interface member as **ether1** and Bridge member as **bridge1;**
4.  **Apply** configuration.

_![](https://help.mikrotik.com/docs/download/attachments/43843592/bridge_port1.png?version=2&modificationDate=1622189781589&api=v2)_

1.  Press on **Bridge** sub-menu;
2.  Add new member with "**+**";
3.  Add interface member as **bonding1** and Bridge member as **bridge1;**
4.  **Apply** configuration.

_![](https://help.mikrotik.com/docs/download/attachments/43843592/bonding_ports2.png?version=1&modificationDate=1622189792250&api=v2)_

## Additional configuration


Interfaces when enabled from greyed out will become active.

Link should be established after all previously explained steps are done. It's recommended to set up administrator password on both devices.