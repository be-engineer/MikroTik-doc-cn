# Overview

-   1[Overview](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Overview)
-   2[Nv2 protocol implementation status](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Nv2protocolimplementationstatus)
-   3[Compatibility and coexistence with other wireless protocols](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Compatibilityandcoexistencewithotherwirelessprotocols)
-   4[How Nv2 compares with Nstreme and 802.11](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-HowNv2compareswithNstremeand802.11)
    -   4.1[Nv2 vs 802.11](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Nv2vs802.11)
    -   4.2[Nv2 vs Nstreme](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Nv2vsNstreme)
-   5[Configuring Nv2](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-ConfiguringNv2)
-   6[Migrating to Nv2](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-MigratingtoNv2)
-   7[Nv2 AP Synchronization](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Nv2APSynchronization)
    -   7.1[Configuration example](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Configurationexample)
-   8[QoS in Nv2 network](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-QoSinNv2network)
    -   8.1[Nv2-qos=default](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Nv2-qos=default)
    -   8.2[Nv2-qos=frame-priority](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Nv2-qos=frame-priority)
-   9[Security in Nv2 network](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-SecurityinNv2network)

Nv2 protocol is a proprietary wireless protocol developed by MikroTik for use with Atheros 802.11 wireless chips. Nv2 is based on TDMA (Time Division Multiple Access) media access technology instead of CSMA (Carrier Sense Multiple Access) media access technology used in regular 802.11 devices.

TDMA media access technology solves hidden node problem and improves media usage, thus improving throughput and latency, especially in PtMP networks.

Nv2 is supported for Atheros 802.11n chips and legacy 802.11a/b/g chips starting from AR5212, but not supported on older AR5211 and AR5210 chips. This means that both - 11n and legacy devices can participate in the same network and it is not required to upgrade hardware to implement Nv2 in network.

Media access in Nv2 network is controlled by Nv2 Access Point. Nv2 AP divides time into fixed size "periods" which are dynamically divided into downlink (data sent from AP to clients) and uplink (data sent from clients to AP) portions, based on the queue state on AP and clients. Uplink time is further divided between connected clients based on their requirements for bandwidth. At the beginning of each period, AP broadcasts a schedule that tells clients when they should transmit and the amount of time they can use.

In order to allow new clients to connect, Nv2 AP periodically assigns uplink time for "unspecified" client - this time interval is then used by a fresh client to initiate registration to AP. Then AP estimates propagation delay between AP and client and starts periodically scheduling uplink time for this client in order to complete registration and receive data from client.

Nv2 implements dynamic rate selection on a per-client basis and ARQ for data transmissions. This enables reliable communications across Nv2 links.

For QoS Nv2 implements variable number of priority queues with built-in default QoS scheduler that can be accompanied with fine-grained QoS policy based on firewall rules or priority information propagated across network using VLAN priority or MPLS EXP bits.

Nv2 protocol limit is 511 clients per interface.

# Nv2 protocol implementation status

Nv2 has the following features:

-   TDMA media access
-   WDS support
-   QoS support with variable number or priority queues
-   data encryption
-   RADIUS authentication features
-   statistics fields
-   Fixed Downlink mode support
-   Uplink/Downlink ratio support
-   Nv2 AP synchronization experimental support

# Compatibility and coexistence with other wireless protocols

Nv2 protocol is not compatible to or based on any other available wireless protocols or implementations, either TDMA based or any other kind. This implies that **only Nv2 supporting and enabled devices can participate in Nv2 network**.

Regular 802.11 devices will not recognize and will not be able to connect to Nv2 AP. RouterOS devices that have Nv2 support (that is - have RouterOS version 5.0rc1 or higher) will see Nv2 APs when issuing scan command, but will only connect to Nv2 AP if properly configured.

As Nv2 does not use CSMA technology it may disturb any other network in the same channel. In the same way other networks may disturb Nv2 network, because every other signal is considered noise.

The key points regarding compatibility and coexistence:

-   only RouterOS devices will be able to participate in Nv2 network
-   only RouterOS devices will see Nv2 AP when scanning
-   Nv2 network will disturb other networks in the same channel
-   Nv2 network may be affected by any (Nv2 or not) other networks in the same channel
-   Nv2 enabled device will not connect to any other TDMA based network

# How Nv2 compares with Nstreme and 802.11

## Nv2 vs 802.11

The key differences between Nv2 and 802.11:

