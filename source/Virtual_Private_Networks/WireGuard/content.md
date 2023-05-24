# 介绍

-   1[Introduction](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Introduction)
-   2[Properties](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Properties)
    -   2.1[Read-only properties](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Read-onlyproperties)
-   3[Peers](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Peers)
    -   3.1[Read-only properties](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Read-onlyproperties.1)
-   4[Application examples](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Applicationexamples)
    -   4.1[Site to Site WireGuard tunnel](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-SitetoSiteWireGuardtunnel)
        -   4.1.1[WireGuard interface configuration](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-WireGuardinterfaceconfiguration)
        -   4.1.2[Peer configuration](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Peerconfiguration)
        -   4.1.3[IP and routing configuration](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-IPandroutingconfiguration)
        -   4.1.4[Firewall considerations](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Firewallconsiderations)
-   5[RoadWarrior WireGuard tunnel](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-RoadWarriorWireGuardtunnel)
    -   5.1[RouterOS configuration](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-RouterOSconfiguration)
    -   5.2[iOS configuration](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-iOSconfiguration)
    -   5.3[Windows 10 configuration](https://help.mikrotik.com/docs/display/ROS/WireGuard#WireGuard-Windows10configuration)

WireGuard<sup>®</sup>是一个非常简单但快速和现代的VPN，利用最先进的加密技术。它的目标是比IPsec更快、更简单、更精简和更有用，同时避免大量的麻烦。它打算比OpenVPN性能更好。WireGuard被设计为一种通用的VPN，可以在嵌入式接口和超级计算机上运行，适合许多不同的情况。它最初是为Linux内核发布的，现在是跨平台的(Windows, macOS, BSD, iOS, Android)，并且可以广泛部署。

**属性**

| 属性                                             | 说明                                             |
| ------------------------------------------------ | ------------------------------------------------ |
| **comment** (_string_;Default:)                  | 隧道的简短描述。                                 |
| **disabled** (_yes \| no_;Default:**no**)        | 开启/关闭隧道。                                  |
| **listen-port** (_integer;Default:13231_)        | WireGuard服务监听传入会话的端口。                |
| **mtu** (_integer [0..65536] _;Default:**1420**) | Layer3最大传输单元。                             |
| **name** (_string_;Default:)                     | 隧道名称。                                       |
| **private-key** (_string_;Default:)              | base64私钥。如果未指定，则在创建接口时自动生成。 |

**只读属性**

| 属性                      | 说明                       |
| ------------------------- | -------------------------- |
| **public-key** (_string_) | 从私钥中计算出base64公钥。 |
| **running** (_yes\| no_)  | 接口是否正在运行。         |

**对等体**

| 属性                                                      | 说明                                                                                                                                                                                                                                 |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **allowed-address** (_IP/IPv6 prefix_; Default: )         | 带有CIDR掩码的IP地址(v4或v6)列表，允许该对等体的入方向流量，也允许该对等体的出方向流量。可以指定_0.0.0.0/0_来匹配所有IPv4地址，也可以指定_::/0_来匹配所有IPv6地址。                                                                  |
| **comment** (_string_;Default:)                           | 对等体的简短描述。                                                                                                                                                                                                                   |
| **disabled** (_yes \| no_; Default: **no**)               | 启用/禁用对等体。                                                                                                                                                                                                                    |
| **endpoint-address** (_IP/主机名_;Default:)               | 端点IP或主机名可以留空以允许从任何地址进行远程连接。                                                                                                                                                                                 |
| **endpoint-port** (_integer:0..65535_;  Default:)         | 端点端口可以留空，允许从任何端口进行远程连接。                                                                                                                                                                                       |
| **interface** (_string;Default:_)                         | 对端所属的WireGuard接口名称。                                                                                                                                                                                                        |
| **persistent-keepalive** (_integer:0..65535; Default: 0_) | 一个秒间隔，在1到65535之间，为保持有状态防火墙或NAT映射持续有效的目的，向对等端发送经过身份验证的空数据包的频率。例如，如果接口很少发送流量，但它可能随时从对等体接收流量，并且它在NAT之后，接口可能会受益于25秒的持久保持时间间隔。 |
| **preshared-key** (_string;Default:_)                     | base64预共享密钥。可选，可以省略。这个选项添加了一个额外的对称密钥加密层，将其混合到已经存在的公钥加密中，以实现后量子抵抗。                                                                                                         |
| **public-key** (_string;Default:_)                        | 计算出的远端公钥。                                                                                                                                                                                                                   |

**只读属性**

| 属性                                     | 说明                                       |
| ---------------------------------------- | ------------------------------------------ |
| **current-endpoint-address** (_IP/IPv6_) | 从对端收到的正确认证报文的最近的源IP地址。 |
| **current-endpoint-port** (_integer_)    | 从对端收到正确认证报文的最近的源IP端口。   |
| **last-handshake** (i_integer_)          | 最后一次成功握手后的秒数。                 |
| **rx** (_integer_)                       | 从对端接收到的总字节数。                   |
| **tx** (_integer_)                       | 向对端发送的总字节数。                     |

# 应用示例

## 站点到站点的WireGuard隧道

考虑如下所示的设置。两个远端办公路由器连接到internet，办公工作站位于NAT后。每个办公室都有自己的本地子网，Office1为10.1.202.0/24,Office2为10.1.101.0/24。两个远程办公室都需要连接路由器后面的本地网络的安全隧道。

![](https://help.mikrotik.com/docs/download/attachments/69664792/Site-to-site-ipsec-example.png?version=1&modificationDate=1622538715602&api=v2)

### WireGuard接口配置

首先，需要在两个站点上配置WireGuard接口，使其能够自动生成私钥和公钥。这两个路由器的命令是相同的:

`/interface/wireguard
add listen-port=13231 name=wireguard1`

现在，在打印接口详细信息时，私钥和公钥都应该是可见的，以便进行交换。

在远程设备上永远不需要任何私钥-因此名称为private。

**Office1**

```shell
/interface/wireguard print
Flags: X - disabled; R - running
 0  R name="wireguard1" mtu=1420 listen-port=13231 private-key="yKt9NJ4e5qlaSgh48WnPCDCEkDmq+VsBTt/DDEBWfEo="
      public-key="u7gYAg5tkioJDcm3hyS7pm79eADKPs/ZUGON6/fF3iI="
```

**Office2**

```shell
/interface/wireguard/print
Flags: X - disabled; R - running
 0  R name="wireguard1" mtu=1420 listen-port=13231 private-key="KMwxqe/iXAU8Jn9dd1o5pPdHep2blGxNWm9I944/I24="
      public-key="v/oIzPyFm1FPHrqhytZgsKjU7mUToQHLrW+Tb5e601M="
```

### 对等体配置

对端配置定义了谁可以使用WireGuard接口，以及哪些流量可以通过该接口发送。为了识别远端对等体，必须在创建WireGuard接口的同时指定其公钥。

**Office1**

```shell
/interface/wireguard/peers
add allowed-address=10.1.101.0/24 endpoint-address=192.168.80.1 endpoint-port=13231 interface=wireguard1 \
public-key="v/oIzPyFm1FPHrqhytZgsKjU7mUToQHLrW+Tb5e601M="
```

**Office2**

```shell
/interface/wireguard/peers
add allowed-address=10.1.202.0/24 endpoint-address=192.168.90.1 endpoint-port=13231 interface=wireguard1 \
public-key="u7gYAg5tkioJDcm3hyS7pm79eADKPs/ZUGON6/fF3iI="
```

### IP和路由配置

最后，必须配置IP和路由信息，以允许流量通过隧道发送。

**Office1**

```shell
/ip/address
add address=10.255.255.1/30 interface=wireguard1
/ip/route
add dst-address=10.1.101.0/24 gateway=wireguard1
```

**Office2**

```shell
/ip/address
add address=10.255.255.2/30 interface=wireguard1
/ip/route
add dst-address=10.1.202.0/24 gateway=wireguard1
```

### 防火墙注意事项

RouterOS默认防火墙会阻止隧道正常建立。在两个站点上的任何drop规则之前，流量应该在“输入”链中被接受。

**Office1**

`/ip/firewall/filter
add action=accept chain=input dst-port=13231 protocol=udp src-address=192.168.80.1`

**Office2**

`/ip/firewall/filter
add action=accept chain=input dst-port=13231 protocol=udp src-address=192.168.90.1`

此外，“转发”链也可能限制子网之间的通信，因此在任何丢弃规则之前也应该接受此类流量。

**Office1**

```shell
/ip/firewall/filter
add action=accept chain=forward dst-address=10.1.202.0/24 src-address=10.1.101.0/24
add action=accept chain=forward dst-address=10.1.101.0/24 src-address=10.1.202.0/24
```

**Office2**

```shell
/ip/firewall/filter
add action=accept chain=forward dst-address=10.1.101.0/24 src-address=10.1.202.0/24
add action=accept chain=forward dst-address=10.1.202.0/24 src-address=10.1.101.0/24
```

# RoadWarrior WireGuard隧道

## RouterOS配置

新建WireGuard接口，并配置IP地址。

```shell
/interface wireguard
add listen-port=13231 name=wireguard1
/ip address
add address=192.168.100.1/24 interface=wireguard1
```

添加新的WireGuard接口将自动生成一对私钥和公钥。需要在远程设备上配置公钥。要获取公钥值，只需打印出接口详细信息。

```shell
[admin@home] > /interface wireguard print
Flags: X - disabled; R - running
 0  R name="wireguard1" mtu=1420 listen-port=13231 private-key="cBPD6JNvbEQr73gJ7NmwepSrSPK3np381AWGvBk/QkU="
      public-key="VmGMh+cwPdb8//NOhuf1i1VIThypkMQrKAO9Y55ghG8="
```

对于接下来的步骤，需要找出远程设备的公钥。有了它之后，通过指定远端设备的公钥和允许通过WireGuard隧道的地址来添加一个新的对端。

```shell
/interface wireguard peers
add allowed-address=192.168.100.2/32 interface=wireguard1 public-key="<paste public key from remote device here>"
```

**防火墙事项**

如果您配置了默认防火墙或严格防火墙，您需要允许远程设备与您的设备建立WireGuard连接。

```shell
/ip firewall filter
add action=accept chain=input comment="allow WireGuard" dst-port=13231 protocol=udp place-before=1
```

如果需要允许远程设备接入RouterOS的业务(如request DNS)，可以允许WireGuard子网在输入链中。

```shell
/ip firewall filter
add action=accept chain=input comment="allow WireGuard traffic" src-address=192.168.100.0/24 place-before=1
```

或者简单地将WireGuard接口添加到“LAN”接口列表中。

`/interface list member
add interface=wireguard1 list=LAN`

## iOS配置

从App Store中下载WireGuard应用程序。打开它并从头创建一个新配置。

![](https://help.mikrotik.com/docs/download/attachments/69664792/IMG_4392.PNG?version=1&modificationDate=1655382066647&api=v2)

首先，为您的连接指定一个“名称”，并选择生成一个密钥对。生成的公钥是RouterOS侧配置对等体所必需的。

![](https://help.mikrotik.com/docs/download/attachments/69664792/IMG_4393.PNG?version=1&modificationDate=1655382081378&api=v2)  


在“地址”字段中指定与服务器端配置的IP地址在同一子网内。此地址将用于通信。在这个例子中，我们在RouterOS端使用192.168.100.1/24，你可以在这里使用192.168.100.2。

如果需要，请配置DNS服务器。如果在RouterOS侧“IP/DNS”区域配置“allow-remote-requests”为“yes”，则可以在此处指定远端WireGuard的IP地址。

![](https://help.mikrotik.com/docs/download/attachments/69664792/IMG_4394.PNG?version=1&modificationDate=1655382092515&api=v2)  


单击“添加对等体”，将显示更多参数。

其中“Public key”为RouterOS侧WireGuard接口生成的公钥值。

“端点”是指iOS设备可以通过Internet与之通信的RouterOS设备的IP地址或端口号。

“允许的ip”设置为0.0.0.0/0，表示允许所有流量通过WireGuard隧道发送。

![](https://help.mikrotik.com/docs/download/attachments/69664792/IMG_4396.PNG?version=1&modificationDate=1655382100586&api=v2)

## Windows 10配置

从WireGuard下载WireGuard安装程序
以管理员身份运行。

![](https://help.mikrotik.com/docs/download/attachments/69664792/test.png?version=1&modificationDate=1679667322504&api=v2)

按Ctrl+n添加新的空隧道，为接口添加名称，应自动生成公钥，将其复制到RouterOS对端配置中。
添加到服务器配置，所以完整的配置看起来像这样,保持你的自动生成的PrivateKey在[接口]部分:


```shell
[Interface]
PrivateKey = your_autogenerated_public_key=
Address = 192.168.100.3/24
DNS = 192.168.100.1

[Peer]
PublicKey = your_MikroTik_public_KEY=
AllowedIPs = 0.0.0.0/0
Endpoint = example.com:13231
```

  
保存和激活
