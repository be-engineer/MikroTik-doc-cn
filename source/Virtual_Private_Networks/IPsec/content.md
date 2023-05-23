# 介绍


**互联网协议安全(IPsec)** 是由互联网工程任务组(IETF)定义的一组协议，用于在未受保护的IP/IPv6网络(如Internet)上确保数据包交换的安全。


IPsec协议套件可以分为以下几组:

- **IKE (Internet Key Exchange)协议** 动态生成和分发AH和ESP的加密密钥。
- **认证头(AH)** RFC 4302
- **封装ESP (Security Payload)** RFC 4303

# Internet密钥交换协议(IKE)

IKE (Internet Key Exchange)是一种为ISAKMP (Internet Security Association and Key Management protocol)框架提供经过认证的密钥材料的协议。还有其他与ISAKMP一起工作的密钥交换方案，但IKE是使用最广泛的一种。它们共同提供了对主机进行身份验证和自动管理安全协会(SA)的方法。

大多数时候，IKE守护进程什么也不做。当它被激活时有两种可能的情况:

策略规则捕获了一些流量，需要对其进行加密或身份验证，但该策略没有任何sa。策略通知IKE守护进程，IKE守护进程发起到远程主机的连接。IKE守护进程响应远程连接。在这两种情况下，对等体建立连接并执行2个阶段:

- 阶段1 -对等体同意在接下来的IKE消息和身份验证中使用的算法。还生成了用于派生所有sa密钥和保护主机之间后续ISAKMP交换的密钥材料。这个阶段应该匹配以下设置:
    - 认证方法
    - DH组
    - 加密算法
    - 交换模式
    - 哈希算法
    - NAT-T
    - DPD和寿命(可选)

- **阶段2** -对等体之间建立一个或多个安全联盟，用于IPsec对数据进行加密。所有由IKE守护进程建立的SA都有生命周期值(限制时间，超过此时间SA将失效，或者可以由该SA加密的数据量，或者两者都有)。这个阶段应该匹配以下设置:
    - IPsec协议
    - 模式(隧道或运输)
    - 认证方法
    - PFS (DH)组
    - 寿命值

有两个寿命值 - 软和硬。 当SA达到其柔软的寿命阈值时，Ike守护程序会收到通知，并开始另一阶段2交换，以新鲜的SA替换此SA。 如果SA终生艰难，它将被丢弃。

如果在生命周期到期时禁用DPD，则阶段1不会重新钥匙，仅重新键入阶段2。 要强制1阶段重新接键，请启用DPD。

众所周知，PSK身份验证在“激进”模式下对离线攻击很容易受到攻击，但是最近的发现表明，在“ Main”和“ IKE2”交换模式的情况下，离线攻击也是可能的。 一般建议是避免使用PSK身份验证方法。

ike可以选择提供一个完美的远期保密（PFS），这是密钥交换的属性，这反过来又意味着损害长期阶段1密钥的IKE将不允许轻松访问所有受保护的IPSEC数据 通过通过此阶段1建立的SAS，这意味着为每个阶段2生成了其他键合材料。

键盘材料的产生在计算上非常昂贵。 示例性Gratia，即使在非常快的计算机上，MODP8192组的使用也可能需要几秒钟。 它通常发生每阶段1交换一次，这在任何主机对之间仅发生一次，然后将其保存很长时间。 PFS还将此昂贵的操作添加到每个2阶段的交换中。

## Diffie-Hellman组

Diffie-Hellman（DH）密钥交换协议允许双方没有任何初始共享的秘密来安全地创建一个方。 支持以下模块化指数（MODP）和椭圆曲线（EC2N）Diffie-Hellman（也称为“ Oakley”）组：

| Diffie-Hellman Group | Name                      | Reference |
| -------------------- | ------------------------- | --------- |
| Group 1              | 768 bits MODP group       | RFC 2409  |
| Group 2              | 1024 bits MODP group      | RFC 2409  |
| Group 3              | EC2N group on GP(2^155)   | RFC 2409  |
| Group 4              | EC2N group on GP(2^185)   | RFC 2409  |
| Group 5              | 1536 bits MODP group      | RFC 3526  |
| Group 14             | 2048 bits MODP group      | RFC 3526  |
| Group 15             | 3072 bits MODP group      | RFC 3526  |
| Group 16             | 4096 bits MODP group      | RFC 3526  |
| Group 17             | 6144 bits MODP group      | RFC 3526  |
| Group 18             | 8192 bits MODP group      | RFC 3526  |
| Group 19             | 256 bits random ECP group | RFC 5903  |
| Group 20             | 384 bits random ECP group | RFC 5903  |
| Group 21             | 521 bits random ECP group | RFC 5903  |

