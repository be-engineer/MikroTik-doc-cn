# 概述

___

CCR3xx、CRS5xx 系列交换机和 CCR2116、CCR2216 路由器具有高度集成的交换机，配备高性能 CPU 和功能丰富的数据包处理器。这些设备可以设计成各种以太网应用，包括非管理型交换机、第 2 层管理型交换机、运营商交换机、VLAN 间路由器和有线统一数据包处理器。

> 本文适用于CRS3xx、CRS5xx系列交换机、CCR2116、CCR2216路由器，不适用于 [CRS1xx/CRS2xx系列交换机](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=103841835) 。

## 特性

| 特性                       | 说明                                                                                                                                                                                                                                                |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Forwarding**             | - 用于交换或路由的可配置端口<br>- 完全无阻塞线速交换<br>- 用于第 2 层单播转发的大型单播 FDB<br>- 基于 IVL转发数据库工作<br>- 支持巨型帧<br>- 支持IGMP 侦听<br>- 使用选项 82 的 DHCP 侦听                                                            |
| **Routing**                | 第 3 层硬件卸载：<br> - IPv4 单播路由<br> - 支持以太网、桥接、绑定和 VLAN 接口<br> - ECMP<br> - Blackholes<br> - 卸载的 Fasttrack 连接（仅适用于某些交换机型号）<br> - 用于 Fasttrack 连接的卸载 NAT（仅适用于某些交换机型号）<br> - 多MTU 配置文件 |
| **Spanning Tree Protocol** | -   STP<br>-   RSTP<br>-   MSTP                                                                                                                                                                                                                     |
| **Mirroring**              | 各种类型的镜像：<br>- 基于端口的镜像<br>- 基于 VLAN 的镜像<br>- 基于 MAC 的镜像                                                                                                                                                                     |
| **VLAN**                   | 完全兼容IEEE802.1Q和IEEE802.1ad VLAN<br>4k 活动 VLAN<br>灵活的 VLAN 分配：<br>- 基于端口的VLAN<br>- 基于协议的VLAN<br>- 基于 MAC 的 VLAN<br>VLAN过滤<br>从任何到任何 VLAN 的转换                                                                    |
| **Bonding**                | - 支持 802.3ad (LACP) 和 balance-xor 模式<br>- 每个绑定接口最多 8 个成员端口<br>- 硬件自动故障转移和负载均衡<br>- MLAG                                                                                                                              |
| **Traffic Shaping**        | - 入口流量限制<br>- 基于端口<br>- 基于 MAC<br>- 基于IP<br>- 基于 VLAN<br>- 基于协议<br>- 基于 DSCP<br>- 基于端口的出口流量限制                                                                                                                      |
| **Port isolation**         | -适用于私有VLAN                                                                                                                                                                                                                                     |
| **Access Control List**    | - 入口 ACL 表<br>- 基于端口、L2、L3、L4协议头分类<br>- ACL动作包括协议头字段的过滤、转发和修改                                                                                                                                                      |

## 型号

下表说明了 Cloud Router Switch 型号和 CCR 路由器之间的主要区别。

