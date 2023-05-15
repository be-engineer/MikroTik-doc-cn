# Introduction

  
**Internet Protocol Security (IPsec)** is a set of protocols defined by the Internet Engineering Task Force (IETF) to secure packet exchange over unprotected IP/IPv6 networks such as the Internet.

  
IPsec protocol suite can be divided into the following groups:

-   **Internet Key Exchange (IKE)** protocols. Dynamically generates and distributes cryptographic keys for AH and ESP.
-   **Authentication Header (AH)** RFC 4302
-   **Encapsulating Security Payload (ESP)** RFC 4303

# Internet Key Exchange Protocol (IKE)

The Internet Key Exchange (IKE) is a protocol that provides authenticated keying material for the Internet Security Association and Key Management Protocol (ISAKMP) framework. There are other key exchange schemes that work with ISAKMP, but IKE is the most widely used one. Together they provide means for authentication of hosts and automatic management of security associations (SA).

Most of the time IKE daemon is doing nothing. There are two possible situations when it is activated:

There is some traffic caught by a policy rule which needs to become encrypted or authenticated, but the policy doesn't have any SAs. The policy notifies the IKE daemon about that, and the IKE daemon initiates a connection to a remote host. IKE daemon responds to remote connection. In both cases, peers establish a connection and execute 2 phases:

-   **Phase 1** - The peers agree upon algorithms they will use in the following IKE messages and authenticate. The keying material used to derive keys for all SAs and to protect following ISAKMP exchanges between hosts is generated also. This phase should match the following settings:
    -   authentication method
    -   DH group
    -   encryption algorithm
    -   exchange mode
    -   hash algorithm
    -   NAT-T
    -   DPD and lifetime (optional)

-   **Phase 2** - The peers establish one or more SAs that will be used by IPsec to encrypt data. All SAs established by the IKE daemon will have lifetime values (either limiting time, after which SA will become invalid, or the amount of data that can be encrypted by this SA, or both). This phase should match the following settings:
    -   IPsec protocol
    -   mode (tunnel or transport)
    -   authentication method
    -   PFS (DH) group
    -   lifetime

There are two lifetime values - soft and hard. When SA reaches its soft lifetime threshold, the IKE daemon receives a notice and starts another phase 2 exchange to replace this SA with a fresh one. If SA reaches a hard lifetime, it is discarded.

Phase 1 is not re-keyed if DPD is disabled when the lifetime expires, only phase 2 is re-keyed. To force phase 1 re-key, enable DPD.

PSK authentication was known to be vulnerable against Offline attacks in "aggressive" mode, however recent discoveries indicate that offline attack is possible also in the case of "main" and "ike2" exchange modes. A general recommendation is to avoid using the PSK authentication method.

IKE can optionally provide a Perfect Forward Secrecy (PFS), which is a property of key exchanges, that, in turn, means for IKE that compromising the long term phase 1 key will not allow to easily gain access to all IPsec data that is protected by SAs established through this phase 1. It means an additional keying material is generated for each phase 2.

The generation of keying material is computationally very expensive. Exempli Gratia, the use of the modp8192 group can take several seconds even on a very fast computer. It usually takes place once per phase 1 exchange, which happens only once between any host pair and then is kept for a long time. PFS adds this expensive operation also to each phase 2 exchange.

## Diffie-Hellman Groups

Diffie-Hellman (DH) key exchange protocol allows two parties without any initial shared secret to create one securely. The following Modular Exponential (MODP) and Elliptic Curve (EC2N) Diffie-Hellman (also known as "Oakley") Groups are supported:

| 
Diffie-Hellman Group

 | 

Name

 | 

Reference

|     |
| --- |  |  |
|     |

Diffie-Hellman Group

 | 

Name

 | 

Reference

|          |
| -------- | ------------------------- | -------- |
| Group 1  | 768 bits MODP group       | RFC 2409 |
| Group 2  | 1024 bits MODP group      | RFC 2409 |
| Group 3  | EC2N group on GP(2^155)   | RFC 2409 |
| Group 4  | EC2N group on GP(2^185)   | RFC 2409 |
| Group 5  | 1536 bits MODP group      | RFC 3526 |
| Group 14 | 2048 bits MODP group      | RFC 3526 |
| Group 15 | 3072 bits MODP group      | RFC 3526 |
| Group 16 | 4096 bits MODP group      | RFC 3526 |
| Group 17 | 6144 bits MODP group      | RFC 3526 |
| Group 18 | 8192 bits MODP group      | RFC 3526 |
| Group 19 | 256 bits random ECP group | RFC 5903 |
| Group 20 | 384 bits random ECP group | RFC 5903 |
| Group 21 | 521 bits random ECP group | RFC 5903 |

