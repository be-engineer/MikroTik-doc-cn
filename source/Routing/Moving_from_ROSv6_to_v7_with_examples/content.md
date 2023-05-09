# 路由表

默认情况下，所有路由都像以前一样被添加到 "主 "路由表中。从配置的角度来看，最大的区别是路由表的限制增加，路由表监控的不同，以及路由如何被添加到特定的路由表（见下例）  
v7引入了一个新的菜单/routing route，它显示所有地址族路由以及所有可能的路由属性的过滤路由。`/ip route` 和 `/ipv6 route` 菜单用于添加静态路由，为了简单起见，只显示基本的路由属性。

关于路由的更深入信息，请看 [IP路由](https://help.mikrotik.com/docs/display/ROS/IP+Routing)

另一个新的变化是，大多数常见的路由打印请求都由路由处理，与v6相比，速度明显提高。

# 使用路由表和策略路由
  

与v6的主要区别是，在配置中实际引用路由表之前，必须将其添加到 `/routing table` 菜单中。  如果路由表要推送路由到FIB，应该指定 **fib** 参数。 
除了菜单的位置外，路由规则的配置是一样的（不是`/ip route rule`，现在是`/routing rule`）。

让我们考虑一个基本的例子，我们想在名为myTable的路由表中只解析8.8.8.8到网关172.16.1.1：

```shell
/routing table add name=myTable fib
/routing rule add dst-address=8.8.8.8 action=lookup-only-in-table table=myTable
/ip route add dst-address=8.8.8.8 gateway=172.16.1.1@main routing-table=myTable
```

  
可以用mangle来代替路由规则，用routing-mark标记数据包，与ROSv6中的方式相同。

# OSPF 配置

OSPFv3和OSPFv2现在合并到一个菜单 `/routing ospf`。在写这篇文章的时候，没有默认的实例和区域。 
要同时启动OSPFv2和OSPFv3实例，要为每个实例创建一个实体，然后为实例添加一个区域。 
  

```shell
/routing ospf instance
add name=v2inst version=2 router-id=1.2.3.4
add name=v3inst version=3 router-id=1.2.3.4
/routing ospf area
add name=backbone_v2 area-id=0.0.0.0 instance=v2inst
add name=backbone_v3 area-id=0.0.0.0 instance=v3inst
```


在这里，已经准备好在网络接口上启动OSPF。在IPv6情况下，可以添加想运行OSPF的接口（与ROSv6相同）或IPv6网络。在第二种情况下，OSPF会自动检测接口。下面是一些接口配置的例子：

```shell
/routing ospf interface-template
add network=192.168.0.0/24 area=backbone_v2
add network=2001:db8::/64 area=backbone_v3
add network=ether1 area=backbone_v3
```

ROSv7使用模板将接口与模板进行匹配，并应用匹配模板的配置。 OSPF菜单 `interface` 和 `neighbor` 包含只读条目，纯粹用于状态监控。

所有的路由分配控制现在纯粹是用路由过滤器选择完成的，在实例中不再有重分配旋钮（由于v7.1beta7的重分配旋钮回来了，需要使用路由过滤器来设置路由成本和类型（如果需要的话）。这具有更大的灵活性，想从哪些协议中重新分配什么路由。 
例如，假设你只想重新分配192.168.0.0/16网络范围内的静态IPv4路由。 
  

```shell
/routing ospf instance
set backbone_v2 out-filter-chain=ospf_out redistribute=static
```

`/routing filter rule add chain=ospf_out rule="if (dst in 192.168.0.0/16) {accept}"`

路由过滤链的默认动作是"丢弃"

# BGP配置

与ROSv6相比，BGP的配置有一个完全的重新设计。第一个最大的区别是没有 **instance** 和 **peer** 配置菜单。取而代之的是 **connection**, **template**  和  **session** 菜单。 
之所以采用这样的结构，是为了严格分割负责连接的参数和BGP协议的特定参数。

让我们从Template开始。它包含所有与BGP协议相关的配置选项。它可以作为动态对等体的模板，对一组对等体应用类似的配置。注意，这与思科设备上的对等体组不一样，在思科设备上，对等体组不仅仅是一个普通的配置。

默认情况下，有一个默认模板，需要设置自己的AS。

`/routing/bgp/template set default as=65533`

从v7.1beta4开始，模板参数在 "连接 "配置中显示。这意味着模板不再是强制性的，基本的BGP连接设置更加简单，类似于ROSv6中的情况。

大多数参数与ROSv6相似，只是有些参数被分组在输出和输入部分，使配置更易读，更容易理解该选项是应用在输入还是输出。如果你熟悉CapsMan，那么语法是一样的，例如，要指定输出选择链，你要设置 `output.filter-chain=myBgpChain`。

也可以从另一个模板继承参数，例如：

```shell
/routing/bgp/template
add name=myAsTemplate as=65500 output.filter-chain=myAsFilter
set default template=myAsTemplate
```

新的路由配置的另一个重要方面是全局的Router ID，在实例中设置router-id和组对等。RouterOS增加了一个默认ID，从任何接口的最高IP中挑选实例-id。默认的BGP模板被设置为使用 "默认 "ID。 
如果出于任何原因需要调整或添加新的实例，可以在 `/routing id` 菜单中完成。 
  

非常有趣的参数是 **input.affinity** 和 **output.affinity**，它们允许控制活动会话的输入和输出将在哪个进程中被处理：

- **alone** - 每个会话的输入和输出都在自己的进程中处理，当有很多内核和很多对等体时，这可能是最好的选择。
- **afi, instance, vrf, remote-as** - 尝试在具有类似参数的进程中运行新会话的输入/输出。
- **main** - 在主进程中运行输入/输出（可能会提高单核的性能，甚至可能在具有少量内核的多核设备上）。
- **input** - 在与输入相同的进程中运行输出（可以只为输出亲和力设置）。

现在我们已经为模板设置了参数，我们可以添加BGP连接。一组最小的参数是 `remote.address`, `template, connect`, `listen` 和 `local.role`。

连接和监听参数指定对等体是否将尝试连接和监听远程地址，或者只是连接或只是监听。在对等体使用多跳连接的情况下，`local.address` 也必须配置（类似于ROSv6中的`update-source`）。

指定一个远程AS号码不是强制性的。ROS v7可以从一个开放的消息中确定远程ASN。只有想接受来自该特定AS的连接时，才应该指定远程AS。

对等体角色现在是一个强制参数，对于基本设置，可以只使用ibgp、ebgp（关于可用角色的更多信息可以在相应的RFC草案 [https://datatracker.ietf.org/doc/draft-ietf-idr-bgp-open-policy/?include\_text=1](https://datatracker.ietf.org/doc/draft-ietf-idr-bgp-open-policy/?include_text=1) 中找到），目前草案中描述的能力、社区和过滤功能还没有实现。

非常基本的iBGP设置是在整个本地网络上监听连接：

```shell
/routing/bgp/connection
add remote.address=10.155.101.0/24 listen=yes template=default local.role=ibgp
```

现在你可以从 `/routing bgp session` 菜单监控所有连接和断开的对等体的状态。

所有路由进程的其他重要调试信息可以从 `/routing stats` 菜单中监控。

```shell
[admin@v7_ccr_bgp] /routing/stats/process> print interval=1
Columns: TASKS, PRIVATE-MEM-BLOCKS, SHARED-MEM-BLOCKS, PSS, RSS, VMS, RETIRED, ID, PID, RPID, PROCESS-TIME, KERNEL-TIME, CUR-B>
# TASKS PRIVATE-M SHARED-ME PSS RSS VMS RET ID PID R PROCESS-TI KERN>
0 routing tables 12.2MiB 20.0MiB 18.7MiB 42.2MiB 83.4MiB 8 main 319 0 19s750ms 8s50>
rib >
connected networks >
1 fib 512.0KiB 0 7.4MiB 30.9MiB 83.4MiB fib 384 1 5s160ms 22s5>
2 ospf 1024.0KiB 1024.0KiB 5.9MiB 25.9MiB 83.4MiB 382 ospf 388 1 1m42s170ms 1m31>
connected networks >
3 fantasy 512.0KiB 0 2061.0KiB 5.9MiB 83.4MiB fantasy 389 1 1s410ms 870m>
4 configuration and reporting 40.0MiB 512.0KiB 45.0MiB 64.8MiB 83.4MiB static 390 1 12s550ms 1s17>
5 rip 768.0KiB 0 5.3MiB 24.7MiB 83.4MiB rip 387 1 1s380ms 1s20>
connected networks >
6 routing policy configuration 512.0KiB 256.0KiB 2189.0KiB 6.0MiB 83.4MiB policy 385 1 1s540ms 1s20>
7 BGP service 768.0KiB 0 2445.0KiB 6.2MiB 83.4MiB bgp 386 1 6s170ms 9s38>
8 BGP Input 10.155.101.217 8.8MiB 6.0MiB 15.6MiB 38.5MiB 83.4MiB 20 21338 1 25s170ms 3s23>
BGP Output 10.155.101.217 >
9 Global memory 256.0KiB global 0 0 >
-- [Q quit|D dump|C-z pause|right]
```

路由过滤与ROSv6有一些不同。在BGP模板中，你现在可以指定output.filter-chain、output.filter-select、input.filter以及几个input.accept-\*选项。

现在input.accept-*允许在传入的消息被解析并存储在内存中之前直接进行过滤，这样可以大大减少内存的使用。常规的输入过滤链只能拒绝前缀，这意味着它仍然会占用内存，并在/routing路由表中显示为 "未激活，已过滤"、 

一个非常基本的BGP输入过滤器的例子，接受来自192.168.0.0/16子网的前缀而不修改任何属性。对于其他前缀，从收到的本地pref值中减去1，并将IGP度量设置为OSPF ext的值。 此外，只接受地址列表中的特定前缀，以减少内存的使用。

```shell
/ip/firewall/address-list
add list=bgp_list dst-address=192.168.1.0/24
add list=bgp_list dst-address=192.168.0.0/24
add list=bgp_list dst-address=172.16.0.0/24
 
/routing/bgp/template
set default input.filter=bgp_in .accept-nlri=bgp_list
```

```shell
/routing/filter/rule
add chain=bgp_in rule="if (dst in 192.168.0.0/16) {accept}"
add chain=bgp_in rule="set bgp-local-pref -1; set bgp-igp-metric ospf-ext-metric; accept"
```

如果没有指定路由过滤链，BGP将尝试公布它在路由表中能找到的所有活动路由。

路由过滤链的默认动作是 "丢弃"

## 监控广告

RouterOS v7默认关闭了对BGP输出的监控。可以大大减少具有大型路由表的设置中的资源使用。

为了能够看到输出广告，应该采取几个步骤：

- 在BGP连接配置中启用 "output.keep-sent-attributes"。
- 从BGP会话菜单中运行 "dump-saved-advertisements"。
- 从"/routing/stats/pcap "菜单中查看保存的输出。

```shell
[admin@arm-bgp] /routing/bgp/connection>  set 0 output.keep-sent-attributes=yes
[admin@arm-bgp] /routing/bgp/session> print
Flags: E - established
 0 E remote.address=10.155.101.183 .as=444 .id=192.168.44.2 .refused-cap-opt=no .capabilities=mp,rr,gr,as4
     .afi=ip,ipv6 .messages=4 .bytes=219 .eor=""
     local.address=10.155.101.186 .as=456 .id=10.155.255.186 .capabilities=mp,rr,gr,as4 .afi=ip,ipv6
     .messages=1 .bytes=19 .eor=""
     output.procid=66 .filter-chain=bgp_out .network=bgp-nets .keep-sent-attributes=yes
     input.procid=66 ebgp
     hold-time=3m keepalive-time=1m uptime=4s30ms
 
[admin@arm-bgp] /routing/bgp/session> dump-saved-advertisements 0 save-to=test_out.pcap
```

## 网络

最后，你可能注意到 **network** 菜单不见了，可能想知道如何广播自己的网络。现在网络添加到防火墙地址列表中，并在BGP配置中引用。 
以下是ROSv6网络配置：

```shell
/routing bgp network add network=192.168.0.0/24 synchronize=yes
/ip route add dst-address=192.168.0.0/24 type=blackhole
```

would translate to v7 as:

```shell
/ip/firewall/address-list/
add list=bgp-networks address=192.168.0.0/24
 
/ip/route
add dst-address=192.168.0.0/24 blackhole
 
/routing/bgp/connection
set peer_name output.network=bgp-networks
```

当只添加一个网络时，需要做更多的配置，当必须处理大量的网络时，则提供了简单性。 

在v7中，不可能关闭与IGP路由的同步（只有当路由表中存在相应的IGP路由时，网络才会被公布）。

# 路由过滤器

从ROSv7.1beta4开始，路由过滤器的配置被改为类似脚本的配置。规则现在可以有 "if ... then "的语法，根据 "if "语句的条件设置参数或应用动作。

多个没有动作的规则被堆叠在一个规则中，像防火墙一样按顺序执行，原因是 "设置 "参数的顺序很重要，每行写一个 "设置"，可以让人从上到下更容易理解应用了什么动作。 
  
例如，匹配静态默认路由和应用接受动作可以写在一条配置规则中：

```shell
/routing/filter/rule
add chain=ospf_in rule="if (dst==0.0.0.0/0 && protocol static) { accept }"
```

  
例如，ROSv6规则"/routing filter add chain=ospf\_in prefix=172.16.0.0/16 prefix-length=24 protocol=static action=accept "转换为ROSv7时将是这样的：

```shell
/routing/filter/rule
add chain=ospf_in rule="if (dst in 172.16.0.16 && dst-len==24 && protocol static) { accept }"
```

另一个例子从172.16.0.0/16范围内匹配前缀长度等于24的前缀，并设置BGP的med和prepend值

```shell
/routing/filter/rule
add chain=BGP_OUT rule="if (dst-len==24 && dst in 172.16.0.0/16) { \n
    set bgp-med 20; set bgp-path-prepend 2; accept }"
```
  

也可以像这样来匹配前缀的长度范围

```shell
/routing/filter/rule
add chain=BGP_OUT rule="if (dst-len>13 && dst-len<31 && dst in 172.16.0.0/16) { accept }"
```

  
现在可以用过滤规则来匹配或设置社区、大型社区和社区列表中的扩展社区：

```shell
/routing/filter/rule
add chain=bgp_in rule="set bgp-large-communities 200001:200001:10 "
```

如果有很多社区集需要在多个规则中应用，可以定义社区集，用它们来匹配或设置：

```shell
/routing/filter/large-community-set
add set=myLargeComSet communities=200001:200001:10
 
 
/routing/filter/rule
add chain=bgp_in rule="append bgp-large-communities myLargeComSet "
```

  

由于路由目标是在扩展社区属性中编码的，要改变或匹配RT，需要对扩展社区属性进行操作，比如说：

```shell
/routing/filter/rule
add chain=bgp_in rule="set bgp-ext-communities rt:327824:20 "
```

# RPKI

RouterOS实现了一个RTR客户端。你连接到服务器，它将发送路由的有效性信息。这个信息可以用来在路由过滤器中用 "rpki-validate "来验证路由，进一步在过滤器中用 "match-rpki "来匹配确切的状态。

更多信息请参考 [RPKI](https://help.mikrotik.com/docs/display/ROS/RPKI) 文档。

# RIP 配置

要启动 RIP，应该配置好实例。在那里应该选择哪些路由将被 RIP 重新分配，以及是否会重新分配默认路由。

```shell
/routing/rip/instance
add name=instance1 originate-default=never redistribute=connected,static ;
```

应该配置接口-模板。在ROS第7版中不需要像第6版那样定义网络。

```shell
/routing/rip/interface-template
add interfaces=ether1 instance=instance1
```

现在路由器上完成了基本配置。RIP 邻居路由器应该以类似的方式进行配置。 

在ROS v7中，只有当有路由要发送或接收时，邻居才会出现。

ROSv6的前缀列表已被废弃，现在所有的过滤必须由路由过滤器完成。