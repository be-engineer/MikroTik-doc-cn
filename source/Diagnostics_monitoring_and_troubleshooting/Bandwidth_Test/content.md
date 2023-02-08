# 概述

```shell
Sub-menu: /tool
Packages required: system
```

带宽测试器可以测量到另一台MikroTik路由器（有线或无线）的吞吐量，帮助发现网络 "瓶颈"。

TCP测试采用有确认功能的标准TCP协议，遵循TCP算法，根据延迟、丢包以及TCP算法中的其他特征来发送多少个数据包。请查阅TCP协议了解内部速度设置和如何分析行为的细节。吞吐量的统计是用整个TCP数据流的大小来计算的。由于确认是TCP的内部工作，它们的大小和链接的使用不包括在吞吐量的统计中。在估计吞吐量时，统计数字不像UDP统计数字那样可靠。

UDP测试器发送的数据包比目前报告的在链路另一端收到的数据包多110%或更多。要看到一个链接的最大吞吐量，数据包大小应设置为链接所允许的最大MTU，通常是1500字节。UDP不需要确认；该方式意味着可以看到最接近吞吐量的情况。

- 在RouterOS 6.44beta39版本中，带宽测试只使用单个CPU核心，在核心100%负载时达到其极限。
- 带宽测试使用所有可用的带宽（默认），可能会影响网络的可用性。

- 带宽测试使用了大量的资源。如果你想测试一个路由器的真实吞吐量，需要通过被测试的路由器运行带宽测试。要做到这一点，至少需要3台路由器连在一起：带宽服务器、被测路由器和带宽客户端。

- 如果使用UDP协议，带宽测试将计算IP头+UDP头+UDP数据。如果使用的是TCP协议，则Bandwidth Test只计算TCP数据（不包括TCP头和IP头）。

## 带宽测试服务器

`Sub-menu: /tool bandwidth-server`
  
| 属性                                                                   | 说明                   |
| ---------------------------------------------------------------------- | ---------------------- |
| **allocate-udp-ports-from** (_integer 1000..64000_; Default: **2000**) | UDP端口范围的开始      |
| **authenticate** (_yes                                                 | no_; Default: **yes**) | 只和经过认证的客户进行通信 |
| **enabled** (_yes                                                      | no_; Default: **yes**) | 定义是否启用带宽服务器     |
| **max-sessions** (_integer 1..1000_; Default: **100**)                 | 最大同时测试次数       |

**例子**

带宽服务器:

```shell
[admin@MikroTik] /tool bandwidth-server> print                                 
                  enabled: yes                                                 
             authenticate: yes                                                 
  allocate-udp-ports-from: 2000                                                
             max-sessions: 100                                                 
[admin@MikroTik] /tool bandwidth-server>
```

活动会话:

```shell
[admin@MikroTik] /tool bandwidth-server session> print
  # CLIENT          PROTOCOL DIRECTION USER
  0 35.35.35.1      udp      send      admin
  1 25.25.25.1      udp      send      admin
  2 36.36.36.1      udp      send      admin
[admin@MikroTik] /tool bandwidth-server session>
```

要启用 **带宽测试** 服务器，不需要客户认证。

```shell
[admin@MikroTik] /tool bandwidth-server> set enabled=yes authenticate=no       
[admin@MikroTik] /tool bandwidth-server> print                                 
                  enabled: yes                                                 
             authenticate: no                                                  
  allocate-udp-ports-from: 2000                                                
             max-sessions: 100                                                 
[admin@MikroTik] /tool bandwidth-server>
```

## 带宽测试客户端

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">Sub-menu</code><code class="ros constants">: /tool bandwidth-test</code></div></div></td></tr></tbody></table>

| 属性                                                                                         | 说明                                                                                                                                                                             |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_IP address \| IPv6 prefix\[%interface\]_; Default:)                            | 主机IP地址                                                                                                                                                                       |
| : **receive**)                                                                               | 数据流方向                                                                                                                                                                       |
| **duration** (_time_; Default: )                                                             | 测试时间                                                                                                                                                                         |
| **interval** (_time: 20ms..5s_; Default: **1s**)                                             | 报告之间的延迟（单位：秒）                                                                                                                                                       |
| **local-tx-speed** (_integer 0..4294967295_; Default: )                                      | 传输测试最高速率（bps）                                                                                                                                                          |
| **local-udp-tx-size** (_integer: 28..64000_)                                                 | 本地传输数据包大小，以字节为单位                                                                                                                                                 |
| **password** (_string_; Default: **""**)                                                     | 远程用户的密码                                                                                                                                                                   |
| **protocol** (_udp                                                \| tcp_; Default: **udp**) | 使用的协议                                                                                                                                                                       |
| **random-data** (_yes                                             \| no_; Default: **no**)   | 如果随机数据设置为 "是"，带宽测试数据包的有效载荷将具有不可压缩的随机数据流，这样使用数据压缩的链接就不会扭曲结果（这是对高速CPU的设置。对于低速CPU，随机数据应该设置为 "否"）。 |
| **remote-tx-speed** (_integer 0..4294967295_; Default: )                                     | 接收测试的最高速率（bps）。                                                                                                                                                      |
| **remote-udp-tx-size** (_integer: 28..64000_)                                                | 远程传输数据包的大小，以字节为单位                                                                                                                                               |
| **connection-count** (_integer 1..100_; Default: **20**)                                     | 使用的TCP连接数                                                                                                                                                                  |
| **user** (_string_; Default: **""**)                                                         | 远程用户                                                                                                                                                                         |

**例子**

对 **10.0.0.32** 主机发送和接收 **1000** 字节的UDP数据包，并使用 **admin** 连接，运行15秒长的带宽测试。

```shell
[admin@MikroTik] /tool> bandwidth-test 10.0.0.32 duration=15s \
\... direction=both local-udp-tx-size=1000 protocol=udp \
\... remote-udp-tx-size=1000 user=admin
                status: done testing
              duration: 15s
            tx-current: 272.8Mbps
  tx-10-second-average: 200.3Mbps
      tx-total-average: 139.5Mbps
            rx-current: 169.6Mbps
  rx-10-second-average: 164.8Mbps
      rx-total-average: 117.0Mbps
          lost-packets: 373
           random-data: no
             direction: both
               tx-size: 1000
               rx-size: 1000
[admin@MikroTik] /tool>
```

**链接本地的IPv6例子**:

```shell
[admin@MikroTik] > /tool bandwidth-test fe80::34:23ff:fe6a:570c%local
                status: running
              duration: 5s
            rx-current: 23.9Mbps
  rx-10-second-average: 15.1Mbps
      rx-total-average: 15.1Mbps
          lost-packets: 0
           random-data: no
             direction: receive
               rx-size: 1500
```
