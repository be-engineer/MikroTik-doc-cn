# 连接到路由器

路由器有两种类型:

- 使用默认配置。
- 没有默认配置。当找不到具体配置时,IP地址192.168.88.1/24将设置在ether1或combo1或sfp1上。

有关当前默认配置的更多信息,请参见设备随附的“快速指南”文档。 快速指南文档包括有关首次连接使用哪些端口以及如何插入设备的信息。

本文介绍了如何从头开始设置设备,因此我们将要求你清除所有默认值。

首次使用默认用户名 **admin** 和 **无密码** (对于某些型号,请检查贴纸上的用户密码)连接到路由器时,系统将要求你重置或保留默认配置(即使默认配置仅有一个IP地址)。 由于本文假设路由器上没有配置,你应该在出现提示时按键盘上的“r”或单击WinBox中的“删除配置”按钮将其删除。

## 无默认配置的路由器

如果路由器上没有默认配置，则有几种选择，这里我们将使用一种适合我们需求的方法。

将路由器的 ether1 端口连接到 WAN 电缆并将你的 PC 连接到 ether2。现在打开 WinBox 并在邻居发现中查找你的路由器。请参阅 [Winbox文章](https://help.mikrotik.com/docs/display/ROS/Winbox#Winbox-StartingWinbox) 中的详细示例。

如果你在列表中看到路由器，单击 MAC 地址，然后单击 **连接**。

确保绝对干净的路由器的最简单方法是运行

`/system reset-configuration no-defaults=yes skip-backup=yes`

或者从WinBox (Fig. 1-1):

![Fig. 1-1](https://help.mikrotik.com/docs/download/attachments/328151/winbox_reset.png?version=1&modificationDate=1569855878503&api=v2&effects=drop-shadow "Fig. 1-1")

## 配置IP访问

由于 MAC 连接不是很稳定，我们需要做的第一件事是设置路由器以便 IP 连接可用：

- 添加网桥接口和网桥端口；
- 为 LAN 接口添加 IP 地址；
- 设置一个DHCP 服务器。

设置网桥和 IP 地址非常简单：

`/interface bridge add name=local`

`/interface bridge port add nterface=ether2 bridge=local`

`/ip address add address=192.168.88.1/24 interface=local`

如果你更喜欢WinBox/WeBfig作为配置工具：

- 打开 **Bridge** 窗口，选择 **Bridge** 选项卡；
- 点击 **+** 按钮，将打开一个新对话框，输入网桥名称 **local** 并点击 **OK**；
- 选择 **Port** 选项卡并单 **+** 按钮，将打开一个新对话框；
- 从下拉列表选择接口 **ether2** 和网桥 **local** ，然后单击 **OK** 按钮应用设置；
- 关闭桥接对话框。

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_add_bridge.png?version=1&modificationDate=1569855959279&api=v2&effects=drop-shadow)

- 打开 **Ip -> Address** 对话框；
- 点击 **+** 按钮，打开一个新对话框；
- 输入 IP 地址 **192.168.88.1/24**， 从下拉列表中选择接口 **local** 然后点击 **OK** 按钮；

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_add_ip.png?version=1&modificationDate=1569856045386&api=v2&effects=drop-shadow)

下一步是设置 DHCP 服务器。 运行 **setup** 命令以方便快速地进行配置：

`[admin@MikroTik] /ip dhcp-server setup [enter]`

`Select interface to run DHCP server on`

`dhcp server interface : local [enter]`

`Select network for DHCP addresses`

`dhcp address space : 192.168.88.0/24 [enter]`

`Select gateway for given network`

`gateway for dhcp network : 192.168.88.1 [enter]`

`Select pool of ip addresses given out by DHCP server`

`addresses to give out : 192.168.88.2-192.168.88.254 [enter]`

`Select DNS servers`

`dns servers : 192.168.88.1 [enter]`

`Select lease time`

`lease time : 10m [enter]`

请注意，大多数配置选项都是自动确定的，你只需按回车键即可。

同样的设置工具也可以在 WinBox/WeBfig 中使用：

- 打开 **Ip -> DHCP server** 窗口，选择 **DHCP** 选项卡；
- 点击 **DHCP setup** 按钮，打开一个新对话框，输入 DHCP 服务器接口 **local** 并点击 **Next** 按钮；
- 按照向导完成设置。

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_dhcp_setup.png?version=1&modificationDate=1569856096203&api=v2&effects=drop-shadow)

现在连接的 PC 应该能获得一个动态 IP 地址。 关闭 Winbox 并使用 IP 地址 (192.168.88.1) 重新连接到路由器。

