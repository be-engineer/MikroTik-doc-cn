# Summary

Bonding is a technology that allows the aggregation of multiple ethernet-like interfaces into a single virtual link, thus getting higher data rates and providing failover.

![](https://help.mikrotik.com/docs/download/attachments/63406084/Lacp.png?version=1&modificationDate=1618901948934&api=v2)

## Configuration Example

Let us assume that we have two Ethernet interfaces on each router (SW1 and SW2) and want to get the maximum data rate between these two routers. To make this possible, follow these steps:

1.  Make sure that you do not have IP addresses on interfaces that will be enslaved for bonding interface.
2.  Add bonding interface and IP address on the SW1:
    
    `/interface bonding` `add` `mode``=802.3ad` `slaves``=ether1,ether2` `name``=bond1`
    
    `/ip address` `add` `address``=172.16.0.1/24` `interface``=bond1`
    
3.  Do the same thing on the SW2:
    
    `/interface bonding` `add` `mode``=802.3ad` `slaves``=ether1,ether2` `name``=bond1`
    
    `/ip address` `add` `address``=172.16.0.2/24` `interface``=bond1`
    
4.  Test the link from Router1:
    
    `[admin@Router1] >` `ping` `172.16.0.2`
    
      `SEQ HOST                                 SIZE TTL TIME  STATUS`                  
    
        `0 172.16.0.2                             56  64 0ms` 
    
        `1 172.16.0.2                             56  64 0ms` 
    
        `2 172.16.0.2                             56  64 0ms` 
    
        `sent``=3` `received``=3` `packet-loss``=0%` `min-rtt``=0ms` `avg-rtt``=0ms` `max-rtt``=0ms`
    

The bonding interface has to be configured on both hosts and needs a couple of seconds to get connectivity with its peers.

## Balancing Modes

## 802.3ad

802.3ad mode is an IEEE standard also called LACP (Link Aggregation Control Protocol). It includes automatic configuration of the aggregates, so minimal configuration of the switch is needed. This standard also mandates that frames will be delivered in order and connections should not see misordering of packets. The standard also mandates that all devices in the aggregate must operate at the same speed and duplex mode.

LACP balances outgoing traffic across the active ports based on hashed protocol header information and accepts incoming traffic from any active port. The hash includes the Ethernet source and destination address and if available, the VLAN tag, and the IPv4/IPv6 source and destination address. How this is calculated depends on the transmit-hash-policy parameter. The ARP link monitoring is not recommended, because the ARP replies might arrive only on one slave port due to transmit hash policy on the LACP peer device. This can result in unbalanced transmitted traffic, so MII link monitoring is the recommended option.

## balance-xor

This mode balances outgoing traffic across the active ports based on the hashed protocol header information and accepts incoming traffic from any active port. The mode is very similar to [LACP](https://wiki.mikrotik.com/wiki/Manual:Interface/Bonding#802.3ad) except that it is not standardized and works with **layer-3-and-4** hash policy. The mode can work together with static Link Aggregation Group (LAG) interfaces.

## Additional Information