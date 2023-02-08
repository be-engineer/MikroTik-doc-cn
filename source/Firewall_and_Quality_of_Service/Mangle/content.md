# 介绍

Mangle is a kind of 'marker' that marks packets for future processing with special marks. Many other facilities in RouterOS make use of these marks, e.g. queue trees, NAT, routing. They identify a packet based on its mark and process it accordingly. The mangle marks exist only within the router, they are not transmitted across the network.

Additionally, the mangle facility is used to modify some fields in the IP header, like TOS (DSCP) and TTL fields.

Firewall mangle rules consist of five predefined chains that cannot be deleted:

![](https://help.mikrotik.com/docs/download/attachments/48660587/mangle.png?version=1&modificationDate=1608289226604&api=v2)

- The **PREROUTING** chain: Rules in this chain apply to packets as they just arrive on the network interface;
- The **INPUT** chain: Rules in this chain apply to packets just before they’re given to a local process;
- The **OUTPUT** chain: The rules here apply to packets just after they’ve been produced by a process;
- The **FORWARD** chain: The rules here apply to any packets that are routed through the current host;
- The **POSTROUTING** chain: The rules in this chain apply to packets as they just leave the network interface;

## Properties

| Property                                        | Description                                        |
| ----------------------------------------------- | -------------------------------------------------- |
| **action** (_action name_; Default: **accept**) | Action to take if a packet is matched by the rule: |
- accept \- accept the packet. A packet is not passed to the next firewall rule.
- add-dst-to-address-list \- add destination address to address list specified by `address-list` parameter
- add-src-to-address-list \- add source address to address list specified by `address-list` parameter
- change-dscp \- change Differentiated Services Code Point (DSCP) field value specified by the new-dscp parameter
- change-mss \- change Maximum Segment Size field value of the packet to a value specified by the new-mss parameter
- change-ttl \- change Time to Live field value of the packet to a value specified by the new-ttl parameter
- clear-df \- clear 'Do Not Fragment' Flag
- fasttrack-connection \- shows fasttrack counters, useful for statistics
- jump \- jump to the user-defined chain specified by the value of `jump-target` parameter
- log \- add a message to the system log containing the following data: in-interface, out-interface, src-mac, protocol, src-ip:port->dst-ip:port and length of the packet. After a packet is matched it is passed to the next rule in the list, similar as `passthrough`
- mark-connection \- place a mark specified by the new-connection-mark parameter on the entire connection that matches the rule
- mark-packet \- place a mark specified by the new-packet-mark parameter on a packet that matches the rule
- mark-routing \- place a mark specified by the new-routing-mark parameter on a packet. This kind of marks is used for policy routing purposes only
- passthrough \- if a packet is matched by the rule, increase counter and go to next rule (useful for statistics).
- return \- pass control back to the chain from where the jump took place
- route \- forces packets to a specific gateway IP by ignoring normal routing decision (prerouting chain only)
- set-priority \- set priority specified by the new-priority parameter on the packets sent out through a link that is capable of transporting priority (VLAN or WMM-enabled wireless interface). [Read more](https://help.mikrotik.com/docs/display/ROS/WMM+and+VLAN+priority)
- sniff-pc \- send a packet to a remote RouterOS CALEA server.
- sniff-tzsp \- send a packet to a remote TZSP compatible system (such as Wireshark). Set remote target with `sniff-target` and `sniff-target-port` parameters (Wireshark recommends port 37008)
- strip-ipv4-options \- strip IPv4 option fields from IP header, the action does not actually remove IPv4 options but rather replaces all option octets with NOP, further matcher with ipv4-options=any will still match the packet. |
| **address-list** (_string_; Default: ) | Name of the address list to be used. Applicable if action is `add-dst-to-address-list` or `add-src-to-address-list` |
| **address-list-timeout** (_none-dynamic | none-static | time_; Default: **none-dynamic**) | Time interval after which the address will be removed from the address list specified by `address-list` parameter. Used in conjunction with `add-dst-to-address-list` or `add-src-to-address-list` actions  
- Value of none-dynamic (`00:00:00`) will leave the address in the address list till reboot
- Value of none-static will leave the address in the address list forever and will be included in configuration export/backup |
| **chain** (_name_; Default: ) | Specifies to which chain the rule will be added. If the input does not match the name of an already defined chain, a new chain will be created |
| **comment** (_string_; Default: ) | Descriptive comment for the rule. |
| **connection-bytes** (_integer-integer_; Default: ) | Matches packets only if a given amount of bytes has been transferred through the particular connection. 0 - means infinity, for example `connection-bytes=2000000-0` means that the rule matches if more than 2MB (upload and download) has been transferred through the relevant connection |
| **connection-limit** (_integer,netmask_; Default: ) | Matches connections per address or address block after a given value is reached |
| **connection-mark** (_no-mark | string_; Default: ) | Matches packets marked via mangle facility with particular connection mark. If **no-mark** is set, the rule will match any unmarked connection. |
| **connection-nat-state** (_srcnat | dstnat_; Default: ) | Can match connections that are srcnatted, dstnatted, or both. Note that connection-state=related connections connection-nat-state is determined by the direction of the first packet. and if connection tracking needs to use dst-nat to deliver this connection to the same hosts as the main connection it will be in connection-nat-state=dstnat even if there are no dst-nat rules at all. |
| **connection-rate** (_Integer 0..4294967295_; Default: ) | Connection Rate is a firewall matcher that allows the capture of traffic based on the present speed of the connection. |
| **connection-state** (_established | invalid | new | related_; Default: ) | Interprets the connection tracking analytics data for a particular packet:
- established \- a packet that belongs to an existing connection
- invalid \- a packet that does not have a determined state in connection tracking (usually - severe out-of-order packets, packets with wrong sequence/ack number, or in case of a resource over usage on a router), for this reason, invalid packet will not participate in NAT (as only connection-state=new packets do), and will still contain original source IP address when routed. We strongly suggest dropping all connection-state=invalid packets in firewall filter forward and input chains
- new \- the packet has started a new connection, or otherwise associated with a connection that has not seen packets in both directions
- related \- a packet that is related to, but not parts of an existing connection, such as ICMP errors or a packet that begins FTP data connection
- untracked - packet which was set to bypass connection tracking in Firewall RAW tables. |
| **connection-type** (_ftp | h323 | irc | pptp | quake3 | sip | tftp_; Default: ) | Matches packets from related connections based on information from their connection tracking helpers. A relevant connection helper must be enabled under: /ip firewall service-port |
| **content** (_string_; Default: ) | Match packets that contain specified text |
| **dscp** (_integer: 0..63_; Default: ) | Matches DSCP IP header field |
| **dst-address** (_IP/netmask | IP range_; Default: ) | Matches packets where the destination is equal to specified IP or falls into a specified IP range |
| **dst-address-list** (_name_; Default: ) | Matches destination address of a packet against user-defined address list |
| **dst-address-type** (_unicast | local | broadcast | multicast_; Default: ) | Matches destination address type:
- unicast \- IP address used for point to point transmission
- local \- if dst-address is assigned to one of the router's interfaces
- broadcast \- packet is sent to all devices in a subnet
- multicast \- packet is forwarded to a defined group of devices |
| **dst-limit** (_integer\[/time\],integer,dst-address | dst-port | src-address\[/time\]_; Default: ) | Matches packets until a given PPS limit is exceeded. As opposed to the limit matcher, every destination IP address/destination port has its own limit. Parameters are written in the following format: `count[/time],burst,mode[/expire]`.
- **count** \- maximum average packet rate measured in packets per `time` interval
- **time** \- specifies the time interval in which the packet rate is measured (optional)
- **burst** \- number of packets that are not counted by packet rate
- **mode** \- the classifier for packet rate limiting
- **expire** \- specifies interval after which recorded ip address /port will be deleted (optional) |
| **dst-port** (_integer\[-integer\]: 0..65535_; Default: ) | List of destination port numbers or port number ranges |
| **fragment** (_yes|no_; Default: ) | Matches fragmented packets. The first (starting) fragment does not count. If connection tracking is enabled there will be no fragments as the system automatically assembles every packet |
| **hotspot** (_auth | from-client | http | local-dst | to-client_; Default: ) | Matches packets received from HotSpot clients against various HotSpot matches.
- auth \- matches authenticated HotSpot client packets
- from-client \- matches packets that are coming from the HotSpot client
- http \- matches HTTP requests sent to the HotSpot server
- local-dst \- matches packets that are destined to the HotSpot server
- to-client \- matches packets that are sent to the HotSpot client |
| **icmp-options** (_integer:integer_; Default: ) | Matches ICMP "type:code" fields |
| **in-bridge-port** (_name_; Default: ) | Actual interface the packet has entered the router if the incoming interface is a bridge |
| **in-interface** (_name_; Default: ) | Interface the packet has entered the router |
| **ingress-priority** (_integer: 0..63_; Default: ) | Matches ingress the priority of the packet. Priority may be derived from VLAN, WMM, or MPLS EXP bit. `[Read more](https://help.mikrotik.com/docs/display/ROS/WMM+and+VLAN+priority)` |
| **ipsec-policy** (_in | out, ipsec | none_; Default: ) | Matches the policy used by IpSec. Value is written in the following format: `**direction, policy**`. The direction is Used to select whether to match the policy used for decapsulation or the policy that will be used for encapsulation.
- in \- valid in the PREROUTING, INPUT, and FORWARD chains
- out \- valid in the POSTROUTING, OUTPUT, and FORWARD chains
- ipsec \- matches if the packet is subject to IpSec processing;
- none \- matches packet that is not subject to IpSec processing (for example, IpSec transport packet).
For example, if a router receives an IPsec encapsulated Gre packet, then rule `ipsec-policy=in,ipsec` will match Gre packet, but a rule `ipsec-policy=in,none` will match the ESP packet. |
| **ipv4-options** (_any | loose-source-routing | no-record-route | no-router-alert | no-source-routing | no-timestamp | none | record-route | router-alert | strict-source-routing | timestamp_; Default: ) | Matches IPv4 header options.
- any \- match packet with at least one of the ipv4 options
- loose-source-routing \- match packets with a loose source routing option. This option is used to route the internet datagram based on information supplied by the source
- no-record-route \- match packets with no record route option. This option is used to route the internet datagram based on information supplied by the source
- no-router-alert \- match packets with no router alter option
- no-source-routing \- match packets with no source routing option
- no-timestamp \- match packets with no timestamp option
- record-route \- match packets with record route option
- router-alert \- match packets with router alter option
- strict-source-routing \- match packets with strict source routing option
- timestamp \- match packets with a timestamp |
| **jump-target** (_name_; Default: ) | Name of the target chain to jump to. Applicable only if `action=jump` |
| **layer7-protocol** (_name_; Default: ) | Layer7 filter name defined in [layer7 protocol menu](https://wiki.mikrotik.com/wiki/Manual:IP/Firewall/L7 "Manual:IP/Firewall/L7"). |
| **limit** (_integer,time,integer_; Default: ) | Matches packets until a given PPS limit is exceeded. Parameters are written in the following format: `count[/time],burst`.
- **count** \- maximum average packet rate measured in packets per `time` interval
- **time** \- specifies the time interval in which the packet rate is measured (optional, 1s will be used if not specified)
- **burst** \- number of packets that are not counted by packet rate |
| **log** (_yes | no; Default:_ **no**) | Add a message to the system log containing the following data: in-interface, out-interface, src-mac, protocol, src-ip:port->dst-ip:port, and length of the packet. |
| **log-prefix** (_string_; Default: ) | Adds specified text at the beginning of every log message. Applicable if _action=log_ or _log=yes_ configured. |
| **new-dscp** (_integer: 0..63_; Default: ) | Sets a new DSCP value for a packet |
| **new-mss** (_integer_; Default: ) | 
Sets a new MSS for a packet.
**Clampt-to-pmtu feature sets (DF) bit in the IP header to dynamically discover the PMTU of a path. Host sends all datagrams on that path with the DF bit set until receives ICMP
Destination Unreachable messages with a code meaning "fragmentation needed and DF set".  Upon receipt of such a message, the source host reduces its assumed PMTU for the path.** |
| **new-packet-mark** (_string_; Default: ) | Sets a new packet-mark value |
| **new-priority** (_integer | from-dscp | from-dscp-high-3-bits | from-ingress_; Default: ) | Sets a new priority for a packet. This can be the VLAN, WMM, DSCP or MPLS EXP priority [Read more](https://help.mikrotik.com/docs/display/ROS/WMM+and+VLAN+priority). This property can also be used to set an internal priority. |
| **new-routing-mark** (_string_; Default: ) | Sets a new routing-mark value (in RouterOS v7 routing mark must be created before as a new [Routing table](https://help.mikrotik.com/docs/display/ROS/Policy+Routing)) |
| **new-ttl** (_decrement | increment | set:integer_; Default: ) | Sets a new Time to live value  |
| **nth** (_integer,integer_; Default: ) | Matches every nth packet: _nth=2,1_ rule will match every first packet of 2, hence, 50% of all the traffic that is matched by the rule |
| **out-bridge-port** (_name_; Default: ) | Actual interface the packet is leaving the router if the outgoing interface is a bridge |
| **out-interface** (; Default: ) | Interface the packet is leaving the router |
| **packet-mark** (_no-mark | string_; Default: ) | Matches packets marked via mangle facility with particular packet mark. If **no-mark** is set, the rule will match any unmarked packet |
| **packet-size** (_integer\[-integer\]:0..65535_; Default: ) | Matches packets of specified size or size range in bytes |
| **passthrough** (_yes|no_; Default: **yes**) | whether to let the packet to pass further (like action passthrough) into the firewall or not (property only valid some actions) |
| **per-connection-classifier** (_ValuesToHash:Denominator/Remainder_; Default: ) | PCC matcher allows division of traffic into equal streams with the ability to keep packets with a specific set of options in one particular stream |
| **port** (_integer\[-integer\]: 0..65535_; Default: ) | Matches if any (source or destination) port matches the specified list of ports or port ranges. Applicable only if `protocol` is TCP or UDP |
| **protocol** (_name or protocol ID_; Default: **tcp**) | Matches particular IP protocol specified by protocol name or number |
| **psd** (_integer,time,integer,integer_; Default: ) | Attempts to detect TCP and UDP scans. Parameters are in the following format `WeightThreshold, DelayThreshold, LowPortWeight, HighPortWeight`
- **WeightThreshold** \- total weight of the latest TCP/UDP packets with different destination ports coming from the same host to be treated as port scan sequence
- **DelayThreshold** \- delay for the packets with different destination ports coming from the same host to be treated as possible port scan subsequence
- **LowPortWeight** \- the weight of the packets with privileged (<1024) destination port
- **HighPortWeight** \- the weight of the packet with a non-privileged destination port |
| **random** (_integer: 1..99_; Default: ) | Matches packets randomly with a given probability. |
| **routing-mark** (_string_; Default: ) | Matches packets marked by mangle facility with particular routing mark |
| **route-dst** (_IP, Default:_) | Matches packets with a specific gateway |
| **priority** (_integer: 0..63_; Default: ) | Matches the packet's priority after a new priority has been set. Priority may be derived from VLAN, WMM, DSCP, MPLS EXP bit, or from the internal priority that has been set using the set-priority action |
| **src-address** (_IP/Netmask, IP range_; Default: ) | Matches packets where the source is equal to specified IP or falls into a specified IP range. |
| **src-address-list** (_name_; Default: ) | Matches source address of a packet against user-defined address list |
| **src-address-type** (_unicast | local | broadcast | multicast_; Default: ) | 
Matches source address type:
- unicast \- IP address used for point-to-point transmission
- local \- if an address is assigned to one of the router's interfaces
- broadcast \- packet is sent to all devices in a subnet
- multicast \- packet is forwarded to a defined group of devices |
| **src-port** (_integer\[-integer\]: 0..65535_; Default: ) | List of source ports and ranges of source ports. Applicable only if a protocol is TCP or UDP. |
| **src-mac-address** (_MAC address_; Default: ) | Matches source MAC address of the packet |
| **tcp-flags** (_ack | cwr | ece | fin | psh | rst | syn | urg_; Default: ) | Matches specified TCP flags
- ack \- acknowledging data
- cwr \- congestion window reduced
- ece \- ECN-echo flag (explicit congestion notification)
- fin \- close connection
- psh \- push function
- rst \- drop connection
- syn \- new connection
- urg \- urgent data |
| **tcp-mss** (_integer\[-integer\]: 0..65535_; Default: ) | Matches TCP MSS value of an IP packet |
| **time** (_time-time,sat | fri | thu | wed | tue | mon | sun_; Default: ) | Allows creation of a filter based on the packets' arrival time and date or, for locally generated packets, departure time and date |
| **tls-host** (_string_; Default: ) | Allows matching traffic based on TLS hostname. Accepts [GLOB syntax](https://en.wikipedia.org/wiki/Glob_(programming)) for wildcard matching. Note that the matcher will not be able to match the hostname if the TLS handshake frame is fragmented into multiple TCP segments (packets). |
| **ttl** (_equal | greater-than | less-than | not-equal : integer(0..255)_; Default: ) | Matches packets TTL value. |

### Stats

To show additional _read-only_ properties:

| Property                | Description                                     |
| ----------------------- | ----------------------------------------------- |
| **bytes** (_integer_)   | The total amount of bytes matched by the rule   |
| **packets** (_integer_) | The total amount of packets matched by the rule |

To print out stats:

```shell
[admin@MikroTik] > ip firewall mangle print stats all
Flags: X - disabled, I - invalid, D - dynamic
# CHAIN ACTION BYTES PACKETS
0 D ;;; special dummy rule to show fasttrack counters
prerouting passthrough 18 176 176 30 562
1 D ;;; special dummy rule to show fasttrack counters
forward passthrough 18 176 176 30 562
2 D ;;; special dummy rule to show fasttrack counters
postrouting passthrough 18 176 176 30 562
3 forward change-mss 18 512 356
```

## Configuration example

### Change MSS

It is a known fact that VPN links have a smaller packet size due to encapsulation overhead. A large packet with MSS that exceeds the MSS of the VPN link should be fragmented prior to sending it via that kind of connection. However, if the packet has a _Don't Fragment_ flag set, it cannot be fragmented and should be discarded. On links that have broken path MTU discovery (PMTUD), it may lead to a number of problems, including problems with FTP and HTTP data transfer and e-mail services.

In the case of a link with broken PMTUD, a decrease of the MSS of the packets coming through the VPN link resolves the problem. The following example demonstrates how to decrease the MSS value via mangle:

`/ip firewall mangle add out-interface=pppoe-out protocol=tcp tcp-flags=syn action=change-mss new-mss=1300 chain=forward tcp-mss=1301-65535`