# 概述

边界网关协议（BGP）可以建立域间动态路由系统，在网络拓扑变化时自动更新运行BGP的设备的路由表。

BGP是一个基于距离向量算法的自治系统间的路由协议。用在互联网上交换路由信息，是唯一为处理互联网这种规模的网络而设计的协议，也是唯一能够很好地处理有多个连接到不相关的路由域的协议。

BGP的设计是为了允许实施复杂的管理性路由策略。它不交换关于网络拓扑结构的信息，而是交换可达信息。因此，BGP更适合于AS间环境和信息反馈等特殊情况。如果你只要在网络中启用动态路由，可以考虑OSPF来代替。

SMIPS设备（hAP lite、hAP lite TC和hAP mini）不支持该功能。

  
标准和技术：

- [RFC 4271](https://tools.ietf.org/html/rfc4271) 边界网关协议4
- [RFC 4456](https://tools.ietf.org/html/rfc4456) BGP路由反射
- [RFC 5065](https://tools.ietf.org/html/rfc5065) BGP的自治系统联盟
- [RFC 1997](https://tools.ietf.org/html/rfc1997) BGP社区属性
- [RFC 8092](https://tools.ietf.org/html/rfc8092) BGP大型社区
- [RFC 4360](https://tools.ietf.org/html/rfc4360), [5668](https://tools.ietf.org/html/rfc5668) BGP扩展社区
- [RFC 2385](https://tools.ietf.org/html/rfc2385) BGPv4的TCP MD5认证
- [RFC 5492](https://tools.ietf.org/html/rfc5492) BGP-4的能力通告通告
- [RFC 2918](https://tools.ietf.org/html/rfc2918) 路线刷新能力
- [RFC 4760](https://tools.ietf.org/html/rfc4760) BGP-4的多协议扩展
- [RFC 2545](https://tools.ietf.org/html/rfc2545) 在IPv6域间路由中使用BGP-4多协议扩展
- [RFC 4893](https://tools.ietf.org/html/rfc4893) BGP对四字节AS号码空间的支持
- [RFC 4364](https://tools.ietf.org/html/rfc4364) BGP/MPLS IP虚拟专用网络(VPN)  
- [RFC 4761](https://tools.ietf.org/html/rfc4761) 使用BGP进行自动发现和信令的虚拟专用局域网服务(VPLS)
- [RFC 6286](https://tools.ietf.org/html/rfc6286) - BGP-4的AS范围唯一BGP标识符

# BGP术语

- AS - 自治系统
- ASN - 自治系统号
- NLRI - 网络层可达性信息，是BGP对等体之间交换的内容，表示如何到达前缀。
- IGP - 内部网关协议
- EGP--外部网关协议
- RR--路由反射器是BGP网络中的路由器，它向所有邻居反射通告，避免了对BGP全网的要求。 
- 路由服务器 - 是不参与流量转发的BGP路由器。路由通常甚至不安装在FIB中。
- 环回地址 - 配置在假桥接口上的一个/32地址，可以作为环回。

# BGP基础知识

BGP路由器通过传输协议交换可达性信息，在BGP的情况下是TCP（端口179）。在形成TCP连接时，这些路由器交换“OPEN”消息，以协商和确认支持的能力。

在就使用的能力达成一致后，会话被认为已经建立，对等体可以通过“UPDATE”消息开始交换NLRI。该信息包含一个指示，说明路由应该采取什么顺序的完整路径（BGP AS号码），以便到达目的网络（NLRI前缀）。

对等体最初交换其完整的路由表，在最初的交换之后，随着路由表的变化，增量更新被发送。因此，BGP不需要定期刷新整个BGP路由表。

BGP维护路由表的版本号，在连接期间任何两个给定的对等体之间都必须是相同的。

**KEEPALIVE** 消息会定期发送，以确保连接处于运行状态，如果在 **Hold Time** 间隔内没有收到 **KEEPALIVE** 消息，连接将被关闭。

为了应对错误或特殊情况，可以生成 **NOTIFICATION** 消息并发送至远程对等体，通知消息类型也表明是否应立即关闭连接。

可以有两种类型的BGP连接：

- **iBGP** - 是连接同一AS的对等体的 "内部 "链接
- **eBGP** - 是一种 "外部 "链接，连接属于两个不同AS的对等体。

特定的AS可能有多个BGP发言人，并向其他AS-es提供过境服务。这意味着BGP发言人必须保持对AS内路由的一致看法。 通过让AS内的所有BGP路由器彼此建立直接的iBGP连接（全网状）或利用Router Reflector设置，可以提供对AS外部路由的一致看法。

使用一套管理策略，AS内的BGP发言人就使用哪个入口/出口点到达某个特定目的地达成协议。这一信息通过内部路由协议（IGP）传达给AS的内部路由器，例如OSPF、RIP或静态路由。在某些设置中，iBGP也可以承担IGP协议的角色。

对于某些BGP属性的处理行为可能会根据设置的连接类型而改变，例如，LOCAL-PREF属性不向eBGP对等体公布。

RouterOS将配置和会话监控分为三个菜单：

- 连接菜单 (`/routing/bgp/connection`)
- 会话菜单 (`/routing/bgp/session`)
- 模板菜单 (`/routing/bgp/template`)

## 连接菜单

看一个非常基本的eBGP配置例子，假设Router1的IP是192.168.1.1，AS 65531，Router2的IP是192.168.1.2，AS 65532：

```shell
#Router1
/routing/bgp/connection
add name=toR2 remote.address=192.168.1.2 as=65531 local.role=ebgp
```

```shell
#Router2
/routing/bgp/connection
add name=toR1 remote.address=192.168.1.1 as=65532 local.role=ebgp
```

BGP连接菜单定义了BGP出站连接，并作为入站BGP连接的模板匹配器。

 `local.role` 参数用来表示该连接将是eBGP。另外，注意该连接不需要指定远程AS号，RouterOS可以从第一个收到的 **OPEN** 消息中动态地确定远程AS号。

与其他厂商和旧版RouterOS "update-source "相当的参数是 "local.address"。在大多数情况下，它可以不配置，让路由器决定地址。

如果没有指定本地地址，BGP将根据当前的设置尝试猜测本地地址：

- 如果对等体是iBGP
    - 如果回环地址可用
        - 选择最高的回环地址
    - 如果环回地址不可用
        - 挑选路由器上的任何最高IP地址
- 如果对等体是eBGP
    - 如果远程对等体的IP不是来自直接连接的网络：
        - 并且没有设置multihop，则抛出一个错误
        - 并且多跳被启用：
            - 如果回环地址可用
                - 选择最高的回环地址
            - 如果环回地址不可用
                - 选取路由器上任何一个最高的IP地址
    - 如果远程对等体的IP来自直接连接的网络：
        - 并且没有设置多跳：
            - 挑选该连接网络中的本地路由器的IP地址
        - 并且多跳被设置：
            - 如果回环地址可用
                - 选择最高的回环地址
            - 如果环回地址不可用
                - 挑选路由器上的任何最高IP地址
  

除了特定于连接的参数，特定于模板的参数也直接暴露在这个菜单中，以便在简单的情况下更容易配置（当模板没有必要时）。

所有连接特定参数的列表可以在下表中看到：

<table class=MsoNormalTable  border=1  cellspacing=0  style="border-collapse:collapse;width:548.2500pt;margin-left:-4.3500pt;
border:none;mso-border-left-alt:0.5000pt solid windowtext;mso-border-top-alt:0.5000pt solid windowtext;
mso-border-right-alt:0.5000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;mso-border-insideh:0.5000pt solid windowtext;
mso-border-insidev:0.5000pt solid windowtext;mso-padding-alt:0.7500pt 0.7500pt 0.7500pt 0.7500pt ;" ><tr><td valign=center  colspan=2  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:1.0000pt solid windowtext;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  align=center  style="mso-pagination:widow-orphan;text-align:center;" ><b><span style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" ><font face="Helvetica" >属性</font></span></b><b><span style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:1.0000pt;" ><o:p></o:p></span></b></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:1.0000pt solid windowtext;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  align=center  style="mso-pagination:widow-orphan;text-align:center;" ><b><span style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" ><font face="Helvetica" >说明</font></span></b><b><span style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:1.0000pt;" ><o:p></o:p></span></b></p></td></tr><tr><td valign=center  colspan=2  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><b style="mso-bidi-font-weight:normal" ><span class="16"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >name</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="17"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >string</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >BGP连接的名称</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td valign=center  colspan=2  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><b style="mso-bidi-font-weight:normal" ><span class="16"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >connect</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="17"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >yes | no</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: yes)</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >是否允许路由器启动连接。</font></span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td valign=center  colspan=2  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><b style="mso-bidi-font-weight:normal" ><span class="16"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >listen</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="17"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >yes | no</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: yes)</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >是否监听进入的连接。</font></span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td valign=center  colspan=2  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><b style="mso-bidi-font-weight:normal" ><span class="16"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >local</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;- 一组与连接的本地侧相关的参数</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td></tr><tr><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="16"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.address</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="17"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >IPv4/6</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default：:: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:1.0000pt solid windowtext;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >本地连接地址。</font></span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="16"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.port</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >(</span><span class="17"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >integer [0..65535]</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default：179 )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >本地连接端口。</font></span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="16"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.role</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >(ebgp| ebgp-customer| ebgp-peer| ebgp-provider | ebgp-rs | ebgp-rs-client | ibgp | ibgp-rr | ibgp-rr-client; Default: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >BGP角色，在大多数常见情况下，应该设置为iBGP或eBGP。关于BGP角色的更多信息可以在相应的RFC草案中找到&nbsp;</span><span style="font-family:Helvetica;color:rgb(0,136,204);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><a href="https://datatracker.ietf.org/doc/draft-ietf-idr-bgp-open-policy/?include_text=1" >https://datatracker.ietf.org/doc/draft-ietf-idr-bgp-open-policy/?include_text=1</a></span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="16"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.ttl</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="17"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >integer [1..255]</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default:)</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >将被记录在发送的</font>TCP数据包中的生存时间（跳数限制）。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td valign=center  colspan=2  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><b style="mso-bidi-font-weight:normal" ><span class="16"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >remote</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;- 一组与连接的远程端相关的参数</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td></tr><tr><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="16"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.address</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="17"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >IPv4/6</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default:</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:1.0000pt solid windowtext;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >用于连接或监听的远程地址。</font></span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="16"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.port</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >(</span><span class="17"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >integer [0..65535]</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default：179 )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >本地连接端口。</font></span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="16"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.as</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >(</span><span class="17"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >integer []</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >远程</font>AS号码。如果不指定，BGP将从OPEN消息中自动确定远程AS。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="16"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.allow-as</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >()</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >允许连接的远程</font>AS号码列表。对于动态对等体配置很有用。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="16"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.ttl</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="17"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >integer [1..255]</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default:)</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >可接受的最小生存时间，该</font>TCP连接的跳数限制。例如，如果 'ttl=255'，那么只有单跳的邻居才能建立连接。这个属性只影响EBGP对等体。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td valign=center  colspan=2  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><b style="mso-bidi-font-weight:normal" ><span class="16"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >tcp-md5-key</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="17"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >string</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >用于用</font>RFC 2385中描述的TCP MD5签名验证连接的密钥。如果不指定，则不使用认证。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td valign=center  colspan=2  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><b style="mso-bidi-font-weight:normal" ><span class="16"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >templates</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="17"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >name[,name]</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: default)</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td valign=center  style="padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;mso-border-left-alt:0.5000pt solid windowtext;
border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;border-top:none;
mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;
background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >模板名称列表，用于继承参数。对动态</font>BGP对等体很有用。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr></table>

## 会话菜单

要查看具有选定模板参数和协商能力的实际活动会话，请参考BGP会话菜单：

```shell
[admin@MikroTik] /routing/bgp/session> print
Flags: E - established
 0 E name="toR2"
     remote.address=192.168.1.2 .as=65532 .id=192.168.1.1 .refused-cap-opt=no
     .capabilities=mp,rr,as4 .afi=ip,ipv6 .messages=43346 .bytes=3635916 .eor=""
     local.address=192.168.1.1 .as=65531 .id=192.168.44.2 .capabilities=mp,rr,gr,as4 .messages=2
     .bytes=71 .eor=""
     output.procid=97 .keep-sent-attributes=no
     .last-notification=ffffffffffffffffffffffffffffffff0015030601
     input.procid=97 .limit-process-routes=500000 ebgp limit-exceeded
     hold-time=3m keepalive-time=1m uptime=4s70ms
```

该菜单显示只读缓存的BGP会话信息。显示会话的当前状态、标志、最后收到的通知，以及协商的会话参数。

即使BGP会话不再活动，缓存仍然可以保存一段时间。从特定会话中收到的路由只有在缓存过期时才会被删除，可以在BGP会话失效时减轻大量路由表的重新计算。

  

另外，在这个菜单中，有一组针对会话的命令。

| 命令                          | 说明                                                                                                                                                                                                                                 |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **clear**                     | 清除会话标志。例如，为了能够在达到前缀限制后重新建立一个会话，必须清除 "limit-exceeded "标志。可以通过指定"flag"参数来实现，该参数可以取以下值：<br>- 输入-最后通知  <br>- 超限  <br>- 输出-最后通知  <br>- 被拒绝的上限  <br>- 停止 |
| **dump-saved-advertisements** | 将指定BGP会话中保存的通告转*.pcap文件中。存储数据的文件名由"save-to"参数设置。                                                                                                                                                   |
| **refresh**                   | 向指定的BGP会话发送路由刷新。用于触发重新发送来自远程对等体的所有路由。"address-family "参数允许指定为哪个地址族发送路由刷新。                                                                                                       |
| **resend**                    | 向指定的BGP会话发送前缀。该命令需要两个参数：<br>- "address-family" - 参数允许指定为哪个地址族重新发送前缀。<br>- "save-to" - 转载重新发送的信息的pcap文件名，可用于调试目的。                                                       |
| **reset**                     | 重置指定的BGP会话。                                                                                                                                                                                                                  |
| **stop**                      | 停止指定的BGP会话。                                                                                                                                                                                                                  |

  

## 模板菜单
  

模板包含所有与BGP协议相关的配置选项。可以作为动态对等体的模板，并将类似的配置应用于一组对等体。注意，这与Cisco设备上的对等体组不一样，在Cisco设备上，对等体组不仅仅是一个普通的配置。
  

可用的模板参数列表：


<table class=MsoNormalTable  border=1  cellspacing=0  style="border-collapse:collapse;width:584.2500pt;margin-left:-4.3500pt;
border:none;mso-border-left-alt:0.5000pt solid windowtext;mso-border-top-alt:0.5000pt solid windowtext;
mso-border-right-alt:0.5000pt solid windowtext;mso-border-bottom-alt:0.5000pt solid windowtext;mso-border-insideh:0.5000pt solid windowtext;
mso-border-insidev:0.5000pt solid windowtext;mso-padding-alt:0.7500pt 0.7500pt 0.7500pt 0.7500pt ;" ><tr><td width=391  valign=center  colspan=2  style="width:293.3000pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:1.0000pt solid windowtext;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  align=center  style="mso-pagination:widow-orphan;text-align:center;" ><b><span style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" ><font face="Helvetica" >属性</font></span></b><b><span style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:1.0000pt;" ><o:p></o:p></span></b></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:1.0000pt solid windowtext;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  align=center  style="mso-pagination:widow-orphan;text-align:center;" ><b><span style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" ><font face="Helvetica" >说明</font></span></b><b><span style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:1.0000pt;" ><o:p></o:p></span></b></p></td></tr><tr><td width=391  valign=center  colspan=2  style="width:293.3000pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >add-path-out</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="15"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >all | none</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td></tr><tr><td width=391  valign=center  colspan=2  style="width:293.3000pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >address-families</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="15"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >ip | ipv6 | l2vpn | l2vpn-cisco | vpnv4</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default:&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >ip</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >)</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >该对等体将交换路由信息的地址族列表。远程对等体必须支持（通常是支持）</font>BGP功能的可选参数，以协商IP以外的任何其他族。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td width=391  valign=center  colspan=2  style="width:293.3000pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >as</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="15"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >integer [0..4294967295]</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >32位BGP自治系统编号。值可以用AS-Plain和AS-Dot格式输入。该参数还用于设置BGP邦联，格式如下：&nbsp;</span><span class="15"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >confederation_as/as</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >。例如，如果</font>AS是34，联盟AS是43，那么作为配置应该是as=43/34。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td width=391  valign=center  colspan=2  style="width:293.3000pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >as-override</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="15"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >yes| no</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default:&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >no</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >)</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >如果设置了，那么在向该对等体发送路由更新之前，</font>BGP AS-PATH属性中的所有远程对等体的AS号都会被替换为本地AS号。这发生在路由过滤和预处理之前。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td width=391  valign=center  colspan=2  style="width:293.3000pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >cisco-vpls-nlri-len-fmt</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="15"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >auto-bits | auto-bytes| bits| bytes</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >VPLS NLRI长度格式类型。用于与Cisco VPLS兼容。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td width=391  valign=center  colspan=2  style="width:293.3000pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >cluster-id</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="15"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >IP address</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >如果这个实例是一个路由反射器：这个实例所属的路由器反射器集群的集群</font>ID。这个属性有助于识别来自本集群中另一个路由反射器的路由更新，避免路由信息的循环。注意，通常一个集群中只有一个路由反射器；在这种情况下，不需要配置 'cluster-id'，而是使用BGP路由器的ID。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td width=391  valign=center  colspan=2  style="width:293.3000pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >disabled</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="15"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >yes | no</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default:&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >no</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >)</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >模板是否被禁用。</font></span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td width=391  valign=center  colspan=2  style="width:293.3000pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >hold-time</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="15"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >time[3s..1h] | infinity</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default:&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >3m</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >)</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >指定与对等体协商时要使用的</font>BGP保持时间值。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><br></span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >根据</font>BGP规范，如果路由器在&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >OPEN</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;消息的保持时间字段中指定的时间内没有收到连续的&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >KEEPALIVE</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;和&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >UPDATE</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;和&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >NOTIFICATION</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;消息，那么与对等体的BGP连接将被关闭。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><br></span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >将实际使用两个对等体的最小保持时间值（注意，特殊值</font>0或 "无穷大 "低于任何其他值）</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><br></span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >- infinity - 永远不会使连接过期，也不会发送keepalive消息。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td width=391  valign=center  colspan=2  style="width:293.3000pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >input</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;- 一组与BGP输入相关的参数</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td></tr><tr><td width=301  valign=center  style="width:226.2500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td width=89  valign=center  style="width:67.0500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.accept-comunities</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="15"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >string</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:1.0000pt solid windowtext;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >一个快速的方法来过滤传入的特定社区的更新。允许在传入的信息被解析并存储在内存中之前直接过滤，这样可以大大减少内存的使用。常规的输入过滤链只能拒绝前缀，这意味着它仍然会占用内存，并在</font>/routing路由表中显示为 "未激活，已过滤"。要应用的变化需要会话刷新。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td width=301  valign=center  style="width:226.2500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td width=89  valign=center  style="width:67.0500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.accept-ext-communities</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >(</span><span class="15"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >string</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >一种快速的方法来过滤进入的特定扩展社区的更新。允许在传入的消息被解析并存储在内存中之前直接过滤，这样可以大大减少内存的使用。常规的输入过滤链只能拒绝前缀，这意味着它仍然会占用内存，并在</font>/routing路由表中显示为 "未激活，已过滤"。要应用的变化需要会话刷新。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td width=301  valign=center  style="width:226.2500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td width=89  valign=center  style="width:67.0500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.accept-large-comunities</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="15"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >string</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >一个快速的方法来过滤传入的特定大型社区的更新。允许在传入的信息被解析并存储在内存中之前直接过滤，这样可以大大减少内存的使用。常规的输入过滤链只能拒绝前缀，这意味着它仍然会占用内存，并在</font>/routing路由表中显示为 "未激活，已过滤"。要应用的变化需要会话刷新。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td width=301  valign=center  style="width:226.2500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td width=89  valign=center  style="width:67.0500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.accept-nlri</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >(</span><span class="15"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >string</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >ipv4/6地址列表的名称。一种快速的方法来过滤带有特定NLRI的传入更新。可以在传入的消息被解析并存储在内存中之前直接过滤，这样可以大大减少内存的使用。常规的输入过滤链只能拒绝前缀，这意味着它仍然会占用内存，并在/routing路由表中显示为 "未激活，已过滤"。要应用的变化需要重新启动会话。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td width=301  valign=center  style="width:226.2500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td width=89  valign=center  style="width:67.0500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.accept-unknown</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >(</span><span class="15"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >string</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >一种快速的方法来过滤带有特定</font> "未知 "属性的传入更新。允许在传入的消息被解析并存储在内存中之前直接过滤，这样可以大大减少内存的使用。常规的输入过滤链只能拒绝前缀，这意味着它仍然会占用内存，并在/routing路由表中显示为 "未激活，已过滤"。要应用的变化需要会话刷新。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td width=301  valign=center  style="width:226.2500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td width=89  valign=center  style="width:67.0500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.affinity</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >(afi &nbsp;| alone | instance | main | remote-as | vrf; Default: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >配置输入多核处理。在</font>&nbsp;</span><span style="font-family:Helvetica;color:rgb(0,136,204);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><a href="https://help.mikrotik.com/docs/display/ROS/Routing+Protocol+Multi-core+Support" ><font face="Helvetica" >路由协议多核支持</font></a></span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;文章中阅读更多内容。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><br></span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >-&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >alone</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;- 每个会话的输入和输出都在自己的进程中处理，当有很多内核和很多对等体时，这很可能是最佳选择。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><br></span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >-&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >afi, instance, vrf, remote-as</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;- 尝试在具有类似参数的进程中运行新会话的输入/输出。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><br></span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >-&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >main</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;- 在主进程中运行输入/输出（可能会提高单核的性能，甚至可能在具有少量内核的多核设备上）。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><br></span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >-&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >input</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;- 在与输入相同的进程中运行输出（可以只为输出亲和力设置）。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td width=301  valign=center  style="width:226.2500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td width=89  valign=center  style="width:67.0500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.allow-as</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="15"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >integer [0..10]</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >表示在</font>AS-PATH中允许自己的AS号码出现多少次，然后再丢弃一个前缀。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr><tr><td width=301  valign=center  style="width:226.2500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p>&nbsp;</o:p></span></p></td><td width=89  valign=center  style="width:67.0500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp; &nbsp; &nbsp;&nbsp;</span><b style="mso-bidi-font-weight:normal" ><span class="17"  style="font-family:Helvetica;color:rgb(0,0,0);letter-spacing:0.0000pt;
mso-ansi-font-weight:bold;text-transform:none;font-style:normal;
font-size:12.0000pt;mso-font-kerning:0.0000pt;" >.filter</span></b><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >&nbsp;(</span><span class="15"  style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >name</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" >; Default: )</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td><td width=387  valign=center  style="width:290.9500pt;padding:4.5000pt 9.7500pt 4.5000pt 9.7500pt ;border-left:1.0000pt solid windowtext;
mso-border-left-alt:0.5000pt solid windowtext;border-right:1.0000pt solid windowtext;mso-border-right-alt:0.5000pt solid windowtext;
border-top:none;mso-border-top-alt:0.5000pt solid windowtext;border-bottom:1.0000pt solid windowtext;
mso-border-bottom-alt:0.5000pt solid windowtext;background:rgb(255,255,255);" ><p class=MsoNormal  style="mso-pagination:widow-orphan;text-align:left;" ><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:0.0000pt;" ><font face="Helvetica" >输入前缀的路由过滤链的名称。这发生在</font>NLRIs被处理之后。如果没有指定链，那么BGP默认接受一切。</span><span style="font-family:Helvetica;color:rgb(51,51,51);letter-spacing:0.0000pt;
text-transform:none;font-style:normal;font-size:12.0000pt;
mso-font-kerning:1.0000pt;" ><o:p></o:p></span></p></td></tr></table>


# 最佳路径选择

BGP路由器可以从多个供应商那里收到多份全局路由表。

应该有一些方法来比较这些多个BGP路由表，并选择通往目的地的最佳路由，解决方案就是BGP最佳路径选择算法。

只有当路由是有效的，该算法才会对其进行评估。一般来说，在以下情况下，该路由被认为是有效的：

- 路由的NEXT_HOP是有效的和可到达的
- 从外部对等体收到的AS_PATH不包含本地AS
- 该路由没有被路由过滤器拒绝

更多信息请阅读 [节点选择和验证](https://wiki.mikrotik.com/wiki/Manual:BGP_nexthop_selection_and_validation_in_RouterOS_3.x "Manual:BGP nexthop selection and validation in RouterOS 3.x")

最佳路径算法还比较了仅由 **个BGP实例** 收到的路由。由不同BGP实例安装的路由通过一般算法进行比较，即比较路由距离，优先选择距离较小的路由。

如果所有的标准都满足，就会采取以下行动：

1.  收到的第一条路径自动被认为是 "最佳路径"。任何进一步收到的路径将与第一个收到的路径进行比较，以确定新的路径是否更好。
2.  优先选择具有最高权重的路径。 
    这个参数不是BGP标准的一部分，它的发明是为了快速在本地选择最佳路径。参数是路由器的本地参数（在BGP输入中用路由过滤器分配），不能被公布。没有分配WEIGHT的路由，其默认值为0。
3.  优先选择具有最高 **LOCAL_PREF** 的路径。 
    这个属性只在一个AS内使用。没有LOCAL_PREF属性的路径，默认值为100。
4.  优先选择具有最短 **AS_PATH** 的路径。(如果 `input.ignore-as-path-len` 设置为 **yes**，则跳过)。 
    每个AS_SET算作1，与集合的大小无关。AS_CONFED_SEQUENCE和AS_CONFED_SET不包括在AS_PATH长度内。
5.  优先选择通过聚合或BGP网络在本地产生的路径
6.  优先选择具有最低 **ORIGIN** 类型的路径。
    
    内部网关协议（IGP）低于外部网关协议（EGP），而EGP低于INCOMPLETE
    
    换言之，**IGP < EGP < INCOMPLETE**。
7.  优先选择具有最低 **多出口判别器** （MED）的路径。
    
    路由器只对具有相同相邻（最左）AS的路径比较MED属性。没有明确MED值的路径以MED为0处理。
    
8.  优先选择 **eBGP** 而不是 **iBGP** 路径
9.  优先选择来自具有最低 **路由器ID** 的BGP路由器的路由。如果路由带有 **ORIGINATOR_ID** 属性，则使用 **ORIGINATOR_ID** 而不是路由器ID。
10.  优先选择具有最短的 **路由反射集群列表** 的路由。没有群集列表的路由被认为具有长度为0的群集列表。
11.  优先选择来自最低邻居地址的路径

  

# 路由过滤器注意事项

在BGP输出时，路由过滤器在BGP本身修改属性之前执行，例如，如果 `nexthop-choice` 被设置为 `force-self`，那么路由过滤器中设置的网关将被覆盖掉。

在BGP输入中，路由过滤器被应用于接收到的属性，这意味着，例如，无论 `nexhop-choice` 的值是什么，设置网关都会起作用。

# 运行一个以上的实例

为了使最佳路径选择正常工作，BGP路由必须从同一个实例接收。但在某些情况下，有必要运行多个BGP实例，并有各自独立的表。 
BGP通过比较配置的本地路由器ID来确定会话是否属于同一实例。 
  
例如，下面的配置将在自己的BGP实例中运行每个对等体

```shell
/routing/bgp/connection
add name=inst1_peer remote.address=192.168.1.1 as=1234 local.role=ebgp router-id=1.1.1.1
add name=inst2_peer remote.address=192.168.1.2 as=5678 local.role=ebgp router-id=2.2.2.2
```
  
当没有指定 "router-id"时，BGP将从"/routing id "中挑选 "默认 "ID。

  

## VPLS

**Sub Menu:** `/routing/bgp/vpls`

该菜单列出了所有配置的基于BGP的VPLS实例。这些实例允许路由器公布VPLS BGP NLRI，并表明路由器属于特定的客户VPLS网络。

基于MP-BGP的自动发现和信令（RFC 4761）。

基于Cisco VPLS BGP的自动发现（草案-ietf-l2vpn-signaling-08）。

支持基于BGP的VPLS的多个导入导出路由目标扩展社区（两者，RFC 4761和draft-ietf-l2vpn-signaling-08）。

| 属性                                                  | 说明                                                                                                                                                                                                                                                                                                                                                                                                |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **bridge** (_name_)                                   | 动态创建的VPLS接口应添加为端口的网桥名称。                                                                                                                                                                                                                                                                                                                                                          |
| **bridge-cost** (_integer [0..4294967295]_)           |
|                                                       |
| **bridge-horizon** (_none\| integer [0..4294967295]_) | 如果设置为无，则不使用桥接水平线。                                                                                                                                                                                                                                                                                                                                                                  |
| **cisco-id** ()                                       | 唯一标识符。必须为cisco风格的VPLS信令设置一个参数。在大多数情况下，不应该使用这个参数，任何现代软件都支持RFC 4761风格的信令（见site-id参数）。参数是l2-router-id和RD的合并，例如：10.155.155.1&6550:123                                                                                                                                                                                             |
| **comment** (_string_)                                | 项目的简短描述                                                                                                                                                                                                                                                                                                                                                                                      |
| **disabled** (_yes                            \| no_) | 定义一个项目是被忽略还是被使用。                                                                                                                                                                                                                                                                                                                                                                    |
| **export-route-target** (list of RTs)                 | 该设置用一个或多个路由目标来标记BGP NLRI，在远端被 `import-route-targets` 使用。                                                                                                                                                                                                                                                                                                                    |
| **import-route-targets** (_list of RTs_)              | 该设置用于通过比较从BGP NLRI收到的路由目标，确定BGP NLRI是否与某个特定的VPLS有关。                                                                                                                                                                                                                                                                                                                  |
| **local-pref** (_integer[0..4294967295]_)             |                                                                                                                                                                                                                                                                                                                                                                                                     |
| **name** (_string_; Default: )                        |                                                                                                                                                                                                                                                                                                                                                                                                     |
| **pw-control-word** (_default \| disabled\| enabled_) | 启用禁用控制词的使用。在 [VPLS Control Word](https://help.mikrotik.com/docs/display/ROS/VPLS+Control+Word) 文章中阅读更多内容。                                                                                                                                                                                                                                                                     |
| **pw-l2mtu** (_integer[32..65535]_)                   | 通告中的伪MTU值。                                                                                                                                                                                                                                                                                                                                                                                   |
| **pw-type** (_raw-ethernet\| tagged-ethernet\| vpls_) | 该参数从v5.16开始可用。允许在NLRI中选择公布的封装方式，只用于比较。它并不影响隧道的功能。 [见pw-type使用例子](https://wiki.mikrotik.com/wiki/Manual:MPLS_L2VPN_vs_Juniper "Manual:MPLS L2VPN vs Juniper")                                                                                                                                                                                           |
| **rd** (_string_)                                     | 指定附加在VPLS NLRI上的值，以便接收的路由器能够区分可能看起来相同的通告。这意味着必须为每个VPLS使用一个独特的路由区分器。没有必要在所有路由器上为某些VPLS使用相同的路由区分器，因为区分器不用于确定某些BGP NLRI是否与特定的VPLS有关（路由目标属性用于此），但必须为不同的VPLS设置不同的区分器。接受3种类型的格式。[阅读更多](https://help.mikrotik.com/docs/display/ROS/BGP#BGP-RouteDistinguisher) |
| **site-id** (_integer [0..65535]_)                    | 唯一的网站标识符。每个站点必须有一个唯一的站点ID。必须为RFC 4761风格的VPLS信令设置一个参数。                                                                                                                                                                                                                                                                                                        |
| **vrf** (_name_)                                      | VRF表名称。                                                                                                                                                                                                                                                                                                                                                                                         |

## VPN

**Sub Menu:** `/routing/bgp/vpn`

### Route Distinguisher

路由区分器是一个64位的整数，分为三个部分：类型（2个字节）、管理员和值。

目前，有三种格式类型的定义。

| **2bytes** | 2bytes     | 2bytes      | 2bytes |
| ---------- | ---------- | ----------- | ------ |
| **Type1**  | ASN        | 4byte value |
| **Type2**  | 4-byte IP  | value       |
| **Type3**  | 4-byte ASN | value       |



### 属性

<table style="border: 1px solid #000000" class="relative-table wrapped confluenceTable" style="width: 87.14969%;"><colgroup class=""><col class="" style="width: 5.313653%;"><col class="" style="width: 28.413284%;"><col class="" style="width: 66.199265%;"></colgroup><tbody class=""><tr><td style="border: 1px solid #000000" class="highlight-#f4f5f7 confluenceTd" colspan="2" data-highlight-colour="#f4f5f7"><strong>disabled</strong><span>&nbsp;</span>(<em>yes | no</em>)</td><td style="border: 1px solid #000000" class="highlight-#f4f5f7 confluenceTd" data-highlight-colour="#f4f5f7"><br></td></tr><tr class=""><td style="border: 1px solid #000000" class="highlight-#deebff confluenceTd" colspan="3" data-highlight-colour="#deebff"><strong>export</strong> - 一组与vpnv4出口相关的参数。</td></tr><tr class=""><td style="border: 1px solid #000000" rowspan="4" class="confluenceTd"><br><br><br></td><td style="border: 1px solid #000000" class="highlight-#f4f5f7 confluenceTd" data-highlight-colour="#f4f5f7"><strong title="">.filter-chain</strong><span title="">&nbsp;</span>(<em>name</em>)</td><td style="border: 1px solid #000000" class="highlight-#f4f5f7 confluenceTd" data-highlight-colour="#f4f5f7">路由过滤链的名称，用于在输出前过滤前缀。</td></tr><tr class=""><td style="border: 1px solid #000000" class="confluenceTd"><strong title="">.filter-select</strong>(<em>name</em>)</td><td class="confluenceTd">选择过滤器链的名称，用于选择要导出的前缀导出。</td></tr><tr class=""><td style="border: 1px solid #000000" class="highlight-#f4f5f7 confluenceTd" data-highlight-colour="#f4f5f7"><strong title="">.redistribute</strong>(<em title="">bgp | connected | dhcp | fantasy | modem | ospf | rip | static | vpn</em>)</td><td style="border: 1px solid #000000" class="highlight-#f4f5f7 confluenceTd" data-highlight-colour="#f4f5f7">启用从VRF到VPNv4的指定路由类型的再分配。</td></tr><tr class=""><td style="border: 1px solid #000000" class="confluenceTd"><strong title="">.route-targets</strong>(<em>rt[,rt]</em>)</td><td style="border: 1px solid #000000" class="confluenceTd">输出VPNv4路由时添加的路由目标列表。接受的RT格式与路由区分器的格式类似。</td></tr><tr><td style="border: 1px solid #000000" class="highlight-#deebff confluenceTd" colspan="3" data-highlight-colour="#deebff"><strong>import</strong> - 一组与vpnv4导入相关的参数。</td></tr><tr><td style="border: 1px solid #000000" rowspan="3" class="confluenceTd"><br></td><td style="border: 1px solid #000000" class="highlight-#f4f5f7 confluenceTd" data-highlight-colour="#f4f5f7"><strong title="">.filter-chain</strong><span title="">&nbsp;</span>(<em>name</em>)</td><td style="border: 1px solid #000000" class="highlight-#f4f5f7 confluenceTd" data-highlight-colour="#f4f5f7">路由过滤链的名称，用于在导入时过滤前缀。</td></tr><tr><td style="border: 1px solid #000000" class="confluenceTd"><strong title="">.route-targets</strong>(<em>rt[,rt]</em>)</td><td style="border: 1px solid #000000" class="confluenceTd">将用于导入VPNv4路由的路由目标列表。接受的RT格式与路由区分器的格式类似。</td></tr><tr><td style="border: 1px solid #000000" class="highlight-grey confluenceTd" data-highlight-colour="grey" title="Background colour : "><strong title="">.router-id</strong>(<em>name | ip</em>)</td><td style="border: 1px solid #000000" class="confluenceTd">将用于BGP最佳路径选择算法的BGP实例的路由器ID。</td></tr><tr><td style="border: 1px solid #000000" colspan="2" class="confluenceTd"><strong title=""><strong>label-allocation-policy</strong></strong>&nbsp;(<em>per-prefix | per-vrf</em>)</td><td style="border: 1px solid #000000" class="confluenceTd"><br></td></tr><tr><td colspan="2" style="border: 1px solid #000000" class="confluenceTd"><strong title=""><strong>name</strong></strong></td><td style="border: 1px solid #000000" class="confluenceTd"><br></td></tr><tr><td style="border: 1px solid #000000" colspan="2" class="confluenceTd"><strong title=""><strong>route-distinguisher<span>&nbsp;</span></strong></strong>(rd)</td><td style="border: 1px solid #000000" class="confluenceTd">有助于区分来自多个VRF的重叠路由。每个VRF应该是唯一的。接受3种类型的格式。 <a href="https://help.mikrotik.com/docs/display/ROS/BGP#BGP-RouteDistinguisher">阅读更多&gt;&gt;</a></td></tr><tr><td style="border: 1px solid #000000" colspan="2" class="confluenceTd"><strong title=""><strong>vrf<span title="">&nbsp;</span></strong></strong>(<em title="">name</em>)</td><td style="border: 1px solid #000000" class="confluenceTd">该VPN实例将使用的VRF表的名称。</td></tr></tbody></table>