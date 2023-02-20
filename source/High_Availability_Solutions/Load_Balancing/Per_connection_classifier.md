# 每连接的分类器

PCC匹配器允许把流量分成相等的数据流，并能把有特定选项集的数据包保留在一个特定的数据流中（可以从src-address, src-port, dst-address, dst-port中指定这组选项）。

## 原理

PCC从IP头中提取选定字段，并在散列算法的帮助下把选定的字段转换成32位数值。然后用这个值除以指定的 _分母_，再将余下的值与指定的 _余数_ 进行比较，如果相等，则数据包将被捕获。可以从报头中选择src-address、dst-address、src-port、dst-port来操作。

```shell
per-connection-classifier=
PerConnectionClassifier ::= [!]ValuesToHash:Denominator/Remainder
  Remainder ::= 0..4294967295    (integer number)
  Denominator ::= 1..4294967295    (integer number)
  ValuesToHash ::= both-addresses|both-ports|dst-address-and-port|
  src-address|src-port|both-addresses-and-ports|dst-address|dst-port|src-address-and-port
```

## 示例

这个配置根据源地址和端口把所有连接分成3组

```shell
/ip firewall mangle add chain=prerouting action=mark-connection \
 new-connection-mark=1st_conn per-connection-classifier=src-address-and-port:3/0
/ip firewall mangle add chain=prerouting action=mark-connection \
  new-connection-mark=2nd_conn per-connection-classifier=src-address-and-port:3/1
/ip firewall mangle add chain=prerouting action=mark-connection \
  new-connection-mark=3rd_conn per-connection-classifier=src-address-and-port:3/2
```

## PCC如何工作

本文用简单的语言解释PCC的工作原理。官方手册维基页面的定义是这样的："PCC从IP头中选取字段，并在散列算法的帮助下将所选字段转换成32位数值。这个值除以指定的分母，然后将余数与指定的余数进行比较，如果相等，数据包就会被捕获。可以从报头中选择src-address、dst-address、src-port、dst-port来操作。可用的字段总数为："both-addresses|both-port|dst-address and-port|src-address|src-port|both-addresses and-ports|dst-address|dst-port|src-address and-port"。如果理解了这个定义，这篇文章中就不会有什么有趣的内容了。

首先，这里是理解该定义所需的术语。

IP数据包有一个包含几个字段的头，其中两个字段是数据包源的IP地址和数据包目的地的IP地址。TCP和UDP数据包也有包含源端口和目的端口的头。

分母和余数是模数运算的一部分。模运算产生的是两个数字相除时剩下的整数，只接受结果中的整数部分。它用%符号表示。下面是一些例子。3 % 3 = 0，因为3可以完全除以3。4 % 3 = 1，因为4的下一个最小数字可以完全除以3，4 - 3 = 1。5 % 3是2，因为5的下一个最小数字可以完全除以3，5 - 3 = 2。

哈希值是输入并产生输出的函数。散列有许多有趣的特性，但对本文而言，唯一重要的是散列函数是确定性的。这意味着，当你给散列函数输入 "hello"，产生输出 "1 "时，如果第二次给它输入 "hello"，再次产生输出 "1"。给一个散列函数提供相同的输入时，将总是产生相同的输出。PCC使用什么确切的散列算法并不重要，在讨论中，假设给它输入IP地址和端口时，它只是将IP地址的八位数和端口加起来作为十进制数字，然后取最后一位数字作为输出。这里有一个例子：

哈希函数输入1.1.1.1作为源IP地址，10000作为源TCP端口，2.2.2.2作为目的IP地址，80作为目的TCP端口。输出将是1+1+1+1+10000+2+2+2+80=10092，其中最后一位数字是2，所以哈希输出是2，每次输入该IP地址和端口组合都会产生2。

需要注意的是，尽管PCC常用于电路上分散负载，但PCC本身与路由、路由标记或分散负载完全没有关系。PCC只是一种匹配数据包的方式，与随后标记这些匹配数据包的动作没有直接关系，即使这是它的主要目的。

这里有三条经常用于PCC的线路，并有其解释。

```shell
/ip firewall mangle add chain=prerouting action=mark-connection \
 new-connection-mark=1st_conn per-connection-classifier=src-address-and-port:3/0
/ip firewall mangle add chain=prerouting action=mark-connection \
  new-connection-mark=2nd_conn per-connection-classifier=src-address-and-port:3/1
/ip firewall mangle add chain=prerouting action=mark-connection \
  new-connection-mark=3rd_conn per-connection-classifier=src-address-and-port:3/2
```

以下是不同的字段选项对数据包匹配的意义，这些字段被送入散列算法（为了在链路间分散负载，决定数据包将放在什么链路上）。请记住，当散列函数有相同的输入时，它总是产生相同的输入。

- src-address。客户端的源地址总是相同的，来自某个特定客户的所有流量总是与同一个PCC匹配器相匹配，并且总是放在同一个链路上。
- dst-address。特定服务器的目标地址始终是相同的，所有到该服务器（例如Mikrotik Wiki）的流量始终匹配相同的PCC匹配器，并始终放在同一链路上。
- both-addresses。同一客户和服务器之间的源和目的IP对总是相同的，所以特定的客户和特定的服务器（例如笔记本电脑和Mikrotik Wiki）之间的所有流量总是匹配相同的PCC匹配器，并且总是放在同一个链接上。
- src-port。客户端的源端口通常是在创建连接时随机选择的，因此在许多连接中，不同的源端口将被送入哈希函数，不同的PCC匹配器将进行匹配，流量将通过不同的链接。然而，一些客户端协议总是选择相同的源端口，路由器后面的服务器大多可能使用相同的服务端口来发送流量回给他们的客户端。路由器后面的网络服务器将从HTTP（80）和HTTPS（443）端口发送大部分流量，这些流量始终匹配相同的PCC匹配器，并放在同一个链接上。
- dst-port。客户端的目的端口通常是定义好的服务端口，客户端和互联网上的服务器之间的所有HTTP（80）流量将始终匹配相同的PCC匹配器，并放在同一个链接上。同样的客户端进行HTTPS（443）流量可能匹配不同的PCC匹配器，并通过不同的链接。
- both-ports。因为通常客户端口是随机选择的，两个端口的组合通常是随机的，并且会在各条链路上分散负载。
- src-address-and-port。与src-port的注意事项相同。
- dst-address-and-port。与dst-port的注意事项相同。
- Both-addresses-and-port。在链路间传播流量的最随机的方式，因为它有最多的变量。

值得注意的是，尽管本文讨论的哈希函数大大简化了，并不是现实生活中使用的，但它很好地展示了哈希函数的另一个特性：两个完全不同的输入可以产生相同的输出。在例子中，3 % 3 = 0，6 % 3 = 0；当输入3时，得到的是0，当输入6时，也是如此。IP地址是32位的，而端口是16位的，所以假设同时使用地址和端口，会给它提供32+32+16+16=96位的输入，而只会收到32位的反馈，所以对不同的输入必须产生相同的输出。这意味着两个完全不相关的连接可以匹配同一个PCC匹配器，并放在同一条线上。把越多的连接放在上面，PCC的效果就越好，这样哈希函数就有更多机会产生不同的输出。
