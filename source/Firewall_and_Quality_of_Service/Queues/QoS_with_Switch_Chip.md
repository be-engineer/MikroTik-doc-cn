# 交换芯片的QoS介绍

RouterOS中的队列是用CPU资源处理的，所以在CPU相对较弱的设备上用队列限制流量并不是一个有效的办法。换句话说，基于交换的设备很快就会过载，因为它们是用来处理第二层流量的。为了避免这种低效率，RouterOS允许使用交换芯片限制流量。

## CRS3xx、CRS5xx系列，以及CCR2116、CCR2216设备

这一节对应以下设备：

<table style="border: 1px solid #000000"><tbody><tr><td style="border: 1px solid #000000"><strong title=""><u>Model</u></strong></td><td style="border: 1px solid #000000"><strong title="">Switch Chip</strong></td><td style="border: 1px solid #000000"><strong title="">CPU</strong></td><td style="border: 1px solid #000000"><strong title="">Cores</strong></td><td style="border: 1px solid #000000"><strong title="">10G SFP+</strong></td>
<td style="border: 1px solid #000000"><strong title="">10G Ethernet</strong></td><td style="border: 1px solid #000000"><strong title="">25G SFP28</strong></td><td style="border: 1px solid #000000"><strong title="">40G QSFP+</strong></td><td style="border: 1px solid #000000"><strong title="">100G QSFP28</strong></td><td style="border: 1px solid #000000"><strong title="">ACL rules</strong></td><td style="border: 1px solid #000000"><strong title="">Unicast FDB entries</strong></td><td style="border: 1px solid #000000"><strong title="">Jumbo Frame (Bytes)</strong></td></tr><tr><td  style="border: 1px solid #000000">netPower 15FR (CRS318-1Fi-15Fr-2S)</td><td  style="border: 1px solid #000000"><strong>Marvell-98DX224S</strong></td><td  style="border: 1px solid #000000"><strong>800MHz</strong></td><td style="border: 1px solid #000000"><strong>1</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>128</strong></td><td style="border: 1px solid #000000"><strong>16,000</strong></td><td style="border: 1px solid #000000"><strong>10218</strong></td></tr><tr><td style="border: 1px solid #000000">netPower 16P (CRS318-16P-2S+)</td><td style="border: 1px solid #000000"><strong>Marvell-98DX226S</strong></td><td style="border: 1px solid #000000"><strong>800MHz</strong></td><td style="border: 1px solid #000000"><strong>1</strong></td><td style="border: 1px solid #000000"><strong>2</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>128</strong></td><td style="border: 1px solid #000000"><strong>16,000</strong></td><td style="border: 1px solid #000000"><strong>10218</strong></td></tr><tr><td style="border: 1px solid #000000">CRS310-1G-5S-4S+ (netFiber 9/IN)</td><td style="border: 1px solid #000000"><strong>Marvell-98DX226S</strong></td><td style="border: 1px solid #000000"><strong>800MHz</strong></td><td style="border: 1px solid #000000"><strong>1</strong></td><td style="border: 1px solid #000000"><strong>4</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>128</strong></td><td style="border: 1px solid #000000"><strong>16,000</strong></td><td style="border: 1px solid #000000"><strong>10218</strong></td></tr><tr><td style="border: 1px solid #000000">CRS326-24G-2S+ (RM/IN)</td><td style="border: 1px solid #000000"><strong>Marvell-98DX3236</strong></td><td style="border: 1px solid #000000"><strong>800MHz</strong></td><td style="border: 1px solid #000000"><strong>1</strong></td><td style="border: 1px solid #000000"><strong>2</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>128</strong></td><td style="border: 1px solid #000000"><strong>16,000</strong></td><td style="border: 1px solid #000000"><strong>10218</strong></td></tr><tr><td style="border: 1px solid #000000">CRS328-24P-4S+</td><td style="border: 1px solid #000000"><strong>Marvell-98DX3236</strong></td><td style="border: 1px solid #000000"><strong>800MHz</strong></td><td style="border: 1px solid #000000"><strong>1</strong></td><td style="border: 1px solid #000000"><strong>4</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>128</strong></td><td style="border: 1px solid #000000"><strong>16,000</strong></td><td style="border: 1px solid #000000"><strong>10218</strong></td></tr><tr><td style="border: 1px solid #000000">CRS328-4C-20S-4S+</td><td style="border: 1px solid #000000"><strong>Marvell-98DX3236</strong></td><td style="border: 1px solid #000000"><strong>800MHz</strong></td><td style="border: 1px solid #000000"><strong>1</strong></td><td style="border: 1px solid #000000"><strong>4</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>128</strong></td><td style="border: 1px solid #000000"><strong>16,000</strong></td><td style="border: 1px solid #000000"><strong>10218</strong></td></tr><tr><td style="border: 1px solid #000000">CRS305-1G-4S+</td><td style="border: 1px solid #000000"><strong>Marvell-98DX3236</strong></td><td style="border: 1px solid #000000"><strong>800MHz</strong></td><td style="border: 1px solid #000000"><strong>1</strong></td><td style="border: 1px solid #000000"><strong>4</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>128</strong></td><td style="border: 1px solid #000000"><strong>16,000</strong></td><td style="border: 1px solid #000000"><strong>10218</strong></td></tr><tr><td style="border: 1px solid #000000">CRS309-1G-8S+</td><td style="border: 1px solid #000000"><strong>Marvell-98DX8208</strong></td><td style="border: 1px solid #000000"><strong>800MHz</strong></td><td style="border: 1px solid #000000"><strong>2</strong></td><td style="border: 1px solid #000000"><strong>8</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>680</strong></td><td style="border: 1px solid #000000"><strong>32 000</strong></td><td style="border: 1px solid #000000"><strong>10218</strong></td></tr><tr><td style="border: 1px solid #000000">CRS317-1G-16S+</td><td style="border: 1px solid #000000"><strong>Marvell-98DX8216</strong></td><td style="border: 1px solid #000000"><strong>800MHz</strong></td><td style="border: 1px solid #000000"><strong>2</strong></td><td style="border: 1px solid #000000"><strong>16</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>680</strong></td><td style="border: 1px solid #000000"><strong>128,000</strong></td><td style="border: 1px solid #000000"><strong>10218</strong></td></tr><tr><td style="border: 1px solid #000000">CRS312-4C+8XG</td><td style="border: 1px solid #000000"><strong>Marvell-98DX8212</strong></td><td style="border: 1px solid #000000"><strong>650MHz</strong></td><td style="border: 1px solid #000000"><strong>1</strong></td><td style="border: 1px solid #000000"><strong>4 (combo ports)</strong></td><td style="border: 1px solid #000000"><strong>8 + 4 (combo ports)</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>341</strong></td><td style="border: 1px solid #000000"><strong>32,000</strong></td><td style="border: 1px solid #000000"><strong>10218</strong></td></tr><tr><td style="border: 1px solid #000000">CRS326-24S+2Q+</td><td style="border: 1px solid #000000"><strong>Marvell-98DX8332</strong></td><td style="border: 1px solid #000000"><strong>650MHz</strong></td><td style="border: 1px solid #000000"><strong>1</strong></td><td style="border: 1px solid #000000"><strong>24</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>2</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>170</strong></td><td style="border: 1px solid #000000"><strong>32,000</strong></td><td style="border: 1px solid #000000"><strong>10218</strong></td></tr><tr><td style="border: 1px solid #000000">CRS354-48G-4S+2Q+</td><td style="border: 1px solid #000000"><strong>Marvell-98DX3257</strong></td><td style="border: 1px solid #000000"><strong>650MHz</strong></td><td style="border: 1px solid #000000"><strong>1</strong></td><td style="border: 1px solid #000000"><strong>4</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>2</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>170</strong></td><td style="border: 1px solid #000000"><strong>32,000</strong></td><td style="border: 1px solid #000000"><strong>10218</strong></td></tr><tr><td style="border: 1px solid #000000">CRS354-48P-4S+2Q+</td><td style="border: 1px solid #000000"><strong>Marvell-98DX3257</strong></td><td style="border: 1px solid #000000"><strong>650MHz</strong></td><td style="border: 1px solid #000000"><strong>1</strong></td><td style="border: 1px solid #000000"><strong>4</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>2</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>170</strong></td><td style="border: 1px solid #000000"><strong>32,000</strong></td><td style="border: 1px solid #000000"><strong>10218</strong></td></tr><tr><td style="border: 1px solid #000000">CRS504-4XQ-IN</td><td style="border: 1px solid #000000"><strong>Marvell-98DX4310</strong></td><td style="border: 1px solid #000000"><strong>650MHz</strong></td><td style="border: 1px solid #000000"><strong>1</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>4</strong></td><td style="border: 1px solid #000000"><strong>1024</strong></td><td style="border: 1px solid #000000"><strong>128,000</strong></td><td style="border: 1px solid #000000"><strong>10218</strong></td></tr><tr><td style="border: 1px solid #000000">CCR2116-12G-4S+</td><td style="border: 1px solid #000000"><strong>Marvell-98DX3255</strong></td><td style="border: 1px solid #000000"><strong>2000MHz</strong></td><td style="border: 1px solid #000000"><strong>16</strong></td><td style="border: 1px solid #000000"><strong>4</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>512</strong></td><td style="border: 1px solid #000000"><strong>32,000</strong></td><td style="border: 1px solid #000000"><strong>9570</strong></td></tr><tr><td style="border: 1px solid #000000">CCR2216-1G-12XS-2XQ</td><td style="border: 1px solid #000000"><strong>Marvell-98DX8525</strong></td><td style="border: 1px solid #000000"><strong>2000MHz</strong></td><td style="border: 1px solid #000000"><strong>16</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>12</strong></td><td style="border: 1px solid #000000"><strong>-</strong></td><td style="border: 1px solid #000000"><strong>2</strong></td><td style="border: 1px solid #000000"><strong>1024</strong></td><td style="border: 1px solid #000000"><strong>128,000</strong></td><td style="border: 1px solid #000000"><strong>9570</strong></td></tr></tbody></table>

