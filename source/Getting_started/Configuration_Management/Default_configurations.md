## 默认配置
所有 MikroTik 设备都带有某种默认配置。 根据电路板类型，有几种不同的配置：

你可以运行命令“/system default-configuration print”来查看确切应用的默认配置命令。

### CPE 路由器

在这种类型的配置中，路由器被配置为无线客户端设备。 WAN接口是一个**无线**接口。 WAN 口已配置 DHCP 客户端，受 IP 防火墙保护，禁用 MAC 发现/连接。

使用此类型配置的路由器列表：

- RB 711,911,912,921,922 - with level3 license
- SXT
- QRT
- SEXTANT
- LHG
- LDF
- DISCl
- Groove
- Metal

### LTE CPE AP路由器

此配置类型适用于同时具有 LTE 和无线接口的路由器。 LTE 接口被视为受防火墙保护的 WAN 端口，并且禁用 MAC 发现/连接。 WAN口的IP地址是自动获取的。 无线配置为接入点并与所有可用的以太网端口桥接。

- wAP LTE Kit
- SXT LTE
- LtAP 4G kit
- LtAP LTE kit

### AP 路由器

这种类型的配置适用于家庭接入点路由器，开箱即用，无需额外配置（路由器密码和无线密钥除外）

第一个以太网始终配置为 WAN 端口（受防火墙保护，启用 DHCP 客户端并禁用 MAC 连接/发现）。 其他以太网端口和无线接口被添加到具有 192.168.88.1/24 地址设置和配置 DHCP 服务器的本地 LAN 网桥。 对于双频路由器，一个无线配置为 5 GHz 接入点，另一个配置为 2.4 GHz 接入点。

使用此类配置的路由器列表：

- RB 450,751,850,951,953,2011,3011,4011
- hEX,PowerBox
- mAP
- wAP,wAP R (没有LTE卡)
- hAP
- cAP
- OmniTIK
- CRS系列具有无线接口

### PTP 桥

带无线接口的桥接以太网。 桥接接口上设置了默认 IP 地址 192.168.88.1/24。 有两种选择——作为 CPE 和作为 AP。 对于 CPE 无线接口设置为“station-bridge”模式，对于 AP 使用“bridge”模式。

使用此类配置的路由器列表：

- DynaDish - as CPE
- Wireless Wire kit
- wAP 60G - 具有level3授权

### WISP 桥

配置与 AP 模式下的 PTP 桥接器相同，只是无线模式设置为 ap_bridge 用于 PTMP 设置。 可以直接使用MAC地址访问路由器。 如果设备连接到启用了 DHCP 服务器的网络，则在桥接接口上配置的 DHCP 客户端将获得 IP 地址，可用于访问路由器。

使用此类配置的路由器列表：

- RB 911,912,921,922 - with Level4 license
- Groove A, RB 711 A
- BaseBox, NetBox
- mANTBox, NetMetal
- wAP 60G AP - 具有level4授权
- LtAP

### 交换

此配置利用交换芯片功能来配置基本交换。 将所有以太网端口添加到交换机组，并在主端口上设置默认 IP 地址 192.168.88.1/24。

使用此类配置的路由器列表：

- FiberBox
- CRS 没有无线接口

### 仅IP

当没有找到具体的配置时，在ether1或combo1或sfp1上设置IP地址192.168.88.1/24。

使用此类配置的路由器列表：

- RB 411,433,435,493,800,M11,M33,1100
- CCR

### CAP

当设备需要用作由 [CAPsMAN](https://help.mikrotik.com/docs/display/ROS/CAPsMAN) 控制的无线客户端设备时，会使用此类配置。

加载 CAP 默认配置时，ether1 被视为配置了 DHCP 客户端的管理端口。 所有其他以太网接口都被桥接并且 wlan1 被设置为由 CAPsMAN 管理。

要加载 CAP 配置，请参阅 [重置按钮手册](https://help.mikrotik.com/docs/display/ROS/Reset+Button)。