-   Media access is scheduled by AP - this eliminates hidden node problem and allows to implement centralized media access policy - AP controls how much time is used by every client and can assign time to clients according to some policy instead of every device contending for media access.
-   Reduced propagation delay overhead - There are no per-frame ACKs in Nv2 - this significantly improves throughput, especially on long-distance links where data frame and following ACK frame propagation delay significantly reduces the effectiveness of media usage.
-   Reduced per frame overhead - Nv2 implements frame aggregation and fragmentation to maximize assigned media usage and reduce per-frame overhead (interframe spaces, preambles).

## Nv2 vs Nstreme

The key differences between Nv2 and Nstreme:

-   Reduced polling overhead - instead of polling each client, Nv2 AP broadcasts an uplink schedule that assigns time to multiple clients, this can be considered "group polling" - no time is wasted for polling each client individually, leaving more time for actual data transmission. This improves throughput, especially in PtMP configurations.
-   Reduced propagation delay overhead - Nv2 must not poll each client individually, this allows to create uplink schedule based on estimated distance (propagation delay) to clients such that media usage is most effective. This improves throughput, especially in PtMP configurations.
-   More control over latency - reduced overhead, adjustable period size and QoS features allows for more control over latency in the network.

# Configuring Nv2

**wireless-protocol** setting controls which wireless protocol selects and uses. Note that the meaning of this setting depends on the interface role (either it is AP or client) that depends on interface **mode** setting. Find possible values of **wireless-protocol** and their meaning in table below.

| 
value

 | 

AP

 | 

client

|                    |
| ------------------ | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| unspecified        | establish nstreme or 802.11 network based on old **nstreme** setting | connect to nstreme or 802.11 network based on old **nstreme** setting                                                                                                                                            |
| any                | same as **unspecified**                                              | scan for all matching networks, no matter what protocol, connect using protocol of chosen network                                                                                                                |
| 802.11             | establish 802.11 network                                             | connect to 802.11 networks only                                                                                                                                                                                  |
| nstreme            | establish Nstreme network                                            | connect to Nstreme networks only                                                                                                                                                                                 |
| Nv2                | establish Nv2 network                                                | connect to Nv2 networks only                                                                                                                                                                                     |
| Nv2-nstreme-802.11 | establish Nv2 network                                                | scan for Nv2 networks, if suitable network found - connect, otherwise scan for Nstreme networks, if suitable network found - connect, otherwise scan for 802.11 network and if suitable network found - connect. |
| Nv2-nstreme        | establish Nv2 network                                                | scan for Nv2 networks, if suitable network found - connect, otherwise scan for Nstreme networks and if suitable network found - connect                                                                          |

Note that **wireless-protocol** values **Nv2-nstreme-802.11** and **Nv2-nstreme** **DO NOT** specify some hybrid or special kind of protocol - these values are implemented to simplify client configuration when protocol of network that client must connect to can change. Using these values can help in migrating network to Nv2 protocol.

Most of Nv2 settings are significant only to Nv2 AP - Nv2 client automatically adapts necessary settings from AP. The following settings are relevant to Nv2 AP:

-   **Nv2-queue-count** - specifies how many priority queues are used in Nv2 network. For more details see [QoS in Nv2 network](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-QoSinNv2network)
-   **Nv2-qos** - controls frame to priority queue mapping policy. For more details see [QoS in Nv2 network](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-QoSinNv2network)
-   **Nv2-cell-radius** - specifies distance to farthest client in Nv2 network in km. This setting affects the size of contention time slot that AP allocates for clients to initiate connection and also size of time slots used for estimating distance to client. If this setting is too small, clients that are farther away may have trouble connecting and/or disconnect with "ranging timeout" error. Although during normal operation the effect of this setting should be negligible, in order to maintain maximum performance, it is advised to not increase this setting if not necessary, so AP is not reserving time that is actually never used, but instead allocates it for actual data transfer.
-   **tdma-period-size** - specifies size in ms of time periods that Nv2 AP uses for media access scheduling. Smaller period can potentially decrease latency (because AP can assign time for client sooner), but will increase protocol overhead and therefore decrease throughput. On the other hand - increasing period will increase throughput but also increase latency. It may be required to increase this value for especially long links to get acceptable throughput. This necessity can be caused by the fact that there is "propagation gap" between downlink (from AP to clients) and uplink (from clients to AP) data during which no data transfer is happening. This gap is necessary because client must receive last frame from AP - this happens after propagation delay after AP's transmission, and only then client can transmit - as a result frame from client arrives at AP after propagation delay after client's transmission (so the gap is propagation delay times two). The longer the distance, the bigger is necessary propagation gap in every period. If propagation gap takes significant portion of period, actual throughput may become unacceptable and period size should get increased at the expense of increased latency. Basically value of this setting must be carefully chosen to maximize throughput but also to keep latency at acceptable levels.
-   **Nv2-mode** - specifies to use dynamic or fixed downlink/uplink ratio. Default value is "dynamic-downlink";

