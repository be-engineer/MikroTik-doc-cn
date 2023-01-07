# 介绍

Netinstall 是一个用于安装或重装 RouterOS 的 MikroTik 设备的工具。 如果怀疑设备无法正常工作，请始终尝试使用 Netinstall。 该工具可用于 Windows（带有图形界面）和 Linux（作为命令行工具）。

简而言之，Netinstall 过程如下： 将您的 PC 直接连接到您要重新安装的设备的 **boot** 端口（通常是 Ether1，标记为 BOOT 或产品手册中另有说明的端口）。 在按住 **reset** 按钮的同时打开设备，直到它出现在 Netinstall 工具中。

!!! warning 注意。 Netinstall 会格式化系统驱动器，所有配置和保存的文件都将丢失。 Netinstall 不会擦除 RouterOS 许可证密钥，也不会重置 RouterBOOT 相关设置，例如，重装设备后 CPU 频率不会改变。

# 适用于 Windows 的说明

- 从[下载](https://mikrotik.com/download) 页面下载**Netinstall**。 如果不确定需要哪个版本，可以选择标记为**Current**（稳定）的版本；
- 从[下载](https://mikrotik.com/download) 页面下载 RouterOS **主包**；
    
     !!!success 您必须选择 RouterOS 版本。 始终可以选择标记为**Current**的版本。 您还必须选择架构（ARM、MIPS、SMIPS、TILE 等...），但如果您不确定，那么您可以下载适用于**所有**架构的 RouterOS 包，Netinstall 将为您选择正确的架构。
    
- 断开计算机与 WiFi、以太网、LTE 或任何其他类型的连接！ Netinstall 只能在您计算机上的一个活动接口上运行，强烈建议您断开任何其他网络接口，以确保 Netinstall 将选择正确的网络接口。
    
- 为您的以太网接口配置一个静态 IP 地址，打开 **Start**，然后选择 **Settings**：
    

![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_4.png?version=1&modificationDate=1587384029368&api=v2)

!!!success Netinstall 也可以在本地网络上运行，在这种情况下您可以跳过设置静态 IP 地址，但如果您不熟悉 Netinstall，强烈建议您设置静态 IP 地址。

- 打开**Network&Internet**并选择**Change adapter options**

![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_5.png?version=1&modificationDate=1587384914250&api=v2)![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_6.png?version=1&modificationDate=1587385041755&api=v2)

- 右键单击您的以太网接口并选择**Properties**

![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_7.png?version=1&modificationDate=1587385120369&api=v2)

-   选择 **Internet Protocol Version 4 (TCP/IPv4)** 并点击 **Properties**

**![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_8.png?version=1&modificationDate=1587385250640&api=v2)**

- 选中使用以下 IP 地址并填写如下图所示的字段

**![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_9.png?version=1&modificationDate=1587385330268&api=v2)**

!!! warning 如果您有可用的路由器，则可以使用它并跳过本教程的设置静态 IP 部分，但需要知道 LAN 地址，因为需要在网络中为网络指定一个未使用的 IP 地址引导服务器。 因此，如果不确定如何从网络中获取这些参数，建议使用静态 IP 地址并严格遵循本指南。

- 打开您的下载文件夹（或保存下载文件的位置）并将 Netinstall.zip文件解压缩到一个方便的地方

![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_1.png?version=1&modificationDate=1587385508581&api=v2)![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_2.png?version=1&modificationDate=1587385541664&api=v2)

- 确保以太网接口已经启用，启动 Netinstall.exe。 如果您严格按照指南进行操作，那么您的计算机上应该没有任何互联网连接，Windows 10 想要验证它运行的所有应用程序，但由于缺少互联网连接而无法执行此操作，因此，可能会弹出警告，请单击**Run**。
    

![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_10.png?version=1&modificationDate=1587385638572&api=v2)

!!!warning Netinstall 需要管理员权限，应该有一个窗口询问运行 Netinstall 的权限，必须接受这些权限才能使 Netinstall 正常工作。

- 允许在**Public** 网络中访问 Netinstall 并配置**Net booting**设置并填写必填字段，如下图所示

![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_11.png?version=2&modificationDate=1587385766358&api=v2)![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_12.png?version=1&modificationDate=1587385770397&api=v2)

!!!warning 客户端 IP 地址必须是唯一的！ 不要使用网络中现有的 IP 地址，这也意味着不能用和计算机相同的 IP 地址。 要使用同一子网的不同的 IP 地址。

- 使用以太网线将设备连接到计算机（中间不能有任何其他设备），将以太网线插入设备的 Etherboot 端口。
- MikroTik 设备能够从 **第一个** 端口（Ether1）或标有“**BOOT**”的端口使用 Netinstall。
  
![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_18.png?version=1&modificationDate=1587385958852&api=v2)

!!!warning 有些计算机的网络接口（尤其是 USB 以太网适配器）往往会产生额外的链路抖动，这足以让 Netinstall 无法检测到处于 Etherboot 模式的设备。 在这种情况下，您可以在您的设备和计算机之间使用交换机或使用桥接模式的路由器来防止出现此问题。

- 启动您的设备并将其置于Etherboot模式

!!!success 有多种方法可以让您的设备进入 Etherboot 模式。 在尝试将设备置于此模式之前，请务必阅读 Etherboot 手册。 方法因不同的 MikroTik 设备而异。

- 等待设备出现在 Netinstall 中，选择它并按**Browse.**。转到**Downloads**文件夹（或保存 RouterOS 包的任何位置）并按**OK**

**![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_13.png?version=1&modificationDate=1587387085890&api=v2)**![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_14.png?version=2&modificationDate=1587387136017&api=v2)

- 选择所需的 RouterOS 版本并按**Install**等待安装完成并按“**Reboot**”（没有串行控制台的设备必须手动重启）

!!!warning 如果您下载了多种架构的 RouterOS 包，那么 Netinstall 只会在您选择后显示适合您设备的架构包。 选择设备后，所有不受支持的包都不会显示在此窗口中。

**![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_15.png?version=1&modificationDate=1587387289302&api=v2)![](https://help.mikrotik.com/docs/download/attachments/24805390/Netinstall_Win10_17.png?version=1&modificationDate=1587387292639&api=v2)**

如果安装没有开始（进度条没有移动或没有显示任何状态），那么可以尝试关闭 Netinstall 应用程序并再次打开它，或者尝试再次将设备置于 Etherboot 模式。 如果您仍然无法让 Netinstall 工作，那您应该尝试在另一台计算机上使用它，因为可能是操作系统的问题导致 Netinstall 无法正常工作。

- 完成！ 断开设备电源，拔下以太网线，将设备接入网络中，您的设备现在应该可以正常运行了！

!!!info 使用 Netinstall 后，设备将重置为默认值（除非您指定不应用默认配置）。 出于安全原因，某些设备无法通过具有默认配置的 **ether1** 端口访问。 请阅读有关[默认配置]（https://wiki.mikrotik.com/wiki/Manual:Default_Configurations“Manual:Default Configurations”）的更多信息。

!!!success 使用**Configure script**选项时，建议在配置执行前加一个[延迟](https://wiki.mikrotik.com/wiki/Manual:Configuration_Management#Startup_delay)。

# Linux 说明

Linux 版本是一个命令行工具，它提供和 Windows 版本几乎相同的参数。

从我们的下载页面下载该工具：

```
wget https://download.mikrotik.com/routeros/[VERSION]/netinstall-[VERSION].tar.gz
```

解压:

```
tar -xzf netinstall-[VERSION].tar.gz
```

运行工具:

```
./netinstall-cli -a 192.168.0.1 routeros-arm64-[VERSION].npk
```

该工具需要特权访问，必须以 root 身份运行，请使用 sudo。

可用参数如下：

| 参数           | 含义                                                                                                                                                                             |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| \-r            | 在重新安装过程中重置配置，可选                                                                                                                                                   |
| \-k keyfile    | 为设备提供许可证密钥（.KEY 格式的密钥文件），可选                                                                                                                                |
| \-s userscript | 使用提供的配置文件（.RSC 格式的文本文件）预配置设备，可选                                                                                                                        |
| \-a IP         | 使用 Netinstall 服务器分配给设备的特定 IP 地址，强制                                                                                                                             |
| PACKAGE        | 指定 Netinstall 将在设备上安装的 RouterOS.NPK 格式包列表，强制                                                                                                                   |
| -i             | **_starting from Release 7.7beta8_** <br>允许使用多个 NIC 指定主机上 netinstall 要运行的接口。 (sudo ./netinstall-cli -i <interface> -r -a 192.168.88.3 routeros-7.5-mipsbe.npk) |
|                |

首先确保您已经在计算机接口上设置了 IP：

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">admin@ubuntu:~$ sudo ifconfig &lt;interface&gt; 192.168.88.2/24</code></div></div></td></tr></tbody></table>

然后运行 Netinstall 版本 6（下面是重新安装过程中重置配置的一个示例）：

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">admin@ubuntu:~$ sudo ./netinstall -r -a 192.168.88.3 routeros-mipsbe-6.48.1.npk</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Using server IP: 192.168.88.2</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Starting PXE server</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">Waiting for RouterBOARD...</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">PXE client: 01:23:45:67:89:10</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text plain">Sending image: mips</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain">Discovered RouterBOARD...</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text plain">Formatting...</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text plain">Sending package routeros-mipsbe-6.48.1.npk ...</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text plain">Ready for reboot...</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="text plain">Sent reboot command</code></div></div></td></tr></tbody></table>

运行 Netinstall 版本 7（下面是重新安装过程中重置配置的一个示例）：


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">admin@ubuntu:~$ sudo ./netinstall-cli -r -a 192.168.88.3 routeros-7.5-mipsbe.npk</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Version: 7.5 (2022-08-30 09:34:59)</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">Using server IP: 192.168.88.2</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">Use Netmask: 255.255.255.0</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">Starting PXE server</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text plain">Waiting for RouterBOARD...</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain">PXE client: C4:AD:34::89:10</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text plain">Sending image: mips</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text plain">Discovered RouterBOARD...</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text plain">Formatting...</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="text plain">Sending package routeros-mipsbe-7.5.npk ...</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="text plain">Ready for reboot...</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="text plain">Sent reboot command</code></div></div></td></tr></tbody></table>

# Etherboot

Etherboot 模式是 MikroTik 设备的一种特殊状态，允许使用 [Netinstall](https://help.mikrotik.com/docs/display/ROS/Netinstall) 重新安装设备。 根据使用的设备，有多种方法可以让设备进入 Etherboot 模式。

## 复位按钮

**Reset**按钮可以在所有 MikroTik 设备上找到，此按钮用于将设备置于 Etherboot 模式。 使用 **Reset** 按钮将设备置于 Etherboot 模式的一种简单方法是关闭设备电源，在按住 **Reset** 按钮的同时打开设备并保持按住，直到设备出现在 **Netinstalll** 窗口中。

![](https://help.mikrotik.com/docs/download/attachments/24805390/262_hi_res.png?version=1&modificationDate=1587460761021&api=v2)

!!!warning 如果您设置了[受保护的引导加载程序](https://help.mikrotik.com/docs/display/ROS/RouterBOARD#RouterBOARD-Protectedbootloader)，则重置按钮的行为会发生变化。 确保记住用于设置受保护引导加载程序的设置，否则您将无法使用 Eterboot 模式，也无法重置您的设备。

## RouterOS

如果设备能够启动并且能够登录，则可以轻松地将设备置于 Etherboot 模式。 为此，只需连接到设备并执行以下命令：

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system routerboard settings </code><code class="ros functions">set </code><code class="ros value">boot-device</code><code class="ros plain">=try-ethernet-once-then-nand</code></div></div></td></tr></tbody></table>

  
之后，重新启动设备或对设备重新上电。 下次设备启动时，它将首先尝试进入 Etherboot 模式。 请注意，在**首次**启动后，设备不会尝试进入 Etherboot 模式，而是直接从 NAND 或设备正在使用的存储启动。

## 串行控制台

有些设备带有串行控制台，可用于将设备置于 Etherboot 模式。 为此，请确保已经配置计算机的串行控制台。 所有 MikroTik 设备（RouterBOARD 230 系列除外）所需的参数如下：


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">115200bit</code><code class="ros constants">/s, 8 data bits, 1 stop bit, no parity, flow control=none by default.</code></div></div></td></tr></tbody></table>

RouterBOARD 230系列设备参数如下：

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">9600bit</code><code class="ros constants">/s, 8 data bits, 1 stop bit, no parity, hardware (RTS/CTS) flow control by default.</code></div></div></td></tr></tbody></table>

确保您使用的是正确的空调制解调器线，您可以在 [此处](https://help.mikrotik.com/docs/display/ROS/Serial+Console) 找到正确的引脚定义。 当设备启动时，继续按键盘上的 **CTRL+E** 直到设备显示它正在**trying bootp protocol**：

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">RouterBOOT booter 6.42.3</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">CRS125-24G-1S</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">CPU frequency</code><code class="ros constants">: 600 MHz</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">Memory speed</code><code class="ros constants">: 175 MHz</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">Memory size</code><code class="ros constants">: 128 MiB</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">NAND size</code><code class="ros constants">: 128 MiB</code></div><div class="line number9 index8 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">Press any key within 2 seconds to enter setup</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">Ethernet link absent...</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">trying bootp protocol.....................</code></div></div></td></tr></tbody></table>

此时您的设备处于 Etherboot 模式，现在该设备应该显示在 Netinstall 窗口中。