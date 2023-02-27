# HTB介绍

HTB（Hierarchical Token Bucket）是一种分类排队方法，对于处理不同种类的流量很有帮助。 本文将集中讨论 **分层令牌桶** (HTB)的 "Token Bucket "部分-单队列内部的算法和配置实例。

## Token Bucket算法(图中红色部分)

Token Bucket算法是对一个桶的类比，在这个桶里，以字节为单位的特定速率被添加到令牌。桶本身有一个特定的容量。

如果桶满了，新到的令牌就会被丢弃。

**桶的容量=桶的大小\*最大限制**。

- **bucket size** (0..10, Default:0.1) - 队列选项在RouterOS v6.35中添加，在此之前，它被硬编码为一个 "0.1 "的值。

在允许任何数据包通过队列之前，队列桶会被检查，看它是否已经包含了足够的令牌。

如果是，适当数量的令牌被移除（"兑现"），数据包允许通过队列。

如果不是，数据包就停留在数据包等待队列的起点，直到有了适当数量的令牌。

在多级队列结构的情况下，在子队列中使用的令牌也被 "收取"到父队列中。换句话说，子队列从父队列中 "借用 "令牌。

## 数据包队列(图中蓝色部分)

数据包队列的大小、顺序、数据包如何添加到这个队列，以及数据包何时丢弃是由以下因素决定的：

