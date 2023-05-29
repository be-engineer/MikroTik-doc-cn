# 概述

-   1 [Overview](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Overview)
-   2 [Nv2 protocol implementation status](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Nv2protocolimplementationstatus)
-   3 [Compatibility and coexistence with other wireless protocols](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Compatibilityandcoexistencewithotherwirelessprotocols)
-   4 [How Nv2 compares with Nstreme and 802.11](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-HowNv2compareswithNstremeand802.11)
    -   4.1 [Nv2 vs 802.11](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Nv2vs802.11)
    -   4.2 [Nv2 vs Nstreme](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Nv2vsNstreme)
-   5 [Configuring Nv2](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-ConfiguringNv2)
-   6 [Migrating to Nv2](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-MigratingtoNv2)
-   7 [Nv2 AP Synchronization](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Nv2APSynchronization)
    -   7.1 [Configuration example](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Configurationexample)
-   8 [QoS in Nv2 network](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-QoSinNv2network)
    -   8.1 [Nv2-qos=default](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Nv2-qos=default)
    -   8.2 [Nv2-qos=frame-priority](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Nv2-qos=frame-priority)
-   9 [Security in Nv2 network](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-SecurityinNv2network)

Nv2协议是由microtik开发的专用无线协议，用于Atheros 802.11无线芯片。Nv2基于TDMA(时分多址)媒体访问技术，而不是普通802.11设备使用的CSMA(载波感知多址)媒体访问技术。

TDMA媒体访问技术解决了隐藏节点问题，提高了媒体利用率，从而提高了吞吐量和延迟，特别是在PtMP网络中。

从AR5212开始的Atheros 802.11n芯片和传统802.11a/b/g芯片支持Nv2，但旧的AR5211和AR5210芯片不支持Nv2。这意味着- 11n和传统设备都可以参与同一个网络，并且不需要升级硬件来实现网络中的Nv2。

Nv2网络中的媒体访问由Nv2接入点控制。Nv2 AP将时间划分为固定大小的“周期”，根据AP和客户端的队列状态，将时间动态划分为下行链路(从AP发送到客户端的数据)和上行链路(从客户端发送到AP的数据)两部分。上行时间根据客户端对带宽的需求进一步划分。在每个周期的开始，AP广播一个时间表，告诉客户端何时应该传输以及他们可以使用的时间量。

为了允许新客户端连接，Nv2 AP定期为“未指定”客户端分配上行时间，然后新客户端使用此时间间隔向AP发起注册。然后AP估计AP和客户端之间的传播延迟，并开始定期为该客户端调度上行时间，以便完成注册并从客户端接收数据。

Nv2实现了基于每个客户端的动态速率选择和数据传输的ARQ。这使得跨Nv2链路的可靠通信成为可能。

对于QoS, Nv2使用内置的默认QoS调度器实现可变数量的优先级队列，该调度器可以伴随着基于防火墙规则的细粒度QoS策略或使用VLAN优先级或MPLS EXP位在网络上传播的优先级信息。

Nv2协议限制是每个接口511个客户端。

# Nv2协议实现状态

Nv2具有以下特点:

- TDMA媒体接入
- WDS支持
- QoS支持可变数量或优先级队列
- 数据加密
- RADIUS认证特性
- 统计字段
- 固定下行模式的支持
- 支持上行/下行比
- Nv2 AP同步实验支持

# 与其他无线协议兼容共存

Nv2协议不兼容或基于任何其他可用的无线协议或实现，无论是基于TDMA还是任何其他类型。这意味着 **只有支持和使能Nv2的设备才能参与Nv2网络** 。

普通的802.11设备将无法识别并连接到Nv2 AP。支持Nv2的RouterOS设备(即拥有RouterOS 5.0rc1或更高版本)在发出扫描命令时将看到Nv2 AP，但只有在正确配置的情况下才会连接到Nv2 AP。

由于Nv2不使用CSMA技术，它可能会干扰同一频道中的任何其他网络。同样，其他网络也会干扰Nv2网络，因为其他信号都被认为是噪声。

兼容与共存的要点:

- 只有RouterOS设备才能参与Nv2网络
- 扫描时，只有RouterOS设备才会看到Nv2 AP
- Nv2网络会干扰同信道的其他网络
- Nv2网络可能会受到同一通道内其他网络(无论是否为Nv2)的影响
- 启用Nv2的设备不会连接到任何其他基于TDMA的网络

# Nv2与nstream和802.11的比较

## Nv2 vs 802.11

Nv2和802.11的主要区别:

