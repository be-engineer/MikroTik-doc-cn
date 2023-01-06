### 硬件支持

RouterOS 与预装的 MikroTik 硬件完全兼容。如果满足以下要求，它也可以在第 3 方设备上运行：

-   i386 兼容架构
-   SMP – 多核和多 CPU 兼容
-   至少32MB的内存，自RouterOS v7以后不再有最大内存限制
-   IDE、SATA、USB 和至少 64MB 空间的存储介质
-   Linux内核支持的网卡（PCI、PCI-X）
-   支持交换关芯片配置

!!! note 注意：NVMe 存储仅支持 CHR、x86、Tile 和 MMIPS 架构。有关具体信息，请查看产品手册或框图。

!!! note 注意：我们不建议在少于 64 MB RAM 的硬件上运行 v7。

### 安装

-   Netinstall：从支持 PXE 或 EtherBoot 的网卡进行基于网络的安装
-   CHR：用于作为虚拟机运行的 RouterOS 版本
-   基于 CD 的安装

### 配置

-   用于初始配置基于 MAC 的访问
-   WinBox – 独立的 Windows GUI 配置工具
-   Webfig - 先进的基于网络的配置界面
-   MikroTik - 基于 Android 和 iOS 的配置工具
-   具有集成脚本功能的强大命令行配置界面，可通过本地终端、串行控制台、telnet 和 ssh 访问
-   API - 创建您自己的配置和监控应用程序的方式

### 备份/恢复

-   二进制配置备份保存和加载
-   以可读的文本格式导出和导入配置

### 防火墙

-   状态过滤
-   源和目标 NAT
-   NAT 助手（h323、pptp、quake3、sip、ftp、irc、tftp）
-   内部连接、路由和数据包标记
-   按 IP 地址和地址范围、端口和端口范围、IP 协议、DSCP 等过滤
-   地址列表
-   自定义 Layer7 匹配器
-   支持 IPv6
-   PCC - 每个连接分类器，用于负载平衡配置
-   RAW 过滤绕过连接跟踪

### 路由

-   静态路由
-   虚拟路由和转发 (VRF)
-   基于策略的路由
-   接口路由
-   ECMP路由
-   IPv4 动态路由协议：RIP v1/v2、OSPFv2、BGP v4
-   IPv6动态路由协议：RIPng、OSPFv3、BGP
-   双向转发检测 (BFD)

### MPLS

-   IPv4 的静态标签绑定
-   IPv4 的标签分发协议
-   RSVP 流量工程隧道
-   基于 VPLS MP-BGP 的自动发现和信令
-   基于 MP-BGP 的 MPLS IP VPN

### VPN

-   IPSec – 隧道和传输模式、证书或 PSK、AH 和 ESP 安全协议。
-   IKEv2 支持
-   IPSec 的 AES-NI 硬件加速支持
-   点对点隧道（OpenVPN、PPTP、PPPoE、L2TP、SSTP）
-   高级 PPP 功能（MLPPP、BCP）
-   简单隧道（​​IPIP、EoIP） IPv4 和 IPv6 支持
-   支持6to4 隧道（IPv6 over IPv4 网络）
-   VLAN – IEEE802.1q 虚拟 LAN 支持，Q-in-Q 支持
-   基于 MPLS 的 VPN
-   WireGuard
-   ZeroTier

### 无线

-   IEEE802.11a/b/g 无线客户端和接入点
-   支持完整的 IEEE802.11n 
-   Nstreme 和 Nstreme2 专有协议
-   NV2协议
-   无线分配系统 (WDS)
-   虚拟AP
-   WEP、WPA、WPA2
-   访问控制列表
-   无线客户端漫游
-   WMM
-   HWMP+无线MESH协议
-   MME无线路由协议

### DHCP

-   按接口的 DHCP 服务器
-   DHCP客户端和中继
-   静态和动态 DHCP 租约
-   RADIUS支持
-   自定义 DHCP 选项
-   DHCPv6 前缀委派 (DHCPv6-PD)
-   DHCPv6 客户端

### 热点

-   即插即用的网络访问
-   本地网络客户端的身份验证
-   用户账户
-   RADIUS 支持身份验证和计费

### QoS

