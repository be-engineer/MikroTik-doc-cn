#概述

MikroTik Torch是一个实时流量监测工具，可用于监测通过接口的流量。 
请观看 [关于此功能的视频]（https://youtu.be/45E2uwI3xhc）。

出现在Torch中的流量是在它被防火墙过滤之前。意味着能够看到可能被防火墙规则丢弃的数据包。

`[admin@MikroTik] > /tool/torch`

可以通过以下分类监控流量:

- source address (IPv4 and IPv6);
- destination address (IPv4 and IPv6);
- port;
- protocol;
- mac-protocol;
- VLAN ID;
- mac-address;
- DSCP;

MikroTik Torch会显示所选择的协议以及特定接口上每个协议的TX/RX速率。

启用了客户端对客户端转发的无线客户端之间的单播流量在Torch工具中是不可见的。启用硬件卸载桥接处理的数据包也不可见（未知的单播、广播和一些多播流量将对Torch工具可见）。
