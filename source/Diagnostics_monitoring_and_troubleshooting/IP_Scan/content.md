# 概述

IP扫描工具允许用户根据网络前缀扫描网络，或通过设置一个接口来监听。无论哪种方式，该工具都会从网络中收集某些数据。

- address - 网络设备的IP地址。
- mac-address - 网络设备的MAC地址。
- time - 找到网络设备时的响应时间。
- DNS - 网络设备的DNS名称。
- SNMP - 设备的SNMP名称。
- NET-BIOS - 设备的NET-BIOS名称，如果设备有通告的话。

使用IP扫描工具时，用户必须选择想要扫描的内容。

- 某些IPv4前缀 - 工具将尝试扫描所有的IP地址或地址设置。
- 路由器的接口 - 工具将尝试监听 "经过"的数据包，并在发现问题时尝试比较结果。

可以同时设置，但结果是不确定的!

## 快速实例

在下面的例子中，将扫描10.155.126.0/24网络上的设备。

```shell
[admin@MikroTik] > /tool ip-scan address-range=10.155.126.1-10.155.126.255
Columns: ADDRESS, MAC-ADDRESS, TIMe, SNMP
  ADDRESS         MAC-ADDRESS        TIM  SNMP    
  10.155.126.1    E4:8D:8C:1C:D3:18  2ms  CCR1036-8G-2S+
  10.155.126.251                     2ms          
  10.155.126.151  E4:8D:8C:49:49:DB  1ms          
  10.155.126.153  6C:3B:6B:48:0E:8B  1ms  750Gr3        
  10.155.126.249  CC:2D:E0:8D:01:88  0ms  CRS328-24P-4S+  
  10.155.126.250  B8:69:F4:B3:1B:D2  0ms          
  10.155.126.252  6C:3B:6B:ED:83:69  0ms          
  10.155.126.253  6C:3B:6B:ED:81:83  0ms
```
