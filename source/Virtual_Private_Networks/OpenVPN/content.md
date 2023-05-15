# Overview

The OpenVPN security model is based on SSL, the industry standard for secure communications via the internet. OpenVPN implements OSI layer 2 or 3 secure network extensions using the SSL/TLS protocol. 

# Introduction

OpenVPN has been ported to various platforms, including Linux and Windows, and its configuration is likewise on each of these systems, so it makes it easier to support and maintain. OpenVPN can run over User Datagram Protocol (UDP) or Transmission Control Protocol (TCP) transports, multiplexing created SSL tunnels on a single TCP/UDP port. OpenVPN is one of the few VPN protocols that can make use of a proxy, which might be handy sometimes.

# Limitations

Currently, unsupported OpenVPN features:

-   LZO compression
-   TLS authentication
-   authentication without username/password

OpenVPN username is limited to 27 characters and the password to 233 characters.

# OVPN Client

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

|                                            |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| **add-default-route** (_yes_               | _no_; Default: **no**)                                                                                                | Whether to add OVPN remote address as a default route.                  |
| **auth** (_md5_                            | _sha1_                                                                                                                | _null_                                                                  | _sha256_     | _sha512_; Default: **sha1**) | Allowed authentication methods. |
| **certificate** (_string_                  | _none_; Default: **none**)                                                                                            | Name of the client certificate                                          |
| **cipher** (_null_                         | _aes128-cbc_                                                                                                          | _aes128-gcm_                                                            | _aes192-cbc_ | _aes192-gcm_                 | _aes256-cbc_                    | _aes256-gcm_ | _blowfish128_; Default: **blowfish128**) | Allowed ciphers. In order to use GCM type ciphers, the "auth" parameter must be set to "null", because GCM cipher is also responsible for "auth", if used. |
| **comment** (_string_; Default: )          | Descriptive name of an item                                                                                           |
| **connect-to** (_IP_; Default: )           | Remote address of the OVPN server.                                                                                    |
| **disabled** (_yes_                        | _no_; Default: **yes**)                                                                                               | Whether the interface is disabled or not. By default it is disabled.    |
| **mac-address** (_MAC_; Default: )         | Mac address of OVPN interface. Will be automatically generated if not specified.                                      |
| **max-mtu** (_integer_; Default: **1500**) | Maximum Transmission Unit. Max packet size that the OVPN interface will be able to send without packet fragmentation. |
| **mode** (_ip_                             | _ethernet_; Default: **ip**)                                                                                          | Layer3 or layer2 tunnel mode (alternatively tun, tap)                   |
| **name** (_string_; Default: )             | Descriptive name of the interface.                                                                                    |
| **password** (_string_; Default: **""**)   | Password used for authentication.                                                                                     |
| **port** (_integer_; Default: **1194**)    | Port to connect to.                                                                                                   |
| **profile** (_name_; Default: **default**) | Specifies which PPP profile configuration will be used when establishing the tunnel.                                  |
| **protocol** (_tcp_                        | _udp_; Default: **tcp**)                                                                                              | indicates the protocol to use when connecting with the remote endpoint. |
| **verify-server-certificate** (_yes_       | _no_; Default: **no**)                                                                                                |

Checks the certificates CN or SAN against the "connect-to" parameter. The IP or hostname must be present in the server's certificate.

 |
| **tls-version** (_any_ | _only-1.2_; Default: **any**) | Specifies which TLS versions to allow |
| **use-peer-dns** (_yes_ | _no_; Default: **no**) | Whether to add DNS servers provided by the OVPN server to IP/DNS configuration. |
| 

**route-nopull** (_yes_ | _no_; Default: **no**)

 | Specifies whether to allow the OVPN server to add routes to the OVPN client instance routing table. |
| **user** (_string_; Default: ) | User name used for authentication. |

Also, it is possible to import the OVPN client configuration from a .ovpn configuration file. Such a file usually is provided from the OVPN server side and already includes configuration so you need to worry only about a few parameters.

