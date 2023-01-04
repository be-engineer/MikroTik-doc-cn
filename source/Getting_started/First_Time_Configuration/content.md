## 连接到路由器

路由器有两种类型:

- 使用默认配置。
- 没有默认配置。如果找不到特定的配置,则在ether1或combo1或sfp1上设置IP地址192.168.88.1/24。

有关当前默认配置的更多信息,请参见设备随附的“快速指南”文档。 快速指南文档将包括有关首次使用哪些端口以及如何插入设备的信息。

本文档介绍了如何从头开始设置设备,因此我们将要求您清除所有默认值。

首次使用默认用户名**admin**和**no password**(对于某些型号,请检查贴纸上的用户密码)连接到路由器时,系统将要求您重置或保留默认配置(即使默认配置仅具有IP地址)。 由于本文假设路由器上没有配置,因此应在出现提示时按键盘上的“ r”或单击WinBox中的“删除配置”按钮将其删除。

## 路由器没有默认配置

如果路由器上没有默认配置，您有多种选择，但在这里我们将使用适合我们需要的一种方法。

将路由器的 ether1 端口连接到 WAN 电缆并将您的 PC 连接到 ether2。现在打开 WinBox 并在邻居发现中查找您的路由器。请参阅[Winbox文章](https://help.mikrotik.com/docs/display/ROS/Winbox#Winbox-StartingWinbox)中的详细示例。

如果您在列表中看到路由器，请单击 MAC 地址，然后单击**连接**。

确保您拥有绝对干净的路由器的最简单方法是运行

`/system` `reset-configuration` `no-defaults``=yes` `skip-backup``=yes`

或者从WinBox (Fig. 1-1):

![Fig. 1-1](https://help.mikrotik.com/docs/download/attachments/328151/winbox_reset.png?version=1&modificationDate=1569855878503&api=v2&effects=drop-shadow "Fig. 1-1")

## 配置IP访问

由于 MAC 连接不是很稳定，我们需要做的第一件事是设置路由器以便 IP 连接可用：

- 添加网桥接口和网桥端口；
- 为 LAN 接口添加 IP 地址；
- 设置 DHCP 服务器。

设置网桥和 IP 地址非常简单：

`/interface bridge` `add` `name``=local`

`/interface bridge port` `add` `interface``=ether2` `bridge``=local`

`/ip address` `add` `address``=192.168.88.1/24` `interface``=local`

如果您更喜欢 WinBox/WeBfig 作为配置工具：

- 打开**Bridge** 窗口，应选择**Bridge** 选项卡；
- 点击+按钮，将打开一个新对话框，输入网桥名称**local**并点击**OK**；
- 选择端”选项卡并单+按钮，将打开一个新对话框；
- 选择接口 **ether2** 和网桥 **local** 形成下拉列表，然后单击 **OK** 按钮应用设置；
- 您可以关闭桥接对话框。

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_add_bridge.png?version=1&modificationDate=1569855959279&api=v2&effects=drop-shadow)

- 打开 **Ip -> Address** 对话框；
- 点击**+**按钮，将打开一个新对话框；
- 输入 IP 地址 **192.168.88.1/24** 从下拉列表中选择接口 **local** 然后点击 **OK** 按钮；

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_add_ip.png?version=1&modificationDate=1569856045386&api=v2&effects=drop-shadow)

下一步是设置 DHCP 服务器。 我们将运行 **setup** 命令以方便快速地进行配置：

`[admin@MikroTik]` `/ip dhcp-server` `setup` `[enter]`

`Select interface to run DHCP server on`

`dhcp server interface``:` `local` `[enter]`

`Select network` `for` `DHCP addresses`

`dhcp address space``: 192.168.88.0/24 [enter]`

`Select gateway` `for` `given network`

`gateway` `for` `dhcp network``: 192.168.88.1 [enter]`

`Select pool of ip addresses given out by DHCP server`

`addresses to give out``: 192.168.88.2-192.168.88.254 [enter]`

`Select DNS servers`

`dns servers``: 192.168.88.1 [enter]`

`Select lease time`

`lease time``: 10m [enter]`

请注意，大多数配置选项都是自动确定的，您只需按回车键即可。

同样的设置工具也可以在 WinBox/WeBfig 中使用：

- 打开 **Ip -> DHCP 服务器** 窗口，应选择 **DHCP** 选项卡；
- 点击 **DHCP 设置** 按钮，将打开一个新对话框，输入 DHCP 服务器界面 **本地** 并点击 **下一步** 按钮；
- 按照向导完成设置。

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_dhcp_setup.png?version=1&modificationDate=1569856096203&api=v2&effects=drop-shadow)