- 媒体访问由AP调度-这消除了隐藏节点问题，并允许实现集中的媒体访问策略- AP控制每个客户端使用多少时间，并可以根据某些策略为客户端分配时间，而不是每个设备都争夺媒体访问。
- 减少传播延迟开销- Nv2中没有每帧ACK -这显着提高了吞吐量，特别是在长距离链路上，数据帧和随后的ACK帧传播延迟显着降低了媒体使用的有效性。
- 减少每帧开销- Nv2实现帧聚合和分片，以最大限度地分配媒体使用和减少每帧开销(帧间空间，前文)。

## Nv2对比nstream

Nv2和nstream的主要区别:

- 减少轮询开销- Nv2 AP不是轮询每个客户端，而是广播一个上行时间表，分配时间给多个客户端，这可以被认为是“组轮询”-没有时间浪费在单独轮询每个客户端，留下更多的时间用于实际的数据传输。这提高了吞吐量，特别是在PtMP配置中。
- 减少传播延迟开销- Nv2不能单独轮询每个客户端，这允许基于到客户端的估计距离(传播延迟)创建上行时间表，这样媒体使用是最有效的。这提高了吞吐量，特别是在PtMP配置中。
- 对延迟的更多控制-减少开销，可调整周期大小和QoS功能允许对网络中的延迟进行更多控制。

# 配置Nv2

无线协议设置控制无线协议选择和使用。请注意，此设置的含义取决于接口角色(AP或客户端)，而接口角色取决于接口模式设置。在下表中找到无线协议的可能值及其含义。

| value              | AP                      | client                                                                                                                                             |
| ------------------ | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| unspecified        | 建立基于旧 nstreme 设置 | 建立NSTREME或802.11网络                                                                                                                            | 基于旧的 nstreme 设置 | 连接到NSTREME或802.11网络 |
| any                | 与unspecified 相同      | 扫描所有匹配网络，无论哪种协议，都使用所选网络协议进行连接                                                                                         |
| 802.11             | 建立802.11网络          | 仅连接到802.11网络                                                                                                                                 |
| nstreme            | 建立Nstreme网络         | 仅连接到Nstreme网络                                                                                                                                |
| NV2                | 建立NV2网络             | 仅连接到NV2网络                                                                                                                                    |
| NV2-NSTREME-802.11 | 建立NV2网络             | 扫描对NV2网络的扫描，如果找到合适的网络 - 连接，否则扫描NSTREME网络，如果找到合适的网络 - 连接，否则扫描802.11网络并找到合适的网络 - 连接 - 连接。 |
| NV2-NSTREME        | 建立NV2网络             | 扫描NV2网络的扫描，如果找到合适的网络 - 连接，否则扫描NSTREME网络并找到合适的网络 - 连接                                                           |

注意，无线协议值Nv2-nstreme-802.11和Nv2-nstreme不要指定一些混合或特殊类型的协议-这些值的实现是为了简化客户端配置，当客户端必须连接的网络协议可以改变。使用这些值有助于将网络迁移到Nv2协议。

大多数Nv2设置只对Nv2 AP有意义——Nv2客户端会自动适应AP的必要设置。以下设置与Nv2 AP相关:

- **Nv2-queue-count** 指定在Nv2网络中使用的优先队列的个数。更多详细信息请参见 [Nv2网络中的QoS](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-QoSinNv2network)
- **Nv2-qos** -控制帧到优先队列的映射策略。更多详细信息请参见 [Nv2网络中的QoS](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-QoSinNv2network)
- **Nv2-cell-radius** 指定到Nv2网络中最远客户端的距离，单位为km。此设置影响AP为客户端分配用于发起连接的争用时隙的大小，以及用于估计到客户端的距离的时隙的大小。如果此设置太小，则较远的客户端可能在连接和/或断开连接时出现“测距超时”错误。虽然在正常操作期间，此设置的影响应该可以忽略不计，但为了保持最大性能，建议在没有必要的情况下不要增加此设置，因此AP不是保留实际上从未使用过的时间，而是将其分配给实际的数据传输。
- **tdma-period-size** 指定Nv2 AP用于媒体访问调度的时间段大小，单位为毫秒。较小的周期可以潜在地减少延迟(因为AP可以更快地为客户机分配时间)，但会增加协议开销，从而降低吞吐量。另一方面，增加周期会增加吞吐量，但也会增加延迟。对于特别长的链路，可能需要增加这个值以获得可接受的吞吐量。这种必要性可能是由于在下行链路(从AP到客户端)和上行链路(从客户端到AP)数据之间存在“传播间隙”，在此期间没有发生数据传输。这个间隔是必要的，因为客户端必须从AP接收到最后一个帧——这发生在AP传输后的传播延迟之后，只有这样客户端才能传输——结果客户端的帧在客户端传输后的传播延迟之后到达AP(所以间隔是传播延迟的两倍)。距离越长，每个周期的必要传播间隙就越大。如果传播间隔占用周期的很大一部分，则实际吞吐量可能变得不可接受，周期大小应该以增加延迟为代价来增加。基本上，必须仔细选择此设置的值，以最大限度地提高吞吐量，同时将延迟保持在可接受的水平。
- **Nv2-mode** 指定使用动态或固定的下行/上行比例。默认值为“dynamic-downlink”;