More on standards can be found [here](https://www.iana.org/assignments/ipsec-registry/ipsec-registry.xhtml).

## IKE Traffic

To avoid problems with IKE packets hit some SPD rule and require to encrypt it with not yet established SA (that this packet perhaps is trying to establish), locally originated packets with UDP source port 500 are not processed with SPD. The same way packets with UDP destination port 500 that are to be delivered locally are not processed in incoming policy checks.

## Setup Procedure

To get IPsec to work with automatic keying using IKE-ISAKMP you will have to configure policy, peer, and proposal (optional) entries.

IPsec is very sensitive to time changes. If both ends of the IPsec tunnel are not synchronizing time equally(for example, different NTP servers not updating time with the same timestamp), tunnels will break and will have to be established again.

## EAP Authentication methods

| 
Outer Auth

 | 

Inner Auth

|     |
| --- |  |
|     |

Outer Auth

 | 

Inner Auth

|              |
| ------------ |  |
| EAP-GTC      |
|              |
| EAP-MD5      |
|              |
| EAP-MSCHAPv2 |
|              |
| EAP-PEAPv0   |

EAP-MSCHAPv2  
EAP-GPSK  
EAP-GTC  
EAP-MD5  
EAP-TLS

 |
| EAP-SIM |   
 |
| EAP-TLS |   
 |
| EAP-TTLS | 

PAP  
CHAP  
MS-CHAP  
MS-CHAPv2  
EAP-MSCHAPv2  
EAP-GTC  
EAP-MD5  
EAP-TLS

 |

**EAP-TLS** on Windows is called "Smart Card or other certificates".

# Authentication Header (AH)

AH is a protocol that provides authentication of either all or part of the contents of a datagram through the addition of a header that is calculated based on the values in the datagram. What parts of the datagram are used for the calculation, and the placement of the header depends on whether tunnel or transport mode is used.

The presence of the AH header allows to verify the integrity of the message but doesn't encrypt it. Thus, AH provides authentication but not privacy. Another protocol (ESP) is considered superior, it provides data privacy and also its own authentication method.

RouterOS supports the following authentication algorithms for AH:

-   SHA2 (256, 512)
-   SHA1
-   MD5

## Transport mode

In transport mode, the AH header is inserted after the IP header. IP data and header is used to calculate authentication value. IP fields that might change during transit, like TTL and hop count, are set to zero values before authentication.

## Tunnel mode

In tunnel mode, the original IP packet is encapsulated within a new IP packet. All of the original IP packets are authenticated.

# Encapsulating Security Payload (ESP)

  

Encapsulating Security Payload (ESP) uses shared key encryption to provide data privacy. ESP also supports its own authentication scheme like that used in AH.

ESP packages its fields in a very different way than AH. Instead of having just a header, it divides its fields into three components:

-   **ESP Header** - Comes before the encrypted data and its placement depends on whether ESP is used in transport mode or tunnel mode.
-   **ESP Trailer** - This section is placed after the encrypted data. It contains padding that is used to align the encrypted data.
-   **ESP Authentication Data** - This field contains an Integrity Check Value (ICV), computed in a manner similar to how the AH protocol works, for when ESP's optional authentication feature is used.

## Transport mode

In transport mode, the ESP header is inserted after the original IP header. ESP trailer and authentication value are added to the end of the packet. In this mode only the IP payload is encrypted and authenticated, the IP header is not secured.

![](https://help.mikrotik.com/docs/download/attachments/11993097/800px-ESP-transport_wiki.png?version=1&modificationDate=1579172163851&api=v2)

  

## Tunnel mode

In tunnel mode, an original IP packet is encapsulated within a new IP packet thus securing IP payload and IP header.

![](https://help.mikrotik.com/docs/download/attachments/11993097/ESP-tunnel_wiki.png?version=1&modificationDate=1579172215119&api=v2)

## Encryption algorithms

RouterOS ESP supports various encryption and authentication algorithms.

Authentication:

-   **MD5**
-   **SHA1**
-   **SHA2 (256-bit, 512-bit)**

Encryption:

-   **AES** - 128-bit, 192-bit, and 256-bit key AES-CBC, AES-CTR, and AES-GCM algorithms;
-   **Blowfish** - added since v4.5
-   **Twofish** - added since v4.5
-   **Camellia** - 128-bit, 192-bit, and 256-bit key Camellia encryption algorithm added since v4.5
-   **DES** - 56-bit DES-CBC encryption algorithm;
-   **3DES** - 168-bit DES encryption algorithm;

## Hardware acceleration

Hardware acceleration allows doing a faster encryption process by using a built-in encryption engine inside the CPU.

List of devices with hardware acceleration is available [here](https://mikrotik.com/products?filter&s=c&f=%5B%22ipsec%22%5D)

<table class="wrapped relative-table confluenceTable" style="width: 95.6452%;"><colgroup><col style="width: 21.4406%;"><col style="width: 4.56606%;"><col style="width: 5.16163%;"><col style="width: 5.22781%;"><col style="width: 4.83076%;"><col style="width: 4.36753%;"><col style="width: 5.09546%;"><col style="width: 5.22781%;"><col style="width: 4.83076%;"><col style="width: 4.36753%;"><col style="width: 5.09546%;"><col style="width: 5.22781%;"><col style="width: 4.83076%;"><col style="width: 4.36753%;"><col style="width: 5.09546%;"><col style="width: 5.22781%;"><col style="width: 4.83076%;"></colgroup><tbody><tr><th rowspan="2" style="width: 401.0px;" class="confluenceTh">CPU</th><th colspan="4" style="width: 255.0px;" class="confluenceTh">DES and 3DES</th><th colspan="4" style="width: 255.0px;" class="confluenceTh">AES-CBC</th><th colspan="4" style="width: 255.0px;" class="confluenceTh">AES-CTR</th><th colspan="4" style="width: 255.0px;" class="confluenceTh">AES-GCM</th></tr><tr><th style="width: 52.0px;" class="confluenceTh">MD5</th><th style="width: 57.0px;" class="confluenceTh">SHA1</th><th style="width: 73.0px;" class="confluenceTh">SHA256</th><th style="width: 73.0px;" class="confluenceTh">SHA512</th><th style="width: 52.0px;" class="confluenceTh">MD5</th><th style="width: 57.0px;" class="confluenceTh">SHA1</th><th style="width: 73.0px;" class="confluenceTh">SHA256</th><th style="width: 73.0px;" class="confluenceTh">SHA512</th><th style="width: 52.0px;" class="confluenceTh">MD5</th><th style="width: 57.0px;" class="confluenceTh">SHA1</th><th style="width: 73.0px;" class="confluenceTh">SHA256</th><th style="width: 73.0px;" class="confluenceTh">SHA512</th><th style="width: 52.0px;" class="confluenceTh">MD5</th><th style="width: 57.0px;" class="confluenceTh">SHA1</th><th style="width: 73.0px;" class="confluenceTh">SHA256</th><th style="width: 73.0px;" class="confluenceTh">SHA512</th></tr><tr><td style="width: 401.0px;" class="confluenceTd">88F7040</td><td class="highlight-red confluenceTd" data-highlight-colour="red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">AL21400</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">AL32400</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">AL52400</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td></tr><tr><td class="confluenceTd">AL73400</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">IPQ-4018 / IPQ-4019</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes*</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes*</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes*</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes*</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">IPQ-6010</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">IPQ-8064</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes*</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes*</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes*</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes*</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">MT7621A</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 52.0px;" title="Background colour : Yellow">yes****</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes****</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes****</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">P1023NSN5CFB</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes**</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes**</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes**</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes**</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">P202ASSE2KFB</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td></tr><tr><td style="width: 401.0px;" class="confluenceTd"><span class="markedContent"><span>PPC460GT</span></span></td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 52.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 52.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">TLR4 (TILE)</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">x86 (AES-NI)</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 52.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 52.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 52.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td></tr></tbody></table>

\* supported only 128 bit and 256 bit key sizes

\*\* only manufactured since 2016, serial numbers that begin with number 5 and 7

\*\*\* AES-CBC and AES-CTR only encryption is accelerated, hashing done in software

\*\*\*\* DES is not supported, only 3DES and AES-CBC

IPsec throughput results of various encryption and hash algorithm combinations are published on the [MikroTik products page](https://mikrotik.com/product/).

# Policies

The policy table is used to determine whether security settings should be applied to a packet.

**Properties**

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

|                      |
| -------------------- | ------- |
| **action** (_discard | encrypt | none_; Default: **encrypt**) | Specifies what to do with the packet matched by the policy. |

-   none - pass the packet unchanged.
-   discard - drop the packet.
-   encrypt - apply transformations specified in this policy and it's SA.

 |
| **comment** (_string_; Default: ) | Short description of the policy. |
| **disabled** (_yes | no_; Default: **no**) | Whether a policy is used to match packets. |
| **dst-address** (_IP/IPv6 prefix_; Default: **0.0.0.0/32**) | Destination address to be matched in packets. Applicable when tunnel mode (tunnel=yes) or template (template=yes) is used. |
| **dst-port** (_integer:0..65535 | any_; Default: **any**) | Destination port to be matched in packets. If set to any all ports will be matched. |
| **group** (_string_; Default: **default**) | Name of the policy group to which this template is assigned. |
| **ipsec-protocols** (_ah | esp_; Default: **esp**) | Specifies what combination of Authentication Header and Encapsulating Security Payload protocols you want to apply to matched traffic. |
| **level** (_require | unique | use_; Default: **require**) | Specifies what to do if some of the SAs for this policy cannot be found:

-   use - skip this transform, do not drop the packet, and do not acquire SA from IKE daemon;
-   require - drop the packet and acquire SA;
-   unique - drop the packet and acquire a unique SA that is only used with this particular policy. It is used in setups where multiple clients can sit behind one public IP address (clients behind NAT).

 |
| **peer** (_string_; Default: ) | Name of the peer on which the policy applies. |
| **proposal** (_string_; Default: **default**) | Name of the proposal template that will be sent by IKE daemon to establish SAs for this policy. |
| **protocol** (_all | egp | ggp| icmp | igmp | ..._; Default: **all**) | IP packet protocol to match. |
| **src-address** (_ip/ipv6 prefix_; Default: **0.0.0.0/32**) | Source address to be matched in packets. Applicable when tunnel mode (tunnel=yes) or template (template=yes) is used. |
| **src-port** (_any | integer:0..65535_; Default: **any**) | Source port to be matched in packets. If set to any all ports will be matched. |
| **template** (_yes | no_; Default: **no**) | Creates a template and assigns it to a specified policy group.

Following parameters are used by template:

-   group - name of the policy group to which this template is assigned;
-   src-address, dst-address - Requested subnet must match in both directions(for example 0.0.0.0/0 to allow all);
-   protocol - protocol to match, if set to all, then any protocol is accepted;
-   proposal - SA parameters used for this template;
-   level - useful when unique is required in setups with multiple clients behind NAT.

 |
| **tunnel** (_yes | no_; Default: **no**) | Specifies whether to use tunnel mode. |

**Read-only properties**

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

|                                                         |
| ------------------------------------------------------- | --------------------------------------------------------------- |
| **active** (_yes                                        | no_)                                                            | Whether this policy is currently in use.                                                                             |
| **default** (_yes                                       | no_)                                                            | Whether this is a default system entry.                                                                              |
| **dynamic** (_yes                                       | no_)                                                            | Whether this is a dynamically added or generated entry.                                                              |
| **invalid** (_yes                                       | no_)                                                            | Whether this policy is invalid - the possible cause is a duplicate policy with the same src-address and dst-address. |
| **ph2-count** (_integer_)                               | A number of active phase 2 sessions associated with the policy. |
| **ph2-state** (_expired                                 | no-phase2                                                       | established_)                                                                                                        | Indication of the progress of key establishing. |
| **sa-dst-address** (_ip/ipv6 address_; Default: **::**) | SA destination IP/IPv6 address (remote peer).                   |
| **sa-src-address** (_ip/ipv6 address_; Default: **::**) | SA source IP/IPv6 address (local peer).                         |

Policy order is important starting from v6.40. Now it works similarly to firewall filters where policies are executed from top to bottom (priority parameter is removed).

All packets are IPIP encapsulated in tunnel mode, and their new IP header's src-address and dst-address are set to sa-src-address and sa-dst-address values of this policy. If you do not use tunnel mode (id est you use transport mode), then only packets whose source and destination addresses are the same as sa-src-address and sa-dst-address can be processed by this policy. Transport mode can only work with packets that originate at and are destined for IPsec peers (hosts that established security associations). To encrypt traffic between networks (or a network and a host) you have to use tunnel mode.

## Statistics

This menu shows various IPsec statistics and errors.

**Read-only properties**

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

|                                           |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **in-errors** (_integer_)                 | All inbound errors that are not matched by other counters.                                                                                                    |
| **in-buffer-errors** (_integer_)          | No free buffer.                                                                                                                                               |
| **in-header-errors** (_integer_)          | Header error.                                                                                                                                                 |
| **in-no-states** (_integer_)              | No state is found i.e. either inbound SPI, address, or IPsec protocol at SA is wrong.                                                                         |
| **in-state-protocol-errors** (_integer_)  | Transformation protocol-specific error, for example, SA key is wrong or hardware accelerator is unable to handle the number of packets.                       |
| **in-state-mode-errors** (_integer_)      | Transformation mode-specific error.                                                                                                                           |
| **in-state-sequence-errors** (_integer_)  | A sequence number is out of a window.                                                                                                                         |
| **in-state-expired** (_integer_)          | The state is expired.                                                                                                                                         |
| **in-state-mismatches** (_integer_)       | The state has a mismatched option, for example, the UDP encapsulation type is mismatched.                                                                     |
| **in-state-invalid** (_integer_)          | The state is invalid.                                                                                                                                         |
| **in-template-mismatches** (_integer_)    | No matching template for states, e.g. inbound SAs are correct but the SP rule is wrong. A possible cause is a mismatched sa-source or sa-destination address. |
| **in-no-policies** (_integer_)            | No policy is found for states, e.g. inbound SAs are correct but no SP is found.                                                                               |
| **in-policy-blocked** (_integer_)         | Policy discards.                                                                                                                                              |
| **in-policy-errors** (_integer_)          | Policy errors.                                                                                                                                                |
| **out-errors** (_integer_)                | All outbound errors that are not matched by other counters.                                                                                                   |
| **out-bundle-errors** (_integer_)         | Bundle generation error.                                                                                                                                      |
| **out-bundle-check-errors** (_integer_)   | Bundle check error.                                                                                                                                           |
| **out-no-states** (_integer_)             | No state is found.                                                                                                                                            |
| **out-state-protocol-errors** (_integer_) | Transformation protocol specific error.                                                                                                                       |
| **out-state-mode-errors** (_integer_)     | Transformation mode-specific error.                                                                                                                           |
| **out-state-sequence-errors** (_integer_) | Sequence errors, for example, sequence number overflow.                                                                                                       |
| **out-state-expired** (_integer_)         | The state is expired.                                                                                                                                         |
| **out-policy-blocked** (_integer_)        | Policy discards.                                                                                                                                              |
| **out-policy-dead** (_integer_)           | The policy is dead.                                                                                                                                           |
| **out-policy-errors** (_integer_)         | Policy error.                                                                                                                                                 |

# Proposals

Proposal information that will be sent by IKE daemons to establish SAs for certain policies.

  
**Properties**

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

|                                         |
| --------------------------------------- | ------------------------------------------ |
| **auth-algorithms** (_md5               | null                                       | sha1                         | sha256      | sha512_; Default: **sha1**) | Allowed algorithms for authorization. SHA (Secure Hash Algorithm) is stronger but slower. MD5 uses a 128-bit key, sha1-160bit key. |
| **comment** (_string_; Default: )       |
|                                         |
| **disabled** (_yes                      | no_; Default: **no**)                      | Whether an item is disabled. |
| **enc-algorithms** (_null               | des                                        | 3des                         | aes-128-cbc | aes-128-cbc                 | aes-128gcm                                                                                                                         | aes-192-cbc | aes-192-ctr | aes-192-gcm | aes-256-cbc | aes-256-ctr | aes-256-gcm | blowfish | camellia-128                  | camellia-192                                              | camellia-256 | twofish_; Default: **aes-256-cbc,aes-192-cbc,aes-128-cbc**) | Allowed algorithms and key lengths to use for SAs. |
| **lifetime** (_time_; Default: **30m**) | How long to use SA before throwing it out. |
| **name** (_string_; Default: )          |
|                                         |
| **pfs-group** (_ec2n155                 | ec2n185                                    | ecp256                       | ecp384      | ecp521                      | modp768                                                                                                                            | modp1024    | modp1536    | modp2048    | modp3072    | modp4096    | modp6144    | modp8192 | none_; Default: **modp1024**) | The diffie-Helman group used for Perfect Forward Secrecy. |

  
**Read-only properties**

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

|                   |
| ----------------- | ---- |
| **default** (_yes | no_) | Whether this is a default system entry. |

# Groups

In this menu, it is possible to create additional policy groups used by policy templates.

  
**Properties**

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

|                                   |
| --------------------------------- |  |
| **name** (_string_; Default: )    |
|                                   |
| **comment** (_string_; Default: ) |
|                                   |

# Peers

Peer configuration settings are used to establish connections between IKE daemons. This connection then will be used to negotiate keys and algorithms for SAs. Exchange mode is the only unique identifier between the peers, meaning that there can be multiple peer configurations with the same remote-address as long as a different exchange-mode is used.

**Properties**

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

|                                                        |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_IP/IPv6 Prefix_; Default: **0.0.0.0/0**) | If the remote peer's address matches this prefix, then the peer configuration is used in authentication and establishment of **Phase 1**. If several peer's addresses match several configuration entries, the most specific one (i.e. the one with the largest netmask) will be used. |
| **comment** (_string_; Default: )                      | Short description of the peer.                                                                                                                                                                                                                                                         |
| **disabled** (_yes                                     | no_; Default: **no**)                                                                                                                                                                                                                                                                  | Whether peer is used to matching remote peer's prefix.                                                                                                                                                                                                                                                                                                                                |
| **exchange-mode** (_aggressive                         | base                                                                                                                                                                                                                                                                                   | main                                                                                                                                                                                                                                                                                                                                                                                  | ike2_; Default: **main**) | Different ISAKMP phase 1 exchange modes according to RFC 2408. the **main** mode relaxes rfc2409 section 5.4, to allow pre-shared-key authentication in the main mode. ike2 mode enables Ikev2 RFC 7296. Parameters that are ignored by IKEv2 proposal-check, compatibility-options, lifebytes, dpd-maximum-failures, nat-traversal. |
| **local-address** (_IP/IPv6 Address_; Default: )       | Routers local address on which Phase 1 should be bounded to.                                                                                                                                                                                                                           |
| **name** (_string_; Default: )                         |
|                                                        |
| **passive** (_yes                                      | no_; Default: **no**)                                                                                                                                                                                                                                                                  | When a passive mode is enabled will wait for a remote peer to initiate an IKE connection. The enabled passive mode also indicates that the peer is xauth responder, and disabled passive mode - xauth initiator. When a passive mode is a disabled peer will try to establish not only phase1 but also phase2 automatically, if policies are configured or created during the phase1. |
| **port** (_integer:0..65535_; Default: **500**)        | Communication port used (when a router is an initiator) to connect to remote peer in cases if remote peer uses the non-default port.                                                                                                                                                   |
| **profile** (_string_; Default: **default**)           | Name of the profile template that will be used during IKE negotiation.                                                                                                                                                                                                                 |
| **send-initial-contact** (_yes                         | no_; Default: **yes**)                                                                                                                                                                                                                                                                 | Specifies whether to send "initial contact" IKE packet or wait for remote side, this packet should trigger the removal of old peer SAs for current source address. Usually, in road warrior setups clients are initiators and this parameter should be set to no. Initial contact is not sent if modecfg or xauth is enabled for ikev1.                                               |

**Read-only properties**

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

|                     |
| ------------------- | ---- |
| **dynamic** (_yes   | no_) | Whether this is a dynamically added entry by a different service (e.g L2TP).                                |
| **responder** (_yes | no_) | Whether this peer will act as a responder only (listen to incoming requests) and not initiate a connection. |

# Identities

Identities are configuration parameters that are specific to the remote peer. The main purpose of identity is to handle authentication and verify the peer's integrity.

**Properties**

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

|                                     |
| ----------------------------------- | --- |
| **auth-method** (_digital-signature | eap | eap-radius | pre-shared-key | pre-shared-key-xauth | rsa-key | rsa-signature-hybrid_; Default: **pre-shared-key**) | Authentication method: |

-   digital-signature - authenticate using a pair of RSA certificates;
-   eap - IKEv2 EAP authentication for initiator (peer with a netmask of /32). Must be used together with eap-methods;
-   eap-radius - IKEv2 EAP RADIUS passthrough authentication for the responder (RFC 3579). A server certificate in this case is required. If a server certificate is not specified then only clients supporting EAP-only (RFC 5998) will be able to connect. Note that the EAP method should be compatible with EAP-only;
-   pre-shared-key - authenticate by a password (pre-shared secret) string shared between the peers (not recommended since an offline attack on the pre-shared key is possible);
-   rsa-key - authenticate using an RSA key imported in keys menu. Only supported in IKEv1;
-   pre-shared-key-xauth - authenticate by a password (pre-shared secret) string shared between the peers + XAuth username and password. Only supported in IKEv1;
-   rsa-signature-hybrid - responder certificate authentication with initiator XAuth. Only supported in IKEv1.

 |
| **certificate** (_string_; Default: ) | Name of a certificate listed in System/Certificates (signing packets; the certificate must have the private key). Applicable if digital signature authentication method (auth-method=digital-signature) or EAP (auth-method=eap) is used. |
| **comment** (_string_; Default: ) | Short description of the identity. |
| **disabled** (_yes | no_; Default: **no**) | Whether identity is used to match remote peers. |
| **eap-methods** (_eap-mschapv2 | eap-peap | eap-tls | eap-ttls_; Default: **eap-tls**) | All EAP methods requires whole certificate chain including intermediate and root CA certificates to be present in System/Certificates menu. Also, the username and password (if required by the authentication server) must be specified. Multiple EAP methods may be specified and will be used in a specified order. Currently supported EAP methods:

-   eap-mschapv2;
-   eap-peap - also known as PEAPv0/EAP-MSCHAPv2;
-   eap-tls - requires additional client certificate specified under certificate parameter;
-   eap-ttls.

 |
| **generate-policy** (_no | port-override | port-strict_; Default: **no**) | Allow this peer to establish SA for non-existing policies. Such policies are created dynamically for the lifetime of SA. Automatic policies allows, for example, to create IPsec secured L2TP tunnels, or any other setup where remote peer's IP address is not known at the configuration time.

-   no - do not generate policies;
-   port-override - generate policies and force policy to use **any** port (old behavior);
-   port-strict - use ports from peer's proposal, which should match peer's policy.

 |
| **key** (_string_; Default: ) | Name of the private key from keys menu. Applicable if RSA key authentication method (auth-method=rsa-key) is used. |
| **match-by** (_remote-id | certificate_; Default: **remote-id**) | Defines the logic used for peer's identity validation.

-   remote-id - will verify the peer's ID according to remote-id setting.
-   certificate will verify the peer's certificate with what is specified under remote-certificate setting.

 |
| **mode-config** (_none | \*request-only | string_; Default: **none**) | Name of the configuration parameters from mode-config menu. When parameter is set mode-config is enabled. |
| **my-id** (_auto | address | fqdn | user-fqdn | key-id_; Default: **auto**) | On initiator, this controls what ID\_i is sent to the responder. On responder, this controls what ID\_r is sent to the initiator. In IKEv2, responder also expects this ID in received ID\_r from initiator.

-   auto - tries to use correct ID automatically: IP for pre-shared key, SAN (DN if not present) for certificate based connections;
-   address - IP address is used as ID;
-   dn - the binary Distinguished Encoding Rules (DER) encoding of an ASN.1 X.500 Distinguished Name;
-   fqdn - fully qualified domain name;
-   key-id - use the specified key ID for the identity;
-   user fqdn - specifies a fully-qualified username string, for example, "user@domain.com".

 |
| **notrack-chain** (_string_; Default: ) | Adds IP/Firewall/Raw rules matching IPsec policy to a specified chain. Use together with generate-policy. |
| **password** (_string_; Default: ) | XAuth or EAP password. Applicable if pre-shared key with XAuth authentication method (auth-method=pre-shared-key-xauth) or EAP (auth-method=eap) is used. |
| **peer** (_string_; Default: ) | Name of the peer on which the identity applies. |
| **policy-template-group** (_none | string_; Default: **default**) | If generate-policy is enabled, traffic selectors are checked against templates from the same group. If none of the templates match, Phase 2 SA will not be established. |
| **remote-certificate** (_string_; Default: ) | Name of a certificate (listed in System/Certificates) for authenticating the remote side (validating packets; no private key required). If a remote-certificate is not specified then the received certificate from a remote peer is used and checked against CA in the certificate menu. Proper CA must be imported in a certificate store. If remote-certificate and match-by=certificate is specified, only the specific client certificate will be matched. Applicable if digital signature authentication method (auth-method=digital-signature) is used. |
| **remote-id** (_auto | fqdn | user-fqdn | key-id | ignore_; Default: **auto**) | This parameter controls what ID value to expect from the remote peer. Note that all types except for ignoring will verify remote peer's ID with a received certificate. In case when the peer sends the certificate name as its ID, it is checked against the certificate, else the ID is checked against Subject Alt. Name.

-   auto - accept all ID's;
-   address - IP address is used as ID;
-   dn - the binary Distinguished Encoding Rules (DER) encoding of an ASN.1 X.500 Distinguished Name;
-   fqdn - fully qualified domain name. Only supported in IKEv2;
-   user fqdn - a fully-qualified username string, for example, "user@domain.com". Only supported in IKEv2;
-   key-id - specific key ID for the identity. Only supported in IKEv2;
-   ignore - do not verify received ID with certificate (dangerous).

 |
| **remote-key** (_string_; Default: ) | Name of the public key from keys menu. Applicable if RSA key authentication method (auth-method=rsa-key) is used. |
| **secret** (_string_; Default: ) | Secret string. If it starts with '0x', it is parsed as a hexadecimal value. Applicable if pre-shared key authentication method (auth-method=pre-shared-key and auth-method=pre-shared-key-xauth) is used. |
| **username** (_string_; Default: ) | XAuth or EAP username. Applicable if pre-shared key with XAuth authentication method (auth-method=pre-shared-key-xauth) or EAP (auth-method=eap) is used. |

  
**Read only properties**

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

|                   |
| ----------------- | ---- |
| **dynamic** (_yes | no_) | Whether this is a dynamically added entry by a different service (e.g L2TP). |

## Profiles

Profiles define a set of parameters that will be used for IKE negotiation during Phase 1. These parameters may be common with other peer configurations.

**Properties**

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

|                                                              |
| ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **dh-group** (_modp768                                       | modp1024                                                                                                                                                                | ec2n155                                                                                                                                                                                                                                                                                                                                                                                                                           | ec2n185                     | modp1536                                                                                                       | modp2048     | modp3072     | modp4096     | modp6144                    | modp8192                                                     | ecp256 | ecp384 | ecp521_; Default: **modp1024,modp2048**) | Diffie-Hellman group (cipher strength) |
| **dpd-interval** (_time                                      | disable-dpd_; Default: **2m**)                                                                                                                                          | Dead peer detection interval. If set to disable-dpd, dead peer detection will not be used.                                                                                                                                                                                                                                                                                                                                        |
| **dpd-maximum-failures** (_integer: 1..100_; Default: **5**) | Maximum count of failures until peer is considered to be dead. Applicable if DPD is enabled.                                                                            |
| **enc-algorithm** (_3des                                     | aes-128                                                                                                                                                                 | aes-192                                                                                                                                                                                                                                                                                                                                                                                                                           | aes-256                     | blowfish                                                                                                       | camellia-128 | camellia-192 | camellia-256 | des_; Default: **aes-128**) | List of encryption algorithms that will be used by the peer. |
| **hash-algorithm** (_md5                                     | sha1                                                                                                                                                                    | sha256                                                                                                                                                                                                                                                                                                                                                                                                                            | sha512_; Default: **sha1**) | Hashing algorithm. SHA (Secure Hash Algorithm) is stronger, but slower. MD5 uses 128-bit key, sha1-160bit key. |
| **lifebytes** (_Integer: 0..4294967295_; Default: **0**)     | Phase 1 lifebytes is used only as administrative value which is added to proposal. Used in cases if remote peer requires specific lifebytes value to establish phase 1. |
| **lifetime** (_time_; Default: **1d**)                       | Phase 1 lifetime: specifies how long the SA will be valid.                                                                                                              |
| **name** (_string_; Default: )                               |
|                                                              |
| **nat-traversal** (_yes                                      | no_; Default: **yes**)                                                                                                                                                  | Use Linux NAT-T mechanism to solve IPsec incompatibility with NAT routers between IPsec peers. This can only be used with ESP protocol (AH is not supported by design, as it signs the complete packet, including the IP header, which is changed by NAT, rendering AH signature invalid). The method encapsulates IPsec ESP traffic into UDP streams in order to overcome some minor issues that made ESP incompatible with NAT. |
| **proposal-check** (_claim                                   | exact                                                                                                                                                                   | obey                                                                                                                                                                                                                                                                                                                                                                                                                              | strict_; Default: **obey**) | Phase 2 lifetime check logic:                                                                                  |

-   claim - take shortest of proposed and configured lifetimes and notify initiator about it
-   exact - require lifetimes to be the same
-   obey - accept whatever is sent by an initiator
-   strict - if the proposed lifetime is longer than the default then reject the proposal otherwise accept a proposed lifetime

 |

# Active Peers

This menu provides various statistics about remote peers that currently have established phase 1 connection.

  
**Read only properties**

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

|                                         |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **dynamic-address** (_ip/ipv6 address_) | Dynamically assigned an IP address by mode config                                                                                 |
| **last-seen** (_time_)                  | Duration since the last message received by this peer.                                                                            |
| **local-address** (_ip/ipv6 address_)   | Local address on the router used by this peer.                                                                                    |
| **natt-peer** (_yes                     | no_)                                                                                                                              | Whether NAT-T is used for this peer.                  |
| **ph2-total** (_integer_)               | The total amount of active IPsec security associations.                                                                           |
| **remote-address** (_ip/ipv6 address_)  | The remote peer's ip/ipv6 address.                                                                                                |
| **responder** (_yes                     | no_)                                                                                                                              | Whether the connection is initiated by a remote peer. |
| **rx-bytes** (_integer_)                | The total amount of bytes received from this peer.                                                                                |
| **rx-packets** (_integer_)              | The total amount of packets received from this peer.                                                                              |
| **side** (_initiator                    | responder_)                                                                                                                       | Shows which side initiated the Phase1 negotiation.    |
| **state** (_string_)                    | State of phase 1 negotiation with the peer. For example, when phase1 and phase 2 are negotiated it will show state "established". |
| **tx-bytes** (_integer_)                | The total amount of bytes transmitted to this peer.                                                                               |
| **tx-packets** (_integer_)              | The total amount of packets transmitted to this peer.                                                                             |
| **uptime** (_time_)                     | How long peers are in an established state.                                                                                       |

  
**Commands**

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

|                         |
| ----------------------- | -------------------------------------- |
| **kill-connections** () | Manually disconnects all remote peers. |

# Mode configs

ISAKMP and IKEv2 configuration attributes are configured in this menu.

  
**Properties**

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
| ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_none                                         | string_; Default: )                                                                                                                                                     | Single IP address for the initiator instead of specifying a whole address pool.                                                                                         |
| **address-pool** (_none                                    | string_; Default: )                                                                                                                                                     | Name of the address pool from which the responder will try to assign address if mode-config is enabled.                                                                 |
| **address-prefix-length** (_integer \[1..32\]_; Default: ) | Prefix length (netmask) of the assigned address from the pool.                                                                                                          |
| **comment** (_string_; Default: )                          |
|                                                            |
| **name** (_string_; Default: )                             |
|                                                            |
| **responder** (_yes                                        | no_; Default: **no**)                                                                                                                                                   | Specifies whether the configuration will work as an initiator (client) or responder (server). The initiator will request for mode-config parameters from the responder. |
| **split-include** (_list of IP prefix_; Default: )         | List of subnets in CIDR format, which to tunnel. Subnets will be sent to the peer using the CISCO UNITY extension, a remote peer will create specific dynamic policies. |
| **src-address-list** (_address list_; Default: )           | Specifying an address list will generate dynamic source NAT rules. This parameter is only available with responder=no. A roadWarrior client with NAT                    |
| **static-dns** (_list of IP_; Default: )                   | Manually specified DNS server's IP address to be sent to the client.                                                                                                    |
| **system-dns** (_yes                                       | no_; Default: )                                                                                                                                                         | When this option is enabled DNS addresses will be taken from `/ip dns`.                                                                                                 |

  
**Read-only properties**

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

|                   |
| ----------------- | ---- |
| **default** (_yes | no_) | Whether this is a default system entry. |

Not all IKE implementations support multiple split networks provided by the split-include option.

If RouterOS client is initiator, it will always send CISCO UNITY extension, and RouterOS supports only split-include from this extension.

It is not possible to use system-dns and static-dns at the same time.

# Installed SAs

This menu provides information about installed security associations including the keys.

  
**Read-only properties**

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

|                                |
| ------------------------------ | ---------------------------------------------- |
| **AH** (_yes                   | no_)                                           | Whether AH protocol is used by this SA.  |
| **ESP** (_yes                  | no_)                                           | Whether ESP protocol is used by this SA. |
| **add-lifetime** (_time/time_) | Added lifetime for the SA in format soft/hard: |

-   soft - time period after which IKE will try to establish new SA;
-   hard - time period after which SA is deleted.

 |
| **addtime** (_time_) | Date and time when this SA was added. |
| **auth-algorithm** (_md5 | null | sha1 | ..._) | Currently used authentication algorithm. |
| **auth-key** (_string_) | Used authentication key. |
| **current-bytes** (_64-bit integer_) | A number of bytes seen by this SA. |
| **dst-address** (_IP_) | The destination address of this SA. |
| **enc-algorithm** (_des | 3des | aes-cbc | ..._) | Currently used encryption algorithm. |
| **enc-key** (_string_) | Used encryption key. |
| **enc-key-size** (_number_) | Used encryption key length. |
| **expires-in** (_yes | no_) | Time left until rekeying. |
| **hw-aead** (_yes | no_) | Whether this SA is hardware accelerated. |
| **replay** (_integer_) | Size of replay window in bytes. |
| **spi** (_string_) | Security Parameter Index identification tag |
| **src-address** (_IP_) | The source address of this SA. |
| **state** (_string_) | Shows the current state of the SA ("mature", "dying" etc) |

  
**Commands**

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

|              |
| ------------ | ----------------------------------------------------- |
| **flush** () | Manually removes all installed security associations. |

# Keys

This menu lists all imported public and private keys, that can be used for peer authentication. Menu has several commands to work with keys.

  
**Properties**

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

|                                |
| ------------------------------ |  |
| **name** (_string_; Default: ) |
|                                |

  
**Read-only properties**

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

|                       |
| --------------------- | ---- |
| **key-size** (_1024   | 2048 | 4096_)                         | Size of this key. |
| **private-key** (_yes | no_) | Whether this is a private key. |
| **rsa** (_yes         | no_) | Whether this is an RSA key.    |

  
**Commands**

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

|                                       |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **export-pub-key** (_file-name; key_) | Export public key to file from one of existing private keys.                                                   |
| **generate-key** (_key-size; name_)   | Generate a private key. Takes two parameters, name of the newly generated key and key size 1024,2048 and 4096. |
| **import** (_file-name; name_)        | Import key from file.                                                                                          |

# Settings

  

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

|                                        |
| -------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **accounting** (_yes                   | no_; Default: )                                                                                     | Whether to send RADIUS accounting requests to a RADIUS server. Applicable if EAP Radius (auth-method=eap-radius) or pre-shared key with XAuth authentication method (auth-method=pre-shared-key-xauth) is used. |
| **interim-update** (_time_; Default: ) | The interval between each consecutive RADIUS accounting Interim update. Accounting must be enabled. |
| **xauth-use-radius** (_yes             | no_; Default: )                                                                                     | Whether to use Radius client for XAuth users or not.                                                                                                                                                            |

# Application Guides

## RoadWarrior client with NAT

Consider setup as illustrated below. RouterOS acts as a RoadWarrior client connected to Office allowing access to its internal resources.

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ipsec-road-warrior.jpg?version=1&modificationDate=1612795265983&api=v2)

A tunnel is established, a local mode-config IP address is received and a set of dynamic policies are generated.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@mikrotik] &gt; ip ipsec policy </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: T - template, X - disabled, D - dynamic, I - invalid, A - active, * - default</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">0 T * </code><code class="ros value">group</code><code class="ros plain">=default</code> <code class="ros value">src-address</code><code class="ros plain">=::/0</code> <code class="ros value">dst-address</code><code class="ros plain">=::/0</code> <code class="ros value">protocol</code><code class="ros plain">=all</code> <code class="ros value">proposal</code><code class="ros plain">=default</code> <code class="ros value">template</code><code class="ros plain">=yes</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">1 DA </code><code class="ros value">src-address</code><code class="ros plain">=192.168.77.254/32</code> <code class="ros value">src-port</code><code class="ros plain">=any</code> <code class="ros value">dst-address</code><code class="ros plain">=10.5.8.0/24</code> <code class="ros value">dst-port</code><code class="ros plain">=any</code> <code class="ros value">protocol</code><code class="ros plain">=all</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros value">action</code><code class="ros plain">=encrypt</code> <code class="ros value">level</code><code class="ros plain">=unique</code> <code class="ros value">ipsec-protocols</code><code class="ros plain">=esp</code> <code class="ros value">tunnel</code><code class="ros plain">=yes</code> <code class="ros value">sa-src-address</code><code class="ros plain">=10.155.107.8</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros value">sa-dst-address</code><code class="ros plain">=10.155.107.9</code> <code class="ros value">proposal</code><code class="ros plain">=default</code> <code class="ros value">ph2-count</code><code class="ros plain">=1</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">2 DA </code><code class="ros value">src-address</code><code class="ros plain">=192.168.77.254/32</code> <code class="ros value">src-port</code><code class="ros plain">=any</code> <code class="ros value">dst-address</code><code class="ros plain">=192.168.55.0/24</code> <code class="ros value">dst-port</code><code class="ros plain">=any</code> <code class="ros value">protocol</code><code class="ros plain">=all</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros value">action</code><code class="ros plain">=encrypt</code> <code class="ros value">level</code><code class="ros plain">=unique</code> <code class="ros value">ipsec-protocols</code><code class="ros plain">=esp</code> <code class="ros value">tunnel</code><code class="ros plain">=yes</code> <code class="ros value">sa-src-address</code><code class="ros plain">=10.155.107.8</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros value">sa-dst-address</code><code class="ros plain">=10.155.107.9</code> <code class="ros value">proposal</code><code class="ros plain">=default</code> <code class="ros value">ph2-count</code><code class="ros plain">=1</code></div></div></td></tr></tbody></table>

Currently, only packets with a source address of 192.168.77.254/32 will match the IPsec policies. For a local network to be able to reach remote subnets, it is necessary to change the source address of local hosts to the dynamically assigned mode config IP address. It is possible to generate source NAT rules dynamically. This can be done by creating a new address list that contains all local networks that the NAT rule should be applied. In our case, it is 192.168.88.0/24.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall address-list </code><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.88.0/24</code> <code class="ros value">list</code><code class="ros plain">=local-RW</code></div></div></td></tr></tbody></table>

By specifying the address list under the mode-config initiator configuration, a set of source NAT rules will be dynamically generated.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec mode-config </code><code class="ros functions">set </code><code class="ros plain">[ </code><code class="ros functions">find </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"request-only"</code> <code class="ros plain">] </code><code class="ros value">src-address-list</code><code class="ros plain">=local-RW</code></div></div></td></tr></tbody></table>

When the IPsec tunnel is established, we can see the dynamically created source NAT rules for each network. Now every host in 192.168.88.0/24 is able to access Office's internal resources.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@mikrotik] &gt; ip firewall nat </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - invalid, D - dynamic</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">0 D ;;; ipsec mode-config</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">to-addresses</code><code class="ros plain">=192.168.77.254</code> <code class="ros value">dst-address</code><code class="ros plain">=192.168.55.0/24</code> <code class="ros value">src-address-list</code><code class="ros plain">=local-RW</code></div><div class="line number5 index4 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">1 D ;;; ipsec mode-config</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">to-addresses</code><code class="ros plain">=192.168.77.254</code> <code class="ros value">dst-address</code><code class="ros plain">=10.5.8.0/24</code> <code class="ros value">src-address-list</code><code class="ros plain">=local-RW</code></div></div></td></tr></tbody></table>

## Allow only IPsec encapsulated traffic

There are some scenarios where for security reasons you would like to drop access from/to specific networks if incoming/outgoing packets are not encrypted. For example, if we have L2TP/IPsec setup we would want to drop nonencrypted L2TP connection attempts.

There are several ways how to achieve this:

-   Using IPsec policy matcher in firewall;
-   Using generic IPsec policy with action set to **drop** and lower priority (can be used in Road Warrior setups where dynamic policies are generated);
-   By setting DSCP or priority in mangle and matching the same values in firewall after decapsulation.

### IPsec policy matcher

Let's set up an IPsec policy matcher to accept all packets that matched any of the IPsec policies and drop the rest:

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">comment</code><code class="ros plain">=</code><code class="ros string">"ipsec policy matcher"</code> <code class="ros value">in-interface</code><code class="ros plain">=WAN</code> <code class="ros value">ipsec-policy</code><code class="ros plain">=in,ipsec</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=drop</code> <code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">comment</code><code class="ros plain">=</code><code class="ros string">"drop all"</code> <code class="ros value">in-interface</code><code class="ros plain">=WAN</code> <code class="ros value">log</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

IPsec policy matcher takes two parameters **direction, policy**. We used incoming direction and IPsec policy. IPsec policy option allows us to inspect packets after decapsulation, so for example, if we want to allow only GRE encapsulated packet from a specific source address and drop the rest we could set up the following rules:

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">comment</code><code class="ros plain">=</code><code class="ros string">"ipsec policy matcher"</code> <code class="ros value">in-interface</code><code class="ros plain">=WAN</code> <code class="ros value">ipsec-policy</code><code class="ros plain">=in,ipsec</code> <code class="ros value">protocol</code><code class="ros plain">=gre</code> <code class="ros value">src</code><code class="ros plain">=address=192.168.33.1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=drop</code> <code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">comment</code><code class="ros plain">=</code><code class="ros string">"drop all"</code> <code class="ros value">in-interface</code><code class="ros plain">=WAN</code> <code class="ros value">log</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

For L2TP rule set would be:

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">comment</code><code class="ros plain">=</code><code class="ros string">"ipsec policy matcher"</code> <code class="ros value">in-interface</code><code class="ros plain">=WAN</code> <code class="ros value">ipsec-policy</code><code class="ros plain">=in,ipsec</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">dst-port</code><code class="ros plain">=1701</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=drop</code> <code class="ros value">chain</code><code class="ros plain">=input</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">dst-port</code><code class="ros plain">=1701</code> <code class="ros value">comment</code><code class="ros plain">=</code><code class="ros string">"drop l2tp"</code> <code class="ros value">in-interface</code><code class="ros plain">=WAN</code> <code class="ros value">log</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

### Using generic IPsec policy

The trick of this method is to add a default policy with an action drop. Let's assume we are running an L2TP/IPsec server on a public 1.1.1.1 address and we want to drop all nonencrypted L2TP:

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec policy</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">src-address</code><code class="ros plain">=1.1.1.1</code> <code class="ros value">dst-address</code><code class="ros plain">=0.0.0.0/0</code> <code class="ros value">sa-src-address</code><code class="ros plain">=1.1.1.1</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">src-port</code><code class="ros plain">=1701</code> <code class="ros value">tunnel</code><code class="ros plain">=yes</code> <code class="ros value">action</code><code class="ros plain">=discard</code></div></div></td></tr></tbody></table>

Now router will drop any L2TP unencrypted incoming traffic, but after a successful L2TP/IPsec connection dynamic policy is created with higher priority than it is on default static rule, and packets matching that dynamic rule can be forwarded.

Policy order is important! For this to work, make sure the static drop policy is below the dynamic policies. Move it below the policy template if necessary.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@rack2_10g1] </code><code class="ros constants">/ip ipsec policy&gt; </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: T - template, X - disabled, D - dynamic, I - inactive, * - default</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">0 T * </code><code class="ros value">group</code><code class="ros plain">=default</code> <code class="ros value">src-address</code><code class="ros plain">=::/0</code> <code class="ros value">dst-address</code><code class="ros plain">=::/0</code> <code class="ros value">protocol</code><code class="ros plain">=all</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros value">proposal</code><code class="ros plain">=default</code> <code class="ros value">template</code><code class="ros plain">=yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">1 D </code><code class="ros value">src-address</code><code class="ros plain">=1.1.1.1/32</code> <code class="ros value">src-port</code><code class="ros plain">=1701</code> <code class="ros value">dst-address</code><code class="ros plain">=10.5.130.71/32</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros value">dst-port</code><code class="ros plain">=any</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">action</code><code class="ros plain">=encrypt</code> <code class="ros value">level</code><code class="ros plain">=require</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros value">ipsec-protocols</code><code class="ros plain">=esp</code> <code class="ros value">tunnel</code><code class="ros plain">=no</code> <code class="ros value">sa-src-address</code><code class="ros plain">=1.1.1.1</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros value">sa-dst-address</code><code class="ros plain">=10.5.130.71</code></div><div class="line number10 index9 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">2 </code><code class="ros value">src-address</code><code class="ros plain">=1.1.1.1/32</code> <code class="ros value">src-port</code><code class="ros plain">=1701</code> <code class="ros value">dst-address</code><code class="ros plain">=0.0.0.0/0</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros value">dst-port</code><code class="ros plain">=any</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">action</code><code class="ros plain">=discard</code> <code class="ros value">level</code><code class="ros plain">=unique</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros value">ipsec-protocols</code><code class="ros plain">=esp</code> <code class="ros value">tunnel</code><code class="ros plain">=yes</code> <code class="ros value">sa-src-address</code><code class="ros plain">=1.1.1.1</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros value">sa-dst-address</code><code class="ros plain">=0.0.0.0</code> <code class="ros value">proposal</code><code class="ros plain">=default</code> <code class="ros value">manual-sa</code><code class="ros plain">=none</code></div></div></td></tr></tbody></table>

