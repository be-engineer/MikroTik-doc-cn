## 概述

证书管理器用于：

- 收集路由器内部的所有证书；
- 管理和创建自签名证书；
- 控制和设置 SCEP 相关配置；

从 RouterOS 版本 6 开始，证书有效性使用本地时区偏移显示。 在以前的版本中，它是 UTF。

  ## 通用菜单

`/certificate`

通用菜单用于管理证书、添加模板、颁发证书和管理 SCEP 客户端。

## 证书模板

执行证书颁发或证书申请命令后，证书模板立即被删除：

```
/certificate
add name=CA-Template common-name=CAtemp key-usage=key-cert-sign,crl-sign 
add name=Server common-name=server
add name=Client common-name=client
```

打印出证书：

```
[admin@4k11] /certificate> print detail 
Flags: K - private-key; L - crl; C - smart-card-key; A - authority; I - issued, R - revoked; E - expired; T - trusted 
 0         name="CA-Template" key-type=rsa common-name="CAtemp" key-size=2048 subject-alt-name="" days-valid=365 key-usage=key-cert-sign,crl-sign 

 1         name="Server" key-type=rsa common-name="server" key-size=2048 subject-alt-name="" days-valid=365 
           key-usage=digital-signature,key-encipherment,data-encipherment,key-cert-sign,crl-sign,tls-server,tls-client 

 2         name="Client" key-type=rsa common-name="client" key-size=2048 subject-alt-name="" days-valid=365 
           key-usage=digital-signature,key-encipherment,data-encipherment,key-cert-sign,crl-sign,tls-server,tls-client 
```

!!!warning 如果删除 CA 证书，则链中所有颁发的证书也将被删除。

## 签署证书

证书应签名。 在以下示例中，我们将签署证书并为服务器证书添加 CRL URL：

```
/certificate 
sign CA-Template 
sign Client      
sign Server ca-crl-host=192.168.88.1 name=ServerCA

```

检查证书是否已签名：

```
[admin@MikroTik] /certificate> print
Flags: K - private-key; L - crl; A - authority; T - trusted
Columns: NAME, COMMON-name, FINGERPRINT
#        NAME         COMMON  FINGERPRINT                                                     
0  K AT  CA-Template  CAtemp  0c7aaa7607a4dde1bbf33deaae6be7bac9fe4064ba47d64e8a73dcefad6cfc38
1  K AT  Client       client  b3ff25ecb166ea41e15733a7493003f3ea66310c10390c33e98fe32364c3659f
2  KLAT  ServerCA     server  152b88c9d81f4b765a59e2302e01efd1fbf11ceeed6e59f4974e87787a5bb980


```

!!!warning 密钥签名过程的时间取决于特定证书的密钥大小。 如果值为 4k 或更高，则可能需要大量时间才能在基于 CPU 的功能较弱的设备上签署此特定证书。

## 导出证书

可以使用密钥和 CA 证书导出客户端证书：

```
/certificate 
export-certificate CA-Template 
export-certificate ServerCA export-passphrase=yourpassphrase
export-certificate Client export-passphrase=yourpassphrase
```

导出的证书在 _/file_ 下可用：

```
[admin@MikroTik] > file print
Columns: NAME, TYPE, SIZE, CREATION-TIME
#  NAME                         TYPE        SIZE  CREATION-TIME       
0  skins                        directory         jan/19/2019 00:00:04
1  flash                        directory         jan/19/2019 01:00:00
2  flash/rw                     directory         jan/19/2019 01:00:00
3  flash/rw/disk                directory         jan/19/2019 01:00:00
4  pub                          directory         jan/19/2019 02:42:16
5  cert_export_CA-Template.crt  .crt file   1119  jan/19/2019 04:15:21
6  cert_export_ServerCA.crt     .crt file   1229  jan/19/2019 04:15:42
7  cert_export_ServerCA.key     .key file   1858  jan/19/2019 04:15:42
8  cert_export_Client.crt       .crt file   1164  jan/19/2019 04:15:55
9  cert_export_Client.key       .key file   1858  jan/19/2019 04:15:55
```

## Let's Encrypt证书

观看[关于此功能的视频](https://youtu.be/T1Dyg4_caa4)。

RouterOS v7 为“www-ssl”服务提供 Let's Encrypt (letsencrypt) 证书支持。 要通过自动证书续订启用 Let's Encrypt 证书服务，请使用“enable-ssl-certificate”命令：

```
/certificate enable-ssl-certificate dns-name=my.domain.com
```

请注意，DNS 名称必须指向路由器并且端口 TCP/80 必须可从 WAN 获得。 如果未指定 dns-name，它将默认为自动生成的 _ip cloud_ 名称（即 [http://example.sn.mynetname.net](http://example.sn.mynetname.net/)）