"sync-master" -工作方式为nv2-mode=fixed-downlink(因此使用nv2-downlink-ratio)，但允许从端同步到这个主端;“sync-slave”-尝试同步到主服务器(或已经同步的从服务器)，并从主服务器调整周期大小和下行链路比率设置。

- **Nv2-downlink-ratio** - Nv2下行比。上行比由下行比自动计算。当使用动态下行模式时，当链路完全饱和时也使用下行比。最小值为20，最大值为80。默认值为50。

以下设置在Nv2 AP和Nv2客户端上都很重要:

- **Nv2-security** -指定Nv2的安全模式，详见 [Nv2网络中的安全](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Security_in_Nv2_network)
- **Nv2-preshared-key** -指定要使用的预共享密钥，详细信息请参见 [Nv2网络安全](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Security_in_Nv2_network)
- **Nv2 -sync-secret** - 指定用于Nv2同步的秘密密钥。为了建立同步状态，Secret应该在主设备和从设备上匹配。

# 迁移到Nv2

使用无线协议设置有助于在现有网络中迁移或评估Nv2协议，这非常简单，并尽可能减少停机时间。以下是建议的步骤:

升级AP到支持Nv2的版本，但不启用Nv2。
- 升级客户端到支持Nv2的版本
- 将所有客户端配置为**wireless-protocol= nv2 - nstream -802.11** 。客户端仍将使用以前使用的协议连接到AP，因为AP尚未切换到Nv2
- 在AP上配置Nv2相关配置
- 如果需要使用数据加密和安全认证，请在AP和客户端上配置Nv2安全相关设置(参见 [Nv2网络中的安全](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Security_in_Nv2_network))。
- 在AP上设置 **wireless-protocol=Nv2** ，使AP切换为Nv2协议。客户端现在应该使用Nv2协议连接。
- 如果遇到麻烦，你可以很容易地切换回以前的协议，只需将其更改回之前在AP上使用的任何协议。
微调Nv2相关设置，以获得可接受的延迟和吞吐量
- 通过QoS策略实现性能最大化。

基本故障排除指南:

- 客户端连接有问题或断开“测距超时”错误-检查 **Nv2-cell-radius** 设置是否正确
- 尽管信号和速率很好，但在长距离链路上的吞吐量出乎意料地低-尝试增加 **tdma-period-size** 设置



# Nv2 AP同步

这一功能将通过减少彼此之间的干扰，使同一位置上的多个MikroTik Nv2 ap以更好的方式共存。该特性将同步同一频率的ap的发送/接收时间窗，使所有同步的MikroTik Nv2 ap同时发送/接收。这允许多个ap在同一位置重复使用相同的无线频率，从而在频率规划方面具有更大的灵活性。

要使Nv2同步设置:

- 对于Nv2同步，应选择Master Nv2 AP，并指定“Nv2 -mode=sync-master”和“Nv2 
- sync-secret”。
- 对于Nv2从AP，应使用与主AP相同的无线频率，并使用与主AP配置相同的“Nv2 -mode=sync-slave”配置Nv2 -sync-secret。
- 当启用主AP时，从AP将尝试通过与指定的“nv2-sync-secret”进行匹配来开始搜索主AP。
- 找到主AP后，从AP将计算到主AP的距离，因为主AP可能不在同一位置。
- 从AP开始作为AP工作，并根据同步的主AP的周期大小和下行比例进行调整。
- 另外，当Slave AP正常工作后，其他Slave AP也可以使用该Slave AP进行同步。
- 从AP定期侦听主AP，检查“nv2-sync-secret”是否仍然匹配，并重新调整参数。如果主AP接口被禁用/启用，所有从AP也将被禁用，并将从头开始同步过程。
如果主AP停止工作，从AP也会停止工作，因为它们没有同步信息。

  

## 配置例子Configuration example

主AP:

```
 /interface wireless set wlan1 mode=ap-bridge ssid=Sector1 frequency=5220 nv2-mode=sync-master nv2-preshared-key=clients1 nv2-sync-secret=Tower1
```

从AP:

```
 /interface wireless set wlan1 mode=ap-bridge ssid=Sector2 frequency=5220 nv2-mode=sync-slave nv2-preshared-key=clients2 nv2-sync-secret=Tower1
```

从AP的监控接口:

```shell
[admin@SlaveAP] /interface wireless> monitor wlan1
                   status: running-ap
                  channel: 5220/20/an
        wireless-protocol: nv2
              noise-floor: -110dBm
       registered-clients: 1
    authenticated-clients: 1
           nv2-sync-state: synced
          nv2-sync-master: 4C:5E:0C:57:84:38
        nv2-sync-distance: 1
     nv2-sync-period-size: 2
  nv2-sync-downlink-ratio: 50

```

  
主AP上的调试日志:

```
 09:22:08 wireless,debug wlan1: 4C:5E:0C:57:85:BE attempts to sync
```

  
从AP上的调试日志:

```
09:22:08 wireless,debug wlan1: attempting to sync to 4C:5E:0C:57:84:38 
09:22:09 wireless,debug wlan1: synced to 4C:5E:0C:57:84:38 

```

# Nv2网络中的QoS

Nv2中的QoS是通过可变数量的优先级队列实现的。根据802.1D-2004推荐的规则，只有在所有高优先级队列为空的情况下，才会考虑队列进行传输。在实践中，这意味着首先将发送所有具有较高优先级队列的帧，然后才考虑下一个队列。因此，必须谨慎设计QoS策略，以便高优先级队列不会使低优先级队列饿死。

在Nv2网络中，QoS策略由AP控制，客户端从AP中调整策略。在AP上，QoS策略配置了 **Nv2-queue-count** 和 **Nv2- QoS** 参数。**Nv2-queue-count** 参数指定使用的优先队列数量。帧到队列的映射由 **Nv2-qos** 参数控制。

## Nv2-qos =default

在这种模式下，首先通过内置的QoS策略算法对出帧进行检查，该算法根据数据包的类型和大小选择队列。如果内置规则不匹配，则根据帧优先级字段选择队列，如Nv2-qos=frame-priority模式。

## Nv2-qos = frame-priority

该模式根据帧优先级字段选择QoS队列。请注意，帧优先级字段不是报头中的某些字段，因此它仅在数据包被给定设备处理时有效。帧优先级字段必须由防火墙规则显式设置，或者由帧转发过程隐式设置，例如从MPLS EXP位设置。有关帧优先级字段的更多信息，请参见:

-   [EXP bit behaviour](https://help.mikrotik.com/docs/display/ROS/EXP+bit+behaviour)
-   [WMM and VLAN priority](https://help.mikrotik.com/docs/display/ROS/WMM+and+VLAN+priority)

根据802.1D推荐用户优先级到流分类映射，根据帧优先级选择队列。映射取决于可用队列的数量(Nv2-queue-count参数)。例如，如果队列数量为4，则映射如下(注意此映射与WMM使用的映射有多相似):

-   priority 0,3 -> queue 0
-   priority 1,2 -> queue 1
-   priority 4,5 -> queue 2
-   priority 6,7 -> queue 3

如果队列数为2(默认)，则映射如下:

-   priority 0,1,2,3 -> queue 0
-   priority 4,5,6,7 -> queue 1

如果队列数为8(最大可能)，映射如下:

-   priority 1 -> queue 0
-   priority 2 -> queue 1
-   priority 0 -> queue 2
-   priority 3 -> queue 3
-   priority 4 -> queue 4
-   priority 5 -> queue 5
-   priority 6 -> queue 6
-   priority 7 -> queue 7

对于其他映射，关于这些映射的基本原理和推荐实践的讨论请参见802.1D-2004。

# Nv2网络的安全性

Nv2安全实现具有以下特点:

- 使用128位密钥的AES-CCM硬件加速数据加密;
- 4路握手密钥管理(类似于802.11i);
- 预共享密码匙认证方法(类似802.11i);
- 定期更新组密钥(用于广播和组播数据)。

作为专有协议，Nv2不使用802.11的安全机制，因此安全配置是不同的。使用Nv2协议的接口忽略安全配置文件设置。相反，通过以下接口设置来配置安全性:

- **Nv2-security** -该设置在Nv2网络中启用/禁用安全功能。注意，当在AP上启用安全性时，它将不接受禁用安全性的客户端。以同样的方式，启用了安全性的客户机将不会连接到不安全的ap。
- **Nv2-preshared-key** -用于认证的预共享密钥。数据加密密钥是在4路握手过程中由预共享密钥派生的。为了使两台设备建立连接，预共享密钥必须相同。如果预共享密钥不同，则连接将超时，因为远程方将无法正确解释密钥交换消息。