## Manually specifying local-address parameter under Peer configuration

### Using different routing table

IPsec, as any other service in RouterOS, uses the main routing table regardless of what local-address parameter is used for Peer configuration. It is necessary to apply routing marks to both IKE and IPSec traffic.

Consider the following example. There are two default routes - one in the main routing table and another in the routing table "backup". It is necessary to use the backup link for the IPsec site to site tunnel.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@pair_r1] &gt; </code><code class="ros constants">/ip route </code><code class="ros functions">print </code><code class="ros functions">detail</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, A - active, D - dynamic, C - connect, S - static, r - rip, b - bgp, o - ospf, m - mme, B - blackhole, U - unreachable, P - prohibit</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">0 A S </code><code class="ros value">dst-address</code><code class="ros plain">=0.0.0.0/0</code> <code class="ros value">gateway</code><code class="ros plain">=10.155.107.1</code> <code class="ros value">gateway-status</code><code class="ros plain">=10.155.107.1</code> <code class="ros plain">reachable via ether1 </code><code class="ros value">distance</code><code class="ros plain">=1</code> <code class="ros value">scope</code><code class="ros plain">=30</code> <code class="ros value">target-scope</code><code class="ros plain">=10</code> <code class="ros value">routing-mark</code><code class="ros plain">=backup</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">1 A S </code><code class="ros value">dst-address</code><code class="ros plain">=0.0.0.0/0</code> <code class="ros value">gateway</code><code class="ros plain">=172.22.2.115</code> <code class="ros value">gateway-status</code><code class="ros plain">=172.22.2.115</code> <code class="ros plain">reachable via ether2 </code><code class="ros value">distance</code><code class="ros plain">=1</code> <code class="ros value">scope</code><code class="ros plain">=30</code> <code class="ros value">target-scope</code><code class="ros plain">=10</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">2 ADC </code><code class="ros value">dst-address</code><code class="ros plain">=10.155.107.0/25</code> <code class="ros value">pref-src</code><code class="ros plain">=10.155.107.8</code> <code class="ros value">gateway</code><code class="ros plain">=ether1</code> <code class="ros value">gateway-status</code><code class="ros plain">=ether1</code> <code class="ros plain">reachable </code><code class="ros value">distance</code><code class="ros plain">=0</code> <code class="ros value">scope</code><code class="ros plain">=10</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">3 ADC </code><code class="ros value">dst-address</code><code class="ros plain">=172.22.2.0/24</code> <code class="ros value">pref-src</code><code class="ros plain">=172.22.2.114</code> <code class="ros value">gateway</code><code class="ros plain">=ether2</code> <code class="ros value">gateway-status</code><code class="ros plain">=ether2</code> <code class="ros plain">reachable </code><code class="ros value">distance</code><code class="ros plain">=0</code> <code class="ros value">scope</code><code class="ros plain">=10</code></div><div class="line number10 index9 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">4 ADC </code><code class="ros value">dst-address</code><code class="ros plain">=192.168.1.0/24</code> <code class="ros value">pref-src</code><code class="ros plain">=192.168.1.1</code> <code class="ros value">gateway</code><code class="ros plain">=bridge-local</code> <code class="ros value">gateway-status</code><code class="ros plain">=ether2</code> <code class="ros plain">reachable </code><code class="ros value">distance</code><code class="ros plain">=0</code> <code class="ros value">scope</code><code class="ros plain">=10</code></div><div class="line number12 index11 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros plain">[admin@pair_r1] &gt; </code><code class="ros constants">/ip firewall nat </code><code class="ros functions">print</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - invalid, D - dynamic</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros plain">0 </code><code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">action</code><code class="ros plain">=masquerade</code> <code class="ros value">out-interface</code><code class="ros plain">=ether1</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div><div class="line number16 index15 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros plain">1 </code><code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">action</code><code class="ros plain">=masquerade</code> <code class="ros value">out-interface</code><code class="ros plain">=ether2</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div></div></td></tr></tbody></table>

