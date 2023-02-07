# 概述

Netwatch监控网络中的主机状态。监控通过以下探针类型完成。 
1) ICMP - ping到一个指定的IP地址或主机，有一个选项可以调整阈值  
2) Simple - 使用ping，不使用高级指标  
3) TCP conn，测试TCP连接  
4) HTTP GET，针对正在监控的服务器发出请求  
  
对于Netwatch表中的每个条目，可以指定一个IP地址、ping间隔和控制台脚本。Netwatch的主要优点是它能够在主机状态变化时发出任意的控制台命令。

自7.4以来，Netwatch的功能得到了扩展，以前的版本只支持简单的ICMP探测。在升级到新版本时，旧的Netwatch条目将保持不变，报告探测类型为 "Simple"，保留相同的功能。

## 属性

**Sub-menu:** `/tool/netwatch`

| 属性                                                                 | 说明                                                                                                                                                                                                                                                                        |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **host** (Default:"")                                                | 要探测的服务器的IP地址。格式：<br>- _ipv4_  <br>- _ipv4@vrf_  <br>- _ipv6_  <br>- _ipv6@vrf ipv6@vrf_  <br>- _ipv6-linklocal%interface_                                                                                                                                     |
| **type** (icmp _\| tcp-conn\|http-get\|simple;_ Default:: **simple*) | 探针类型: <br>- icmp - (ping-style)带有统计信息的ICMP请求,回应。 <br>- tcp-conn - 测试由IP和端口指定的服务器的TCP连接（3-way handshake）。 <br>- http-get - HTTP获取请求并测试正确的回复  <br>- simple - 简化的ICMP探针，选项比 "ICMP "类型少，用于向后兼容旧的Netwatch版本 |
| **interval** (Default：**10s**)                                      | 探针测试时间间隔                                                                                                                                                                                                                                                            |
| **timeout** (Default: **3s**)                                        | 等待响应的最大时间限制。                                                                                                                                                                                                                                                    |
| **start-delay** (Default: **3s**)                                    | 启动探针前的等待时间（在添加、启用或系统启动时）。                                                                                                                                                                                                                          |
| **up-script** (Default:"")                                           | 探针状态改变 "失败"-->"OK "时要执行的脚本。                                                                                                                                                                                                                                 |
| **down-script** (Default:"")                                         | 在探测状态变化为 "OK"-->"失败 "时执行的脚本。                                                                                                                                                                                                                               |
| **test-script** (Default:"")                                         | 在每次探针测试结束时执行的脚本                                                                                                                                                                                                                                              |

Netwatch 以 *sys 用户身份执行脚本，因此 Netwatch 脚本中任何定义的全局变量都不会被调度员或其他用户读取。

Netwatch限制在 _读、写、测试、重启_ 脚本策略。如果脚本的所有者没有足够的权限来执行脚本中的某个命令，那么该脚本将不会被执行。如果脚本的策略大于 _read,write,test,reboot_ - 那么脚本也不会被执行，请确保你的脚本不超过上述策略。

可以在 _/system/scripts_ 菜单下禁用RouterOS脚本的权限检查。当Netwatch没有足够的权限来执行脚本时很有用，尽管这降低了整体的安全性。建议给脚本分配适当的权限。

## 特定类型的选项

所有特定于一种探针类型的配置选项(如icmp的包间隔)对于其他探针类型(tcp-conn, http-get)都被忽略。

### ICMP探测选项

| 属性                                                              | 说明                                             |
| ----------------------------------------------------------------- | ------------------------------------------------ |
| **packet-interval** (Default: **50ms**)                           | ICMP请求包发送的间隔时间。                       |
| **packet-count** (Default: **10**)                                | 在一次测试中要发送的ICMP数据包的总计数。         |
| **packet-size** (Default: **54** (IPv4) 或 **54** (IPv6))         | IP ICMP数据包的总大小                            |
| **thr-rtt-max** (Default **: 1s**)                                | rtt-max的失败阈值（高于thr-max的值为探测失败）。 |
| **thr-rtt-avg** (Default: **100ms**)                              | rtt-avg的失败阈值                                |
| **thr-rtt-stdev** (Default: **250ms**)                            | rtt-stdev的失败阈值。                            |
| **thr-rtt-jitter** (Default: **1s**)                              | rtt-jitter的失败阈值                             |
| **thr-loss-percent** (Default: **85.0%**)                         | loss-percent的失败阈值。                         |
| **thr-loss-count** (Default: **4294967295**) **4294967295**(max)) | 损失数的失败阈值                                 |  |

