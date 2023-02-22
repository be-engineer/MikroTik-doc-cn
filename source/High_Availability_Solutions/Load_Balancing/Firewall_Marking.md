# 防火墙标记

本节由基于防火墙的负载均衡方法的设置实例组成。

## 示例 1

## 使用防火墙标记的故障转移

这个例子演示了如何用防火墙标记、过滤器和NAT规则来设置故障转移。

![](https://help.mikrotik.com/docs/download/attachments/5668881/load-balancing-firewall-marking.jpg?version=2&modificationDate=1573202222548&api=v2)

### 详细的概述

#### IP地址

在这个例子中，供应商分配了两条上行链路，一条连接到 **ether1**，另一条连接到 **ether2**。本地网络有两个子网192.168.1.0/24和192.168.2.0/24

`/ip address`

`add address =10.1.101.18/30 interface =ether1`

`add address =10.1.200.18/30 interface =ether2`

`add address =192.168.1.1/24 interface =ether3`

`add address =192.168.2.1/24 interface =ether4`

#### Mangle  

通过ether1接口的连接标记为 **第一**，通过ether2接口的数据包标记为 **其他**。

`/ip firewall mangle`

`add action =mark-connection chain =forward connection-mark =no-mark new-connection-mark =first out-interface =ether1 passthrough =yes`

`add action =mark-connection chain =forward connection-mark =no-mark new-connection-mark =other out-interface =ether2 passthrough =yes`

#### 防火墙过滤器

当主链路发生故障时，将拒绝所有已建立的连接，新的连接将通过辅助链路进行。当主链路再次恢复时，同样的行为也会发生，这里将防止本地IP泄漏到公共网络，这是伪装的缺点之一。

`/ip firewall filter`

`add action =reject chain =forward connection-mark =other out-interface =ether1 reject-with =icmp-network-unreachable`

`add action =reject chain =forward connection-mark =first out-interface =ether2 reject-with =icmp-network-unreachable`

#### NAT

对本地网络使用src-nat而不是masquerade，因为不想清除连接，这是masquerade在主链路失效时的主要功能。用防火墙规则来限制它们（在这个例子的后面）：

`/ip firewall nat`

`add action =src-nat chain =srcnat out-interface =ether1 to-address =10.1.101.18`

`add action =src-nat chain =srcnat out-interface =ether2 to-address =10.1.200.18`

#### Routes

添加两条默认路由。通过 _distance_ 参数设置路由优先级：

`/ip route add gateway =10.1.101.17 distance =1 check-gateway =ping`

`/ip route add gateway =10.1.200.17 distance =2`

## 实例2

## 负载均衡多个相同子网的链接

这个例子演示了在供应商为所有链接提供同一子网的IP地址时，如何设置负载均衡。

![](https://help.mikrotik.com/docs/download/attachments/5668881/load-balancing-firewall-marking-example2.jpg?version=1&modificationDate=1573200375444&api=v2)

### 详细概述

#### IP地址

在这个例子中，我们的供应商分配了两个上游链接，一个连接到 **ether1**，另一个连接到 **ether2**。两个链接的IP地址都来自同一个子网。本地网络有两个子网192.168.1.0/24和192.168.2.0/2。

`/ip address`

`add address =10.1.101.18/24 interface =ether1`

`add address =10.1.101.10/24 interface =ether2`

`add address =192.168.1.1/24 interface =ether3`

`add address =192.168.2.1/24 interface =ether4`

IP地址设置完后，连接的路由将安装为ECMP路由:

```shell
[admin@MikroTik] > /ip route print detail

 0 ADC dst-address =10.1.101.0/24 pref-src =10.1.101.18 gateway =ether1,ether2

        gateway-status =ether1 reachable,ether2 reachable distance =0 scope =10
```

#### Mangle  

在这个例子中，使用了非常简单的策略路由。为每个mangle标记添加路由表： 

`/routing table`

`add fib name =first`

`add fib name =other`

来自192.168.1.0/24子网的客户被标记为使用 **第一** 路由表，192.168.2.0/24则使用 **其他** 子网。

`/ip firewall mangle`

`add action =mark-routing chain =prerouting src-address =192.168.1.0/24 new-routing-mark =first`

`add action =mark-routing chain =prerouting src-address =192.168.2.0/24 new-routing-mark =other`

#### NAT

伪装成本地网络:

`/ip firewall nat`

`add action =masquerade chain =srcnat out-interface =ether1`

`add action =masquerade chain =srcnat out-interface =ether2`

同样可以通过设置路由规则而不是mangle来实现。

#### 路由

要添加两个网关，一个在 **第一个** 路由表中解析，另一个在 **其他 ** 路由表中。

`/ip route`

`add gateway =10.1.101.1@main routing-table =first`

`add gateway =10.1.101.1@main routing-table =other`

## 示例 3 (PCC)

## 负载均衡与每个连接分类器  

### 概述  

PCC匹配器允许把流量分成相等的流，并能把有特定选项集的数据包保留在一个特定的流中（可以从src-address、src-port、dst-address、dst-port等指定这组选项）。 PCC从IP头中选择字段，并在散列算法的帮助下将选择的字段转换为32位数值。然后把这个值除以指定的 _分母_，再把余数与指定的 _余数_ 进行比较，如果相等，则数据包将被捕获。可以从报头中选择src-address、dst-address、src-port、dst-port用于这个操作。

 ```shell
per-connection-classifier=
PerConnectionClassifier ::= [!]ValuesToHash:Denominator/Remainder
  Remainder ::= 0..4294967295    (integer number)
  Denominator ::= 1..4294967295    (integer number)
  ValuesToHash ::= both-addresses|both-ports|dst-address-and-port|
  src-address|src-port|both-addresses-and-ports|dst-address|dst-port|src-address-and-port 
 ```

### 详细的概述

![](https://help.mikrotik.com/docs/download/attachments/5668881/load-balancing-PCC.jpg?version=1&modificationDate=1573205467828&api=v2)

#### IP地址

路由器有两个上游 **ether1** 和 **ether2** 接口，地址为 **10.111.0.2/24** 和 **10.112.0.2/24.**，**ether3** 接口的IP地址为**192.168.1.1/24**。

`/ip address`

`add address =192.168.1.1/24 network =192.168.0.0 broadcast =192.168.0.255 interface =ether3`

`add address =10.111.0.2/30 network =10.111.0.0 broadcast =10.111.0.255 interface =ether1`

`add address =10.112.0.2/30 network =10.112.0.0 broadcast =10.112.0.255 interface =ether2`

#### Mangle

通过策略路由，可以强制所有流量到特定的网关，即使流量的目的地是来自连接网络的主机（而不是网关）。这样会产生路由环路，与这些主机的通信就无法完成了。为了避免这种情况，要允许使用默认路由表来处理连接网络的流量。

`/ip firewall mangle`

`add chain =prerouting dst-address =10.111.0.0/30 action =accept in-interface =ether3`

`add chain =prerouting dst-address =10.112.0.0/30 action =accept in-interface =ether3`

首先要管理从外部发起的连接-回复必须通过同一接口（来自同一公共IP）请求离开。标记所有新进入的连接，记住是什么接口。

`/ip firewall mangle`

`add chain =prerouting in-interface =ether1 connection-mark =no-mark action =mark-connection new-connection-mark =ISP1_conn`

`add chain =prerouting in-interface =ether2 connection-mark =no-mark action =mark-connection new-connection-mark =ISP2_conn`

在配置 _mark-routing_ 之前，必须为每个人创建一个路由表:

`/routing/table`

`add fib name =to_ISP1`

`add fib name =to_ISP2`

动作 _mark-routing_ 只能在mangle chain **output** 和 **prerouting** 中使用，但mangle chain **prerouting** 捕捉所有去往路由器本身的流量。为了避免这种情况，使用 _dst-address-type=！local_ 。而在新的PCC的帮助下，根据源地址和目的地址把流量分成两组:

`/ip firewall mangle`

`add chain =prerouting in-interface =ether3 connection-mark =no-mark dst-address-type =!local per-connection-classifier =both-addresses:2/0 action =mark-connection new-connection-mark =ISP1_conn`

`add chain =prerouting in-interface =ether3 connection-mark =no-mark dst-address-type =!local per-connection-classifier =both-addresses:2/1 action =mark-connection new-connection-mark =ISP2_conn`

然后要对来自这些连接的所有数据包进行适当的标记。由于策略路由只用于前往互联网的流量，不要忘记指定in-interface选项:

`/ip firewall mangle`

`add chain =prerouting connection-mark =ISP1_conn in-interface =ether3 action =mark-routing new-routing-mark =to_ISP1`

`add chain =prerouting connection-mark =ISP2_conn in-interface =ether3 action =mark-routing new-routing-mark =to_ISP2`

`add chain =output connection-mark =ISP1_conn action =mark-routing new-routing-mark =to_ISP1`

`add chain =output connection-mark =ISP2_conn action =mark-routing new-routing-mark =to_ISP2`

#### NAT

由于已经做出路由决定，只要为所有出站数据包固定src-addresses规则。如果这个数据包通过wlan1离开，它将被NAT到10.112.0.2，如果通过wlan2则被NAT到10.111.0.2。:

`/ip firewall nat`

`add chain =srcnat out-interface =ether1 action =masquerade`

`add chain =srcnat out-interface =ether2 action =masquerade`

#### 路由

为每个路由标记创建一个路由

`/ip route`

`add gateway =10.111.0.1@main routing-table =to_ISP1 check-gateway =ping`

`add gateway =10.112.0.1@main routing-table =to_ISP2 check-gateway =ping`

## 实例4（NTH）

## 负载平衡与NTH

### 概述

每个规则都有自己的计数器。当规则收到一个数据包时，当前规则的计数器会加1。如果计数器与 "每个"数据包的值相匹配，则计数器将被设置为零。

如果只用一条规则来匹配50%的流量:

`/ip firewall mangle`

`add action =mark-packet chain =prerouting new-packet-mark =AAA nth =2,1 ;`

为了把流量分成两个以上的部分，可以使用以下配置。第一条规则看到所有的数据包并匹配其中的1/3，第二条规则看到2/3的数据包并匹配其中的一半，第三条规则看到并匹配所有通过前两条规则的数据包（所有数据包的1/3）:

`/ip firewall mangle`

`add action =mark-packet chain =prerouting new-packet-mark =AAA nth =3,1 passthrough =no ;`

`add action =mark-packet chain =prerouting new-packet-mark =BBB nth =2,1 passthrough =no ;`

`add action =mark-packet chain =prerouting new-packet-mark =CCC ;`

这个例子是调度负载均衡例子的一个不同版本。增加了持久的用户会话，也就是说一个特定的用户使用相同的源IP地址进行所有的出站连接。考虑以下网络布局: 

![](https://help.mikrotik.com/docs/download/attachments/5668881/load-balancing-PCC.jpg?version=1&modificationDate=1573205467828&api=v2)

### 详细概述

#### IP地址

路由器有两个上行（WAN）接口，地址为10.111.0.2/24和10.112.0.2/24。局域网接口的名称为 "local"，IP地址为192.168.1.1/24。 

`/ip address`

`add address =192.168.1.1/24 network =192.168.1.0 broadcast =192.168.1.255 interface =Local`

`add address =10.111.0.2/24 network =10.111.0.0 broadcast =10.111.0.255 interface =ether2`

`add address =10.112.0.2/24 network =10.112.0.0 broadcast =10.112.0.255 interface =ether1`

#### Mangle

来自客户的所有流量，如果其IP地址先前被置于地址列表中的 "奇数"，就会立即被标记为连接和路由标记 "奇数"。之后，流量将被排除在预路由链中连续的纠错规则的处理之外:

`/ip firewall mangle`

`add chain =prerouting src-address-list =odd in-interface =Local action =mark-connection new-connection-mark =odd passthrough =yes`

`add chain =prerouting src-address-list =odd in-interface =Local action =mark-routing new-routing-mark =odd`

与上面的配置相同，只是客户的IP地址以前被放在地址列表中的 "偶数":

`/ip firewall mangle`

`add chain =prerouting src-address-list =even in-interface =Local action =mark-connection new-connection-mark =even passthrough =yes`

`add chain =prerouting src-address-list =even in-interface =Local action =mark-routing new-routing-mark =even`

首先把每一个建立新会话的数据包（注意connection-state=new），用连接标记 "奇数 "来标记。所有属于同一会话的连续数据包将带有连接标记 "奇数"。注意，把这些数据包传递给第二和第三条规则（passthrough=yes）。第二条规则把客户端的IP地址添加到地址列表中，使所有连续的会话都能通过同一个网关。第三条规则在所有属于 "奇数 "连接的数据包上放置路由标记 "奇数"，并停止处理预路由链中这些数据包的所有其他纠错规则:

`/ip firewall mangle`

`add chain =prerouting in-interface =Local connection-state =new nth =2,1 action =mark-connection new-connection-mark =odd passthrough =yes`

`add chain =prerouting in-interface =Local action =add-src-to-address-list address-list =odd address-list-timeout =1d connection-mark =odd passthrough =yes`

`add chain =prerouting in-interface =Local connection-mark =odd action =mark-routing new-routing-mark =odd passthrough =no`

这些规则对其余一半流量的处理与前三条规则对前一半流量的处理相同。

下面的代码意味着，每一个从本地网络通过路由器发起的新连接都将被标记为 "奇数 "或 "偶数"，并有路由和连接标记。

`/ip firewall mangle`

`add chain =prerouting in-interface =Local connection-state =new nth =2,2 action =mark-connection new-connection-mark =even passthrough =yes`

`add chain =prerouting in-interface =Local action =add-src-to-address-list address-list =even address-list-timeout =1d connection-mark =even passthrough =yes`

`add chain =prerouting in-interface =Local connection-mark =even action =mark-routing new-routing-mark =even passthrough =no`

以上工作正常。然而在某些情况下，你可能会发现同一个IP地址同时被列在ODD和EVEN的scr-address-list下。这种行为会给需要持久连接的应用程序带来问题。简单补救措施是在mangle规则中添加以下语句，确保新的连接不会已经是ODD src-address-list的一部分。必须对ODD mangle规则做同样的处理，从而排除已经属于EVEN scr-address-list的IP:

`add chain =prerouting in-interface =Local connection-state =new nth =2,2 src-address-list =!odd action =mark-connection new-connection-mark =even passthrough =yes`

#### NAT

根据出站接口固定源地址：

`/ip firewall nat`

`add chain =srcnat out-interface =ether1 action =masquerade`

`add chain =srcnat out-interface =ether2 action =masquerade`

#### 路由

对所有标记为 "奇数 "的流量（有10.111.0.2的翻译源地址），使用10.111.0.1网关。以同样的方式，所有标记为 "偶数 "的流量通过10.112.0.1网关进行路由。

`/ip route`

`add dst-address =0.0.0.0/0 gateway =10.111.0.1 scope =255 target-scope =10 routing-mark =odd`

`add dst-address =0.0.0.0/0 gateway =10.112.0.1 scope =255 target-scope =10 routing-mark =even`

最后，有一个额外的条目指定来自路由器本身的流量（没有任何路由标记的流量）应该转到10.111.0.2网关。:

`add dst-address =0.0.0.0/0 gateway =10.111.0.2 scope =255 target-scope =10`
