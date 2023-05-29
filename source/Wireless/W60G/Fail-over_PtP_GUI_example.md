# GUI中结合60Ghz设备配置自动故障转移概述

本示例展示了如何在GUI中结合60Ghz设备配置自动故障转移(bonding) 5Ghz链路。
当60Ghz无线之间的连接丢失时，它会自动使用绑定接口。
示例是通过 [WinBox](https://mikrotik.com/download) 实用程序从空配置状态完成的

## 连接设备



配置复位后，只允许mac-telnet。在主WinBox屏幕上按“邻居”，选择设备的MAC地址并按“连接”:

1. 选择正确的设备MAC地址;
2. 登录默认为admin，未设置密码;
3. 点 **connect**

![](https://help.mikrotik.com/docs/download/attachments/43843592/connect_To_device.png?version=1&modificationDate=1622190419447&api=v2)

## 配置网桥

添加新的网桥。

1.  打开网桥子菜单;
2.  按“+”键添加新网桥;
3.  应用更改。

![](https://help.mikrotik.com/docs/download/attachments/43843592/winbox_bridge_screen.png?version=1&modificationDate=1604312525470&api=v2)

在后面的指令中，它要求为它分配桥成员。这将允许通过流量从以太网到W60G接口没有路由

## 设置60Ghz无线连接

所有前面解释的步骤都与 **桥** 和 **站** 设备相同。在配置无线接口时，需要使用不同的模式。

配置 **网桥** 设备如下:

1.  打开接口菜单;
2.  双击wlan60-1界面;
3.按无线子菜单，设置模式为网桥(PtmP为ap网桥);
4.  设置SSID、密码和区域;
5.  选择之前创建的桥梁，在“Put Stations In bridge”下;
6.  应用您的更改;
7.  按enable开始传输。

![](https://help.mikrotik.com/docs/download/attachments/43843592/60Ghz_connection_bridge.png?version=1&modificationDate=1622183751843&api=v2)

配置站设备如下:

1.  打开接口菜单;
2.  双击wlan60-1界面;
3.  点击无线子菜单，设置模式为station bridge
4.  设置SSID和密码;
5.  应用更改;
6.  按enable开始传输。

![](https://help.mikrotik.com/docs/download/attachments/43843592/60Ghz_station.png?version=1&modificationDate=1622184307117&api=v2)

## 设置5Ghz无线连接


**为设备选择安全配置文件**

1.  选择无线菜单
2.  选择安全配置文件子菜单
3.  添加带有“+”标志的新配置文件
4.  选择名称、模式、认证类型和安全密码。
5.  应用配置。

![](https://help.mikrotik.com/docs/download/attachments/43843592/5Ghz_security_profile.png?version=1&modificationDate=1622186103507&api=v2)

**用于桥接设备**

1.  打开接口菜单;
2.  双击wlan1界面;
3.  点击无线子菜单，设置模式为网桥(PtmP为ap网桥);
4.  设置SSID、密码和国家
5.  点击“高级模式”

![](https://help.mikrotik.com/docs/download/attachments/43843592/5ghz_bridge1.png?version=1&modificationDate=1622186905895&api=v2)

1.  选择安全配置文件;
2.  应用更改;
3.  按enable开始传输。

![](https://help.mikrotik.com/docs/download/attachments/43843592/5ghz_bridge2.png?version=1&modificationDate=1622187051362&api=v2)

**适用于工作站设备**

1.  打开接口菜单;
2.  双击wlan1界面;
3.  点击无线子菜单，设置模式为station-bridge;
4.  设置SSID、密码和国家;
5.  点击高级模式(类似桥接装置);
6.  选择安全配置文件;
7.  应用更改;
8.  点击enable开始传输。

![](https://help.mikrotik.com/docs/download/attachments/43843592/5ghz_station.png?version=1&modificationDate=1622187363087&api=v2)

如果一切都做得正确-运行(R)标志应该出现在屏幕截图上 
![](https://help.mikrotik.com/docs/download/attachments/43843592/R_flags.png?version=1&modificationDate=1622187671524&api=v2)

## 配置绑定


在此设置中配置绑定并分配从接口，它被选择为内置的wlan1接口，但在其他类型的设置中也可以是以太网接口。

**用于桥接设备**

1.  点击Bonding子菜单;
2.  添加带有“+”的新成员;
3.  将接口成员(wlan1和wlan60-station-1)作为Slaves添加到bonding接口
4.  添加接口成员wlan60-station-1为主接口;
5.  选择模式为主备份;
6.  应用配置。

![](https://help.mikrotik.com/docs/download/attachments/43843592/Bridge_bonding.png?version=1&modificationDate=1622188481448&api=v2)

**适用于工作站设备**

1.  点击Bonding子菜单;
2.  添加带有“+”的新成员;
3.  将接口成员(wlan1和wlan60-1)作为slave添加到bonding接口
4.  添加接口成员wlan60-1为主接口;
5.  选择模式为主备份;
6.  应用配置。

![](https://help.mikrotik.com/docs/download/attachments/43843592/Station_bonding.png?version=1&modificationDate=1622188982907&api=v2)

## 配置网桥


active-backup要在旧设备上工作，必须配置网桥设置，包括绑定接口(在这种情况下，网桥和站的设备设置相同)。


1.  点击桥接子菜单;
2.  添加带有“+”的新成员;
3.  添加接口成员为ether1，网桥成员为bridge1;
4.  应用配置。

![](https://help.mikrotik.com/docs/download/attachments/43843592/bridge_port1.png?version=2&modificationDate=1622189781589&api=v2)

1.  点击桥接子菜单;
2.  添加带有“+”的新成员;
3.  添加接口成员为bonding1和桥成员为bridge1;
4.  应用配置。

![](https://help.mikrotik.com/docs/download/attachments/43843592/bonding_ports2.png?version=1&modificationDate=1622189792250&api=v2)

## 附加配置


接口启用后将变为活动状态。

在完成前面解释的所有步骤后，应该建立链接。建议在两台设备上都设置管理员密码。