### TCP-CONNECT/HTTP-GET 探针选项

| **属性**                   | 说明                                    |
| -------------------------- | --------------------------------------- |
| **port** (Default: **80**) | TCP端口（用于tcp-conn和http-get探测）。 |

### TCP-CONNECT 合格标准

| 属性                                    | 说明                       |
| --------------------------------------- | -------------------------- |
| **thr-tcp-conn-time** (Default: **1s**) | tcp-connect-time的失败阈值 |

### HTTP-GET探针的通过/失败标准

| 属性                                 | 说明                                                                                                                                                                                                                                                                   |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **thr-http-time** (Default: **10s**) | http-resp-time的失败阈值                                                                                                                                                                                                                                               |
| **http-code-min** (Default: **100**) | HTTP响应代码的确定/失败标准。                                                                                                                                                                                                                                          |
| **http-code-max** (Default: **299**) | 在[`http-code-min` , `http-code-max`]范围内的响应是探测通过/OK；超出范围是探测失败。参见 [mozilla-http-status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status "HTTP Status") 或 [rfc7231](https://datatracker.ietf.org/doc/html/rfc7231#section-6 "RFC7231") | 。 |

##探针统计/变量

可以查看统计数据，并在脚本中使用这些变量，记住，包含"-"的变量必须这样写，例如，"one-tests "将是$"one-tests"

### 通用的

| 属性             | 说明                                 |
| ---------------- | ------------------------------------ |
| **name**         | 用户为Netwatch添加的名称             |
| **comment**      | 用户添加的注释                       |
| **host**         | 被探测的主机                         |
| **type**         | 探测类型                             |
| **interval**     | 间隔时间                             |
| **timeout**      | 超时                                 |
| **since**        | 最后一次发生状态变化的时间           |
| **status**       | 探针的当前状态                       |
| **don-tests**    | 到目前为止已经完成的探针测试的总计数 |
| **failed-tests** | 探针测试失败的次数                   |

### ICMP

| 属性               | 说明                            |
| ------------------ | ------------------------------- |
| **sent-count**     | 发出的ICMP数据包                |
| **response-count** | 收到匹配的/有效的ICMP数据包响应 |
| **loss-count**     | 丢失数据包的数量                |
| **loss-percent**   | 丢失数据包数量的百分比          |
| **rtt-avg**        | rtt（数据包往返时间）的平均值   |
| **rtt-min**        | 最小rtt                         |
| **rtt-max**        | 最大rtt                         |
| **rtt-jitter**     | 抖动（=最大-最小）的RTT         |
| **rtt-stdev**      | Rtt的标准偏差                   |

### TCP

| 属性                 | 说明                  |
| -------------------- | --------------------- |
| **tcp-connect-time** | 建立TCP连接所需的时间 |

### HTTP

| 属性                 | 说明                                                                                                                                                                                                      |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **http-status-code** | HTTP响应状态代码（200 OK, 404 Not Found, etc.）。见 [mozilla-http-status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) 或 [RFC7231](https://datatracker.ietf.org/doc/html/rfc7231#section-6) |

## 日志

在每个探针OK/Fail状态改变时。

- 探针识别信息和OK->Fail或Fail->OK打印到信息层。
- 详细的探针统计信息和配置被打印到调试级别。

## 状态

命令 _/tool/netwatch/print_ 将显示Netwatch的当前状态和 **只读的** 属性。

- since - 表示主机的某个状态上次改变的时间。
- status - 显示主机的当前状态。
- host - 被监控的地址

## 快速实例

这里将使用一个简单的到IP为8.8.8.8主机的ICMP检查。

```shell
[admin@MikroTik] > /tool/netwatch add host=8.8.8.8 interval=30s up-script=":log info \"Ping to 8.8.8.8 successful\""
```

之后在日志部分可以看到Netwatch执行的脚本。

```shell
[admin@MikroTik] > log print where message~"8.8.8.8"
08:03:26 script,info Ping to 8.8.8.8 successful
```
