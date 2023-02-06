# 概述
___

Dot1X 是 IEEE 802.1X 标准在 RouterOS 中的实现。 主要目的是使用 EAP over LAN（也称为 EAPOL）提供基于端口的网络访问控制。 802.1X 由请求者（客户端）、认证者（服务器）和认证服务器（RADIUS 服务器）组成。 目前，RouterOS 支持验证方和请求方。 请求者支持的 EAP 方法是 EAP-TLS、EAP-TTLS、EAP-MSCHAPv2 和 PEAPv0/EAP-MSCHAPv2。
SMIPS 设备（hAP lite、hAP lite TC 和 hAP mini）不支持该功能。

## 客户端

___

请求方设置。

**子菜单:** `/interface dot1x client`

| 属性                                                                                                                                                                                                                                                  | 说明                                                                                                                                |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **anon-identity** (_string_;Default: )                                                                                                                                                                                                                | 外层 EAP 身份验证。 仅与 `eap-ttls` 和 `eap-peap` 方法一起使用。 如果未设置，来自 `identity` 参数的值将用于外层 EAP 身份验证。      |
| **client-certificate** (_string_;Default: )                                                                                                                                                                                                           | [System/Certificates](https://help.mikrotik.com/docs/display/ROS/Certificates) 中列出的证书名称。 当使用 `eap-tls` 方法时是必需的。 |
| **comment** (_string_; Default: )                                                                                                                                                                                                                     | 条目的简短描述。                                                                                                                    |
| **disabled** (_yes                           \| no_; Default: **no**)                                                                                                                                                                                 | 客户端是否启用。                                                                                                                    |
| **eap-methods** (_eap-tls                                             \| eap-ttls                                                                                                                            \| eap-peap \| eap-mschapv2_; Default: ) | 用于身份验证的 EAP 方法的有序列表。                                                                                                 |
| **identity** (_string_; Default: )                                                                                                                                                                                                                    | 用于 EAP 身份验证的请求者身份。                                                                                                     |
| **interface** (_string_; Default: )                                                                                                                                                                                                                   | 客户端将运行的接口的名称。                                                                                                          |
| **password** (_string_; Default: )                                                                                                                                                                                                                    | 请求方的明文密码。                                                                                                                  |

**只读属性**

| 属性                                                   | 说明                                                                                                                                                                                                                                                                                                                                                                                |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| status ( authenticated \| authenticating \| disabled ) | 可能状态： <br>authenticated - 客户端已成功通过身份验证； <br>authenticated without server - 无需与服务器通信即可授予对端口的访问权限； <br>authenticating - 已到达服务器并且身份验证过程正在进行中； <br>connecting - 身份验证过程的初始阶段； <br>disabled - 客户端被禁用； <br>error - 发生内部错误； <br>interface is down-父接口没有运行； <br>rejected - 服务器拒绝身份验证。 |

## 服务端

___

RouterOS dot1x 服务器充当身份验证器。 启用 dot1x 服务器的接口将阻止除用于身份验证的 EAPOL 数据包之外的所有流量。 客户端认证成功后，该接口将接受所有接收到的流量。 如果接口连接到具有多个主机的共享介质，则当一个客户端成功通过身份验证时，将接受来自所有主机的流量。 但是，可以 [配置动态切换规则](https://help.mikrotik.com/docs/display/ROS/Dot1X#Dot1X-Dynamicsswitchruleconfiguration) 仅接受经过身份验证的用户源 MAC 地址并丢弃所有其他源 MAC 地址。 如果身份验证失败，可以接受具有专用端口 VLAN ID 的流量。

在网桥端口上创建 dot1x 服务器时，网桥应该运行 (R/M)STP，否则来自客户端的 EAP 数据包不会被正确接受。 默认情况下，使用 `protocol-mode=rstp` 创建网桥接口。 如果网桥端口不发送任何 BPDU 或忽略任何接收到的 BPDU，请在网桥端口上使用 edge=yes 配置。

**子菜单:** `/interface dot1x server`

| 属性                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | 说明                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **accounting** (_yes                                                            \| no_; Default: **yes**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 是否向认证服务器发送RADIUS 计费请求。                                                                                                                                                                                                                                                                         |
| **auth-timeout** (_time_; Default: **1m**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 可用于 EAP 身份验证的总时间。                                                                                                                                                                                                                                                                                 |
| **auth-types** (_dot1x                                                          \| mac-auth_; Default: **dot1x**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | 在服务器接口上使用的身份验证类型。 当同时选择两个选项时，服务器将首选“dot1x”身份验证类型，并且只有在 3 个`retrans-timeout`周期后，身份验证类型才会回退到`mac-auth`。 为了使`mac-auth`身份验证起作用，服务器接口应至少接收一个包含客户端设备源 MAC 地址的帧。                                                  |
| **comment** (_string_; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | 条目的简短描述。                                                                                                                                                                                                                                                                                              |
| **disabled** (_yes                                                              \| no_; Default: **no**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 服务器配置是否启用。                                                                                                                                                                                                                                                                                          |
| **guest-vlan-id** (i _integer: 1..4094_; Default: **!guest-vlan-id**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | 当终端设备不支持`dot1x`身份验证且未配置`mac-auth`回退时分配的 VLAN。 该设置将在 3 个`retrans-timeout`周期后应用。 创建启用 dot1x 的客户端并成功进行重新身份验证后，该端口将从访客 VLAN 中删除。 设置仅在 RouterOS 7.2 版本后可用，并且在启用网桥`vlan-filtering`时有效。 默认情况下，访客 VLAN 处于禁用状态。 |
| **interface** (_string_; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 服务器在运行的接口或接口列表的名称。                                                                                                                                                                                                                                                                          |
| **interim-update** (_time_; Default: **0s**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | 计划的 RADIUS 临时更新消息之间的间隔。                                                                                                                                                                                                                                                                        |
| **mac-auth-mode** (_mac-as-username                                                                               \| mac-as-username-and-password_; Default: **mac-as-username**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | 允许在使用 MAC 身份验证时控制用户名和用户密码 RADIUS 属性。                                                                                                                                                                                                                                                   |
| **radius-mac-format** (_XX-XX-XX-XX-XX-XX                                                                         \| XX:XX:XX:XX:XX:XX                                                                                                                                                                                                                                                                                                                                                                                                                    \| XXXXXXXXXXXX                                                                                   \| xx-xx-xx-xx-xx-xx \| xx:xx:xx:xx:xx:xx \| xxxxxxxxxxxx_; Default: **XX:XX:XX:XX:XX:XX**) | 控制在使用 MAC 身份验证时客户端的 MAC 地址如何在用户名和用户密码属性中编码。                                                                                                                                                                                                                                  |
| **reauth-timeout** (_time_; Default: **!reauth-timeout**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 启用服务器端口重新验证。 当启用`dot1x`身份验证时，服务器会尝试向客户端发送 EAP-Request Identity 来重新验证客户端。 当启用`mac-auth`身份验证类型时，服务器将尝试用最后一次看到的 MAC 地址使用 RADIUS 服务器重新验证客户端。 设置仅适用于 RouterOS 7.2 版本。 默认情况下，重新验证是禁用的。                    |
| **reject-vlan-id** (i _integer: 1..4094_; Default: **!reject-vlan-id**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | 在身份验证失败且 RADIUS 服务器响应访问拒绝消息时分配的 VLAN。 如果 RADIUS 服务器根本没有响应，则此属性将不适用，客户端身份验证会超时并且服务将不可用。 此属性仅在启用网桥 `vlan-filtering` 时有效。 默认情况下，拒绝 VLAN 处于禁用状态。                                                                      |
| **retrans-timeout** (_time_; Default: **30s**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | 如果未收到请求方的响应，重传消息之间的时间间隔。                                                                                                                                                                                                                                                              |
| **server-fail-vlan-id** (i _integer: 1..4094_; Default: **!server-fail-vlan-id**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | 当 RADIUS 服务器未响应且请求超时过期时分配的 VLAN。 设置仅在 RouterOS 7.2 版本后可用，并且在启用网桥`vlan-filtering`时有效。 默认情况下，服务器故障 VLAN 处于禁用状态。                                                                                                                                       |

当前经过身份验证的客户端列在活动菜单中（只读属性）。

**子菜单:** `/interface dot1x server active`

| 属性                           | 说明                                                                                                                                                                                             |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **auth-info** (_string_)       | 认证信息:<br>-   dot1x<br>-   dot1x (guest vlan)<br>-   dot1x (reject vlan)<br>-   dot1x (server fail vlan)<br>-   mac-auth<br>-   mac-auth (reject vlan)<br>-   mac-auth (server fail vlan)<br> |
| **client-mac** (_mac-address_) | 请求方的 MAC 地址                                                                                                                                                                                |
| **interface** (_string_)       | 接口名称                                                                                                                                                                                         |
| **session-id** (_string_)      | 唯一会话标识符                                                                                                                                                                                   |
| **username** (_string_)        | 申请人标识符                                                                                                                                                                                     |
| **vlan-id** (_string_)         | 分配给接口的未标记 VLAN ID。 必须在网桥上启用 VLAN ID 过滤                                                                                                                                       |

所有活动的 dot1x 服务器接口的状态都列在状态菜单中（只读属性）

**子菜单:** `/interface dot1x server state`

| 属性                     | 说明                                                                                                                                                                                        |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **interface** (_string_) | 接口名称                                                                                                                                                                                    |
| **status** (_string_)    | 可能的接口状态：<br> -   authorized \- 授予对接口的访问权限；<br> -   iface-down \- 接口未运行;<br> -   rejected-holding \- 访问被RADIUS服务器拒绝;<br> -   un-authorized \- 接口访问未授权 |

## 示例

___

下面描述了 dot1x 服务器和客户端最常见的配置示例。

## RouterOS 认证器配置

![](https://help.mikrotik.com/docs/download/attachments/328090/Dot1x-setup.jpg?version=2&modificationDate=1612431387000&api=v2)

首先添加一个新的 RADIUS 客户端。 身份验证服务器 (RADIUS) 不必与身份验证器位于同一 LAN 中，但它必须可以从身份验证器访问，必须考虑防火墙限制。

```shell
/radius
add address=10.1.2.3 secret=radiussecret service=dot1x

```

> 如果通过公网进行RADIUS通信，建议使用RadSec进行RADIUS通信。 更多信息请见：[RADIUS](https://help.mikrotik.com/docs/display/ROS/RADIUS)

添加新的 dot1x 服务器实例。

```shell
/interface dot1x server
add interface=ether2 interim-update=30s comment=accounted
add interface=ether12 accounting=no comment=notaccounted

```

### 基于端口的 VLAN ID 分配

可以使用网桥 VLAN 过滤将经过身份验证的接口分配给特定的 VLAN ID。 这可以使用 RADIUS Tunnel-Type、Tunnel-Medium-Type 和 Tunnel-Private-Group-ID 属性来完成。 请注意，只有具有硬件卸载 VLAN 过滤的设备才能在交换芯片中执行此操作。

首先，确保将接口添加到启用了 VLAN 过滤的网桥。

```shell
/interface bridge
add name=bridge1 vlan-filtering=yes
/interface bridge port
add bridge=bridge1 interface=ether1
add bridge=bridge1 interface=ether2
add bridge=bridge1 interface=ether12

```

有必要为要通过 ether1 接口发送的标记 VLAN 流量添加静态 VLAN 配置。

```shell
/interface bridge vlan
add bridge=bridge1 tagged=ether1 vlan-ids=2
add bridge=bridge1 tagged=ether1 vlan-ids=12

```

用 RADIUS 调试日志，可以看到具有所有属性的完整 RADIUS 消息包。 在我们的示例中，隧道属性是在来自 RADIUS 服务器的 Access-Accept 消息中接收到的：

```shell
09:51:45 radius,debug,packet received Access-Accept with id 64 from 10.1.2.3:1812
09:51:45 radius,debug,packet     Tunnel-Type = 13
09:51:45 radius,debug,packet     Tunnel-Medium-Type = 6
09:51:45 radius,debug,packet     Tunnel-Private-Group-ID = "12"
(..)
09:51:45 radius,debug,packet     User-Name = "dot1x-user"

```

VLAN ID 现在出现在活动会话列表中，并且未标记的端口被添加到先前创建的静态 VLAN 配置中。

```shell
/interface dot1x server active print
 0 interface=ether12 username="dot1x-user" user-mac=00:0C:42:EB:71:F6 session-id="86b00006" vlan=12

```

```shell
/interface bridge vlan print detail
Flags: X - disabled, D - dynamic
 0 D bridge=bridge1 vlan-ids=1 tagged="" untagged="" current-tagged="" current-untagged=bridge1,ether3
 
 1   bridge=bridge1 vlan-ids=2 tagged=ether1 untagged="" current-tagged=ether1 current-untagged=ether2
 
 2   bridge=bridge1 vlan-ids=12 tagged=ether1 untagged="" current-tagged=ether1 current-untagged=ether12

```

### 动态交换规则配置

在某些网络配置中，特定请求者需要额外的访问规则来限制或允许某些网络服务。 可以使用 Mikrotik-Switching-Filter 属性来完成，请参阅 [RADIUS 供应商词典](https://wiki.mikrotik.com/wiki/Manual:RADIUS_Client/vendor_dictionary "Manual:RADIUS Client/vendor dictionary")。 当客户端成功通过身份验证服务器的验证时，服务器可以传回 Mikrotik-Switching-Filter 属性。 根据接收到的信息，身份验证器将在客户端所在的交换机端口上创建动态访问规则。 只要客户端会话处于活动状态并且接口正在运行，这些规则就会处于活动状态。关于正确的交换规则实施有一定的顺序和限制：

- `mac-protocol`、`src-mac-address`（自 RouterOS 7.2 版本起可用）、`src-address`（IPv4/掩码，自 RouterOS 7.2 版本起可用）、`dst-address`（IPv4/ mask), `protocol` (IPv4) `src-port` (L4, RouterOS 7.2 版本后可用), `dst-port` (L4) 支持条件参数
- 十六进制或十进制表示法可用于 `mac-protocol` 和 `protocol` 参数（例如 `protocol 17` 或 `protocol 0x11`）
- `src-port` 和 `dst-port` 支持单个或范围值（例如 `src-port 10` 或 `src-port 10-20`）
- `src-mac-address` 支持 "xx:xx:xx:xx:xx:xx" 或 "xxxxxxxxxxxx" 格式，并且可以使用 "none" 关键字设置没有任何源 MAC 地址的切换规则（例如 `src-mac-address none`)
- `src-mac-address`（如果属性尚未设置）、`switch` 和 `ports` 条件参数会自动为每个规则设置
- 每条规则都应以操作属性结尾，支持的值为 **drop** 或 **allow**。 如果未设置操作属性，将使用默认的 **allow** 值。
- 单个请求者支持多个规则，它们必须用逗号“,”分隔

下面是 Mikrotik-Switching-Filter 属性和它们创建的动态切换规则的一些示例：

```shell
# Drop ARP frames (EtherType: 0x0806 or 2054)
Mikrotik-Switching-Filter = "mac-protocol 2054 action drop"
 
/interface ethernet switch rule print
Flags: X - disabled, I - invalid, D - dynamic
 0  D ;;; dot1x dynamic
      switch=switch1 ports=ether1 src-mac-address=CC:2D:E0:11:22:33/FF:FF:FF:FF:FF:FF mac-protocol=arp copy-to-cpu=no redirect-to-cpu=no mirror=no new-dst-ports=""
 
# Allow UDP (IP protocol: 0x11 or 17) destination port 100 and drop all other packets
Mikrotik-Switching-Filter = "protocol 17 dst-port 100 action allow, action drop"
 
/interface ethernet switch rule print
Flags: X - disabled, I - invalid, D - dynamic
 0  D ;;; dot1x dynamic
      switch=switch1 ports=ether1 src-mac-address=CC:2D:E0:11:22:33/FF:FF:FF:FF:FF:FF protocol=udp dst-port=100 copy-to-cpu=no redirect-to-cpu=no mirror=no
 
 1  D ;;; dot1x dynamic
      switch=switch1 ports=ether1 src-mac-address=CC:2D:E0:11:22:33/FF:FF:FF:FF:FF:FF copy-to-cpu=no redirect-to-cpu=no mirror=no new-dst-ports=""
 
# Allow only authenticated source MAC address, drop all other packets
Mikrotik-Switching-Filter = "action allow, src-mac-address none action drop"
 
/interface ethernet switch rule print
Flags: X - disabled, I - invalid; D - dynamic
 0  D ;;; dot1x dynamic
      switch=switch1 ports=ether1 src-mac-address=CC:2D:E0:01:6D:EB/FF:FF:FF:FF:FF:FF copy-to-cpu=no redirect-to-cpu=no mirror=no
 
 1  D ;;; dot1x dynamic
      switch=switch1 ports=ether1 copy-to-cpu=no redirect-to-cpu=no mirror=no new-dst-ports=""

```
  
在我们的示例中，ether2 上的 Supplicant2 仅允许访问具有 UDP 目标端口 50 的 192.168.50.0/24 网络，应丢弃所有其他流量。 首先，确保硬件卸载在桥接端口上正常工作，否则交换规则可能无法正常工作。

```shell
/interface bridge port print
Flags: X - disabled, I - inactive, D - dynamic, H - hw-offload
 #     INTERFACE                   BRIDGE                   HW  PVID PRIORITY  PATH-COST INTERNAL-PATH-COST    HORIZON
 0   H ether1                      bridge1                  yes    1     0x80         10                 10       none
 1   H ether2                      bridge1                  yes    1     0x80         10                 10       none
 2   H ether12                     bridge1                  yes    1     0x80         10                 10       none

```
  
使用 RADIUS 调试日志，可以看到具有所有属性的完整 RADIUS 消息包。 在我们的示例中，Mikrotik-Switching-Filter 属性是在来自 Radius 服务器的 Access-Accept 消息中接收到的：

```shell
02:35:38 radius,debug,packet received Access-Accept with id 121 from 10.1.2.3:1812
(..)
02:35:38 radius,debug,packet     MT-Switching-Filter = "mac-protocol 2048 dst-address 192.168.50.0/24 dst-port 50 protocol 17 action allow,action drop"

```
  
动态交换规则在交换菜单下：

```shell
/interface ethernet switch rule print
Flags: X - disabled, I - invalid, D - dynamic
 0  D ;;; dot1x dynamic
      switch=switch1 ports=ether2 src-mac-address=CC:2D:E0:11:22:33/FF:FF:FF:FF:FF:FF mac-protocol=ip dst-address=192.168.50.0/24 protocol=udp dst-port=50 copy-to-cpu=no redirect-to-cpu=no mirror=no
 
 1  D ;;; dot1x dynamic
      switch=switch1 ports=ether2 src-mac-address=CC:2D:E0:11:22:33/FF:FF:FF:FF:FF:FF copy-to-cpu=no redirect-to-cpu=no mirror=no new-dst-ports=""

```

> 动态交换规则仅适用于支持交换规则的路由器板——CRS3xx、CRS5xx 系列交换机、CCR2116、CCR2216 以及带有 QCA8337、Atheros8327 和 Atheros8316 交换芯片的设备。 CRS1xx/2xx 系列交换机不支持此功能。 每个设备的最大规则数，请参阅 [CRS3xx、CRS5xx、CCR2116、CCR2216 表](https://help.mikrotik.com/docs/display/ROS/CRS3xx%2C+CRS5xx%2C+CCR2116%2C+CCR2216+switch+chip+features#CRS3xx,CRS5xx,CCR2116,CCR2216switchchipfeatures-Models) 和 [基本交换芯片表](https://help.mikrotik.com/docs/display/ROS/Switch+Chip+Features#heading-Introduction)

## RouterOS 请求者配置

`eap-tls、eap-ttls` 和 `eap-peap` 身份验证方法需要 CA 证书。 `eap-tls` 方法需要客户端证书。此示例我们已经导入了一个包含自签名客户端和 CA 证书的 P12 证书包。 有关如何在 RouterOS 中导入证书的更多信息，请访问 [System/Certificates](https://help.mikrotik.com/docs/display/ROS/Certificates)。

```shell
/certificate print
Flags: K - private-key, L - crl, C - smart-card-key, A - authority, I - issued, R - revoked, E - expired, T - trusted
 #         NAME                                            COMMON-NAME                                         SUBJECT-ALT-NAME                             FINGERPRINT                                       
 0 K  A  T dot1x-client                                    ez_dot1x-client                                     IP:10.1.2.34
 1  L A  T dot1x CA                                        ca

```

只需添加一个新的 dot1x 客户端实例即可启动身份验证过程。

```shell
/interface dot1x client
add anon-identity=anonymous client-certificate=dot1x-client eap-methods=eap-tls identity=dot1x-user interface=ether1 password=dot1xtest

```

如果身份验证成功，接口的状态应为已验证。

```shell
/interface dot1x client print
Flags: I - inactive, X - disabled
 0   interface=ether1 eap-methods=eap-peap identity="dot1x-user" password="dot1xtest" anon-identity="anonymous" client-certificate=dot1x-client status="authenticated"

```