现在连接的 PC 应该能够获得动态 IP 地址。 关闭 Winbox 并使用 IP 地址 (192.168.88.1) 重新连接到路由器

## 配置互联网连接

下一步是让路由器访问互联网。 可以有多种类型的互联网连接，最常见的是：

- 动态公共IP地址；
- 静态公共 IP 地址；
- PPPoE 连接。

## 动态公共IP地址

动态地址配置是最简单的一种。 您只需要在公共接口上设置一个 DHCP 客户端。 DHCP 客户端将从互联网服务提供商 (ISP) 接收信息，并为您设置 IP 地址、DNS、NTP 服务器和默认路由。

`/ip dhcp-client` `add` `disabled``=no` `interface``=ether1`

添加客户端后，应该看到分配的地址和状态应该是绑定的
`[admin@MikroTik] /ip dhcp-client> print`

`Flags: X - disabled, I - invalid`

 `#   INTERFACE           USE ADD-DEFAULT-ROUTE STATUS        ADDRESS`

 `0   ether1               yes yes               bound         1.2.3.100/24`

## 静态公共IP

在静态地址配置的情况下，您的 ISP 会为您提供参数，例如：

- IP：1.2.3.100/24
- 网关：1.2.3.1
- DNS：8.8.8.8

这些是使互联网连接正常工作所需的三个基本参数

要在 RouterOS 中进行设置，我们将手动添加 IP 地址，使用提供的网关添加默认路由，并设置 DNS 服务器

`/ip address` `add` `address``=1.2.3.100/24` `interface``=ether1`

`/ip route` `add` `gateway``=1.2.3.1`

`/ip dns` `set` `servers``=8.8.8.8`

## PPPoE连接

PPPoE 连接还为您提供动态 IP 地址，并可以动态配置 DNS 和默认网关。 通常服务提供商 (ISP) 会为您提供连接的用户名和密码

