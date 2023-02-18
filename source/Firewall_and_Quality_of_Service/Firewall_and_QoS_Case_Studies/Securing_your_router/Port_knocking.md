# Port knocking

所有可用的公共IP地址不断被机器人和shodan.io等服务进行端口扫描，任何人都可以利用这些信息进行暴力攻击和执行任何已知的漏洞。Port knocking是一种经济有效的防御方式，它不暴露任何端口，只是监听连接尝试-如果端口连接尝试的序列正确，客户端就被认为是安全的，并被添加到绕过WAN防火墙规则的安全地址列表中。

## 设置实例

假设已经设置了一个防火墙，可以丢弃来自WAN口的所有连接尝试，因此需要在这之前添加额外的规则。
首先创建一个防火墙规则，在一个给定的端口上进行监听，并将连接的源IP添加到地址列表中-这是第一次敲门。

`add action =add-src-to-address-list address-list =888 address-list-timeout =30s chain =input dst-port =888 in-interface-list =WAN protocol =tcp`

然后添加一个规则，在另一个端口做同样的事情，但只批准已经在第一个列表中的IP。可以重复这个步骤，次数不限。

`add action =add-src-to-address-list address-list =555 address-list-timeout =30s chain =input dst-port =555 in-interface-list =WAN protocol =tcp src-address-list =888`

最后一次敲击将添加到一个IP列表中，该列表是可信的，任何输入都被接受。

`add action =add-src-to-address-list address-list =secured address-list-timeout =30m chain =input dst-port =222 in-interface-list =WAN protocol =tcp src-address-list =555`
`add action =accept chain =input in-interface-list =WAN src-address-list =secured`

## 敲击以获得访问权

为了从广域网访问电路板，可以用一个端口敲击客户端，一个简单的单行bash和nmap就可以完成工作。

`for x in 888,555,222; do nmap -p $x -Pn xx.xx.xx.xx; done`

## 黑名单

除非使用大量的敲击，否则简单的端口扫描可能会意外地以正确的顺序触发正确的端口，所以建议添加一个黑名单。

在防火墙堆栈的最顶端为黑名单添加一个丢弃规则。

`add action =drop chain =input disabled =yes in-interface-list =WAN src-address-list =blacklist`

然后将可疑的IP添加到黑名单中。

不好的端口 - 是那些永远不被信任的用户使用的端口，有很高的超时惩罚。

`add action =add-src-to-address-list address-list =blacklist address-list-timeout =1000m chain =input disabled =yes dst-port =666 in-interface-list =WAN protocol =tcp`

这些端口大大降低了端口扫描的速度，以至于没有意义，但绝不会长时间锁定一个真正的用户。这包括除 "敲门"端口以外的每一个端口，关键是源IP不在安全列表中，因此这些端口在成功敲门后可以使用。

`add action =add-src-to-address-list address-list =blacklist address-list-timeout =1m chain =input disabled =yes dst-port =21,22,23,8291,10000-60000 in-interface-list =WAN protocol =tcp src-address-list =!secured`

## 为每一次敲门使用一个口令

可以更进一步在每次敲门时发送一个密码。

警告

第7层规则是非常耗费资源的。除非你知道自己在做什么，否则不要使用。

 点击打开代码块

然后创建一个可以在敲门规则上请求的layer7重码检查。

```shell
/ip firewall layer7-protocol add name=pass regexp="^passphrase/$"  
/ip firewall filter  
add action=add-src-to-address-list address-list=888 address-list-timeout=30s chain=input dst-port=888 in-interface-list=WAN protocol=udp layer7-protocol=pass
```
