# 企业无线安全与用户管理器

User Manager version 5(适用于RouterOS v7)支持通过EAP (Extensible authentication Protocol)协议对用户进行认证。

本指南将解释将User Manager v5配置为microtik无线接入点的身份验证服务器所需的步骤，并为用户提供PEAP和EAP-TLS身份验证方法。

本指南假设在网络地址10.0.0.10上运行User Manager的独立设备和2个接入点-一个在10.0.0.11，另一个在10.0.0.12

# 安装用户管理器

User Manager v5可以在 [最新版本的RouterOS v7](https://mikrotik.com/download) 的“Extra packages”存档中找到。

下载相应CPU架构的归档文件，解压缩它，将User Manager包上传到路由器并重新启动它。

# 生成TLS证书

当使用安全EAP方法时，客户机设备(请求方)在向身份验证服务器发送自己的凭据之前验证其身份。
为此，身份验证服务器需要一个TLS证书。

该证书应:

1.  由客户端设备信任的证书颁发机构有效并签名
2.  在通用名称(CN)和主题替代名称字段中有一个完全合格的域名
3.  是否有扩展密钥使用属性表明它被授权对TLS服务器进行身份验证
4.  有效期不超过825天

EAP-TLS方法要求客户端设备具有TLS证书(而不是密码)。

要被用户管理器视为有效，客户端证书必须:

1.  由运行用户管理器的设备所信任的权威机构有效并签名
2.  在Subject Alt name (SAN)字段中设置用户名。为了向后兼容，您还可以将其添加到CN字段中。更多信息请访问: [https://datatracker.ietf.org/doc/html/rfc5216#section-5.2](https://datatracker.ietf.org/doc/html/rfc5216#section-5.2)

最后，[WPA3企业规范](https://www.wi-fi.org/download.php?file=/sites/default/files/private/WPA3_Specification_v3.0.pdf) 包括一个额外的安全模式，它提供192位加密安全性。

此模式需要使用EAP-TLS和以下证书:

1.  请使用长度至少为3072位的P-384椭圆曲线密钥或RSA密钥
2.  使用SHA384作为摘要(哈希)算法

为了简洁起见(以及展示更多的RouterOS功能)，本指南将展示如何在运行User Manager的设备上生成所有证书，但在大型企业环境中，认证服务器和客户端设备将各自在本地生成私钥和证书签名请求，然后将csr上传到证书颁发机构进行签名。

在运行User Manager的设备上执行的命令

```shell
# Generating a Certificate Authority
/certificate
add name=radius-ca common-name="RADIUS CA" key-size=secp384r1 digest-algorithm=sha384 days-valid=1825 key-usage=key-cert-sign,crl-sign
sign radius-ca ca-crl-host=radius.mikrotik.test
# Generating a server certificate for User Manager
add name=userman-cert common-name=radius.mikrotik.test subject-alt-name=DNS:radius.mikrotik.test key-size=secp384r1 digest-algorithm=sha384 days-valid=800 key-usage=tls-server
sign userman-cert ca=radius-ca
# Generating a client certificate
add name=maija-client-cert common-name=maija@mikrotik.test key-usage=tls-client days-valid=800 key-size=secp384r1 digest-algorithm=sha384
sign maija-client-cert ca=radius-ca
# Exporting the public key of the CA as well as the generated client private key and certificate for distribution to client devices
export-certificate radius-ca file-name=radius-ca
# A passphrase is needed for the export to include the private key
export-certificate maija-client-cert type=pkcs12 export-passphrase="true zebra capacitor ziptie"
```

# 配置用户管理器

在运行User Manager的设备上执行的命令

```shell
# Enabling User Manager and specifying, which certificate to use
/user-manager
set enabled=yes certificate=userman-cert
# Enabling CRL checking to avoid accepting revoked user certificates
/certificate settings
set crl-download=yes crl-use=yes
# Adding access points
/user-manager router
add name=ap1 address=10.0.0.11 shared-secret="Use a secure password generator for this"
add name=ap2 address=10.0.0.12 shared-secret="Use a secure password generator for this too"
# Limiting allowed authentication methods
/user-manager user group
set [find where name=default] outer-auths=eap-tls,eap-peap
add name=certificate-authenticated outer-auths=eap-tls
# Adding users
/user-manager user
add name=maija@mikrotik.test group=certificate-authenticated
add name=paija@mikrotik.test group=default password="right mule accumulator nail"
```

# 配置接入点

## AP运行常规无线包

在ap1上执行的命令

```shell
# Configuring radius client
/radius
add address=10.0.0.10 secret="Use a secure password generator for this" service=wireless timeout=1s
# Adding a security profile and applying it to wireless interfaces
/interface/wireless/security-profile
add name=radius mode=dynamic-keys authentication-types=wpa2-eap
/interface/wireless
set [find] security-profile=radius
```

## AP运行wifiwave2包

ap2上执行的命令

```shell
# Configuring radius client
/radius
add address=10.0.0.10 secret="Use a secure password generator for this too" service=wireless timeout=1s
# Configuring enabled authentication types. Can also be done via a security profile, but note that interface properties, if specified, override profile properties
/interface/wifiwave2 set [find] security.authentication-types=wpa2-eap,wpa3-eap
```

wifiwave2 AP也可以配置为使用更安全的wpa3-eap-192模式，但请注意，它要求所有客户端设备支持gmp -256密码并使用EAP-TLS身份验证。

客户端设备配置注意事项

## Windows

在Windows中手动安装CA时，请确保显式地将其放置在“受信任的根证书颁发机构”证书存储区中。它不会自动放置在那里。

## 安卓

当连接到带有EAP认证的网络时，Android设备会要求用户指定一个“域”。这是指RADIUS服务器的TLS证书中包含的主机名的预期域(microtik)。Test(在我们的例子中)。

缺省情况下，Android设备使用设备内置的根CA列表验证RADIUS服务器的证书。当使用自己的CA时，需要在适当的下拉菜单中选择它。

## iOS

Apple iOS似乎并不真正信任手动导入的CA来认证RADIUS服务器。服务器证书被标记为“不受信任”，除非CA是使用Apple专有的“Configurator”实用程序或经过批准的第三方MDM工具导入的。
