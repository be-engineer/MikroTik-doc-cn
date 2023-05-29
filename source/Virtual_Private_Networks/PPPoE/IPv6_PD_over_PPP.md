# 概述

本示例介绍PPPoE server和client使用IPv6 Prefix Delegation的配置过程。

IPv6前缀可以通过PPP接口进行委派。当客户端连接时，PPP会自动添加动态 [DHCPv6-PD服务器](https://help.mikrotik.com/docs/display/ROS/DHCP#DHCP-DHCPv6Server) 。这允许在PPP接口上运行DHCPv6客户端。

## 配置

## 服务器

使用“PPP配置文件”下的dhcpv6-pd-pool参数开启PPP- pd功能。PPP将使用指定的 [IPv6池](https://help.mikrotik.com/docs/display/ROS/IP+Pools#IPPools-IPv6Pool) 创建动态DHCP服务器。

因此，第一步是添加IPv6池:

`/ipv6 pool
add name=myPool prefix=2001:db8:7501:ff00::/60 prefix-length=62`

现在可以配置PPP配置文件并添加PPPoE服务器

```shell
/ppp profile set default dhcpv6-pd-pool=myPool
 
/interface pppoe-server server
add service-name=test interface=ether1
```

## 客户端

在客户端需要建立PPPoE客户端接口，并在其上运行DHCP客户端。

```shell
/interface pppoe-client
add name=client-test interface=ether1 user=a1 service-name=test
 
/ipv6 dhcp-client
add interface=client-test pool-name=ppp-test pool-prefix-length=64
```

## 测试状态

在服务器端检查是否添加了动态DHCP服务器，是否为特定客户端绑定了前缀。

```shell
[admin@RB1100] /ipv6 dhcp-server> print
Flags: D - dynamic, X - disabled, I - invalid
 #    NAME              INTERFACE            ADDRESS-POOL            LEASE-TIME
 0 D  <pppoe-a1>        <pppoe-a1>           myPool                  3d       
 
[admin@RB1100] /ipv6 dhcp-server binding> print
Flags: X - disabled, D - dynamic
 #   ADDRESS                                        DU       IAID SER.. STATUS
 1 D 2001:db8:7501:ff04::/62                                  247 <pp.. bound 
```

在客户端，检查DHCP客户端是否绑定，池是否添加:

```shell
[admin@x86-test] /ipv6 dhcp-client> print
Flags: D - dynamic, X - disabled, I - invalid
 #    INTERFACE           STATUS        PREFIX                            EXPIRES-AFTER 
0    client-test          bound         2001:db8:7501:ff04::/62           2d23h18m17s 
 
[admin@x86-test] /ipv6 pool> print
Flags: D - dynamic
 #   NAME                        PREFIX                                   PREFIX-LENGTH
 0 D ppp-test                    2001:db8:7501:ff04::/62                             64
```