本文适用于CRS3xx、CRS5xx系列交换机，不适用于CRS1xx/CRS2xx系列交换机!

对于CRS3xx系列交换机，可以用ACL规则来限制符合某些参数的入站流量，也可以按端口来限制入站/出站流量。监控器用于入站流量，整形器用于出站流量。入站监控器通过丢弃数据包来控制收到的流量。所有超过定义限制的数据都会被丢弃。这可能会影响到终端主机的TCP拥堵控制机制，实现的带宽实际上可能比定义的要少。出站整形器试图将超过限制的数据包排队，而不是丢弃它们。最终，当输出队列满了，它也会丢弃数据包，但是，它应该允许更好地利用定义的吞吐量。

基于端口的流量监控（入站）和整形器（出站）。

`/interface ethernet switch port`

`set ether1 ingress-rate =10M egress-rate =5M`

基于MAC的流量监控器:

`/interface ethernet switch rule`

`add ports =ether1 switch =switch1 src-mac-address =64:D1:54:D9:27:E6/FF:FF:FF:FF:FF:FF rate =10M`

基于VLAN的流量监控器:

`/interface bridge`

`set bridge1 vlan-filtering =yes`

`/interface ethernet switch rule`

`add ports =ether1 switch =switch1 vlan-id =11 rate =10M`