## 配置互联网连接

下一步是让路由器访问互联网。 有多种类型的互联网连接，最常见的是：

- 动态公共IP地址；
- 静态公共 IP 地址；
- PPPoE 连接。

## 动态公共IP地址

动态地址配置是最简单的一种。 只需要在公共接口上设置一个 DHCP 客户端。 DHCP 客户端将接收来自互联网服务提供商 (ISP) 的信息，并为你设置 IP 地址、DNS、NTP 服务器和默认路由。

`/ip dhcp-client add disabled=no interface=ether1`

添加客户端后，应该看到分配的地址和状态应该是绑定的
`[admin@MikroTik] /ip dhcp-client> print`

`Flags: X - disabled, I - invalid`

 `#   INTERFACE           USE ADD-DEFAULT-ROUTE STATUS        ADDRESS`

 `0   ether1               yes yes               bound         1.2.3.100/24`

## 静态公共IP地址

在静态地址配置的情况下，ISP 会提供参数，例如：

- IP：1.2.3.100/24
- gateway：1.2.3.1
- DNS：8.8.8.8

这些是让互联网连接正常工作所需的三个基本参数

要在 RouterOS 中进行设置，要手动添加一个IP地址，使用提供的网关添加默认路由，并设置 DNS 服务器

`/ip address add address=1.2.3.100/24 interface=ether1`

`/ip route add gateway=1.2.3.1`

`/ip dns set servers=8.8.8.8`

## PPPoE连接

PPPoE 连接也提供一个动态 IP 地址，并可以动态配置 DNS 和默认网关。 通常服务提供商 (ISP) 会提供连接的用户名和密码

