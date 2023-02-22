# 在两个无线链路上绑定EoIP隧道

这是把多个网络接口聚合到一个管道的例子。特别展示了如何聚合多个虚拟（EoIP）接口获得最大吞吐量（MT），并强调了可用性。

## 网络图

两个路由器R1和R2通过多跳无线链路相互连接。两边的无线接口都有IP地址。

![](https://help.mikrotik.com/docs/download/attachments/132349985/Bonding_ARP_Monitoring_Exam.jpg?version=1&modificationDate=1655272825695&api=v2)

## 开始使用

绑定只能用于OSI第二层（以太网级别）的连接。因此需要在每个无线链接上创建EoIP接口。方法如下：

在路由器R1上：

`[admin@MikroTik] > /interface eoip add remote-address =10.0.1.1/24 tunnel-id =1 [admin@MikroTik] > /interface eoip add remote-address =10.0.2.1/24 tunnel-id =2`

在路由器R2上:

`[admin@MikroTik] > /interface eoip add remote-address =10.1.1.1/24 tunnel-id =1 [admin@MikroTik] > /interface eoip add remote-address =10.2.2.1/24 tunnel-id =2`

第二步是添加一个绑定接口，并指定EoIP接口为从机:

R1:

`[admin@MikroTik] > / interface bonding add slaves =eoip-tunnel1,eoip-tunnel2 mode =balance-rr`

R2:

`[admin@MikroTik] > / interface bonding add slaves =eoip-tunnel1,eoip-tunnel2 mode =balance-rr`

最后一步是为绑定接口添加IP地址:

R1:

`[admin@MikroTik] > / ip address add address 192.168.0.1/24 interface =bonding1`

R2:

`[admin@MikroTik] > / ip address add address 192.168.0.2/24 interface =bonding1`

## 测试配置

现在，两台路由器能用192.168.0.0/24网络的地址互相通信。为了验证绑定接口的功能，执行以下操作:

R1:

`[admin@MikroTik] > /interface monitor-traffic eoip-tunnel1,eoip-tunnel2`

R2:

`[admin@MikroTik] > /tool bandwidth-test 192.168.0.1 direction=transmit`

应该看到，流量在两个EoIP接口上被平均分配。:

```shell
[admin@MikroTik] > /int monitor-traffic eoip-tunnel1,eoip-tunnel2             
    received-packets-per-second : 685      685                                
       received-bits-per-second : 8.0Mbps  8.0Mbps                             
        sent-packets-per-second : 21       20                                  
           sent-bits-per-second : 11.9kbps 11.0kbps                            
    received-packets-per-second : 898      899                                 
       received-bits-per-second : 10.6Mbps 10.6Mbps                            
        sent-packets-per-second : 20       21                                  
           sent-bits-per-second : 11.0kbps 11.9kbps                            
    received-packets-per-second : 975      975                                 
       received-bits-per-second : 11.5Mbps 11.5Mbps                            
        sent-packets-per-second : 22       22                                  
           sent-bits-per-second : 12.4kbps 12.3kbps                            
    received-packets-per-second : 980      980                                 
       received-bits-per-second : 11.6Mbps 11.6Mbps                            
        sent-packets-per-second : 21       21                                  
           sent-bits-per-second : 11.9kbps 11.8kbps                            
    received-packets-per-second : 977      977                                 
       received-bits-per-second : 11.6Mbps 11.5Mbps                            
        sent-packets-per-second : 21       21                                  
           sent-bits-per-second : 11.9kbps 11.8kbps                          
-- [Q quit|D dump|C-z pause]
```

## 链路监控

很容易注意到，在上面的配置中，只要任何一条链路出现故障，绑定接口的吞吐量就会崩溃。这是因为没有进行链路监控，因此，绑定驱动程序不知道基础链路的问题。在大多数绑定配置中，启用链接监控是必须的。要启用ARP链路监控，请执行以下操作：

R1:

`[admin@MikroTik] > / interface bonding set bonding1 link-monitoring =arp arp-ip-targets =192.168.0.2`

R2:

`[admin@MikroTik] > / interface bonding set bonding1 link-monitoring =arp arp-ip-targets =192.168.0.1`