基于协议的流量监控器:

`/interface ethernet switch rule`

`add ports =ether1 switch =switch1 mac-protocol =ipx rate =10M`

## CRS1xx/CRS2xx系列设备

该节不能用于CRS3XX系列设备!

## 配置方案

基于MAC的流量调度和整形: [MAC address in UFDB] -> [QoS Group] -> [Priority] -> [Queue] -> [Shaper]

基于VLAN的流量调度和整形: [VLAN id in VLAN table] -> [QoS Group] -> [Priority] -> [Queue] -> [Shaper]

基于协议的流量调度和整形: [Protocol in Protocol VLAN table] -> [QoS Group] -> [Priority] -> [Queue] -> [Shaper]

基于PCP/DEI的流量调度和整形: [Switch port PCP/DEI mapping] -> [Priority] -> [Queue] -> [Shaper]

基于DSCP的流量调度和整形: [QoS DSCP mapping] -> [Priority] -> [Queue] -> [Shaper]

## 使用内部优先级进行基于MAC的流量调度

## 基于MAC的流量调度使用内部优先级

在严格的优先级调度模式下，最高优先级的队列首先被服务。队列号代表优先级，队列号最高的队列具有最高优先级。流量从最高优先级队列发送，直到该队列为空，然后移动到下一个最高优先级队列，以此类推。如果出站端口没有出现拥堵，数据包一收到就被发送。如果在高优先级流量不断到来的端口上发生拥堵，低优先级队列就会饿死。

