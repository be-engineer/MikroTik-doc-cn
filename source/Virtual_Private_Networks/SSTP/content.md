# 概述

SSTP (Secure Socket Tunneling Protocol)是一种通过TLS通道传输PPP隧道的协议。在TCP端口443上使用TLS允许SSTP通过几乎所有的防火墙和代理服务器。

# 介绍

看看SSTP的连接机制:
  

![](https://help.mikrotik.com/docs/download/attachments/2031645/Sstp-how-works.png?version=2&modificationDate=1615377176687&api=v2)

1. 从客户端到服务器建立TCP连接(默认端口443);
2. SSL验证服务器证书。如果证书有效，则建立连接，否则将拒绝连接。(但请参见下文注释);
3. 客户端在HTTPS会话中发送SSTP控制报文，建立双方的SSTP状态机;
4. 基于SSTP的PPP协商。客户端向服务器端进行认证，并在SSTP接口绑定IP地址;

SSTP隧道已经建立，可以进行报文封装;

从v5.0beta2开始，SSTP不需要证书就可以操作，并且可以使用任何可用的身份验证类型。这个功能将只在两个microtik路由器之间工作，因为它不符合微软的标准。否则，要建立安全隧道 **mschap** 身份验证和来自同一链的客户端/服务器证书应该使用。

# 证书

为了建立一个安全的SSTP隧道，需要使用证书。在服务器上，身份验证仅由username和password完成，但在客户端上，服务器使用服务器证书进行身份验证。它也被客户端用来加密绑定SSL和PPP认证，这意味着客户端通过SSTP连接发送一个特殊的值给服务器，这个值来自于PPP认证和服务器证书过程中产生的密钥数据，这允许服务器检查两个通道是否安全。

如果SSTP客户端在Windows PC上，那么在使用自签名证书时建立安全SSTP隧道的唯一方法是在SSTP服务器上导入“server”证书，并在Windows PC上在 [受信任的根](https://technet.microsoft.com/en-us/library/dd458982.aspx) 中添加CA证书。

如果您的服务器证书是由Windows已经知道的CA颁发的，那么Windows客户端将无需向受信任的根导入任何额外的证书即可工作。

如果证书被SSTP使用，RSA密钥长度必须至少为472位。较短的密钥被认为是安全威胁。

  

在RouterOS客户端上也可以进行类似的配置，导入CA证书并启用verify-server-certificate选项。在这种情况下，中间人攻击是不可能的。

在两个microtik路由器之间，也可以通过根本不使用证书来建立不安全的隧道。在这种情况下，通过SSTP隧道的数据使用匿名DH，很容易实现中间人攻击。此场景不兼容Windows客户端。

还可以通过使用客户端证书添加额外的授权来创建安全的SSTP隧道。配置要求如下:

- 服务器端和客户端证书
- 在服务器端和客户端启用验证选项

这种情况对于Windows客户机也是不可能的，因为没有办法在Windows上设置客户机证书。

证书错误消息

当SSL握手失败时，您将看到以下证书错误之一:

- **证书尚未生效** - notBefore证书日期在当前时间之后;
- **证书已过期** -证书有效期在当前时间之前;
- **无效证书用途** -所提供的证书不能用于指定的用途;
- **自己签名的证书链** -证书链可以使用不可信的证书建立，但无法在本地找到根
- **无法在本地获取颁发者证书** - CA证书未在本地导入;
- **cserver的IP地址与证书不匹配** -启用了服务器地址验证，但证书中提供的地址与服务器地址不匹配;

# 快速示例

![](https://help.mikrotik.com/docs/download/attachments/2031645/sstp-setup.jpg?version=1&modificationDate=1571825575193&api=v2)

## SSTP客户端

在下面的配置示例中，e将创建一个不使用证书的简单SSTP客户端:

```shell
[admin@MikroTik > interface sstp-client add connect-to=192.168.62.2 disabled=no name=sstp-out1 password=StrongPass profile=default-encryption user=MT-User
[admin@MikroTik > interface sstp-client print
Flags: X - disabled; R - running
 0  R name="sstp-out1" max-mtu=1500 max-mru=1500 mrru=disabled connect-to=192.168.62.2:443
      http-proxy=0.0.0.0:443 certificate=none verify-server-certificate=no
      verify-server-address-from-certificate=yes user="MT-User" password="StrongPass"
      profile=default-encryption keepalive-timeout=60 add-default-route=no dial-on-demand=no
      authentication=pap,chap,mschap1,mschap2 pfs=no tls-version=any
```

## SSTP服务器

为特定用户配置PPP密码，然后简单地启用SSTP服务器:

```shell
[admin@MikroTik] > ppp secret add local-address=10.0.0.1 name=MT-User password=StrongPass remote-address=10.0.0.5 service=sstp
[admin@MikroTik] > interface sstp-server server set default-profile=default-encryption enabled=yes
[admin@MikroTik] > interface sstp-server server print
                    enabled: yes
                       port: 443
                    max-mtu: 1500
                    max-mru: 1500
                       mrru: disabled
          keepalive-timeout: 60
            default-profile: default-encryption
             authentication: pap,chap,mschap1,mschap2
                certificate: none
  verify-client-certificate: no
                        pfs: no
                tls-version: any
```