IPsec peer and policy configurations are created using the backup link's source address, as well as the NAT bypass rule for IPsec tunnel traffic.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec peer</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.155.130.136/32</code> <code class="ros value">local-address</code><code class="ros plain">=10.155.107.8</code> <code class="ros value">secret</code><code class="ros plain">=test</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec policy</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">sa-src-address</code><code class="ros plain">=10.155.107.8</code> <code class="ros value">src-address</code><code class="ros plain">=192.168.1.0/24</code> <code class="ros value">dst-address</code><code class="ros plain">=172.16.0.0/24</code> <code class="ros value">sa-dst-address</code><code class="ros plain">=10.155.130.136</code> <code class="ros value">tunnel</code><code class="ros plain">=yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall nat</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">src-address</code><code class="ros plain">=192.168.1.0/24</code> <code class="ros value">dst-address</code><code class="ros plain">=172.16.0.0/24</code> <code class="ros value">place-before</code><code class="ros plain">=0</code></div></div></td></tr></tbody></table>

Currently, we see "phase1 negotiation failed due to time up" errors in the log. It is because IPsec tries to reach the remote peer using the main routing table with an incorrect source address. It is necessary to mark UDP/500, UDP/4500, and ipsec-esp packets using Mangle:

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall mangle</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=mark-connection</code> <code class="ros value">chain</code><code class="ros plain">=output</code> <code class="ros value">connection-mark</code><code class="ros plain">=no-mark</code> <code class="ros value">dst-address</code><code class="ros plain">=10.155.130.136</code> <code class="ros value">dst-port</code><code class="ros plain">=500,4500</code> <code class="ros value">new-connection-mark</code><code class="ros plain">=ipsec</code> <code class="ros value">passthrough</code><code class="ros plain">=yes</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=mark-connection</code> <code class="ros value">chain</code><code class="ros plain">=output</code> <code class="ros value">connection-mark</code><code class="ros plain">=no-mark</code> <code class="ros value">dst-address</code><code class="ros plain">=10.155.130.136</code> <code class="ros value">new-connection-mark</code><code class="ros plain">=ipsec</code> <code class="ros value">passthrough</code><code class="ros plain">=yes</code> <code class="ros value">protocol</code><code class="ros plain">=ipsec-esp</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=mark-routing</code> <code class="ros value">chain</code><code class="ros plain">=output</code> <code class="ros value">connection-mark</code><code class="ros plain">=ipsec</code> <code class="ros value">new-routing-mark</code><code class="ros plain">=backup</code> <code class="ros value">passthrough</code><code class="ros plain">=no</code></div></div></td></tr></tbody></table>

### Using the same routing table with multiple IP addresses