"sync-master" - works as nv2-mode=fixed-downlink (so uses nv2-downlink-ratio), but allows slaves to sync to this master; "sync-slave" - tries to sync to master (or already synced slave) and adapt period-size and downlink ratio settings from master.

-   **Nv2-downlink-ratio** - specifies the Nv2 downlink ratio. Uplink ratio is automatically calculated from the downlink-ratio value. When using dynamic-downlink mode the downlink-ratio is also used when link get fully saturated. Minimum value is 20 and maximum 80. Default value is 50.

The follwing settings are significant on both - Nv2 AP and Nv2 client:

-   **Nv2-security** - specifies Nv2 security mode, for more details see [Security in Nv2 network](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Security_in_Nv2_network)
-   **Nv2-preshared-key** - specifies preshared key to be used, for more details see [Security in Nv2 network](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Security_in_Nv2_network)
-   **nv2-sync-secret** - specifies secret key for use in the Nv2 synchronization. Secret should match on Master and Slave devices in order to establish the synced state.

# Migrating to Nv2

Using **wireless-protocol** setting aids in migration or evaluating Nv2 protocol in existing networks really simple and reduce downtime as much as possible. These are the recommended steps:

-   upgrade AP to version that supports Nv2, but do not enable Nv2 on AP yet.
-   upgrade clients to version that supports Nv2
-   configure all clients with **wireless-protocol=Nv2-nstreme-802.11**. Clients will still connect to AP using protocol that was used previously, because AP is not changed over to Nv2 yet
-   configure Nv2 related settings on AP
-   if it is necessary to use data encryption and secure authentication, configure Nv2 security related settings on AP and clients (refer to [Security in Nv2 network](https://help.mikrotik.com/docs/display/ROS/Nv2#Nv2-Security_in_Nv2_network)).
-   set **wireless-protocol=Nv2** on AP. This will make AP to change to Nv2 protocol. Clients should now connect using Nv2 protocol.
-   in case of some trouble you can easily switch back to previous protocol by simply changing it back to whatever was used before on AP.
-   fine tune Nv2 related settings to get acceptable latency and throughput
-   implement QoS policy for maximum performance.

The basic troubleshooting guide:

-   clients have trouble connecting or disconnect with "ranging timeout" error - check that **Nv2-cell-radius** setting is set appropriately
-   unexpectedly low throughput on long distance links although signal and rate is fine - try to increase **tdma-period-size** setting

  

# Nv2 AP Synchronization

This feature will let multiple MikroTik Nv2 APs on the same location to coexist in a better fashion by reducing the interference between each other. This feature will synchronize the transmit/receive time windows of APs in the same frequency, so that all synced MikroTik Nv2 APs transmits/receives at the same time. That allows to reuse the same wireless frequency on the location for multiple APs giving more flexibility in frequency planning.

To make Nv2 synced setup:

-   For Nv2 Synchronization a Master Nv2 AP should be chosen and "nv2-mode=sync-master" should be specified together with "nv2-sync-secret".
-   For Nv2 Slave APs the same wireless frequency as Master AP should be used and "nv2-mode=sync-slave" should be specified with the same "nv2-sync-secret" as the in Master AP configuration.
-   When Master AP is enabled Slave APs will try start searching for Master AP by matching it against specified "nv2-sync-secret".
-   After Master AP is found the Slave AP will calculate the distance to the Master AP as it is possible that Master AP is located not on the same location.
-   Then Slave AP starts operating as AP and it adapts the period size and downlink ratio from the synced Master AP.
-   In addition after the Slave AP is operational other Slave APs can use this Slave AP to sync with.
-   Slave AP periodically listens for the Master AP and checks if the "nv2-sync-secret" still matches and adapts the parameters again. If Master AP interface is disabled/enabled all the Slaves will be also disabled and will start the synchronization process from the beginning.
-   If Master AP stops working Slave APs also will stop working as they do not have sync information.

  

## Configuration example

Master AP:

```
 /interface wireless set wlan1 mode=ap-bridge ssid=Sector1 frequency=5220 nv2-mode=sync-master nv2-preshared-key=clients1 nv2-sync-secret=Tower1
```

Slave AP:

```
 /interface wireless set wlan1 mode=ap-bridge ssid=Sector2 frequency=5220 nv2-mode=sync-slave nv2-preshared-key=clients2 nv2-sync-secret=Tower1
```

Monitor interface on the Slave AP:

```
[admin@SlaveAP] /interface wireless> monitor wlan1
                   status: running-ap
                  channel: 5220/20/an
        wireless-protocol: nv2
              noise-floor: -110dBm
       registered-clients: 1
    authenticated-clients: 1
           nv2-sync-state: synced
          nv2-sync-master: 4C:5E:0C:57:84:38
        nv2-sync-distance: 1
     nv2-sync-period-size: 2
  nv2-sync-downlink-ratio: 50

```

  
Debug logs on the Master AP:

```
 09:22:08 wireless,debug wlan1: 4C:5E:0C:57:85:BE attempts to sync
```

  
Debug logs on the Slave AP:

```
09:22:08 wireless,debug wlan1: attempting to sync to 4C:5E:0C:57:84:38 
09:22:09 wireless,debug wlan1: synced to 4C:5E:0C:57:84:38 

```

# QoS in Nv2 network

QoS in Nv2 is implemented by means of variable number of priority queues. Queue is considered for transmission based on rule recommended by 802.1D-2004 - only if all higher priority queues are empty. In practice this means that at first all frames from queue with higher priority will be sent, and only then next queue is considered. Therefore QoS policy must be designed with care so that higher priority queues do not make lower priority queues starve.

QoS policy in Nv2 network is controlled by AP, clients adapt policy from AP. On AP QoS policy is configured with **Nv2-queue-count** and **Nv2-qos** parameters. **Nv2-queue-count** parameter specifies number of priority queues used. Mapping of frames to queues is controlled by **Nv2-qos** parameter.

## Nv2-qos=default

In this mode outgoing frame at first is inspected by built-in QoS policy algorithm that selects queue based on packet type and size. If built-in rules do not match, queue is selected based on frame priority field, as in **Nv2-qos=frame-priority** mode.

## Nv2-qos=frame-priority

In this mode QoS queue is selected based on frame priority field. Note that frame priority field is not some field in headers and therefore it is valid only while packet is processed by given device. Frame priority field must be set either explicitly by firewall rules or implicitly from ingress priority by frame forwarding process, for example, from MPLS EXP bits. For more information on frame priority field see:

-   [EXP bit behaviour](https://help.mikrotik.com/docs/display/ROS/EXP+bit+behaviour)
-   [WMM and VLAN priority](https://help.mikrotik.com/docs/display/ROS/WMM+and+VLAN+priority)

Queue is selected based on frame priority according to 802.1D recommended user priority to traffic class mapping. Mapping depends on number of available queues (**Nv2-queue-count** parameter). For example, if number of queues is 4, mapping is as follows (pay attention how this mapping resembles mapping used by WMM):

-   priority 0,3 -> queue 0
-   priority 1,2 -> queue 1
-   priority 4,5 -> queue 2
-   priority 6,7 -> queue 3

If number of queues is 2 (default), mapping is as follows:

-   priority 0,1,2,3 -> queue 0
-   priority 4,5,6,7 -> queue 1

If number of queues is 8 (maximum possible), mapping is as follows:

-   priority 1 -> queue 0
-   priority 2 -> queue 1
-   priority 0 -> queue 2
-   priority 3 -> queue 3
-   priority 4 -> queue 4
-   priority 5 -> queue 5
-   priority 6 -> queue 6
-   priority 7 -> queue 7

For other mappings, discussion on rationale for these mappings and recommended practices please see 802.1D-2004.

# Security in Nv2 network

Nv2 security implementation has the following features:

-   hardware accelerated data encryption using AES-CCM with 128 bit keys;
-   4-way handshake for key management (similar to that of 802.11i);
-   preshared key authentication method (similar to that of 802.11i);
-   periodically updated group keys (used for broadcast and multicast data).

Being proprietary protocol Nv2 does not use security mechanisms of 802.11, therefore security configuration is different. Interface using Nv2 protocol ignores **security-profile** setting. Instead, security is configured by the following interface settings:

-   **Nv2-security** - this setting enables/disables use of security in Nv2 network. Note that when security is enabled on AP, it will not accept clients with disabled security. In the same way clients with enabled security will not connect to unsecure APs.
-   **Nv2-preshared-key** - preshared key to use for authentication. Data encryption keys are derived from preshared key during 4-way handshake. Preshared key must be the same in order for 2 devices to establish connection. If preshared key will differ, connection will time out because remote party will not be able to correctly interpret key exchange messages.