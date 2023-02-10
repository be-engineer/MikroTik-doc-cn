# 队列大小例子

创建这个例子是为了强调队列大小对由特定队列排队的流量的影响。

在Mikrotik RouterOS中，队列大小可以在"/queue type "菜单中指定。每种队列类型都有不同的选项来指定队列大小（pfifo-limit、bfifo-limit、pcq-limit、pcq-total-limit、red-limit），所有的原则都是一样的-队列大小是决定是否应该丢弃包或安排在以后的时间的主要选项。

在实时环境中，这个过程是连续发生的，没有任何停顿、步骤或中断，为了作为一个例子来展示，我们把它分成几个步骤，在这些步骤中，有可能确切地知道每一步将有多少数据包被接收/传送出去。

我们不会讨论TCP和掉包重传的具体细节-只将这些数据包视为简单的UDP流。

![](https://help.mikrotik.com/docs/download/attachments/137986083/700px-Queue_size_No_Limit.jpg?version=1&modificationDate=1658487303008&api=v2)

正如上图中看到的，有 **25 个步骤**，在此时间范围内总共有 **1610 个传入数据包**。

## 100% 整形

当超过限制的每个数据包都将丢弃时，队列是 100% 整形。 这样所有没有丢弃的包都会立即送出。

在示例中应用 **max-limit=100 包每步** 限制：

![](https://help.mikrotik.com/docs/download/attachments/137986083/700px-Queue_size_0_packets.jpg?version=1&modificationDate=1658487594673&api=v2)
  
由于这种限制，1610 个数据包中只有 1250 个能够通过队列（**22.4% 数据包丢弃**），但所有数据包都没有延迟到达。

## 100% 调度

当没有丢失数据包时，队列是 100% 调度的，所有数据包都会排队并在第一时间发送。

在每一步中，队列必须先将前面步骤中排队的数据包发送出去，然后将这一步的数据包发送出去，这样才能保持正确的数据包顺序。

将再次使用相同的限制（**每步 100 个数据包**）。

![](https://help.mikrotik.com/docs/download/attachments/137986083/700px-Queue_size_Unlimited_Packets.jpg?version=1&modificationDate=1658487655761&api=v2)

没有丢包，但是 630 **(39,1%) 数据包有 1 步延迟**，另外 170 **(10,6%) 数据包有 2 步延迟**。 （delay = latency）

## 默认小队列类型

没有丢包，但是 630 **(39,1%) 数据包有 1 步延迟**，另外 170 **(10,6%) 数据包有 2 步延迟**。 （delay = latency）

## 默认小队列类型

当队列同时使用这两个方式（整形和调度）时，也可以选择中间方式。 默认情况下，RouterOS 中的大多数队列大小为 10。

![](https://help.mikrotik.com/docs/download/attachments/137986083/700px-Queue_size_10_packets.jpg?version=1&modificationDate=1658487745816&api=v2)
  
有 320 **(19,9%) 数据包被丢弃**，80 **(5,0%) 数据包有 1 步延迟**。

## 默认队列类型

RouterOS 中另一个常用的队列大小是 50。

![](https://help.mikrotik.com/docs/download/attachments/137986083/700px-Queue_size_50_packets.jpg?version=1&modificationDate=1658487824078&api=v2)

有 190 **(11.8%) 数据包被丢弃**，400 **(24.8%) 数据包有 1 步延迟**。