在所有的CRS交换机上，基于MAC的出口流量调度是根据内部优先级进行的，方案如下: [MAC address] -> [QoS Group] -> [Priority] -> [Queue];  
在这个例子中，主机1（E7:16:34:00:00:01）和主机2（E7:16:34:00:00:02）拥有较高的优先级1，其余的主机拥有较低的优先级0，用于在 ether7端口发送流量。注意，CRS每个端口最多有8个队列。

```shell
/interface bridge
add name =bridge1
/interface bridge port
add bridge =bridge1 interface =ether6 hw =yes
add bridge =bridge1 interface =ether7 hw =yes
add bridge =bridge1 interface =ether8 hw =yes
```

创建一个供UFDB使用的QoS组:

`/interface ethernet switch qos-group`

`add name =group1 priority =1`

添加UFDB条目以匹配ether7上的特定MAC并应用QoS组1:

```shell
/interface ethernet switch unicast-fdb
add mac-address =E7:16:34:00:00:01 port =ether7 qos-group =group1 svl =yes
add mac-address =E7:16:34:00:00:02 port =ether7 qos-group =group1 svl =yes
```

配置ether7端口队列，根据严格的优先级和QoS方案工作，只针对目标地址。:

```shell
/interface ethernet switch port
set ether7 per-queue-scheduling = "strict-priority :0,strict-priority:0,strict-priority:0,strict-priority:0,strict-prior
    ity :0,strict-priority:0,strict-priority:0,strict-priority:0" priority-to-queue=0:0,1:1 
    qos-scheme-precedence =da-based
```

## 基于MAC的流量整形使用内部优先级

基于MAC的流量整形是根据内部优先级来完成的，方案如下。[MAC address] -> [QoS Group] -> [Priority] -> [Queue] -> [Shaper]。
在这个例子中，不限流量的优先级是0，有限流量的优先级是1，带宽限制是10Mbit。注意，CRS每个端口最多有8个队列。

创建一个用于交换的端口组：

```shell
/interface bridge
add name =bridge1
/interface bridge port
add bridge =bridge1 interface =ether6 hw =yes
add bridge =bridge1 interface =ether7 hw =yes
add bridge =bridge1 interface =ether8 hw =yes
```

创建供UFDB使用的QoS组:

```shell
/interface ethernet switch qos-group
add name =group1 priority =1
```

添加UFDB条目以匹配ether8上的特定MAC并应用QoS组1:

```shell
/interface ethernet switch unicast-fdb
add mac-address =E7:16:34:A1:CD:18 port =ether8 qos-group =group1 svl =yes
```

配置ether8端口队列，根据严格的优先级和QoS方案工作，只针对目标地址。:

```shell
/interface ethernet switch port
set ether8 per-queue-scheduling = "strict-priority :0,strict-priority:0,strict-priority:0,strict-priority:0,strict-prior
    ity :0,strict-priority:0,strict-priority:0,strict-priority:0" priority-to-queue=0:0,1:1 
    qos-scheme-precedence =da-based
```

在ether8上为queue1应用带宽限制:

`/interface ethernet switch shaper`
`add port =ether8 rate =10M target =queue1`

如果CRS交换机支持访问控制列表，这个配置就比较简单了:

```shell
/interface ethernet switch acl policer
add name =policer1 yellow-burst =100k yellow-rate =10M
/interface ethernet switch acl
add mac-dst-address =E7:16:34:A1:CD:18 policer =policer1
```

## 基于VLAN的流量调度+使用内部优先级的整形

