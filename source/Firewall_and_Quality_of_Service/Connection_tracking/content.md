# 介绍

`/ip firewall connection`

有几种方法可以看到哪些连接是通过路由器进行的。

在Winbox防火墙窗口，切换到 "连接 "选项卡查看当前进出路由器的连接。看起来像这样：

![](https://help.mikrotik.com/docs/download/attachments/130220087/Screenshot_1.png?version=1&modificationDate=1653993869514&api=v2)

## 属性

连接表中的所有属性都是只读的

| 属性                                   | 说明                                                                                                |
| -------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **assured** (_yes \| no_)              | 表示这个连接是有保证的，如果达到可能的最大跟踪连接数，不会被删除。                                  |
| **confirmed** (_yes \| no_)            | 连接已确认，有数据包从设备发出。                                                                    |
| **connection-mark** (_string_)         | 由mangle规则设置的连接标记。                                                                        |
| **connection-type** (_pptp \| ftp_)    | 连接类型，如果连接跟踪无法确定预定义的连接类型，则属性为空。                                        |
| **dst-address** (_ip[:port]_)          | 目标地址和端口（如果协议是基于端口的）。                                                            |
| **dstnat** (_yes\| no_)                | 一个连接经过了DST-NAT（例如，端口转发）。                                                           |
| **dying** (_yes\| no_)                 | 连接超时，该连接快要死亡。                                                                          |
| **expected** (_yes\| no_)              | 连接是用连接助手（预定义的服务规则）设置的。                                                        |
| **fasttrack** (_yes\| no_)             | 连接是否是快速跟踪的。                                                                              |
| **gre-key** (_integer_)                | GRE Key字段内容。                                                                                   |
| **gre-protocol** (_string_)            | 封装的有效载荷协议。                                                                                |
| **gre-version** (_string_)             | 连接中使用了GRE协议的一个版本。                                                                     |
| **icmp-code** (_string_)               | ICMP代码域                                                                                          |
| **icmp-id** (_integer_)                | 包含ICMP ID                                                                                         |
| **icmp-type** (_integer_)              | ICMP类型编号                                                                                        |
| **orig-bytes** (_integer_)             | 使用特定连接从源地址发出的字节数。                                                                  |
| **orig-fasttrack-bytes** (_integer_)   | 使用特定连接从源地址发出的快速跟踪字节数。                                                          |
| **orig-fasttrack-packets** (_integer_) | 使用特定连接从源地址发出的快速跟踪数据包的数量。                                                    |
| **orig-packets** (_integer_)           | 使用特定连接从源地址发出的数据包数量。                                                              |
| **orig-rate** (_integer_)              | 使用特定连接从源地址发出的数据包速率。                                                              |
| **protocol** (_string_)                | IP协议类型                                                                                          |
| **repl-bytes** (_integer_)             | 使用特定连接从目标地址接收的字节数。                                                                |
| **repl-fasttrack-bytes** (_string_)    | 使用特定连接从目标地址接收的快速跟踪字节数。                                                        |
| **repl-fasttrack-packets** (_integer_) | 使用特定连接从目标地址收到的快速跟踪数据包数量。                                                    |
| **repl-packets** (_integer_)           | 使用特定连接从目标地址收到的数据包数量。                                                            |
| **repl-rate** (_string_)               | 使用特定连接从目标地址接收数据包的数据速率。                                                        |
| **reply-dst-address** (_ip[:port]_)    | 预计返回数据包的目标地址（和端口）。通常与 "src-address: port "相同。                               |
| **reply-src-address** (_ip[:port]_)    | 返回数据包的源地址（和端口）。通常与 "dst-address: port "相同。                                     |
| **seen-reply** (_yes \| no_)           | 目标地址已回复源地址。                                                                              |
| **src-address** (_ip[:port]_)          | 源地址和端口（如果协议是基于端口的）。                                                              |
| **srcnat** (_yes\| no_)                | 连接正在通过SRC-NAT，包括通过NAT伪装的数据包。                                                      |
| **tcp-state** (_string_)               | TCP连接的当前状态：  <br>- "已建立"<br>- "时间等待"<br>- "关闭"<br>- "已同步发送"<br>- "已同步接收" |
| **timeout** (_time_)                   | 连接从连接列表中删除后的时间。                                                                      |

## 连接跟踪设置

`/ip firewall connection tracking`

### 属性

| 属性                                                   | 说明                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **enabled** (_yes \| no \| auto_; Default: **auto**)   | 禁用或启用连接跟踪。禁用连接跟踪会导致一些防火墙功能停止工作。参见受影响的功能的 [列表](https://wiki.mikrotik.com/wiki/Manual:IP/Firewall/Connection_tracking#Features_affected_by_connection_tracking)。从v6.0rc2开始，默认值为自动。意味着连接跟踪被禁用，直到至少有一条防火墙规则被添加。 |
| **loose-tcp-tracking** (_yes_; Default: **yes**)       | 禁止拾取已建立的连接。                                                                                                                                                                                                                                                                       |
| **tcp-syn-sent-timeout** (_time_; Default: **5s**)     | TCP SYN超时。                                                                                                                                                                                                                                                                                |
| **tcp-syn-received-timeout** (_time_; Default: **5s**) | TCP SYN超时。                                                                                                                                                                                                                                                                                |
| **tcp-established-timeout** (_time_; Default: **1d**)  | 已建立的TCP连接超时。                                                                                                                                                                                                                                                                        |
| **tcp-fin-wait-timeout** (_time_; Default: **10s**)    |
| **tcp-close-wait-timeout** (_time_; Default: **10s**)  |
| **tcp-last-ack-timeout** (_time_; Default: **10s**)    |
| **tcp-time-wait-timeout** (_time_; Default: **10s**)   |
| **tcp-close-timeout** (_time_; Default: **10s**)       |
| **udp-timeout** (_time_; Default: **10s**)             | 指定UDP连接在一个方向上看到数据包的超时。                                                                                                                                                                                                                                                    |
| **udp-stream-timeout** (_time_; Default: **3m**)       | 指定UDP连接在两个方向上看到数据包的超时。                                                                                                                                                                                                                                                    |
| **icmp-timeout** (_time_; Default: **10s*)             | ICMP连接超时                                                                                                                                                                                                                                                                                 |
| **generic-timeout** (_time_; Default: **10m**)         | 所有其他连接项的超时。                                                                                                                                                                                                                                                                       |
  
**只读属性**

| 属性                          | 说明                                                                                                                                                              |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **max-entries** (_integer_)   | 连接跟踪表可容纳的最多条目数量。这个值取决于RAM大小。注意，系统在启动时不会创建一个最大的连接跟踪表，如果情况需要，并且路由器还有空余内存，可以增加最大条目数量。 |
| **total-entries** (_integer_) | 当前连接表拥有的连接数量。                                                                                                                                        |
