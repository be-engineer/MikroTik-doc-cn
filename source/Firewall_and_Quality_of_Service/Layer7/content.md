# 概述

Layer7 协议是一种在 ICMP/TCP/UDP 流中搜索模式的方法。

L7 匹配器非常耗费资源。 仅对非常特定的流量使用此功能。 不建议 L7 匹配器用于一般流量，例如阻止网页。 这几乎永远不会正常工作，设备将耗尽其资源来捕获所有流量。 用其他功能通过 URL去 阻止网页。

L7 匹配器收集连接的前 **10 个数据包** 或连接的前 **2KB** 并在收集的数据中搜索模式。 如果在收集的数据中未找到该模式，匹配器会停止进一步检查。 分配的内存被释放，协议被认为是 **未知**。 要考虑到大量连接会增加内存和 CPU 使用率。 为避免这种情况，请添加常规防火墙匹配器以减少重复发给第 7 层过滤器的数据量。

另一个要求是 layer7 匹配器必须看到两个方向的流量（传入和传出）。 为了满足这个要求，应该在 **forward** 链中设置 l7 规则。 如果在 **input/prerouting** 链中设置了规则，则 **必须** 在 **output/postrouting** 链中设置相同的规则，否则，收集的数据可能不完整，导致 错误匹配的模式。

  第 7 层匹配器不区分大小写！

可以在 [l7-filter 项目页面](http://l7-filter.sourceforge.net/protocols) 上找到与 RouterOS 兼容的示例 L7 模式。

  在某些情况下无法执行第 7 层正则表达式时，RouterOS 会记录_topic=firewall, warning_ 并在消息中说明问题的错误信息！
## 属性

`/ip firewall layer7-protocol`

| 属性                              | 说明                                                                                                          |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **name**（_string_；Default：）   | 防火墙规则中配置使用的 l7 模式的描述名称。 请参阅示例 [>>](https://wiki.mikrotik.com/wiki/L7#Examples "L7")。 |
| **regexp**（_string_；Default：） | POSIX 兼容的正则表达式作为匹配模式。                                                                          |

## 例子

### 简单的 L7示例

首先，将 Regexp 字符串添加到协议菜单，定义要查找的字符串。 在这个例子中，用一个模式来匹配 RDP 数据包。

`/ip firewall layer7-protocol`
`add name =rdp regexp = "rdpdr.*cliprdr.*rdpsnd"`

然后使用防火墙中定义的协议。

```shell
/ip firewall filter

add action =accept chain =forward comment = "" disabled =no port =80 protocol =tcp
add action =accept chain =forward comment = "" disabled =no port =443 protocol =tcp
addaction =accept chain =forward comment = "" disabled =no layer7-protocol =\
    rdp protocol =tcp
```

正如在 l7 规则之前看到的那样，添加了几个常规规则来匹配已知流量，从而减少内存使用。

### 输入链中的L7

在这个例子中，尝试匹配连接到路由器的 telnet 协议。

`/ip firewall layer7-protocol add comment = "" name =telnet regexp = "^\\xff[\\xfb-\\xfe].\\xff[\\xfb-\\xfe].\\xff[\\xfb-\\xfe]"`

请注意，需要两个方向，这就是为什么还需要输出链中的 l7 规则来查看传出数据包。

```shell
/ip firewall filter
add action =accept chain =input comment = "" disabled =no layer7-protocol =telnet \
    protocol =tcp
add action =passthrough chain =output comment = "" disabled =no layer7-protocol =telnet \
    protocol =tcp
```

### Youtube 匹配器

当用户登录时，youtube 使用 HTTPS，意味着 L7 无法匹配此流量。 只能匹配未加密的 HTTP。

`/ip firewall layer7-protocol`
`add name =youtube regexp = "(GET \\/videoplayback\\\?|GET \\/crossdomain\\.xml)"`