[此处](https://www.iana.org/assignments/ipsec-registry/ipsec-registry.xhtml) 可以找到有关标准的更多信息。

## ike流量

为了避免IKE数据包的问题击中某些SPD规则，并需要使用尚未建立的SA（可能正在尝试建立此数据包）进行加密加密，则使用SPD处理了带有UDP源端口500的本地发起的数据包。 与本地交付的UDP目标端口500相同的数据包未在传入的策略检查中处理。

##设置过程

要使IPSEC使用IKE-ISAKMP使用自动键合，您将必须配置策略，同行和建议（可选）条目。

IPSEC对时间变化非常敏感。 如果IPSEC隧道的两端不是平等地同步时间（例如，不同的NTP服务器未使用相同的时间戳更新时间），则隧道将断开，并且必须再次建立。

## EAP身份验证方法

| Outer Auth   | Inner Auth                                                                                         |
| ------------ | -------------------------------------------------------------------------------------------------- |
| EAP-GTC      |                                                                                                    |  |
| EAP-MD5      |                                                                                                    |  |
| EAP-MSCHAPv2 |                                                                                                    |  |
| EAP-PEAPv0   | EAP-MSCHAPv2  <br>EAP-GPSK  <br>EAP-GTC  <br>EAP-MD5  <br>EAP-TLS                                  |
| EAP-SIM      |                                                                                                    |
| EAP-TLS      |                                                                                                    |
| EAP-TTLS     | PAP  <br>CHAP  <br>MS-CHAP  <br>MS-CHAPv2  <br>EAP-MSCHAPv2  <br>EAP-GTC  <br>EAP-MD5  <br>EAP-TLS |

**aep-tls** 在Windows上称为“智能卡或其他证书”。

# 身份验证标题（AH）

AH是一项协议，通过添加基于数据报中的值来计算的标头来提供数据报的全部或部分数据验证。 数据报的哪些部分用于计算，并且标头的放置取决于是否使用了隧道或运输模式。

AH标头的存在允许验证消息的完整性，但不会对其进行加密。 因此，AH提供了身份验证，但没有隐私。 另一个协议（ESP）被认为是优越的，它提供了数据隐私以及其自己的身份验证方法。

Routeros支持以下AH的身份验证算法：

-   SHA2 (256, 512)
-   SHA1
-   MD5

## 传输模式

在传输模式下，AH头插入在IP头之后。IP数据和报头用于计算认证值。在传输过程中可能发生变化的IP字段，如TTL和跳数，在身份验证之前被设置为零值。

## 隧道模式

在隧道模式下，原IP报文被封装成一个新的IP报文。所有的原始IP报文都被认证。

# 封装安全负载(ESP)

  

ESP (Encapsulating Security Payload)使用共享密钥加密来提供数据隐私。ESP还支持自己的身份验证方案，就像AH中使用的那样。

ESP封装字段的方式与AH非常不同。它不是只有一个标题，而是将其字段分为三个组件:

- **ESP报头** -出现在加密数据之前，它的位置取决于ESP是在传输模式还是隧道模式下使用。
- **ESP尾包** -放置在加密数据后。它包含用于对齐加密数据的填充。
- **ESP认证数据** -当使用ESP的可选认证特性时，该字段包含一个ICV (Integrity Check Value)，计算方式类似于AH协议的工作方式。

## 传输模式

在传输模式下，ESP头插入到原IP头之后。报文末尾添加ESP拖尾和认证值。在这种模式下，只对IP有效载荷进行加密和认证，对IP报头不进行安全保护。

![](https://help.mikrotik.com/docs/download/attachments/11993097/800px-ESP-transport_wiki.png?version=1&modificationDate=1579172163851&api=v2)

  

## 隧道模式

在隧道模式下，原IP报文被封装在一个新的IP报文中，从而保证了IP负载和IP报头的安全。

![](https://help.mikrotik.com/docs/download/attachments/11993097/ESP-tunnel_wiki.png?version=1&modificationDate=1579172215119&api=v2)

## 加密算法

RouterOS ESP支持多种加密和认证算法。

身份验证:

-   **MD5**
-   **SHA1**
-   **SHA2 (256-bit, 512-bit)**

加密:

- **AES** - 128位、192位、256位密钥AES- cbc、AES- ctr、AES- gcm算法;
- **Blowfish** -自v4.5添加
- Twofish -自v4.5起添加
- **Camellia** - 128位，192位和256位密钥山茶花加密算法自v4.5以来添加
- **DES** - 56位DES- cbc加密算法;
- **3DES** - 168位DES加密算法;

## 硬件加速

硬件加速允许通过使用CPU内部的内置加密引擎来执行更快的加密过程。

提供硬件加速的设备列表 [在这里](https://mikrotik.com/products?filter&s=c&f=%5B%22ipsec%22%5D)


<table class="wrapped relative-table confluenceTable" style="width: 95.6452%;"><colgroup><col style="width: 21.4406%;"><col style="width: 4.56606%;"><col style="width: 5.16163%;"><col style="width: 5.22781%;"><col style="width: 4.83076%;"><col style="width: 4.36753%;"><col style="width: 5.09546%;"><col style="width: 5.22781%;"><col style="width: 4.83076%;"><col style="width: 4.36753%;"><col style="width: 5.09546%;"><col style="width: 5.22781%;"><col style="width: 4.83076%;"><col style="width: 4.36753%;"><col style="width: 5.09546%;"><col style="width: 5.22781%;"><col style="width: 4.83076%;"></colgroup><tbody><tr><th rowspan="2" style="width: 401.0px;" class="confluenceTh">CPU</th><th colspan="4" style="width: 255.0px;" class="confluenceTh">DES and 3DES</th><th colspan="4" style="width: 255.0px;" class="confluenceTh">AES-CBC</th><th colspan="4" style="width: 255.0px;" class="confluenceTh">AES-CTR</th><th colspan="4" style="width: 255.0px;" class="confluenceTh">AES-GCM</th></tr><tr><th style="width: 52.0px;" class="confluenceTh">MD5</th><th style="width: 57.0px;" class="confluenceTh">SHA1</th><th style="width: 73.0px;" class="confluenceTh">SHA256</th><th style="width: 73.0px;" class="confluenceTh">SHA512</th><th style="width: 52.0px;" class="confluenceTh">MD5</th><th style="width: 57.0px;" class="confluenceTh">SHA1</th><th style="width: 73.0px;" class="confluenceTh">SHA256</th><th style="width: 73.0px;" class="confluenceTh">SHA512</th><th style="width: 52.0px;" class="confluenceTh">MD5</th><th style="width: 57.0px;" class="confluenceTh">SHA1</th><th style="width: 73.0px;" class="confluenceTh">SHA256</th><th style="width: 73.0px;" class="confluenceTh">SHA512</th><th style="width: 52.0px;" class="confluenceTh">MD5</th><th style="width: 57.0px;" class="confluenceTh">SHA1</th><th style="width: 73.0px;" class="confluenceTh">SHA256</th><th style="width: 73.0px;" class="confluenceTh">SHA512</th></tr><tr><td style="width: 401.0px;" class="confluenceTd">88F7040</td><td class="highlight-red confluenceTd" data-highlight-colour="red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">AL21400</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">AL32400</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">AL52400</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td></tr><tr><td class="confluenceTd">AL73400</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">IPQ-4018 / IPQ-4019</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes*</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes*</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes*</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes*</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">IPQ-6010</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green">yes</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">IPQ-8064</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes*</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes*</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes*</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes*</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">MT7621A</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 52.0px;" title="Background colour : Yellow">yes****</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes****</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes****</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">P1023NSN5CFB</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes**</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes**</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes**</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes**</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">P202ASSE2KFB</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td></tr><tr><td style="width: 401.0px;" class="confluenceTd"><span class="markedContent"><span>PPC460GT</span></span></td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 52.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 52.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">TLR4 (TILE)</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 52.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 57.0px;" title="Background colour : Green">yes</td><td class="highlight-green confluenceTd" data-highlight-colour="green" style="width: 73.0px;" title="Background colour : Green">yes</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td></tr><tr><td style="width: 401.0px;" class="confluenceTd">x86 (AES-NI)</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 52.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 57.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-red confluenceTd" data-highlight-colour="red" style="width: 73.0px;" title="Background colour : Red">no</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 52.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 52.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 52.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 57.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td><td class="highlight-yellow confluenceTd" data-highlight-colour="yellow" style="width: 73.0px;" title="Background colour : Yellow">yes***</td></tr></tbody></table>

\* 只支持128位和256位密钥大小

\*\* 仅自2016年以来生产，序列号以数字5和7开始

\*\*\* 仅加速AES-CBC和AES-CTR加密，在软件中完成哈希

\*\*\*\* 不支持DES，只支持3DES和AES-CBC

各种加密和哈希算法组合的IPsec吞吐量结果发布在 [microtik产品页面](https://mikrotik.com/product/) 上。

# 策略

策略表用于确定是否应该对数据包应用安全设置。

**属性**

| 属性                                                                     | 说明                                                                                                                                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **action** (_discard \| encrypt \| none_; Default: **encrypt**)          | 指定对匹配策略的报文进行处理。<br>- none不加修改地传递报文。<br>- discard -丢弃报文。<br>- encrypt -应用此策略中指定的转换，它是SA。                                                                                                                                                                                                       |
| **comment** (_string_; Default: )                                        | 政策的简短描述。                                                                                                                                                                                                                                                                                                                           |
| **disabled** (_yes \| no_;Default:**no**)                                | 是否使用策略匹配报文。                                                                                                                                                                                                                                                                                                                     |
| **dst-address** (_IP/IPv6 prefix_;Default:**0.0.0.0/32**)                | 要在报文中匹配的目的地址。适用于隧道模式(tunnel=yes)和模板模式(template=yes)。                                                                                                                                                                                                                                                             |
| **dst-port** (_integer:0..65535 \| any_;Default:**any**)                 | 要在报文中匹配的目的端口。如果设置为任意，所有端口将被匹配。                                                                                                                                                                                                                                                                               |
| **group** (_string_;Default: **Default**)                                | 该模板所分配的策略组名称。                                                                                                                                                                                                                                                                                                                 |
| **ipsec-protocols** (_ah \| esp_;Default:**esp**)                        | 指定要应用于匹配流量的认证头协议和封装安全有效载荷协议的组合。                                                                                                                                                                                                                                                                             |
| **level** (_require \| unique \| use_; Default: **require**)             | 指定在找不到该策略的某些SA时该怎么做：<br>- use - 跳过这个转换，不丢弃数据包，也不从IKE守护进程中获取SA；<br>- require - 丢弃数据包并获取SA；<br>- unique - 丢弃数据包，并获得一个只用于这个特定策略的唯一SA。它用于设置多个客户端可以坐在一个公共IP地址后面（NAT后面的客户端）。                                                          |
| **peer** (_string_; Default: )                                           | 应用策略的对等体名称。                                                                                                                                                                                                                                                                                                                     |
| **proposal** (_string_;Default: **Default**)                             | IKE守护进程发送的安全提议模板名称，用于为该策略建立安全联盟。                                                                                                                                                                                                                                                                              |
| **protocol** (_all \| egp \| ggp\| icmp \| igmp \| ..._;Default:**all**) | IP包协议匹配。                                                                                                                                                                                                                                                                                                                             |
| **src-address** (_ip/ipv6 prefix_;Default:**0.0.0.0/32**)                | 报文中匹配的源地址。适用于隧道模式(tunnel=yes)和模板模式(template=yes)。                                                                                                                                                                                                                                                                   |
| **src-port** (_any \| integer:0..65535_;Default:**any**)                 | 报文中要匹配的源端口。如果设置为任意，所有端口将被匹配。                                                                                                                                                                                                                                                                                   |
| **template** (_yes \| no_; Default: **no**)                              | 创建模板，并将模板分配给指定策略组。<br>模板使用的参数如下:<br>- group -分配给该模板的策略组名称;<br>—src-address, dst-address—请求的子网必须在两个方向上都匹配(例如0.0.0.0/0允许所有);<br>- protocol -协议匹配，如果设置为all，则接受任何协议;<br>- proposal -用于此模板的SA参数;<br>- level -在NAT后的多个客户端设置中需要unique时有用。 |
| **tunnel** (_yes \| no_; Default: **no**)                                | 是否使用隧道模式。                                                                                                                                                                                                                                                                                                                         |

**只读属性**

| 属性                                                  | 说明                                                                 |
| ----------------------------------------------------- | -------------------------------------------------------------------- |
| **active** (_yes\| no_)                               | 当前是否使用此策略。                                                 |
| **default** (_yes\| no_)                              | 是否为默认系统项。                                                   |
| **dynamic** (_yes\| no_)                              | 这是动态添加的还是生成的条目。                                       |
| **invalid** (_yes\| no_)                              | 策略是否无效，可能是由于存在相同src-address和dst-address的重复策略。 |
| **ph2-count** (_integer_)                             | 与策略关联的激活的第二阶段会话数。                                   |
| **ph2-state** (_expired\| no-phase2\| established_)   | 键建立进度指示。                                                     |
| **sa-dst-address** (_ip/ipv6 address_;Default:**::**) | SA目的IP/IPv6地址(对端)。                                            |
| **sa-src-address** (_ip/ipv6 address_;Default:**::**) | SA源IP/IPv6地址(本端)。                                              |

从v6.40开始，策略顺序非常重要。现在，它的工作原理类似于防火墙过滤器，从上到下执行策略(删除优先级参数)。

所有报文都采用隧道方式进行IPIP封装，其新IP头的src-address和dst-address设置为本策略的sa-src-address和sa-dst-address。如果不使用隧道模式(id test使用传输模式)，则只有源地址和目的地址与sa-src-address和sa-dst-address相同的报文才能被此策略处理。传输模式只能用于发源于IPsec对等体(建立安全关联的主机)并以IPsec对等体为目的地的数据包。要加密网络之间(或网络与主机之间)的流量，必须使用隧道模式。

## 统计

此菜单显示各种IPsec统计信息和错误。

**只读属性**

| 属性                                       | 说明                                                                                             |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| **in-errors** (_integer_)                  | 所有与其他计数器不匹配的入站错误。                                                               |
| **in-buffer-errors** (_integer_)           | 没有可用的缓冲区。                                                                               |
| **in-header-errors** (_integer_)           | 报头错误。                                                                                       |
| **in-no-states** (_integer_)               | 没有找到状态，即SA的入站SPI，地址或IPsec协议错误。                                               |
| **in-state-protocol-errors** (_integer_)   | 转换协议特定的错误，例如SA密钥错误或硬件加速器无法处理数据包数量。                               |
| **in-state-mode-errors** (_integer_)       | 转换模式特有的错误。                                                                             |
| **in-state-sequence-errors** (_integer_)   | 序列号超出窗口。                                                                                 |
| **in-state-expired** (_integer_)           | 状态过期。                                                                                       |
| **in-state-mismatches** (_integer_)        | 状态有不匹配选项，如UDP封装类型不匹配。                                                          |
| **in-state-invalid** (_integer_)           | 状态无效。                                                                                       |
| **in-template-mismatches** (_integer_)     | 状态没有匹配模板，例如入站sa是正确的，但SP规则是错误的。可能的原因是sa源地址或sa目的地址不匹配。 |
| **in-no-policies** (_integer_)             | 未找到状态的策略，例如入站sa正确但未找到SP。                                                     |
| **in-policy-blocked** (_integer_)          | 策略丢弃。                                                                                       |
| **in-policy-errors** (_integer_)           | 策略错误。                                                                                       |
| **out-errors** (_integer_)                 | 所有未被其他计数器匹配的出站错误。                                                               |
| **out-bundle-errors** (_integer_)          | 包生成错误。                                                                                     |
| **out-bundle-check-errors** (_integer_)    | 捆绑检查错误。                                                                                   |
| **out-no-states**（_Integer_）             | 无状态。                                                                                         |
| **out-state-protocol-errors**（_Integer_） | 转换协议特殊错误。                                                                               |
| **out-state-mode-errors**（_Integer_）     | 转换模式特殊错误。                                                                               |
| **out-state-sequence-errors**（_integer_） | 序列错误，例如序列号溢出。                                                                       |
| **out-state-expired**（_Integer_）         | 状态已过期                                                                                       |
| **out-policy-blocked**（_Integer_）        | 丢弃策略                                                                                         |
| **out-policy-dead**（_integer_）           | 该策略已死                                                                                       |
| **Out-Policy-Errors**（_integer_）         | 策略错误                                                                                         |

＃建议

Ike Daemons将向某些政策建立SAS的建议信息。

  
**特性**

| 属性                                                                                                                                                                                                                                                                                                     | 说明                                                                             |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **auth-algorithms** (_md5\| null\| sha1 \| sha256 \| sha512_; Default: **sha1**)                                                                                                                                                                                                                         | 允许授权算法。 SHA（安全哈希算法）更强，但较慢。 MD5使用128位键，SHA1-160BIT键。 |
| **comment** (_string_; Default: )                                                                                                                                                                                                                                                                        |                                                                                  |
| **disabled** (_yes \| no_; Default: **no**)                                                                                                                                                                                                                                                              | 是否禁用项目。                                                                   |
| **enc-algorithms** (_null\| des \| 3des \| aes-128-cbc \| aes-128-cbc \| aes-128gcm \| aes-192-cbc \| aes-192-ctr \| aes-192-gcm \| aes-256-cbc \| aes-256-ctr \| aes-256-gcm \| blowfish \| camellia-128 \| camellia-192 \| camellia-256 \| twofish_; Default: **aes-256-cbc,aes-192-cbc,aes-128-cbc**) | 允许用于SAS的算法和密钥长度。                                                    |
| **lifetime** (_time_; Default: **30m**)                                                                                                                                                                                                                                                                  | SA扔出去之前使用SA多长时间。                                                     |
| **name** (_string_; Default: )                                                                                                                                                                                                                                                                           |                                                                                  |
| **pfs-group** (_ec2n155 \| ec2n185\| ecp256 \| ecp384 \| ecp521  \| modp768 \| modp1024 \| modp1536\| modp2048    \| modp3072    \| modp4096    \| modp6144    \| modp8192 \| none_; Default: **modp1024**)                                                                                              | 用于完美转发保密的diffie-Helman组。                                              |

  
**只读属性**

| 属性              | 说明 |
| ----------------- | ---- |
| **default** (_yes | no_) | 是否是一个默认的系统条目。 |

# 组

在这个菜单中，可以创建策略模板使用的额外组。

  
**属性**

| 属性                              | 说明 |
| --------------------------------- | ---- |
| **name** (_string_; Default: )    |      |
| **comment** (_string_; Default: ) |      |

# 对等体

对等体配置用于在IKE守护进程之间建立连接。这种连接将被用于协商密钥和SA的算法。交换模式是对等体之间唯一的标识符，这意味着只要使用不同的交换模式，就可以有多个具有相同远程地址的对等体配置。

**属性**

| 属性                                                                        | 说明                                                                                                                                                                                                                              |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_IP/IPv6 Prefix_; Default: **0.0.0.0/0**)                      | 如果远程对等体的地址与这个前缀相匹配，那么对等体的配置就会在认证和建立 **阶段** 中使用。如果几个对等体的地址与几个配置项相匹配，将使用最具体的一个（即具有最大净掩码的那个）。                                                    |
| **comment** (_string_; Default: )                                           | 对等体的简短描述。                                                                                                                                                                                                                |
| **disabled** (_yes \| no_; Default: **no**)                                 | 对等体是否用于匹配远程对等体的前缀。                                                                                                                                                                                              |
| **exchange-mode** (_aggressive \| base \| main \| ike2_; Default: **main**) | 根据RFC2408的不同ISAKMP第一阶段交换模式，**main** 模式放宽了rfc2409第5.4节，允许在主模式下进行预共享密钥认证。ike2模式启用Ikev2 RFC7296。IKEv2提案检查、兼容性选项、生命值、dpd-maximum-failures、nat-traversal等参数都会被忽略。 |
| **local-address** (_IP/IPv6 Address_; Default: )                            | 路由器的本地地址，第1阶段应以其为界。                                                                                                                                                                                             |
| **name** (_string_; Default: )                                              |                                                                                                                                                                                                                                   |
| **passive** (_yes\| no_; Default: **no**)                                   | 当启用被动模式时，将等待远程对等体启动IKE连接。启用被动模式也表示对等体是xauth响应者，禁用被动模式--xauth发起者。当被动模式被禁用时，如果在第一阶段配置或创建了策略，对等体不仅会尝试建立第一阶段，还会自动建立第二阶段。         |
| **port** (_integer:0...65535_; Default: **500**)                            | 如果远程对等体使用非默认端口，则使用通信端口（当路由器为发起者时）连接到远程对等体。                                                                                                                                              |
| **profile** (_string_; default: **default**)                                | IKE协商时使用的配置文件模板名称。                                                                                                                                                                                                 |
| **send-initial-contact** (_yes \| no_; Default: **yes**)                    | 指定是否发送 "初始接触 "IKE数据包或等待远程端，该数据包应触发删除当前源地址的旧对等协议。通常情况下，在公路战士设置中，客户端是发起者，这个参数应该设置为否。如果ikev1启用了modecfg或xauth，则不发送初始联系。                    |

**只读属性**

| 属性                        | 说明                                                     |
| --------------------------- | -------------------------------------------------------- |
| **dynamic** (_yes \| no_)   | 是否是一个由不同服务（如L2TP）动态添加的条目。           |
| **responder** (_yes \| no_) | 对等体是否只充当响应者（监听传入的请求），而不启动连接。 |

# Identities

Identities are configuration parameters that are specific to the remote peer. The main purpose of identity is to handle authentication and verify the peer's integrity.

**属性**

| 属性                                                                                                                                                                 | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **auth-method** (_digital-signature \| eap \| eap-radius \| pre-shared-key \| pre-shared-key-xauth \| rsa-key \| rsa-signature-hybrid_; Default: **pre-shared-key**) | 认证方法： <br>- digital-signature - 使用一对RSA证书进行认证；<br>- eap - IKEv2 EAP认证的发起者（网络掩码为/32的对端）。必须与eap-methods一起使用；<br>- eap-radius - 响应者的IKEv2 EAP RADIUS穿透式认证（RFC 3579）。在这种情况下，需要一个服务器证书。如果没有指定服务器证书，那么只有支持EAP-only（RFC 5998）的客户端才能连接。请注意，EAP方法应该与EAP-only兼容；<br>- pre-shared-key - 通过对等体之间共享的密码（预共享秘密）字符串进行认证（不推荐，因为预共享密钥可能受到离线攻击）；<br>- rsa-key - 使用钥匙菜单中导入的RSA钥匙进行验证。仅在IKEv1中支持；<br>- pre-shared-key-xauth - 通过对等人之间共享的密码（预共享秘密）字符串+XAuth用户名和密码进行认证。只在IKEv1中支持；<br>- rsa-signature-hybrid - 通过发起者的XAuth进行响应者证书认证。只在IKEv1中支持。 |
| **certificate** (_string_; Default: )                                                                                                                                | 系统证书中列出的证书名称（签署数据包；该证书必须有私钥）。如果使用数字签名认证方法（auth-method=digital-signature）或EAP（auth-method=eap），则适用。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **comment** (_string_; Default: )                                                                                                                                    | 身份的简短描述。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **disabled** (_yes \| no_; Default: **no**)                                                                                                                          | 身份是否用于匹配远程对等体。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **eap-methods** (_eap-mschapv2 \| eap-peap \| eap-tls \| eap-ttls_; Default: **eap-tls**)                                                                            | 所有EAP方法都需要整个证书链，包括中间和根CA证书，都要在系统/证书菜单中出现。另外，必须指定用户名和密码（如果认证服务器要求）。可以指定多种EAP方法，并按指定的顺序使用。目前支持的EAP方法：<br>- eap-mschapv2；<br>- eap-peap - 也被称为PEAPv0/EAP-MSCHAPv2；<br>- eap-tls - 需要在证书参数下指定的额外客户证书；<br>- eap-ttls。                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **generate-policy** (_no \| port-override \| port-strict_; Default: **no**)                                                                                          | 允许该对等体为不存在的策略建立SA。这种策略在SA的有效期内动态地创建。自动策略允许，例如，创建IPsec安全的L2TP隧道，或任何其他设置，其中远程对等体的IP地址在配置时不知道。<br>- no - 不生成策略；<br>- port-override - 产生策略并强制策略使用任何端口（旧行为）；<br>- port-strict - 使用对等体建议的端口，这些端口应该与对等体的策略相匹配。                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **key** (_string_; Default: )                                                                                                                                        | 密钥菜单中的私钥名称。如果使用RSA密钥认证方法（auth-method=rsa-key），则适用。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **match-by** (_remote-id \| certificate_; Default: **remote-id**)                                                                                                    | 定义用于对等体身份验证的逻辑。<br>- remote-id - 根据 remote-id 设置来验证对等体的 ID。<br>- certificate 根据远程证书设置中指定的内容验证对等体的证书。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **mode-config** (_none \| request-only \| string_; Default: **none**)                                                                                                | 模式配置菜单中的配置参数名称。当参数设置后，模式配置被启用。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **my-id** (_auto \| address \| fqdn \| user-fqdn \| key-id_; Default: **auto**)                                                                                      | 在启动器上，它控制向响应者发送什么ID_i。在应答方，这控制了发送给发起方的ID_r。在IKEv2中，响应方也希望从发起方收到的ID_r中包含这个ID。<br>- auto - 试图自动使用正确的ID： IP用于预共享密钥，SAN（如果没有的话）用于基于证书的连接；<br>- address - IP地址作为ID使用；<br>- dn - ASN.1 X.500区分名称的二进制区分编码规则（DER）编码；<br>- fqdn - 完全合格的域名；<br>- key-id - 使用指定的密钥ID作为身份；<br>- user fqdn - 指定一个完全限定的用户名字符串，例如，"user@domain.com"。                                                                                                                                                                                                                                                                                        |
| **notrack-chain** (_string_; Default: )                                                                                                                              | 将符合IPsec策略的IP/Firewall/Raw规则添加到指定链中。与generate-policy一起使用。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **password** (_string_; Default: )                                                                                                                                   | XAuth或EAP密码。如果使用XAuth认证方法的预共享密钥(auth-method=pre-shared-key-xauth)或EAP(auth-method=eap)，则适用。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **peer** (_string_; Default: )                                                                                                                                       | 适用于该身份的对等体的名称。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **policy-template-group** (_none \| string_; Default: **default**)                                                                                                   | 如果启用了生成-policy，流量选择器将根据同一组的模板进行检查。如果没有一个模板匹配，第二阶段的SA将不会被建立。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **remote-certificate** (_string_; Default: )                                                                                                                         | 用于验证远程端（验证数据包；不需要私钥）的证书名称（列在System/Certificates中）。如果没有指定remote-certificate，那么将使用从远程对等体收到的证书，并与证书菜单中的CA核对。适当的CA必须在证书库中导入。如果指定了远程证书和match-by=certificate，那么只有特定的客户证书会被匹配。如果使用数字签名认证方法（auth-method=digital-signature），则适用。                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **remote-id** (_auto \| fqdn \| user-fqdn \| key-id \| ignore_; Default: **auto**)                                                                                   | 这个参数控制期望从远程对等体获得什么ID值。请注意，除忽略外，所有类型都会用收到的证书验证远程对等体的ID。如果对等体发送证书名称作为它的ID，它将与证书核对，否则ID将与Subject Alt. 名称。<br>- auto - 接受所有ID；<br>- address - 使用 IP 地址作为 ID；<br>- dn - ASN.1 X.500区分名称的二进制区分编码规则（DER）编码；<br>- fqdn - 完全合格的域名。仅在IKEv2中支持；<br>- user fqdn - 一个完全限定的用户名字符串，例如 "user@domain.com"。仅在IKEv2中支持；<br>- key-id - 该身份的特定密钥ID。仅在IKEv2中支持；<br>- ignore - 不用证书来验证收到的ID（危险）。                                                                                                                                                                                                                |
| **remote-key** (_string_; Default: )                                                                                                                                 | 密钥菜单中的公钥名称。如果使用RSA密钥认证方法（auth-method=rsa-key），则适用。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **secret** (_string_; Default: )                                                                                                                                     | 秘密字符串。如果它以'0x'开头，则被解析为十六进制值。如果使用预共享密钥认证方法(auth-method=pre-shared-key and auth-method=pre-shared-key-xauth)则适用。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **username** (_string_; Default: )                                                                                                                                   | XAuth或EAP用户名。如果使用XAuth认证方法的预共享密钥(auth-method=pre-shared-key-xauth)或EAP(auth-method=eap)，则适用。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

  
**只读属性**

| 属性              | 说明 |
| ----------------- | ---- |
| **dynamic** (_yes | no_) | 这是否是由不同的服务（如L2TP）动态添加的条目。 |

## 配置文件

配置文件定义了一组参数，将用于第一阶段的IKE协商。这些参数可能与其他对等体的配置相同。

**属性**

| 属性                                                                                                                                                 | 说明                                                                                                                                                                                                                                                     |
| ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **dh-group** (_modp768 \| modp1024\| ec2n155\| ec2n185\| modp1536 \| modp2048                                                                        | modp3072 \| modp4096 \| modp6144\| modp8192\| ecp256 \| ecp384 \| ecp521_; Default: **modp1024,modp2048**)                                                                                                                                               | Diffie-Hellman组（密码强度）。 |
| **dpd-interval** (_time\| disable-dpd_; Default: **2m**)                                                                                             | 死亡对等检测间隔。 如果禁用DPD，则不会使用死亡对等检测。                                                                                                                                                                                                 |
| **dpd-maximum-failures** (_integer: 1..100_; Default: **5**)                                                                                         | 最大的失败计数，直到对等体被认为死亡。 如果启用了DPD，则适用。                                                                                                                                                                                           |
| **enc-algorithm** (_3des \| aes-128 \| aes-192 \| aes-256 \| blowfish \| camellia-128 \| camellia-192 \| camellia-256 \| des_; Default: **aes-128**) | 对等体将使用的加密算法列表。                                                                                                                                                                                                                             |
| **hash-algorithm** (_md5\| sha1\| sha256\| sha512_; Default: **sha1**)                                                                               | 哈希算法。SHA（安全哈希算法）更强大，但速度较慢。MD5使用128位密钥，sha1-160位密钥。                                                                                                                                                                      |
| **lifebytes** (_Integer: 0..4294967295_; Default: **0**)                                                                                             | 阶段1的生命值仅作为管理值，添加到提案中。在远程对等体需要特定的生命字节值来建立第一阶段时使用。                                                                                                                                                          |
| **lifetime** (_time_; Default: **1d**)                                                                                                               | 阶段1寿命：指定SA有效多长时间。                                                                                                                                                                                                                          |
| **name** (_string_; Default: )                                                                                                                       |                                                                                                                                                                                                                                                          |
| **nat-traversal** (_yes\| no_; Default: **yes**)                                                                                                     | 使用Linux NAT-T机制来解决IPsec与IPsec对等体之间的NAT路由器的不兼容性。这只能用于ESP协议（AH在设计上不被支持，因为它签署了完整的数据包，包括IP头，而IP头被NAT改变，使AH签名无效）。该方法将IPsec ESP流量封装成UDP流，以克服一些小问题，使ESP与NAT不兼容。 |
| **proposal-check** (_claim \| exact\| obey \| strict_; Default: **obey**)                                                                            | Phase 2 寿命检查逻辑：<br>- claim  - 在提议的和配置的寿命中选择最短的，并将其通知发起者<br>- exact -要求寿命相同<br>- obey  - 接受发起者发送的任何信息<br>- strict -如果提议的寿命比默认值长，则拒绝该提议，否则接受提议的寿命                           |

# 活跃的对等体

这个菜单提供了目前已建立第一阶段连接的远程对等体的各种统计数据。

  
**只读属性**

| 属性                                    | 说明                                                                                      |
| --------------------------------------- | ----------------------------------------------------------------------------------------- |
| **dynamic-address** (_ip/ipv6 address_) | 通过模式配置动态分配的IP地址                                                              |  |  |  |  |  |  |  |  |  |  |  |  | 。 |
| **last-seen** (_time_)                  | 自该对等体最后一次收到信息后的持续时间。                                                  |
| **local-address** (_ip/ipv6 address_)   | 该对等体使用的路由器上的本地地址。                                                        |
| **natt-peer** (_yes\| no_)              | 此对等体是否使用NAT-T。                                                                   |
| **ph2-total** (_integer_)               | 活动的IPsec安全关联的总量。                                                               |
| **remote-address** (_ip/ipv6 address_)  | 远程对方的ip/ipv6地址。                                                                   |
| **responder** (_yes\| no_)              | 该连接是否由远程对等体发起。                                                              |
| **rx-bytes** (_integer_)                | 从这个对等体收到的总字节数。                                                              |
| **rx-packets** (_integer_)              | 从这个对等体收到的数据包的总量。                                                          |
| **side** (_initiator\| responder_)      | 显示哪一方发起了Phase1协商。                                                              |
| **state** (_string_)                    | 与对等体进行Phase1协商的状态。例如，当phase1和phase2进行协商时，它将显示状态为 "已建立"。 |
| **tx-bytes** (_integer_)                | 传输给该对等体的总字节数。                                                                |
| **tx-packets** (_integer_)              | 传输给该对等体的数据包总量。                                                              |
| **uptime** (_time_)                     | 对等体处于建立状态的时间。                                                                |

  
**命令**

| 属性                    | 说明                           |
| ----------------------- | ------------------------------ |
| **kill-connections** () | 手动断开所有远程对等体的连接。 |

# 模式配置

ISAKMP和IKEv2的配置属性在这个菜单中进行配置。

  
**属性**

| 属性                                                     | 说明                                                                                                  |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **address** (_none \| string_; Default: )                | 启动器的单个IP地址，而不是指定整个地址池。                                                            |
| **address-pool** (_none                                  | string_; Default: )                                                                                   | 地址池的名称，如果启用模式配置，响应者将尝试从该地址池分配地址。 |
| **address-prefix-length** (_integer [1..32]_; Default: ) | 从地址池分配地址的前缀长度（netmask）。                                                               |
| **comment** (_string_; Default: )                        |                                                                                                       |
| **name** (_string_; Default: )                           |                                                                                                       |
| **responder** (_yes\| no_; Default: **no**)              | 指定配置是否将作为发起者（客户）或响应者（服务器）工作。发起者将向响应者请求模式-配置参数。           |
| **split-include** (_list of IP prefix_; Default: )       | CIDR格式的子网列表，用于隧道。子网将使用CISCO UNITY扩展发送给对等体，远程对等体将创建特定的动态策略。 |
| **src-address-list** (_address list_; Default: )         | 指定一个地址列表将生成动态源NAT规则。这个参数只在responder=no时可用。一个有NAT的roadWarrior客户端     |
| **static-dns** (_list of IP_; Default: )                 | 手动指定DNS服务器的IP地址，发送给客户端。                                                             |
| **system-dns** (_yes \| no_; Default: )                  | 当这个选项被启用时，DNS地址将从 `/ip dns` 中获取。                                                    |

  
**只读属性**

| 属性                      | 说明                       |
| ------------------------- | -------------------------- |
| **default** (_yes \| no_) | 是否是一个默认的系统条目。 |

并非所有的IKE实现都支持split-include选项所提供的多个分割网络。

如果RouterOS客户端是发起者，它将始终发送CISCO UNITY扩展，而RouterOS只支持该扩展的split-include。

不可能同时使用 system-dns 和 static-dns。

# 已安装的SA

这个菜单提供了关于已安装的安全关联的信息，包括密钥。

  
**只读属性**

| 属性                                 | 说明                                                                                                      |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| **AH** (_yes \| no_)                 | 此SA是否使用AH协议。                                                                                      |
| **ESP** (_yes \| no_)                | 此SA是否使用ESP协议。                                                                                     |
| **add-lifetime** (_time/time_)       | 为SA添加的寿命，格式为：<br>- soft - IKE将尝试建立新的SA的时间段；<br>- hard - 在一段时间后，SA将被删除。 |
| **addtime** (_time_)                 | 添加该SA的日期和时间。                                                                                    |
| **auth-algorithm** (_md5             | null                                                                                                      | sha1    | ..._) | 目前使用的认证算法。 |
| **auth-key** (_string_)              | 使用的认证密钥。                                                                                          |
| **current-bytes** (_64-bit integer_) | 这个SA所看到的字节数。                                                                                    |
| **dst-address** (_IP_)               | 此SA的目标地址。                                                                                          |
| **enc-algorithm** (_des              | 3des                                                                                                      | aes-cbc | ..._) | 目前使用的加密算法。 |
| **enc-key** (_string_)               | 使用的加密密钥。                                                                                          |
| **enc-key-size** (_number_)          | 使用的加密密钥长度。                                                                                      |
| **expires-in** (_yes \| no_)         | 距离重启密钥的时间。                                                                                      |
| **hw-aead** (_yes \| no_)            | 这个SA是否是硬件加速的。                                                                                  |
| **replay** (_integer_)               | 重放窗口的大小，以字节为单位。                                                                            |
| **spi** (_string_)                   | 安全参数索引识别标签                                                                                      |
| **src-address** (_IP_)               | 此SA的源地址。                                                                                            |
| **state** (_string_)                 | 显示SA的当前状态（"成熟"、"濒死 "等）。                                                                   |

  
**命令**

| 属性         | 说明                           |
| ------------ | ------------------------------ |
| **flush** () | 手动删除所有已安装的安全关联。 |

# 密钥

该菜单列出了所有导入的公钥和私钥，可用于同行认证。菜单中有几个命令来处理钥匙。

  
**属性**

| 属性                           | 说明 |
| ------------------------------ | ---- |
| **name** (_string_; Default: ) |      |

  
**只读的属性**

| 属性                                  | 说明                  |
| ------------------------------------- | --------------------- |
| **key-size** (_1024 \| 2048 \| 4096_) | 此密钥的大小。        |
| **private-key** (_yes \| no_)         | 这是否是一个私钥。    |
| **rsa** (_yes \| no_)                 | 这是否是一个RSA密钥。 |

  
**命令**

| 属性                                  | 说明                                                                       |
| ------------------------------------- | -------------------------------------------------------------------------- |
| **export-pub-key** (_file-name; key_) | 从现有的一个私钥中导出公钥到文件。                                         |
| **generate-key** (_key-size; name_)   | 生成一个私钥。接收两个参数，新生成的密钥的名称和密钥大小1024、2048和4096。 |
| **导入** (_file-name; name_)          | 从文件中导入密钥。                                                         |

# 设置
  

| 属性                                          | 说明                                                                                                                                                    |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **accounting** (_yes\| no_; Default: )        | 是否向RADIUS服务器发送RADIUS审计请求。如果使用EAP Radius(auth-method=eap-radius)或预共享密钥与XAuth认证方法(auth-method=pre-shared-key-xauth)，则适用。 |
| **interim-update** (_time_; Default: )        | 每次连续的RADIUS审计临时更新之间的间隔。必须启用审计。                                                                                                  |
| **xauth-use-radius** (_yes \| no_; Default: ) | 是否对XAuth用户使用Radius客户端。                                                                                                                       |

# 应用指南

## RoadWarrior客户端与NAT

考虑设置如下图所示。RouterOS作为一个RoadWarrior客户端连接到办公室，允许访问其内部资源。

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ipsec-road-warrior.jpg?version=1&modificationDate=1612795265983&api=v2)

一个隧道被建立，一个本地模式配置的IP地址被接收，一组动态策略被生成。

```shell
[admin@mikrotik] > ip ipsec policy print
Flags: T - template, X - disabled, D - dynamic, I - invalid, A - active, * - default
0 T * group=default src-address=::/0 dst-address=::/0 protocol=all proposal=default template=yes
 
1 DA src-address=192.168.77.254/32 src-port=any dst-address=10.5.8.0/24 dst-port=any protocol=all
action=encrypt level=unique ipsec-protocols=esp tunnel=yes sa-src-address=10.155.107.8
sa-dst-address=10.155.107.9 proposal=default ph2-count=1
 
2 DA src-address=192.168.77.254/32 src-port=any dst-address=192.168.55.0/24 dst-port=any protocol=all
action=encrypt level=unique ipsec-protocols=esp tunnel=yes sa-src-address=10.155.107.8
sa-dst-address=10.155.107.9 proposal=default ph2-count=1
```

目前，只有源地址为192.168.77.254/32的数据包才符合IPsec策略。为了使本地网络能够到达远程子网，有必要将本地主机的源地址改为动态分配的模式配置IP地址。可以动态地生成源NAT规则。这可以通过创建一个新的地址列表来实现，该地址列表包含了NAT规则应该应用的所有本地网络。在这个例子中，它是192.168.88.0/24。

`/ip firewall address-list add address=192.168.88.0/24 list=local-RW`。

通过在mode-config启动器配置下指定地址列表，将动态生成一组源NAT规则。

`/ip ipsec mode-config set [ find name="require-only" ] src-address-list=local-RW`。

当IPsec隧道建立后，可以看到为每个网络动态创建的源NAT规则。现在192.168.88.0/24的每台主机都能访问Office的内部资源。

```shell
[admin@mikrotik] > ip firewall nat print
Flags: X - disabled, I - invalid, D - dynamic
0 D ;;; ipsec mode-config
chain=srcnat action=src-nat to-addresses=192.168.77.254 dst-address=192.168.55.0/24 src-address-list=local-RW
 
1 D ;;; ipsec mode-config
chain=srcnat action=src-nat to-addresses=192.168.77.254 dst-address=10.5.8.0/24 src-address-list=local-RW
```

## 只允许IPsec封装的流量

在某些情况下，出于安全考虑，如果传入传出的数据包没有加密，想放弃特定网络的访问。例如，如果有L2TP/IPsec设置，希望放弃非加密的L2TP连接尝试。

有几种方法可以实现：

- 使用防火墙中的IPsec策略匹配器；
- 使用通用的IPsec策略，动作设置为 **丢弃** 和较低的优先级（可用于生成动态策略的Road Warrior设置中）；
- 通过在mangle中设置DSCP或优先级，并在解封装后在防火墙中匹配相同的值。

### IPsec策略匹配器

设置一个IPsec策略匹配器，接受所有与任何IPsec策略相匹配的数据包，并放弃其余的：

```shell
add chain=input comment="ipsec policy matcher" in-interface=WAN ipsec-policy=in,ipsec
add action=drop chain=input comment="drop all" in-interface=WAN log=yes
```

IPsec政策匹配器需要两个参数 **方向、策略** 。使用传入方向和IPsec策略。IPsec策略选项允许在解封装后检查数据包，因此，例如，如果想只允许来自特定源地址的GRE封装的数据包，而放弃其余的，可以设置以下规则：

```shell
add chain=input comment="ipsec policy matcher" in-interface=WAN ipsec-policy=in,ipsec protocol=gre src=address=192.168.33.1
add action=drop chain=input comment="drop all" in-interface=WAN log=yes
```

对于L2TP规则集将是：

```shell
add chain=input comment="ipsec policy matcher" in-interface=WAN ipsec-policy=in,ipsec protocol=udp dst-port=1701
add action=drop chain=input protocol=udp dst-port=1701 comment="drop l2tp" in-interface=WAN log=yes
```

### 使用通用 IPsec 策略

这个方法的诀窍是添加一个默认的策略，并加上一个动作drop。假设在一个公共的1.1.1.1地址上运行一个L2TP/IPsec服务器，想丢弃所有非加密的L2TP：

```shell
/ip ipsec policy
add src-address=1.1.1.1 dst-address=0.0.0.0/0 sa-src-address=1.1.1.1 protocol=udp src-port=1701 tunnel=yes action=discard
```

现在，路由器将丢弃任何L2TP未加密的传入流量，但在L2TP/IPsec连接成功后，将创建动态策略，其优先级高于默认的静态规则，符合该动态规则的数据包可以被转发。

策略的顺序很重要! 为了使其发挥作用，确保静态丢弃策略在动态策略的下面。如果有必要，将它移到策略模板的下面。

```shell
[admin@rack2_10g1] /ip ipsec policy> print
Flags: T - template, X - disabled, D - dynamic, I - inactive, * - default
0 T * group=default src-address=::/0 dst-address=::/0 protocol=all
proposal=default template=yes
 
1 D src-address=1.1.1.1/32 src-port=1701 dst-address=10.5.130.71/32
dst-port=any protocol=udp action=encrypt level=require
ipsec-protocols=esp tunnel=no sa-src-address=1.1.1.1
sa-dst-address=10.5.130.71
 
2 src-address=1.1.1.1/32 src-port=1701 dst-address=0.0.0.0/0
dst-port=any protocol=udp action=discard level=unique
ipsec-protocols=esp tunnel=yes sa-src-address=1.1.1.1
sa-dst-address=0.0.0.0 proposal=default manual-sa=none
```

## 手动指定对等体配置下的本地地址参数

### 使用不同的路由表

IPsec和RouterOS中的其他服务一样，使用主要的路由表，而不管Peer配置中使用的是什么本地地址参数。有必要对IKE和IPSec流量都应用路由标记。

考虑一下下面的例子。有两条默认路由--一条在主路由表，另一条在路由表 "备份 "中。有必要在IPsec站点到站点的隧道中使用备份链接。

```shell
[admin@pair_r1] > /ip route print detail
Flags: X - disabled, A - active, D - dynamic, C - connect, S - static, r - rip, b - bgp, o - ospf, m - mme, B - blackhole, U - unreachable, P - prohibit
0 A S dst-address=0.0.0.0/0 gateway=10.155.107.1 gateway-status=10.155.107.1 reachable via ether1 distance=1 scope=30 target-scope=10 routing-mark=backup
 
1 A S dst-address=0.0.0.0/0 gateway=172.22.2.115 gateway-status=172.22.2.115 reachable via ether2 distance=1 scope=30 target-scope=10
 
2 ADC dst-address=10.155.107.0/25 pref-src=10.155.107.8 gateway=ether1 gateway-status=ether1 reachable distance=0 scope=10
 
3 ADC dst-address=172.22.2.0/24 pref-src=172.22.2.114 gateway=ether2 gateway-status=ether2 reachable distance=0 scope=10
 
4 ADC dst-address=192.168.1.0/24 pref-src=192.168.1.1 gateway=bridge-local gateway-status=ether2 reachable distance=0 scope=10
 
[admin@pair_r1] > /ip firewall nat print
Flags: X - disabled, I - invalid, D - dynamic
0 chain=srcnat action=masquerade out-interface=ether1 log=no log-prefix=""
 
1 chain=srcnat action=masquerade out-interface=ether2 log=no log-prefix=""
```

使用备份链路的源地址以及IPsec隧道流量的NAT绕过规则，创建IPsec对等和策略配置。

```shell
/ip ipsec peer
add address=10.155.130.136/32 local-address=10.155.107.8 secret=test
/ip ipsec policy
add sa-src-address=10.155.107.8 src-address=192.168.1.0/24 dst-address=172.16.0.0/24 sa-dst-address=10.155.130.136 tunnel=yes
/ip firewall nat
add action=accept chain=srcnat src-address=192.168.1.0/24 dst-address=172.16.0.0/24 place-before=0
```

在日志中看到 "phase1 negotiation failed due to time up "错误。这是因为IPsec试图用一个不正确的源地址通过主路由表到达远程对等体。有必要使用Mangle标记UDP/500、UDP/4500和ipsec-esp数据包：

```shell
/ip firewall mangle
add action=mark-connection chain=output connection-mark=no-mark dst-address=10.155.130.136 dst-port=500,4500 new-connection-mark=ipsec passthrough=yes protocol=udp
add action=mark-connection chain=output connection-mark=no-mark dst-address=10.155.130.136 new-connection-mark=ipsec passthrough=yes protocol=ipsec-esp
add action=mark-routing chain=output connection-mark=ipsec new-routing-mark=backup passthrough=no
```

### 使用同一路由表的多个 IP 地址

考虑下面的例子。公共接口上有多个来自同一子网的IP地址。在out-interface上配置了Masquerade规则。有必要明确使用其中一个IP地址。

```shell
[admin@pair_r1] > /ip address print
Flags: X - disabled, I - invalid, D - dynamic
# ADDRESS NETWORK INTERFACE
0 192.168.1.1/24 192.168.1.0 bridge-local
1 172.22.2.1/24 172.22.2.0 ether1
2 172.22.2.2/24 172.22.2.0 ether1
3 172.22.2.3/24 172.22.2.0 ether1
 
[admin@pair_r1] > /ip route print
Flags: X - disabled, A - active, D - dynamic, C - connect, S - static, r - rip, b - bgp, o - ospf, m - mme, B - blackhole, U - unreachable, P - prohibit
# DST-ADDRESS PREF-SRC GATEWAY DISTANCE
1 A S 0.0.0.0/0 172.22.2.115 1
3 ADC 172.22.2.0/24 172.22.2.1 ether1 0
4 ADC 192.168.1.0/24 192.168.1.1 bridge-local 0
 
[admin@pair_r1] /ip firewall nat> print
Flags: X - disabled, I - invalid, D - dynamic
0 chain=srcnat action=masquerade out-interface=ether1 log=no log-prefix=""
```

使用其中一个公共IP地址创建IPsec对等体和策略配置。

```shell
/ip ipsec peer
add address=10.155.130.136/32 local-address=172.22.2.3 secret=test
/ip ipsec policy
add sa-src-address=172.22.2.3 src-address=192.168.1.0/24 dst-address=172.16.0.0/24 sa-dst-address=10.155.130.136 tunnel=yes
/ip firewall nat
add action=accept chain=srcnat src-address=192.168.1.0/24 dst-address=172.16.0.0/24 place-before=0
```

目前，第一阶段的连接使用了与指定的不同的源地址，而且日志中显示了 "phase1 negotiation failed due to time up "的错误。这是因为masquerade正在改变连接的源地址以匹配连接路由的pref-src地址。解决的办法是排除来自公共IP地址的连接被伪装。

```shell
/ip firewall nat
add action=accept chain=srcnat protocol=udp src-port=500,4500 place-before=0
```

# 应用实例

## 站点到站点的IPsec（IKEv1）隧道

考虑如下图所示的设置。两个远程办公室路由器连接到互联网，办公室工作站在NAT后面。每个办公室都有自己的本地子网，办公室1为10.1.202.0/24，办公室2为10.1.101.0/24。这两个远程办公室都需要通过安全隧道进入路由器后面的本地网络。

  

![](https://help.mikrotik.com/docs/download/attachments/11993097/Site-to-site-ipsec-example.png?version=1&modificationDate=1615380469161&api=v2)

### site1配置

首先，使用更强或更弱的加密参数创建一个新的第1阶段配置文件和第2阶段建议条目，以满足你的需要。建议为每个菜单创建单独的条目，以便在将来有必要调整任何设置时，它们对每个对等体是唯一的。这些参数必须在网站之间匹配，否则将无法建立连接。

```shell
/ip ipsec profile
add dh-group=modp2048 enc-algorithm=aes-128 name=ike1-site2
/ip ipsec proposal
add enc-algorithms=aes-128-cbc name=ike1-site2 pfs-group=modp2048
```

继续配置一个对等体。指定远程路由器的地址。这个地址应该可以通过UDP/500和UDP/4500端口到达，所以要确保对路由器的防火墙采取适当的措施。为这个对等体以及新创建的配置文件指定名称。

`/ip ipsec peer
add address=192.168.80.1/32 name=ike1-site2 profile=ike1-site2`

下一步是创建一个身份。对于一个基本的预共享密钥安全隧道，除了一个强密码和这个身份所适用的对等体，没有什么可设置的。

`/ip ipsec identity
add peer=ike1-site2 secret=thisisnotasecurepsk`

如果安全问题很重要，考虑使用IKEv2和不同的认证方法。

最后，创建一个策略，控制网络/主机之间的流量应该被加密。

```shell
/ip ipsec policy
add src-address=10.1.202.0/24 src-port=any dst-address=10.1.101.0/24 dst-port=any tunnel=yes action=encrypt proposal=ike1-site2 peer=ike1-site2
```

### site2的配置

site2的配置与site1几乎相同，都是适当的IP地址配置。首先创建一个新的第1阶段配置文件和第2阶段建议条目：

```shell
/ip ipsec profile
add dh-group=modp2048 enc-algorithm=aes-128 name=ike1-site1
/ip ipsec proposal
add enc-algorithms=aes-128-cbc name=ike1-site1 pfs-group=modp2048
```

接下来是同行和身份：

```shell
/ip ipsec peer
add address=192.168.90.1/32 name=ike1-site1 profile=ike1-site1
/ip ipsec identity
add peer=ike1-site1 secret=thisisnotasecurepsk
```

完成后，创建一个策略：

```shell
/ip ipsec policy
add src-address=10.1.101.0/24 src-port=any dst-address=10.1.202.0/24 dst-port=any tunnel=yes action=encrypt proposal=ike1-site1 peer=ike1-site1
```

在这一点上，应该建立隧道，并在两个路由器上创建两个IPsec安全关联：

```shell
/ip ipsec
active-peers print
installed-sa print
```

### 绕过NAT和Fasttrack

在这一点上，如果试图通过IPsec隧道发送流量，它将无法工作，数据包将丢失。这是因为两个路由器都有NAT规则（伪装），在数据包被加密之前，正在改变源地址。路由器无法对数据包进行加密，因为源地址与策略配置中指定的地址不匹配。更多信息请参见IPsec数据包流程示例。

为了解决这个问题，需要设置IP/Firewall/NAT旁路规则。

office1的路由器：

```shell
/ip firewall nat
add chain=srcnat action=accept place-before=0 src-address=10.1.202.0/24 dst-address=10.1.101.0/24
```

office2的路由器：

```shell
/ip firewall nat
add chain=srcnat action=accept place-before=0 src-address=10.1.101.0/24 dst-address=10.1.202.0/24
```

如果以前在添加NAT旁路规则之前试图建立一个IP连接，必须从现有的连接中清除连接表或重新启动两个路由器。

非常重要的是，旁路规则要放在所有其他NAT规则的顶部。

另一个问题是，如果启用了IP/Fasttrack，数据包会绕过IPsec策略。所以需要在FastTrack之前添加接受规则。

```shell
/ip firewall filter
add chain=forward action=accept place-before=1
src-address=10.1.101.0/24 dst-address=10.1.202.0/24 connection-state=established,related
add chain=forward action=accept place-before=1
src-address=10.1.202.0/24 dst-address=10.1.101.0/24 connection-state=established,related
```

然而，如果有相当数量的隧道和每个隧道上的大量流量，这可能会给路由器的CPU增加很大的负荷。

解决方案是使用IP/Firewall/Raw来绕过连接跟踪，这样就不需要上面列出的过滤规则，并将CPU上的负载减少约30%。

```shell
/ip firewall raw
add action=notrack chain=prerouting src-address=10.1.101.0/24 dst-address=10.1.202.0/24
add action=notrack chain=prerouting src-address=10.1.202.0/24 dst-address=10.1.101.0/24
```

## 使用DNS通过IPsec（IKEv2）建立站点到站点的GRE隧道

这个例子解释了当一个或两个站点没有静态IP地址时，如何在两个RouterOS设备之间建立一个安全和加密的GRE隧道。在实现这一配置之前，有必要为其中一台将作为响应者（服务器）的设备分配一个DNS名称。为了简单起见，使用RouterOS内置的DDNS服务IP/Cloud。

![](https://help.mikrotik.com/docs/download/attachments/11993097/Site-to-site-gre-over-ipsec-example.png?version=1&modificationDate=1617275261923&api=v2)

### site1（服务器）配置

这一边将监听传入的连接并作为响应者。将使用模式配置为第二个站点提供一个IP地址，但首先要创建一个回环（空白）网桥，并为其分配一个IP地址，以后将用于GRE隧道的建立。

```shell
/interface bridge
add name=loopback
/ip address
add address=192.168.99.1 interface=loopback
```

继续进行IPsec配置，首先创建一个新的第1阶段配置文件和第2阶段建议条目，使用更强或更弱的加密参数来满足你的需要。注意，这个配置实例将监听所有传入的IKEv2请求，这意味着配置文件配置将在所有其他配置（如RoadWarrior）之间共享。

```shell
/ip ipsec profile
add dh-group=ecp256,modp2048,modp1024 enc-algorithm=aes-256,aes-192,aes-128 name=ike2
/ip ipsec proposal
add auth-algorithms=null enc-algorithms=aes-128-gcm name=ike2-gre pfs-group=none
```

下一步，创建一个新的模式配置条目，responder=yes。这将为另一个站点提供一个IP配置，以及用于策略生成的主机（回环地址）。

```shell
/ip ipsec mode-config
add address=192.168.99.2 address-prefix-length=32 name=ike2-gre split-include=192.168.99.1/32 system-dns=no
```

建议创建一个新的策略组，将此配置与任何现有或未来的IPsec配置分开。

`/ip ipsec policy group
add name=ike2-gre`

现在是时候建立一个新的策略模板，以匹配远程对等体的新动态地址和回环地址。

```shell
/ip ipsec policy
add dst-address=192.168.99.2/32 group=ike2-gre proposal=ike2-gre src-address=192.168.99.1/32 template=yes
```

下一步是创建一个将监听所有IKEv2请求的对等体配置。如果已经有这样一个条目，你可以跳过这一步。

`/ip ipsec peer
add exchange-mode=ike2 name=ike2 passive=yes profile=ike2`

最后，设置一个身份，通过预共享密钥认证和特定的秘密来匹配我们的远程同伴。

```shell
/ip ipsec identity
add generate-policy=port-strict mode-config=ike2-gre peer=ike2 policy-template-group=ike2-gre secret=test
```

服务器端现在已经配置好了，并且正在监听所有IKEv2请求。请确保防火墙没有阻挡UDP/4500端口。

最后一步是创建GRE接口本身。这也可以在以后从客户端建立IPsec连接时进行。

```shell
/interface gre
add local-address=192.168.99.1 name=gre-tunnel1 remote-address=192.168.99.2
```

配置IP地址并通过GRE接口路由到远程网络。

```shell
/ip address
add address=172.16.1.1/30 interface=gre-tunnel1
/ip route
add dst-network=10.1.202.0/24 gateway=172.16.1.2
```

### site2（客户端）配置

与服务器配置类似，首先创建一个新的第一阶段配置文件和第二阶段建议配置。由于这个站点将是发起者，我们可以使用更具体的配置文件配置来控制使用哪些确切的加密参数，只要确保它们与服务器端配置的参数重叠即可。

```shell
/ip ipsec profile
add dh-group=ecp256 enc-algorithm=aes-256 name=ike2-gre
/ip ipsec proposal
add auth-algorithms=null enc-algorithms=aes-128-gcm name=ike2-gre pfs-group=none
```

下一步，创建一个新的模式配置条目，其中responder=no。这将确保对等体从服务器请求IP和分离网络配置。

`/ip ipsec mode-config
add name=ike2-gre responder=no`

建议创建一个新的策略组，将此配置与任何现有或未来的IPsec配置分开。

`/ip ipsec 策略组
add name=ike2-gre`

在客户端也要创建一个新的策略模板。

```shell
/ip ipsec policy
add dst-address=192.168.99.1/32 group=ike2-gre proposal=ike2-gre src-address=192.168.99.2/32 template=yes
```

转到对等体配置。现在可以在地址参数下指定服务器的DNS名称。很明显，你也可以使用一个IP地址。

```shell
/ip ipsec peer
add address=n.mynetname.net exchange-mode=ike2 name=p1.ez profile=ike2-gre
```

最后，为我们新创建的对等体创建一个身份。

```shell
/ip ipsec身份
add generate-policy=port-strict mode-config=ike2-gre peer=p1.ez policy-template-group=ike2-gre secret=test
```


如果一切操作正常，应该有一个新的动态策略出现。

```shell
/ip ipsec policy print
Flags: T - template, X - disabled, D - dynamic, I - invalid, A - active, * - default
0 T * group=default src-address=::/0 dst-address=::/0 protocol=all proposal=default template=yes
 
1 T group=ike2-gre src-address=192.168.99.2/32 dst-address=192.168.99.1/32 protocol=all proposal=ike2-gre template=yes
 
2 DA src-address=192.168.99.2/32 src-port=any dst-address=192.168.99.1/32 dst-port=any protocol=all action=encrypt level=unique ipsec-protocols=esp
tunnel=yes sa-src-address=192.168.90.1 sa-dst-address=(current IP of n.mynetname.net) proposal=ike2-gre ph2-count=1
```

现在两个站点之间建立了一条安全隧道，它将对192.168.99.2 <=> 192.168.99.1地址之间的所有流量进行加密。可以用这些地址来创建一个GRE隧道。

`/interface gre
add local-address=192.168.99.2 name=gre-tunnel1 remote-address=192.168.99.1`

配置IP地址并通过GRE接口路由到远程网络。

```shell
/ip address
add address=172.16.1.2/30 interface=gre-tunnel1
/ip route
add dst-network=10.1.101.0/24 gateway=172.16.1.1
```

## 使用IKEv2与RSA认证的公路勇士设置

这个例子解释了如何在一个连接到互联网的设备（公路勇士客户端）和一个运行RouterOS作为服务器的设备之间建立安全的IPsec连接。

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ipsec-road-warrior.png?version=1&modificationDate=1615382411689&api=v2)

### RouterOS服务器配置

在配置IPsec之前，需要设置证书。可以使用单独的证书管理机构进行证书管理，然而在这个例子中，自签名的证书是在RouterOS系统/证书菜单中生成的。要将各种设备连接到服务器上，应该满足一些证书要求：

- 通用名称应包含服务器的IP或DNS名称；
- SAN（主体替代名称）应包含服务器的IP或DNS；
- EKU（扩展密钥使用）tls-server和tls-client是必需的。

考虑到上述所有要求，生成CA和服务器证书：

```shell
/certificate
add common-name=ca name=ca
sign ca ca-crl-host=2.2.2.2
add common-name=2.2.2.2 subject-alt-name=IP:2.2.2.2 key-usage=tls-server name=server1
sign server1 ca=ca
```

现在已经在路由器上创建了有效的证书，添加一个新的第1阶段配置文件和第2阶段建议条目，并使用pfs-group=none：

```shell
/ip ipsec profile
add name=ike2
/ip ipsec proposal
add name=ike2 pfs-group=none
```

模式配置用于从IP/池中分配地址：

```shell
/ip pool
add name=ike2-pool ranges=192.168.77.2-192.168.77.254
/ip ipsec mode-config
add address-pool=ike2-pool address-prefix-length=32 name=ike2-conf
```

由于策略模板必须被调整为只允许特定的网络策略，建议创建一个单独的策略组和模板。

```shell
/ip ipsec policy group
add name=ike2-policies
/ip ipsec policy
add dst-address=192.168.77.0/24 group=ike2-policies proposal=ike2 src-address=0.0.0.0/0 template=yes
```

创建一个新的IPsec对等体条目，监听所有传入的IKEv2请求。

`/ip ipsec peer
add exchange-mode=ike2 name=ike2 passive=yes profile=ike2`

#### 身份配置

身份菜单允许匹配特定的远程对等体并为每个对等体分配不同的配置。首先，创建一个默认的身份，它将接受所有的对等体，但将用其证书验证对等体的身份。

```shell
/ip ipsec identity
add auth-method=digital-signature certificate=server1 generate-policy=port-strict mode-config=ike2-conf peer=ike2 policy-template-group=ike2-policies
```

如果对等体的ID(ID_i)与其发送的证书不匹配，身份查询将失败。见身份部分的remote-id。

例如，想为用户 "A "分配一个不同的模式配置，他使用证书 "rw-client1 "来向服务器验证自己。首先确保一个新的模式配置已经创建并准备好应用于特定的用户。

```shell
/ip ipsec mode-config
add address=192.168.66.2 address-prefix-length=32 name=usr_A split-include=192.168.55.0/24 system-dns=no
```

通过使用match-by=certificate参数和用remote-certificate指定他的证书，可以对用户 "A "应用这种配置。

```shell
/ip ipsec identity
add auth-method=digital-signature certificate=server1 generate-policy=port-strict match-by=certificate mode-config=usr_A peer=ike2 policy-template-group=ike2-policies remote-certificate=rw-client1
```

####（可选） 分离式隧道配置

分离式隧道是一种允许公路战士客户端只访问特定的安全网络，同时根据其内部路由表发送其余流量的方法（而不是通过隧道发送所有流量）。要配置分离式隧道，需要对模式配置参数进行修改。

例如，允许公路勇士客户只访问10.5.8.0/24网络。

`/ip ipsec mode-conf
set [find name="rw-conf"] split-include=10.5.8.0/24`

也可以发送一个特定的DNS服务器供客户使用。默认情况下，使用的是system-dns=yes，它发送的是IP/DNS中路由器本身配置的DNS服务器。可以通过使用static-dns参数强制客户端使用不同的DNS服务器。

`/ip ipsec mode-conf
set [find name="rw-conf"] system-dns=no static-dns=10.5.8.1`

虽然可以调整IPsec策略模板，只允许公路勇士客户端生成策略到由split-include参数配置的网络，但这可能导致与不同供应商实现的兼容性问题（见已知限制）。与其调整策略模板，不如允许访问IP/Firewall/Filter中的安全网络，而丢弃其他的。

```shell
/ip firewall filter
add action=drop chain=forward src-address=192.168.77.0/24 dst-address=!10.5.8.0/24
```

分离式网络不是一种安全措施。客户端（发起人）仍然可以请求一个不同的第二阶段流量选择器。

#### 生成客户证书

要为客户生成一个新的证书，并用以前创建的CA进行签名。

```shell
/certificate
add common-name=rw-client1 name=rw-client1 key-usage=tls-client
sign rw-client1 ca=ca
```

**PKCS12格式** 被大多数客户端实现所接受，因此在导出证书时，确保指定PKCS12。

`/certificate
export-certificate rw-client1 export-passphrase=1234567890 type=pkcs12`

一个名为 _cert_export_rw-client1.p12_ 的文件现在位于路由器的系统/文件部分。这个文件应该被安全地传送到客户的设备上。

通常，PKCS12捆绑文件还包含一个CA证书，但有些供应商可能没有安装这个CA，所以必须使用PEM格式单独导出一个自签名的CA证书。

`/certificate
export-certificate ca type=pem`

一个名为 _cert_export_ca.crt_ 的文件现在位于路由器的系统文件部分。这个文件也应该被安全地传送到客户的设备上。

**PEM** 是另一种用于不支持PKCS12的客户端软件的证书格式。其原理基本相同。

```shell
/certificate
export-certificate ca
export-certificate rw-client1 export-passphrase=1234567890
```

现在有三个文件位于路由器的文件部分： _cert_export_ca.crt_、_cert_export_rw-client1.crt_ 和 _cert_export_rw-client1.key_，它们应该被安全地传输到客户端设备。

#### 已知的限制

以下是流行的客户端软件IKEv2实现的已知限制列表。

- Windows将始终忽略通过split-include收到的网络，并请求目的地为0.0.0.0/0（TSr）的策略。当IPsec-SA生成时，Windows请求DHCP选项249，RouterOS将自动用配置好的split-include网络来响应。

- 苹果macOS和iOS都只接受第一个分割包含的网络。

- 苹果macOS和iOS只有在使用0.0.0.0/0分割包含时，才会使用系统-dns和静态-dns参数中的DNS服务器。

- 虽然有些实现可以为第二阶段利用不同的PFS组，但建议在建议下使用pfs-group=none以避免任何兼容性问题。

### RouterOS客户端配置

在RouterOS中导入一个PKCS12格式的证书。

`/certificate import file-name=cert_export_RouterOS_client.p12 passphrase=1234567890`

现在在证书菜单中应该有自签的CA证书和客户证书。找出客户证书的名称。

`/certificate print`

**cert_export_RouterOS_client.p12_0** 是客户证书。

建议创建单独的第1阶段配置文件和第2阶段建议配置，以免干扰任何现有的IPsec配置。

```shell
/ip ipsec profile
add name=ike2-rw
/ip ipsec proposal
add name=ike2-rw pfs-group=none
```

虽然可以使用默认的策略模板来生成策略，但最好是创建一个新的策略组和模板，将该配置与任何其他IPsec配置分开。

```shell
/ip ipsec policy group
add name=ike2-rw
/ip ipsec policy
add group=ike2-rw proposal=ike2-rw template=yes
```

创建一个新的模式配置条目，responder=no，从服务器请求配置参数。

`/ip ipsec mode-config
add name=ike2-rw responder=no`

最后，创建对等和身份配置。

```shell
/ip ipsec peer
add address=2.2.2.2/32 exchange-mode=ike2 name=ike2-rw-client
/ip ipsec identity
add auth-method=digital-signature certificate=cert_export_RouterOS_client.p12_0 generate-policy=port-strict mode-config=ike2-rw peer=ike2-rw-client policy-template-group=ike2-rw
```

验证连接是否成功建立。

```shell
/ip ipsec
active-peers print
installed-sa print
```

#### 启用动态源NAT规则生成

如果我们看一下生成的动态策略，我们会发现只有具有特定（由模式配置接收的）源地址的流量才会通过隧道发送。但是，在大多数情况下，路由器需要通过隧道路由一个特定的设备或网络。在这种情况下，可以使用源NAT来改变数据包的源地址以匹配模式配置地址。由于模式配置地址是动态的，所以不可能创建一个静态的源NAT规则。在RouterOS中，可以为模式配置客户端生成动态源NAT规则。

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ipsec-road-warrior-client.png?version=1&modificationDate=1617263807501&api=v2)

例如，在路由器后有一个本地网络192.168.88.0/24，希望这个网络的所有流量都能通过隧道发送。首先必须建立一个新的IP/防火墙/地址列表，其中包括本地网络

`/ip firewall address-list
add address=192.168.88.0/24 list=local`

当它完成后，我们可以将新创建的IP/防火墙/地址列表分配给模式配置。

`/ip ipsec mode-config
set [ find name=ike2-rw ] src-address-list=local`

验证正确的源NAT规则是在隧道建立时动态生成的。


```shell
[admin@MikroTik] > /ip firewall nat print
Flags: X - disabled, I - invalid, D - dynamic
0 D ;;; ipsec mode-config
chain=srcnat action=src-nat to-addresses=192.168.77.254 src-address-list=local dst-address-list=!local
```

确保动态模式的配置地址不是本地网络的一部分。

### Windows客户端配置

在Windows计算机上打开PKCS12格式的证书文件。按照说明安装该证书。确保选择本地机器存储位置。

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ike2v2_cert_win.png?version=1&modificationDate=1617264637750&api=v2) 

现在可以进入网络和互联网设置->VPN，并添加一个新的配置。填入连接名称、服务器名称或地址参数。在VPN类型下选择IKEv2。完成后，有必要选择 "使用机器证书"。这可以在网络和共享中心通过点击VPN连接的属性菜单来完成。该设置位于安全标签下。

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ike2v2_conf_win.png?version=1&modificationDate=1617264693224&api=v2)

目前，Windows 10兼容以下第1阶段（配置文件）和第2阶段（建议）建议集：

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

### macOS客户端配置

在macOS计算机上打开PKCS12格式的证书文件，将证书安装到 "系统 "钥匙串中。由于该CA证书是自签的，因此有必要手动将其标记为受信任。在 "系统 "标签下找到证书macOS Keychain Access应用程序，并将其标记为始终信任。

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ikev2_cert_macos.png?version=1&modificationDate=1617265736527&api=v2)

