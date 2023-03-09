Every RouterBOARD with a miniPCI-e slot which supports LTE modems can also be used as a LoRaWAN gateway by installing **R11e-LoRa8** or **R11e-LoRa9** card. In order to work with Lora, Lora package should be installed. You can find the package for your device architecture in extra packages archive on the [download](https://mikrotik.com/download) page.

_**note**:_  RouterOS does not support 3rd party LoRaWAN gateway cards.

# Properties

**Sub-menu:** /lora

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                                                            |
 | ---------------------------------------------------------- | ---------------------- |
 | **antenna-gain** (_integer \[-128..127\]_; Default: **0**) | Antenna gain in dBi.   |
 | **channel-plan** (_as-923                                  | au-915                 | custom                                        | eu-868                                                              | in-865 | kr-920 | ru-864 | ru-864-mid | us-915-1 | us-915-2_; Default: **eu-868**) | Frequency plans for various regions. |
 | **disabled** (_yes                                         | no_; Default: **yes**) | Whether LoRaWAN gateway is disabled.          |
 | **forward** (_crc-disabled                                 | crc-error              | crc-valid_; Default: **crc-valid,crc-error**) | Defines what kind of packets should be forwarded to Network server: |

-   crc-disabled - forward packets which CRC code isn\`t checked
-   crc-error - forward packets with incorrect CRC code
-   crc-valid - forward valid packets with correct CRC.

 |
| **lbt-enabled** (_yes | no_; Default: **no**) | Whether gateway should use LBT (Listen Before Talk) protocol. |
| **listen-time** (_integer \[0us..4294967295us\]_; Default: **5000us**) | Time in microseconds to track RSSI before TX (used when **lbt-enabled=yes**). |
| **name** (_string_; Default: ) | Name of LoRaWAN gateway. |
| **network** (_private | public_; Default: **public**) | Whether sync word should (network=private) or should not (network=public) be used. |
| **rssi-threshold** (_integer \[-32,768 .. 32,767\]_; Default: **\-65dB**) | RSSI value to determine whether forwarder may use specific channel to talk. If RSSI value is below **rssi-threshold**, channel could be used (used when **lbt-enabled=yes**). |
| **servers** (_list of string_; Default: ) | Name or names of servers from /lora servers. |
| **src-address** (_IP_; Default: ) | Specifies uplink packet source address if necessary (address should match an address configured on the RB). |
| **spoof-gps** (_string_; Default: ) | 

Set custom GPS location:

-   Latitude \[-90..90\]
-   Longitude \[-180..180\]
-   Altitude(**m**) \[-2147483648..2147483647\]

 |

  

# Channels

**Sub-menu:** `/lora channels`

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                                                          |
 | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
 | **bandwidth** (_7.8\_kHz                                 | 15.6\_kHz                                                                                                                                    | 31.2\_kHz                                  | 62.5\_kHz | 125\_kHz | 250\_kHz          | 500\_kHz_; Default: **125\_kHz**)                                                                   | Bandwidth of specific channel, predefined when any of channel-plan preset is used, but could be manually changed when channel-plan is set to custom. |
 | **disabled** (_yes                                       | no_; Default: **no**)                                                                                                                        | Whether specific channel is disabled.      |
 | **freq-off** (_integer_ \[-400000..400000\]; Default:  ) | Channel frequency offset against radio central frequency, it makes possible to adjust channel frequencies so that channels does not overlap. |
 | **radio** (_radio0                                       | radio1_; Default: )                                                                                                                          | Defines which radio uses selected channel. |
 | **spread-factor** (_SF7                                  | SF8                                                                                                                                          | SF9                                        | SF10      | SF11     | SF12_; Default: ) | Defines the Spread Factor for a channel with type=LoRa. Lower Spread Factor means higher data rate. |

  

# Servers

**Sub-menu:** `/lora servers`

`There are two predefined servers that can be used (it requires to make an [The Things Network](https://thethingsnetwork.org) account to use them).`

```
[admin@MikroTik] > lora servers print
 # NAME             UP-PORT DOWN-PORT ADDRESS                                                                                                                                          
 0 TTN-EU              1700      1700 eu.mikrotik.thethings.industries                                                                                                                 
 1 TTN-US              1700      1700 us.mikrotik.thethings.industries
```

`Custom servers can be added as well. Data forwarding to multiple servers can work simultaneously if the first server does not change "DevAdress" part of the packet and under the condition that all servers are able to decode the packet.   `

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                                                      |
 | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | **address** (_domain name or IP address_; Default: ) | Defines LoRaWAN Network server address.                                                                                                                                                                                            |
 | **down-port** (_integer \[0..65535\]_; Default: )    | Defines port for down-link communication (from server to node) with LoRaWAN Network server. Most of known open source servers uses port 1700 as default, but it can change if multiple servers are configured on the same machine. |
 | **name** (_string_; Default: )                       | Defines server name.                                                                                                                                                                                                               |
 | **up-port** (_integer \[0..65535\]_; Default: )      | Defines port for up-link communication (from node to server) with LoRaWAN Network server. Most of known open source servers uses port 1700 as default, but it can change if multiple servers are configured on the same machine.   |