-   具有 CIR、MIR、突发和优先级支持的分层令牌桶 (HTB) QoS 系统
-   基本 QoS 实施的简单快速解决方案 - 简单队列
-   动态客户端速率均衡 (PCQ)

### 代理

-   HTTP缓存代理服务器
-   透明 HTTP 代理
-   SOCKS 协议支持
-   DNS 静态条目
-   支持在单独的驱动器上缓存
-   支持父代理
-   访问控制列表
-   缓存列表

### 工具

-   Ping, traceroute
-   带宽测试, ping flood
-   数据包嗅探, torch
-   Telnet, ssh
-   电子邮件和短信发送工具
-   自动脚本执行工具
-   CALEA
-   文件抓取工具
-   高级流发生器
-   WoL（局域网唤醒）

### 其他特性

-   Samba支持
-   开放流支持
-   桥接 – 生成树协议（STP、RSTP）、网桥防火墙和 MAC natting。
-   动态DNS更新工具
-   NTP 客户端/服务器并与 GPS 系统同步
-   VRRP v2 和 v3 支持
-   SNMP
-   M3P - 用于无线链路和以太网的 MikroTik 数据包打包协议
-   MNDP - MikroTik 邻居发现协议，支持 CDP（Cisco 发现协议）
-   RADIUS认证计费
-   TFTP服务器
-   同步接口支持（仅限 Farsync 卡）（在 v5.x 中删除）
-   异步——串行 PPP 拨入/拨出，按需拨出
-   ISDN – 拨入/拨出、128K 捆绑支持、Cisco HDLC、x75i、x75ui、x75bui 线路协议、按需拨号

### 内核版本

-   RouterOS version 6.x uses 3.3.5
-   RouterOS version 7.x uses 5.6.3

### 支持的加密

RouterOS 7 用于网络（电信）设备的管理。

-   RouterOS 7 包括加密功能（组件），用于数据（信息）安全，通过电信渠道和设备控制渠道传递。

-   所有加密功能（组件）都是 RouterOS 7 的组成部分，最终用户无法更改。

-   RouterOS 7 旨在供最终用户安装，无需供应商提供显著支持。

-   RouterOS 7 使用以下安全协议：



<table cellspacing="0" border="0">
	<colgroup width="171"></colgroup>
	<colgroup width="157"></colgroup>
	<colgroup width="160"></colgroup>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" height="17" align="center"><b><font face="Liberation Serif">支持的安全协议</font></b></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center"><b><font face="Liberation Serif">加密算法</font></b></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center"><b><font face="Liberation Serif">最大密钥长度</font></b></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" rowspan=6 height="102" align="left"><font face="Liberation Serif">IPSec</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">DES</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">56 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">3DES</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">168 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">AES</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">128, 192, 256 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">Blowfish</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">448 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">Twofish</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">256 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">Camelia</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">128, 192, 256 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" height="17" align="left"><font face="Liberation Serif">PPTP (with MPPE)</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">RC4</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">128 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" height="17" align="left"><font face="Liberation Serif">L2TP (with MPPE)</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">RC4</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">128 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" rowspan=2 height="34" align="left"><font face="Liberation Serif">SNMP</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">DES</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">56 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">AES</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">128 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" rowspan=3 height="51" align="left"><font face="Liberation Serif">SSH</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">Blowfish</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">128 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">3DES</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">192 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">AES</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">128, 192, 256 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" rowspan=2 height="34" align="left"><font face="Liberation Serif">SSTP</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">AES</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">256 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">RC4</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">128 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" height="32" align="left"><font face="Liberation Serif">Used in WinBox connection (nameless)</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">AES</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">128 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" height="17" align="left"><font face="Liberation Serif">WEP</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">RC4</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">104 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" height="17" align="left"><font face="Liberation Serif">WPA-TKIP</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">RC4</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">128 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" height="17" align="left"><font face="Liberation Serif">WPA2-TKIP</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">RC4</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">128 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" height="17" align="left"><font face="Liberation Serif">WPA-AES</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">AES</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">128 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" height="17" align="left"><font face="Liberation Serif">WPA2-AES</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">AES</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">128 bit</font></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" height="32" align="left"><font face="Liberation Serif">HTTPS</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">NULL, RC4, DES, DES40, 3DES, AES</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left"><font face="Liberation Serif">128, 192, 256 bit</font></td>
	</tr>
</table>