现在你可以进入系统偏好 -> 网络，点击 "+"按钮添加新的配置。选择接口： VPN，VPN类型： IKEv2并命名你的连接。远程ID必须设置为等于服务器证书的通用名称或subjAltName。本地ID可以留空。在认证设置下选择无，并选择客户端证书。现在你可以测试连接性了。

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ikev2_conf_macos.png?version=1&modificationDate=1617265766455&api=v2)

目前，macOS兼容以下第一阶段（配置文件）和第二阶段（建议）的建议集：

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

### iOS客户端配置

通常PKCS12捆绑包还包含一个CA证书，但iOS并不安装这个CA，所以必须使用PEM格式单独安装一个自签名的CA证书。在iOS设备上打开这些文件，按照说明安装两个证书。有必要在iOS设备上把自签CA证书标记为受信任。这可以在设置->通用->关于->证书信任设置菜单中完成。完成后，在 "设置"->"常规"->"配置文件 "菜单下检查两个证书是否被标记为 "已验证"。

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ikev2_cert_ios.png?version=1&modificationDate=1617265950259&api=v2)

现在你可以进入设置->通用->VPN菜单，添加新的配置。远程ID必须设置为等于服务器证书的通用名称或subjAltName。本地ID可以留空。

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ikev2_conf_ios.png?version=1&modificationDate=1617265989863&api=v2)