Consider the following example. There are multiple IP addresses from the same subnet on the public interface. Masquerade rule is configured on out-interface. It is necessary to use one of the IP addresses explicitly.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@pair_r1] &gt; </code><code class="ros constants">/ip address </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - invalid, D - dynamic</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros comments"># ADDRESS NETWORK INTERFACE</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">0 </code><code class="ros color1">192.168.1.1/24</code> <code class="ros plain">192.168.1.0 bridge-local</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">1 </code><code class="ros color1">172.22.2.1/24</code> <code class="ros plain">172.22.2.0 ether1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">2 </code><code class="ros color1">172.22.2.2/24</code> <code class="ros plain">172.22.2.0 ether1</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">3 </code><code class="ros color1">172.22.2.3/24</code> <code class="ros plain">172.22.2.0 ether1</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">[admin@pair_r1] &gt; </code><code class="ros constants">/ip route </code><code class="ros functions">print</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, A - active, D - dynamic, C - connect, S - static, r - rip, b - bgp, o - ospf, m - mme, B - blackhole, U - unreachable, P - prohibit</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros comments"># DST-ADDRESS PREF-SRC GATEWAY DISTANCE</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">1 A S </code><code class="ros color1">0.0.0.0/0</code> <code class="ros plain">172.22.2.115 1</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros plain">3 ADC </code><code class="ros color1">172.22.2.0/24</code> <code class="ros plain">172.22.2.1 ether1 0</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros plain">4 ADC </code><code class="ros color1">192.168.1.0/24</code> <code class="ros plain">192.168.1.1 bridge-</code><code class="ros functions">local </code><code class="ros plain">0</code></div><div class="line number15 index14 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros plain">[admin@pair_r1] </code><code class="ros constants">/ip firewall nat&gt; </code><code class="ros functions">print</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - invalid, D - dynamic</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros plain">0 </code><code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">action</code><code class="ros plain">=masquerade</code> <code class="ros value">out-interface</code><code class="ros plain">=ether1</code> <code class="ros value">log</code><code class="ros plain">=no</code> <code class="ros value">log-prefix</code><code class="ros plain">=</code><code class="ros string">""</code></div></div></td></tr></tbody></table>

IPsec peer and policy configuration is created using one of the public IP addresses.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec peer</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.155.130.136/32</code> <code class="ros value">local-address</code><code class="ros plain">=172.22.2.3</code> <code class="ros value">secret</code><code class="ros plain">=test</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec policy</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">sa-src-address</code><code class="ros plain">=172.22.2.3</code> <code class="ros value">src-address</code><code class="ros plain">=192.168.1.0/24</code> <code class="ros value">dst-address</code><code class="ros plain">=172.16.0.0/24</code> <code class="ros value">sa-dst-address</code><code class="ros plain">=10.155.130.136</code> <code class="ros value">tunnel</code><code class="ros plain">=yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall nat</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">src-address</code><code class="ros plain">=192.168.1.0/24</code> <code class="ros value">dst-address</code><code class="ros plain">=172.16.0.0/24</code> <code class="ros value">place-before</code><code class="ros plain">=0</code></div></div></td></tr></tbody></table>

Currently, the phase 1 connection uses a different source address than we specified, and "phase1 negotiation failed due to time up" errors are shown in the logs. This is because masquerade is changing the source address of the connection to match the pref-src address of the connected route. The solution is to exclude connections from the public IP address from being masqueraded.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall nat</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">protocol</code><code class="ros plain">=udp</code> <code class="ros value">src-port</code><code class="ros plain">=500,4500</code> <code class="ros value">place-before</code><code class="ros plain">=0</code></div></div></td></tr></tbody></table>

# Application examples

## Site to Site IPsec (IKEv1) tunnel

Consider setup as illustrated below. Two remote office routers are connected to the internet and office workstations are behind NAT. Each office has its own local subnet, 10.1.202.0/24 for Office1 and 10.1.101.0/24 for Office2. Both remote offices need secure tunnels to local networks behind routers.

  

