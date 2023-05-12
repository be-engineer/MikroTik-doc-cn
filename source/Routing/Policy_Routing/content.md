# 概述

策略路由是将符合特定条件的流量引导到特定网关的方法。这可以用于强制来自服务器的某些客户或特定协议(例如HTTP流量)始终被路由到某个网关。它甚至可以用来引导本地和海外的流量到不同的网关。

RouterOS实现了几个可以用来完成上述任务的组件:

-路由表
-路由规则
-防火墙mangle标记

# 路由表

一台路由器可以有多个路由表，它们有自己的一组路由，将同一个目的地路由到不同的网关。

可以从“/routing/table”菜单中查看和配置表。

缺省情况下，RouterOS只有 **main** 路由表:

```shell
[admin@rack1_b33_CCR1036] /routing/table> print
Flags: D - dynamic; X - disabled, I - invalid; U - used
0 D name="main" fib
```

如果需要自定义路由表，在使用之前，应该在菜单中定义它。

考虑一个基本的例子，有两个网关172.16.1.1和172.16.2.1，希望只在名为 **myTable** 的路由表中解析到网关172.16.2.1的8.8.8.8:

```shell
/routing table add name=myTable fib
/ip route add dst-address=8.8.8.8 gateway=172.16.1.1
/ip route add dst-address=8.8.8.8 gateway=172.16.2.1@main routing-table=myTable
```

为了让用户创建的表能够解析目的地，主路由表也应该能够解析目的地。

在示例中，主路由表也应该有一条到目的地址8.8.8.8的路由，或者至少有一条缺省路由，因为缺省路由是由DHCP动态添加的，出于安全考虑，最好在主表中也添加8.8.8.8。

```shell
[admin@rack1_b33_CCR1036] /ip/route> print detail Flags: D - dynamic; X - disabled, I - inactive, A - active;
c - connect, s - static, r - rip, b - bgp, o - ospf, d - dhcp, v - vpn, m - modem, y - cop
y;
H - hw-offloaded; + - ecmp
   DAd   dst-address=0.0.0.0/0 routing-table=main pref-src="" gateway=172.16.1.1
         immediate-gw=172.16.1.1%ether8 distance=1 scope=30 target-scope=10
         vrf-interface=ether8 suppress-hw-offload=no
 
 0  As   dst-address=8.8.8.8/32 routing-table=main pref-src="" gateway=172.16.1.1
         immediate-gw=172.16.1.1%ether8 distance=1 scope=30 target-scope=10 suppress-hw-offload=no
 
    DAc   dst-address=172.16.1.0/24 routing-table=main gateway=ether8 immediate-gw=ether8
         distance=0 scope=10 suppress-hw-offload=no local-address=172.16.1.2%ether8
 
    DAc   dst-address=172.16.2.0/24 routing-table=main gateway=ether7 immediate-gw=ether7
         distance=0 scope=10 suppress-hw-offload=no local-address=172.16.2.2%ether7
    
 1  As   dst-address=8.8.8.8/32 routing-table=myTable pref-src="" gateway=172.16.2.1
         immediate-gw=172.16.2.1%ether7 distance=1 scope=30 target-scope=10 suppress-hw-offload=no
```

但是上面的配置还不够，需要一种方法来强制流量使用新创建的表。RouterOS提供了两种选择:

-防火墙mangle-它提供了更多的控制标准，用于引导流量，例如，每个连接或每个包平衡等。有关如何使用mangle标记的更多信息，请参阅 [防火墙标记](https://help.mikrotik.com/docs/display/ROS/Firewall+Marking) 示例。
-路由规则-一组基本参数，可用于快速引导流量。这就是例子中要用到的方法。

不建议同时使用这两种方法，否则您应该确切地知道自己在做什么。如果确实需要在同一设置中同时使用mangle和路由规则，那么请记住，mangle具有更高的优先级，这意味着如果mangle标记的流量可以在表中被解析，那么路由规则将永远不会看到该流量。

路由表的数量限制为4096个唯一表。

# 路由规则

路由规则允许基于基本参数(如源地址、目的地址或接口内)以及其他参数来控制流量。

在这个例子中，希望选择目的地址为8.8.8.8的流量，并且不返回到 **main** 表:

`/routing rule add dst-address=8.8.8.8 action=lookup-only-in-table table=myTable`

假设知道客户连接到ether4，并且只希望该客户将8.8.8.8路由到特定的网关。可以用以下规则:

`/routing rule add dst-address=8.8.8.8 action=lookup-only-in-table table=myTable interface=ether4`

如果由于某种原因，表中使用的网关发生故障，那么整个锁将失败，并且目的地将不可达。在active-backup设置中，我们希望流量能够回到 **main** 表。要做到这一点，将操作从' lookup-only-in-table'更改为' lookup'。

此外，路由规则可以用作“基本的防火墙”。如果不想让连接到ether4的客户访问192.168.1.0/24网络:

`/routing rule add dst-address=192.168.1.0/24 interface=ether4 action=drop`

路由规则可以使用的所有参数列表:

|属性|说明|
| --- | --- |
| **action** (_drop \| lookup \| lookup-only-in-table \| unreachable_) |对匹配数据包采取的动作:<br>- drop -无声地丢弃数据包。<br>- lookup - 在路由表中进行查找。<br>- lookup-only-in-table -只在指定的路由表中查找(参见table参数)。<br>- unreachable - 生成ICMP不可达报文，并返回给源。|
| **comment** (_string_) | |
| **disabled** (_yes \| no_) |禁用规则未使用。|
| **dst-address**() |要匹配的报文的目的地址。|
| **interface** (_string_) |匹配的输入接口。|
| **min-prefix** (_integer[0..4294967295]_) |相当于Linux IP规则' suppress_prefixlength '。例如，如果要抑制路由决策中的缺省路由，则将该值设置为0。|
| **routing-mark** (_string_) |匹配特定的路由标记。|
| **src-address** (_string_) |匹配报文的源地址。|
| **table** (_name_) |要查找的路由表名。|
