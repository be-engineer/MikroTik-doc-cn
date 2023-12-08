# 无线VLAN聚合

一个非常常见的任务是在无线点对点（PtP）链路上只转发某一组VLAN。自RouterOS v6.41以来，这可以通过网桥VLAN过滤来实现，并且应该用它来代替任何其他方法（包括桥接VLAN接口）。比如要通过无线链路转发到2个不同的VLAN，所有其他的VLAN ID应该被丢弃。VLAN 10是互联网流量，而VLAN 99是管理流量。下面是网络拓扑结构。

![](https://help.mikrotik.com/docs/download/attachments/122388482/Wlan_trunk.jpg?version=1&modificationDate=1653919647235&api=v2)

## 配置

首先在 **AP** 和 **ST** 上创建一个新的网桥，并向其添加 **ether1** 和 **wlan1** 端口。

```shell
/interface bridge
add name=bridge protocol-mode=none
/interface bridge port
add bridge=bridge interface=ether1
add bridge=bridge interface=wlan1

```
  
如果需要的话，可以启用 RSTP，但一般来说，PtP 链接不需要 RSTP，因为不应该发生环路。
  
为了安全起见，应该启用入站过滤，因为你只希望有标记的流量，可以设置网桥过滤掉所有未标记的流量。在 **AP** 和 **ST** 上进行如下操作。

```shell
/interface bridge port
set [find where interface=ether1 or interface=wlan1] frame-types=admit-only-vlan-tagged ingress-filtering=yes

```
  
设置网桥VLAN表。由于 VLAN99 是管理流量，那么需要允许这个 VLAN ID 能够访问网桥接口，否则，当你试图访问设备时，流量就会被丢弃。VLAN10 不需要访问网桥，因为它只是被转发到另一端。为了实现这样的功能，在 **AP** 和 **ST** 的网桥 VLAN 表中加入这些项。
  
```shell
/interface bridge vlan
add bridge=bridge tagged=ether1,wlan1 vlan-ids=10
add bridge=bridge tagged=ether1,wlan1,bridge vlan-ids=99

```
  
可以限制允许从哪些接口访问设备。例如， 如果不希望设备从 `wlan1` 被访问， 那么可以从相应的网桥 VLAN 项中删除该接口。

对于有 [硬件卸载VLAN过滤](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-BridgeHardwareOffloading) 和无线接口支持的设备(如RB4011带RTL8367交换芯片，或LtAP带MT7621交换芯片)，需要更加注意。如果不允许VLAN访问CPU，从HW卸载端口到无线的数据包可以被过滤掉。可以通过将网桥接口添加为VLAN成员（类似于VLAN99的例子）或禁用网桥端口的HW卸载来允许某个VLAN的CPU访问。
  
所有设备（**R1**，**R2**，**AP，** 和 **ST**）都需要创建一个VLAN接口，以便能够通过特定的VLAN ID访问设备。对于 **AP** 和 **ST** 来说，在网桥接口之上创建VLAN接口，并给它分配一个IP地址。

```shell
/interface vlan
add interface=bridge name=MGMT vlan-id=99
/ip address
add address=192.168.99.X/24 interface=MGMT

```

对于 **R1** 和 **R2** 做同样的事情，但创建VLAN接口的接口可能会改变，这取决于设置。

```shell
/interface vlan
add interface=ether1 name=MGMT vlan-id=99
/ip address
add address=192.168.99.X/24 interface=MGMT

```
  
要允许更多的VLAN被转发，只需要在网桥VLAN表中指定更多的VLAN ID，可以指定多个用coma甚至VLAN范围划分的VLAN。
  
在 **AP** 上设置无线链接。

```shell
/interface wireless security-profiles
add authentication-types=wpa2-psk mode=dynamic-keys name=wlan_sec wpa2-pre-shared-key=use_a_long_password_here
/interface wireless
set wlan1 band=5ghz-a/n/ac channel-width=20/40/80mhz-Ceee disabled=no mode=bridge scan-list=5180 security-profile=wlan_sec ssid=ptp_test

```

在 **ST** 上设置无线链接。

```shell
/interface wireless security-profiles
add authentication-types=wpa2-psk mode=dynamic-keys name=wlan_sec wpa2-pre-shared-key=use_a_long_password_here
/interface wireless
set wlan1 band=5ghz-a/n/ac channel-width=20/40/80mhz-Ceee disabled=no mode=station-bridge scan-list=5180 security-profile=wlan_sec ssid=ptp_test

```
  
对于每一种类型的设置，都有不同的要求，对于PtP链接，通常使用NV2无线协议。可以在 [NV2手册](https://wiki.mikrotik.com/wiki/Manual:Nv2 "Manual:Nv2") 上阅读更多关于NV2的信息。

当链接设置好后，可以在 **AP** 和 **ST** 上启用网桥VLAN过滤。

```shell
/interface bridge
set bridge vlan-filtering=yes

```
  
在启用 VLAN 过滤之前，请仔细检查网桥 VLAN 表。错误配置的网桥VLAN表会导致设备无法访问，可能需要重置配置。
