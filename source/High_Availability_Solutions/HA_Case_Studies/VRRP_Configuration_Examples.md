# VRRP基本设置

基本的VRRP配置例子。

注意事项

建议对所有具有相同VRID的设备使用相同版本的RouterOS来实现VRRP。

![](https://help.mikrotik.com/docs/download/attachments/128221211/Vrrp-simple%20%281%29.jpg?version=1&modificationDate=1659607942284&api=v2)

根据这个配置，只要主站R1是正常的，所有指向外部网络的流量都会引导到R1。一旦R1发生故障，R2就会作为主站接管，并处理转发到与IP（R1）相关的接口数据包。在这个设置中，路由器 "R2 "在备份期间是完全空闲的。

## 配置

R1 配置:

`/ip address add address =192.168.1.10/24 interface =ether1`

`/interface vrrp add interface =ether1 vrid =49 priority =254`

`/ip address add address =192.168.1.1/32 interface =vrrp1`

R2 配置:

`/ip address add address =192.168.1.20/24 interface =ether1`

`/interface vrrp add interface =ether1 vrid =49`

`/ip address add address =192.168.1.1/32 interface =vrrp1`

## 测试

首先，检查两个路由器的VRRP接口标志是否正确。在路由器R1上应该是这样的

```shell
/interface vrrp print detail
 0   RM name = "vrrp1" mtu =1500 mac-address =00:00:5E:00:01:31 arp =enabled interface =ether1 vrid =49
        priority =254 interval =1 preemption-mode =yes authentication =none password = "" on-backup = ""
        on-master = "" version =3 v3-protocol =ipv4
```

路由器R2上:

```shell
/interface vrrp print detail
 0    B name = "vrrp1" mtu =1500 mac-address =00:00:5E:00:01:31 arp =enabled interface =ether1 vrid =49
        priority =100 interval =1 preemption-mode =yes authentication =none password = ""
        on-backup = "" on-master = " version =3 v3-protocol =ipv4
```

可以看到两个路由器上的VRRP接口MAC地址是相同的。现在要检查VRRP是否正常工作，尝试从客户端ping虚拟地址并检查ARP条目:

`[admin@client] > / ping 192.168.1.1`

`192.168.1.254 64 byte ping : ttl=64 time=10 ms`

`192.168.1.254 64 byte ping : ttl=64 time=8 ms`

`2 packets transmitted, 2 packets received, 0% packet loss`

`round-trip min /avg/max = 8/9.0/10 ms`

`[admin@client] /ip arp> print`

`Flags : X - disabled, I - invalid, H - DHCP, D - dynamic`

 `...`

 `1 D 192.168.1.1   00 :00:5E:00:01:31 bridge1`

现在拔掉路由器R1上的ether1电缆。R2将成为VRRP主站，客户端的ARP表不会改变，但流量将开始在R2路由器上流动。

如果VRRP和反向路径过滤一起使用，那么建议把 `rp-filter` 设置为 `loose`，否则，VRRP接口可能无法到达。

## 负载共享

在基本配置例子中，R2在备份状态下是完全空闲的。可能会认为是对宝贵资源的浪费。在这种情况下，R2路由器可以设置为一些客户的网关。 
这种配置的明显优势是建立了一个负载共享方案。但R2路由器没有受到当前VRRP设置的保护。 
为了使设置工作，需要两个虚拟路由器。

![](https://help.mikrotik.com/docs/download/attachments/128221211/Vrrp-load-sharing.jpg?version=1&modificationDate=1653990835746&api=v2)

V1虚拟路由器的配置和基本例子中的配置相同-R1是主路由器，R2是备份路由器。在V2中，主站是R2，备份是R1。 
通过这种配置在R1和R2之间建立了负载共享；此外，让两个路由器互相作为备份来创建一个保护设置。

## 配置

R1 配置:

`/ip address add address =192.168.1.1/24 interface =ether1`

`/interface vrrp add interface =ether1 vrid =49 priority =254`

`/interface vrrp add interface =ether1 vrid =77`

`/ip address add address =192.168.1.253/32 interface =vrrp1`

`/ip address add address =192.168.1.254/32 interface =vrrp2`

R2 配置:

`/ip address add address =192.168.1.2/24 interface =ether1`

`/interface vrrp add interface =ether1 vrid =49`

`/interface vrrp add interface =ether1 vrid =77 priority =254`

`/ip address add address =192.168.1.253/32 interface =vrrp1`

`/ip address add address =192.168.1.254/32 interface =vrrp2`

## VRRP无抢占模式

每次当有较高优先级的路由器可用时，它就会成为主路由器。有时这不是想要的行为，可以通过在VRRP配置中设置 `preemption-mode=no` 来关闭。

## 配置

使用和基本例子相同的设置。唯一的区别是在配置中设置preemption-mode=no。可以通过修改现有配置完成:

`/interface vrrp set [find] preemption-mode =no`

## 测试

尝试关闭R1路由器，R2将成为主路由器，因为它在可用的路由器中拥有最高优先级。

现在打开R1路由器，你会看到R2路由器继续成为主站，即使R1的优先级更高。
