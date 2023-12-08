# CAPsMAN VLAN概述

可以为家庭或办公环境创建可扩展到许多接入点的集中式接入点管理设置，这种设置非常容易配置，并在 [简单CAPsMAN设置](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=1409149#APController(CAPsMAN)-SimplesetupofaCAPsMANsystem) 指南中进行了说明，但对于更复杂的设置，可能需要vlan。CAPsMAN具有在特定条件下分配特定VLAN ID的功能。本指南将举例说明如何根据无线客户端所连接的AP为无线报文分配VLAN ID。具有vlan的CAPsMAN可以通过使用 [本地转发模式](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=1409149#APController(CAPsMAN)-LocalForwardingMode) 或 [CAPsMAN转发模式](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=1409149#APController(CAPsMAN)-ManagerForwardingMode) 来实现，本地转发模式将提供在ap和CAPsMAN路由器之间使用交换机来交换数据包的可能性(以实现更大的吞吐量)。而CAPsMAN转发模式应用于所有流量都应始终转发到CAPsMAN路由器(在大多数情况下过滤数据包)。

在本例中，如果无线客户端连接到WiFi_WORK，把所有无线客户端分配到VLAN10，如果无线客户端连接到WiFi_GUEST，把无线客户端分配到VLAN20。用Virtual ap和CAPsMAN为无线客户端创建多个ssid，以便在使用单个物理设备时连接到它们。还将通过使用CAPsMAN配置规则展示如何为单个物理设备使用单个SSID的示例。

# 使用本地转发模式

![](https://help.mikrotik.com/docs/download/attachments/137986075/CAPsMAN_VLANs_local.jpg?version=1&modificationDate=1659444976438&api=v2)

在本地转发模式下，CAPsMAN路由器将配置分发到由CAPsMAN路由器提供的所有cap上。在本地转发模式中，流量不需要发送到CAPsMAN路由器，而是可以在转发流量时发送到不同的路由器，而不涉及CAPsMAN路由器。这种模式允许您在流量从无线客户端发送到您的网络之前将其标记为特定的VLAN ID，这增加了使用交换机将某些VLAN ID限制到某些端口的可能性。在本地转发模式中，流量没有封装在一个特殊的CAPsMAN报头中，这个报头只能由CAPsMAN路由器移除。

## CAPsMAN路由器:

—为每个VLAN配置相应的CAP配置

```shell
/caps-man configuration
add country=latvia datapath.local-forwarding=yes datapath.vlan-id=10 datapath.vlan-mode=use-tag name=Config_WORK security.authentication-types=wpa-psk,wpa2-psk \
    security.passphrase=secret_work_password ssid=WiFi_WORK
add country=latvia datapath.local-forwarding=yes datapath.vlan-id=20 datapath.vlan-mode=use-tag name=Config_GUEST security.authentication-types=\
    wpa-psk,wpa2-psk security.passphrase=secret_guest_password ssid=WiFi_GUEST

```

- 创建一个单一的CAPsMAN配置规则来创建WiFi_WORK和WiFi_GUEST ssid在单个设备上，每个连接的CAP将自动创建这些ssid

```shell
/caps-man provisioning
add action=create-dynamic-enabled master-configuration=Config_WORK slave-configurations=Config_GUEST
```

通过添加多个从配置，可以创建更多的Virtual ap。这需要前面创建的多个CAPsMAN配置。

—出于安全考虑，请将CAPsMAN限制为单个接口

```shell
/caps-man manager interface
set [ find default=yes ] forbid=yes
add disabled=no interface=ether1

```

-   启用CAPsMAN管理器

```
/caps-man manager
set enabled=yes

```

-   为每个VLAN配置DHCP Server

```shell
/interface vlan
add interface=ether1 name=VLAN10 vlan-id=10
add interface=ether1 name=VLAN20 vlan-id=20
/ip address
add address=192.168.10.1/24 interface=VLAN10
add address=192.168.20.1/24 interface=VLAN20
/ip pool
add name=dhcp_pool10 ranges=192.168.10.2-192.168.10.254
add name=dhcp_pool20 ranges=192.168.20.2-192.168.20.254
/ip dhcp-server
add address-pool=dhcp_pool10 disabled=no interface=VLAN10 name=dhcp10
add address-pool=dhcp_pool20 disabled=no interface=VLAN20 name=dhcp20
/ip dhcp-server network
add address=192.168.10.0/24 dns-server=8.8.8.8 gateway=192.168.10.1
add address=192.168.20.0/24 dns-server=8.8.8.8 gateway=192.168.20.1
```

## 交换

在这个例子中使用 [网桥VLAN过滤](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-VLANExample-TrunkandAccessPorts) 来过滤未知的VLAN，并将其他设备分配到相同的网络。 有些设备能够将其卸载到内置的交换芯片，请查看 [基本VLAN交换](https://help.mikrotik.com/docs/display/ROS/Basic+VLAN+switching) 指南，了解如何在不同类型的设备上配置它。

- 设置网桥VLAN过滤

```shell
/interface bridge
add name=bridge1 vlan-filtering=yes
/interface bridge port
add bridge=bridge1 interface=ether1
add bridge=bridge1 interface=ether2
add bridge=bridge1 interface=ether3
add bridge=bridge1 interface=ether4 pvid=10
add bridge=bridge1 interface=ether5 pvid=20
/interface bridge vlan
add bridge=bridge1 tagged=ether1,ether2,ether3 untagged=ether4 vlan-ids=10
add bridge=bridge1 tagged=ether1,ether2,ether3 untagged=ether5 vlan-ids=20
```

在本例中，未标记的流量将用于CAPs和CAPsMAN路由器之间的通信。缺省情况下，如果不更改PVID，则在具有相同PVID值(包括缺省PVID)的端口之间转发无标签流量。

## CAP

- 创建一个桥接并分配一个端口给它，连接到CAPsMAN路由器

```shell
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether1

```

-   在AP上启用CAP模式，并确保指定使用新创建的网桥

```shell
/interface wireless cap
set bridge=bridge1 discovery-interfaces=bridge1 enabled=yes interfaces=wlan1

```

-   CAPs成功连接到CAPsMAN路由器后，wlan1 (SSID WiFi_WORK)和新创建的虚拟wlan5 (SSID WiFi_GUEST)接口将被动态添加为桥接端口。为无线接口分配VLAN，因此，所有来自无线的数据都被标记，只有带有此标记的数据将通过无线发送出去。如果不需要额外的VLAN管理和控制，可以禁用网桥VLAN过滤。关联的VLAN可以通过端口VLAN ID (PVID)属性来查看。

```shell
[admin@CAP_1] /interface bridge port pr
Flags: X - disabled, I - inactive, D - dynamic, H - hw-offload 
 #     INTERFACE                     BRIDGE                    HW  PVID PRIORITY  PATH-COST INTERNAL-PATH-COST    HORIZON
 0   H ether1                        bridge1                   yes    1     0x80         10                 10       none
 1  D  wlan1                         bridge1                         10     0x80         10                 10       none
 2  D  wlan5                         bridge1                         20     0x80         10                 10       none

```

就是这样!把无线客户端连接到ap并检查连通性。

# 使用CAPsMAN转发模式

![](https://help.mikrotik.com/docs/download/attachments/137986075/CAPsMAN_VLANs.jpg?version=1&modificationDate=1659445096063&api=v2)

在CAPsMAN转发模式中，所有来自CAP的流量都被封装在一个特殊的CAPsMAN报头中，这个报头只能被CAPsMAN路由器删除，这意味着交换机将无法区分CAP设置的VLAN ID，因为VLAN标签也将被封装。这种模式限制了在第2层网络中转移流量的可能性，但使您可以通过第3层网络转发来自每个CAP的流量，以便远程CAPsMAN路由器处理流量，当您希望控制远程位置的多个CAP，但希望使用中心网关时，这种模式非常有用。

## CAPsMAN路由器:

- 配置网桥VLAN过滤，将接口限制在相应的VLAN中

```shell
/interface bridge
add name=bridge1 vlan-filtering=yes
/interface bridge port
add bridge=bridge1 interface=ether1 pvid=10
add bridge=bridge1 interface=ether2 pvid=20
/interface bridge vlan
add bridge=bridge1 tagged=bridge1 untagged=ether1 vlan-ids=10
add bridge=bridge1 tagged=bridge1 untagged=ether2 vlan-ids=20

```

CAPsMAN将把CAP接口附加到网桥上，并自动将适当的条目添加到网桥VLAN表中

**注:**  CAPsMAN将把CAP接口附加到网桥上，并自动将适当的表项添加到网桥VLAN表中。该特性从RouterOS v6.43开始可用

—为每个VLAN配置相应的CAP配置

```shell
/caps-man configuration
add country=latvia datapath.bridge=bridge1 datapath.vlan-id=10 datapath.vlan-mode=use-tag name=Config_WORK security.authentication-types=wpa-psk,wpa2-psk \
    security.passphrase=secret_work_password ssid=WiFi_WORK
add country=latvia datapath.bridge=bridge1 datapath.vlan-id=20 datapath.vlan-mode=use-tag name=Config_GUEST security.authentication-types=wpa-psk,wpa2-psk \
    security.passphrase=secret_guest_password ssid=WiFi_GUEST

```

- 创建一个CAPsMAN配置规则来在单个设备上创建WiFi_WORK和WiFi_GUEST ssid，每个连接CAP将自动创建这些ssid

```shell
/caps-man provisioning
add action=create-dynamic-enabled master-configuration=Config_WORK slave-configurations=Config_GUEST
```

通过添加多个从配置，可以创建更多的Virtual ap。这需要前面创建的多个CAPsMAN配置。

- 出于安全考虑，建议将CAPsMAN限制为接口。cap将被连接到哪里？

```shell
/caps-man manager interface
set [ find default=yes ] forbid=yes
add disabled=no interface=ether3
add disabled=no interface=ether4

```

- 启用CAPsMAN管理器

```
/caps-man manager
set enabled=yes

```

- 为每个VLAN配置DHCP Server

```shell
/interface vlan
add interface=bridge1 name=VLAN10 vlan-id=10
add interface=bridge1 name=VLAN20 vlan-id=20
/ip address
add address=192.168.10.1/24 interface=VLAN10
add address=192.168.20.1/24 interface=VLAN20
/ip pool
add name=dhcp_pool10 ranges=192.168.10.2-192.168.10.254
add name=dhcp_pool20 ranges=192.168.20.2-192.168.20.254
/ip dhcp-server
add address-pool=dhcp_pool10 disabled=no interface=VLAN10 name=dhcp10
add address-pool=dhcp_pool20 disabled=no interface=VLAN20 name=dhcp20
/ip dhcp-server network
add address=192.168.10.0/24 dns-server=8.8.8.8 gateway=192.168.10.1
add address=192.168.20.0/24 dns-server=8.8.8.8 gateway=192.168.20.1
```

## CAPs

-  在每个AP上使能CAP模式，指定连接到CAPsMAN路由器的接口

```
/interface wireless cap set discovery-interfaces=ether1 enabled=yes interfaces=wlan1

```

-  CAPsMAN路由器与CAPs连接成功后，将在CAPsMAN路由器上动态创建两个CAP接口。由于显式地选择具有数据路径的桥接接口，这两个接口将作为桥接端口动态地添加到同一个CAPsMAN路由器上。bridge=bridge1，使用默认的CAPsMAN转发模式datapath.local-forwarding=no。由于使用已启用VLAN过滤的网桥，两个CAP接口也将显示在网桥VLAN表中。

```shell
[admin@CAPsMAN_Router] /interface bridge port print
Flags: X - disabled, I - inactive, D - dynamic, H - hw-offload 
 #     INTERFACE                       BRIDGE                      HW  PVID PRIORITY  PATH-COST INTERNAL-PATH-COST    HORIZON
 0     ether1                          bridge1                     yes   10     0x80         10                 10       none
 1     ether2                          bridge1                     yes   20     0x80         10                 10       none
 2  D  cap16                           bridge1                           10     0x80         10                 10       none
 3  D  cap17                           bridge1                           20     0x80         10                 10       none
[admin@CAPsMAN_Router] /interface bridge vlan print
Flags: X - disabled, D - dynamic 
 #   BRIDGE                         VLAN-IDS  CURRENT-TAGGED                         CURRENT-UNTAGGED                        
 0 D bridge1                        1                                                bridge1                                 
 1   bridge1                        10        cap16                                  ether1                                  
 2   bridge1                        20        cap17                                  ether2  

```

就是这样!把无线客户端连接到ap并检查连通性。

# 案例研究

## 没有虚拟ap

并不是每个人都想创建虚拟ap，因为这会降低总吞吐量。如果您希望使用多个设备创建多个ssid，那么可以根据其标识在CAP上分配特定的配置。要实现这一点，您应该使用CAPsMAN配置规则和RegEx表达式。在本例中，把 **Config_WORK** 配置分配给具有身份设置为 **AP_WORK_** 的CAPs，把 **Config_GUEST** 配置分配给具有身份设置为 **AP_GUEST_** 的CAPs。为此只需要更改CAPsMAN规则。

- 删除所有现有的发放规则

```
/caps-man provisioning remove [f]

```

- 创建新的供应规则，根据CAP的标识为其分配适当的配置

```shell
/caps-man provisioning
add action=create-dynamic-enabled identity-regexp=^AP_GUEST_ master-configuration=Config_GUEST
add action=create-dynamic-enabled identity-regexp=^AP_WORK_ master-configuration=Config_WORK
```

不要忘记在cap上设置适当的标识，因为CAPsMAN将根据它的标识在ap上分配适当的配置。