![](https://help.mikrotik.com/docs/download/attachments/11993097/Site-to-site-ipsec-example.png?version=1&modificationDate=1615380469161&api=v2)

### **Site 1 configuration**

Start off by creating a new Phase 1profileand Phase 2proposalentries using stronger or weaker encryption parameters that suit your needs. It is advised to create separate entries for each menu so that they are unique for each peer in case it is necessary to adjust any of the settings in the future. These parameters must match between the sites or else the connection will not establish.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec pro</code><code class="ros plain">file</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dh-group</code><code class="ros plain">=modp2048</code> <code class="ros value">enc-algorithm</code><code class="ros plain">=aes-128</code> <code class="ros value">name</code><code class="ros plain">=ike1-site2</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec proposal</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">enc-algorithms</code><code class="ros plain">=aes-128-cbc</code> <code class="ros value">name</code><code class="ros plain">=ike1-site2</code> <code class="ros value">pfs-group</code><code class="ros plain">=modp2048</code></div></div></td></tr></tbody></table>

Continue by configuring a peer. Specify the address of the remote router. This address should be reachable through UDP/500 and UDP/4500 ports, so make sure appropriate actions are taken regarding the router's firewall. Specify the name for this peer as well as the newly created profile.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec peer</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.80.1/32</code> <code class="ros value">name</code><code class="ros plain">=ike1-site2</code> <code class="ros value">profile</code><code class="ros plain">=ike1-site2</code></div></div></td></tr></tbody></table>

The next step is to create an identity. For a basic pre-shared key secured tunnel, there is nothing much to set except for a **strong** secret and the peer to which this identity applies.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec identity</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">peer</code><code class="ros plain">=ike1-site2</code> <code class="ros value">secret</code><code class="ros plain">=thisisnotasecurepsk</code></div></div></td></tr></tbody></table>

If security matters, consider using IKEv2 and a different auth-method.

Lastly, create a policy that controls the networks/hosts between whom traffic should be encrypted.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec policy</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">src-address</code><code class="ros plain">=10.1.202.0/24</code> <code class="ros value">src-port</code><code class="ros plain">=any</code> <code class="ros value">dst-address</code><code class="ros plain">=10.1.101.0/24</code> <code class="ros value">dst-port</code><code class="ros plain">=any</code> <code class="ros value">tunnel</code><code class="ros plain">=yes</code> <code class="ros value">action</code><code class="ros plain">=encrypt</code> <code class="ros value">proposal</code><code class="ros plain">=ike1-site2</code> <code class="ros value">peer</code><code class="ros plain">=ike1-site2</code></div></div></td></tr></tbody></table>

  

### **Site 2 configuration**

Office 2 configuration is almost identical to Office 1 with proper IP address configuration. Start off by creating a new Phase 1 profile and Phase 2 proposal entries:

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec pro</code><code class="ros plain">file</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dh-group</code><code class="ros plain">=modp2048</code> <code class="ros value">enc-algorithm</code><code class="ros plain">=aes-128</code> <code class="ros value">name</code><code class="ros plain">=ike1-site1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec proposal</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">enc-algorithms</code><code class="ros plain">=aes-128-cbc</code> <code class="ros value">name</code><code class="ros plain">=ike1-site1</code> <code class="ros value">pfs-group</code><code class="ros plain">=modp2048</code></div></div></td></tr></tbody></table>

Next is the peer and identity:

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec peer</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.90.1/32</code> <code class="ros value">name</code><code class="ros plain">=ike1-site1</code> <code class="ros value">profile</code><code class="ros plain">=ike1-site1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec identity</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">peer</code><code class="ros plain">=ike1-site1</code> <code class="ros value">secret</code><code class="ros plain">=thisisnotasecurepsk</code></div></div></td></tr></tbody></table>

When it is done, create a policy:

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec policy</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">src-address</code><code class="ros plain">=10.1.101.0/24</code> <code class="ros value">src-port</code><code class="ros plain">=any</code> <code class="ros value">dst-address</code><code class="ros plain">=10.1.202.0/24</code> <code class="ros value">dst-port</code><code class="ros plain">=any</code> <code class="ros value">tunnel</code><code class="ros plain">=yes</code> <code class="ros value">action</code><code class="ros plain">=encrypt</code> <code class="ros value">proposal</code><code class="ros plain">=ike1-site1</code> <code class="ros value">peer</code><code class="ros plain">=ike1-site1</code></div></div></td></tr></tbody></table>

At this point, the tunnel should be established and two IPsec Security Associations should be created on both routers:

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">active-peers print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">installed-sa </code><code class="ros functions">print</code></div></div></td></tr></tbody></table>

### **NAT and Fasttrack Bypass**

At this point if you try to send traffic over the IPsec tunnel, it will not work, packets will be lost. This is because both routers have NAT rules (masquerade) that are changing source addresses before a packet is encrypted. A router is unable to encrypt the packet because the source address does not match the address specified in the policy configuration. For more information see the IPsec packet flow example.

To fix this we need to set up IP/Firewall/NAT bypass rule.

Office 1 router:

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall nat</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">place-before</code><code class="ros plain">=0</code> <code class="ros value">src-address</code><code class="ros plain">=10.1.202.0/24</code> <code class="ros value">dst-address</code><code class="ros plain">=10.1.101.0/24</code></div></div></td></tr></tbody></table>

Office 2 router:

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall nat</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">place-before</code><code class="ros plain">=0</code> <code class="ros value">src-address</code><code class="ros plain">=10.1.101.0/24</code> <code class="ros value">dst-address</code><code class="ros plain">=10.1.202.0/24</code></div></div></td></tr></tbody></table>

If you previously tried to establish an IP connection before the NAT bypass rule was added, you have to clear the connection table from the existing connection or restart both routers.

It is very important that the bypass rule is placed at the top of all other NAT rules.

Another issue is if you have IP/Fasttrack enabled, the packet bypasses IPsec policies. So we need to add accept rule before FastTrack.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall filter</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">place-before</code><code class="ros plain">=1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros value">src-address</code><code class="ros plain">=10.1.101.0/24</code> <code class="ros value">dst-address</code><code class="ros plain">=10.1.202.0/24</code> <code class="ros value">connection-state</code><code class="ros plain">=established,related</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">action</code><code class="ros plain">=accept</code> <code class="ros value">place-before</code><code class="ros plain">=1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros value">src-address</code><code class="ros plain">=10.1.202.0/24</code> <code class="ros value">dst-address</code><code class="ros plain">=10.1.101.0/24</code> <code class="ros value">connection-state</code><code class="ros plain">=established,related</code></div></div></td></tr></tbody></table>

However, this can add a significant load to the router's CPU if there is a fair amount of tunnels and significant traffic on each tunnel.

The solution is to use IP/Firewall/Raw to bypass connection tracking, that way eliminating the need for filter rules listed above and reducing the load on CPU by approximately 30%.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall raw</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=notrack</code> <code class="ros value">chain</code><code class="ros plain">=prerouting</code> <code class="ros value">src-address</code><code class="ros plain">=10.1.101.0/24</code> <code class="ros value">dst-address</code><code class="ros plain">=10.1.202.0/24</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=notrack</code> <code class="ros value">chain</code><code class="ros plain">=prerouting</code> <code class="ros value">src-address</code><code class="ros plain">=10.1.202.0/24</code> <code class="ros value">dst-address</code><code class="ros plain">=10.1.101.0/24</code></div></div></td></tr></tbody></table>

## Site to Site GRE tunnel over IPsec (IKEv2) using DNS

This example explains how it is possible to establish a secure and encrypted GRE tunnel between two RouterOS devices when one or both sites do not have a static IP address. Before making this configuration possible, it is necessary to have a DNS name assigned to one of the devices which will act as a responder (server). For simplicity, we will use RouterOS built-in DDNS service IP/Cloud.

![](https://help.mikrotik.com/docs/download/attachments/11993097/Site-to-site-gre-over-ipsec-example.png?version=1&modificationDate=1617275261923&api=v2)

### Site 1 (server) configuration

This is the side that will listen to incoming connections and act as a responder. We will use mode config to provide an IP address for the second site, but first, create a loopback (blank) bridge and assign an IP address to it that will be used later for GRE tunnel establishment.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface bridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=loopback</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.99.1</code> <code class="ros value">interface</code><code class="ros plain">=loopback</code></div></div></td></tr></tbody></table>

Continuing with the IPsec configuration, start off by creating a new Phase 1 profile and Phase 2 proposal entries using stronger or weaker encryption parameters that suit your needs. Note that this configuration example will listen to all incoming IKEv2 requests, meaning the profile configuration will be shared between all other configurations (e.g. RoadWarrior).

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec pro</code><code class="ros plain">file</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dh-group</code><code class="ros plain">=ecp256,modp2048,modp1024</code> <code class="ros value">enc-algorithm</code><code class="ros plain">=aes-256,aes-192,aes-128</code> <code class="ros value">name</code><code class="ros plain">=ike2</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec proposal</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">auth-algorithms</code><code class="ros plain">=null</code> <code class="ros value">enc-algorithms</code><code class="ros plain">=aes-128-gcm</code> <code class="ros value">name</code><code class="ros plain">=ike2-gre</code> <code class="ros value">pfs-group</code><code class="ros plain">=none</code></div></div></td></tr></tbody></table>

Next, create a new mode config entry with responder=yes. This will provide an IP configuration for the other site as well as the host (loopback address) for policy generation.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec mode-config</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.99.2</code> <code class="ros value">address-prefix-length</code><code class="ros plain">=32</code> <code class="ros value">name</code><code class="ros plain">=ike2-gre</code> <code class="ros value">split-include</code><code class="ros plain">=192.168.99.1/32</code> <code class="ros value">system-dns</code><code class="ros plain">=no</code></div></div></td></tr></tbody></table>

It is advised to create a new policy group to separate this configuration from any existing or future IPsec configuration.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec policy group</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ike2-gre</code></div></div></td></tr></tbody></table>

Now it is time to set up a new policy template that will match the remote peers new dynamic address and the loopback address.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec policy</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=192.168.99.2/32</code> <code class="ros value">group</code><code class="ros plain">=ike2-gre</code> <code class="ros value">proposal</code><code class="ros plain">=ike2-gre</code> <code class="ros value">src-address</code><code class="ros plain">=192.168.99.1/32</code> <code class="ros value">template</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

The next step is to create a peer configuration that will listen to all IKEv2 requests. If you already have such an entry, you can skip this step.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec peer</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">exchange-mode</code><code class="ros plain">=ike2</code> <code class="ros value">name</code><code class="ros plain">=ike2</code> <code class="ros value">passive</code><code class="ros plain">=yes</code> <code class="ros value">profile</code><code class="ros plain">=ike2</code></div></div></td></tr></tbody></table>

Lastly, set up an identity that will match our remote peer by pre-shared-key authentication with a specific secret.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec identity</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">generate-policy</code><code class="ros plain">=port-strict</code> <code class="ros value">mode-config</code><code class="ros plain">=ike2-gre</code> <code class="ros value">peer</code><code class="ros plain">=ike2</code> <code class="ros value">policy-template-group</code><code class="ros plain">=ike2-gre</code> <code class="ros value">secret</code><code class="ros plain">=test</code></div></div></td></tr></tbody></table>

The server side is now configured and listening to all IKEv2 requests. Please make sure the firewall is not blocking UDP/4500 port.

The last step is to create the GRE interface itself. This can also be done later when an IPsec connection is established from the client-side.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface gre</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">local-address</code><code class="ros plain">=192.168.99.1</code> <code class="ros value">name</code><code class="ros plain">=gre-tunnel1</code> <code class="ros value">remote-address</code><code class="ros plain">=192.168.99.2</code></div></div></td></tr></tbody></table>

Configure IP address and route to remote network through GRE interface.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=172.16.1.1/30</code> <code class="ros value">interface</code><code class="ros plain">=gre-tunnel1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip route</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-network</code><code class="ros plain">=10.1.202.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=172.16.1.2</code></div></div></td></tr></tbody></table>

### Site 2 (client) configuration

Similarly to server configuration, start off by creating a new Phase 1 profile and Phase 2 proposal configurations. Since this site will be the initiator, we can use a more specific profile configuration to control which exact encryption parameters are used, just make sure they overlap with what is configured on the server-side.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec pro</code><code class="ros plain">file</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dh-group</code><code class="ros plain">=ecp256</code> <code class="ros value">enc-algorithm</code><code class="ros plain">=aes-256</code> <code class="ros value">name</code><code class="ros plain">=ike2-gre</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec proposal</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">auth-algorithms</code><code class="ros plain">=null</code> <code class="ros value">enc-algorithms</code><code class="ros plain">=aes-128-gcm</code> <code class="ros value">name</code><code class="ros plain">=ike2-gre</code> <code class="ros value">pfs-group</code><code class="ros plain">=none</code></div></div></td></tr></tbody></table>

Next, create a new mode config entry with responder=no. This will make sure the peer requests IP and split-network configuration from the server.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec mode-config</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ike2-gre</code> <code class="ros value">responder</code><code class="ros plain">=no</code></div></div></td></tr></tbody></table>

It is also advised to create a new policy group to separate this configuration from any existing or future IPsec configuration.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec policy group</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ike2-gre</code></div></div></td></tr></tbody></table>

Create a new policy template on the client-side as well.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec policy</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=192.168.99.1/32</code> <code class="ros value">group</code><code class="ros plain">=ike2-gre</code> <code class="ros value">proposal</code><code class="ros plain">=ike2-gre</code> <code class="ros value">src-address</code><code class="ros plain">=192.168.99.2/32</code> <code class="ros value">template</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Move on to peer configuration. Now we can specify the DNS name for the server under the address parameter. Obviously, you can use an IP address as well.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec peer</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=n.mynetname.net</code> <code class="ros value">exchange-mode</code><code class="ros plain">=ike2</code> <code class="ros value">name</code><code class="ros plain">=p1.ez</code> <code class="ros value">profile</code><code class="ros plain">=ike2-gre</code></div></div></td></tr></tbody></table>

Lastly, create an identity for our newly created peers.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec identity</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">generate-policy</code><code class="ros plain">=port-strict</code> <code class="ros value">mode-config</code><code class="ros plain">=ike2-gre</code> <code class="ros value">peer</code><code class="ros plain">=p1.ez</code> <code class="ros value">policy-template-group</code><code class="ros plain">=ike2-gre</code> <code class="ros value">secret</code><code class="ros plain">=test</code></div></div></td></tr></tbody></table>

If everything was done properly, there should be a new dynamic policy present.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec policy </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: T - template, X - disabled, D - dynamic, I - invalid, A - active, * - default</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">0 T * </code><code class="ros value">group</code><code class="ros plain">=default</code> <code class="ros value">src-address</code><code class="ros plain">=::/0</code> <code class="ros value">dst-address</code><code class="ros plain">=::/0</code> <code class="ros value">protocol</code><code class="ros plain">=all</code> <code class="ros value">proposal</code><code class="ros plain">=default</code> <code class="ros value">template</code><code class="ros plain">=yes</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">1 T </code><code class="ros value">group</code><code class="ros plain">=ike2-gre</code> <code class="ros value">src-address</code><code class="ros plain">=192.168.99.2/32</code> <code class="ros value">dst-address</code><code class="ros plain">=192.168.99.1/32</code> <code class="ros value">protocol</code><code class="ros plain">=all</code> <code class="ros value">proposal</code><code class="ros plain">=ike2-gre</code> <code class="ros value">template</code><code class="ros plain">=yes</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">2 DA </code><code class="ros value">src-address</code><code class="ros plain">=192.168.99.2/32</code> <code class="ros value">src-port</code><code class="ros plain">=any</code> <code class="ros value">dst-address</code><code class="ros plain">=192.168.99.1/32</code> <code class="ros value">dst-port</code><code class="ros plain">=any</code> <code class="ros value">protocol</code><code class="ros plain">=all</code> <code class="ros value">action</code><code class="ros plain">=encrypt</code> <code class="ros value">level</code><code class="ros plain">=unique</code> <code class="ros value">ipsec-protocols</code><code class="ros plain">=esp</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros value">tunnel</code><code class="ros plain">=yes</code> <code class="ros value">sa-src-address</code><code class="ros plain">=192.168.90.1</code> <code class="ros value">sa-dst-address</code><code class="ros plain">=(current</code> <code class="ros plain">IP of n.mynetname.net) </code><code class="ros value">proposal</code><code class="ros plain">=ike2-gre</code> <code class="ros value">ph2-count</code><code class="ros plain">=1</code></div></div></td></tr></tbody></table>

A secure tunnel is now established between both sites which will encrypt all traffic between 192.168.99.2 <=> 192.168.99.1 addresses. We can use these addresses to create a GRE tunnel.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface gre</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">local-address</code><code class="ros plain">=192.168.99.2</code> <code class="ros value">name</code><code class="ros plain">=gre-tunnel1</code> <code class="ros value">remote-address</code><code class="ros plain">=192.168.99.1</code></div></div></td></tr></tbody></table>

Configure IP address and route to remote network through GRE interface.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip address</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=172.16.1.2/30</code> <code class="ros value">interface</code><code class="ros plain">=gre-tunnel1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip route</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-network</code><code class="ros plain">=10.1.101.0/24</code> <code class="ros value">gateway</code><code class="ros plain">=172.16.1.1</code></div></div></td></tr></tbody></table>

## Road Warrior setup using IKEv2 with RSA authentication

This example explains how to establish a secure IPsec connection between a device connected to the Internet (road warrior client) and a device running RouterOS acting as a server.

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ipsec-road-warrior.png?version=1&modificationDate=1615382411689&api=v2)

### RouterOS server configuration

Before configuring IPsec, it is required to set up certificates. It is possible to use a separate Certificate Authority for certificate management, however in this example, self-signed certificates are generated in RouterOS System/Certificates menu. Some certificate requirements should be met to connect various devices to the server:

-   Common name should contain IP or DNS name of the server;
-   SAN (subject alternative name) should have IP or DNS of the server;
-   EKU (extended key usage) tls-server and tls-client are required.

Considering all requirements above, generate CA and server certificates:

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/certificate</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">common-name</code><code class="ros plain">=ca</code> <code class="ros value">name</code><code class="ros plain">=ca</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">sign ca </code><code class="ros value">ca-crl-host</code><code class="ros plain">=2.2.2.2</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">common-name</code><code class="ros plain">=2.2.2.2</code> <code class="ros value">subject-alt-name</code><code class="ros plain">=IP:2.2.2.2</code> <code class="ros value">key-usage</code><code class="ros plain">=tls-server</code> <code class="ros value">name</code><code class="ros plain">=server1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">sign server1 </code><code class="ros value">ca</code><code class="ros plain">=ca</code></div></div></td></tr></tbody></table>

Now that valid certificates are created on the router, add a new Phase 1 profile and Phase 2 proposal entries with pfs-group=none:

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec pro</code><code class="ros plain">file</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ike2</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec proposal</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ike2</code> <code class="ros value">pfs-group</code><code class="ros plain">=none</code></div></div></td></tr></tbody></table>

Mode config is used for address distribution from IP/Pools:

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip pool</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ike2-pool</code> <code class="ros value">ranges</code><code class="ros plain">=192.168.77.2-192.168.77.254</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec mode-config</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address-pool</code><code class="ros plain">=ike2-pool</code> <code class="ros value">address-prefix-length</code><code class="ros plain">=32</code> <code class="ros value">name</code><code class="ros plain">=ike2-conf</code></div></div></td></tr></tbody></table>

Since that the policy template must be adjusted to allow only specific network policies, it is advised to create a separate policy group and template.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec policy group</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ike2-policies</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec policy</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=192.168.77.0/24</code> <code class="ros value">group</code><code class="ros plain">=ike2-policies</code> <code class="ros value">proposal</code><code class="ros plain">=ike2</code> <code class="ros value">src-address</code><code class="ros plain">=0.0.0.0/0</code> <code class="ros value">template</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Create a new IPsec peer entry that will listen to all incoming IKEv2 requests.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec peer</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">exchange-mode</code><code class="ros plain">=ike2</code> <code class="ros value">name</code><code class="ros plain">=ike2</code> <code class="ros value">passive</code><code class="ros plain">=yes</code> <code class="ros value">profile</code><code class="ros plain">=ike2</code></div></div></td></tr></tbody></table>

#### Identity configuration

The identity menu allows to match specific remote peers and assign different configurations for each one of them. First, create a default identity, that will accept all peers, but will verify the peer's identity with its certificate.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec identity</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">auth-method</code><code class="ros plain">=digital-signature</code> <code class="ros value">certificate</code><code class="ros plain">=server1</code> <code class="ros value">generate-policy</code><code class="ros plain">=port-strict</code> <code class="ros value">mode-config</code><code class="ros plain">=ike2-conf</code> <code class="ros value">peer</code><code class="ros plain">=ike2</code> <code class="ros value">policy-template-group</code><code class="ros plain">=ike2-policies</code></div></div></td></tr></tbody></table>

If the peer's ID (ID\_i) is not matching with the certificate it sends, the identity lookup will fail. See remote-id in the identities section.

For example, we want to assign a different mode config for user "A", who uses certificate "rw-client1" to authenticate itself to the server. First of all, make sure a new mode config is created and ready to be applied for the specific user.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec mode-config</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.66.2</code> <code class="ros value">address-prefix-length</code><code class="ros plain">=32</code> <code class="ros value">name</code><code class="ros plain">=usr_A</code> <code class="ros value">split-include</code><code class="ros plain">=192.168.55.0/24</code> <code class="ros value">system-dns</code><code class="ros plain">=no</code></div></div></td></tr></tbody></table>

It is possible to apply this configuration for user "A" by using the match-by=certificate parameter and specifying his certificate with remote-certificate.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec identity</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">auth-method</code><code class="ros plain">=digital-signature</code> <code class="ros value">certificate</code><code class="ros plain">=server1</code> <code class="ros value">generate-policy</code><code class="ros plain">=port-strict</code> <code class="ros value">match-by</code><code class="ros plain">=certificate</code> <code class="ros value">mode-config</code><code class="ros plain">=usr_A</code> <code class="ros value">peer</code><code class="ros plain">=ike2</code> <code class="ros value">policy-template-group</code><code class="ros plain">=ike2-policies</code> <code class="ros value">remote-certificate</code><code class="ros plain">=rw-client1</code></div></div></td></tr></tbody></table>

#### (Optional) Split tunnel configuration

Split tunneling is a method that allows road warrior clients to only access a specific secured network and at the same time send the rest of the traffic based on their internal routing table (as opposed to sending all traffic over the tunnel). To configure split tunneling, changes to mode config parameters are needed.

For example, we will allow our road warrior clients to only access the 10.5.8.0/24 network.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec mode-conf</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"rw-conf"</code><code class="ros plain">] </code><code class="ros value">split-include</code><code class="ros plain">=10.5.8.0/24</code></div></div></td></tr></tbody></table>

It is also possible to send a specific DNS server for the client to use. By default, system-dns=yes is used, which sends DNS servers that are configured on the router itself in IP/DNS. We can force the client to use a different DNS server by using the static-dns parameter.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec mode-conf</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"rw-conf"</code><code class="ros plain">] </code><code class="ros value">system-dns</code><code class="ros plain">=no</code> <code class="ros value">static-dns</code><code class="ros plain">=10.5.8.1</code></div></div></td></tr></tbody></table>

While it is possible to adjust the IPsec policy template to only allow road warrior clients to generate policies to network configured by split-include parameter, this can cause compatibility issues with different vendor implementations (see known limitations). Instead of adjusting the policy template, allow access to a secured network in IP/Firewall/Filter and drop everything else.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall filter</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=drop</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">src-address</code><code class="ros plain">=192.168.77.0/24</code> <code class="ros value">dst-address</code><code class="ros plain">=!10.5.8.0/24</code></div></div></td></tr></tbody></table>

Split networking is not a security measure. The client (initiator) can still request a different Phase 2 traffic selector.

#### Generating client certificates

To generate a new certificate for the client and sign it with a previously created CA.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/certificate</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">common-name</code><code class="ros plain">=rw-client1</code> <code class="ros value">name</code><code class="ros plain">=rw-client1</code> <code class="ros value">key-usage</code><code class="ros plain">=tls-client</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">sign rw-client1 </code><code class="ros value">ca</code><code class="ros plain">=ca</code></div></div></td></tr></tbody></table>

**PKCS12 format** is accepted by most client implementations, so when exporting the certificate, make sure PKCS12 is specified.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/certificate</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">export-certificate rw-client1 </code><code class="ros value">export-passphrase</code><code class="ros plain">=1234567890</code> <code class="ros value">type</code><code class="ros plain">=pkcs12</code></div></div></td></tr></tbody></table>

A file named _cert\_export\_rw-client1.p12_ is now located in the routers System/File section. This file should be securely transported to the client's device.

Typically PKCS12 bundle contains also a CA certificate, but some vendors may not install this CA, so a self-signed CA certificate must be exported separately using PEM format.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/certificate</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">export-certificate ca </code><code class="ros value">type</code><code class="ros plain">=pem</code></div></div></td></tr></tbody></table>

A file named _cert\_export\_ca.crt_ is now located in the routers System/File section. This file should also be securely transported to the client's device.

**PEM** is another certificate format for use in client software that does not support PKCS12. The principle is pretty much the same.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/certificate</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">export-certificate ca</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">export-certificate rw-client1 </code><code class="ros value">export-passphrase</code><code class="ros plain">=1234567890</code></div></div></td></tr></tbody></table>

Three files are now located in the routers Files section: _cert\_export\_ca.crt_, _cert\_export\_rw-client1.crt_ and _cert\_export\_rw-client1.key_ which should be securely transported to the client device.

#### Known limitations

Here is a list of known limitations by popular client software IKEv2 implementations.

-   Windows will always ignore networks received by split-include and request policy with destination 0.0.0.0/0 (TSr). When IPsec-SA is generated, Windows requests DHCP option 249 to which RouterOS will respond with configured split-include networks automatically.

-   Both Apple macOS and iOS will only accept the first split-include network.

