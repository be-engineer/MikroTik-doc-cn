# 路由过滤

## 过滤语法

路由过滤规则实现了类似脚本的语法。下面的例子是一个路由过滤器的快速演示，它匹配来自子网192.168.1.0/24的前缀长度大于24的前缀，并将默认距离增加1。如果没有匹配，则将默认距离减去1。

```shell
/routing filter rule
  add chain=myChain
  rule="if (dst in 192.168.1.0/24 && dst-len>24) {set distance +1; accept} else {set distance -1; accept}"
```
  
过滤规则可以由多个匹配器和动作组成:

`if ( [matchers] ) { [actions] } else { [actions] }`
  
有两种类型的属性:

- 只读 -那些值只能读不能重写的属性，这些属性只能被匹配器使用
-可读写- 可读写的值，由过滤器使用，也可以由匹配器使用

可读属性可以通过其他可读属性(仅适用于数字属性)或使用布尔运算符的常量值进行匹配。

```shell
[matchers]:
[prop readable] [bool operator] [prop readable]
 
[actions]:
[action] [prop writeable] [value]
```

如果只有一个可能的操作，则不使用布尔运算符。

不带布尔运算符的示例:

`if ( protocol connected ) { accept }`

使用布尔运算符的示例:

`if ( bgp-med < 30 ) { accept }`

使用可读标志属性，matcher使用时不需要指定布尔运算符，也不需要值

`if ( ospf-dn ) { reject }`

请注意，路由过滤器链的默认动作是“拒绝”

### 只读属性

