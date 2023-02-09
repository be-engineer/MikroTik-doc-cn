# 概述

分析器工具显示RouterOS中运行的每个进程的CPU使用率。有助于确定哪个进程在使用大部分的CPU资源。
可观看 [关于此功能的视频](https://youtu.be/BkRaW14p8_s)。

`[admin@MikroTik] > /tool/profile`。

在多核系统上，该工具允许指定每个核的CPU使用情况。

"CPU "参数允许指定整数，代表一个或两个核心的预定义值 **全部** 和 **总计：**

- total - 设置为显示所有核心使用量的总和。
- all -设置为分别显示每个可用内核的CPU使用情况。

在下面的例子中，可以看一下这两个预定义值。

```shell
[admin@MikroTik] > /tool/profile cpu=all
NAME             CPU        USAGE      
ethernet         1          0%         
kvm              0          0%         
kvm              1          4.5%       
management       0          0%         
management       1          0.5%       
idle             0          100%       
idle             1          93%        
profiling        0          0%         
profiling        1          2%   
 
[admin@MikroTik] > /tool profile cpu=total
NAME             CPU        USAGE      
ethernet         all        0%         
console          all        0%         
kvm              all        2.7%       
management       all        0%         
idle             all        97.2%      
profiling        all        0%         
bridging         all        0%
```

## 分类器

配置文件在几个分类器中对过程进行分类。其中大多数是显而易见的，不需要详细解释。

- backup
- bfd
- bgp
- bridging
- btest
- certificate
- console
- dhcp
- disk
- dns
- dude
- e-mail
- eoip
- ethernet
- fetcher
- firewall
- firewall-mgmt
- flash
- ftp
- gps
- graphing
- gre
- health
- hotspot
- idle
- igmp-proxy
- internet-detect
- ip-pool
- ipsec
- isdn
- kvm
- l2tp
- l7-matcher
- ldp
- logging
- m3p
- management
- mme
- mpls
- networking
- ntp
- ospf
- ovpn
- p2p-matcher
- pim
- ppp
- pppoe
- pptp
- profiling
- queue-mgmt
- queuing
- radius
- radv
- rip
- routing
- serial
- sniffing
- snmp
- socks
- ssh
- ssl
- sstp
- synchronous
- telnet
- tftp
- traffic-accounting
- traffic-flow
- upnp
- usb
- user-manager
- web-proxy
- winbox
- wireless
- www