目前，iOS与以下第1阶段（配置文件）和第2阶段（建议）的建议集兼容：

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

如果通过WiFi连接到VPN，iOS设备可以进入睡眠模式并断开与网络的连接。

### Android（strongSwan）客户端配置

目前，安卓系统中没有IKEv2的原生支持，不过，可以使用Google Play商店中的strongSwan，它将IKEv2带到了安卓。strongSwan接受PKCS12格式的证书，因此在strongSwan中设置VPN连接之前，请确保将PKCS12捆绑下载到你的安卓设备上。完成后，在strongSwan中创建一个新的VPN配置文件，输入服务器IP，并选择 "IKEv2证书 "作为VPN类型。在选择用户证书时，按 "安装"，并按照证书提取程序指定PKCS12捆绑包。保存配置文件，并在VPN配置文件上按下测试连接。

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ikev2_conf_android.png?version=1&modificationDate=1617266889478&api=v2)

通过勾选 "显示高级设置 "复选框，可以在 strongSwan 中指定自定义加密设置。目前，strongSwan 默认与以下第一阶段（配置文件）和第二阶段（建议）建议集兼容：

 Phase 1       

| Hash Algorithm | Encryption Algorithm | DH Group |
| -------------- | -------------------- | -------- |
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

  

Phase 2        

