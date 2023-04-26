## LoRa卡的安装

本指南将以LtAP LTE套件为例进行说明。

打开路由器外壳，卸下所有的螺丝，小心地将上机箱移到左侧，因为LTE天线是连接在机箱的内侧。

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/1.png?version=1&modificationDate=1609848720368&api=v2)

  

将R11e-LoRa卡插入mini-PCIe插槽，将两颗螺丝钉套在螺纹件上。

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/OpenCaseNoCard.jpeg?version=1&modificationDate=1609922446595&api=v2)

  

把天线连接到卡上（UFL连接器） 

也可以使用UFL → SMA电缆，因为LtAP的外壳有一个专门的插槽。

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/OpenCase.jpeg?version=1&modificationDate=1609922460528&api=v2)

  

前面的步骤完成后，就可以关闭路由器外壳，继续进行配置。

## 配置

### GUI设置

通过Winbox或WebFig连接到你的路由器。

Winbox可以在下面的链接中下载：

[https://mikrotik.com/download](https://mikrotik.com/download)

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/WinboxLogin.png?version=2&modificationDate=1609922552358&api=v2)

  

强烈建议将RouterOS版本升级到最新的可用版本。安装新版本将执行重启。

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/rosUpgrade.png?version=1&modificationDate=1609921627894&api=v2)

  

为路由器结构和rOS版本下载额外的软件包。可以在Winbox窗口的顶部或系统→资源→架构名称中看到你的路由器架构类型。

[https://mikrotik.com/download](https://mikrotik.com/download)

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/ExtraPackages.png?version=1&modificationDate=1609923306859&api=v2)

  

一旦下载并解压了软件包，将LoRa软件包上传到你的路由器，可以通过拖放来完成。上传完成后，它应该出现在文件夹中，重新启动你的路由器（系统→重启）安装该软件包。

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/LoraUpload.png?version=3&modificationDate=1609929801527&api=v2)

  

重启后，软件包应该在软件包列表中可见。

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/LoRaInstalled.png?version=1&modificationDate=1609929836867&api=v2)

  

检查LoRa网关是否已经初始化，如果没有，检查USB类型是否设置为Mini-PCIe。



![](https://help.mikrotik.com/docs/download/attachments/50692141/LoraPackageVisible.png?version=2&modificationDate=1609932721368&api=v2)

  

网关显示出来后选择它，选择默认网络服务器，或者添加自己的网络服务器并启用它。

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/Server.png?version=2&modificationDate=1609940527272&api=v2)

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/LoraEnabling.png?version=3&modificationDate=1609940543598&api=v2)

  

导航到流量选项卡，监测周围节点发送的请求。

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/Traffic.png?version=2&modificationDate=1609933802611&api=v2)

  

LoRa mini-PCIe卡的基本安装和配置到此结束。有关其他设置，请查看： [General Properties](https://help.mikrotik.com/docs/display/ROS/General+Properties)