-   Both Apple macOS and iOS will use the DNS servers from system-dns and static-dns parameters only when 0.0.0.0/0 split-include is used.

-   While some implementations can make use of different PFS group for phase 2, it is advised to use pfs-group=none under proposals to avoid any compatibility issues.

### RouterOS client configuration

Import a PKCS12 format certificate in RouterOS.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/certificate </code><code class="ros functions">import </code><code class="ros value">file-name</code><code class="ros plain">=cert_export_RouterOS_client.p12</code> <code class="ros value">passphrase</code><code class="ros plain">=1234567890</code></div></div></td></tr></tbody></table>

There should now be the self-signed CA certificate and the client certificate in the Certificate menu. Find out the name of the client certificate.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/certificate </code><code class="ros functions">print</code></div></div></td></tr></tbody></table>

**cert\_export\_RouterOS\_client.p12\_0** is the client certificate.

It is advised to create a separate Phase 1 profile and Phase 2 proposal configurations to not interfere with any existing IPsec configuration.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec pro</code><code class="ros plain">file</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ike2-rw</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec proposal</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ike2-rw</code> <code class="ros value">pfs-group</code><code class="ros plain">=none</code></div></div></td></tr></tbody></table>

While it is possible to use the default policy template for policy generation, it is better to create a new policy group and template to separate this configuration from any other IPsec configuration.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec policy group</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ike2-rw</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec policy</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">group</code><code class="ros plain">=ike2-rw</code> <code class="ros value">proposal</code><code class="ros plain">=ike2-rw</code> <code class="ros value">template</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Create a new mode config entry with responder=no that will request configuration parameters from the server.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec mode-config</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ike2-rw</code> <code class="ros value">responder</code><code class="ros plain">=no</code></div></div></td></tr></tbody></table>

Lastly, create peer and identity configurations.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec peer</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=2.2.2.2/32</code> <code class="ros value">exchange-mode</code><code class="ros plain">=ike2</code> <code class="ros value">name</code><code class="ros plain">=ike2-rw-client</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec identity</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">auth-method</code><code class="ros plain">=digital-signature</code> <code class="ros value">certificate</code><code class="ros plain">=cert_export_RouterOS_client.p12_0</code> <code class="ros value">generate-policy</code><code class="ros plain">=port-strict</code> <code class="ros value">mode-config</code><code class="ros plain">=ike2-rw</code> <code class="ros value">peer</code><code class="ros plain">=ike2-rw-client</code> <code class="ros value">policy-template-group</code><code class="ros plain">=ike2-rw</code></div></div></td></tr></tbody></table>

Verify that the connection is successfully established.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">active-peers print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">installed-sa </code><code class="ros functions">print</code></div></div></td></tr></tbody></table>

#### Enabling dynamic source NAT rule generation

If we look at the generated dynamic policies, we see that only traffic with a specific (received by mode config) source address will be sent through the tunnel. But a router in most cases will need to route a specific device or network through the tunnel. In such case, we can use source NAT to change the source address of packets to match the mode config address. Since the mode config address is dynamic, it is impossible to create a static source NAT rule. In RouterOS, it is possible to generate dynamic source NAT rules for mode config clients.

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ipsec-road-warrior-client.png?version=1&modificationDate=1617263807501&api=v2)

For example, we have a local network 192.168.88.0/24 behind the router and we want all traffic from this network to be sent over the tunnel. First of all, we have to make a new IP/Firewall/Address list which consists of our local network

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip firewall address-list</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=192.168.88.0/24</code> <code class="ros value">list</code><code class="ros plain">=local</code></div></div></td></tr></tbody></table>

When it is done, we can assign the newly created IP/Firewall/Address list to the mode config configuration.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec mode-config</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[ </code><code class="ros functions">find </code><code class="ros value">name</code><code class="ros plain">=ike2-rw</code> <code class="ros plain">] </code><code class="ros value">src-address-list</code><code class="ros plain">=local</code></div></div></td></tr></tbody></table>

Verify correct source NAT rule is dynamically generated when the tunnel is established.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/ip firewall nat </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - invalid, D - dynamic</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">0 D ;;; ipsec mode-config</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros value">chain</code><code class="ros plain">=srcnat</code> <code class="ros value">action</code><code class="ros plain">=src-nat</code> <code class="ros value">to-addresses</code><code class="ros plain">=192.168.77.254</code> <code class="ros value">src-address-list</code><code class="ros plain">=local</code> <code class="ros value">dst-address-list</code><code class="ros plain">=!local</code></div></div></td></tr></tbody></table>

Make sure the dynamic mode config address is not a part of a local network.

### Windows client configuration

Open PKCS12 format certificate file on the Windows computer. Install the certificate by following the instructions. Make sure you select the Local Machine store location.![](https://help.mikrotik.com/docs/download/attachments/11993097/Ike2v2_cert_win.png?version=1&modificationDate=1617264637750&api=v2) You can now proceed to Network and Internet settings -> VPN and add a new configuration. Fill in the Connection name, Server name, or address parameters. Select IKEv2 under VPN type. When it is done, it is necessary to select "Use machine certificates". This can be done in Network and Sharing Center by clicking the Properties menu for the VPN connection. The setting is located under the Security tab.

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ike2v2_conf_win.png?version=1&modificationDate=1617264693224&api=v2)

Currently, Windows 10 is compatible with the following Phase 1 ( profiles) and Phase 2 ( proposals) proposal sets:

| Phase 1        |
| -------------- |
| Hash Algorithm | Encryption Algorithm | DH Group |
| SHA1           | 3DES                 | modp1024 |
| SHA256         | 3DES                 | modp1024 |
| SHA1           | AES-128-CBC          | modp1024 |
| SHA256         | AES-128-CBC          | modp1024 |
| SHA1           | AES-192-CBC          | modp1024 |
| SHA256         | AES-192-CBC          | modp1024 |
| SHA1           | AES-256-CBC          | modp1024 |
| SHA256         | AES-256-CBC          | modp1024 |
| SHA1           | AES-128-GCM          | modp1024 |
| SHA256         | AES-128-GCM          | modp1024 |
| SHA1           | AES-256-GCM          | modp1024 |
| SHA256         | AES-256-GCM          | modp1024 |

  

| Phase 2        |
| -------------- |
| Hash Algorithm | Encryption Algorithm | PFS Group |
| SHA1           | AES-256-CBC          | none      |
| SHA1           | AES-128-CBC          | none      |
| SHA1           | 3DES                 | none      |
| SHA1           | DES                  | none      |
| SHA1           | none                 | none      |

### macOS client configuration

Open the PKCS12 format certificate file on the macOS computer and install the certificate in the "System" keychain. It is necessary to mark the CA certificate as trusted manually since it is self-signed. Locate the certificate macOS Keychain Access app under the System tab and mark it as Always Trust.

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ikev2_cert_macos.png?version=1&modificationDate=1617265736527&api=v2)

You can now proceed to System Preferences -> Network and add a new configuration by clicking the + button. Select Interface: VPN, VPN Type: IKEv2 and name your connection. Remote ID must be set equal to common-name or subjAltName of server's certificate. Local ID can be left blank. Under Authentication Settings select None and choose the client certificate. You can now test the connectivity.

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ikev2_conf_macos.png?version=1&modificationDate=1617265766455&api=v2)

Currently, macOS is compatible with the following Phase 1 ( profiles) and Phase 2 ( proposals) proposal sets:

| Phase 1        |
| -------------- |
| Hash Algorithm | Encryption Algorithm | DH Group |
| SHA256         | AES-256-CBC          | modp2048 |
| SHA256         | AES-256-CBC          | ecp256   |
| SHA256         | AES-256-CBC          | modp1536 |
| SHA1           | AES-128-CBC          | modp1024 |
| SHA1           | 3DES                 | modp1024 |

  

| Phase 2        |
| -------------- |
| Hash Algorithm | Encryption Algorithm | PFS Group |
| SHA256         | AES-256-CBC          | none      |
| SHA1           | AES-128-CBC          | none      |
| SHA1           | 3DES                 | none      |

### iOS client configuration

Typically PKCS12 bundle contains also a CA certificate, but iOS does not install this CA, so a self-signed CA certificate must be installed separately using PEM format. Open these files on the iOS device and install both certificates by following the instructions. It is necessary to mark the self-signed CA certificate as trusted on the iOS device. This can be done in Settings -> General -> About -> Certificate Trust Settings menu. When it is done, check whether both certificates are marked as "verified" under the Settings -> General -> Profiles menu.

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ikev2_cert_ios.png?version=1&modificationDate=1617265950259&api=v2)

You can now proceed to Settings -> General -> VPN menu and add a new configuration. Remote ID must be set equal to common-name or subjAltName of server's certificate. Local ID can be left blank.

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ikev2_conf_ios.png?version=1&modificationDate=1617265989863&api=v2)

Currently, iOS is compatible with the following Phase 1 ( profiles) and Phase 2 ( proposals) proposal sets:

| Phase 1        |
| -------------- |
| Hash Algorithm | Encryption Algorithm | DH Group |
| SHA256         | AES-256-CBC          | modp2048 |
| SHA256         | AES-256-CBC          | ecp256   |
| SHA256         | AES-256-CBC          | modp1536 |
| SHA1           | AES-128-CBC          | modp1024 |
| SHA1           | 3DES                 | modp1024 |

  

| Phase 2        |
| -------------- |
| Hash Algorithm | Encryption Algorithm | PFS Group |
| SHA256         | AES-256-CBC          | none      |
| SHA1           | AES-128-CBC          | none      |
| SHA1           | 3DES                 | none      |

If you are connected to the VPN over WiFi, the iOS device can go into sleep mode and disconnect from the network.

### Android (strongSwan) client configuration

Currently, there is no IKEv2 native support in Android, however, it is possible to use strongSwan from Google Play Store which brings IKEv2 to Android. StrongSwan accepts PKCS12 format certificates, so before setting up the VPN connection in strongSwan, make sure you download the PKCS12 bundle to your Android device. When it is done, create a new VPN profile in strongSwan, type in the server IP, and choose "IKEv2 Certificate" as VPN Type. When selecting a User certificate, press Install and follow the certificate extract procedure by specifying the PKCS12 bundle. Save the profile and test the connection by pressing on the VPN profile.

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ikev2_conf_android.png?version=1&modificationDate=1617266889478&api=v2)

It is possible to specify custom encryption settings in strongSwan by ticking the "Show advanced settings" checkbox. Currently, strongSwan by default is compatible with the following Phase 1 ( profiles) and Phase 2 ( proposals) proposal sets:

| Phase 1        |
| -------------- |
| Hash Algorithm | Encryption Algorithm | DH Group |
| SHA\*          | AES-\*-CBC           | modp2048 |
| SHA\*          | AES-\*-CBC           | ecp256   |
| SHA\*          | AES-\*-CBC           | ecp384   |
| SHA\*          | AES-\*-CBC           | ecp521   |
| SHA\*          | AES-\*-CBC           | modp3072 |
| SHA\*          | AES-\*-CBC           | modp4096 |
| SHA\*          | AES-\*-CBC           | modp6144 |
| SHA\*          | AES-\*-CBC           | modp8192 |
| SHA\*          | AES-\*-GCM           | modp2048 |
| SHA\*          | AES-\*-GCM           | ecp256   |
| SHA\*          | AES-\*-GCM           | ecp384   |
| SHA\*          | AES-\*-GCM           | ecp521   |
| SHA\*          | AES-\*-GCM           | modp3072 |
| SHA\*          | AES-\*-GCM           | modp4096 |
| SHA\*          | AES-\*-GCM           | modp6144 |
| SHA\*          | AES-\*-GCM           | modp8192 |

  

| Phase 2        |
| -------------- |
| Hash Algorithm | Encryption Algorithm | PFS Group |
| none           | AES-256-GCM          | none      |
| none           | AES-128-GCM          | none      |
| SHA256         | AES-256-CBC          | none      |
| SHA512         | AES-256-CBC          | none      |
| SHA1           | AES-256-CBC          | none      |
| SHA256         | AES-192-CBC          | none      |
| SHA512         | AES-192-CBC          | none      |
| SHA1           | AES-192-CBC          | none      |
| SHA256         | AES-128-CBC          | none      |
| SHA512         | AES-128-CBC          | none      |
| SHA1           | AES-128-CBC          | none      |

### Linux (strongSwan) client configuration

Download the PKCS12 certificate bundle and move it to /etc/ipsec.d/private directory.

Add exported passphrase for the private key to /etc/ipsec.secrets file where "strongSwan\_client.p12" is the file name and "1234567890" is the passphrase.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="bash plain">: P12 strongSwan_client.p12 </code><code class="bash string">"1234567890"</code></div></div></td></tr></tbody></table>

Add a new connection to /etc/ipsec.conf file

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="bash plain">conn </code><code class="bash string">"ikev2"</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="bash plain">keyexchange=ikev2</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="bash plain">ike=aes128-sha1-modp2048</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="bash plain">esp=aes128-sha1</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="bash plain">leftsourceip=%modeconfig</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="bash plain">leftcert=strongSwan_client.p12</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="bash plain">leftfirewall=</code><code class="bash functions">yes</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="bash plain">right=2.2.2.2</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="bash plain">rightid=</code><code class="bash string">"CN=2.2.2.2"</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="bash plain">rightsubnet=0.0.0.0</code><code class="bash plain">/0</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="bash plain">auto=add</code></div></div></td></tr></tbody></table>

You can now restart (or start) the ipsec daemon and initialize the connection

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="bash plain">$ ipsec restart</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="bash plain">$ ipsec up ikev2</code></div></div></td></tr></tbody></table>

## Road Warrior setup using IKEv2 with EAP-MSCHAPv2 authentication handled by User Manager (RouterOS v7)  

This example explains how to establish a secure IPsec connection between a device connected to the Internet (road warrior client) and a device running RouterOS acting as an IKEv2 server and User Manager. It is possible to run User Manager on a separate device in network, however in this example both User Manager and IKEv2 server will be configured on the same device (Office).  

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ipsec-road-warrior.png?version=1&modificationDate=1615382411689&api=v2)

### RouterOS server configuration

#### Requirements

For this setup to work there are several prerequisites for the router:

1.  Router's IP address should have a valid public DNS record - IP Cloud could be used to achieve this.
2.  Router should be reachable through port TCP/80 over the Internet - if the server is behind NAT, port forwarding should be configured.
3.  User Manager package should be installed on the router.

#### Generating Let's Encrypt certificate

During the EAP-MSCHAPv2 authentication, TLS handshake has to take place, which means the server has to have a certificate that can be validated by the client. To simplify this step, we will use Let's Encrypt certificate which can be validated by most operating systems without any intervention by the user. To generate the certificate, simply enable SSL certificate under the Certificates menu. By default the command uses the dynamic DNS record provided by IP Cloud, however a custom DNS name can also be specified. Note that, the DNS record should point to the router.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/certificate enable-ssl-certificate</code></div></div></td></tr></tbody></table>