| Hash Algorithm | Encryption Algorithm | PFS Group |
| -------------- | -------------------- | --------- |
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

### Linux（strongSwan）客户端配置

下载 PKCS12 证书包并将其移至 /etc/ipsec.d/private 目录。

在 /etc/ipsec.secrets 文件中添加私钥的导出口令，其中 "strongSwan_client.p12" 是文件名，"1234567890" 是口令。

`: P12 strongSwan_client.p12 "1234567890"`

在/etc/ipsec.conf文件中添加一个新连接

```shell
conn "ikev2"
keyexchange=ikev2
ike=aes128-sha1-modp2048
esp=aes128-sha1
leftsourceip=%modeconfig
leftcert=strongSwan_client.p12
leftfirewall=yes
right=2.2.2.2
rightid="CN=2.2.2.2"
rightsubnet=0.0.0.0/0
auto=add
```

现在可以重启（或启动）ipsec守护进程并初始化连接了

```shell
$ ipsec restart
$ ipsec up ikev2
```

## 道路勇士设置使用IKEv2，由用户管理器处理EAP-MSCHAPv2认证(RouterOS v7)  

这个例子解释了如何在连接到互联网的设备（公路勇士客户端）和运行RouterOS作为IKEv2服务器和用户管理器的设备之间建立一个安全的IPsec连接。可以在网络中的单独设备上运行用户管理器，但是在这个例子中，用户管理器和IKEv2服务器将被配置在同一个设备上（办公室）。 