`/interface pppoe-client`

  `add` `disabled``=no` `interface``=ether1` `user``=me` `password``=123` `\`

    `add-default-route``=yes` `use-peer-dns``=yes`

Winbox/Webfig 操作：

- 打开 **PPP** 窗口，应选择 **Interfaces** 选项卡；
- 点击**+**按钮，从下拉列表中选择**PPPoE客户端**，新对话框将打开；
- 从下拉列表中选择接口 **ether1**，然后单击 **OK** 按钮应用设置。
  
![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_add_pppoe.png?version=1&modificationDate=1569856189121&api=v2&effects=drop-shadow)

!!! warning 进一步配置 **WAN** 接口，现在是 **pppoe-out** 接口，而不是 **ether1**。

## 验证连接

配置成功后，应该可以从路由器访问互联网。

通过 ping 已知 IP 地址验证 IP 连接（例如谷歌 DNS 服务器）

`[admin@MikroTik] > /ping 8.8.8.8`

`HOST                                     SIZE TTL TIME  STATUS`

`8.8.8.8                                    56  47 21ms`

`8.8.8.8                                    56  47 21ms`

验证DNSi请求

`[admin@MikroTik] > /ping www.google.com`

`HOST                                     SIZE TTL TIME  STATUS`

`173.194.32.49                              56  55 13ms`

`173.194.32.49                              56  55 12ms`

如果一切设置正确，在这两种情况下 ping 应该不会失败。

如果失败，请参考[故障排除](https://10.55.8.167/?t=ros_v7&c=1&a=configuring#Troubleshooting)部分

## 保护路由器

现在世界上任何人都可以访问我们的路由器，因此现在是保护它免受入侵者和基本攻击的最佳时机

## 用户密码访问

MikroTik 路由器需要配置密码，我们建议使用密码生成器工具来创建安全且不重复的密码。 对于安全密码，我们的意思是：

- 至少 12 个字符；
- 包括数字、符号、大写和小写字母；
- 不是词典词或词典词的组合；

`/user` `set` `0` `password``=``"!={Ba3N!40TуX+GvKBzjTLIUcx/,"`

设置密码的另一个选项，

我们强烈建议使用第二种方法或 Winbox 界面为您的路由器应用新密码，只是为了防止其他未经授权的访问。

`[admin@MikroTik] > / password`

`old password:`

`new password: ******`

`retype new password: ******`

请务必记住密码！ 如果您忘记了它，则无法恢复。 您将需要重新安装路由器！

您还可以在 **/user** 菜单中添加更多具有完全或有限路由器访问权限的用户

!!! success 最佳做法是添加一个具有强密码的新用户，并禁用或删除默认的 **admin** 用户。

`/user` `add` `name``=myname` `password``=mypassword` `group``=full`

`/user` `remove` `admin`

!!! note **注意：** 使用新凭据登录路由器以检查用户名/密码是否有效。

## MAC地址连接访问

默认情况下，mac 服务器在所有接口上运行，因此我们将禁用默认的 **all** 条目并添加一个本地接口以禁止来自 WAN 端口的 MAC 连接。 MAC Telnet 服务器功能允许您对接口“列表”应用限制。

首先，创建一个接口列表：

`[admin@MikroTik] >` `/interface list` `add` `name``=listBridge`

然后，将您之前创建的名为“local”的网桥添加到接口列表中：

`[admin@MikroTik] >` `/interface list member` `add` `list``=listBridge` `interface``=local`

将新创建的（接口）“列表”应用到 MAC 服务器：

`[admin@MikroTik] > tool mac-server` `set` `allowed-interface-list``=listBridge`

对 Winbox MAC 访问做同样的事情

`[admin@MikroTik] > tool mac-server mac-winbox` `set` `allowed-interface-list``=listBridge`

Winbox/Webfig 操作：

- 打开 **Interfaces → Interface List → Lists** 窗口并点击“+”添加新列表；
- 在**Name**字段中输入接口列表名称“listBridge”，然后单击**确定**；
- 返回**Interfaces →****Interfaces list**部分并点击“+”；
- 从下拉**List**选项中选择“listBridge”，然后从下拉**Interfaces **选项中选择“local”，然后单击**OK**；
- 打开**Tools -> Mac Server** 窗口；
- 单击**“MAC Telnet Server”**按钮，将打开一个新对话框；
- 从下拉列表中选择新创建的列表“listBridge”，然后单击“**OK**”按钮应用设置。

在 **MAC** **Winbox Server** 选项卡中执行相同的操作以阻止来自 Internet 的 Mac Winbox 连接。

## Neighbor Discovery

MikroTik Neighbor discovery protocol is used to show and recognize other MikroTik routers in the network. Disable neighbor discovery on public interfaces:

`/ip neighbor discovery-settings` `set` `discover-interface-list``=listBridge`

## IP Connectivity Access

Besides the fact that the firewall protects your router from unauthorized access from outer networks, it is possible to restrict username access for the specific IP address

`/user` `set` `0` `allowed-address``=x.x.x.x/yy`

_x.x.x.x/yy - your IP or network subnet that is allowed to access your router._

IP connectivity on the public interface must be limited in the firewall. We will accept only ICMP(ping/traceroute), IP Winbox, and ssh access.

`/ip firewall filter`

  `add` `chain``=input` `connection-state``=established,related` `action``=accept` `comment``=``"accept established,related"``;`

  `add` `chain``=input` `connection-state``=invalid` `action``=drop``;`

  `add` `chain``=input` `in-interface``=ether1` `protocol``=icmp` `action``=accept` `comment``=``"allow ICMP"``;`

  `add` `chain``=input` `in-interface``=ether1` `protocol``=tcp` `port``=8291` `action``=accept` `comment``=``"allow Winbox"``;`

  `add` `chain``=input` `in-interface``=ether1` `protocol``=tcp` `port``=22` `action``=accept` `comment``=``"allow SSH"``;`

  `add` `chain``=input` `in-interface``=ether1` `action``=drop` `comment``=``"block everything else"``;`

In case if a public interface is a pppoe, then the in-interface should be set to "pppoe-out".

The first two rules accept packets from already established connections, so we assume those are OK to not overload the CPU. The third rule drops any packet which connection tracking thinks is invalid. After that, we set up typical accept rules for specific protocols.

If you are using Winbox/Webfig for configuration, here is an example of how to add an established/related rule:

-   Open **Ip -> Firewall** window, click on **Filter rules** tab;
-   Click on the **+** button, a new dialog will open;
-   Select chain input, click on **Connection state,** and select checkboxes for established and related;
-   Click on the **Action** tab and make sure action accept is selected;
-   Click on the **Ok** button to apply settings.

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_ip_fw.png?version=1&modificationDate=1569856324140&api=v2&effects=drop-shadow)

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_ip_fw_add_est.png?version=1&modificationDate=1569856350353&api=v2&effects=drop-shadow)

To add other rules click on **+** for each new rule and fill the same parameters as provided in the console example.

## Administrative Services

Although the firewall protects the router from the public interface, you may still want to disable RouterOS services.

Most of RouterOS administrative tools are configured at  the /ip service menu

Keep only secure ones,

`/ip service` `disable` `telnet,ftp,www,api`

Change default service ports, this will immediately stop most of the random SSH brute force login attempts:

`/ip service` `set` `ssh` `port``=2200`

Additionally, each service can be secured by allowed IP address or address range(the address service will reply to), although more preferred method is to block unwanted access in firewall because the firewall will not even allow to open socket

`/ip service` `set` `winbox` `address``=192.168.88.0/24`

## Other Services

A bandwidth server is used to test throughput between two MikroTik routers. Disable it in the production environment.

`/tool bandwidth-server` `set` `enabled``=no`

A router might have DNS cache enabled, which decreases resolving time for DNS requests from clients to remote servers. In case DNS cache is not required on your router or another router is used for such purposes, disable it.

`/ip dns` `set` `allow-remote-requests``=no`

  
Some RouterBOARDs have an LCD module for informational purposes, set pin or disable it.

  
It is good practice to disable all unused interfaces on your router, in order to decrease unauthorized access to your router.

`/interface` `print`

`/interface` `set` `x` `disabled``=yes`

Where "X" is a number of the unused interfaces.

RouterOS utilizes stronger crypto for SSH, most newer programs use it, to turn on SSH strong crypto:

`/ip ssh` `set` `strong-crypto``=yes`

Following services are disabled by default,  nevertheless, it is better to make sure that none of then were enabled accidentally:

-   MikroTik caching proxy,

-   MikroTik socks proxy,

-   MikroTik UPNP service,

-   MikroTik dynamic name service or IP cloud,

`/ip cloud` `set` `ddns-enabled``=no` `update-time``=no`

## NAT Configuration

At this point, PC is not yet able to access the Internet, because locally used addresses are not routable over the Internet. Remote hosts simply do not know how to correctly reply to your local address.

The solution for this problem is to change the source address for outgoing packets to routers public IP. This can be done with the NAT rule:

`/ip firewall nat`

  `add` `chain``=srcnat` `out-interface``=ether1` `action``=masquerade`

In case if a public interface is a pppoe, then the out-interface should be set to "pppoe-out".

Another benefit of such a setup is that NATed clients behind the router are not directly connected to the Internet, that way additional protection against attacks from outside mostly is not required.

## Port Forwarding

Some client devices may need direct access to the internet over specific ports. For example, a client with an IP address 192.168.88.254 must be accessible by Remote desktop protocol (RDP).

After a quick search on Google, we find out that RDP runs on TCP port 3389. Now we can add a destination NAT rule to redirect RDP to the client's PC.

`/ip firewall nat`

  `add` `chain``=dstnat` `protocol``=tcp` `port``=3389` `in-interface``=ether1` `\`

    `action``=dst-nat` `to-address``=192.168.88.254`

If you have set up strict firewall rules then RDP protocol must be allowed in the firewall filter forward chain.

## Setting up Wireless

For ease of use bridged wireless setup will be made so that your wired hosts are in the same Ethernet broadcast domain as wireless clients.

The important part is to make sure that our wireless is protected, so the first step is the security profile.

Security profiles are configured from `/interface wireless security-profiles` menu in a terminal.

`/interface wireless security-profiles`

  `add` `name``=myProfile` `authentication-types``=wpa2-psk` `mode``=dynamic-keys` `\`

    `wpa2-pre-shared-key``=1234567890`

in Winbox/Webfig click on **Wireless** to open wireless windows and choose the **Security Profile** tab.

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_wlan_sec_profile.png?version=1&modificationDate=1569856421347&api=v2&effects=drop-shadow)

If there are legacy devices that do not support WPA2 (like Windows XP), you may also want to allow WPA protocol.

WPA and WPA2 pre-shared keys should not be the same.

Now when the security profile is ready we can enable the wireless interface and set the desired parameters

`/interface wireless`

  `enable` `wlan1;`

  `set` `wlan1` `band``=2ghz-b/g/n` `channel-width``=20/40mhz-Ce` `distance``=indoors` `\`

    `mode``=ap-bridge` `ssid``=MikroTik-006360` `wireless-protocol``=802.11` `\`

    `security-profile``=myProfile` `frequency-mode``=regulatory-domain` `\`

    `set` `country``=latvia` `antenna-gain``=3`

To do the same from Winbox/Webfig:

-   Open Wireless window, select wlan1 interface, and click on the _enable_ button;
-   Double click on the wireless interface to open the configuration dialog;
-   In the configuration dialog click on the **Wireless** tab and click the **Advanced mode** button on the right side. When you click on the button additional configuration parameters will appear and the description of the button will change to **Simple mode**;
-   Choose parameters as shown in the screenshot, except for the country settings and SSID. You may want to also choose a different frequency and antenna gain;
-   Next, click on the **HT** tab and make sure both chains are selected;
-   Click on the **OK** button to apply settings.

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_wlan_iface.png?version=1&modificationDate=1569856463320&api=v2&effects=drop-shadow)

The last step is to add a wireless interface to a local bridge, otherwise connected clients will not get an IP address:

`/interface bridge port`

  `add` `interface``=wlan1` `bridge``=local`

Now wireless should be able to connect to your access point, get an IP address, and access the internet.

## Protecting the Clients

Now it is time to add some protection for clients on our LAN. We will start with a basic set of rules.

`/ip firewall filter`

  `add` `chain``=forward` `action``=fasttrack-connection` `connection-state``=established,related` `\`

    `comment``=``"fast-track for established,related"``;`

  `add` `chain``=forward` `action``=accept` `connection-state``=established,related` `\`

    `comment``=``"accept established,related"``;`

  `add` `chain``=forward` `action``=drop` `connection-state``=invalid`

  `add` `chain``=forward` `action``=drop` `connection-state``=new` `connection-nat-state``=!dstnat` `\`

    `in-interface``=ether1` `comment``=``"drop access to clients behind NAT from WAN"`

A ruleset is similar to input chain rules (accept established/related and drop invalid), except the first rule with `action=fasttrack-connection`. This rule allows established and related connections to bypass the firewall and significantly reduce CPU usage.

Another difference is the last rule which drops all new connection attempts from the WAN port to our LAN network (unless DstNat is used). Without this rule, if an attacker knows or guesses your local subnet, he/she can establish connections directly to local hosts and cause a security threat.

For more detailed examples on how to build firewalls will be discussed in the firewall section, or check directly  [Building Your First Firewall](https://help.mikrotik.com/docs/display/ROS/Building+Your+First+Firewall) article.

## Blocking Unwanted Websites

Sometimes you may want to block certain websites, for example, deny access to entertainment sites for employees, deny access to porn, and so on. This can be achieved by redirecting HTTP traffic to a proxy server and use an access-list to allow or deny certain websites.

First, we need to add a NAT rule to redirect HTTP to our proxy. We will use RouterOS built-in proxy server running on port 8080.

`/ip firewall nat`

  `add` `chain``=dst-nat` `protocol``=tcp` `dst-port``=80` `src-address``=192.168.88.0/24` `\`

    `action``=redirect` `to-ports``=8080`

Enable web proxy and drop some websites:

`/ip proxy` `set` `enabled``=yes`

`/ip proxy access` `add` `dst-host``=www.facebook.com` `action``=deny`

`/ip proxy access` `add` `dst-host``=*.youtube.*` `action``=deny`

`/ip proxy access` `add` `dst-host``=:vimeo` `action``=deny`

Using Winbox:

-   On the left menu navigate to IP -> Web Proxy
-   Web proxy settings dialog will appear.
-   Check the "Enable" checkbox and click on the "Apply" button
-   Then click on the "Access" button to open the "Web Proxy Access" dialog

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_ip_web_proxy.png?version=1&modificationDate=1569856600346&api=v2&effects=drop-shadow)

-   In the "Web Proxy Access" dialog click on "+" to add a new Web-proxy rule
-   Enter Dst hostname that you want to block, in this case, "[www.facebook.com](https://www.facebook.com/)", choose the action "deny"
-   Then click on the "Ok" button to apply changes.
-   Repeat the same to add other rules.

![](https://help.mikrotik.com/docs/download/attachments/328151/winbox_ip_web_proxy_access.png?version=1&modificationDate=1569856640042&api=v2&effects=drop-shadow)

## Troubleshooting

RouterOS has built-in various troubleshooting tools, like ping, traceroute, torch, packet sniffer, bandwidth test, etc.

We already used the ping tool in this article to [verify internet connectivity](https://help.mikrotik.com/docs/display/ROS/First+Time+Configuration#FirstTimeConfiguration-VerifyConnectivity).

## Troubleshoot if ping fails

The problem with the ping tool is that it says only that destination is **unreachable**, but no more detailed information is available. Let's overview the basic mistakes.

You cannot reach [www.google.com](https://www.google.com/) from your computer which is connected to a MikroTik device:

![](https://help.mikrotik.com/docs/download/attachments/328151/troubleshoot_if_ping_fails.jpg?version=1&modificationDate=1582275155077&api=v2)

If you are not sure how exactly configure your gateway device, please reach MikroTik's official [consultants](https://mikrotik.com/consultants) for configuration support.