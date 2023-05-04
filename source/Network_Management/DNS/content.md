# Introduction

Domain Name System (DNS) usually refers to the Phonebook of the Internet. In other words, DNS is a database that links strings (known as hostnames), such as [www.mikrotik.com](https://www.google.com) to a specific IP address, such as 159.148.147.196.

A MikroTik router with a DNS feature enabled can be set as a DNS cache for any DNS-compliant client. Moreover, the MikroTik router can be specified as a primary DNS server under its DHCP server settings. When the remote requests are enabled, the MikroTik router responds to TCP and UDP DNS requests on port 53.

When both static and dynamic servers are set, static server entries are preferred, however, it does not indicate that a static server will always be used (for example, previously query was received from a dynamic server, but static was added later, then a dynamic entry will be preferred).

When DNS server _allow-remote-requests_ are used make sure that you limit access to your server over TCP and UDP protocol port 53 only for known hosts.

There are several options on how you can manage DNS functionality on your LAN - use public DNS, use the router as a cache, or do not interfere with DNS configuration. Let us take as an example the following setup: Internet service provider (ISP) → Gateway (GW) → Local area network (LAN). The GW is RouterOS based device with the default configuration:

-   You do not configure any DNS servers on the "GW" DHCP server network configuration - the device will forward the DNS server IP address configuration received from \`ISP\` to \`LAN\` devices;
-   You configure DNS servers on the "GW" DHCP server network configuration - the device will give configured DNS servers to \`LAN\` devices (also "/ip dns set allow-remote-requests=yes_" must_ be enabled);
-   "dns-none" configured under DNS servers on "GW" DHCP server network configuration - the device will not forward any of the **dynamic** DNS servers to \`LAN\` devices;

## DNS configuration

DNS facility is used to provide domain name resolution for the router itself as well as for the clients connected to it.

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

 |                                                                      |
 | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | **allow-remote-requests** (_yes_                                     | _no_; Default: **no**)                                                                                                                                                            | Specifies whether to allow router usage as a DNS cache for remote clients. Otherwise, only the router itself will use DNS configuration. |
 | **cache-max-ttl** (_time_; Default: **1w**)                          | Maximum time-to-live for cache records. In other words, cache records will expire unconditionally after cache-max-TTL time. Shorter TTLs received from DNS servers are respected. |
 | **cache-size** (_integer\[64..4294967295\]_; Default: **2048**)      | Specifies the size of the DNS cache in KiB.                                                                                                                                       |
 | **max-concurrent-queries** (_integer_; Default: **100**)             | Specifies how many concurrent queries are allowed.                                                                                                                                |
 | **max-concurrent-tcp-sessions** (_integer_; Default: **20**)         | Specifies how many concurrent TCP sessions are allowed.                                                                                                                           |
 | **max-udp-packet-size** (_integer \[50..65507\]_; Default: **4096**) | Maximum size of allowed UDP packet.                                                                                                                                               |
 | **query-server-timeout** (_time_; Default: **2s**)                   | Specifies how long to wait for a query response from a server.                                                                                                                    |
 | **query-total-timeout** (_time_; Default: **10s**)                   | Specifies how long to wait for query response in total. Note that this setting must be configured taking into account "query-server-timeout" and the number of used DNS servers.  |
 | **servers** (_list of IPv4/IPv6 addresses_; Default: )               | List of DNS server IPv4/IPv6 addresses                                                                                                                                            |
 | **cache-used** (_integer_)                                           | Shows the currently used cache size in KiB                                                                                                                                        |
 | **dynamic-server** (_IPv4/IPv6 list_)                                | List of dynamically added DNS servers from different services, for example, DHCP.                                                                                                 |
 |                                                                      |

**doh-max-concurrent-queries** (_integer_; Default: **50**)

 | Specifies how many DoH concurrent queries are allowed. |
| 

**doh-max-server-connections** (_integer_; Default: **5**)

 | Specifies how many concurrent connections to the DoH server are allowed. |
| 

**doh-timeout** (_time_; Default: **5s**)

 | Specifies how long to wait for query response from the DoH server. |
| 

**use-doh-server** (_string; Default: )_

 | Specified which DoH server must be used for DNS queries. DoH functionality overrides "_servers_" usage if specified. The server must be specified with an "https://" prefix. |
| 

**verify-doh-cert**  (_yes_ | _no_; Default: **no**)

 | 

Specifies whether to validate the DoH server, when one is being used. Will use the "/certificate" list in order to verify server validity.

 |

  

[?](https://help.mikrotik.com/docs/display/ROS/DNS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@MikroTik] &gt; ip dns print&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">servers:</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">dynamic-servers: 10.155.0.1</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">use-doh-server:</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">verify-doh-cert: no</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;</code><code class="text plain">doh-max-server-connections: 5</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;</code><code class="text plain">doh-max-concurrent-queries: 50</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">doh-timeout: 5s</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">allow-remote-requests: yes</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">max-udp-packet-size: 4096</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">query-server-timeout: 2s</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">query-total-timeout: 10s</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">max-concurrent-queries: 100</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;</code><code class="text plain">max-concurrent-tcp-sessions: 20</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">cache-size: 2048KiB</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">cache-max-ttl: 1d</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">cache-used: 48KiB</code></div></div></td></tr></tbody></table>

Dynamic DNS servers are obtained from different facilities available in RouterOS, for example, DHCP client, VPN client, IPv6 Router Advertisements, etc. 

## DNS Cache

This menu provides two lists with DNS records stored on the server:

-   _"_/ip dns cache_"_: this menu provides a list with cache DNS entries that RouterOS cache can reply with to client requests ;
-   _"_/ip dns cache all_"_: This menu provides a complete list with all cached DNS records stored including also, for example, PTR records.

You can empty the DNS cache with the command: "/ip dns cache flush"_._

## DNS Static

The MikroTik RouterOS DNS cache has an additional embedded DNS server feature that allows you to configure multiple types of DNS entries that can be used by the DNS clients using the router as their DNS server. This feature can also be used to provide false DNS information to your network clients. For example, resolving any DNS request for a certain set of domains (or for the whole Internet) to your own page.

[?](https://help.mikrotik.com/docs/display/ROS/DNS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@MikroTik] /ip dns static add name=www.mikrotik.com address=10.0.0.1</code></div></div></td></tr></tbody></table>

The server is also capable of resolving DNS requests based on POSIX basic regular expressions so that multiple requests can be matched with the same entry. In case an entry does not conform with DNS naming standards, it is considered a regular expression. The list is ordered and checked from top to bottom. Regular expressions are checked first, then the plain records.

Use regex to match DNS requests:

[?](https://help.mikrotik.com/docs/display/ROS/DNS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@MikroTik] /ip dns static add regexp="[*mikrotik*]" address=10.0.0.2</code></div></div></td></tr></tbody></table>

If DNS static entries list matches the requested domain name, then the router will assume that this router is responsible for any type of DNS request for the particular name. For example, if there is only an "A" record in the list, but the router receives an "AAAA" request, then it will reply with an "A" record from the static list and will query the upstream server for the "AAAA" record. If a record exists, then the reply will be forwarded, if not, then the router will reply with an "ok" DNS reply without any records in it. If you want to override domain name records from the upstream server with unusable records, then you can, for example, add a static entry for the particular domain name and specify a dummy IPv6 address for it "::ffff".

List all of the configured DNS entries as an ordered list:

[?](https://help.mikrotik.com/docs/display/ROS/DNS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@MikroTik] /ip/dns/static/print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">Columns: NAME, REGEXP, ADDRESS, TTL</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain"># NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; REGEXP&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ADDRESS&nbsp;&nbsp; TTL</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="text plain">0 www.mikrotik.com&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 10.0.0.1&nbsp; 1d</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [*mikrotik*]&nbsp; 10.0.0.2&nbsp; 1d</code></div></div></td></tr></tbody></table>

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

 |                                      |
 | ------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
 | **address** (_IPv4/IPv6_)            | The address that will be used for "A" or "AAAA" type records.                                                     |
 | **cname** (_string__)_               | Alias name for a domain name.                                                                                     |
 | **forward-to**                       | The IP address of a domain name server to which a particular DNS request must be forwarded.                       |
 | **mx-exchange** (_string_)           | The domain name of the MX server.                                                                                 |
 | **name** (_string)_                  | Domain name.                                                                                                      |
 | **srv-port** (_integer_; Default: 0) | The TCP or UDP port on which the service is to be found.                                                          |
 | **srv-target**                       | The canonical hostname of the machine providing the service ends in a dot.                                        |
 | **text** (_string__)_                | Textual information about the domain name.                                                                        |
 | **type** (_A_                        | _AAAA_                                                                                                            | _CNAME_ | _FWD_ | _MX_ | _NS_ | _NXDOMAIN_ | _SRV_ | _TXT_ ; Default: _A_) | Type of the DNS record. |
 | **address-list** (_string__)_        | Name of the Firewall address list to which address must be dynamically added when some request matches the entry. |
 | **comment** (_string__)_             | Comment about the domain name record.                                                                             |
 |                                      |

**disabled** (_yes_ | _no_; Default: yes)

 | Whether the DNS record is active. |
| 

**match-subdomain** (_yes_ | _no_; Default: no)

 | Whether the record will match requests for subdomains. |
| 

**mx-preference** (_integer_; Default: 0)

 | Preference of the particular MX record. |
| 

**ns** (_string_)

 | Name of the authoritative domain name server for the particular record. |
| 

**regexp** (POSIX regex)

 | Regular expression against which domain names should be verified. |
| 

**srv-priority** (_integer_; Default: 0)

 | 

Priority of the particular SRV record.

 |
| 

**src-weight** (_integer_; Default: 0)

 | 

Weight of the particular SRC record.

 |
| 

**ttl** (_time_; Default: _24h_)

 | 

Maximum time-to-live for cached records.

 |

Regexp is case-sensitive, but DNS requests are not case sensitive, RouterOS converts DNS names to lowercase before matching any static entries. You should write regex only with lowercase letters. Regular expression matching is significantly slower than plain text entries, so it is advised to minimize the number of regular expression rules and optimize the expressions themselves.

Be careful when you configure regex through mixed user interfaces - CLI and GUI. Adding the entry itself might require escape characters when added from CLI. It is recommended to add an entry and the execute print command in order to verify that regex was not changed during addition.

# DNS over HTTPS (DoH)

Starting from RouterOS version v6.47 it is possible to use DNS over HTTPS (DoH). DoH uses HTTPS protocol to send and receive DNS requests for better data integrity. The main goal is to provide privacy by eliminating "man-in-the-middle" attacks (MITM). Currently, DoH is not compatible with FWD-type static entries, in order to utilize FWD entries, DoH must not be configured.   
  
Watch our [video about this feature](https://youtu.be/w4erB0VzyIE). 

It is strongly recommended to import the root CA certificate of the DoH server you have chosen to use for increased security. We strongly suggest not using third-party download links for certificate fetching. Use the Certificate Authority's own website.

There are various ways to find out what root CA certificate is necessary. The easiest way is by using your WEB browser, navigating to the DoH site, and checking the security of the website. Using, for example, Firefox we can see that DigiCert Global Root CA is used by the Cloudflare DoH server. You can download the certificate straight from the browser or navigate to the DigiCert website and fetch the certificate from a trusted source. 

![](https://help.mikrotik.com/docs/download/attachments/37748767/Rootca.PNG?version=1&modificationDate=1628148171413&api=v2)

Download the certificate, upload it to your router and import it: 

[?](https://help.mikrotik.com/docs/display/ROS/DNS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/certificate </code><code class="ros functions">import </code><code class="ros value">file-name</code><code class="ros plain">=DigiCertGlobalRootCA.crt.pem</code></div></div></td></tr></tbody></table>

Configure the DoH server: 

[?](https://help.mikrotik.com/docs/display/ROS/DNS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip dns </code><code class="ros functions">set </code><code class="ros value">use-doh-server</code><code class="ros plain">=<a href="https://cloudflare-dns.com/dns-query">https://cloudflare-dns.com/dns-query</a></code> <code class="ros value">verify-doh-cert</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Note that you need at least one regular DNS server configured for the router to resolve the DoH hostname itself. If you do not have any dynamical or static DNS server configured, add a static DNS entry for the DoH server domain name like this: 

[?](https://help.mikrotik.com/docs/display/ROS/DNS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip dns </code><code class="ros functions">set </code><code class="ros value">servers</code><code class="ros plain">=1.1.1.1</code></div></div></td></tr></tbody></table>

RouterOS prioritizes DoH over the DNS server if both are configured on the device.