- **queue-type** - [Queue](https://help.mikrotik.com/docs/display/ROS/Queues)
- **queue-size** - [Queue Size](http://wiki.mikrotik.com/wiki/Manual:Queue_Size)

## 令牌速率选择（图中黑色部分）

任何时候的最大令牌速率都等于这些数值中最高的活动项。

- **limit-at** (_NUMBER/NUMBER_)：保证上传/下载到目标的速率
- **max-limit** (_NUMBER/NUMBER_)：允许目标的最大上传/下载速率。
- **burst-limit** (_NUMBER/NUMBER_)：当 "burst "激活时，允许目标的最大上传/下载速率。

**burst-limit** 只有在 'burst' 处于允许状态时才有效-更多信息在这里。[Queue Burst](https://help.mikrotik.com/docs/display/ROS/Queue+Burst)

在 **limit-at** 为最高值的情况下，要发出额外的令牌来补偿所有未从父队列中借入的缺失令牌。

## 图示

![](https://help.mikrotik.com/docs/download/attachments/137986076/Bucket_size.png?version=1&modificationDate=1658839566852&api=v2)

## Bucket Size动作

一个简单的设置，所有来自一个IP地址的流量都被标记为数据包标记:

`/ip firewall mangle`

`add chain =forward action =mark-connection connection-mark =no-mark src-address =192.168.88.101 new-connection-mark =pc1_conn`

`add chain =forward action =mark-connection connection-mark =no-mark dst-address =192.168.88.101 new-connection-mark =pc1_conn`

`add chain =forward action =mark-packet connection-mark =pc1_conn new-packet-mark =pc1_traffic`

### 默认队列桶

`/queue tree`

`add name =download parent =Local packet-mark =PC1-traffic max-limit =10M`

`add name =upload parent =Public packet-mark =PC1-traffic max-limit =10M`

在此，bucket-size=0.1，所以bucket-capacity= 0.1 x 10M = 1M

如果bucket满了（也就是客户端在一段时间内没有使用队列的全部容量），接下来的1Mb流量可以不受限制的速度通过队列。

### 大队列桶

`/queue tree`

`add name =download parent =Local packet-mark =PC1-traffic max-limit =10M bucket-size =10`

`add name =upload parent =Public packet-mark =PC1-traffic max-limit =10M bucket-size =10`

尝试把同样的逻辑用于桶为最大值时的情况。

这里，bucket-size=10，所以bucket-capacity= 10 x 10M = 100M

如果桶已经满了（也就是客户端在一段时间内没有使用队列的全部容量），则接下来的100Mb流量可以不受限制地通过队列。

所以有：

- 20Mbps的传输速度为10s
- 60Mbps的传输突发时间为2s
- 1Gbps传输突发速率约100ms

可以看到，该桶允许通过队列的流量有一种 "突发性"。该行为类似正常的突发功能，但缺少突发上限。如果我们在队列结构中利用桶的大小，就可以避免这种挫折。

### 大的子队列桶，小的父队列桶

`/queue tree`

`add name =download_parent parent =Local max-limit =20M`

`add name =download parent =download_parent packet-mark =PC1-traffic max-limit =10M bucket-size =10`

`add name =upload_parent parent =Public max-limit =20M`

`add name =upload parent =upload_parent packet-mark =PC1-traffic max-limit =10M bucket-size =10`

在此：

- parent queue bucket-size=0.1, bucket-capacity= 0.1 x 20M = 2M
- child queue bucket-size=10, bucket-capacity= 10 x 10M = 100M

父队列比子队列更快地耗尽令牌，由于子队列总是从父队列中借用令牌，整个系统被限制在父队列的令牌速率上-因此，最大限制=20M。这一速率将持续到子队列用完令牌，并被限制在10Mbps的令牌速率。

通过这种方式，可以在20Mbps的速度下进行突发，时间长达10秒。

## 配置

必须遵循三个基本步骤来创建HTB：

- **匹配和标记流量** - 对流量进行分类，以便进一步使用。由一个或多个匹配参数组成，为特定类别选择数据包。
- **创建规则（策略）来标记流量** - 将特定的流量类别放入特定的队列，并定义对每个类别采取的行动。
- 为特定接口附加策略** - 为所有接口（全局输入、全局输出或全局总数）、特定接口或特定父队列附加策略。

HTB允许创建一个分层的队列结构，并确定队列之间的关系，如 "父-子 "或 "子-子"。

只要队列至少有一个孩子，它就成为一个 **内部** 队列，所有没有孩子的队列是 **叶子** 队列。**叶子** 队列进行实际的流量消耗，**内部** 队列只负责流量分配。所有的 **叶子** 队列都被平等对待。

在RouterOS中，有必要指定 **父母** 选项，把一个队列作为另一个队列的子队列。

## 双重限制

HTB中的每个队列有两个速率限制。

- **CIR** (Committed Information Rate) - (RouterOS中的 **limit-at** )最坏情况，无论如何都会得到这个流量（假设真的可以发送这么多数据）。
- **MIR** (Maximal Information Rate) - (RouterOS中的 **max-limit**) 最好的情况是，如果队列的上级有多余的带宽，流量可以达到的速率。

换句话说，一开始所有队列的 **limit-at**（**CIR**）将得到满足，然后子队列才会尝试从父队列中借用必要的数据速率，以达到其**max-limit**（**MIR**）。

无论怎样，**CIR** 将被分配给相应的队列。(即使超过了父代的最大限制)

这就是为什么，为了确保双重限制功能的最佳（按照设计）使用，我们建议坚持这些规则。

- 所有子女的承诺速率之和必须小于或等于父母的可用流量。

CIR(parent)\* ≥ CIR(child1) +...+ CIR(childN)\*在父母是主要父母的情况下，CIR(parent)=MIR(parent)

- 任何子队列的最大速率必须小于或等于父母的最大速率

MIR (parent) ≥ MIR(child1) & MIR (parent) ≥ MIR(child2) & ... & MIR (parent) ≥ MIR(childN)

Winbox中的队列颜色：

- 0% - 50%可用流量 - 绿色
- 51% - 75%可用流量 - 黄色
- 76% - 100%可用流量 - 红色

### 优先权

无论如何，所有队列的 **limit-at**（**CIR**）都会被送出。

优先级负责将剩余的父队列流量分配给子队列，以便它们能够达到 **max-limit**。

优先级较高的队列将在优先级较低的队列之前达到其 **最大限度**。8是最低的优先级，而1是最高的。

请注意，优先级只起作用。

- 对于 **叶子** 队列-**内部** 队列的优先级没有意义。
- 如果指定了 **max-limit** （不是0）

## 示例

本节中将分析HTB的运行情况。为了做到这一点，将采用一个HTB结构，并试图涵盖所有可能的情况和功能，通过改变HTB必须回收的传入流量的数量改变一些选项。

### 结构

HTB结构由5个队列组成。

- **Queue01** 内部队列有两个子队列 - **Queue02** 和 **Queue03**。
- **Queue02** 内部队列有两个子队列 - **Queue04** 和 **Queue05**
- **Queue03** 叶子队列
- **Queue04** 叶子队列
- **Queue05** 叶子队列

**Queue03**、**Queue04、** 和 **Queue05** 是需要10Mbps的客户端，出站接口能够处理10Mbps的流量。

### Example 1: Usual case

![](https://help.mikrotik.com/docs/download/attachments/137986076/600px-HTB_Example1.jpg?version=1&modificationDate=1658484391069&api=v2)

- **Queue01** limit-at=0Mbps max-limit=10Mbps
- **Queue02** limit-at=4Mbps max-limit=10Mbps
- **Queue03** limit-at=6Mbps max-limit=10Mbps priority=1
- **Queue04** limit-at=2Mbps max-limit=10Mbps priority=3
- **Queue05** limit-at=2Mbps max-limit=10Mbps priority=5

### 例1的结果

- **Queen03** 将收到6Mbps
- **Queue04** 将收到2Mbps的数据
- **Queue05** 将收到2Mbps。
- **说明：** HTB的构建方式是，通过满足所有的 **limit-at**，主队列不再有吞吐量可以分配。

### 例2：通常情况下的最大限制

![](https://help.mikrotik.com/docs/download/attachments/137986076/600px-HTB_Example2.jpg?version=1&modificationDate=1658484471588&api=v2)

- **Queue01** limit-at=0Mbps max-limit=10Mbps
- **Queue02** limit-at=4Mbps max-limit=10Mbps
- **Queue03** limit-at=2Mbps max-limit=10Mbps priority=3
- **Queue04** limit-at=2Mbps max-limit=10Mbps priority=1
- **Queue05** limit-at=2Mbps max-limit=10Mbps priority=5

### 例2的结果

- **Queue03** 将收到2Mbps的数据
- **Queue04** 将收到6Mbps的数据
- **Queue05** 将收到2Mbps的数据
- **说明：** 在满足所有 **limit-at** 后，HTB将把吞吐量给有最高优先级的队列。

### 例3：内部队列limit-at

![](https://help.mikrotik.com/docs/download/attachments/137986076/600px-HTB_Example3.jpg?version=1&modificationDate=1658484595993&api=v2)

- **Queue01** limit-at=0Mbps max-limit=10Mbps
- **Queue02** limit-at=8Mbps max-limit=10Mbps
- **Queue03** limit-at=2Mbps max-limit=10Mbps priority=1
- **Queue04** limit-at=2Mbps max-limit=10Mbps priority=3
- **Queue05** limit-at=2Mbps max-limit=10Mbps priority=5

### 例3的结果

- **Queue03** 将收到2Mbps的数据
- **Queue04** 将收到6Mbps的数据
- **Queue05** 将收到2Mbps的数据
- **说明：** 在满足所有的 **limit-at** 后，HTB将把吞吐量给具有最高优先级的队列。因此，**内部** 队列 **Queue02** 指定了 **limit-at**，通过这样做，它为队列 **Queue04** 和 **Queue05** 保留8Mbps的吞吐量。在这两个队列中，**Queue04** 的优先级最高，这就是为什么它能获得额外的吞吐量。

### 例4：叶子队列limit-at

![](https://help.mikrotik.com/docs/download/attachments/137986076/600px-HTB_Example4.jpg?version=1&modificationDate=1658484626764&api=v2)

- **Queue01** limit-at=0Mbps max-limit=10Mbps
- **Queue02** limit-at=4Mbps max-limit=10Mbps
- **Queue03** limit-at=6Mbps max-limit=10Mbps priority=1
- **Queue04** limit-at=2Mbps max-limit=10Mbps priority=3
- **Queue05** limit-at=12Mbps max-limit=15Mbps priority=5

### 例4的结果

- **Queue03** 将收到~3Mbps的数据
- **Queue04** 将收到~1Mbps的数据
- **Queue05** 将收到~6Mbps的数据
- **说明：** 只有满足所有的 **limit-at**，HTB才被迫分配20Mbps-6Mbps到 **Queen03**，2Mbps到 **Queen04**，12Mbps到 **Queen05**，但输出接口能够处理10Mbps。由于输出接口队列通常是先进先出的，吞吐量分配将保持6：2：12或3：1：6的比例。