| 属性                             | 类型                                                                         | 说明                                                                                                                                                                                                                                                                                            |
| -------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| _**数值属性**_                   |
| dst-len                          |                                                                              | 目的前缀长度                                                                                                                                                                                                                                                                                    |
| bgp-path-len                     |
| BGP AS-PATH的当前长度            |
| bgp-input-local-as               |                                                                              | 被发送到的本地对等体的AS号                                                                                                                                                                                                                                                                      |
| bgp-input-remote-as              |                                                                              | 接收到前缀的远端对等体的AS号                                                                                                                                                                                                                                                                    |
| bgp-output-local-as              |                                                                              | 将发布该前缀的对等体AS号                                                                                                                                                                                                                                                                        |
| bgp-output-remote-as             |                                                                              | 将该前缀发布到的对等体AS号                                                                                                                                                                                                                                                                      |
| OSPF -metric                     |                                                                              | 当前OSPF度量值                                                                                                                                                                                                                                                                                  |
| OSPF -tag                        |                                                                              | 当前OSPF标签                                                                                                                                                                                                                                                                                    |
| RIP -metric                      |                                                                              | 当前RIP度量值                                                                                                                                                                                                                                                                                   |
| RIP -tag                         |                                                                              | 当前RIP标签                                                                                                                                                                                                                                                                                     |
| _**标志属性**_                   |
| active                           |                                                                              | 路由是否激活                                                                                                                                                                                                                                                                                    |
| bp -atomic-aggregate             |                                                                              |
| BGP - Communities -empty         |                                                                              | BGP Communities属性是否为空                                                                                                                                                                                                                                                                     |
| BGP -ext- Communities -empty     |                                                                              | 表示BGP扩展团体属性是否为空                                                                                                                                                                                                                                                                     |
| BGP - Large - Communities -empty |                                                                              | 表示BGP大团体属性是否为空                                                                                                                                                                                                                                                                       |
| BGP -network                     |                                                                              | 前缀是否来自BGP网络                                                                                                                                                                                                                                                                             |
| OSPF - DN                        |                                                                              | OSPF路由是否设置了DN位。                                                                                                                                                                                                                                                                        |
| _**前缀属性**_                   |
| dst                              |                                                                              | 目的地                                                                                                                                                                                                                                                                                          |
| OSPF -fwd                        |                                                                              | 当前OSPF转发地址                                                                                                                                                                                                                                                                                |
| bgp-input-local-addr             |                                                                              | 发送到的本地对等体IP地址                                                                                                                                                                                                                                                                        |
| bgp-input-remote-addr            |                                                                              | 接收到前缀的远端对等体的IP地址                                                                                                                                                                                                                                                                  |
| bgp-output-local-addr            |                                                                              | 要发布前缀的对等体IP地址                                                                                                                                                                                                                                                                        |
| bgp-output-remote-addr           |                                                                              | 要向其发布前缀的对等体IP地址                                                                                                                                                                                                                                                                    |
| 其他属性                         |
| afi                              | ipv4 \| ipv6 \| l2vpn \| l2vpn-cisco \| vpnv4 \| vpnv6                       | 路由的地址族。                                                                                                                                                                                                                                                                                  |
| bgp-as-path                      | numeric_regexp                                                               | AS路径匹配, [阅读更多](https://help.mikrotik.com/docs/display/ROS/Route+Selection+and+Filters#RouteSelectionandFilters-AS-PATHRegexpMatching)                                                                                                                                                   |
| bgp-as-path-slow-legacy          | string_regexp                                                                | **弃用**. 非常慢的旧式AS路径匹配。在从旧的ROS v6配置迁移时，此参数应仅用作临时匹配器。[阅读更多](https://help.mikrotik.com/docs/display/ROS/Route+Selection+and+Filters#RouteSelectionandFilters-AS-PATHRegexpMatching)                                                                         |
| chain                            | chain_name                                                                   |                                                                                                                                                                                                                                                                                                 |
| ospf-type                        | ext1 \| ext2 \| inter \| intra \| nssa1 \| nssa2                             | OSPF路由类型:<br>- ext1 - external (Type 5 LSA) with type1 metric<br>- ext2 - external (Type 5 LSA) with type2 metric<br>- inter - inter-area-route (Type 3 LSA)<br>- intra - intra-area-route (Type 4 LSA)<br>- nssa1 - Type 7 LSA with type1 metric<br>- nssa2 - Type 7 LSA with type1 metric |
| protocol                         | bgp \| connected \| dhcp \| fantasy \| modem \| ospf \| rip \| static \| vpn | 引入路由的协议类型。                                                                                                                                                                                                                                                                            |
| rpki                             | invalid \| unknown \| valid \| unverified                                    | 前缀的RPKI验证状态                                                                                                                                                                                                                                                                              |
| rtab                             | routing_table_name                                                           | 引入路由的路由表名                                                                                                                                                                                                                                                                              |
| vrf                              | vrf_name                                                                     | 引入路由的vrf名称                                                                                                                                                                                                                                                                               |

### 可写属性

| 属性                      | 类型                                                    | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ** _数值属性_**           |
| distance                  |                                                         | 路线距离                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| scope                     |                                                         |                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| scope-target              |                                                         | 目标作用域                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| BGP - WEIGHT              |                                                         | BGP WEIGHT属性                                                                                                                                                                                                                                                                                                                                                                                                                             |
| BGP - MED                 |                                                         | BGP MED属性是路由器的本地属性。它也用于iBGP对等体的输出。                                                                                                                                                                                                                                                                                                                                                                                  |
| BGP -out- MED             |                                                         | 发送到远端对等体的BGP MED属性。在eBGP对等体的输出链中使用。                                                                                                                                                                                                                                                                                                                                                                                |
| BGP -local-pref           |                                                         | BGP LOCALPREF属性                                                                                                                                                                                                                                                                                                                                                                                                                          |
| BGP - IGP - METRIC        |                                                         | BGP IGP METRIC                                                                                                                                                                                                                                                                                                                                                                                                                             |
| bgp-path-peer-prepend     |                                                         | 预写上次接收到的远端对等体ASN。如果前缀来自路由器，则该参数不会对路由器的输出产生任何影响，因为ASN还不存在。<br>如果在BGP输入中使用matcher，则可以过滤超过一定前缀数的前缀。例如，如果一个远端对等体提前了5次ASN，但我们希望允许最多提前4次ASN，那么我们可以使用:" if (bgp-path-peer-prepend > 4) {reject}  "<br>该参数还可以覆盖从远端接收到的任何前缀，例如，如果远端对等体在BGP输入中设置“ BGP -path-peer-prepend  1”，则可以删除该前缀 |
| BGP -path- preend         |                                                         | preend路由器的ASN，在BGP输出中使用。                                                                                                                                                                                                                                                                                                                                                                                                       |
| OSPF -ext-metric          |                                                         | OSPF外部路由度量                                                                                                                                                                                                                                                                                                                                                                                                                           |
| OSPF -ext-tag             |                                                         | OSPF外部路由标记                                                                                                                                                                                                                                                                                                                                                                                                                           |
| RIP -ext-metric           |                                                         | RIP外部路由度量                                                                                                                                                                                                                                                                                                                                                                                                                            |
| RIP -ext-tag              |                                                         | RIP外部路由标签                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **标志属性**              |
| OSPF -ext- DN             |                                                         | 外部OSPF路由DN位                                                                                                                                                                                                                                                                                                                                                                                                                           |
| blackhole                 |                                                         |                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| suppress-hw-offload       |                                                         | 是否 [抑制L3 HW卸载](https://help.mikrotik.com/docs/display/ROS/L3+Hardware+Offloading#L3HardwareOffloading-SuppressingHWOffload)                                                                                                                                                                                                                                                                                                          |
| use-te-nexthop            |                                                         |                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **其他属性**              |
| gw                        | ipv4/6 address                                          | IPv4/IPv6地址或接口名称。在BGP输出的情况下，可以在以下情况下调整网关:<br>-是BGP反射器<br>- nexthop-choice设置为传播<br>-不是eBGP，也没有设置nexthop-choice=force-self。                                                                                                                                                                                                                                                                    |
| gw-interface              | interface_name                                          | Interface part of the gateway. Should be used if it is required to attach a specific interface for next-hop, like (1.2.3.4%ether1)                                                                                                                                                                                                                                                                                                         |
| gw-check                  | _none\|arp\|icmp\|bfd\|bfd-mh_                          |                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| pref-src                  | ipv4/6 address                                          |                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| bgp-origin                | _igp\|egp\|incomplete_                                  |                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ospf-ext-fwd              | ipv4/6 address                                          |                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ospf-ext-type             | _type1\|type2_                                          |                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| comment                   | string                                                  |                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| bgp-communities           | inline_community_set\| community_list_name              | BGP团体属性在RFC 1997中定义。每个团体的大小为32位。                                                                                                                                                                                                                                                                                                                                                                                        |
| BGP -ext- Communities     | inline_ext_community_set \| ext_community_list_name     | BGP扩展社区属性在RFC 4360中定义。RouterOS解析site-of-origin(前缀为soo:)和route-target(前缀为rt:)扩展团体。例如:set bgp-ext-communities rt:1111:2.3.4.5;可以设置/匹配64位十六进制的RAW扩展团体值，例如:“set bgp-ext-community 0x.........;”                                                                                                                                                                                                 |
| BGP - Large - Communities | inline_large_community_set \| large_community_list_name | BGP大团体属性在RFC 8092中定义。适用于包括32位asn在内的所有asn。每个community长度为12字节，由“global_admin:locap_part_1:local_part_2”3部分组成。                                                                                                                                                                                                                                                                                            |

### 命令

| 命令         | 参数                          | 说明                                                                                                                                                                                                                                          |
| ------------ | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| accept       |                               | 接受匹配的前缀                                                                                                                                                                                                                                |
| reject       |                               | reject匹配的前缀，前缀将以“过滤”的形式存储在内存中，而不是被选为最佳路径的候选。                                                                                                                                                              |
| return       | 返回到父链                    |
| jump         | _jump chain_name_             | 跳转到指定链                                                                                                                                                                                                                                  |
| unset        | _unset prop_name_             | 用于取消设置以下属性的值:<br>pref-src \| bgp-med \| bgp-out-med \| bgp-local-pref                                                                                                                                                             |
| append       |                               | append位于列表或字符串的末尾。可以添加以下属性值:bgp-communities、bgp-ext-communities、bgp-large-communities、comment                                                                                                                         |
| filter       |                               | 删除动作的逆操作(删除除指定值以外的所有内容)。可以过滤的属性有:bgp-communities、bgp-ext-communities、bgp-large-communities                                                                                                                    |
| delete       |                               | 删除指定属性的值。可以删除的属性有:bgp-communities、bgp-ext-communities、bgp-large-communities                                                                                                                                                |
| set          | _set prop_writeable value_    | 设置一个新的可写属性值。值可以从匹配类型的其他可读属性设置。对于数字属性，可以在值前加上+/-，这将使当前属性值增加或减少给定的量。例如，“set pref-src +1”将当前pref-src增加1，或者从其他可读的num属性中提取值，“set distance +ospf-ext-metric” |
| RPKI -verify | _rpki-verify rpki_group_name_ | 启用当前链中来自指定RPKI组的RPKI验证。                                                                                                                                                                                                        |

### 操作符

#### 匹配器操作符

| 操作符 | 说明         | 例子                                                     |
| ------ | ------------ | -------------------------------------------------------- |
| &&     | 逻辑与操作符 | if (dst in 192.168.0.0/16 && dst-len in 16-32) {reject;} |
|        |              |                                                          | 逻辑或操作符 |  |
| not    | 逻辑非操作符 | if ( not bgp-network) {reject; }                         |

#### Num Prop操作符

| 操作符 | 说明                                                                                  |
| ------ | ------------------------------------------------------------------------------------- |
| in     | 如果值在提供的数值范围内，则返回true。数值范围可以写成以下格式:{int..int}， {int-int} |
| ==     | 如果数值相等，则返回true                                                              |
| =      | 如果数值不等于                                                                        | 则返回true |
| >      | 如果左边的数值大于右边的数值                                                          | 则返回true |
| <      | 如果左侧数值小于右侧数值，则返回true                                                  |
| >=     | 如果左值大于或等于右值                                                                | 则返回true |
| <=     | 如果左边的数值小于或等于右边的数值                                                    | 则返回true |

#### 前缀操作符

| 操作符 | 说明                                                                                                                           |
| ------ | ------------------------------------------------------------------------------------------------------------------------------ |
| in     | 如果前缀是所提供网络的子网，则返回true。如果使用操作符来匹配地址列表中的前缀(例如"dst in list_name")，则它将只匹配精确的前缀。 |
| !=     | 如果前缀不等于提供的值                                                                                                         | 则返回true |
| ==     | 如果前缀等于提供的值                                                                                                           | 则返回true |

#### BGP团体操作符

| 操作符        | 说明                                                               | 例子 |
| ------------- | ------------------------------------------------------------------ | ---- |
| equal         | 如果提供的社群等于routes属性值                                     |      | 则返回true   |  |
| equal-list    | 如果提供的社区列表中的社区等于路由的属性值                         |      | 则返回true   |  |
| any           | 如果路由的属性值至少包含一个所提供的共同体                         |      | ，则返回true |  |
| any-list      | 如果路由的属性值包含了所提供列表中的至少一个社区，则返回true       |      |
| includes      | 如果路由的属性值包含指定的社区                                     |      | 则返回true   |  |
| includes-list | 如果路由的属性值包含指定的communities-list中的所有团体，则返回true |      |
| subset        |                                                                    |      |
| subset-list   |                                                                    |      |
| any-regexp    |                                                                    |      |
| subset-regexp |                                                                    |      |

#### 字符串操作符

| 操作符 | 说明                                     |
| ------ | ---------------------------------------- |
| find   | 检查所提供的子字符串是否为属性值的一部分 |
| regexp | 匹配属性值的字符串regexp                 |

删除BGP团体

路由过滤器允许使用delete命令清除BGP团体。Delete命令根据团体类型接受几个参数:

- **团体**:
- “wk”-将匹配和删除知名社区
- “other”-将匹配和删除其他不知名的社区
- "regexp" -匹配需要删除的团体的regexp模式
- "\<community-list name\>" -删除指定community-list中的团体
- **ext-communities**:
- "rt" -将匹配并删除 **RouteTarget**
- “soo”-将匹配并删除 **原产地**
- “other”-将匹配并删除其他非RT或SSO的ext社区
- "regexp" -匹配需要删除的ext团体的regexp模式
- "\<community-ext-list name\>" -删除指定community-ext-list中的团体
- **大团体**:
- “all”-删除所有内容
- "regexp" -匹配需要删除的大型团体的regexp模式
- "\<community-large-list name\>" -删除指定community-large-list中的大团体

可以指定多个团体类型，例如从community-ext列表中删除所有sso，其他类型的ext团体和特定的RTs:

```shell
/routing/filter/community-ext-list
add list=myRTList communities="rt:1.1.1.1:222"
/routing/filter/rule/add
chain=myChain rule="delete bgp-ext-communities sso,other,myRTList;"
```

AS-PATH正则表达式匹配

AS路径是自治系统编号(autonomous system number, asn)的序列，例如AS路径123 456789表示路由来自编号为789的自治系统，为了到达目的地，数据包需要经过两个自治系统:456和789。要应用特定的路由策略，管理员可能希望匹配AS路径中的特定AS号或一组数字(例如，拒绝经过AS 456的前缀)，这可以使用正则表达式(regexp)实现。

有两种常见的方法来操作AS路径数据:

-将整个AS路径转换为字符串，并让regexp对字符串进行操作(ROS v6或Cisco风格)
-让regexp操作AS路径中的每个条目作为一个数字(ROS v7, Juniper风格)

基本上，第一种方法是对每个字符执行匹配，第二种方法是对每个AS号执行匹配。正如您所想象的那样，后一种方法比字符串匹配方法更快，资源消耗更少。

这种更改将要求管理员实现新的Regex策略。RouterOS v6中的旧Regex模式不能直接复制/粘贴，因为它们会导致语法错误或意想不到的结果。

以一个基本的AS路径过滤规则为例。

```shell
/routing/filter/rule/add
chain=myChain rule="if (bgp-as-path .1234.) {accept}"
```

在ROS v7中，此Regex模式将匹配AS路径中间的任何地方的ASN 1234，在ROS v6中，相同的模式将匹配包含ASN至少由6个字符组成并包含字符串“1234”的任何AS路径。显然，如果直接将Regex模式从一个实现复制粘贴到另一个实现，将会导致意想不到的危险结果。在ROS v6中，一个等效的模式看起来像这样:"._1234_."。

从ROS v6中再举一个例子，假设有一个模式“1234[5-9]”，它所做的是匹配字符串中的任何位置的12345到12349，这意味着有效的匹配是as路径“12345 3434”，“11 9123467 22”等等。如果在ROS v7中输入相同的模式，它将匹配包含精确ASN 1234的AS路径，然后是ASN范围从5到9(匹配的AS路径将是“1234 7 111”，“111 12345 222”等，它将不匹配“12345 3434”)。

不要直接从ROS v6或Cisco配置中复制Regex模式，它们不是直接兼容的。在某些情况下，可能导致意外甚至危险的配置。

### 正则表达式测试工具

现在，RouterOS内置了正则表达式检查工具，简化了管理员的工作。该工具还支持num-list，因此可以在将精确正则表达式应用于路由过滤器之前针对任何as-path进行测试。

```shell
/routing/filter/num-list add list=test range=100-1500
 
/routing/filter/test-as-path-regexp regexp="[[:test:]]5678\$" as-path="1234,5678"
```

### 支持的操作符

| 操作符   | 说明                                                                                                                                                                                                                                                                    | 示例               | 示例解释                                                           | 示例匹配                                                                         |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| ^        | 表示路径的开始                                                                                                                                                                                                                                                          | ^1234              | 将以ASN 1234                                                       |                                                                                  | 开始的as路径                                                  |
| $        | 表示路径的结尾                                                                                                                                                                                                                                                          | 1234$              | 将匹配原始ASN 1234                                                 |                                                                                  |
| *        | 列出的ASN                                                                                                                                                                                                                                                               | ^1234*$            | 出现零次或多次将计算为空路径或ASN 1234可能出现或不出现多次的路径   | **Math:**<br>1234<br>1234 1234 1234<br>Null path<br>**No Match:**<br>1234 5678   |
| +        | 列出的ASN出现一次或多次                                                                                                                                                                                                                                                 | 1234+              | 是否匹配ASN 1234至少出现一次的as路径                               | **Match:**<br>1234<br>3 1234 6<br>**No match:**<br>12345 678                     |
| ?        | 列出的ASN零次或一次出现                                                                                                                                                                                                                                                 | ^1234? 5678        | 匹配的as路径可能以ASN 1234开头，也可能不以出现一次的ASN 1234开头。 | **Match**:<br>5678<br>1234 5678<br>**No match:**<br>1234 1234 5678<br>12345 5678 |
| .        | 任何ASN出现一次。                                                                                                                                                                                                                                                       | ^. $               | 将匹配任何长度为1的as路径。                                        | **Match:**<br>12345<br>45678<br>**No match:**<br>1234 5678                       |
| \|       | 每侧匹配两个ASN中的一个                                                                                                                                                                                                                                                 | ^(1234\|5678)      | 将匹配以ASN 1234或5678 开头的as路径                                | **Match**:<br>1234<br>5678<br>1234 5678<br>**No Match:**<br>91011                |
| [ ] [^ ] | 表示必须匹配列表中一个AS号的AS号集合。<br>在开始括号后使用^来对集合求反。<br>也可以使用 [[:numset_name:]] 从 [num-list](https://help.mikrotik.com/docs/display/ROS/Route+Selection+and+Filters#RouteSelectionandFilters-/routing/filter/num-list) 引用预定义的num-lists | ^[1234 5678 1-100] | 是否会匹配以1234或5678开头或从1到100的as路径                       | **Match:**<br>1234<br>99<br>5678<br>**No Match:**<br>101                         |
| ()       | 匹配的regexp项组                                                                                                                                                                                                                                                        | ^(1234$            | 5678)                                                              | 将匹配以1234开头和结尾的as路径或以5678开头的as路径                               | **Match:**<br>1234<br>5678 9999<br>**No Match:**<br>1234 5678 |

不支持重复范围{}。

## 团体和Num列表

常用号码列表可以通过' /routing/filter/num-list '菜单配置。这些数字列表可以在过滤器规则中使用，以简化过滤器设置过程。

以类似的方式，您还可以定义团体、扩展团体和大型团体列表。团体集可用于匹配、追加和设置。

例如，从列表中匹配团体并清除属性:

```shell
/routing/filter/community-list
add communities=111:222 list=myCommunityList
 
/routing/filter/rule/add
chain=myChain rule="if (bgp-communities equal-list myCommunityList) {delete bgp-communities wk,other; accept;}"
```

`/routing/filter/community-list`

| 属性                                               | 说明                                                                                                                                                                                                                                                                                                                                                                                          |
| -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **comment** (_string_; Default: )                  |                                                                                                                                                                                                                                                                                                                                                                                               |
| **communities** (_list of communities_; Default: ) | 以 **已知** 名称或如下格式表示的团体列表:**as****:number**，其中每个部分可以是整数[0..65535]。<br>已知的名字:<br>accept-own     graceful-shutdown  no-advertise         no-llgr         route-filter-6  <br>accept-own-nh  internet           no-export            no-peer         route-filter-xlate-4  <br>blackhole      llgr-stale         local-as  route-filter-4  route-filter-xlate-6 |
| **disabled** (yes _\| no_)                         |                                                                                                                                                                                                                                                                                                                                                                                               |
| **name** (_integer [string_; Default: )            | 参考名                                                                                                                                                                                                                                                                                                                                                                                        |
| **regexp** (string)                                | Regexp匹配器来匹配团体。只有regexp参数设置的团体不能用于附加团体。                                                                                                                                                                                                                                                                                                                            |

`/routing/filter/community-ext-list`


| 属性                                                   | 说明                                                                                                                                                                            |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **comment** (_string_; Default: )                      |                                                                                                                                                                                 |
| **communities** (_list of ext communities_; Default: ) | 扩展团体列表表示为 **raw** 整数值或键入格式: **type:value**，其中type可以为:<br>- **rt** - route-target<br>- **soo** -产地<br>值取决于类型，有关RT和SoO值的更多信息请询问谷歌。 |
| **disabled** (yes _\| no_)                             |                                                                                                                                                                                 |
| **name** (_integer [string_; Default: )                | 参考名                                                                                                                                                                          |
| **regexp** (string)                                    | Regexp匹配器来匹配团体。只有regexp参数设置的团体不能用于附加团体。                                                                                                              |

`/routing/filter/community-large-list`


| 属性                                                     | 说明                                                                           |
| -------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **comment** (_string_; Default: )                        |                                                                                |
| **communities** (_list of large communities_; Default: ) | 大型团体列表，格式为: **admin:value1:value2**，每段取值为整数[0..4294967295]。 |
| **disabled** (yes _\| no_)                               |                                                                                |
| **name** (_integer [string_; Default: )                  | 参考名                                                                         |
| **regexp** (string)                                      | Regexp匹配器来匹配团体。只有regexp参数设置的团体不能用于附加团体。             |

# 路由选择

路由选择规则允许控制如何从可用的候选路由中选择输出路由。默认情况下(如果没有设置选择规则)，输出总是选择最佳路由。

例如，看下面的路由表，可以看到有2个候选路由和一个最佳路由。缺省情况下，BGP在选择发送路由时选择活动路由。

```shell
[admin@4] /routing/route> print where dst-address=1.0.0.0/24
Flags: A - ACTIVE; b, y - COPY
Columns: DST-ADDRESS, GATEWAY, AFI, DISTANCE, SCOPE, TARGET-SCOPE, IMMEDIATE-GW
   DST-ADDRESS  GATEWAY         AFI  DISTANCE  SCOPE  TARGET-SCOPE  IMMEDIATE-GW        
 b 1.0.0.0/24   10.155.101.217  ip4        19     40            30  10.155.109.254%ether1
Ab 1.0.0.0/24   10.155.101.232  ip4        20     40            30  10.155.109.254%ether1
 b 1.0.0.0/24   10.155.101.231  ip4        20     40            30  10.155.109.254%ether1
```

但在某些情况下，你可能想要优先选择其他路线，而不是活动路线，这里有一个选择规则。

RouterOS中的选择规则是通过“/routing/filter/select-rule”菜单配置的。

选择规则还可以调用路由过滤器，其中根据过滤规则选择路由。例如，为了模拟默认的输出选择，可以设置以下规则集:

```shell
/routing filter rule
add chain=get_active rule="if (active) {accept}"
 
/routing filter select-rule
add chain=my_select_chain do-where=get_active
```

# 属性引用

`/routing/filter/chain`

BGP/OSPF配置中可引用的过滤规则链动态列表。

**只读属性:**


| 属性                        | 说明 |
| --------------------------- | ---- |
| **dynamic** (_yes   \| no_) |      |
| **inactive** (yes _ \| no_) |      |
| **name** (_string_)         |      |

`/routing/filter/select-chain`

BGP/OSPF配置中可以引用的过滤选择链动态列表。

**只读属性:**


| 属性                        | 说明 |
| --------------------------- | ---- |
| **dynamic** (_yes   \| no_) |      |
| **inactive** (yes _ \| no_) |      |
| **name** (_string_)         |      |
