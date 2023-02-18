# 连接速率介绍

连接速率是一个防火墙匹配器，允许根据目前的连接速度来捕获流量。

## 理论

连接跟踪表中的每个条目代表双向通信。每当数据包与一个特定的条目关联时，数据包的大小值（包括IP头）就会添加到这个条目的 "连接字节 "值中。(换句话说，"连接字节 "包括上传和下载）。

连接速率根据 "连接字节 "的变化计算连接速度。连接速度每秒钟都会重新计算，没有任何平均数。

"连接字节"和 "连接速率 "这两个选项只对TCP和UDP流量起作用。(要指定一个协议来激活这些选项）。在 "连接率"中可以指定一个想捕捉的速度范围。

```shell
ConnectionRate ::= [!]From-To
  From,To ::= 0..4294967295    (integer number)
```

## 规则实例

这些规则将捕获连接速度低于100kbps时通过路由器的TCP/UDP流量。

`/ip firewall filter`
`add action =accept chain =forward connection-rate =0-100k protocol =tcp`
`add action =accept chain =forward connection-rate =0-100k protocol =udp`

## 应用实例-流量优先级的确定

连接速率可以用各种不同的方式来实现，但最常见的设置是检测和设置较低的优先级给 "重度连接"（长时间保持高速率的连接（如P2P、HTTP、FTP下载）。这样做可以优先考虑所有其他流量，通常包括VOIP和HTTP浏览以及在线游戏。

这个例子中描述的方法可以和其他方法一起使用，以检测和优先处理流量。由于连接率选项没有任何平均数，需要确定识别 "重度连接 "的余量是多少。假设一个正常的HTTP浏览连接长度小于500kB（4Mb），VOIP要求的速度不超过200kbps，那么在第一个500kB之后仍然有超过200kbps速度的每个连接都可以被认为是 "重度"。

(网络中可能有不同的HTTP浏览的 "连接字节 "和不同的VOIP的 "连接速率"，所以，在用这个例子之前，请自己研究)

在这个例子中，假设有一个6Mbps的上传和下载连接到ISP。

## 快速开始

```shell
/ip firewall mangle
add chain =forward action =mark-connection connection-mark =!heavy_traffic_conn new-connection-mark =all_conn
add chain =forward action =mark-connection connection-bytes =500000-0 connection-mark =all_conn connection-rate =200k-100M new-connection-mark =heavy_traffic_conn protocol =tcp
add chain =forward action =mark-connection connection-bytes =500000-0 connection-mark =all_conn connection-rate =200k-100M new-connection-mark =heavy_traffic_conn protocol =udp
add chain =forward action =mark-packet connection-mark =heavy_traffic_conn new-packet-mark =heavy_traffic passthrough =no
add chain =forward action =mark-packet connection-mark =all_conn new-packet-mark =other_traffic passthrough =no
/queue tree
add name =upload parent =public max-limit =6M
add name =other_upload parent =upload limit-at =4M max-limit =6M packet-mark =other_traffic priority =1
add name =heavy_upload parent =upload limit-at =2M max-limit =6M packet-mark =heavy_traffic priority =8
add name =download parent =local max-limit =6M
add name =other_download parent =download limit-at =4M max-limit =6M packet-mark =other_traffic priority =1
add name =heavy_download parent =download limit-at =2M max-limit =6M packet-mark =heavy_traffic priority =8
```

### 解释

在mangle中，要把所有的连接分成两组，然后从这两组中标记数据包。由于讨论的是客户端流量，最合理的标记位置是mangle链的转发。

请记住，一旦 "重 "连接的优先级降低，队列就会达到最大极限，重连接就会降速，连接速率也会降低。这会导致变为更高的优先级，连接能够在短时间内获得更多的流量，这时连接率将再次提高，将再次导致改变为较低的优先级）。为了避免这种情况，必须确保一旦检测到 "重度连接"，将一直被标记为 "重度连接"。

### IP 防火墙mangle

这个规则确保 "重度 "连接将保持"重度"。 并用默认连接标记其余的连接。

`/ip firewall mangle`
`add chain =forward action =mark-connection connection-mark =!heavy_traffic_conn new-connection-mark =all_conn`

这两条规则将根据标准来标记所有的重度连接，即每一个在第一个500kB之后仍然有超过200kbps速度的连接可以认为是 "重度"。

```shell
add chain =forward action =mark-connection connection-bytes =500000-0 \
    connection-mark =all_conn connection-rate =200k-100M new-connection-mark =heavy_traffic_conn protocol =tcp
add chain =forward action =mark-connection connection-bytes =500000-0 \
    connection-mark =all_conn connection-rate =200k-100M new-connection-mark =heavy_traffic_conn protocol =udp
The last two rules in mangle will simply mark all traffic from corresponding connections:
add chain =forward action =mark-packet connection-mark =heavy_traffic_conn new-packet-mark =heavy_traffic passthrough =no
add chain =forward action =mark-packet connection-mark =all_conn new-packet-mark =other_traffic passthrough =no
```

### 队列

这是一个简单的队列树，放在接口HTB上-"public "是ISP连接的接口，而 "local "是客户所在的地方。如果有一个以上的 "public "或一个以上的 "local"，则需要把上传和下载分开，并把队列树放在全局中。

`/queue tree`
`add name =upload parent =public max-limit =6M`
`add name =other_upload parent =upload limit-at =4M max-limit =6M packet-mark =other_traffic priority =1`
`add name =heavy_upload parent =upload limit-at =2M max-limit =6M packet-mark =heavy_traffic priority =8`
`add name =download parent =local max-limit =6M`
`add name =other_download parent =download limit-at =4M max-limit =6M packet-mark =other_traffic priority =1`
`add name =heavy_download parent =download limit-at =2M max-limit =6M packet-mark =heavy_traffic priority =8`
