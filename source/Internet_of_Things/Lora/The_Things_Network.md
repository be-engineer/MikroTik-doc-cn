#  物联网

一旦在路由器上安装了lora软件包，并在 [The Things Network](https://thethingsnetwork.org) 上创建了一个账户，就可以设置运行中的网关了

- 登录你的账户，进入控制台并选择网关

![](https://help.mikrotik.com/docs/download/attachments/16351627/L1.png?version=1&modificationDate=1582031630567&api=v2)

  

- 选择 __注册网关_ 并填写空白。网关EUI可以在lora界面中找到

![](https://help.mikrotik.com/docs/download/attachments/16351627/L5.png?version=2&modificationDate=1582034145426&api=v2)

  

- 必须手动添加网络服务器，或者可以把路由器升级到稳定版本 **6.48.2**，服务器将自动添加（强烈建议）。


    [https://wiki.mikrotik.com/wiki/Manual:Upgrading\_RouterOS](https://wiki.mikrotik.com/wiki/Manual:Upgrading_RouterOS)

![](https://help.mikrotik.com/docs/download/attachments/16351627/image2021-5-19_9-22-15.png?version=1&modificationDate=1621405335830&api=v2)

  

```shell
/lora servers

add address=eu1.cloud.thethings.industries down-port=1700 name="TTS Cloud (eu1)" up-port=1700  
add address=nam1.cloud.thethings.industries down-port=1700 name="TTS Cloud (nam1)" up-port=1700  
add address=au1.cloud.thethings.industries down-port=1700 name="TTS Cloud (au1)" up-port=1700
```

  

![](https://help.mikrotik.com/docs/download/attachments/16351627/image2021-5-18_12-9-23.png?version=1&modificationDate=1621328963704&api=v2)

- 都填好后，按页面底部的注册网关。如果已经按照前面的步骤进行了相应的设置，应该看到lora网关已经连接上了。

![](https://help.mikrotik.com/docs/download/attachments/16351627/L9.png?version=4&modificationDate=1582035206074&api=v2)

- 一切都设置好了，现在有一个工作的lora网关。可以在流量部分监控传入的数据包

![](https://help.mikrotik.com/docs/download/attachments/16351627/L10.png?version=1&modificationDate=1582035498832&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/16351627/L11.png?version=1&modificationDate=1582035719531&api=v2)

  

今年晚些时候，The Things Network将迁移到一个新版本的网络服务器，称为 [The Things Stack](https://console.cloud.thethings.network/)。