If the certificate generation succeeded, you should see the Let's Encrypt certificate installed under the Certificates menu.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/certificate </code><code class="ros functions">print </code><code class="ros functions">detail </code><code class="ros plain">where name~</code><code class="ros string">"letsencrypt"</code></div></div></td></tr></tbody></table>

#### Configuring User Manager

First of all, allow receiving RADIUS requests from the localhost (the router itself):

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user-manager router</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=127.0.0.1</code> <code class="ros value">comment</code><code class="ros plain">=localhost</code> <code class="ros value">name</code><code class="ros plain">=local</code> <code class="ros value">shared-secret</code><code class="ros plain">=test</code></div></div></td></tr></tbody></table>

Enable the User Manager and specify the Let's Encrypt certificate (replace the name of the certificate to the one installed on your device) that will be used to authenticate the users.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user-manager</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">certificate</code><code class="ros plain">=</code><code class="ros string">"letsencrypt_2021-04-09T07:10:55Z"</code> <code class="ros value">enabled</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Lastly add users and their credentials that clients will use to authenticate to the server.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user-manager user</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=user1</code> <code class="ros value">password</code><code class="ros plain">=password</code></div></div></td></tr></tbody></table>

#### Configuring RADIUS client

For the router to use RADIUS server for user authentication, it is required to add a new RADIUS client that has the same shared secret that we already configured on User Manager.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/radius</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=127.0.0.1</code> <code class="ros value">secret</code><code class="ros plain">=test</code> <code class="ros value">service</code><code class="ros plain">=ipsec</code></div></div></td></tr></tbody></table>

#### IPsec (IKEv2) server configuration

Add a new Phase 1 profile and Phase 2 proposal entries with pfs-group=none:

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec pro</code><code class="ros plain">file</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ike2</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec proposal</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ike2</code> <code class="ros value">pfs-group</code><code class="ros plain">=none</code></div></div></td></tr></tbody></table>

Mode config is used for address distribution from IP/Pools.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip pool</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ike2-pool</code> <code class="ros value">ranges</code><code class="ros plain">=192.168.77.2-192.168.77.254</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec mode-config</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address-pool</code><code class="ros plain">=ike2-pool</code> <code class="ros value">address-prefix-length</code><code class="ros plain">=32</code> <code class="ros value">name</code><code class="ros plain">=ike2-conf</code></div></div></td></tr></tbody></table>

Since that the policy template must be adjusted to allow only specific network policies, it is advised to create a separate policy group and template.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec policy group</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ike2-policies</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec policy</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">dst-address</code><code class="ros plain">=192.168.77.0/24</code> <code class="ros value">group</code><code class="ros plain">=ike2-policies</code> <code class="ros value">proposal</code><code class="ros plain">=ike2</code> <code class="ros value">src-address</code><code class="ros plain">=0.0.0.0/0</code> <code class="ros value">template</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Create a new IPsec peer entry which will listen to all incoming IKEv2 requests.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec peer</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">exchange-mode</code><code class="ros plain">=ike2</code> <code class="ros value">name</code><code class="ros plain">=ike2</code> <code class="ros value">passive</code><code class="ros plain">=yes</code> <code class="ros value">profile</code><code class="ros plain">=ike2</code></div></div></td></tr></tbody></table>

Lastly create a new IPsec identity entry that will match all clients trying to authenticate with EAP. Note that generated Let's Encrypt certificate must be specified.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec identity</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">auth-method</code><code class="ros plain">=eap-radius</code> <code class="ros value">certificate</code><code class="ros plain">=</code><code class="ros string">"letsencrypt_2021-04-09T07:10:55Z"</code> <code class="ros value">generate-policy</code><code class="ros plain">=port-strict</code> <code class="ros value">mode-config</code><code class="ros plain">=ike2-conf</code> <code class="ros value">peer</code><code class="ros plain">=ike2</code> <code class="ros plain">\</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros value">policy-template-group</code><code class="ros plain">=ike2-policies</code></div></div></td></tr></tbody></table>

#### (Optional) Split tunnel configuration

Split tunneling is a method that allows road warrior clients to only access a specific secured network and at the same time send the rest of the traffic based on their internal routing table (as opposed to sending all traffic over the tunnel). To configure split tunneling, changes to mode config parameters are needed.

For example, we will allow our road warrior clients to only access the 10.5.8.0/24 network.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec mode-conf</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"rw-conf"</code><code class="ros plain">] </code><code class="ros value">split-include</code><code class="ros plain">=10.5.8.0/24</code></div></div></td></tr></tbody></table>

It is also possible to send a specific DNS server for the client to use. By default, system-dns=yes is used, which sends DNS servers that are configured on the router itself in IP/DNS. We can force the client to use a different DNS server by using the static-dns parameter.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec mode-conf</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"rw-conf"</code><code class="ros plain">] </code><code class="ros value">system-dns</code><code class="ros plain">=no</code> <code class="ros value">static-dns</code><code class="ros plain">=10.5.8.1</code></div></div></td></tr></tbody></table>

  

Split networking is not a security measure. The client (initiator) can still request a different Phase 2 traffic selector.

#### (Optional) Assigning static IP address to user

Static IP address to any user can be assigned by use of RADIUS Framed-IP-Address attribute.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user-manager user</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"user1"</code><code class="ros plain">] </code><code class="ros value">attributes</code><code class="ros plain">=Framed-IP-Address:192.168.77.100</code> <code class="ros value">shared-users</code><code class="ros plain">=1</code></div></div></td></tr></tbody></table>

To avoid any conflicts, the static IP address should be excluded from the IP pool of other users, as well as shared-users should be set to 1 for the specific user.

#### (Optional) Accounting configuration

To keep track of every user's uptime, download and upload statistics, RADIUS accounting can be used. By default RADIUS accounting is already enabled for IPsec, but it is advised to configure Interim Update timer that sends statistic to the RADIUS server regularly. If the router will handle a lot of simultaneous sessions, it is advised to increase the update timer to avoid increased CPU usage.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ipsec settings</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">interim-update</code><code class="ros plain">=1m</code></div></div></td></tr></tbody></table>

## Basic L2TP/IPsec setup

This example demonstrates how to easily set up an L2TP/IPsec server on RouterOS for road warrior connections (works with Windows, Android, iOS, macOS, and other vendor L2TP/IPsec implementations).

### RouterOS server configuration

The first step is to enable the L2TP server:

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface l2tp-server server</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">enabled</code><code class="ros plain">=yes</code> <code class="ros value">use-ipsec</code><code class="ros plain">=required</code> <code class="ros value">ipsec-secret</code><code class="ros plain">=mySecret</code> <code class="ros value">default-profile</code><code class="ros plain">=default</code></div></div></td></tr></tbody></table>

use-ipsec is set to **required** to make sure that only IPsec encapsulated L2TP connections are accepted.

Now what it does is enables an L2TP server and creates a dynamic IPsec peer with a specified secret.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/ip ipsec peer&gt; </code><code class="ros functions">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">0 D </code><code class="ros value">address</code><code class="ros plain">=0.0.0.0/0</code> <code class="ros value">local-address</code><code class="ros plain">=0.0.0.0</code> <code class="ros value">passive</code><code class="ros plain">=yes</code> <code class="ros value">port</code><code class="ros plain">=500</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros value">auth-method</code><code class="ros plain">=pre-shared-key</code> <code class="ros value">secret</code><code class="ros plain">=</code><code class="ros string">"123"</code> <code class="ros value">generate-policy</code><code class="ros plain">=port-strict</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros value">exchange-mode</code><code class="ros plain">=main-l2tp</code> <code class="ros value">send-initial-contact</code><code class="ros plain">=yes</code> <code class="ros value">nat-traversal</code><code class="ros plain">=yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros value">hash-algorithm</code><code class="ros plain">=sha1</code> <code class="ros value">enc-algorithm</code><code class="ros plain">=3des,aes-128,aes-192,aes-256</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros value">dh-group</code><code class="ros plain">=modp1024</code> <code class="ros value">lifetime</code><code class="ros plain">=1d</code> <code class="ros value">dpd-interval</code><code class="ros plain">=2m</code> <code class="ros value">dpd-maximum-failures</code><code class="ros plain">=5</code></div></div></td></tr></tbody></table>

Care must be taken if static IPsec peer configuration exists.

The next step is to create a VPN pool and add some users.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip pool </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=vpn-pool</code> <code class="ros value">range</code><code class="ros plain">=192.168.99.2-192.168.99.100</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/ppp pro</code><code class="ros plain">file</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">default </code><code class="ros value">local-address</code><code class="ros plain">=192.168.99.1</code> <code class="ros value">remote-address</code><code class="ros plain">=vpn-pool</code></div><div class="line number5 index4 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/ppp secret</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=user1</code> <code class="ros value">password</code><code class="ros plain">=123</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=user2</code> <code class="ros value">password</code><code class="ros plain">=234</code></div></div></td></tr></tbody></table>

Now the router is ready to accept L2TP/IPsec client connections.

### RouterOS client configuration

For RouterOS to work as L2TP/IPsec client, it is as simple as adding a new L2TP client.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface l2tp-client</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">connect-to</code><code class="ros plain">=1.1.1.1</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">ipsec-secret</code><code class="ros plain">=mySecret</code> <code class="ros value">name</code><code class="ros plain">=l2tp-out1</code> <code class="ros plain">\</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros value">password</code><code class="ros plain">=123</code> <code class="ros value">use-ipsec</code><code class="ros plain">=yes</code> <code class="ros value">user</code><code class="ros plain">=user1</code></div></div></td></tr></tbody></table>

It will automatically create dynamic IPsec peer and policy configurations.

## Troubleshooting/FAQ

**Phase 1 Failed to get a valid proposal**

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/log&gt; </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">(..)</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">17</code><code class="ros constants">:12:32 ipsec,</code><code class="ros functions">error </code><code class="ros plain">no suitable proposal found.</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">17</code><code class="ros constants">:12:32 ipsec,</code><code class="ros functions">error </code><code class="ros plain">10.5.107.112 failed to </code><code class="ros functions">get </code><code class="ros plain">valid proposal.</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">17</code><code class="ros constants">:12:32 ipsec,</code><code class="ros functions">error </code><code class="ros plain">10.5.107.112 failed to pre-process ph1 packet (side</code><code class="ros constants">: 1, status 1).</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">17</code><code class="ros constants">:12:32 ipsec,</code><code class="ros functions">error </code><code class="ros plain">10.5.107.112 phase1 negotiation failed.</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">(..)</code></div></div></td></tr></tbody></table>

Peers are unable to negotiate encryption parameters causing the connection to drop. To solve this issue, enable IPSec to debug logs and find out which parameters are proposed by the remote peer, and adjust the configuration accordingly.

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/system logging&gt; </code><code class="ros functions">add </code><code class="ros value">topics</code><code class="ros plain">=ipsec,!debug</code></div></div></td></tr></tbody></table>

[?](https://help.mikrotik.com/docs/display/ROS/IPsec#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/log&gt; </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">(..)</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">17</code><code class="ros constants">:21:08 ipsec rejected hashtype: DB(prop#1:trns#1):Peer(prop#1:trns#1) = MD5:SHA</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">17</code><code class="ros constants">:21:08 ipsec rejected enctype: DB(prop#1:trns#2):Peer(prop#1:trns#1) = 3DES-CBC:AES-CBC</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">17</code><code class="ros constants">:21:08 ipsec rejected hashtype: DB(prop#1:trns#2):Peer(prop#1:trns#1) = MD5:SHA</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">17</code><code class="ros constants">:21:08 ipsec rejected enctype: DB(prop#1:trns#1):Peer(prop#1:trns#2) = AES-CBC:3DES-CBC</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">17</code><code class="ros constants">:21:08 ipsec rejected hashtype: DB(prop#1:trns#1):Peer(prop#1:trns#2) = MD5:SHA</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">17</code><code class="ros constants">:21:08 ipsec rejected hashtype: DB(prop#1:trns#2):Peer(prop#1:trns#2) = MD5:SHA</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">17</code><code class="ros constants">:21:08 ipsec,</code><code class="ros functions">error </code><code class="ros plain">no suitable proposal found.</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">17</code><code class="ros constants">:21:08 ipsec,</code><code class="ros functions">error </code><code class="ros plain">10.5.107.112 failed to </code><code class="ros functions">get </code><code class="ros plain">valid proposal.</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">17</code><code class="ros constants">:21:08 ipsec,</code><code class="ros functions">error </code><code class="ros plain">10.5.107.112 failed to pre-process ph1 packet (side</code><code class="ros constants">: 1, status 1).</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">17</code><code class="ros constants">:21:08 ipsec,</code><code class="ros functions">error </code><code class="ros plain">10.5.107.112 phase1 negotiation failed.</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros plain">(..)</code></div></div></td></tr></tbody></table>

In this example, the remote end requires SHA1 to be used as a hash algorithm, but MD5 is configured on the local router. Setting before the column symbol (:) is configured on the local side, parameter after the column symbol (:) is configured on the remote side.

**"phase1 negotiation failed due to time up" what does it mean?**

There are communication problems between the peers. Possible causes include - misconfigured Phase 1 IP addresses; firewall blocking UDP ports 500 and 4500; NAT between peers not properly translating IPsec negotiation packets. This error message can also appear when a local-address parameter is not used properly. More information available here.

**Random packet drops or connections over the tunnel are very slow, enabling packet sniffer/torch fixes the problem?**

Problem is that before encapsulation packets are sent to Fasttrack/FastPath, thus bypassing IPsec policy checking. The solution is to exclude traffic that needs to be encapsulated/decapsulated from Fasttrack, see configuration example here.

**How to enable ike2?**

For basic configuration enabling ike2 is very simple, just change exchange-mode in peer settings to ike2.

**fatal NO-PROPOSAL-CHOSEN notify message?**

Remote peer sent notify that it cannot accept proposed algorithms, to find the exact cause of the problem, look at remote peers debug logs or configuration and verify that both client and server have the same set of algorithms.

**I can ping only in one direction?**

A typical problem in such cases is strict firewall, firewall rules allow the creation of new connections only in one direction. The solution is to recheck firewall rules, or explicitly accept all traffic that should be encapsulated/decapsulated.

**Can I allow only encrypted traffic?**

Yes, you can, see "Allow only IPsec encapsulated traffic" examples.

**I enable IKEv2 REAUTH on StrongSwan and got the error 'initiator did not reauthenticate as requested'**

RouterOS does not support rfc4478, reauth must be disabled on StrongSwan.