最好的做法是为被整形器限制的流量分配较低的内部QoS优先级，使其在严格的优先级调度器中不那么重要。(更高的优先级应该是更重要的和无限的）。

例子：
交换机端口ether6正在使用一个整形器限制来自ether7和ether8的流量。
当一条链路达到其容量时，具有最高优先级的流量将被首先发送出去。
VLAN10 -> QoS group0 = lowest priority  
VLAN20 -> QoS group1 = normal priority  
VLAN30 -> QoS group2 = highest priority

```shell
/interface bridge
add name =bridge1
/interface bridge port
add bridge =bridge1 interface =ether6 hw =yes
add bridge =bridge1 interface =ether7 hw =yes
add bridge =bridge1 interface =ether8 hw =yes
```

创建用于VLAN表的QoS组:

`/interface ethernet switch qos-group`
`add name =group0 priority =0`
`add name =group1 priority =1`
`add name =group2 priority =2`

添加VLAN条目，对某些VLAN应用QoS组:

`/interface ethernet switch vlan`
`add ports =ether6,ether7,ether8 qos-group =group0 vlan-id =10`
`add ports =ether6,ether7,ether8 qos-group =group1 vlan-id =20`
`add ports =ether6,ether7,ether8 qos-group =group2 vlan-id =30`

配置ether6、ether7、ether8端口队列，使其根据严格的优先级和QoS方案工作，仅用于基于VLAN的QoS:

```shell
/interface ethernet switch port
set ether6 per-queue-scheduling = "strict-priority :0,strict-priority:0,strict-priority:0,strict-priority:0,strict-prior
    ity :0,strict-priority:0,strict-priority:0,strict-priority:0" priority-to-queue=0:0,1:1,2:2 
    qos-scheme-precedence =vlan-based
set ether7 per-queue-scheduling = "strict-priority :0,strict-priority:0,strict-priority:0,strict-priority:0,strict-prior
    ity :0,strict-priority:0,strict-priority:0,strict-priority:0" priority-to-queue=0:0,1:1,2:2 
    qos-scheme-precedence =vlan-based
set ether8 per-queue-scheduling = "strict-priority :0,strict-priority:0,strict-priority:0,strict-priority:0,strict-prior
    ity :0,strict-priority:0,strict-priority:0,strict-priority:0" priority-to-queue=0:0,1:1,2:2 
    qos-scheme-precedence =vlan-based
```

在ether6上应用带宽限制:

`/interface ethernet switch shaper`
`add port =ether6 rate =10M`

## 基于PCP的流量调度

默认情况下，CRS1xx/CRS2xx系列设备将忽略PCP/CoS/802.1p值，并基于FIFO（先进先出）方式转发数据包。当设备的内部队列未满时，那么数据包是以先进先出的方式，但只要队列被填满，更高优先级的流量就可以先发出去。考虑一个场景，当 **ether1** 和 **ether2** 正在向 **ether3** 转发数据，但是当 **ether3** 拥堵时，那么数据包就要被安排好，可以配置交换机保留最低优先级的数据包，直到所有高优先级的数据包被发送出去，这是VoIP类型设置中非常常见的场景，一些流量需要被优先处理。

为了实现这样的行为，将 **ether1**、**ether2** 和 **ether3** 端口交换到一起：

`/interface bridge`
`add name =bridge1`
`/interface bridge port`
`add bridge =bridge1 interface =ether1 hw =yes`
`add bridge =bridge1 interface =ether2 hw =yes`
`add bridge =bridge1 interface =ether3 hw =yes`

为每个端口上的每个内部队列启用 **严格策略**:

`/interface ethernet switch port`
`set ether1,ether2,ether3 per-queue-scheduling = "strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0,strict-priority:0"`

把每个PCP值映射到一个内部优先级值，为方便起见，只需将PCP映射到一个内部优先级1-1。:

`/interface ethernet switch port`
`set ether1,ether2,ether3 pcp-based-qos-priority-mapping =0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7`

由于交换机会先清空最大的队列，而你需要最高的优先级先得到服务，那可以把这个内部优先级分配给一个队列1-1:

`/interface ethernet switch port`
`set ether1,ether2,ether3 priority-to-queue =0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7`

最后，将每个交换机端口设置为根据PCP值安排数据包:

`/interface ethernet switch port`
`set ether1,ether2,ether3 qos-scheme-precedence =pcp-based`

## 带宽限制

入站端口监控器和整形器都为CRS交换机提供带宽限制功能。

入站端口监控器在端口上设置RX限制:

`/interface ethernet switch ingress-port-policer`
`add port =ether5 meter-unit =bit rate =10M`

整形器在端口上设置TX限制:

`/interface ethernet switch shaper`
`add port =ether5 meter-unit =bit rate =10M`

## 流量风暴控制

同样的入站端口监控器也可用于流量风暴控制，以防止广播、多播或单播流量风暴对二层端口造成的干扰。

ether5端口的广播风暴控制例子，每秒有500个数据包的限制：

`/interface ethernet switch ingress-port-policer`
`add port =ether5 rate =500 meter-unit =packet packet-types =broadcast`

例子有多种数据包类型，包括ARP和ND协议以及未注册的组播流量。未注册的组播是未在组播转发数据库中定义的流量。

`/interface ethernet switch ingress-port-policer`
`add port =ether5 rate =5k meter-unit =packet packet-types =broadcast,arp-or-nd,unregistered-multicast`