<table cellspacing="0" border="0">
	<colgroup width="255"></colgroup>
	<colgroup width="180"></colgroup>
	<colgroup span="2" width="85"></colgroup>
	<colgroup width="131"></colgroup>
	<colgroup span="7" width="85"></colgroup>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">Model</font></td>
		<td align="left"><font face="Liberation Sans">Switch Chip</font></td>
		<td align="left"><font face="Liberation Sans">CPU</font></td>
		<td align="left"><font face="Liberation Sans">Cores</font></td>
		<td align="left"><font face="Liberation Sans">10G SFP+</font></td>
		<td align="left"><font face="Liberation Sans">10G Ethernet</font></td>
		<td align="left"><font face="Liberation Sans">25G SFP28</font></td>
		<td align="left"><font face="Liberation Sans">40G QSFP+</font></td>
		<td align="left"><font face="Liberation Sans">100G QSFP28</font></td>
		<td align="left"><font face="Liberation Sans">ACL rules</font></td>
		<td align="left"><font face="Liberation Sans">Unicast FDB entries</font></td>
		<td align="left"><font face="Liberation Sans">Jumbo Frame (Bytes)</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">netPower 15FR (CRS318-1Fi-15Fr-2S)</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX224S</font></td>
		<td align="left"><font face="Liberation Sans">800MHz</font></td>
		<td align="right" sdval="1" sdnum="2052;"><font face="Liberation Sans">1</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="128" sdnum="2052;"><font face="Liberation Sans">128</font></td>
		<td align="right" sdval="16000" sdnum="2052;"><font face="Liberation Sans">16000</font></td>
		<td align="right" sdval="10218" sdnum="2052;"><font face="Liberation Sans">10218</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">netPower 16P (CRS318-16P-2S+)</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX226S</font></td>
		<td align="left"><font face="Liberation Sans">800MHz</font></td>
		<td align="right" sdval="1" sdnum="2052;"><font face="Liberation Sans">1</font></td>
		<td align="right" sdval="2" sdnum="2052;"><font face="Liberation Sans">2</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="128" sdnum="2052;"><font face="Liberation Sans">128</font></td>
		<td align="right" sdval="16000" sdnum="2052;"><font face="Liberation Sans">16000</font></td>
		<td align="right" sdval="10218" sdnum="2052;"><font face="Liberation Sans">10218</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">CRS310-1G-5S-4S+ (netFiber 9/IN)</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX226S</font></td>
		<td align="left"><font face="Liberation Sans">800MHz</font></td>
		<td align="right" sdval="1" sdnum="2052;"><font face="Liberation Sans">1</font></td>
		<td align="right" sdval="4" sdnum="2052;"><font face="Liberation Sans">4</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="128" sdnum="2052;"><font face="Liberation Sans">128</font></td>
		<td align="right" sdval="16000" sdnum="2052;"><font face="Liberation Sans">16000</font></td>
		<td align="right" sdval="10218" sdnum="2052;"><font face="Liberation Sans">10218</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">CRS326-24G-2S+ (RM/IN)</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX3236</font></td>
		<td align="left"><font face="Liberation Sans">800MHz</font></td>
		<td align="right" sdval="1" sdnum="2052;"><font face="Liberation Sans">1</font></td>
		<td align="right" sdval="2" sdnum="2052;"><font face="Liberation Sans">2</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="128" sdnum="2052;"><font face="Liberation Sans">128</font></td>
		<td align="right" sdval="16000" sdnum="2052;"><font face="Liberation Sans">16000</font></td>
		<td align="right" sdval="10218" sdnum="2052;"><font face="Liberation Sans">10218</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">CRS328-24P-4S+</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX3236</font></td>
		<td align="left"><font face="Liberation Sans">800MHz</font></td>
		<td align="right" sdval="1" sdnum="2052;"><font face="Liberation Sans">1</font></td>
		<td align="right" sdval="4" sdnum="2052;"><font face="Liberation Sans">4</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="128" sdnum="2052;"><font face="Liberation Sans">128</font></td>
		<td align="right" sdval="16000" sdnum="2052;"><font face="Liberation Sans">16000</font></td>
		<td align="right" sdval="10218" sdnum="2052;"><font face="Liberation Sans">10218</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">CRS328-4C-20S-4S+</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX3236</font></td>
		<td align="left"><font face="Liberation Sans">800MHz</font></td>
		<td align="right" sdval="1" sdnum="2052;"><font face="Liberation Sans">1</font></td>
		<td align="right" sdval="4" sdnum="2052;"><font face="Liberation Sans">4</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="128" sdnum="2052;"><font face="Liberation Sans">128</font></td>
		<td align="right" sdval="16000" sdnum="2052;"><font face="Liberation Sans">16000</font></td>
		<td align="right" sdval="10218" sdnum="2052;"><font face="Liberation Sans">10218</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">CRS305-1G-4S+</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX3236</font></td>
		<td align="left"><font face="Liberation Sans">800MHz</font></td>
		<td align="right" sdval="1" sdnum="2052;"><font face="Liberation Sans">1</font></td>
		<td align="right" sdval="4" sdnum="2052;"><font face="Liberation Sans">4</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="128" sdnum="2052;"><font face="Liberation Sans">128</font></td>
		<td align="right" sdval="16000" sdnum="2052;"><font face="Liberation Sans">16000</font></td>
		<td align="right" sdval="10218" sdnum="2052;"><font face="Liberation Sans">10218</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">CRS309-1G-8S+</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX8208</font></td>
		<td align="left"><font face="Liberation Sans">800MHz</font></td>
		<td align="right" sdval="2" sdnum="2052;"><font face="Liberation Sans">2</font></td>
		<td align="right" sdval="8" sdnum="2052;"><font face="Liberation Sans">8</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="1024" sdnum="2052;"><font face="Liberation Sans">1024</font></td>
		<td align="right" sdval="32000" sdnum="2052;"><font face="Liberation Sans">32000</font></td>
		<td align="right" sdval="10218" sdnum="2052;"><font face="Liberation Sans">10218</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">CRS317-1G-16S+</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX8216</font></td>
		<td align="left"><font face="Liberation Sans">800MHz</font></td>
		<td align="right" sdval="2" sdnum="2052;"><font face="Liberation Sans">2</font></td>
		<td align="right" sdval="16" sdnum="2052;"><font face="Liberation Sans">16</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="1024" sdnum="2052;"><font face="Liberation Sans">1024</font></td>
		<td align="right" sdval="128000" sdnum="2052;"><font face="Liberation Sans">128000</font></td>
		<td align="right" sdval="10218" sdnum="2052;"><font face="Liberation Sans">10218</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">CRS312-4C+8XG</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX8212</font></td>
		<td align="left"><font face="Liberation Sans">650MHz</font></td>
		<td align="right" sdval="1" sdnum="2052;"><font face="Liberation Sans">1</font></td>
		<td align="left"><font face="Liberation Sans">4 (combo ports)</font></td>
		<td align="left"><font face="Liberation Sans">8 + 4 (combo ports)</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="512" sdnum="2052;"><font face="Liberation Sans">512</font></td>
		<td align="right" sdval="32000" sdnum="2052;"><font face="Liberation Sans">32000</font></td>
		<td align="right" sdval="10218" sdnum="2052;"><font face="Liberation Sans">10218</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">CRS326-24S+2Q+</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX8332</font></td>
		<td align="left"><font face="Liberation Sans">650MHz</font></td>
		<td align="right" sdval="1" sdnum="2052;"><font face="Liberation Sans">1</font></td>
		<td align="right" sdval="24" sdnum="2052;"><font face="Liberation Sans">24</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="2" sdnum="2052;"><font face="Liberation Sans">2</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="256" sdnum="2052;"><font face="Liberation Sans">256</font></td>
		<td align="right" sdval="32000" sdnum="2052;"><font face="Liberation Sans">32000</font></td>
		<td align="right" sdval="10218" sdnum="2052;"><font face="Liberation Sans">10218</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">CRS354-48G-4S+2Q+</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX3257</font></td>
		<td align="left"><font face="Liberation Sans">650MHz</font></td>
		<td align="right" sdval="1" sdnum="2052;"><font face="Liberation Sans">1</font></td>
		<td align="right" sdval="4" sdnum="2052;"><font face="Liberation Sans">4</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="2" sdnum="2052;"><font face="Liberation Sans">2</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="170" sdnum="2052;"><font face="Liberation Sans">170</font></td>
		<td align="right" sdval="32000" sdnum="2052;"><font face="Liberation Sans">32000</font></td>
		<td align="right" sdval="10218" sdnum="2052;"><font face="Liberation Sans">10218</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">CRS354-48P-4S+2Q+</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX3257</font></td>
		<td align="left"><font face="Liberation Sans">650MHz</font></td>
		<td align="right" sdval="1" sdnum="2052;"><font face="Liberation Sans">1</font></td>
		<td align="right" sdval="4" sdnum="2052;"><font face="Liberation Sans">4</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="2" sdnum="2052;"><font face="Liberation Sans">2</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="170" sdnum="2052;"><font face="Liberation Sans">170</font></td>
		<td align="right" sdval="32000" sdnum="2052;"><font face="Liberation Sans">32000</font></td>
		<td align="right" sdval="10218" sdnum="2052;"><font face="Liberation Sans">10218</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">CRS504-4XQ-IN</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX4310</font></td>
		<td align="left"><font face="Liberation Sans">650MHz</font></td>
		<td align="right" sdval="1" sdnum="2052;"><font face="Liberation Sans">1</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="4" sdnum="2052;"><font face="Liberation Sans">4</font></td>
		<td align="right" sdval="1024" sdnum="2052;"><font face="Liberation Sans">1024</font></td>
		<td align="right" sdval="128000" sdnum="2052;"><font face="Liberation Sans">128000</font></td>
		<td align="right" sdval="10218" sdnum="2052;"><font face="Liberation Sans">10218</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">CRS518-16XS-2XQ</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX8525</font></td>
		<td align="left"><font face="Liberation Sans">650MHz</font></td>
		<td align="right" sdval="1" sdnum="2052;"><font face="Liberation Sans">1</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="16" sdnum="2052;"><font face="Liberation Sans">16</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="2" sdnum="2052;"><font face="Liberation Sans">2</font></td>
		<td align="right" sdval="1024" sdnum="2052;"><font face="Liberation Sans">1024</font></td>
		<td align="right" sdval="128000" sdnum="2052;"><font face="Liberation Sans">128000</font></td>
		<td align="right" sdval="10218" sdnum="2052;"><font face="Liberation Sans">10218</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">CCR2116-12G-4S+</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX3255</font></td>
		<td align="left"><font face="Liberation Sans">2000MHz</font></td>
		<td align="right" sdval="16" sdnum="2052;"><font face="Liberation Sans">16</font></td>
		<td align="right" sdval="4" sdnum="2052;"><font face="Liberation Sans">4</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="512" sdnum="2052;"><font face="Liberation Sans">512</font></td>
		<td align="right" sdval="32000" sdnum="2052;"><font face="Liberation Sans">32000</font></td>
		<td align="right" sdval="9570" sdnum="2052;"><font face="Liberation Sans">9570</font></td>
	</tr>
	<tr>
		<td height="17" align="left"><font face="Liberation Sans">CCR2216-1G-12XS-2XQ</font></td>
		<td align="left"><font face="Liberation Sans">Marvell-98DX8525</font></td>
		<td align="left"><font face="Liberation Sans">2000MHz</font></td>
		<td align="right" sdval="16" sdnum="2052;"><font face="Liberation Sans">16</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="12" sdnum="2052;"><font face="Liberation Sans">12</font></td>
		<td align="left"><font face="Liberation Sans">-</font></td>
		<td align="right" sdval="2" sdnum="2052;"><font face="Liberation Sans">2</font></td>
		<td align="right" sdval="1024" sdnum="2052;"><font face="Liberation Sans">1024</font></td>
		<td align="right" sdval="128000" sdnum="2052;"><font face="Liberation Sans">128000</font></td>
		<td align="right" sdval="9570" sdnum="2052;"><font face="Liberation Sans">9570</font></td>
	</tr>
