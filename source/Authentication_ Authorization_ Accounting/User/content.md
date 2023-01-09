# 概述

User Manager is RADIUS server implementation in RouterOS which provides centralized user authentication and authorization to a certain service. Having a central user database allows better track of system users and customers. As a separate package, User Manager is available on all architectures including SMIPS, however care must be taken due to limited free space available. It supports many different authentication methods including PAP, CHAP, MS-CHAP, MS-CHAPv2, EAP-TLS, EAP-TTLS and EAP-PEAP. In RouterOS, DHCP, Dot1x, Hotspot, IPsec, PPP, Wireless are features that benefit from User Manager the most. Each user can see their account statistics and manage available profiles using WEB interface. Additionally, users are able buy their own data plans (profiles) using the most popular payment gateway - PayPal making it a great system for service providers. Customized reports can be generated to ease processing by billing department. User Manager works according to RADIUS standard defined in [RFC2865](https://tools.ietf.org/html/rfc2865) and [RFC3579](https://tools.ietf.org/html/rfc3579).

![](https://help.mikrotik.com/docs/download/attachments/2555940/usermanager.jpg?version=1&modificationDate=1657264766867&api=v2)

# Attributes

**Sub-menu:** `/user-manager attribute`

RADIUS attributes are defined authorization, information and configuration parameters that are passed between the RADIUS server and client. User Manager allows sending customized attributes defined in "attributes" menu. RouterOS has a set of predefined attributes already present, but it is also possible to add additional attributes if necessary. Predefined attributes:

| 
Attribute

 | 

Vendor ID

 | 

Type ID

 | 

Value type

 | 

Packet type

 | 

Description

 |     |
 | --- |  |  |  |  |  |
 |     |

Framed-IP-Address

 | 0 (standard) | 8 | ip address | Access-Accept | [RFC2865 section 5.8](https://tools.ietf.org/html/rfc2865#section-5.8) |
| 

Framed-IP-Netmask

 | 0 (standard) | 9 | ip address | Access-Accept | [RFC2865 section 5.9](https://tools.ietf.org/html/rfc2865#section-5.9) |
| 

Session-Timeout

 | 0 (standard) | 27 | integer | Access-Accept, Access-Challenge | [RFC2865 section 5.27](https://tools.ietf.org/html/rfc2865#section-5.27) |
| 

Idle-Timeout

 | 0 (standard) | 28 | integer | Access-Accept, Access-Challenge | [RFC2865 section 5.28](https://tools.ietf.org/html/rfc2865#section-5.28) |
| 

Tunnel-Type

 | 0 (standard) | 64 | 

| 
Value

 | 

Description

 |     |
 | --- | ---------------------------------------------------------- |
 | 1   | Point-to-Point Tunneling Protocol (PPTP)                   |
 | 2   | Layer Two Forwarding (L2F)                                 |
 | 3   | Layer Two Tunneling Protocol (L2TP)                        |
 | 4   | Ascend Tunnel Management Protocol (ATMP)                   |
 | 5   | Virtual Tunneling Protocol (VTP)                           |
 | 6   | IP Authentication Header in the Tunnel-mode (AH)           |
 | 7   | IP-in-IP Encapsulation (IP-IP)                             |
 | 8   | Minimal IP-in-IP Encapsulation (MIN-IP-IP)                 |
 | 9   | IP Encapsulating Security Payload in the Tunnel-mode (ESP) |
 | 10  | Generic Route Encapsulation (GRE)                          |
 | 11  | Bay Dial Virtual Services (DVS)                            |
 | 12  | IP-in-IP Tunneling                                         |



 | Access-Accept | [RFC2868 section 3.1](https://tools.ietf.org/html/rfc2868#section-3.1) |
| 

Tunnel-Medium-Type

 | 0 (standard) | 65 | 

| 
Value

 | 

Description

 |     |
 | --- | ------------------------------------------------------------- |
 | 1   | IPv4 (IP version 4)                                           |
 | 2   | IPv6 (IP version 6)                                           |
 | 3   | NSAP                                                          |
 | 4   | HDLC (8-bit multidrop)                                        |
 | 5   | BBN 1822                                                      |
 | 6   | 802 (includes all 802 media plus Ethernet "canonical format") |
 | 7   | E.163 (POTS)                                                  |
 | 8   | E.164 (SMDS, Frame Relay, ATM)                                |
 | 9   | F.69 (Telex)                                                  |
 | 10  | X.121 (X.25, Frame Relay)                                     |
 | 11  | IPX                                                           |
 | 12  | Appletalk                                                     |
 | 13  | Decnet IV                                                     |
 | 14  | Banyan Vines                                                  |
 | 15  | E.164 with NSAP format subaddress                             |



 | Access-Accept | [RFC2868 section 3.2](https://tools.ietf.org/html/rfc2868#section-3.2) |
| 

Tunnel-Private-Group-ID

 | 0 (standard) | 81 | string | Access-Accept | [RFC2868 section 3.6](https://tools.ietf.org/html/rfc2868#section-3.6) |
| 

Framed-Pool

 | 0 (standard) | 88 | string | Access-Accept | [RFC2869 section 5.18](https://tools.ietf.org/html/rfc2869#section-5.18) |
| Framed-IPv6-Prefix | 0 (standard) | 97 | ipv6 prefix | Access-Accept | [RFC3162 section 2.3](https://tools.ietf.org/html/rfc3162#section-2.3) |
| 

Framed-IPv6-Pool

 | 0 (standard) | 100 | string | Access-Accept | [RFC3162 section 2.6](https://tools.ietf.org/html/rfc3162#section-2.6) |
| 

Delegated-IPv6-Prefix

 | 0 (standard) | 123 | ipv6 prefix | Access-Accept | [RFC4818](https://tools.ietf.org/html/rfc4818) |
| Framed-IPv6-Address | 0 (standard) | 168 | ip address | Access-Accept | [RFC6911 section 3.1](https://tools.ietf.org/html/rfc6911#section-3.1) |
| Mikrotik-Recv-Limit | 14988 (Mikrotik) | 1 | integer | Access-Accept | Total receive limit in bytes for the client. |
| Mikrotik-Xmit-Limit | 14988 (Mikrotik) | 2 | integer | Access-Accept | Total transmit limit in bytes for the client. |
| Mikrotik-Group | 14988 (Mikrotik) | 3 | string | Access-Accept | 

User's group for local users.

HotSpot profile for HotSpot users.

PPP profile for PPP users.

 |
| Mikrotik-Wireless-Forward | 14988 (Mikrotik) | 4 | integer | Access-Accept | Not forward the client's frames back to the wireless infrastructure if this attribute is set to "0" (wireless only). |
| Mikrotik-Wireless-Skip-Dot1x | 14988 (Mikrotik) | 5 | integer | Access-Accept | Disable 802.1x authentication for the particular wireless client if set to non-zero value (wireless only). |
| Mikrotik-Wireless-Enc-Algo | 14988 (Mikrotik) | 6 | 

| 
Value

 | 

Description

 |     |
 | --- | ------------- |
 | 0   | No-encryption |
 | 1   | 40-bit-WEP    |
 | 2   | 104-bit-WEP   |
 | 3   | AES-CCM       |
 | 4   | TKIP          |



 | Access-Accept | WEP encryption algorithm( wireless only). |
| Mikrotik-Wireless-Enc-Key | 14988 (Mikrotik) | 7 | string | Access-Accept | WEP encryption key for the client (wireless only). |
| Mikrotik-Rate-Limit | 14988 (Mikrotik) | 8 | string | Access-Accept | Datarate limitation for clients. Format is: rx-rate\[/tx-rate\] \[rx-burst-rate\[/tx-burst-rate\] \[rx-burst-threshold\[/tx-burst-threshold\] \[rx-burst-time\[/tx-burst-time\] \[priority\] \[rx-rate-min\[/tx-rate-min\]\]\]\] from the point of view of the router (so "rx" is client upload, and "tx" is client download). All rates should be numbers with optional 'k' (1,000s) or 'M' (1,000,000s). If tx-rate is not specified, rx-rate is as tx-rate too. Same goes for tx-burst-rate and tx-burst-threshold and tx-burst-time. If both rx-burst-threshold and tx-burst-threshold are not specified (but burst-rate is specified), rx-rate and tx-rate is used as burst thresholds. If both rx-burst-time and tx-burst-time are not specified, 1s is used as default. Priority takes values 1..8, where 1 implies the highest priority, but 8 - the lowest. If rx-rate-min and tx-rate-min are not specified rx-rate and tx-rate values are used. The rx-rate-min and tx-rate-min values can not exceed rx-rate and tx-rate values.  |
| Mikrotik-Realm | 14988 (Mikrotik) | 9 | string | Access-Request | If it is set in /radius menu, it is included in every RADIUS request as Mikrotik-Realm attribute. If it is not set, the same value is sent as in MS-CHAP-Domain attribute (if MS-CHAP-Domain is missing, Realm is not included neither). |
| Mikrotik-Host-IP | 14988 (Mikrotik) | 10 | ip address | Access-Request | IP address of HotSpot client before Universal Client translation (the original IP address of the client). |
| Mikrotik-Mark-Id | 14988 (Mikrotik) | 11 | string | Access-Accept | Firewall mangle chain name (HotSpot only). The MikroTik RADIUS client upon receiving this attribute creates a dynamic firewall mangle rule with action=jump chain=hotspot and jump-target equal to the attribute value. Mangle chain name can have suffixes .in or .out, that will install rule only for incoming or outgoing traffic. Multiple Mark-id attributes can be provided, but only last ones for incoming and outgoing is used.  |
| Mikrotik-Advertise-URL | 14988 (Mikrotik) | 12 | string | Access-Accept | URL of the page with advertisements that should be displayed to clients. If this attribute is specified, advertisements are enabled automatically, including transparent proxy, even if they were explicitly disabled in the corresponding user profile. Multiple attribute instances may be send by RADIUS server to specify additional URLs which are chosen in round robin fashion. |
| Mikrotik-Advertise-Interval | 14988 (Mikrotik) | 13 | integer | Access-Accept | Time interval between two adjacent advertisements. Multiple attribute instances may be send by RADIUS server to specify additional intervals. All interval values are treated as a list and are taken one-by-one for each successful advertisement. If end of list is reached, the last value is continued to be used. |
| Mikrotik-Recv-Limit-Gigawords | 14988 (Mikrotik) | 14 | integer | Access-Accept | 4G (2^32) bytes of total receive limit (bits 32..63, when bits 0..31 are delivered in Mikrotik-Recv-Limit). |
| Mikrotik-Xmit-Limit-Gigawords | 14988 (Mikrotik) | 15 | integer | Access-Accept | 4G (2^32) bytes of total transmit limit (bits 32..63, when bits 0..31 are delivered in Mikrotik-Recv-Limit). |
| Mikrotik-Wireless-PSK | 14988 (Mikrotik) | 16 | string | Access-Accept |   
 |
| Mikrotik-Total-Limit | 14988 (Mikrotik) | 17 | integer | Access-Accept |   
 |
| Mikrotik-Total-Limit-Gigawords | 14988 (Mikrotik) | 18 | integer | Access-Accept |   
 |
| Mikrotik-Address-List | 14988 (Mikrotik) | 19 | string | Access-Accept |   
 |
| Mikrotik-Wireless-MPKey | 14988 (Mikrotik) | 20 | string | Access-Accept |   
 |
| Mikrotik-Wireless-Comment | 14988 (Mikrotik) | 21 | string | Access-Accept |   
 |
| Mikrotik-Delegated-IPv6-Pool | 14988 (Mikrotik) | 22 | string | Access-Accept | IPv6 pool used for Prefix Delegation. |
| Mikrotik-DHCP-Option-Set | 14988 (Mikrotik) | 23 | string | Access-Accept |   
 |
| Mikrotik-DHCP-Option-Param-STR1 | 14988 (Mikrotik) | 24 | string | Access-Accept |   
 |
| Mikrotik-DHCP-Option-Param-STR2 | 14988 (Mikrotik) | 25 | string | Access-Accept |   
 |
| Mikrotik-Wireless-VLANID | 14988 (Mikrotik) | 26 | integer | Access-Accept | VLAN ID for the client (Wireless only). |
| Mikrotik-Wireless-VLANIDtype | 14988 (Mikrotik) | 27 | 

| 
Value

 | 

Description

 |     |
 | --- | ------- |
 | 0   | 802.1q  |
 | 1   | 802.1ad |



 | Access-Accept | VLAN ID type for the client (Wireless only).  |
| Mikrotik-Wireless-Minsignal | 14988 (Mikrotik) | 28 | string | Access-Accept |   
 |
| Mikrotik-Wireless-Maxsignal | 14988 (Mikrotik) | 29 | string | Access-Accept |   
 |
| Mikrotik-Switching-Filter | 14988 (Mikrotik) | 30 | string | Access-Accept | Allows to create dynamic switch rules when authenticating clients with dot1x server. |

**Properties**

| 
Property

 | 

Description

 |                                                         |
 | ------------------------------------------------------- | ---------------------- |
 | **name** (_string_; Default: )                          | Name of the attribute. |
 | **packet-types** (_string_; Default: **access-accept**) |

-   access-accept - use this attribute in RADIUS Access-Accept messages
-   access-challenge - use this attribute in RADIUS Access-Challenge messages

 |
| **type-id** (_integer:1..255_; Default: ) | Attribute identification number from the specific vendor's attribute database. |
| **value-type** (_string_; Default: ) | 

-   hex
-   ip-address - IPv4 or IPv6 IP address
-   ip6-prefix - IPv6 prefix
-   macro
-   string
-   uint32

 |
| **vendor-id** (_integer_; Default: **0**) | IANA allocated specific enterprise identification number. |

# Database

**Sub-menu:** `/user-manager database`

All RADIUS related information is stored in a separate User Manager's database configurable under the "database" sub-menu. "Enabled" and "db-path" are the only parameters that are not stored in User Manager's database and are stored in main RouterOS configuration table meaning that these parameters will be affected by RouterOS configuration reset. The rest of the configuration, session and payment data is stored in a separate SQLite database on devices FLASH storage. When performing any actions with databases, it is advised to make backup before and after any activity.

**Properties**

| 
Property

 | 

Description

 |                                   |
 | --------------------------------- | ----------------------------------------------------- |
 | **db-path** (_string_; Default: ) | Path to location where database files will be stored. |

**Read-only properties**

| 
Property

 | 

Description

 |                     |
 | ------------------- | ----------------------------------------------------- |
 | **db-size**         | Current size of the database.                         |
 | **free-disk-space** | Free space left on the disk where database is stored. |

**Commands**

| 
Property

 | 

Description

 |                                                    |
 | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
 | **load** (_name_)                                  | Restore previously created backup file in .umb format.                                                               |
 | **migrate-legacy-db** (_database-path; overwrite_) | Convert old User Manager (from RouterOS v6 or before) to new standard. It is possible to overwrite current database. |
 | **optimize-db** ()                                 |
 |                                                    |
 | **save** (name; overwrite)                         | Save current state of the User Manager database.                                                                     |

# Limitations

**Sub-menu:** `/user-manager limitation`

Limitations are used by Profiles and are linked together by Profile-Limitations. RADIUS accounting and Interim updates must be enabled to seamlessly switch between multiple limitations or disconnect active sessions when _download-limit_, _upload-limit_ or _uptime-limit_ is reached.

To disconnect already active sessions from User Manager, _accept_ must be set to _yes_ on RADIUS client side. If simultaneous session limits are not unlimited (shared-users) and it has reached maximal allowed number, then router will try to disconnect older user session firstly.

User-Manager attempts to disconnect active session, before new user will be accepted (when appropriate limit is set), that's why in such setups it is suggested to use 1s for /radius client timeout.

  

IPsec service in RouterOS does not support rate limitations.

**Properties**

| 
Property

 | 

Description

 |                                                       |
 | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
 | **comment** (_string_; Default: )                     | Short description of the limitation.                                                                                                           |
 | **download-limit** (_integer_; Default: **0**)        | Total amount of traffic a user can download in Bytes.                                                                                          |
 | **name** (_string_; Default: )                        | Unique name of the limitation.                                                                                                                 |
 | **rate-limit-burst-rx** ()                            | Part of _MT-Rate-Limit_ RADIUS attribute. Refer to [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue). |
 | **rate-limit-burst-threshold-rx** ()                  | Part of _MT-Rate-Limit_ RADIUS attribute. Refer to [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue). |
 | **rate-limit-burst-threshold-tx** ()                  | Part of _MT-Rate-Limit_ RADIUS attribute. Refer to [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue). |
 | **rate-limit-burst-time-rx** ()                       | Part of _MT-Rate-Limit_ RADIUS attribute. Refer to [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue). |
 | **rate-limit-burst-time-tx** ()                       | Part of _MT-Rate-Limit_ RADIUS attribute. Refer to [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue). |
 | **rate-limit-burst-tx** ()                            | Part of _MT-Rate-Limit_ RADIUS attribute. Refer to [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue). |
 | **rate-limit-min-rx** ()                              | Part of _MT-Rate-Limit_ RADIUS attribute. Refer to [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue). |
 | **rate-limit-min-tx** ()                              | Part of _MT-Rate-Limit_ RADIUS attribute. Refer to [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue). |
 | **rate-limit-priority** ()                            | Part of _MT-Rate-Limit_ RADIUS attribute. Refer to [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue). |
 | **rate-limit-rx** ()                                  | Part of _MT-Rate-Limit_ RADIUS attribute. Refer to [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue). |
 | **rate-limit-tx** ()                                  | Part of _MT-Rate-Limit_ RADIUS attribute. Refer to [Queues#SimpleQueue](https://help.mikrotik.com/docs/display/ROS/Queues#Queues-SimpleQueue). |
 | **reset-counters-interval** (_hourly_                 | _daily_                                                                                                                                        | _weekly_ | _monthly_ | _disabled_); Default: **disabled**) | Interval from _reset-counters-start-time_ when all associated user statistics are cleared. |
 | **reset-counters-start-time** (_datetime_; Default: ) | Static date and time value from which _reset-counters-interval_ is calculated.                                                                 |
 | **transfer-limit** (_integer_; Default: **0**)        | Total amount of aggregated (download+uptime) traffic in Bytes.                                                                                 |
 | **upload-limit** (_integer_; Default: **0**)          | Total amount of traffic a user can upload in Bytes.                                                                                            |
 | **uptime-limit** (_time_; Default: **00:00:00**)      | Total amount of uptime a user can stay active.                                                                                                 |

# Payments

**Sub-menu:** `/user-manager payment`

Information about all received payments are available in this section.

**Read-only properties**

| 
Property

 | 

Description

 |                                        |
 | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | **currency** (_string_)                | The currency used in the transaction.                                                                                                                                                                      |
 | **method** (_string_)                  | Service used for the transaction (currently PayPal only).                                                                                                                                                  |
 | **price** (_decimal_)                  | Amount paid by the user.                                                                                                                                                                                   |
 | **profile** (_profile_)                | Name of the profile the user purchased.                                                                                                                                                                    |
 | **trans-end** (_datetime_)             | Date and time when the transaction started.                                                                                                                                                                |
 | **trans-start** (_datetime_)           | Date and time when the transaction ended.                                                                                                                                                                  |
 | **trans-status** (_string_)            | Status of the transaction. Possible statuses - _started_, _pending_, _approved_, _declined_, _error_, _timeout_, _aborted_, _user approved_. Only _approved_ should be considered as complete transaction. |
 | **user** (_string_; Default: )         | Name of the user who performed the transaction.                                                                                                                                                            |
 | **user-message** (_string_; Default: ) |
 |                                        |

# Profiles

**Sub-menu:** `/user-manager profile`

**Properties**

| 
Property

 | 

Description

 |                                          |
 | ---------------------------------------- | ----------------------------------------------------------------- |
 | **comment** (_string_; Default: )        | Short description of the entry.                                   |
 | **name** (_string_; Default: )           | Unique name of the profile.                                       |
 | **name-for-users** (_string_; Default: ) | Name of the profile that will be shown for users on the Web page. |
 | **override-shared-users** (_decimal      | off                                                               | unlimited_; Default: **off**)                                                                                                                                        | Whether to allow multiple sessions with the same user name. This overrides the _shared-users_ setting. |
 | **price** (_decimal_; Default: **0.00**) |
 |                                          |
 | **starts-when** (_assigned_              | _first-auth_; Default: **assigned**)                              | When does the profile become active. _Assigned_ \- immediately when a User Profile entry is created. _First-auth_ - upon first authentication request from the user. |
 | **validity** (_time                      | unlimited_; Default: **unlimited**)                               | Total amount of time a user can use this profile.                                                                                                                    |

# Profile Limitations

**Sub-menu:** `/user-manager profile-limitation`

Profile-Limitations table links Limitations and Profiles together and defines its validity period. When multiple Limitations are assigned to the same Profile, a user must comply with all Limitations for session to establish. This allows more complicated setups to be created, for example, separate monthly and daily bandwidth limits.

**Properties**

| 
Property

 | 

Description

 |                                                                                                           |
 | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
 | **comment** (_string_; Default: )                                                                         | Short description of the entry.                   |
 | **from-time** (_time_; Default: **00:00:00**)                                                             | Time of day when the limitation should start.     |
 | **limitation** (_limitation_; Default: )                                                                  | Name of already created **Limitation**.           |
 | **profile** (_profile_; Default: )                                                                        | Name of already created **Profile**.              |
 | **till-time** (_time_; Default: **23:59:59**)                                                             | Time of day when the limitation should end.       |
 | **weekdays** (_day of week_; Default: **Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday**) | Day of week when the limitation should be active. |

# Routers

**Sub-menu:** `/user-manager router`

Here are defined all NAS devices that can use User Manager as RADIUS server.

**Properties**

| 
Property

 | 

Description

 |                                                      |
 | ---------------------------------------------------- | ------------------------------------------------------------------------- |
 | **coa-port** (_integer:1..65535_; Default: **3799**) | Port number of CoA (Change of Authorization) communication.               |
 | **address** (_IP/IPv6_**;** Default: )               | IP address of the RADIUS client.                                          |
 | **comment** (_string_; Default: )                    | Short description of the NAS.                                             |
 | **disabled** (_yes                                   | no_; Default: **no**)                                                     | Controls whether the entry is currently active or not. |
 | **name** (_string_; Default: )                       | Unique name of the RADIUS client.                                         |
 | **shared-secret** (_string_; Default: )              | Used to secure communication between a RADIUS server and a RADIUS client. |

**Commands**

| 
Property

 | 

Description

 |                       |
 | --------------------- | ------------------------------------------------ |
 | **reset-counters** () | Clear all statistics for specific RADIUS client. |

# Sessions

**Sub-menu:** `/user-manager session`

Sessions are logged only if accounting is enabled on NAS.

**Read-only properties**

| 
Property

 | 

Description

 |                                         |
 | --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | **acct-session-id** (_string_)          | Unique identification of the accounting session.                                                                                                                                                                                                                 |
 | **active** (_yes                        | no_)                                                                                                                                                                                                                                                             | Whether the session is currently used. |
 | **calling-station-id** (_string_)       | User's identifier, usually IP address or MAC address.                                                                                                                                                                                                            |
 | **download** (_Bytes_)                  | Amount of traffic downloaded.                                                                                                                                                                                                                                    |
 | **ended** (_datetime_)                  | Date and time when the session was closed. Empty for active sessions.                                                                                                                                                                                            |
 | **last-accounting-packet** (_datetime_) | Date and time when the last accounting update was received.                                                                                                                                                                                                      |
 | **nas-ip-address** (_IP address_)       | IP address of the NAS.                                                                                                                                                                                                                                           |
 | **nas-port-id** (_string_)              | Identifier of the NAS port that is authenticating the user.                                                                                                                                                                                                      |
 | **nas-port-type** (_string_)            | The port type (_physical_ or _virtual_) that is authenticating the user.                                                                                                                                                                                         |
 | **started** (_datetime_)                | Date and time when the session was established.                                                                                                                                                                                                                  |
 | **status** (_list of statuses_)         | Possible available statuses of a session: _start -_ accounting message _Start_ has been received, _stop -_ accounting message _Stop_ has been received, _interim - Interim update_ has been received, _close-acked_ - session is successfully closed, _expired._ |
 | **terminate-cause** (_string_)          | Reason why the session was closed.                                                                                                                                                                                                                               |
 | **upload** (_Bytes_)                    | Amount of traffic uploaded.                                                                                                                                                                                                                                      |
 | **uptime** (_time_)                     | Total logged uptime on the session.                                                                                                                                                                                                                              |
 | **user** (_string_)                     | Name of the user.                                                                                                                                                                                                                                                |
 | **user-address** (_IP address_)         | IP address provided to the user.                                                                                                                                                                                                                                 |

# Settings

**Sub-menu:** `/user-manager   `

**Properties**

| 
Property

 | 

Description

 |                                                        |
 | ------------------------------------------------------ | ----------------------------------------------------------- |
 | **accounting-port** (_integer_; Default: **1813**)     | Port to listen for RADIUS accounting requests.              |
 | **authentication-port** (_integer_; Default: **1812**) | Port to listen for RADIUS authentication requests.          |
 | **_certificate_** (_certificate_; Default: )           | Certificate for use in EAP TLS type authentication methods. |
 | **_enabled_** (_yes                                    | no_; Default: **no**)                                       | Whether the User Manager functionality is enabled.                                                                              |
 | **use-profiles** (_yes                                 | no_; Default: **no**)                                       | Whether to use **Profiles** and **Limitations**. When set to _no,_ only **User** configuration is required to run User Manager. |

## Advanced

**Sub-menu:** `/user-manager advanced`

**Properties**

| 
Property

 | 

Description

 |                                                  |
 | ------------------------------------------------ | ---------------------------------------------------------------------- |
 | **paypal-allow** (_yes                           | no_; Default: **no**)                                                  | Whether to enable PayPal functionality for User Manager.          |
 | **paypal-currency** (_string_; Default: **USD**) | The currency related to _price_ setting in which users will be billed. |
 | **paypal-password** (_string_; Default: )        | Password of your PayPal API account.                                   |
 | **paypal-signature** (_string_; Default: )       | Signature of your PayPal API account.                                  |
 | **paypal-use-sandbox** (_yes                     | no_; Default: **no**)                                                  | Whether to use PayPal's sandbox environment for testing purposes. |
 | **paypal-user** (_string_; Default: )            | Username of your PayPal API account.                                   |
 | **web-private-password** (_string_; Default: )   | Password for accessing _/um/PRIVATE/_ section over HTTP.               |
 | **web-private-username** (_string_; Default: )   | Username for accessing _/um/PRIVATE/_ section over HTTP.               |

# Users

**Sub-menu:** `/user-manager user`

**Properties**

| 
Property

 | 

Description

 |                                                   |
 | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
 | **attributes** (_array of attributes_; Default: ) | Custom set of **Attributes** with their values that will additionally be added to Access-Accept messages. |
 | **caller-id** (_string_; Default: )               | Allow user's authentication with a specific _Calling-Station-Id_ value.                                   |
 | **comment** (_string_; Default: )                 | Short description of the user.                                                                            |
 | **disabled** (_yes                                | no_; Default: **no**)                                                                                     | Controls whether the user can be used or not.                   |
 | **group** (_group_; Default: **default**)         | Name of the **Group** the user is associated to.                                                          |
 | **name** (_string_; Default: )                    | Username for session authentication.                                                                      |
 | **otp-secret** (_string_; Default: )              | A one-time password token that is attached to the password.                                               |
 |                                                   |
 | **password** (_string_; Default: )                | Password of the user for session authentication.                                                          |
 | **shared-users** (_integer                        | unlimited_; Default: **1**)                                                                               | Total amount of sessions the user can simultaneously establish. |

**Commands**

| 
Property

 | 

Description

 |                         |
 | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | **add-batch-users** ()  | The command can generate multiple user accounts based on various parameters.                                                                                  |
 | **generate-voucher** () | Generates a file based on _voucher-template_ that can be presented to the end user.                                                                           |
 | **monitor** ()          | Shows total statistics for a user. Stats include _total-uptime_, _total-download_, _total-upload_, _active-sessions_, _actual-profile_, _attributes-details_. |

# User Groups

**Sub-menu:** `/user-manager user group`

User groups defines common characteristics of multiple users such as allowed authentication methods and RADIUS attributes. There are two groups already present in User Manager called _default_ and _default-anonymous_.

**Properties**

| 
Property

 | 

Description

 |                                                   |
 | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | **attributes** (_array of attributes_; Default: ) | Custom set of **Attributes** with their values that will additionally be added to Access-Accept messages for users in this group.                                                                     |
 | **comment** (_string_; Default: )                 | Short description of the group.                                                                                                                                                                       |
 | **inner-auths** (_list of auths_; Default: )      | List of allowed authentication methods for tunneled (outer) authentication methods. Supported inner authentication methods - _ttls-pap_, _ttls-chap_, _ttls-mschap1_, _ttls-mschap2_, _peap-mschap2_. |
 | **name** (_string_; Default: )                    | Unique name of the group.                                                                                                                                                                             |
 | **outer-auths** (_list of auths_; Default: )      | List of allowed authentication methods. Supported outer authentication methods - _pap_, _chap_, _mschap1_, _mschap2_, _eap-tls_, _eap-ttls_, _eap-peap_, _eap-mschap2_.                               |

# User Profiles

**Sub-menu:** `/user-manager user-profile`

This menu assigns users with a profile and tracks the status of the profile. A single user can have multiple profiles assigned, however only one can be used at the same time. A user will seamlessly be switched to the next profile when currently active profile expires without dropping the user's session.

**Properties**

| 
Property

 | 

Description

 |                                    |
 | ---------------------------------- | ------------------------------------------- |
 | **profile** (_profile_; Default: ) | Name of the profile to assign for user.     |
 | **user** (_user_; Default: )       | Name of the user to use particular profile. |

**Read-only properties**

| 
Property

 | 

Description

 |                             |
 | --------------------------- | ----------------------------------------------- |
 | **end-time** (_datetime_)   | Date and time the **User Profile** will expire. |
 | **state** (_running active_ | running                                         | _used_) | Current state of the **User Profile**. _Running active -_ currently used profile by the user. _Running_ - a profile is ready to be used. _Used_ \- expired profile that can no longer be activated. |

**Commands**

| 
Property

 | 

Description

 |                              |
 | ---------------------------- | ------------------------------------------------- |
 | **activate-user-profile** () | Make a **User Profile** entry active immediately. |

# WEB Interface

Each user has access to his personal profile using a WEB interface. The WEB interface can be accessed by adding "/um/" directory to router's IP or domain, for example, [http://example.com/um/](http://router.ip/um/). Note that the WEB interface is affected by IP Services "www" and "www-ssl". The WEB interface can be customized using CSS, JavaScript and HTML.

**Customizable file reference**

| 
File

 | 

Description

 |                                 |
 | ------------------------------- | ------------------------------------------------------- |
 | **css/login.css**               | Cascading style sheet file used in login prompt page.   |
 | **css/user.css**                | Cascading style sheet file used in user's profile page. |
 | **img/PayPal\_mark\_37x23.gif** | PayPal logo image.                                      |
 | **img/ajax-loader.gif**         | Loading gif while processing page switching.            |
 | **img/mikrotik\_logo.png**      | MikroTik logo displayed on all pages.                   |
 | **js/generic.js**               | Javascript file used on all pages.                      |
 | **js/login.js**                 | Javascript file used in login prompt page.              |
 | **js/user.js**                  | Javascript file used in user's profile page.            |
 | **user/login\_dynamic.html**    | Layout of the login prompt page.                        |
 | **user/user\_dynamic.html**     | Layout of the user's profile page.                      |

# Application Guides

## Batch user creation

It is possible to create multiple new users with randomly generated username and password. For example, the following command will generate 3 new users with 6 lowercase symbols as the username and 6 lowercase, uppercase and numbers as the password.

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user-manager user</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">add-batch-users </code><code class="ros value">number-of-users</code><code class="ros plain">=3</code> <code class="ros value">password-characters</code><code class="ros plain">=lowercase,numbers,uppercase</code> <code class="ros value">password-length</code><code class="ros plain">=6</code> <code class="ros value">username-characters</code><code class="ros plain">=lowercase</code> <code class="ros value">username-length</code><code class="ros plain">=6</code></div></div></td></tr></tbody></table>

The command generated users can be seen by printing the user's table:

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user-manager user </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disab</code><code class="ros plain">led</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;&nbsp; </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"olsgkl"</code> <code class="ros value">password</code><code class="ros plain">=</code><code class="ros string">"86a6zH"</code> <code class="ros value">otp-secret</code><code class="ros plain">=</code><code class="ros string">""</code> <code class="ros value">group</code><code class="ros plain">=default</code> <code class="ros value">shared-users</code><code class="ros plain">=1</code> <code class="ros value">attributes</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1&nbsp;&nbsp; </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"lkbwss"</code> <code class="ros value">password</code><code class="ros plain">=</code><code class="ros string">"jaKY5V"</code> <code class="ros value">otp-secret</code><code class="ros plain">=</code><code class="ros string">""</code> <code class="ros value">group</code><code class="ros plain">=default</code> <code class="ros value">shared-users</code><code class="ros plain">=1</code> <code class="ros value">attributes</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">2&nbsp;&nbsp; </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"cwxbwu"</code> <code class="ros value">password</code><code class="ros plain">=</code><code class="ros string">"a62yZd"</code> <code class="ros value">otp-secret</code><code class="ros plain">=</code><code class="ros string">""</code> <code class="ros value">group</code><code class="ros plain">=default</code> <code class="ros value">shared-users</code><code class="ros plain">=1</code> <code class="ros value">attributes</code><code class="ros plain">=</code><code class="ros string">""</code></div></div></td></tr></tbody></table>

## Providing NAS with custom RADIUS attributes

It is possible to send additional RADIUS attributes during authentication process to provide NAS with custom information about the session, such as what IP address should be assigned to the supplicant or what address pool to use for address assigning.

### Static IP address for a user

To assign end user a static IP address, _Framed-IP-Address_ attribute can be used. When using static IP address allocation, _shared-sessions_ must be set to 1 to prevent cases when a user has multiple simultaneous sessions, but there is only one IP address. For example:

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user-manager user</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros value">name</code><code class="ros plain">=username]</code> <code class="ros value">shared-users</code><code class="ros plain">=1</code> <code class="ros value">attributes</code><code class="ros plain">=Framed-IP-Address:192.168.1.4</code></div></div></td></tr></tbody></table>

### Specifying address pool for group of users

We can group up multiple similar users and assign RADIUS attributes to all of them at once. First of all, create a new group:

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user-manager user group</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=location1</code> <code class="ros value">outer-auths</code><code class="ros plain">=chap,eap-mschap2,eap-peap,eap-tls,eap-ttls,mschap1,mschap2,pap</code> <code class="ros plain">\</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros value">inner-auths</code><code class="ros plain">=peap-mschap2,ttls-chap,ttls-mschap1,ttls-mschap2,ttls-pap</code> <code class="ros value">attributes</code><code class="ros plain">=Framed-Pool:pool1</code></div></div></td></tr></tbody></table>

Next step is to assign a user to the group:

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user-manager user</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros value">name</code><code class="ros plain">=username]</code> <code class="ros value">group</code><code class="ros plain">=location1</code></div></div></td></tr></tbody></table>

In this case an IP address from _pool1_ will be assigned to the user upon authentication - make sure _pool1_ is created on NAS device.

## Using TOTP (time-based one time password) for user authentication

User Manager supports time based authentication token addition to user's password field that is regenerated every 30 seconds.

OTP depends on clock, so make sure time settings are configured correctly.

TOTP works by having a shared secret on the supplicant (client) and the authentication server (User Manager). To configure TOTP on RouterOS, simply set the _otp-secret_ for the user. For example:

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user-manager user</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros value">name</code><code class="ros plain">=username]</code> <code class="ros value">password</code><code class="ros plain">=mypass</code> <code class="ros value">otp-secret</code><code class="ros plain">=mysecret</code></div></div></td></tr></tbody></table>

To calculate TOTP token on supplicant side, many widely available applications can be used, for example, Google Authenticator or [https://totp.app/](https://totp.app/). Adding _mysecret_ to TOTP token generator will provide a new unique 6 digit code that must be added to the users password.

![](https://help.mikrotik.com/docs/download/attachments/2555940/TOTP_generator.PNG?version=1&modificationDate=1657111279930&api=v2)

The following example will accept user's authentication with calculated TOTP token added to the common password until a new TOTP token is generated, for example,

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">User-Name=username</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">User-Password=mypass620872</code></div></div></td></tr></tbody></table>

## Exporting user credentials

### **Printable login credentials for single user**

To generate a single user's printable voucher card, simply use the _generate-voucher_ command. Specify the RouterOS ID number of the user or use _find_ command to specify a username. A template is already included in User Manager's installation available in Files section of your device. You can customize the template for your needs.

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user-manager user</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">generate-voucher </code><code class="ros value">voucher-template</code><code class="ros plain">=printable_vouchers.html</code> <code class="ros plain">[</code><code class="ros functions">find </code><code class="ros plain">where </code><code class="ros value">name</code><code class="ros plain">=username]</code></div></div></td></tr></tbody></table>

The generated voucher card is available by accessing the router using a WEB browser and navigating to _/um/PRIVATE/GENERATED/vouchers/gen\_printable\_vouchers.html_

By default the printable card looks like this:

![](https://help.mikrotik.com/docs/download/attachments/2555940/image.png?version=1&modificationDate=1663149747172&api=v2)

To access the PRIVATE path of the /um/ directory by the WEB browser, _private-username_ and _private-password_ must be configured. See **Settings** section.

It is possible to use different variables when generating vouchers. Currently, supported variables are:

$(username) - Represents User Manager username  
$(password) - Password of the username  
$(userprofname) - Profile that is active for the particular user  
$(userprofendtime) - Profile validity end time if specified

### Multiple user credential export

It is possible to generate a CSV or XML file with multiple or all user credentials at once by using the _export.xml_ or _export.csv_ as _voucher-template_.

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user-manager user</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">generate-voucher </code><code class="ros value">voucher-template</code><code class="ros plain">=export.xml</code> <code class="ros plain">[find]</code></div></div></td></tr></tbody></table>

The command generates an XML file _um5files/PRIVATE/GENERATED/vouchers/gen\_export.xml_ which can either be accessible by WEB browser or any other file access tools.

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">&lt;?xml version="1.0" encoding="UTF-8"?&gt;</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">&lt;users&gt;</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">&lt;user&gt;</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">&lt;username&gt;olsgkl&lt;/username&gt;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">&lt;password&gt;86a6zH&lt;/password&gt;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">&lt;/user&gt;</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">&lt;user&gt;</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">&lt;username&gt;lkbwss&lt;/username&gt;</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">&lt;password&gt;jaKY5V&lt;/password&gt;</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">&lt;/user&gt;</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">&lt;user&gt;</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">&lt;username&gt;cwxbwu&lt;/username&gt;</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">&lt;password&gt;a62yZd&lt;/password&gt;</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">&lt;/user&gt;</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">&lt;user&gt;</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">&lt;username&gt;username&lt;/username&gt;</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">&lt;password&gt;secretpassword&lt;/password&gt;</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">&lt;/user&gt;</code></div><div class="line number19 index18 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="text plain">&lt;/users&gt;</code></div></div></td></tr></tbody></table>

## Generating usage report

In cases where a presentable network usage information is required by companies billing or legal team an automated session export can be created using _generate-report_ command. The command requires an input of report template - an example of the template is available in _um5files/PRIVATE/TEMPLATES/reports/report\_default.html_. Example of the report generation:

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user-manager</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">generate-report </code><code class="ros value">report-template</code><code class="ros plain">=report_default.html</code> <code class="ros value">columns</code><code class="ros plain">=username,uptime,download,upload</code></div></div></td></tr></tbody></table>

The generated report is available by accessing the router using a WEB browser and navigating to _/um/PRIVATE/GENERATED/reports/gen\_report\_default.html_

_![](https://help.mikrotik.com/docs/download/attachments/2555940/Capture.PNG?version=2&modificationDate=1657102682105&api=v2)_

## Purchasing a profile

After logging into user's private profile by accessing the router's _/um/_ directory using WEB browser, for example, [http://example.com/um/,](http://example.com/um/,) he will be able to see all available **Profiles** in the respective menu. Profiles that have specified _price_ value will have _Buy this Profile_ button available.

![](https://help.mikrotik.com/docs/download/attachments/2555940/buy_profile.PNG?version=1&modificationDate=1657107133572&api=v2)

After pressing the _Buy this Profile_ button, the user will be asked to choose from available transaction service providers (currently only PayPal available) and later redirected to PayPal's payment processing page.

![](https://help.mikrotik.com/docs/download/attachments/2555940/paypal_purchase.PNG?version=1&modificationDate=1657107263155&api=v2)

When the payment is completed, the User Manager will ask PayPal to approve the transaction. After approval, the profile is assigned to the user and is ready to use.![](https://help.mikrotik.com/docs/download/attachments/2555940/purchase_complete.PNG?version=1&modificationDate=1657107833111&api=v2)

## Migrating from RouterOS v6

  

# Application Examples

## Basic L2TP/IPsec server with User Manager authentication

![](https://help.mikrotik.com/docs/download/attachments/2555940/scheme.jpg?version=1&modificationDate=1657282433977&api=v2)

**User Manager configuration**

Start off by enabling User Manager functionality.

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user-manager</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">enabled</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Allow receiving RADIUS requests from the localhost (the router itself).

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user-manager router</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=127.0.0.1</code> <code class="ros value">comment</code><code class="ros plain">=localhost</code> <code class="ros value">name</code><code class="ros plain">=local</code> <code class="ros value">shared-secret</code><code class="ros plain">=test</code></div></div></td></tr></tbody></table>

Next, add users and their credentials that clients will use to authenticate to the server.

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user-manager user</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=user1</code> <code class="ros value">password</code><code class="ros plain">=password</code></div></div></td></tr></tbody></table>

**Configuring RADIUS client**

For the router to use RADIUS server for user authentication, it is required to add a new RADIUS client that has the same shared secret that we already configured on User Manager.

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/radius</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=127.0.0.1</code> <code class="ros value">secret</code><code class="ros plain">=test</code> <code class="ros value">service</code><code class="ros plain">=ipsec</code></div></div></td></tr></tbody></table>

**L2TP/IPsec server configuration**

Configure the IP pool from which IP addresses will be assigned to the users and assign it to the PPP Profile.

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip pool</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=vpn-pool</code> <code class="ros value">range</code><code class="ros plain">=192.168.99.2-192.168.99.100</code></div><div class="line number3 index2 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/ppp pro</code><code class="ros plain">file</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">default-encryption </code><code class="ros value">local-address</code><code class="ros plain">=192.168.99.1</code> <code class="ros value">remote-address</code><code class="ros plain">=vpn-pool</code></div></div></td></tr></tbody></table>

Enable the use of RADIUS for PPP authentication.

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ppp aaa</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">use-radius</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Enable L2TP server with IPsec encryption.

[?](https://help.mikrotik.com/docs/display/ROS/User+Manager#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface l2tp-server server</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">enabled</code><code class="ros plain">=yes</code> <code class="ros value">use-ipsec</code><code class="ros plain">=required</code> <code class="ros value">ipsec-secret</code><code class="ros plain">=mySecret</code></div></div></td></tr></tbody></table>

That is it. Your router is now ready to accept L2TP/IPsec connections and authenticate them to the internal User Manager