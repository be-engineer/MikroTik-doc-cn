# NTP

RouterOS v6采用RFC4330定义的SNTP协议，不支持多播模式。SNTP客户端包含在system包中。使用NTP服务器时，ntp包必须 [installed and enabled](https://help.mikrotik.com/docs/display/ROS/Packages)。

RouterOS v7主包包含NTP客户端和服务器功能，基于RFC5905。

客户端配置在“/system ntp client”控制台路径下，在“system > SNTP client” (RouterOS版本6)”、“system > ntp client” (RouterOS版本7)”WinBox窗口中配置。此配置由system包中的SNTP客户端实现和ntp包中的NTP客户端实现共享。安装并启用“ntp package”后，会自动禁用SNTP客户端。

# RouterOS version 6

**SNTP客户端属性:**

| 属性                                                                | 说明                                                                                                                                                                                                                                                |
| ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **enabled** (_yes,default:no_)                                      | 启用SNTP客户端时间同步                                                                                                                                                                                                                              |
| **mode** (_broadcast, unicast, filed is read-only_)                 | SNTP客户端操作的模式。如果未配置NTP服务器，则使用“broadcast模式”。如果使用了动态或静态NTP服务器IP地址或FQDN，则会自动切换到单播模式。                                                                                                               |
| **primary-ntp** (_IP address default: 0.0.0.0_)                     | 用于时间同步的NTP服务器的IP地址。如果两个值都不为零，则SNTP客户端将在两个服务器地址之间交替，当对当前服务器的请求超时或接收到“KoD”数据包时切换到另一个服务器，这表明服务器不愿意响应来自该客户端的请求。<br>接受以下格式:<br>_- ipv4_  <br>_- ipv6_ |
| **secondary-ntp** (_IP address default: 0.0.0.0_)                   | see **primary-ntp**                                                                                                                                                                                                                                 |
| **server-dns-names** (_Comma separated domain name list default:_ ) | 使用域名方式设置NTP服务器。每次发送NTP请求时，域名都会被解析。路由器必须配置/ip dns。                                                                                                                                                               |

**状态**

- **active-server** (IP地址，只读属性):当前选择的NTP服务器地址。取值等于 **primary-ntp** 或 **secondary-ntp** 。
- **poll-interval** (时间间隔，只读属性):发送到活动服务器的请求之间的当前间隔。初始值为16秒，增加一倍至15分钟。

**最后收到的数据包信息**

当SNTP客户端由于配置更改或网络错误而停止或重新启动时，将重置以下属性的值。

- **last-update-from** (IP地址;只读属性):最后一次收到的处理成功的NTP服务器包的源IP地址。
- **last-update-before** (时间间隔;只读属性):自上次成功接收服务器消息以来的时间。
- **last-adjustment** (时间间隔;只读属性):从上次成功接收到的NTP服务器消息计算出的时钟调整量。
- **last-bad-packet-from** (IP地址;只读属性):上次收到的未成功处理的SNTP包的源IP地址。失败的原因和收到数据包后的时间在接下来的两个属性中可用。
- **last-bad-packet-before**(时间间隔;只读属性):距离上次接收失败的时间。
- **last-bad-packet-reason** (Text;只读属性):描述上次接收失败原因的文本。可能的值有:
  - bad-packet-length -报文长度不在可接受范围内。
  - server-not-synchronized -Leap Indicator字段设置为“alarm condition”的值，表示该服务器的时钟尚未同步。
  - zero-transmit-timestamp - Transmit时间戳字段值为0。
  - bad- Mode - Mode字段的值既不是'server'也不是'broadcast'。
  - kod-ABCD -收到“KoD”(死亡之吻)回应。ABCD是来自参考标识符字段的简短“kiss code”文本。
  - broadcast -收到的广播消息，但mode=unicast。
  - non-broadcast -收到的包是服务器的回复，但mode=broadcast。
  - server-ip-mismatch -从非active-server地址收到的响应。
  - originate-timestamp-mismatch - Originate服务器响应消息中的时间戳字段与上次请求中包含的时间戳字段不一致。
  - roundtrip-too long -请求/响应往返时间超过1秒。

## 客户端设置示例:

在命令行中查看NTP客户端状态，使用print命令

```shell
[admin@ntp-example_v6] > /system ntp client print
           enabled: no
       primary-ntp: 0.0.0.0
     secondary-ntp: 0.0.0.0
  server-dns-names:
              mode: unicast
```

启用NTP客户端，设置NTP服务器的IP地址或FQDN。

```shell
[admin@ntp-example_v6] > /system ntp client set enabled=yes
[admin@ntp-example_v6] > /system ntp client print
             enabled: yes
         primary-ntp: 0.0.0.0
       secondary-ntp: 0.0.0.0
    server-dns-names:
                mode: unicast
     dynamic-servers: x.x.x.x, x.x.x.x
       poll-interval: 15s
       active-server: x.x.x.x
    last-update-from: x.x.x.x
  last-update-before: 6s570ms
     last-adjustment: -1ms786us
[admin@ntp-example_v6] > /system ntp client set primary-ntp=162.159.200.123
[admin@ntp-example_v6] > /system ntp client print
           enabled: yes
       primary-ntp: 162.159.200.123
     secondary-ntp: 0.0.0.0
  server-dns-names:
              mode: unicast
   dynamic-servers: x.x.x.x, x.x.x.x
     poll-interval: 16s
     active-server: x.x.x.x
```

## NTP服务器设置

服务器配置位于“/system ntp Server”目录下

| 属性                                            | 说明                                                            |
| ----------------------------------------------- | --------------------------------------------------------------- |
| **enabled** (_yes or no_;default :_no_)         | 启用NTP服务器                                                   |
| **broadcast** (_yes or no_;default :_no_)       | 启用某些NTP服务器模式，为了使该模式工作，您必须设置广播地址字段 |
| **multicast** (_yesor no_;default :_no_)        | 启用某些NTP服务器模式                                           |
| **manycast** (_yes or no_;default :_no_)        | 启用某些NTP服务器模式                                           |
| **broadcast-addresses** (_IP address_;default:) | 设置NTP服务器广播模式使用的广播地址                             |

**例子**

设置NTP服务器，本地网络地址为192.168.88.0/24

`/system ntp server set broadcast=yes broadcast-addresses=192.168.88.255 enabled=yes manycast=no`

# RouterOS version 7

**NTP客户端属性**

| 属性                                                 | 说明                                                                                                                                                                                                                                                                                                                                                                                  |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **enabled** (_yes，default:no_)                      | 启用NTP客户端时间同步                                                                                                                                                                                                                                                                                                                                                                 |
| **mode** (_broadcast, manycast, multicast, unicast_) | NTP客户端工作模式                                                                                                                                                                                                                                                                                                                                                                     |
| **NTP servers**                                      | NTP服务器列表。 可以添加静态条目。<br>接受以下格式：<br>-FQDN（“已解决的地址”将出现在“服务器”  - 如果地址已解决的情况下，则可以在适当的列中出现）或可以使用IP地址。 如果dhcp-client属性"use-peer-ntp = yes"  -  [dhcp](https://help.mikrotik.com/docs/display/ros/ros/ros/dhcp) 通告的动态入口<br>- ipv4_  <br>- ipv4@vrf  <br>- ipv6  <br>- ipv6@vrf  <br>- ipv6-linklocal%interface |
| **vrf** (_default: main_)                            | 虚拟路由与转发                                                                                                                                                                                                                                                                                                                                                                        |
| **Servers** (_Button/Section_)                       | 动态和静态添加的NTP服务器(地址、解析地址、最小轮询、最大轮询、iBurst、Auth的详细表。)<br>通过FQDN设置NTP服务器。每次发送NTP请求时，域名都会被解析。路由器必须配置/ip/dns。                                                                                                                                                                                                            |
| **Peers**                                            | 当前参数值<br><code>[admin@ntp-example_v7] > /system/ntp/monitor-peers<br> type="ucast-client" address=x.x.x.x refid="y.y.y.y" stratum=3 hpoll=10 ppoll=10 root-delay=28.869 ms root-disp=50.994 ms<br>   offset=-0.973 ms delay=0.522 ms disp=15.032 ms jitter=0.521 ms<br>-- [Q quit\|D dump\|C-z pause] </code>                                                                    |
| **Keys**                                             | NTP对称密钥，用于NTP客户端和服务器之间的认证。密钥标识符(Key ID)——标识用于生成消息身份验证代码的加密密钥的整数。                                                                                                                                                                                                                                                                      |

**状态**

- **已同步、已停止、等待、using-local-clock** - NTP客户端当前状态
- **频率偏移** - 每单位时间的分数频率偏移。
- **synchronized - Server** - NTP服务器的IP地址。
- **synsed -stratum** - 每台服务器的准确性由一个称为层的数字来定义，最顶层(主服务器)被分配为1，每层(辅助服务器)在层次结构中被分配为比前一层大1。
- **system-offset** - 这是一个有符号的定点数字，表示NTP服务器时钟相对于本地时钟的偏移量，以秒为单位。

## NTP服务器设置

服务器配置位于“/system ntp Server ”目录下

| 属性                                            | 说明                                                                                                             |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **enabled** (_yes or no_;default :_no_)         | 启用NTP服务器                                                                                                    |
| **broadcast** (_yes or no_;default :_no_)       | 启用某些NTP服务器模式，为了使该模式工作，您必须设置广播地址字段                                                  |
| **multicast** (_yes or no_;default :_no_)       | 启用NTP服务器模式                                                                                                |
| **manycast** (_yes or no_;default :_no_ )       | 启用NTP服务器模式                                                                                                |
| **broadcast-addresses** (_IP地址_;default : )   | 设置NTP服务器广播模式使用的广播地址                                                                              |
| **vrf** (_default: main_)                       | 虚拟路由转发                                                                                                     |
| **use-local-clock** (_yes or no_;default :_no_) | 如果其他时间不可用，服务器将提供其本地系统时间作为有效时间。                                                     |
| **local-clock-stratum**                         | 如果use-local-clock=yes则手动设置stratum                                                                         |
| **auth-key**(default :_none_)                   | NTP对称密钥，用于NTP客户端与服务器之间的认证。密钥标识符(Key ID)——标识用于生成消息身份验证代码的加密密钥的整数。 |

# 日志消息

SNTP客户端可以产生以下日志消息。 有关如何设置日志记录以及如何检查日志，请参见文章 [日志](https://wiki.mikrotik.com/wiki/log"log")。

- NTP，调试逐渐通过OFFS调整
- NTP，调试立即通过OFFS调整
- NTP，调试等待n秒，然后发送下一条消息
- NTP，调试等待n秒钟，然后重新启动
- NTP，调试，数据包数据包收到错误，重新启动
- NTP，调试，数据包收到了PKT
- NTP，调试，忽略收到PKT的数据包
- NTP，调试，数据包错误发送到IP，重新启动
- NTP，调试，数据包发送到IP PKT

日志消息字段的说明

 -  _OFFS_ - 十六进制中两个NTP时间戳值的差异。
 -  _PKT_ - NTP数据包的转储。 如果数据包短于最低48个字节，则将其倾倒为十六进制字符串。 否则，将数据包倾倒为字段名称和值列表，每个日志行。 字段的名称遵循RFC4330。
 -  _IP_ - 远程IP地址。

**注意**：上述记录规则仅与内置SNTP客户端一起使用，单独的NTP软件包没有任何记录设施。