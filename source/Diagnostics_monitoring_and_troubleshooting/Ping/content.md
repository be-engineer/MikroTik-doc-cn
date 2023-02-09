# 概述

Ping使用互联网控制消息协议(ICMP)回波消息来确定远程主机是否活动，并确定与之通信时的往返延迟。Ping工具向主机发送ICMP（类型8）消息，并等待ICMP回波（类型0）。事件之间的时间间隔被称为往返时间。如果响应（即所谓的pong）直到该间隔结束还没有到来，我们就认为它已经超时了。报告的第二个重要参数是TTL（生存时间），在处理数据包的每台机器上是递减的。只有当TTL大于源和目的地之间的路由器数量时，数据包才能到达目的地。

## 快速实例

RouterOS Ping工具可以配置额外的参数，例如：

- arp-ping;
- address;
- src-address;
- count;
- dscp;
- interface;
- interval;
- routing-table;
- size;
- ttl;

让我们看看这个简单的例子。

```shell
[admin@MikroTik] > /tool/ping address=10.155.126.252 count=5 interval=200ms 
  SEQ HOST                                     SIZE TTL TIME  STATUS                                                                                                                                                                             
    0 10.155.126.252                             56  64 0ms 
    1 10.155.126.252                             56  64 0ms 
    2 10.155.126.252                             56  64 0ms 
    3 10.155.126.252                             56  64 0ms 
    4 10.155.126.252                             56  64 0ms 
    sent=5 received=5 packet-loss=0% min-rtt=0ms avg-rtt=0ms max-rtt=0ms
```

同样，可以用更短的CLI命令实现。

```shell
[admin@MikroTik] > /ping 10.155.126.252 count=5 interval=50ms              
  SEQ HOST                                     SIZE TTL TIME  STATUS                                                                                                                                                                             
    0 10.155.126.252                             56  64 0ms 
    1 10.155.126.252                             56  64 0ms 
    2 10.155.126.252                             56  64 0ms 
    3 10.155.126.252                             56  64 0ms 
    4 10.155.126.252                             56  64 0ms 
    sent=5 received=5 packet-loss=0% min-rtt=0ms avg-rtt=0ms max-rtt=0ms
```

也可以通过ping多播地址来发现属于多播组的所有主机。

```shell
[admin@MikroTik] > /ping ff02::1
HOST                                    SIZE  TTL TIME  STATUS                                        
fe80::20c:42ff:fe49:fceb                56    64  1ms   echo reply                                    
fe80::20c:42ff:fe72:a1b0                56    64  1ms   echo reply                                    
fe80::20c:42ff:fe28:7945                56    64  1ms   echo reply                                    
fe80::21a:4dff:fe5d:8e56                56    64  3ms   echo reply                                    
    sent=1 received=4 packet-loss=-300% min-rtt=1ms avg-rtt=1ms max-rtt=3ms
```

通过DNS名称进行Ping:

```shell
[admin@MikroTik]  > /ping www.google.com count=5 interval=50ms
  SEQ HOST                                     SIZE TTL TIME  STATUS                                                                                                                                                                             
    0 216.58.207.228                             56  51 14ms
    1 216.58.207.228                             56  51 13ms
    2 216.58.207.228                             56  51 13ms
    3 216.58.207.228                             56  51 13ms
    4 216.58.207.228                             56  51 13ms
    sent=5 received=5 packet-loss=0% min-rtt=13ms avg-rtt=13ms max-rtt=14ms
```

当使用域名和CLI进行Ping时，路由器的DNS用来解析地址。当使用Winbox工具/Ping时，计算机的DNS将用来解析给定的地址。

## MAC Ping

这个子菜单允许启用mac ping服务器。

当mac ping启用时，同一广播域的其他主机可以使用ping工具来ping mac地址：

`[admin@MikroTik]  > /tool mac-server ping set enabled=yes`

Ping MAC 地址:

```shell
[admin@MikroTik]  > /ping 00:0C:42:72:A1:B0
HOST                                    SIZE  TTL TIME  STATUS                                        
00:0C:42:72:A1:B0                       56        0ms 
00:0C:42:72:A1:B0                       56        0ms 
    sent=2 received=2 packet-loss=0% min-rtt=0ms avg-rtt=0ms max-rtt=0ms
```
