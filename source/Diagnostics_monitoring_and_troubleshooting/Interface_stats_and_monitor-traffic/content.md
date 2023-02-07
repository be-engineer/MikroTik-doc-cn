# 概述

每个RouterOS接口都包含各种计数器，例如，接收和传输的数据包数量，[快速路径](https://help.mikrotik.com/docs/display/ROS/Packet+Flow+in+RouterOS#PacketFlowinRouterOS-FastPath) 字节数以及连接丢失。

## 统计

使用 `stats` 或 `stats-detail` 命令来打印接口计数器。以 "fp "开头的值表示 [快速路径](https://help.mikrotik.com/docs/display/ROS/Packet+Flow+in+RouterOS#PacketFlowinRouterOS-FastPath) 计数器。 "tx-queue-drop "表示 [接口队列](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-InterfaceQueue) 的丢包数量。

```shell
[admin@MikroTik] > /interface print stats
Flags: R - RUNNING
Columns: NAME, RX-BYTE, TX-BYTE, RX-PACKET, TX-PACKET, TX-QUEUE-DROP
#   NAME        RX-BYTE      TX-BYTE  RX-PACKET  TX-PACKET  TX-QUEUE-DROP
0 R ether1  205 149 015  147 887 338    158 132    150 015              2
1 R ether2   32 400 148  335 690 764         19    216 509              0
2 R ether3  944 043 040   32 392 350    617 271         17              0
3 R ether4    7 038 417   32 398 973          9          4              0
4 R ether5    7 036 903   32 502 437          5          9              0
5   sfp1              0            0          0          0              0
[admin@MikroTik] > /interface print stats-detail
Flags: D - dynamic; X - disabled, R - running; S - slave; P - passthrough
 0  R   name="ether1" last-link-down-time=jul/19/2022 12:37:06 last-link-up-time=jul/19/2022 12:37:09 link-downs=2
        rx-byte=205 164 277 tx-byte=147 977 500 rx-packet=158 254 tx-packet=150 156 tx-queue-drop=2
        fp-rx-byte=199 271 067 fp-tx-byte=0 fp-rx-packet=1 473 603 fp-tx-packet=0
 
 1  R   name="ether2" last-link-down-time=jul/19/2022 12:46:06 last-link-up-time=jul/19/2022 12:46:07 link-downs=10
        rx-byte=32 400 148 tx-byte=335 690 764 rx-packet=19 tx-packet=216 509 tx-queue-drop=0
        fp-rx-byte=33 718 434 fp-tx-byte=67 fp-rx-packet=60 037 fp-tx-packet=1
 
 2  R   name="ether3" last-link-down-time=jul/19/2022 12:46:06 last-link-up-time=jul/19/2022 12:46:08 link-downs=11
        rx-byte=944 043 040 tx-byte=32 392 350 rx-packet=617 271 tx-packet=17 tx-queue-drop=0 fp-rx-byte=6 860 921
        fp-tx-byte=0 fp-rx-packet=46 671 fp-tx-packet=0
 
 3  R   name="ether4" last-link-down-time=jul/19/2022 12:46:06 last-link-up-time=jul/19/2022 12:46:07 link-downs=10
        rx-byte=7 038 417 tx-byte=32 398 973 rx-packet=9 tx-packet=4 tx-queue-drop=0 fp-rx-byte=6 852 283
        fp-tx-byte=0 fp-rx-packet=46 586 fp-tx-packet=0
 
 4  R   name="ether5" last-link-down-time=jul/19/2022 12:46:06 last-link-up-time=jul/19/2022 12:46:08 link-downs=10
        rx-byte=7 036 903 tx-byte=32 502 437 rx-packet=5 tx-packet=9 tx-queue-drop=0 fp-rx-byte=6 850 637
        fp-tx-byte=178 fp-rx-packet=46 568 fp-tx-packet=2
 
 5      name="sfp1" link-downs=0 rx-byte=0 tx-byte=0 rx-packet=0 tx-packet=0 tx-queue-drop=0 fp-rx-byte=0
        fp-tx-byte=0 fp-rx-packet=0 fp-tx-packet=0
```

## 监控流量

使用 `monitor-traffic` 命令可以监控通过任何接口的流量。

```shell
[admin@MikroTik] > /interface monitor-traffic [find]
                         name:     ether1 ether2 ether3 ether4 ether5 sfp1
        rx-packets-per-second:         19      0      0      0      0    0
           rx-bits-per-second:   27.8kbps   0bps   0bps   0bps   0bps 0bps
     fp-rx-packets-per-second:         29      0      0      0      0    0
        fp-rx-bits-per-second:   26.8kbps   0bps   0bps   0bps   0bps 0bps
        tx-packets-per-second:         21      0      0      0      0    0
           tx-bits-per-second:  149.4kbps   0bps   0bps   0bps   0bps 0bps
     fp-tx-packets-per-second:          0      0      0      0      0    0
        fp-tx-bits-per-second:       0bps   0bps   0bps   0bps   0bps 0bps
    tx-queue-drops-per-second:          0      0      0      0      0    0
```

在"/interface ethernet"菜单中可以获得额外的 [以太网统计信息](https://help.mikrotik.com/docs/display/ROS/Ethernet#Ethernet-Stats)。