</table>


L3硬件卸载功能和硬件限制，请参考[功能支持](https://help.mikrotik.com/docs/display/ROS/L3+Hardware+Offloading#L3HardwareOffloading-L3HWFeatureSupport)和[设备支持](https://help.mikrotik.com/docs/display/ROS/L3+Hardware+Offloading#L3HardwareOffloading-L3HWDeviceSupport)用户手册。

## 缩写

- FDB - 转发数据库
- MDB - 组播数据库
- SVL - 共享 VLAN 学习
- IVL - 独立 VLAN 学习
- PVID - 端口 VLAN ID
- ACL - 访问控制列表
- CVID - 客户 VLAN ID
- SVID - 服务 VLAN ID

## 端口交换

___

要设置端口交换，请查看 [Bridge Hardware Offloading](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeHardwareOffloading) 页面。

目前，只能创建一个带硬件卸载的网桥。 使用 `hw=yes/no` 参数选择哪个网桥将使用硬件卸载。

网桥 STP/RSTP/MSTP、IGMP 侦听和 VLAN 过滤设置不影响硬件卸载，因为 RouterOS v6.42 绑定的接口也会被硬件卸载。

## VLAN

___

从 RouterOS 版本 6.41 开始，网桥在网桥内提供 VLAN 感知的第 2 层转发和 VLAN 标记修改。 这组功能使桥接操作更像传统的以太网交换机，并且与桥接类似隧道的 VLAN 接口时的配置相比，可以克服生成树兼容性问题。 强烈建议桥接 VLAN 过滤配置符合 STP (802.1D)、RSTP (802.1w) 标准，并且必须在 RouterOS 中启用 MSTP (802.1s) 支持。

## VLAN过滤

VLAN 过滤在 [桥接 VLAN 过滤](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeVLANFiltering) 部分进行了描述。

VLAN设置示例

下面描述了如何利用 VLAN 转发的一些最常见的方法。

### 基于端口的 VLAN

[桥接 VLAN 过滤](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeVLANFiltering) 部分描述了配置。

### 基于 MAC 的 VLAN

- 交换机规则表用于基于 MAC 的 VLAN 功能，请参阅 [此表](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-Models) 查看每个设备支持多少规则。
- 基于 MAC 的 VLAN 只能在交换机端口之间正常工作，而不能在交换机端口和 CPU 之间正常工作。 当数据包被转发到 CPU 时，将始终使用桥接端口的 `pvid` 属性，而不是 ACL 规则中的 `new-vlan-id`。
- 当启用 DHCP 侦听时，基于 MAC 的 VLAN 将不适用于 DHCP 数据包。

通过创建启用硬件卸载的网桥来启用端口交换：

```shell
/interface bridge
add name=bridge1 vlan-filtering=yes
/interface bridge port
add bridge=bridge1 interface=ether2 hw=yes
add bridge=bridge1 interface=ether7 hw=yes

```

在 Bridge VLAN 表中添加 VLAN 并指定端口：

```shell
/interface bridge vlan
add bridge=bridge1 tagged=ether2 untagged=ether7 vlan-ids=200,300,400

```

添加基于 MAC 地址分配 VLAN id 的交换机规则：

```shell
/interface ethernet switch rule
add switch=switch1 ports=ether7 src-mac-address=A4:12:6D:77:94:43/FF:FF:FF:FF:FF:FF new-vlan-id=200
add switch=switch1 ports=ether7 src-mac-address=84:37:62:DF:04:20/FF:FF:FF:FF:FF:FF new-vlan-id=300
add switch=switch1 ports=ether7 src-mac-address=E7:16:34:A1:CD:18/FF:FF:FF:FF:FF:FF new-vlan-id=400

```

### 基于协议的VLAN

- 交换机规则表用于基于协议的 VLAN 功能，请参阅 [此表](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-Models) 查看每个设备支持多少规则。
- 基于协议的 VLAN 只能在交换机端口之间正常工作，而不能在交换机端口和 CPU 之间正常工作。 当数据包被转发到 CPU 时，将始终使用桥接端口的“pvid”属性，而不是 ACL 规则中的“new-vlan-id”。
- 当启用 DHCP 侦听时，基于协议的 VLAN 将不适用于 DHCP 数据包。

通过创建启用硬件卸载的网桥来启用端口交换：

```shell
/interface bridge
add name=bridge1 vlan-filtering=yes
/interface bridge port
add bridge=bridge1 interface=ether2 hw=yes
add bridge=bridge1 interface=ether6 hw=yes
add bridge=bridge1 interface=ether7 hw=yes
add bridge=bridge1 interface=ether8 hw=yes

```

在 Bridge VLAN 表中添加 VLAN 并指定端口：

```shell
/interface bridge vlan
add bridge=bridge1 tagged=ether2 untagged=ether6 vlan-ids=200
add bridge=bridge1 tagged=ether2 untagged=ether7 vlan-ids=300
add bridge=bridge1 tagged=ether2 untagged=ether8 vlan-ids=400

```

添加基于 MAC 协议分配 VLAN id 的交换机规则：

```shell
/interface ethernet switch rule
add mac-protocol=ip new-vlan-id=200 ports=ether6 switch=switch1
add mac-protocol=ipx new-vlan-id=300 ports=ether7 switch=switch1
add mac-protocol=0x80F3 new-vlan-id=400 ports=ether8 switch=switch1

```

### VLAN隧道(Q-in-Q)

从 RouterOS v6.43 开始，可以同时使用提供商网桥 (IEEE 802.1ad) 和标签堆叠 VLAN 过滤以及硬件卸载。 [桥接 VLAN 隧道 (Q-in-Q)](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-VLANTunneling(QinQ)) 部分描述了配置。

带有Marvell-98DX3257交换芯片的设备（例如 CRS354 系列）不支持在 1Gbps 以太网接口上对其他 VLAN 类型（`0x88a8` 和 `0x9100`）进行 VLAN 过滤。

## 入站VLAN转换

可以使用入站端口上的 ACL 规则将某个 VLAN ID 转换为不同的 VLAN ID。 在这个例子中，我们创建了两个 ACL 规则，允许双向通信。 这可以通过执行以下操作来完成。

创建一个新网桥并通过硬件卸载向其添加端口：


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code> <code class="ros value">vlan-filtering</code><code class="ros plain">=no</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

添加 ACL 规则以便在每个方向上转换 VLAN ID：


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">new-dst-ports</code><code class="ros plain">=ether2</code> <code class="ros value">new-vlan-id</code><code class="ros plain">=20</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">vlan-id</code><code class="ros plain">=10</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">new-dst-ports</code><code class="ros plain">=ether1</code> <code class="ros value">new-vlan-id</code><code class="ros plain">=10</code> <code class="ros value">ports</code><code class="ros plain">=ether2</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">vlan-id</code><code class="ros plain">=20</code></div></div></td></tr></tbody></table>

将两个 VLAN ID 添加到网桥 VLAN 表中：


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge vlan</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether1</code> <code class="ros value">vlan-ids</code><code class="ros plain">=10</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">tagged</code><code class="ros plain">=ether2</code> <code class="ros value">vlan-ids</code><code class="ros plain">=20</code></div></div></td></tr></tbody></table>

允许网桥进行VLAN过滤:


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge </code><code class="ros functions">set </code><code class="ros plain">bridge1 </code><code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

双向通信仅限于两个交换机端口之间。 在更多端口之间转换 VLAN ID 会导致流量泛滥或相同 VLAN 端口之间的错误转发。

通过启用“vlan-filtering”，将过滤掉发往 CPU 的流量，在启用 VLAN 过滤之前，要确保设置了一个[管理端口](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-Managementaccessconfiguration)。

## (R/M)STP

___

CRS3xx、CRS5xx系列交换机和CCR2116、CCR2216路由器能够在硬件层面上运行STP、RSTP和MSTP。 有关更多详细信息，可以查看 [生成树协议](https://help.mikrotik.com/docs/display/ROS/Spanning+Tree+Protocol) 手册。

## 绑定

___

CRS3xx、CRS5xx 系列交换机和 CCR2116、CCR2216 路由器支持带绑定接口的硬件卸载。 只有 `802.3ad` 和 `balance-xor` 绑定模式是硬件卸载的，其他绑定模式将使用 CPU 的资源。 你可以在 [绑定接口](https://help.mikrotik.com/docs/display/ROS/Bonding) 部分找到更多信息。 如果使用 802.3ad 模式，则支持 LACP（链路聚合控制协议）。

要创建硬件卸载绑定接口，必须使用受支持的绑定模式创建绑定接口：


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bonding</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mode</code><code class="ros plain">=802.3ad</code> <code class="ros value">name</code><code class="ros plain">=bond1</code> <code class="ros value">slaves</code><code class="ros plain">=ether1,ether2</code></div></div></td></tr></tbody></table>

此接口可以和其他接口一起添加到网桥中：


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=bond1</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether3</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge</code> <code class="ros value">interface</code><code class="ros plain">=ether4</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

不要将接口添加到已经处于绑定中的网桥，RouterOS 不允许将接口添加到已经是绑定的从端口的网桥。

通过检查“H”标志确保绑定接口是硬件卸载的：


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">/interface bridge port print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Flags: X - disabled, I - inactive, D - dynamic, H - hw-offload</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">#&nbsp;&nbsp;&nbsp;&nbsp; INTERFACE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; BRIDGE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; HW</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">0&nbsp;&nbsp; H bond1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">1&nbsp;&nbsp; H ether3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; yes</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;</code><code class="text plain">2&nbsp;&nbsp; H ether4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; bridge&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; yes</code></div></div></td></tr></tbody></table>

对于 HW-offloaded 绑定接口，内置交换芯片将始终使用 Layer2+Layer3+Layer4 作为传输哈希策略，手动更改传输哈希策略将不起作用。

## 多机箱链路聚合组

___

RouterOS 中的 MLAG（多机箱链路聚合组）实现允许在两个独立的设备上配置 LACP 绑定，而客户端设备认为连接在同一台机器上。 这在交换机故障的情况下提供了物理冗余。 所有 CRS3xx、CRS5xx 系列和 CCR2116、CCR2216 设备都可以配置 MLAG。 阅读[此处](https://help.mikrotik.com/docs/display/ROS/Multi-chassis+Link+Aggregation+Group)了解更多信息。

## L3 硬件卸载

___

Layer3 硬件卸载（也称为 IP 交换或 HW 路由）将允许将一些路由器功能卸载到交换芯片上。 这允许在路由数据包时达到线速，而这对于 CPU 来说是不可能的。

卸载的功能集取决于所使用的芯片组。 阅读 [此处](https://help.mikrotik.com/docs/display/ROS/L3+Hardware+Offloading) 了解更多信息。

## 端口隔离

___

由于 RouterOS v6.43 可以创建专用 VLAN 设置，因此可以在 [交换机芯片端口隔离](https://help.mikrotik.com/docs/display/ROS/Switch+Chip+Features) #SwitchChipFeatures-Portisolation）手册中找到示例 。 硬件卸载绑定接口不包含在交换机端口隔离菜单中，但仍然可以在绑定的每个辅助接口上单独配置端口隔离。

## IGMP/MLD 侦听

___

CRS3xx、CRS5xx 系列交换机和 CCR2116、CCR2216 路由器能够在硬件级别上使用 IGMP/MLD侦听。 要查看更多详细信息，请查看 [IGMP/MLD 侦听](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=59277403) 手册。

## DHCP 侦听和 DHCP 选项 82

___

CRS3xx、CRS5xx 系列交换机和 CCR2116、CCR2216 路由器能够在硬件级别上使用带有选项 82 的 DHCP 侦听。 交换机将创建动态ACL规则来捕获DHCP数据包并将它们重定向到主CPU进行进一步处理。 要查看更多详细信息，请访问 [DHCP 侦听和 DHCP 选项 82](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-DHCPSnoopingandDHCPOption82) 手册。

> 创建硬件卸载绑定接口时，DHCP 侦听将不起作用。

## 控制器桥和端口扩展器

___

控制器桥 (CB) 和端口扩展器 (PE) 是 RouterOS 中的 IEEE 802.1BR 标准实现。 它允许使用 PE 设备虚拟扩展 CB 端口，并从单个控制设备管理这些扩展接口。 这样的配置提供了简化的网络拓扑结构、灵活性、增加端口密度和易管理性。 请参阅 [Controller Bridge and Port Extender 手册](https://help.mikrotik.com/docs/display/ROS/Controller+Bridge+and+Port+Extender) 了解更多详情。

## 镜像

___

镜像让交换机可以嗅探进入交换机芯片的所有流量，并将这些数据包的副本发送到另一个端口（镜像目标）。 此功能可用于轻松设置分路器设备，使你可以在流量分析设备上检查网络上的流量。 可以设置简单的基于端口的镜像，但也可以根据各种参数设置更复杂的镜像。 请注意，镜像目标端口必须属于同一个交换机（请参阅`/interface ethernet` 菜单中哪个端口属于哪个交换机）。 此外，mirror-target 可以有一个特殊的`cpu`值，这意味着嗅探到的数据包将从交换芯片的 CPU 端口发送出去。 可用于镜像特定流量的可能性有很多种，你可以在下面找到最常见的镜像示例：

基于端口的镜像：


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">switch1 </code><code class="ros value">mirror-source</code><code class="ros plain">=ether2</code> <code class="ros value">mirror-target</code><code class="ros plain">=ether3</code></div></div></td></tr></tbody></table>

属性 `mirror-source` 会将入口和出口数据包副本发送到 `mirror-target` 端口。 `mirror-source` 和 `mirror-target` 都仅限于一个接口。


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">switch1 </code><code class="ros value">mirror-source</code><code class="ros plain">=none</code> <code class="ros value">mirror-target</code><code class="ros plain">=ether3</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mirror</code><code class="ros plain">=yes</code> <code class="ros value">ports</code><code class="ros plain">=ether1,ether2</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code></div></div></td></tr></tbody></table>

使用 ACL 规则，可以镜像来自多个“端口”接口的数据包。 只有入口数据包被镜像到“镜像目标”接口。

基于 VLAN 的镜像：


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">bridge1 </code><code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">switch1 </code><code class="ros value">mirror-target</code><code class="ros plain">=ether3</code> <code class="ros value">mirror-source</code><code class="ros plain">=none</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mirror</code><code class="ros plain">=yes</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">vlan-id</code><code class="ros plain">=11</code></div></div></td></tr></tbody></table>

通过启用“vlan-filtering”，将过滤掉发往 CPU 的流量，在启用 VLAN 过滤之前，要确保设置了一个[管理端口](https://help.mikrotik.com/docs/display/ ROS/Bridging+and+Switching#BridgingandSwitching-Managementaccessconfiguration）。

基于 MAC 的镜像：

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">switch1 </code><code class="ros value">mirror-target</code><code class="ros plain">=ether3</code> <code class="ros value">mirror-source</code><code class="ros plain">=none</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mirror</code><code class="ros plain">=yes</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">dst-mac-address</code><code class="ros plain">=64:D1:54:D9:27:E6/FF:FF:FF:FF:FF:FF</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mirror</code><code class="ros plain">=yes</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">src-mac-address</code><code class="ros plain">=64:D1:54:D9:27:E6/FF:FF:FF:FF:FF:FF</code></div></div></td></tr></tbody></table>

基于协议的镜像:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">switch1 </code><code class="ros value">mirror-target</code><code class="ros plain">=ether3</code> <code class="ros value">mirror-source</code><code class="ros plain">=none</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mirror</code><code class="ros plain">=yes</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">mac-protocol</code><code class="ros plain">=ipx</code></div></div></td></tr></tbody></table>

基于IP地址的镜像:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">switch1 </code><code class="ros value">mirror-target</code><code class="ros plain">=ether3</code> <code class="ros value">mirror-source</code><code class="ros plain">=none</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mirror</code><code class="ros plain">=yes</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">src-address</code><code class="ros plain">=192.168.88.0/24</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">mirror</code><code class="ros plain">=yes</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">dst-address</code><code class="ros plain">=192.168.88.0/24</code></div></div></td></tr></tbody></table>

还有其他选项，请查看 [ACL 部分](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features# CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-SwitchRules(ACL)）找出所有可以用来匹配数据包的参数。

## 流量整形

___

可以限制与 ACL 规则匹配的某些参数的入口流量，并且可以限制每个端口的入口/出口流量。 监管器用于入口流量，整形器用于出口流量。 入口监管器通过丢包控制接收到的流量。 超出定义限制的所有内容都将被删除。 这会影响终端主机上的 TCP 拥塞控制机制，并且实际的带宽实际上可能低于定义的带宽。 出口整形器尝试将超过限制的数据包排队而不是丢弃它们。 最终，当输出队列变满时，它也会丢弃数据包，但是，它允许更好地利用定义的吞吐量。

基于端口的流量监管器和整形器：


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch port</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">ether1 </code><code class="ros value">ingress-rate</code><code class="ros plain">=10M</code> <code class="ros value">egress-rate</code><code class="ros plain">=5M</code></div></div></td></tr></tbody></table>

基于MAC的流量监管器:


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">src-mac-address</code><code class="ros plain">=64:D1:54:D9:27:E6/FF:FF:FF:FF:FF:FF</code> <code class="ros value">rate</code><code class="ros plain">=10M</code></div></div></td></tr></tbody></table>

基于VLAN的流量监管器:


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">bridge1 </code><code class="ros value">vlan-filtering</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">vlan-id</code><code class="ros plain">=11</code> <code class="ros value">rate</code><code class="ros plain">=10M</code></div></div></td></tr></tbody></table>

通过启用“vlan-filtering”，将过滤掉发往 CPU 的流量，在启用 VLAN 过滤之前，要确保设置了一个[管理端口](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-管理访问配置)。

基于协议的流量监管器：


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code> <code class="ros value">mac-protocol</code><code class="ros plain">=ipx</code> <code class="ros value">rate</code><code class="ros plain">=10M</code></div></div></td></tr></tbody></table>

还有其他选项，请查看 [ACL 部分](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-SwitchRules(ACL))找出所有用来匹配数据包的参数。

开关规则表用于 QoS 功能，请参阅[此表](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-Models)查看每个设备支持多少规则。

#3 流量风暴控制

___

从 RouterOS v6.42 开始，可以启用流量风暴控制。 当某些帧在网络上不断泛滥时，可能会出现流量风暴。 例如，如果已创建网络环路并且未使用环路控制机制（例如 [生成树协议](https://help.mikrotik.com/docs/display/ROS/Spanning+Tree+Protocol)），则广播或多播帧会迅速淹没网络，导致网络性能下降甚至完全崩溃。 使用 CRS3xx、CRS5xx 系列交换机和 CCR2116、CCR2216 路由器，可以限制广播、未知多播和未知单播流量。 当交换机不包含目标 MAC 地址的主机条目时，将考虑未知单播流量。 当交换机在“/interface bridge mdb”菜单中不包含多播组条目时，就会考虑未知多播流量。 风暴控制设置要应用于入口端口，出口流量将受到限制。

风暴控制参数以链路速度的百分比 (%) 指定。 如果你的链接速度为 1Gbps，则将 `storm-rate` 指定为 `10` 将仅允许转发 100Mbps 的广播、未知多播和/或未知单播流量。

**子菜单:** `/interface ethernet switch port`

| Property                                                                      | Description                                                  |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------ |
| **limit-broadcasts** (_yes                          \| no_; Default: **yes**) | 在一个交换端口上限制广播流量                                 |
| **limit-unknown-multicasts** (_yes                  \| no_; Default: **no**)  | 在一个交换端口上限制未知的多播流量                           |
| **limit-unknown-unicasts** (_yes                    \| no_; Default: **no**)  | 在一个交换端口上限制未知的单播流量                           |
| **storm-rate** (_integer 0..100_; Default: **100**)                           | 广播、未知多播和未知单播流量的数量被限制在链接速度的百分比。 |
 
> 采用Marvell-98DX3236交换芯片的设备无法区分未知组播流量和所有组播流量。 例如，当使用 `limit-unknown-multicasts` 和 `storm-rate` 时，CRS326-24G-2S+ 将限制所有多播流量。 对于其他设备，例如 CRS317-1G-16S+，`limit-unknown-multicasts` 参数将仅限制未知多播流量（不在`/interface bridge mdb` 中的地址）。

例如，要限制 ether1 (1Gbps) 上 1% (10Mbps) 的广播和未知单播流量，请使用以下命令：


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch port</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">ether1 </code><code class="ros value">storm-rate</code><code class="ros plain">=1</code> <code class="ros value">limit-broadcasts</code><code class="ros plain">=yes</code> <code class="ros value">limit-unknown-unicasts</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

#3 MPLS硬件卸载

___

由于 RouterOS v6.41 可以将某些 MPLS 功能卸载到交换机芯片，交换机必须是 PE-P-PE 设置中的 (P)rovider 路由器才能实现硬件卸载。 可以在[基本 MPLS 设置示例](https://wiki.mikrotik.com/wiki/Manual:Basic_MPLS_setup_example "Manual:Basic MPLS setup example") 手册中找到设置示例。 只有当 LDP 接口配置为物理交换机接口（例如以太网、SFP、SFP+）时，才会发生硬件卸载。

目前只有使用 RouterOS v6.41 及更新版本的 CRS317-1G-16S+ 和 CRS309-1G-8S+ 能够硬件卸载某些 MPLS 功能。 `CRS317-1G-16S+` 和 `CRS309-1G-8S+` 内置交换芯片无法从数据包中弹出 MPLS 标签，在 PE-P-PE 设置中，必须使用显式 null 或禁用 TTL 传播 MPLS网络实现硬件卸载。

> 自 RouterOS v7 以来，MPLS 硬件卸载已被删除。

## 交换规则(ACL)

___

访问控制列表包含入口策略和出口策略引擎。 请参阅[此表](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-Models)查看每个设备支持多少条规则。 它是一种基于第 2 层、第 3 层和第 4 层协议头条件进行线速数据包过滤、转发和修改的高级工具。

> 为每个收到的数据包检查 ACL 规则，直到找到匹配项。 如果有多个规则可以匹配，那么只会触发第一个规则。 没有任何操作参数的规则是接受数据包的规则。

> 当交换机 ACL 规则被修改（例如添加、删除、禁用、启用或移动）时，现有的交换机规则将在短时间内处于非活动状态。 这可能会导致在 ACL 规则修改期间发生一些数据包泄漏。
  
**子菜单:** `/interface ethernet switch rule`

| Property                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Description                                                                                                                                 |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **copy-to-cpu** (_no                     \| yes_; Default: **no**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | 克隆匹配的数据包发送到CPU                                                                                                                   |
| **disabled** (_yes                       \| no_; Default: **no**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | 启用或禁用ACL条目                                                                                                                           |
| **dscp** (_0..63_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | 匹配DSCP 字段的数据包                                                                                                                       |
| **dst-address** (_IP address/Mask_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | 匹配目IP地址和掩码，也匹配ARP报文中的目的IP。                                                                                               |
| **dst-address6** (_IPv6 address/Mask_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | 匹配目IPv6地址和掩码，也匹配 ARP 数据包中的源 IP。                                                                                          |
| **dst-mac-address** (_MAC address/Mask_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | 匹配目标 MAC 地址和掩码。                                                                                                                   |
| **dst-port** (_0..65535_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 匹配目标协议的端口号                                                                                                                        |
| **flow-label** (_0..1048575_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | 匹配 IPv6 流标签。                                                                                                                          |
| **mac-protocol** (_802.2                 \| arp                                                                                                                                                                                                                                         \| homeplug-av                                                                                     \| ip    \| ipv6    \| ipx \| lldp \| loop-protect \| mpls-multicast \| mpls-unicast \| packing-compr \| packing-simple \| pppoe   \| pppoe-discovery \| rarp     \| service-vlan \| vlan \| or 0..65535 \| or 0x0000-0xffff_)                                                                                                                                                                                                                                                                                | 匹配由协议名称或编号指定的特定 MAC 协议                                                                                                     |
| **mirror** (_no                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    \| yes_)              | 克隆匹配的数据包并将其发送到镜像目标端口。                                                                                                  |
| **new-dst-ports** (_ports_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 按指定的更改目标端口。 空设置将丢弃数据包。 指定的端口会将数据包重定向到它。 当不使用该参数时，数据包将被接受。 不支持多个“new-dst-ports”。 |
| **new-vlan-id** (_0..4095_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 将 VLAN ID 更改为指定值。 需要 `vlan-filtering=yes`。                                                                                       |
| **new-vlan-priority** (_0..7_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | 更改 VLAN 优先级（优先级代码点）。 需要 `vlan-filtering=yes`。                                                                              |
| **ports** (_ports_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | 规则将用于接收流量的匹配端口。                                                                                                              |
| **protocol** (_dccp                      \| ddp                                                                                                                                                                                                                                         \| egp                                                                                             \| encap \| etherip \| ggp \| gre  \| hmp          \| icmp           \| icmpv6       \| idpr-cmtp     \| igmp           \| ipencap \| ipip            \| ipsec-ah \| ipsec-esp    \| ipv6 \| ipv6-frag   \| ipv6-nonxt         \| ipv6-opts                                                             \| ipv6-route \| iso-tp4 \| l2tp \| ospf \| pim \| pup \| rdp \| rspf \| rsvp \| sctp \| st \| tcp \| udp \| udp-lite \| vmtp \| vrrp \| xns-idp \| xtp \| or 0..255_)                                | 匹配由协议名称或编号指定的特定 IP 协议。                                                                                                    |
| **rate** (_0..4294967295_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 为匹配的流量设置入口流量限制（bps）。                                                                                                       |
| **redirect-to-cpu** (_no                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  \| yes_)                       | 将匹配数据包的目标端口更改为 CPU。                                                                                                          |
| **src-address** (_IP address\/Mask_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 匹配源IP地址和掩码                                                                                                                          |
| **src-address6** (_IPv6 address/Mask_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | 匹配源IPv6地址和掩码                                                                                                                        |
| **src-mac-address** (_MAC address/Mask_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | 匹配源MAC地址和掩码                                                                                                                         |
| **src-port** (_0..65535_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 匹配源协议端口号                                                                                                                            |
| **switch** (_switch group_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 要应用规则的匹配的交换组。                                                                                                                  |
| **traffic-class** (_0..255_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | 匹配 IPv6 流量类别。                                                                                                                        |
| **vlan-id** (_0..4095_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | 匹配的 VLAN ID。 需要 `vlan-filtering=yes`。                                                                                                |
| **vlan-header** (_not-present                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               \| present_) | 匹配是否存在的 VLAN 头。 需要 `vlan-filtering=yes`。                                                                                        |
| **vlan-priority** (_0..7_)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 匹配的 VLAN 优先级（优先级代码点）。                                                                                                        |

动作参数:

-   copy-to-cpu
-   redirect-to-cpu
-   mirror
-   new-dst-ports (可丢弃的数据包)
-   new-vlan-id
-   new-vlan-priority
-   rate

Layer2条件参数:

-   dst-mac-address
-   mac-protocol
-   src-mac-address
-   vlan-id
-   vlan-header
-   vlan-priority

Layer3条件参数:

-   dscp
-   protocol
-   IPv4 conditions:
    -   dst-address
    -   src-address
-   IPv6 conditions:
    -   dst-address6
    -   flow-label
    -   src-address6
    -   traffic-class

Layer4条件参数:

-   dst-port
-   src-port

  

> 要使 VLAN 相关匹配器或 VLAN 相关操作参数起作用，你需要在网桥接口上启用 `vlan-filtering` 并确保在这些端口上启用硬件卸载，否则，这些参数将不起作用。

> 当网桥接口 ether-type 设置为 0x8100 时，VLAN 相关的 ACL 规则与 0x8100 (CVID) 数据包相关，这包括 vlan-id 和 new-vlan-id。 当网桥接口 `ether-type` 设置为 `0x88a8` 时，ACL 规则与 0x88A8（SVID）数据包相关。

## 端口安全

___

可以限制单个交换机端口上允许的 MAC 地址。 例如，要在交换机端口上允许 64:D1:54:81:EF:8E MAC 地址，首先将多个端口一起交换，此示例中64:D1:54:81:EF:8E 将位于后面 **ether1**。

创建一个 ACL 规则允许给定的 MAC 地址并丢弃 **ether1** 上的所有其他流量（对于入口流量):


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ethernet switch rule</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">src-mac-address</code><code class="ros plain">=64:D1:54:81:EF:8E/FF:FF:FF:FF:FF:FF</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">new-dst-ports</code><code class="ros plain">=</code><code class="ros string">""</code> <code class="ros value">ports</code><code class="ros plain">=ether1</code> <code class="ros value">switch</code><code class="ros plain">=switch1</code></div></div></td></tr></tbody></table>

将所有需要的端口一起交换，禁用 MAC 学习并禁用 **ether1** 上的未知单播泛滥：


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=bridge1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge port</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">hw</code><code class="ros plain">=yes</code> <code class="ros value">learn</code><code class="ros plain">=no</code> <code class="ros value">unknown-unicast-flood</code><code class="ros plain">=no</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether2</code> <code class="ros value">hw</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

为 64:D1:54:81:EF:8E 添加静态主机条目（用于出口流量）：


<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge host</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">bridge</code><code class="ros plain">=bridge1</code> <code class="ros value">interface</code><code class="ros plain">=ether1</code> <code class="ros value">mac-address</code><code class="ros plain">=64:D1:54:81:EF:8E</code></div></div></td></tr></tbody></table>

广播流量仍将从 **ether1** 发出。 要限制桥接端口上的广播流量泛滥，你可以使用“广播泛滥”参数来交换它。 请注意，某些协议依赖于广播流量，例如流式传输协议和 DHCP。

## 双启动

___

“双启动”功能允许选择你喜欢在 CRS3xx 系列交换机、RouterOS 或 SwOS 上使用的操作系统。 可以使用以下方式更改设备操作系统：

- 命令行（`/system routerboard settings set boot-os=swos`）
- Winbox
- 网络图
- 串行控制台

有关 SwOS 的更多详细信息，请参见此处：[SwOS 手册](https://help.mikrotik.com/docs/display/SWOS/SwOS)

## 使用 RouterOS 配置 SwOS

___

从 RouterOS 6.43 开始，可以加载、保存和重置 SwOS 配置，以及升级 SwOS 并使用 RouterOS 为 CRS3xx 系列交换机设置 IP 地址。

- 使用 `/system swos save-config` 保存配置

配置将以 `swos.config` 作为文件名保存在同一台设备上，请记得从设备下载文件，因为配置文件将在重启后删除。

- 使用`/system swos load-config`加载配置
- 使用`/system swos password`更改密码
- 使用 `/system swos reset-config` 重置配置
- 使用`/system swos upgrade`从 RouterOS 升级 SwOS

升级命令将自动安装最新可用的 SwOS 版本，确保设备可以访问 Internet，以便升级过程正常进行。 当设备启动进入 SwOS 时，版本号将包含字母“p”，表示主版本。 然后，你可以从 SwOS“升级”菜单安装最新可用的 SwOS 二级主版本。

| 属性                                                                                                        | 说明                                                                                                                                                                                                                                      |
| ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address-acquisition-mode** (_dhcp-only \| dhcp-with-fallback \| static_; Default: **dhcp-with-fallback**) | 更改地址获取方式：<br>dhcp-only \- 仅使用 DHCP 客户端获取地址<br>dhcp-with-fallback \- 前 10 秒将尝试使用 DHCP 客户端获取地址。 如果请求不成功，地址将回退到静态，如静态 IP 地址属性所定义<br>static \- 地址由 static-ip-address 属性定义 |
| **allow-from** (_IP/Mask_; Default: **0.0.0.0/0**)                                                          | 可访问交换机的 IP 地址或网络。 默认情况下，任何 IP 地址都可以访问交换机。                                                                                                                                                                 |
| **allow-from-ports** (_name_; Default: )                                                                    | 可访问设备的交换机端口列表。 默认允许所有端口访问交换机                                                                                                                                                                                   |
| **allow-from-vlan** (_integer: 0..4094_; Default: **0**)                                                    | 可访问设备的 VLAN ID。 默认情况下，允许所有 VLAN                                                                                                                                                                                          |
| **identity** (_name_; Default: **Mikrotik**)                                                                | 交换机名称（用于 Mikrotik 邻居发现协议）                                                                                                                                                                                                  |
| **static-ip-address** (_IP_; Default: **192.168.88.1**)                                                     | 交换机的 IP 地址获取模式设置为 dhcp-with-fallback 或静态。 通过设置静态IP地址，地址获取过程不会改变，默认为DHCP with fallback。 这意味着只有当同一广播域中没有 DHCP 服务器时，配置的静态 IP 地址才会变为活动状态                          |

## 参考文档

[CRS Router](https://wiki.mikrotik.com/wiki/Manual:CRS_Router "Manual:CRS Router")

[CRS3xx VLANs with Bonds](https://wiki.mikrotik.com/wiki/Manual:CRS3xx_VLANs_with_Bonds "Manual:CRS3xx VLANs with Bonds")

[Basic VLAN switching](https://help.mikrotik.com/docs/display/ROS/Basic+VLAN+switching)

[Bridge Hardware Offloading](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeHardwareOffloading)

[Route Hardware Offloading](https://help.mikrotik.com/docs/display/ROS/L3+Hardware+Offloading)

[Spanning Tree Protocol](https://help.mikrotik.com/docs/display/ROS/Spanning+Tree+Protocol)

[MTU on RouterBOARD](https://help.mikrotik.com/docs/display/ROS/MTU+in+RouterOS)

[Layer2 misconfiguration](https://help.mikrotik.com/docs/display/ROS/Layer2+misconfiguration)

[Bridge VLAN Table](https://help.mikrotik.com/docs/display/ROS/Bridge+VLAN+Table)

[Bridge IGMP/MLD snooping](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=59277403)

[Multi-chassis Link Aggregation Group](https://help.mikrotik.com/docs/display/ROS/Multi-chassis+Link+Aggregation+Group)