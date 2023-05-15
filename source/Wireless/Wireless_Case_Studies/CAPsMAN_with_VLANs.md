# Summary

It is possible to create a centralized Access Point management setup for a home or office environment that is scalable to many Access Points, such a setup is quite easy to configure and has been explained in the [Simple CAPsMAN setup](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=1409149#APController(CAPsMAN)-SimplesetupofaCAPsMANsystem) guide, but for more complex setups VLANs might be required. CAPsMAN has the functionality to assign a certain VLAN ID under certain conditions. This guide will provide an example on how to assign a VLAN ID to Wireless packets based on the AP, to which a wireless client connects to. CAPsMAN with VLANs can be achieved either by using [Local Forwarding Mode](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=1409149#APController(CAPsMAN)-LocalForwardingMode) or [CAPsMAN Forwarding Mode](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=1409149#APController(CAPsMAN)-ManagerForwardingMode), the Local Forwarding Mode will provide the possibility to use a switch between your APs and CAPsMAN router to switch packets (to achieve larger throughput), while CAPsMAN Forwarding Mode should be used when all traffic should always be forwarded to the CAPsMAN router (in most cases to filter packets).

In this example, we are going to assign all our Wireless clients to **VLAN10**, if they connect to **WiFi\_WORK**, and going to assign Wireless clients to **VLAN20**, if they connect to **WiFi\_GUEST**. We are going to use Virtual APs along with CAPsMAN to create multiple SSIDs for our Wireless clients to connect to while using a single physical device. An example of how to use a single SSID for a single physical device will also be shown by using CAPsMAN provisioning rules.

# Using Local Forwarding Mode

![](https://help.mikrotik.com/docs/download/attachments/137986075/CAPsMAN_VLANs_local.jpg?version=1&modificationDate=1659444976438&api=v2)

In Local Forwarding Mode, the CAPsMAN router is distributing the configuration across all CAPs that are being provisioned by the CAPsMAN router. In Local Forwarding Mode traffic is not required to be sent to the CAPsMAN router, rather it can be sent to a different router without involving the CAPsMAN router when forwarding traffic. This mode allows you to tag traffic to a certain VLAN ID before it is sent to your network from your Wireless client, which adds the possibility to use a switch to limit certain VLAN IDs to certain ports. In Local Forwarding Mode traffic is not encapsulated with a special CAPsMAN header, which can only be removed by a CAPsMAN router.

## CAPsMAN Router:

-   Create appropriate CAP configurations for each VLAN

```
/caps-man configuration
add country=latvia datapath.local-forwarding=yes datapath.vlan-id=10 datapath.vlan-mode=use-tag name=Config_WORK security.authentication-types=wpa-psk,wpa2-psk \
    security.passphrase=secret_work_password ssid=WiFi_WORK
add country=latvia datapath.local-forwarding=yes datapath.vlan-id=20 datapath.vlan-mode=use-tag name=Config_GUEST security.authentication-types=\
    wpa-psk,wpa2-psk security.passphrase=secret_guest_password ssid=WiFi_GUEST

```

-   We are going to create a single CAPsMAN provisioning rule to create the **WiFi\_WORK** and the **WiFi\_GUEST** SSIDs on a single device, each connected CAP is going to create these SSIDs automatically

```
/caps-man provisioning
add action=create-dynamic-enabled master-configuration=Config_WORK slave-configurations=Config_GUEST
```

You can create even more Virtual APs by adding multiple slave-configurations. That requires multiple CAPsMAN configurations that were created earlier.

-   For security reasons, limit the CAPsMAN to a single interface

```
/caps-man manager interface
set [ find default=yes ] forbid=yes
add disabled=no interface=ether1

```

-   Enable the CAPsMAN manager

```
/caps-man manager
set enabled=yes

```

-   Setup DHCP Server for each VLAN

```
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

## Switch:

In this example, we are going to be using [Bridge VLAN Filtering](https://help.mikrotik.com/docs/display/ROS/Bridging+and+Switching#BridgingandSwitching-VLANExample-TrunkandAccessPorts) to filter unknown VLANs and to assign other devices to the same networks. Some devices are capable of offloading this to the built-in switch chip, check [Basic VLAN switching](https://help.mikrotik.com/docs/display/ROS/Basic+VLAN+switching) guide to see how to configure it on different types of devices.

-   Setup Bridge VLAN Filtering

```
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

In this example, untagged traffic is going to be used to communicate between CAPs and CAPsMAN Router. By default, if PVID is not changed, untagged traffic is going to be forwarded between ports that have the same PVID value set (including the default PVID).

## CAPs:

-   Create a bridge and assign a port to it, that is connected to the CAPsMAN Router

```
/interface bridge
add name=bridge1
/interface bridge port
add bridge=bridge1 interface=ether1

```

-   Enable CAP mode on the AP, and make sure you specify to use the newly created bridge

```
/interface wireless cap
set bridge=bridge1 discovery-interfaces=bridge1 enabled=yes interfaces=wlan1

```

-   After CAPs are successfully connected to the CAPsMAN Router, the wlan1 (SSID **WiFi\_WORK**) and a newly created virtual wlan5 (SSID **WiFi\_GUEST**) interfaces get dynamically added as bridge ports. The VLAN is assigned for a wireless interface and as a result, all data coming from wireless gets tagged and only data with this tag will be sent out over wireless. A bridge vlan-filtering can be disabled if additional VLAN managing and controlling is not needed. The associated VLAN can be seen with a port VLAN ID (PVID) property.

```
[admin@CAP_1] /interface bridge port pr
Flags: X - disabled, I - inactive, D - dynamic, H - hw-offload 
 #     INTERFACE                     BRIDGE                    HW  PVID PRIORITY  PATH-COST INTERNAL-PATH-COST    HORIZON
 0   H ether1                        bridge1                   yes    1     0x80         10                 10       none
 1  D  wlan1                         bridge1                         10     0x80         10                 10       none
 2  D  wlan5                         bridge1                         20     0x80         10                 10       none

```

That is it! Connect Wireless clients to your APs and check connectivity.

# Using CAPsMAN Forwarding Mode

![](https://help.mikrotik.com/docs/download/attachments/137986075/CAPsMAN_VLANs.jpg?version=1&modificationDate=1659445096063&api=v2)

In CAPsMAN Forwarding Mode all traffic that is coming from a CAP is encapsulated with a special CAPsMAN header, which can only be removed by a CAPsMAN router, this means that a switch will not be able to distinguish the VLAN ID set by the CAP since the VLAN tag is also going to be encapsulated. This mode limits the possibility to divert traffic in Layer2 networks, but gives you the possibility to forward traffic from each CAP over Layer3 networks for a distant CAPsMAN router to process the traffic, this mode is useful when you want to control multiple CAPs in remote locations, but want to use a central gateway.

## CAPsMAN router:

-   Setup Bridge VLAN filtering to limit interfaces to appropriate VLANs

```
/interface bridge
add name=bridge1 vlan-filtering=yes
/interface bridge port
add bridge=bridge1 interface=ether1 pvid=10
add bridge=bridge1 interface=ether2 pvid=20
/interface bridge vlan
add bridge=bridge1 tagged=bridge1 untagged=ether1 vlan-ids=10
add bridge=bridge1 tagged=bridge1 untagged=ether2 vlan-ids=20

```

  

CAPsMAN will attach CAP interfaces to the bridge and automatically will add appropriate entries to the bridge VLAN table

  

**Note:** CAPsMAN will attach CAP interfaces to the bridge and automatically will add appropriate entries to the bridge VLAN table. This feature is available starting with RouterOS v6.43

  

-   Create appropriate CAP configurations for each VLAN

```
/caps-man configuration
add country=latvia datapath.bridge=bridge1 datapath.vlan-id=10 datapath.vlan-mode=use-tag name=Config_WORK security.authentication-types=wpa-psk,wpa2-psk \
    security.passphrase=secret_work_password ssid=WiFi_WORK
add country=latvia datapath.bridge=bridge1 datapath.vlan-id=20 datapath.vlan-mode=use-tag name=Config_GUEST security.authentication-types=wpa-psk,wpa2-psk \
    security.passphrase=secret_guest_password ssid=WiFi_GUEST

```

-   We are going to create a single CAPsMAN provisioning rule to create the **WiFi\_WORK** and the **WiFi\_GUEST** SSIDs on a single device, each connect CAP is going to create these SSIDs automatically

```
/caps-man provisioning
add action=create-dynamic-enabled master-configuration=Config_WORK slave-configurations=Config_GUEST
```

  

You can create even more Virtual APs by adding multiple slave-configurations. That requires multiple CAPsMAN configurations that were created earlier.

  

-   For security reasons, limit the CAPsMAN to interfaces. to which CAPs are going to be connected

```
/caps-man manager interface
set [ find default=yes ] forbid=yes
add disabled=no interface=ether3
add disabled=no interface=ether4

```

-   Enable the CAPsMAN manager

```
/caps-man manager
set enabled=yes

```

-   Setup DHCP Server for each VLAN

```
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

## CAPs:

-   Enable CAP mode on each AP, specify which interface is connected to the CAPsMAN router

```
/interface wireless cap set discovery-interfaces=ether1 enabled=yes interfaces=wlan1

```

-   After CAPs are successfully connected to the CAPsMAN Router, two CAP interfaces will be dynamically created on the CAPsMAN Router. Both of these interfaces will get dynamically added as bridge ports on the same CAPsMAN Router due to explicitly selecting the bridge interface with datapath.bridge=bridge1 and using the default CAPsMAN Forwarding Mode datapath.local-forwarding=no. Because of using a bridge with enabled vlan-filtering, both CAP interfaces will also show up in a bridge VLAN table.

```
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

That is it! Connect Wireless clients to your APs and check connectivity.

# Case studies

## Without Virtual APs

Not everyone wants to create Virtual APs since that does decrease the total throughput. If you want to use multiple devices to create multiple SSIDs, then it is possible to assign a certain configuration on a CAP based on its identity. To achieve this you should use CAPsMAN provisioning rules along with RegEx expressions. In this example we are going to assign the **Config\_WORK** configuration to CAPs that have identity set to "'**AP\_WORK\_\***" and we are going to assign the **Config\_GUEST** configuration to CAPs that have identity set to "**AP\_GUEST\_\***". To do this, you simply need to change the CAPsMAN provisioning rules.

-   Remove any existing provisioning rules

```
/caps-man provisioning remove [f]

```

-   Create new provisioning rules that will assign appropriate configuration on a CAP based on its identity

```
/caps-man provisioning
add action=create-dynamic-enabled identity-regexp=^AP_GUEST_ master-configuration=Config_GUEST
add action=create-dynamic-enabled identity-regexp=^AP_WORK_ master-configuration=Config_WORK
```

  

Don't forget to set a proper identity on the CAPs since CAPsMAN is going to assign appropriate configuration on the APs based on it's identity.