![](https://help.mikrotik.com/docs/download/attachments/11993097/Ipsec-road-warrior.png?version=1&modificationDate=1615382411689&api=v2)

### RouterOS服务器配置

#### 要求

为了使这个设置工作，对路由器有几个先决条件：

1.  路由器的IP地址应该有一个有效的公共DNS记录-可以使用IP云来实现这一点。
2.  路由器应该可以通过互联网的TCP/80端口到达 - 如果服务器在NAT后面，应该配置端口转发。
3.  路由器上应安装用户管理器包。

#### 生成Let's Encrypt证书

在EAP-MSCHAPv2认证过程中，必须进行TLS握手，这意味着服务器必须有一个可以被客户端验证的证书。为了简化这一步骤，将使用Let's Encrypt证书，它可以被大多数操作系统验证而不需要用户的任何干预。要生成证书，只需在证书菜单下启用SSL证书。默认情况下，该命令使用IP Cloud提供的动态DNS记录，但也可以指定一个自定义的DNS名称。请注意，DNS记录应指向路由器。

`/certificate enable-ssl-certificate`

如果证书生成成功，在证书菜单下可以看到安装的Let's Encrypt证书。

`/certificate print detail where name~"letsencrypt"`

#### 配置用户管理器

首先，允许接收来自localhost（路由器本身）的RADIUS请求：

`/user-manager router
add address=127.0.0.1 comment=localhost name=local shared-secret=test`

启用用户管理器，并指定Let's Encrypt证书（将证书名称替换为安装在你设备上的那个），该证书将用于验证用户。

`/user-manager
set certificate="letsencrypt_2021-04-09T07:10:55Z" enabled=yes`

最后添加用户和他们的证书，客户将使用这些证书来验证服务器。

`/user-manager user
add name=user1 password=password`

#### 配置RADIUS客户端

为了让路由器使用RADIUS服务器进行用户认证，需要添加一个新的RADIUS客户端，该客户端拥有与我们在用户管理器上已经配置的共享秘密。

`/radius
add address=127.0.0.1 secret=test service=ipsec`

#### IPsec（IKEv2）服务器配置

添加一个新的第1阶段配置文件和第2阶段建议条目，pfs-group=none：

```shell
/ip ipsec profile
add name=ike2
/ip ipsec proposal
add name=ike2 pfs-group=none
```

模式配置用于从IP/池中分配地址。

```shell
/ip pool
add name=ike2-pool ranges=192.168.77.2-192.168.77.254
/ip ipsec mode-config
add address-pool=ike2-pool address-prefix-length=32 name=ike2-conf
```

由于策略模板必须调整为只允许特定的网络策略，因此建议创建一个单独的策略组和模板。

```shell
/ip ipsec policy group
add name=ike2-policies
/ip ipsec policy
add dst-address=192.168.77.0/24 group=ike2-policies proposal=ike2 src-address=0.0.0.0/0 template=yes
```

创建一个新的IPsec对等体条目，它将监听所有传入的IKEv2请求。

`/ip ipsec peer
add exchange-mode=ike2 name=ike2 passive=yes profile=ike2`

最后，创建一个新的IPsec身份条目，它将与所有试图用EAP认证的客户相匹配。注意，必须指定生成的Let's Encrypt证书。

```shell
/ip ipsec identity
add auth-method=eap-radius certificate="letsencrypt_2021-04-09T07:10:55Z" generate-policy=port-strict mode-config=ike2-conf peer=ike2 \
policy-template-group=ike2-policies
```

####（可选） 分离式隧道配置

分离式隧道是一种允许公路战士客户端只访问特定的安全网络，同时根据其内部路由表发送其余流量的方法（而不是通过隧道发送所有流量）。要配置分离式隧道，需要对模式配置参数进行修改。

例如，允许公路战士客户只访问10.5.8.0/24网络。

`/ip ipsec mode-conf
set [find name="rw-conf"] split-include=10.5.8.0/24`

也可以发送一个特定的DNS服务器供客户使用。默认情况下，使用的是system-dns=yes，它发送的是IP/DNS中路由器本身配置的DNS服务器。可以通过使用static-dns参数强制客户端使用不同的DNS服务器。

`/ip ipsec mode-conf
set [find name="rw-conf"] system-dns=no static-dns=10.5.8.1`

  

分离式网络不是一种安全措施。客户端（发起者）仍然可以请求一个不同的第二阶段流量选择器。

####（可选）为用户分配静态IP地址

可以通过使用RADIUS Framed-IP-Address属性给任何用户分配静态IP地址。

`/user-manager user
set [find name="user1"] attributes=Framed-IP-Address:192.168.77.100 shared-users=1`

为了避免任何冲突，静态IP地址应该从其他用户的IP池中排除，同时，对于特定的用户，共享用户应该设置为1。

#### （可选）账户配置

为了跟踪每个用户的正常运行时间、下载和上传统计数据，可以使用RADIUS账户。默认情况下，RADIUS账户已经为IPsec启用，但建议配置临时更新定时器，定期向RADIUS服务器发送统计信息。如果路由器要处理大量的同步会话，建议增加更新定时器，以避免增加CPU的使用。

`/ip ipsec settings
set interim-update=1m`

## 基本L2TP/IPsec设置

这个例子演示了如何在RouterOS上轻松设置L2TP/IPsec服务器，用于公路战士连接（适用于Windows、Android、iOS、macOS和其他厂商的L2TP/IPsec实现）。

### RouterOS服务器配置

第一步是启用L2TP服务器：

`/interface l2tp-server server
set enabled=yes use-ipsec=required ipsec-secret=mySecret default-profile=default`

us-ipsec被设置为 **required**，以确保只接受IPsec封装的L2TP连接。

现在，它所做的是启用一个L2TP服务器，并创建一个具有指定秘密的动态IPsec对等体。

```shell
[admin@MikroTik] /ip ipsec peer> print
0 D address=0.0.0.0/0 local-address=0.0.0.0 passive=yes port=500
auth-method=pre-shared-key secret="123" generate-policy=port-strict
exchange-mode=main-l2tp send-initial-contact=yes nat-traversal=yes
hash-algorithm=sha1 enc-algorithm=3des,aes-128,aes-192,aes-256
dh-group=modp1024 lifetime=1d dpd-interval=2m dpd-maximum-failures=5
```

如果存在静态IPsec对等体配置，必须小心。

下一步是创建一个VPN池并添加一些用户。

```shell
/ip pool add name=vpn-pool range=192.168.99.2-192.168.99.100
 
/ppp profile
set default local-address=192.168.99.1 remote-address=vpn-pool
 
/ppp secret
add name=user1 password=123
add name=user2 password=234
```

现在，路由器已经准备好接受L2TP/IPsec客户端连接。

### RouterOS客户端配置

要使RouterOS作为L2TP/IPsec客户端工作，就像添加一个新的L2TP客户端一样简单。

```shell
/interface l2tp-client
add connect-to=1.1.1.1 disabled=no ipsec-secret=mySecret name=l2tp-out1 \
password=123 use-ipsec=yes user=user1
```

它将自动创建动态IPsec对等体和策略配置。

## 故障排除常见问题

**第1阶段未能获得有效的建议**

```shell
[admin@MikroTik] /log> print
(..)
17:12:32 ipsec,error no suitable proposal found.
17:12:32 ipsec,error 10.5.107.112 failed to get valid proposal.
17:12:32 ipsec,error 10.5.107.112 failed to pre-process ph1 packet (side: 1, status 1).
17:12:32 ipsec,error 10.5.107.112 phase1 negotiation failed.
(..)
```

对等体无法协商加密参数，导致连接中断。为了解决这个问题，启用IPSec调试日志，找出远程对等体提出的参数，并相应调整配置。

`[admin@MikroTik] /system logging> add topics=ipsec,!debug`

```shell
[admin@MikroTik] /log> print
(..)
17:21:08 ipsec rejected hashtype: DB(prop#1:trns#1):Peer(prop#1:trns#1) = MD5:SHA
17:21:08 ipsec rejected enctype: DB(prop#1:trns#2):Peer(prop#1:trns#1) = 3DES-CBC:AES-CBC
17:21:08 ipsec rejected hashtype: DB(prop#1:trns#2):Peer(prop#1:trns#1) = MD5:SHA
17:21:08 ipsec rejected enctype: DB(prop#1:trns#1):Peer(prop#1:trns#2) = AES-CBC:3DES-CBC
17:21:08 ipsec rejected hashtype: DB(prop#1:trns#1):Peer(prop#1:trns#2) = MD5:SHA
17:21:08 ipsec rejected hashtype: DB(prop#1:trns#2):Peer(prop#1:trns#2) = MD5:SHA
17:21:08 ipsec,error no suitable proposal found.
17:21:08 ipsec,error 10.5.107.112 failed to get valid proposal.
17:21:08 ipsec,error 10.5.107.112 failed to pre-process ph1 packet (side: 1, status 1).
17:21:08 ipsec,error 10.5.107.112 phase1 negotiation failed.
(..)
```

在这个例子中，远端要求使用SHA1作为哈希算法，但本地路由器上配置的是MD5。列符号（:）之前的设置是在本地端配置的，列符号（:）之后的参数是在远程端配置的。

**phase1的协商由于超时而失败，这是什么意思？**

对等体之间存在通信问题。可能的原因包括 - 错误配置的第1阶段IP地址；防火墙阻止了UDP端口500和4500；对等体之间的NAT没有正确翻译IPsec协商数据包。当本地地址参数使用不当时，也会出现这个错误信息。更多信息请见这里。

**随机丢包或通过隧道的连接非常慢，启用数据包嗅探器/torch可以解决这个问题？**

问题是，在封装之前，数据包被发送到Fasttrack/FastPath，从而绕过了IPsec策略检查。解决方案是将需要封装/解封装的流量排除在Fasttrack之外，请看这里的配置例子。

**如何启用ike2?**

对于基本配置来说，启用ike2是非常简单的，只要把对等体设置中的交换模式改为ike2即可。

**致命的NO-PROPOSAL-CHOSEN通知信息？**

远程对等体发送通知说它不能接受提议的算法，要找到问题的确切原因，请查看远程对等体的调试日志或配置，并确认客户和服务器都有相同的算法集。

**我只能在一个方向上ping？**

在这种情况下，一个典型的问题是严格的防火墙，防火墙规则只允许在一个方向创建新的连接。解决方案是重新检查防火墙规则，或者明确接受所有应该被封装/解封装的流量。

**我可以只允许加密的流量吗？**

是的，可以，请看 "只允许IPsec封装的流量 "的例子。

**我在StrongSwan上启用IKEv2 REAUTH，得到的错误是-发起人没有按照要求重新认证**

RouterOS不支持rfc4478，必须在StrongSwan上禁用reauth。