[?](https://help.mikrotik.com/docs/display/ROS/OpenVPN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/ovpn-client/import-ovpn-configuration ovpn-password=secure</code><code class="ros plain">password \</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros value">key-passphrase</code><code class="ros plain">=certificatekeypassphrase</code> <code class="ros value">ovpn-user</code><code class="ros plain">=myuserid</code> <code class="ros value">skip-cert-import</code><code class="ros plain">=no</code></div></div></td></tr></tbody></table>

# OVPN Server

An interface is created for each tunnel established to the given server. There are two types of interfaces in the OVPN server's configuration

-   Static interfaces are added administratively if there is a need to reference the particular interface name (in firewall rules or elsewhere) created for the particular user.
-   Dynamic interfaces are added to this list automatically whenever a user is connected and its username does not match any existing static entry (or in case the entry is active already, as there can not be two separate tunnel interfaces referenced by the same name).

Dynamic interfaces appear when a user connects and disappear once the user disconnects, so it is impossible to reference the tunnel created for that use in router configuration (for example, in the firewall), so if you need a persistent rule for that user, create a static entry for him/her. Otherwise, it is safe to use dynamic configuration.

In both cases PPP users must be configured properly - static entries do not replace PPP configuration.

## Properties

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

|                                                    |
| -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **auth** (_md5_                                    | _sha1_                                                                                                                | _null_                                                                                                                                                                                                                                                                     | _sha256_     | _sha512_; Default: **sha1,md5,sha256,sha512**) | Authentication methods that the server will accept. |
| **certificate** (_name_                            | _none_; Default: **none**)                                                                                            | Name of the certificate that the OVPN server will use.                                                                                                                                                                                                                     |
| **cipher** (_null_                                 | _aes128-cbc_                                                                                                          | _aes128-gcm_                                                                                                                                                                                                                                                               | _aes192-cbc_ | _aes192-gcm_                                   | _aes256-cbc_                                        | _aes256-gcm_ | _blowfish128_; Default: **aes128-cbc,blowfish128**) | Allowed ciphers. |
| **default-profile** (_name_; Default: **default**) | Default profile to use.                                                                                               |
| **enabled** (_yes_                                 | _no_; Default: **no**)                                                                                                | Defines whether the OVPN server is enabled or not.                                                                                                                                                                                                                         |
| **protocol (_tcp_                                  | _udp_; Default: tcp)**                                                                                                | indicates the protocol to use when connecting with the remote endpoint.                                                                                                                                                                                                    |
| **keepalive-timeout** (_integer_                   | _disabled_; Default: **60**)                                                                                          | Defines the time period (in seconds) after which the router is starting to send keepalive packets every second. If no traffic and no keepalive responses have come for that period of time (i.e. 2 \* keepalive-timeout), not responding client is proclaimed disconnected |
| **mac-address** (_MAC_; Default: )                 | Automatically generated MAC address of the server.                                                                    |
| **max-mtu** (_integer_; Default: **1500**)         | Maximum Transmission Unit. Max packet size that the OVPN interface will be able to send without packet fragmentation. |
| **mode** (_ip_                                     | _ethernet_; Default: **ip**)                                                                                          | Layer3 or layer2 tunnel mode (alternatively tun, tap)                                                                                                                                                                                                                      |
| **netmask** (_integer_; Default: **24**)           | Subnet mask to be applied to the client.                                                                              |
| **port** (_integer_; Default: **1194**)            | Port to run the server on.                                                                                            |
| **require-client-certificate** (_yes_              | _no_; Default: **no**)                                                                                                | If set to yes, then the server checks whether the client's certificate belongs to the same certificate chain.                                                                                                                                                              |
| **redirect-gateway** (_def1_                       | _disabled_                                                                                                            | _ipv6;_ Default: **disabled**)                                                                                                                                                                                                                                             |

Specifies what kind of routes the OVPN client must add to the routing table. 

`def1` – Use this flag to override the default gateway by using 0.0.0.0/1 and 128.0.0.0/1 rather than 0.0.0.0/0. This has the benefit of overriding but not wiping out the original default gateway.  
`disabled` - Do not send redirect-gateway flags to the OVPN client.  
`ipv6` - Redirect IPv6 routing into the tunnel on the client side. This works similarly to the def1 flag, that is, more specific IPv6 routes are added (2000::/4 and 3000::/4), covering the whole IPv6 unicast space.

 |
| **enable-tun-ipv6** (y_es_ | _no;_ Default: **no**) | 

Specifies if IPv6 IP tunneling mode should be possible with this OVPN server.

 |
| **ipv6-prefix-len** (_integer;_ Default: **64**) | 

Length of IPv6 prefix for IPv6 address which will be used when generating OVPN interface on the server side.

 |
| **tun-server-ipv6** (_IPv6 prefix;_ Default: **::**) | 

IPv6 prefix address which will be used when generating the OVPN interface on the server side.

 |

Also, it is possible to prepare a .ovpn file for the OVPN client which can be easily imported on the end device.

[?](https://help.mikrotik.com/docs/display/ROS/OpenVPN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface/ovpn-server/server/export-client-configuration ca-certificate=myCa.crt \</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros value">client-certificate</code><code class="ros plain">=client1.crt</code> <code class="ros value">client-cert-key</code><code class="ros plain">=client1.key</code> <code class="ros value">server-address</code><code class="ros plain">=192.168.88.1</code></div></div></td></tr></tbody></table>

It is very important that the date on the router is within the range of the installed certificate's date of expiration. To overcome any certificate verification problems, enable **NTP** date synchronization on both the server and the client.

# Example

## Setup Overview

![](https://help.mikrotik.com/docs/download/attachments/2031655/OpenVPN.png?version=1&modificationDate=1615380050324&api=v2)

Assume that Office public IP address is 2.2.2.2 and we want two remote OVPN clients to have access to 10.5.8.20 and 192.168.55.0/24 networks behind the office gateway. 

## Creating Certificates

All certificates can be created on the RouterOS server using the certificate manager. [See example >>](https://wiki.mikrotik.com/wiki/Manual:Create_Certificates#Generate_certificates_on_RouterOS "Manual:Create Certificates").

For the simplest setup, you need only an OVPN server certificate.

## Server Config

The first step is to create an IP pool from which client addresses will be assigned and some users.

[?](https://help.mikrotik.com/docs/display/ROS/OpenVPN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip pool </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ovpn-pool</code> <code class="ros value">range</code><code class="ros plain">=192.168.77.2-192.168.77.254</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ppp pro</code><code class="ros plain">file </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ovpn</code> <code class="ros value">local-address</code><code class="ros plain">=192.168.77.1</code> <code class="ros value">remote-address</code><code class="ros plain">=ovpn-pool</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/ppp secret</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=client1</code> <code class="ros value">password</code><code class="ros plain">=123</code> <code class="ros value">profile</code><code class="ros plain">=ovpn</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=client2</code> <code class="ros value">password</code><code class="ros plain">=234</code> <code class="ros value">profile</code><code class="ros plain">=ovpn</code></div></div></td></tr></tbody></table>

Assume that the server certificate is already created and named "server" 

[?](https://help.mikrotik.com/docs/display/ROS/OpenVPN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ovpn-server server </code><code class="ros functions">set </code><code class="ros value">enabled</code><code class="ros plain">=yes</code> <code class="ros value">certificate</code><code class="ros plain">=server</code></div></div></td></tr></tbody></table>

## Client Config

Since RouterOS does not support route-push you need to add manually which networks you want to access over the tunnel. 

[?](https://help.mikrotik.com/docs/display/ROS/OpenVPN#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ovpn-client</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ovpn-client1</code> <code class="ros value">connect-to</code><code class="ros plain">=2.2.2.2</code> <code class="ros value">user</code><code class="ros plain">=client1</code> <code class="ros value">password</code><code class="ros plain">=123</code> <code class="ros value">disabled</code><code class="ros plain">=no</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip route</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=10.5.8.20</code> <code class="ros value">gateway</code><code class="ros plain">=ovpn-client1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=192.168.55.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=ovpn-client1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/ip firewall nat </code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">action</code><code class="ros plain">=masquerade</code> <code class="ros value">out-interface</code><code class="ros plain">=ovpn-client1</code></div></div></td></tr></tbody></table>