# 概述

**Sub-menu:** `/tool traceroute`

**Traceroute** 显示数据包到达远程主机所经过的路由器列表。**traceroute** 或 **tracepath** 工具几乎在所有类Unix操作系统上都可以使用，**tracert** 在Microsoft Windows操作系统上可用。

Traceroute基于TTL值和ICMP "超时 "消息。IP头中的TTL值用来避免路由循环。如果TTL值为零，数据包将被丢弃，发生这种情况时，ICMP超时消息将发回给发送者。

初始traceroute TTL值被设置为1，当下一个路由器发现一个TTL=1的数据包时，它将TTL值设置为0，并以ICMP "超时 "消息回应来源。该消息让源头知道，数据包一跳穿越了特定的路由器,下一次TTL值将增加1，以此类推。通常情况下，在通往目的地的路径中，每个路由器都会将TTL字段递减一个单位TTL值直至为0。

用这个命令，可以看到数据包是如何在网络中传输的，以及它在哪里可能出现故障或速度变慢。利用这些信息，可以确定导致网络问题或故障的计算机、路由器、交换机或其他网络设备。

## 快速示例

```shell
[admin@MikroTik] > tool traceroute 10.255.255.1
     ADDRESS                                    STATUS
   1       10.0.1.17 2ms 1ms 1ms 
   2    10.255.255.1 5ms 1ms 1ms
[admin@MikroTik] >
```
