# SYN Dos和DDoS保护介绍

拒绝服务（DoS）或分布式拒绝服务（DDoS）攻击是一种恶意尝试，通过用大量的互联网流量淹没目标或周围的基础设施来破坏目标服务器、服务或网络的正常通信。有几种类型的DDoS攻击，例如，HTTP泛滥、SYN泛滥、DNS放大等。

![](https://help.mikrotik.com/docs/download/attachments/28606504/Untitled%20Diagram%20%281%29.jpg?version=1&modificationDate=1590666013808&api=v2)

## 对DDoS的保护

## 配置行

```shell
/ip firewall address-list
add list=ddos-attackers
add list=ddos-targets
/ip firewall filter
add action=return chain=detect-ddos dst-limit=32,32,src-and-dst-addresses/10s
add action=add-dst-to-address-list address-list=ddos-targets address-list-timeout=10m chain=detect-ddos
add action=add-src-to-address-list address-list=ddos-attackers address-list-timeout=10m chain=detect-ddos
/ip firewall raw
add action=drop chain=prerouting dst-address-list=ddos-targets src-address-list=ddos-attackers
```

## 配置解释

首先把每个新连接发送到检测DDoS的特定防火墙链。

`/ip/firewall/filter/ add chain =forward connection-state =new action =jump jump-target =detect-ddos`

在新创建的链中，添加以下带有 "dst-limit"参数的规则。参数的书写格式如下。**dst-limit=** **count[/time],burst,mode[/expire]** . 根据目的地和源地址流来匹配32个数据包，每10秒更新一次，有32个数据包突发。这个规则会一直工作到超过给定速率。

`/ip/firewall/filter/ add chain =detect-ddos dst-limit =32,32,src-and-dst-addresses/10s action =return`。

到目前为止，所有的合法流量都通过 "action=return"，但在DoS/DDoS的情况下，"dst-limit "缓冲区将被填满，规则就不会 "捕获 "任何新的流量。下面是下一个规则，用来处理攻击问题。从创建一个攻击者和受害者的列表开始到丢弃这个列表。

`ip /firewall/address-list/ add list =ddos-attackers`

`ip /firewall/address-list/ add list =ddos-targets`

`ip /firewall/raw/ add chain =prerouting action =drop src-address-list =ddos-attackers dst-address-list =ddos-targets`

通过防火墙过滤器，在 "DDoS-攻击者"列表中添加攻击者，在 "ddos-目标"列表中添加受害者:

`/ip/firewall/filter/`

`add action =add-dst-to-address-list address-list =ddos-targets address-list-timeout =10m chain =detect-ddos`

`add action =add-src-to-address-list address-list =ddos-attackers address-list-timeout =10m chain =detect-ddos`

## SYN攻击

## SYN泛滥

SYN泛滥是DoS攻击的一种形式，攻击者向目标系统发送连续的SYN请求，试图消耗足够的服务器资源，使系统对合法流量没有反应。幸运的是，在RouterOS中，有专门针对这种攻击的功能。

`/ip/settings/ set tcp-syncookies =yes`。

该功能的工作原理是发送包含一个小的加密哈希值的ACK包，响应的客户端会将其作为SYN-ACK包的一部分回传。如果内核在回复包中没有看到这个 "cookie"，它会认为这个连接是假的，并丢弃。

## SYN-ACK泛滥

SYN-ACK泛滥是一种攻击方法，包括以高速向目标服务器发送欺骗性的SYN-ACK数据包。服务器需要大量的资源不按顺序地处理这些数据包（不按照正常的SYN、SYN-ACK、ACK的TCP三方握手机制），可能会忙于处理攻击流量，以至于无法处理合法流量，因此攻击者达到了DoS/DDoS状态。在RouterOS中，可以从前面提到的例子中配置类似的规则，但更具体的是针对SYN-ACK泛滥：

`/ip/firewall/filter add action =return chain =detect-ddos dst-limit =32,32,src-and-dst-addresses/10s protocol =tcp tcp-flags =syn,ack`
