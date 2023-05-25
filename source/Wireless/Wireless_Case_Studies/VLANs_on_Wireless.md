# 概述

vlan提供了将设备隔离到不同的Layer2段的可能性，同时仍然使用相同的Layer1介质。这在您希望分离不同类型的用户设备的设置中非常有用。此功能对于无线设置也非常有用，因为您可以使用防火墙隔离不同的虚拟ap并限制对某些服务或网络的访问。下面是在同一设备上设置两个接入点的示例，将它们隔离到不同的vlan中。当您拥有Guest AP和Work AP时，这种情况非常常见。

**例子**

![](https://help.mikrotik.com/docs/download/attachments/122388507/Vlan-wlan1.jpg?version=1&modificationDate=1650965266847&api=v2)

[网桥VLAN过滤](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeVLANFiltering) 自RouterOS v6.41起，在网桥内提供VLAN感知的二层转发和VLAN标签修改功能。

** R1: **

- 在以太网接口上添加必要的VLAN接口，使其成为VLAN trunk端口。在VLAN接口上添加ip地址。
```shell
[admin@R1] >
/interface vlan
add interface=ether1 name=vlan111 vlan-id=111
add interface=ether1 name=vlan222 vlan-id=222
 
/ip address
add address=192.168.1.1/24 interface=vlan111
add address=192.168.2.1/24 interface=vlan222
```

  

**R2:**

- 在wlan1接口下添加VirtualAP，并分别为wlan1和wlan2创建无线安全配置文件

```shell
[admin@R2] >
/interface bridge
add fast-forward=no name=bridge1 vlan-filtering=yes
 
/interface bridge port
add bridge=bridge1 interface=ether2
add bridge=bridge1 interface=wlan1
add bridge=bridge1 interface=wlan2
/interface bridge vlan
add bridge=bridge1 tagged=ether2,wlan1 vlan-ids=111
add bridge=bridge1 tagged=ether2,wlan2 vlan-ids=222
```
  

重要的是将wlan1、wlan2的vlan模式设置为“use-tag”。


- 创建_vlan-filtering=yes_的桥
- 添加必要的桥接端口
- 在 _interface bridge vlan_ section下添加 _tagged_ 接口，并配置正确的 _vlan-ids_

```shell
[admin@R2] >
/interface bridge
add fast-forward=no name=bridge1 vlan-filtering=yes
 
/interface bridge port
add bridge=bridge1 interface=ether2
add bridge=bridge1 interface=wlan1
add bridge=bridge1 interface=wlan2
/interface bridge vlan
add bridge=bridge1 tagged=ether2,wlan1 vlan-ids=111
add bridge=bridge1 tagged=ether2,wlan2 vlan-ids=222
```
  

一些设备有内置的交换芯片，可以在以太网端口之间以线速性能交换数据包。网桥VLAN过滤禁用硬件卸载(除了在CRS3xx系列交换机上)，这将阻止数据包的交换，这不会影响无线接口，因为通过它们的流量无论如何都不能卸载到交换芯片上。

在此设置中不需要VLAN过滤，但出于安全原因强烈建议使用。在某些情况下，不进行VLAN过滤可以转发未知的VLAN id。禁用VLAN过滤确实具有性能优势。

  

**R3:**

- 在wlan1接口添加IP地址。
- 创建兼容R2 wlan1的无线安全配置文件。

```shell
[admin@R3] >
/ip address
add address=192.168.1.3/24 interface=wlan1
 
/interface wireless
set [ find default-name=wlan1 ] disabled=no security-profile=vlan111
```

**R4:**

- 在wlan1接口添加IP地址。
- 创建兼容R2 wlan2的无线安全配置文件。

```shell
[admin@R4] >
/ip address
add address=192.168.2.4/24 interface=wlan1
 
/interface wireless
set [ find default-name=wlan1 ] disabled=no security-profile=vlan222
```