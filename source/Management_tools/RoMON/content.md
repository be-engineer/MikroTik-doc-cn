<!--
 * @Author: be-engineer 41234995@qq.com
 * @Date: 2023-05-08 22:54:30
 * @LastEditors: be-engineer 41234995@qq.com
 * @LastEditTime: 2023-05-16 18:34:56
 * @FilePath: /MikroTik-doc-cn/source/Management_tools/RoMON/content.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# 概述

RoMON是 "路由器管理叠加网络 "的缩写。RoMON通过建立一个独立的MAC层对等体发现和数据转发网络来工作。RoMON数据包以EtherType 0x88bf和DST-MAC 01:80:c2:00:88:bf进行封装，其网络独立于L2或L3转发配置运行。当RoMON启用时，任何收到的RoMON数据包都不会被嗅探器或torch工具显示。

RoMON网络上的每个路由器都被分配了其RoMON ID。RoMON ID可以从端口MAC地址中选择或由用户指定。

RoMON协议不提供加密服务。加密是在 "应用 "层面提供的，例如通过使用ssh或使用安全的Winbox。

# 用secrets

RoMON协议的秘密用于消息认证、完整性检查和防止重放，方法是用MD5对消息内容进行散列。

对于每个接口，如果特定接口的秘密列表为空，则使用一个全局秘密列表。当发送时，如果列表不是空的，并且第一个不是 "空秘密"（空字符串=""），则用列表中的第一个秘密对报文进行散列，否则，报文将被发送为未散列。当收到时，只有当秘密列表为空或包含 "空秘密 "时，才会接受未加密的信息，如果与列表中的任何秘密进行了哈希处理，则接受哈希处理的信息。

这种设计允许在不中断RoMON服务的情况下逐步引入和/或改变网络中的秘密，并且可以通过RoMON本身发生，例如：

- 最初，所有的路由器都没有秘密；
- 将每个路由器逐一配置为secrets="", "mysecret"--这将使所有路由器仍然发送未受保护的帧，但它们都将准备接受受秘密 "mysecret"保护的帧；
- 用secrets="mysecret",逐一配置每个路由器 - 这将使所有路由器使用秘密 "mysecret"，但也仍然接受未受保护的帧（来自尚未被改变的路由器）；
- 在每个路由器上配置secrets="mysecret" - 这将使所有路由器使用secrets "mysecret"，并且只接受用 "mysecret"保护的帧；

网络中秘密的改变应该以类似的方式进行，在一段时间内，两个秘密都在网络中使用。

# 对等发现

为了发现RoMON网络上的所有路由器，必须使用RoMON discover命令：

```shell
[admin@MikroTik] > /tool/romon/discover
Flags: A - active
Columns: ADDRESS, COSt, Hops, PATH, L2MTu, IDENTITY, VERSION, BOARD
   ADDRESS            COS  H  PATH               L2MT  IDENTITY   VERSION    BOARD             
A  6C:3B:6B:48:0E:8B  200  1  6C:3B:6B:48:0E:8B  1500  hEX        6.47beta7  RB750Gr3          
A  6C:3B:6B:ED:83:69  200  1  6C:3B:6B:ED:83:69  1500  CCR1009    6.47beta7  CCR1009-7G-1C-1S+ 
A  B8:69:F4:B3:1B:D2  200  1  B8:69:F4:B3:1B:D2  1500  4K11       6.47beta7  RB4011iGS+5HacQ2HnD
A  CC:2D:E0:26:22:4D  200  1  CC:2D:E0:26:22:4D  1500  CCR1036    6.47beta7  CCR1036-8G-2S+    
A  CC:2D:E0:8D:01:88  200  1  CC:2D:E0:8D:01:88  1500  CRS328     6.47beta7  CRS328-24P-4S+    
A  E4:8D:8C:1C:D3:0E  200  1  E4:8D:8C:1C:D3:0E  1500  MikroTik   6.47beta7  RB2011iLS         
A  E4:8D:8C:49:49:DB  200  1  E4:8D:8C:49:49:DB  1500  hAP        6.47beta7  RB962UiGS-5HacT2HnT
```

# 配置示例

为了让设备参与到RoMON网络中，必须启用RoMON功能，并指定参与RoMON网络的端口。

`/tool romon set enabled=yes secrets=testing`.

参与RoMON网络的端口是在 **RoMON** 菜单中配置的。端口列表是一个列表，匹配特定端口或所有端口，并指定匹配的端口是否被禁止参与RoMON网络，如果端口允许参与RoMON网络条目还指定端口开销。请注意，所有特定的端口条目比带有 **interface=all** 的通配符条目具有更高的优先级。

例如，下面的列表指定所有端口以100的成本参与RoMON网络，以200的开销参与 ether7接口：

```shell
[admin@MikroTik] > /tool/romon/port/print
Flags: * - default
Columns: INTERFace, FOrbid, COSt
#     INTERF  FO  COS
0  *  all     no  100
1     ether7  no  200
```

默认情况下创建一个带有 **forbid=no** 和 **cost=100** 的通配符条目。

## 应用程序

多个应用程序可以在RoMON网络上运行。

为了测试RoMON网络上特定路由器的可达性，可以使用RoMON ping命令：

```shell
[admin@MikroTik] > /tool/romon/ping id=6C:3B:6B:48:0E:8B count=5
  SEQ HOST                                    TIME  STATUS                                                   
    0 6C:3B:6B:48:0E:8B                       1ms                                                            
    1 6C:3B:6B:48:0E:8B                       0ms                                                            
    2 6C:3B:6B:48:0E:8B                       1ms                                                            
    3 6C:3B:6B:48:0E:8B                       0ms                                                            
    4 6C:3B:6B:48:0E:8B                       1ms                                                            
    sent=5 received=5 packet-loss=0% min-rtt=0ms avg-rtt=0ms max-rtt=1ms
```

为了建立一个安全的终端连接到RoMON网络上的路由器，可以使用RoMON SSH命令：

`[admin@MikroTik] > /tool/romon/ssh 6C:3B:6B:48:0E:8B`

## 通过CLI在Winbox中运行RoMON

为了在计算机上直接使用命令行建立RoMON会话，必须指定RoMON代理和所需的路由器地址。RoMON代理必须保存在Winbox的管理路由器列表中，以便成功连接：

`winbox.exe --romon 192.168.88.1 6C:3B:6B:48:0E:8B admin ""`