`/interface pppoe-client`

  `add disabled=no interface=ether1 user=me password=123 \`

    `add-default-route=yes use-peer-dns=yes`

Winbox/Webfig 操作：

- 打开 **PPP** 窗口，应选择 **Interfaces** 选项卡；
- 点击 **+** 按钮，从下拉列表中选择 **PPPoE客户端**，打开一个新对话框；
- 从下拉列表中选择接口 **ether1**，然后单击 **OK** 按钮应用设置。
  
![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_add_pppoe.png?version=1&modificationDate=1569856189121&api=v2&effects=drop-shadow)

> 此外，在配置中， **WAN** 口现在是 **pppoe-out** 接口，而不是 **ether1**。

## 验证连接

配置成功后，应该可以从路由器访问互联网了。

通过 ping 已知 IP 地址来验证 IP 连接（例如谷歌 DNS 服务器）

`[admin@MikroTik] > /ping 8.8.8.8`

`HOST                                     SIZE TTL TIME  STATUS`

`8.8.8.8                                    56  47 21ms`

`8.8.8.8                                    56  47 21ms`

验证DNS请求

`[admin@MikroTik] > /ping www.google.com`

`HOST                                     SIZE TTL TIME  STATUS`

`173.194.32.49                              56  55 13ms`

`173.194.32.49                              56  55 12ms`

如果设置正确，两种情况下的 ping 都不会失败。

如果失败，请参考 [故障排除](https://10.55.8.167/?t=ros_v7&c=1&a=configuring#Troubleshooting) 部分

## 保护路由器

现在世界上任何人都可以访问我们的路由器，因此现在是保护它免受入侵者和基本攻击的最佳时机

## 用户密码访问

MikroTik 路由器需要配置密码，我们建议使用密码生成器工具来创建安全且不重复的密码。 对于安全密码，我们的意思是：

- 至少 12 个字符；
- 包括数字、符号、大写和小写字母；
- 不是词典中的单词或单词的组合；

`/user set 0 password= "!={Ba3N!40TуX+GvKBzjTLIUcx/,"`

设置密码的另一个选项，

我们强烈建议使用第二种方法或 Winbox 界面为你的路由器应用新密码，只是为了防止其他未经授权的访问。

`[admin@MikroTik] > / password`

`old password:`

`new password: ******`

`retype new password: ******`

请务必记住密码！ 如果忘记了就无法恢复。 只能重新安装路由器！

可以在 **/user** 菜单中添加更多具有完全或有限路由器访问权限的用户

> 最佳做法是添加一个具有强密码的新用户，并禁用或删除默认的 **admin** 用户。

`/user add name=myname password=mypassword group=full`

`/user remove admin`

> **注意：** 使用新凭据登录路由器以检查用户名/密码是否有效。

## MAC地址连接访问

默认情况下，mac 服务器在所有接口上运行，因此将禁用默认的 **所有** 条目并添加一个本地接口以禁止来自 WAN 端口的 MAC 连接。 MAC Telnet 服务器功能允许你对接口“列表”加限制。

首先，创建一个接口列表：

`[admin@MikroTik] > /interface list add name=listBridge`

然后，将你之前创建的名为“local”的网桥添加到接口列表中：

`[admin@MikroTik] > /interface list member add list=listBridge interface=local`

将新创建的（接口）“列表”应用到 MAC 服务器：

`[admin@MikroTik] > tool mac-server set allowed-interface-list=listBridge`

对 Winbox MAC 访问做同样的事情

`[admin@MikroTik] > tool mac-server mac-winbox set allowed-interface-list=listBridge`

Winbox/Webfig 操作：

- 打开 **Interfaces → Interface List → Lists** 窗口并点击“+”添加新列表；
- 在 **Name** 字段中输入接口列表名称“listBridge”，然后单击 **确定** ；
- 返回 **Interfaces →** **Interfaces list**部分并点击“+”；
- 从下拉 **List** 选项中选择“listBridge”，然后从下拉 **Interfaces** 选项中选择“local”，然后单击 **OK**；
- 打开 **Tools -> Mac Server** 窗口；
- 单击 **“MAC Telnet Server”** 按钮，将打开一个新对话框；
- 从下拉列表中选择新创建的列表“listBridge”，然后单击 **OK** 按钮应用设置。

![](https://help.mikrotik.com/docs/download/attachments/328151/image2021-12-7_9-59-33.png?version=1&modificationDate=1638863965880&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/328151/image2021-12-7_11-3-20.png?version=1&modificationDate=1638867793584&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/328151/image2021-12-7_10-4-32.png?version=1&modificationDate=1638864265017&api=v2)

在 **MAC** **Winbox Server** 选项卡中执行相同的操作以阻止来自 Internet 的 Mac Winbox 连接。

## 邻居发现协议

MikroTik 邻居发现协议用于显示和识别网络中的其他 MikroTik 路由器。可以在公共接口上禁用邻居发现：

`/ip neighbor discovery-settings set discover-interface-list=listBridge`

## IP连接访问

除了防火墙保护你的路由器免受来自外部网络的未经授权访问之外，还可以限制特定 IP 地址的用户名访问

`/user set 0 allowed-address=x.x.x.x/yy`

_x.x.x.x/yy - 允许访问路由器的 IP 和子网。_

公共接口上的 IP 连接必须在防火墙中受到限制。 只接受 ICMP(ping/traceroute)、IP Winbox 和 ssh 访问。

`/ip firewall filter`

  `add chain=input connection-state=established,related action=accept comment="accept established,related" ;`

  `add chain=input connection-state=invalid action=drop ;`

  `add chain=input in-interface=ether1 protocol=icmp action=accept comment="allow ICMP" ;`

  `add chain=input in-interface=ether1 protocol=tcp port=8291 action=accept comment="allow Winbox" ;`

  `add chain=input in-interface=ether1 protocol=tcp port=22 action=accept comment="allow SSH" ;`

  `add chain=input in-interface=ether1 action=drop comment="block everything else" ;`

> 如果公共接口是 pppoe，则输入接口应设置为“pppoe-out”。

前两个规则接受来自已建立连接的数据包，假设这些规则不会使 CPU 过载。 第三条规则丢弃任何连接跟踪认为无效的数据包。 之后，我们为特定协议设置典型的接受规则。

如果你使用 Winbox/Webfig 进行配置，这里是一个如何添加已建立/相关规则的示例：

- 打开 **Ip -> Firewall**窗口, 点击 **Filter rules** 标签;
- 点击 **+** 按键, 打开一个新的对话框;
- 选择chain input, 点击 **Connection state,** 选择 **established** 和 **related** 复选框;
- 点击 **Action** 标签，确保 **action accept** 被选中;
- 点击 **Ok** 按钮应用设置.

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_ip_fw.png?version=1&modificationDate=1569856324140&api=v2&effects=drop-shadow)

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_ip_fw_add_est.png?version=1&modificationDate=1569856350353&api=v2&effects=drop-shadow)

要添加其他规则，请为每个新规则单击 **+** 并填写控制台示例中提供的相同参数。

## 管理服务

虽然防火墙保护了路由器的公共接口不受影响，但你可能仍希望禁用 RouterOS 服务。

大多数 RouterOS 管理工具都在 /ip 服务菜单中配置

只保留安全的，

`/ip service disable telnet,ftp,www,api`

更改默认服务端口，这将立即停止大多数随机 SSH 暴力登录尝试：

`/ip service set ssh port=2200`

此外，每个服务都可以通过允许的 IP 地址或地址范围（地址服务将回复的地址）来保护，尽管更可取的方法是在防火墙中阻止不需要的访问，因为防火墙不允许打开套接字

`/ip service set winbox address=192.168.88.0/24`

## 其他服务

带宽服务器用于测试两个 MikroTik 路由器之间的吞吐量。 在生产环境中最好禁用。

`/tool bandwidth-server set enabled=no`

路由器可能启用了 DNS 缓存，这减少了从客户端到远程服务器的 DNS 请求的解析时间。 如果你的路由器不需要 DNS 缓存或其他路由器用于此类目的，请禁用。

`/ip dns set allow-remote-requests=no`
  
一些 RouterBOARD 有一个 LCD 模块用于信息显示，可以设置引脚或禁用它。
  
最好禁用路由器上所有未使用的接口，以减少对路由器的非法访问。

`/interface print`

`/interface set x disabled=yes`

其中“X”是一些未使用接口的编号。

RouterOS 为 SSH 使用更强的加密，大多数较新的程序都使用它，要打开 SSH 强加密：

`/ip ssh set strong-crypto=yes`

默认情况下禁用以下服务，最好确保没有意外启用这些服务：

- MikroTik 缓存代理，

- MikroTik socks代理，

- MikroTik UPNP 服务，

- MikroTik 动态名称服务或 IP 云服务，

`/ip cloud set ddns-enabled=no update-time=no`

## NAT配置

此时，PC 还不能访问 Internet，因为本地使用的地址无法通过 Internet 路由。 远程主机根本不知道如何正确回复本地地址。

解决办法是将传出数据包的源地址更改为路由器公共 IP。 通过 NAT 规则来完成：

`/ip firewall nat`

  `add chain=srcnat out-interface=ether1 action=masquerade`

> 如果公共接口是 pppoe，则输出接口应设置为“pppoe-out”。

该设置的另一个好处是路由器后面的 NAT 客户端不直接连接到 Internet，这样就不需要额外的保护来抵御来自外部的攻击。

## 转发端口

某些客户端设备可能需要通过特定端口直接访问互联网。 例如，IP 地址为 192.168.88.254 的客户端必须通过远程桌面协议 (RDP) 访问。

在谷歌上快速搜索发现 RDP 运行在 TCP 端口 3389 上。可以添加目标 NAT 规则以将 RDP 重定向到客户端的 PC。

`/ip firewall nat`

  `add chain=dstnat protocol=tcp port=3389 in-interface=ether1 \`

    `action=dst-nat to-address=192.168.88.254`

> 如果设置了严格的防火墙规则，则防火墙过滤器转发链中必须允许 RDP 协议。

## 设置无线

为了便于使用，要进行无线桥接设置，使有线主机与无线客户端位于相同的以太网广播域中。

重要的是确保无线网络受到保护，因此第一步是安全配置文件。

安全配置文件是从终端中的“/interface wireless security-profiles”菜单配置的。

`/interface wireless security-profiles`

  `add name=myProfile authentication-types=wpa2-psk mode=dynamic-keys \`

    `wpa2-pre-shared-key=1234567890`

在 Winbox/Webfig 中点击 **Wireless** 打开无线窗口并选择 **Security Profile** 选项卡。

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_wlan_sec_profile.png?version=1&modificationDate=1569856421347&api=v2&effects=drop-shadow)

如果有不支持 WPA2 的旧设备（如 Windows XP），可能还要允许 WPA 协议。

> WPA 和 WPA2 预共享密钥最好不同。

现在，当安全配置文件准备好后，就可以启用无线接口并设置所需的参数

`/interface wireless`

  `enable wlan1;`

  `set wlan1 band=2ghz-b/g/n channel-width=20/40mhz-Ce distance=indoors \`

    `mode=ap-bridge ssid=MikroTik-006360 wireless-protocol=802.11 \`

    `security-profile=myProfile frequency-mode=regulatory-domain \`

    `set country=latvia antenna-gain=3`

- 打开无线窗口，选择 wlan1 接口，然后点击 _enable_ 按钮；
- 双击无线接口打开配置对话框；
- 在配置对话框中单击 **Wireless** 选项卡，然后单击右侧的 **Advanced Mode** 按钮。 当你单击该按钮时，将出现其他配置参数，并且该按钮的描述将更改为 **Simple Mode**；
- 选择屏幕截图中显示的参数，国家设置和 SSID 除外。 可能还要选择不同的频率和天线增益；
- 接下来，单击 **HT** 选项卡并确保选择了两个chain；
- 单击 **OK** 按钮应用设置。

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_wlan_iface.png?version=1&modificationDate=1569856463320&api=v2&effects=drop-shadow)

最后一步是把无线接口添加到本地网桥，否则连接的客户端无法获得 IP 地址：

`/interface bridge port`

  `add interface=wlan1 bridge=local`

现在无线客户端应该能够连接到你的接入点、获取 IP 地址并访问互联网。

## 保护客户

现在要为 LAN 客户端添加一些保护。 从一组基本规则开始。

`/ip firewall filter`

  `add chain=forward action=fasttrack-connection connection-state=established,related \`

    `comment= "fast-track for established,related" ;`

  `add chain=forward action=accept connection-state=established,related \`

    `comment= "accept established,related" ;`

  `add chain=forward action=drop connection-state=invalid`

  `add chain=forward action=drop connection-state=new connection-nat-state=!dstnat \`

    `in-interface=ether1 comment= "drop access to clients behind NAT from WAN"`

规则集类似于输入链规则（接受已建立或相关的并丢弃无效的），除了第一个带有“action=fasttrack-connection”的规则。 此规则允许已建立的相关连接绕过防火墙并显著降低 CPU 使用率。

另一个区别是最后一条规则会丢弃所有从 WAN 口到 LAN 网络的新连接尝试（除非使用 DstNat）。 如果没有这条规则，攻击者知道或猜到你的本地子网，就可以直接与本地主机建立连接并造成安全威胁。

有关如何构建防火墙的更多详细示例将在防火墙部分讨论，或直接查看 [建立第一个防火墙](https://help.mikrotik.com/docs/display/ROS/Building+Your+First+Firewall) 。

## 阻止不需要的网站

有时你可能想要阻止某些网站，例如，拒绝员工访问娱乐网站、拒绝访问色情网站等。 这可以通过将 HTTP 流量重定向到代理服务器并使用访问列表来允许或拒绝某些网站来实现。

首先，我们需要添加一个 NAT 规则来将 HTTP 重定向到我们的代理。 我们将使用运行在端口 8080 上的 RouterOS 内置代理服务器。

`/ip firewall nat`

  `add chain=dst-nat protocol=tcp dst-port=80 src-address=192.168.88.0/24 \`

    `action=redirect to-ports=8080`

启用网络代理并删除一些网站：

`/ip proxy set enabled=yes`

`/ip proxy access add dst-host=www.facebook.com action=deny`

`/ip proxy access add dst-host=*.youtube.* action=deny`

`/ip proxy access add dst-host=:vimeo action=deny`

使用 Winbox：

- 在左侧菜单导航到 IP -> Web Proxy
- 将出现 Web Proxy设置对话框。
- 选中“Enable”复选框并单击“Apply”按钮
- 然后单击“Access”按钮打开“Web Proxy访问”对话框

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_ip_web_proxy.png?version=1&modificationDate=1569856600346&api=v2&effects=drop-shadow)

- 在“Web Proxy Access”对话框中单击“+”以添加新的 Web 代理规则
- 输入你要阻止的 Dst 主机名，在本例中为“[www.facebook.com](https://www.facebook.com/)”，选择action“deny”
- 然后单击“OK”按钮应用更改。
- 重复相同的操作以添加其他规则。

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_ip_web_proxy_access.png?version=1&modificationDate=1569856640042&api=v2&effects=drop-shadow)

## 故障排除

RouterOS 内置了各种故障排除工具，如 ping、traceroute、torch、数据包嗅探器、带宽测试等。

前面已经使用本文中的 ping 工具来 [验证互联网连接](https://help.mikrotik.com/docs/display/ROS/First+Time+Configuration#FirstTimeConfiguration-VerifyConnectivity).

## 如果 ping 失败，需要进行故障排除

ping 工具只说目的地是 **unreachable**，但没有更详细的信息可用。 只是让我们了解基本错误。

无法从连接到 MikroTik 设备的计算机访问 [www.google.com](https://www.google.com/)：

![](https://help.mikrotik.com/docs/download/attachments/328151/troubleshoot_if_ping_fails.jpg?version=1&modificationDate=1582275155077&api=v2)

> 如果不确定如何配置网关设备，请联系 MikroTik 的官方 [顾问](https://mikrotik.com/consultants) 以获得配置支持。
