# ThingsBoard MQTT/HTTP服务器介绍

在RouterOS中引入容器功能，使得在路由器内运行各种任务的各种服务器成为可能。这对想减少网络设备数量的人来说尤其重要。与其在一个单独的设备/机器上运行服务器，为什么不在路由器内运行呢？

很多用户需要一个能够收集数据、存储数据并以容易理解的方式显示数据的服务器。这就是 [ThingsBoard](https://thingsboard.io/) 这样的平台能够发挥作用的地方。

它定位为一个物联网平台，可以在 [链接](https://thingsboard.io/iot-use-cases/) 中找到各种用例。

从RouterOS用户角度来看，最吸引人的是它可以作为MQTT服务器（MQTT broker）或HTTP服务器使用。这意味着可以使用 [MQTT publish](https://help.mikrotik.com/docs/display/ROS/MQTT) 或[HTTP post](https://help.mikrotik.com/docs/display/ROS/Fetch) 来发布数据。可以用 [这里](https://thingsboard.io/docs/reference/mqtt-api/) 的链接找到ThingsBoard MQTT API指南，用 [这里](https://thingsboard.io/docs/reference/http-api/) 的链接找到HTTP API。

简而言之，可以利用 [脚本](https://help.mikrotik.com/docs/display/ROS/Scripting) 来收集RouterOS的统计数据（如正常运行时间、GPS坐标、数据包统计，以及几乎所有打印到终端的其他信息），然后将这些信息存储到变量中，并从这些变量中构造一个JSON消息。然后通过 [scheduler](https://help.mikrotik.com/docs/display/ROS/Scheduler) 用MQTT或HTTP post将这个消息发送到ThingsBoard上（只要需要就可以运行这个脚本）。可以在 [本指南](https://help.mikrotik.com/docs/display/ROS/MQTT+and+ThingsBoard+configuration) 中找到基本脚本例子。

ThingsBoard在 [widgets](https://thingsboard.io/docs/user-guide/ui/widget-library/) 的帮助下存储和显示数据，可以用来设置仪表盘，以图形、表格、地图和其他方式的可视化数据。

有3个版本的ThingsBoard实例可用，每个实例使用不同的数据库:

- [thingsboard/tb-postgres](https://hub.docker.com/r/thingsboard/tb-postgres/) 
- [thingsboard/tb-cassandra](https://hub.docker.com/r/thingsboard/tb-cassandra/)
- [thingsboard/tb](https://hub.docker.com/r/thingsboard/tb/)

可以在 ThingsBoard/docker 文档中找到更多信息。

在这个例子中将展示 **tb-postgres** - 一个带有PostgreSQL数据库的ThingsBoard的单一实例。

## 概述

**Sub-menu:** `/container`

**注意**: 需要 **container** 包。

7.8rc1之前的RouterOS版本无法运行这个方案。

在进行配置之前，请务必研究 [容器](https://help.mikrotik.com/docs/display/ROS/Container) 指南。确保检查 [免责声明](https://help.mikrotik.com/docs/display/ROS/Container#Container-Disclaimer) 和 [要求](https://help.mikrotik.com/docs/display/ROS/Container#Container-Requirements) 部分了解所有风险和必要步骤。

这个例子将在一个 [云主机路由器（CHR）](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=18350234) 设备上运行它。为了在 [Virtual Box](https://www.virtualbox.org/) 中进行设置，请查看 [youtube教程](https://www.youtube.com/watch?v=oHXkaHkSVVo)。

在本指南发布时，**thingsboard/tb-postgres** 镜像只适用于linux/ **arm64** 操作系统架构，无法在arm32位架构的RouterOS设备上运行这个方案。

有几个参数需要牢记：

- 要明白这是一个 **服务器**，要有额外的空间来存放数据和镜像。测试中，8GB的磁盘空间足够了，但是可能要考虑为应用增加更多的空间，特别是如果打算运行更多的容器。要记住有一个储备会更好。
- 与磁盘空间一样，RAM内存也很重要。根据ThingsBoard文档，用带有PostgreSQL数据库的ThingsBoard单一实例时，建议分配至少1GB的RAM，并用最低负载（每秒几条消息）。建议使用2-4GB的RAM。换句话说，如果要在RouterBoard设备上运行，可能无法在内存小于1GB的设备上实现。这就是为什么要考虑一个有更多RAM内存的设备。在 "规格 "部分查看设备的RAM大小，例如 [CCR2004-16G-2S+](https://mikrotik.com/product/ccr2004_16g_2splus)。

转到 [技巧和窍门](https://help.mikrotik.com/docs/display/ROS/Container#Container-Tipsandtricks) 部分了解如何限制RAM。

## 配置

## 容器模式

启用容器模式:

`/system/device-mode/update container=yes`

如果在X86上使用容器，要按下复位按钮来确认设备模式，或者进行冷重启。

## 网络

为容器添加 veth 接口：

`/interface/veth/ add name =veth1 address =172.18.0.2/24 gateway =172.18.0.1`

为容器创建一个网桥，为其分配一个 IP 网络，并将 veth 添加到网桥上：

`/interface/bridge/ add name =dockertb`

`/ip/address/ add address =172.18.0.1/24 interface =dockertb`

`/interface/bridge/port add bridge =dockertb interface =veth1`

为出站流量设置NAT：

`/ip/firewall/nat/ add chain =srcnat action =masquerade src-address =172.18.0.0/24`

转发TCP 9090用于HTTP管理（ThingsBoard文档中的默认HTTP端口）。

建议只在本地测试时或通过VPN（当你确定本地网络是安全的）使用HTTP访问。

从互联网（从公共网络/WAN）访问容器WEB管理时，请考虑使用 **HTTPS** 。

`/ip firewall nat add action =dst-nat chain =dstnat dst-address =192.168.88.1 dst-port =9090 protocol =tcp to-addresses =172.18.0.2 to-ports =9090`

在上面DNAT（dst-nat）规则中显示的 `dst-address` 字段中，使用设备的本地IP地址。

在设置了本指南所示的其余步骤并验证ThingsBoard管理门户在本地工作后 **进一步确保设置** ：

- (a) 确保所有默认的ThingsBoard用户凭证已修改/删除，实施了强密码（参考ThingsBoard文档）。
- (b) **启用HTTPS**（步骤将在本指南后面解释）。
- (c) 最好将HTTPS端口改为非标准端口（参考 ThingsBoard 文档）。

只有提高了安全性之后才能考虑从广域网启用远程访问（通过在 `dst-address` 字段中使用公共IP地址，而不是上面例子中使用的本地IP）。此外，为了进一步提高安全性，可以使用 "src-address "或 "src-address-list "参数，在这里可以输入信任的公共源IP地址（一个已知信任的地址列表，例如，属于你的分支机构，可以从那里访问服务器），需要对安全负责。如果留下一扇门，有人可能会利用它。要有网络知识，并在设置此类方案时了解风险。

为非SSL MQTT转发TCP 1883（根据ThingsBoard文档使用的默认MQTT端口）。

建议仅在本地或通过VPN测试时使用非SSL MQTT（TCP 1883）通信（确定本地网络是安全的）。

请考虑使用 **SSL MQTT（TCP端口8883）**，而不是非SSL MQTT（TCP端口1883）用于现实生活中的应用，当从互联网（从公共网络）访问时。如果使用非SSL MQTT，客户端（MQTT publisher）和服务器（MQTT broker）之间的通信很容易被嗅探，这会损害认证数据（如客户端ID，用户名和密码）。

`/ip firewall nat add action =dst-nat chain =dstnat dst-address =192.168.88.1 dst-port =1883 protocol =tcp to-addresses =172.18.0.2 to-ports =1883`

与HTTP访问一样，在DNAT（dst-nat）规则中显示的 `dst-address` 字段，使用设备的本地IP地址。

在使用了本指南所示的其余步骤并验证ThingsBoard非SSL MQTT通信在本地工作后 **进一步确保设置** ：

- (a) 考虑从ThingsBoard安装中删除模板设备。
- (b) **启用SSL MQTT** （该步骤在本指南后面说明）。
- (c) 最好将MQTT端口改为非标准端口（参考 ThingsBoard 文档）。

启用SSL MQTT时，可以考虑从广域网打开TCP 8883（这是默认的SSL MQTT端口）（通过在 `dst-address` 字段中使用公共IP地址而不是本地IP，并将 `dst-port` 和 `to-ports` 从1883改为8883）。此外，为了进一步提高安全性，使用 `src-address` 或 `src-address-list` 参数，设置信任的公共IP地址列表。只有配置的受信IP才能与ThingsBoard代理建立MQTT连接。

## 环境变量和挂载

查看 [docker-thingsboard](https://hub.docker.com/r/thingsboard/tb-postgres) 文档，了解要添加的挂载和变量。

环境变量：

`/container/envs/ add name =tb_envs key =TB_QUEUE_TYPE value = "in-memory"`

Mounts:

`/container/mounts/ add name =mytb-data src =tb/mytb-data dst =/data`

`/container/mounts/ add name =mytb-logs src =tb/mytb-logs dst =/var/log/thingsboard`

## 获取镜像

为了简化配置，从外部库中获取镜像，也可以通过 [.tar](https://help.mikrotik.com/docs/display/ROS/Container#Container-b)importimagefromPC) 文件导入。

确保有相应的 "注册表URL "设置，限制RAM的使用（如果需要），并为镜像设置一个目录。

拉取镜像：

`/container/ add remote-image =thingsboard/tb-postgres:latest interface =veth1 root-dir =ThingsBoard mounts =mytb-data,mytb-logs envlist =tb_envs logging =yes`

运行该命令后，RouterOS应该开始 "提取 "软件包。检查 "文件系统 "是否有新创建的文件夹，用 `/container/print` 命令监控容器状态。

## 启动容器

确定容器已经添加，并且在运行 `/container/print` 后状态变为 `status=stopped` ，然后启动它。

等待几分钟，让容器完全加载。

## 验证

##管理权限

容器启动并安装后，用任何浏览器访问它，方法是 [http://192.168.88.1:9090](http://192.168.88.1:9090/)（其中IP地址是DNAT规则中使用的地址）:

![](https://help.mikrotik.com/docs/download/attachments/166920348/image-2023-1-19_14-18-55.png?version=1&modificationDate=1674130728030&api=v2)

默认凭证是（用户名/密码）。

- **系统管理员**: sysadmin@thingsboard.org / sysadmin
- **租户管理员**: tenant@thingsboard.org / tenant

登录提示确认服务器正在运行。

## MQTT测试

用 **租户** 登录，创建一个新的设备。进入 **设备** 菜单，点击 **+** （添加设备）按钮，选择 **添加新设备** 选项。

![](https://help.mikrotik.com/docs/download/attachments/166920348/image-2023-1-20_11-21-14.png?version=1&modificationDate=1674206465922&api=v2)

 按喜欢的方式命名，并点击 "**添加**":

![](https://help.mikrotik.com/docs/download/attachments/166920348/image-2023-1-20_11-22-22.png?version=1&modificationDate=1674206533996&api=v2)

点击刚刚创建的设备并选择 "**管理证书**" 设置来检查设备访问令牌（复制生成的访问令牌或输入你自己的"YOUR_TOKEN"）。:

![](https://help.mikrotik.com/docs/download/attachments/166920348/image-2023-1-20_11-24-15.png?version=1&modificationDate=1674206646593&api=v2)

在这些步骤之后，进入RouterOS设置（回到CHR设置），创建一个新的 [MQTT broker](https://help.mikrotik.com/docs/display/ROS/MQTT)（**确保你已经安装了IoT包**，否则将没有这个菜单）:

`/iot/mqtt/brokers/ add name =tb address =172.18.0.2 port =1883 username =YOUR_TOKEN`

以JSON格式发布一个静态测试MQTT消息：

`/iot/mqtt/publish broker="tb" topic="v1/devices/me/telemetry" message="{"test\":\"123\"}"`。

确认消息已经发布：

![](https://help.mikrotik.com/docs/download/attachments/166920348/image-2023-1-20_12-16-42.png?version=1&modificationDate=1674209793981&api=v2)

## 启用HTTPS和SSL MQTT

默认情况下，使用HTTP和MQTT协议。正如之前在 "网络 "部分提到的，使用非SSL的HTTP和非SSL的MQTT不是很安全（除非是在配置好的防火墙/限制访问的保护网络中使用），**建议启用HTTPS** 和 **SSL MQTT** 。

请查看ThingsBoard文档以了解更多信息  [HTTP over SSL](https://thingsboard.io/docs/user-guide/ssl/http-over-ssl/)  和 [MQTT over SSL](https://thingsboard.io/docs/user-guide/mqtt-over-ssl/)  指南。

首先，没有证书就没有SSL，需要制作（或购买）一个证书。

简而言之，本节将演示如何为HTTPS和SSL MQTT生成自签名证书。然后把它们上传到ThingsBoard中的正确文件夹，并相应地改变ThingsBoard配置文件。

在指南中使用RouterOS来生成这两个 [证书](https://help.mikrotik.com/docs/display/ROS/Certificates)，也可以使用OpenSSL或其他工具。

## 创建证书

为HTTPS创建一个证书：

`/certificate add name =TBhttps comm-name =172.18.0.2`

`/certificate sign TBhttps`

为MQTT创建一个证书：

`/certificate add name =TBmqtt common-name =172.18.0.2`

`/certificate sign TBmqtt`

用 `/certificate/print` 确认它们已添加：

`[admin@MikroTik] > /certificate/ print`

`Flags : K - PRIVATE-KEY; A - AUTHORITY; T - TRUSTED`

`Columns : NAME, COMMON-NAME, FINGERPRINT`

`0 KAT TBhttps  172.18.0.2   863f4547c74ce3ec70c3e82172502711517b52bbc055d18c24ba4aafec46152c`

`1 KAT TBmqtt   172.18.0.2   ebf3ff5d03ed4cc73546e058da9bc414cdaf24ce45da29b203348045fbbd21ae`

使用PKCS12格式导出证书，并为其设置密码口令:

`/certificate/export-certificate file-name=keystore export-passphrase=thingsboard_cert_ password type =pkcs12 numbers =0`

`/certificate/export-certificate file-name=mqttserver export-passphrase=thingsboard_mqttcert_ password type =pkcs12 numbers =1`

用你自己的 `export-passphrase` 并记住。

上述命令的输出将创建证书 **keystore.p12** 和 **mqttserver.p12** 文件，从 [文件列表](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=2555971) 菜单中下载。

```shell
[admin@MikroTik] > /file/print
Columns: NAME, TYPE, SIZE, CREATION-TIME
 #  NAME                 TYPE             SIZE       CREATION-TIME      
 0  tb/mytb-data         container store             jan/19/2023 13:43:16
 1  container-log.0.txt  .txt file        2240.5KiB  jan/27/2023 15:37:41
 2  skins                directory                   jan/18/2023 15:12:22
 3  tb/mytb-logs         container store             jan/27/2023 12:24:30
 4  pull                 directory                   jan/19/2023 13:41:01
 5  pub                  directory                   jan/18/2023 16:15:29
 6  tb                   directory                   jan/23/2023 15:46:39
 7  tb/data              container store             jan/18/2023 16:50:08
 8  tb/logs              container store             jan/18/2023 16:50:08
 9  mqttserver.p12       .p12 file        2438       jan/27/2023 15:36:26
10  keystore.p12         .p12 file        2448       jan/27/2023 15:08:07
11  ThingsBoard          container store             jan/19/2023 13:40:50
```

把两个文件从路由器下载到电脑上的任何目录。例如下载到 `C:\Users\Admin\Desktop\ThingsBoard` 文件夹。

## 下载 ThingsBoard 的配置文件

打开命令终端（"CMD"，以管理员身份，适用于Windows用户，或 "Linux Shell或命令终端"，适用于Linux用户）并导航到证书所在的目录：

```shell
C:\Windows\System32>cd c:\Users\Admin\Desktop\ThingsBoard
C:\Users\Admin\Desktop\ThingsBoard>dir
Directory of C:\Users\Admin\Desktop\ThingsBoard
 
27.01.2023  15:36    <DIR>          .
27.01.2023  15:36    <DIR>          ..
27.01.2023  15:09             2 448 keystore.p12
27.01.2023  15:36             2 434 mqttserver.p12
               2 File(s)          4 882 bytes
               2 Dir(s)  51 380 154 368 bytes free
```

从这个目录通过SFTP连接到路由器的IP（允许使用SSH协议进行文件传输，所以需要事先确保 [SSH服务](https://help.mikrotik.com/docs/display/ROS/Services) 已启用）:

`c:\Users\Admin\Desktop\ThingsBoard>sftp admin@192.168.88.1`

`The authenticity of host '192.168.88.1 (192.168.88.1)' can't be established.`

`RSA key fingerprint is SHA256:/WmmZErqWL51SOlS4EaGvSQ0i4HPnSIHCEjnc8AmP2c.`

`Are you sure you want to continue connecting (yes/no/[fingerprint])?yes`

`admin@192.168.88.1's password:`

`Connected to 192.168.88.1.`

`sftp>`

当容器运行时，进入ThingsBoard配置文件文件夹（使用 `dir` 或 `ls` 命令查看所在的文件夹内容，使用 `cd` 命令进入选择的文件夹）。默认它应该包含 "**thingsboard.yml**" 配置文件。在这个例子中可以定位在:

`sftp> cd ThingsBoard\usr\share\thingsboard\conf`

`sftp> dir`

`banner.txt          i18n                logback.xml         templates           thingsboard.conf    thingsboard.yml`     

使用 `get` 命令下载 "**thingsboard.yml**" 配置。把默认的ThingsBoard配置文件下载到机器上（启动SFTP的目录）:

```shell

sftp> get thingsboard.yml
Fetching /ThingsBoard/usr/share/thingsboard/conf/thingsboard.yml to thingsboard.yml
/ThingsBoard/usr/share/thingsboard/conf/thingsboard.yml                               100%   67KB   2.0MB/s   00:00
sftp> quit
 
c:\Users\Admin\Desktop\ThingsBoard>dir
 Directory of c:\Users\Admin\Desktop\ThingsBoard
 
30.01.2023  10:59    <DIR>          .
30.01.2023  10:59    <DIR>          ..
27.01.2023  15:09             2 448 keystore.p12
27.01.2023  15:36             2 434 mqttserver.p12
30.01.2023  10:59            68 846 thingsboard.yml
               3 File(s)         73 728 bytes
               2 Dir(s)  50 901 626 880 bytes free
```

## 改变 ThingsBoard 的设置

用文本编辑器（记事本或其他）打开 "**thingsboard.yml**"，修改几行。可以备份这个文件，以不同的名字保存，以便有一个默认设置的副本，防出现错误配置。

HTTPS相关设置:

1. Enable SSL →  Change "SSL_ENABLED:**false**" to "SSL_ENABLED:**true**";
2. Change credentials type → from "SSL_CREDENTIALS_TYPE:**PEM**" to "SSL_CREDENTIALS_TYPE:**KEYSTORE**";
3. Change the path → from "SSL_KEY_STORE:**classpath:keystore/keystore.p12**" to "SSL_KEY_STORE:**keystore.p12**" (optional);
4. Disable key alias setting → comment it → just put the "**#**" symbol in front of the **key_alias: "${SSL_KEY_ALIAS:tomcat}"** line;
5. Input your own certificate password that was used in RouterOS → from "SSL_KEY_STORE_PASSWORD:**thingsboard**" to "SSL_KEY_STORE_PASSWORD:**thingsboard_cert_password**" and from "SSL_KEY_PASSWORD:**thingsboard**" to "SSL_KEY_PASSWORD:**thingsboard_cert_password**".

```shell
ssl:
  # Enable/disable SSL support
  enabled: "${SSL_ENABLED:true}"
  # Server SSL credentials
  credentials:
    # Server credentials type (PEM - pem certificate file; KEYSTORE - java keystore)
    type: "${SSL_CREDENTIALS_TYPE:KEYSTORE}"
    # Keystore server credentials
    keystore:
      # Type of the key store (JKS or PKCS12)
      type: "${SSL_KEY_STORE_TYPE:PKCS12}"
      # Path to the key store that holds the SSL certificate
      store_file: "${SSL_KEY_STORE:keystore.p12}"
      # Password used to access the key store
      store_password: "${SSL_KEY_STORE_PASSWORD:thingsboard_cert_password}"
      # Key alias
      #key_alias: "${SSL_KEY_ALIAS:tomcat}"
      # Password used to access the key
      key_password: "${SSL_KEY_PASSWORD:thingsboard_cert_password}"
```

MQTT相关设置:

1. Enable SSL →  Change "MQTT_SSL_ENABLED:**false**" to "MQTT_SSL_ENABLED:**true**";
2. Change credentials type → from "MQTT_SSL_CREDENTIALS_TYPE:**PEM**" to "MQTT_SSL_CREDENTIALS_TYPE:**KEYSTORE**";
3. Change type of key → from "MQTT_SSL_KEY_STORE_TYPE:**JKS**" to "MQTT_SSL_KEY_STORE_TYPE:**PKCS12**";
4. Change the path (extension) → from "MQTT_SSL_KEY_STORE:mqttserver**.jks**" to "MQTT_SSL_KEY_STORE:mqttserver**.p12**";
5. Disable key alias setting → comment it → just put the "**#**" symbol in front of the **key_alias: "${MQTT_SSL_KEY_ALIAS:}"** line;
6. Input your own certificate password that was used in RouterOS → from "MQTT_SSL_KEY_STORE_PASSWORD:**server_ks_password**" to "MQTT_SSL_KEY_STORE_PASSWORD:**thingsboard_mqttcert_password**" and from "MQTT_SSL_KEY_PASSWORD:**server_key_password**" to "MQTT_SSL_KEY_PASSWORD:**thingsboard_mqttcert_password**".

```shell
ssl:
  # Enable/disable SSL support
  enabled: "${MQTT_SSL_ENABLED:true}"
  # Server SSL credentials
  credentials:
    # Server credentials type (PEM - pem certificate file; KEYSTORE - java keystore)
    type: "${MQTT_SSL_CREDENTIALS_TYPE:KEYSTORE}"
    # Keystore server credentials
    keystore:
      # Type of the key store (JKS or PKCS12)
      type: "${MQTT_SSL_KEY_STORE_TYPE:PKCS12}"
      # Path to the key store that holds the SSL certificate
      store_file: "${MQTT_SSL_KEY_STORE:mqttserver.p12}"
      # Password used to access the key store
      store_password: "${MQTT_SSL_KEY_STORE_PASSWORD:thingsboard_mqttcert_password}"
      # Optional alias of the private key; If not set, the platform will load the first private key from the keystore;
      #key_alias: "${MQTT_SSL_KEY_ALIAS:}"
      # Optional password to access the private key. If not set, the platform will attempt to load the private keys that are not protected with the password;
      key_password: "${MQTT_SSL_KEY_PASSWORD:thingsboard_mqttcert_password}"
```

将其余的设置保持为默认值。除非你知道自己在做什么，否则不要删除或改变上面例子中没有显示的行。

更改应用于 "**thingsboard.yml**" 文件（编辑后重新保存）。

## 上传更改后的 ThingsBoard 配置文件

剩下的就是用修改后的文件覆盖当前的配置文件，并上传两个证书。

再次确保终端指向正确的文件夹（其中有3个文件-两个证书和一个经过修改的 "thingsboard.yml "文件），SFTP到容器的配置文件目录中:

```shell
c:\Users\Admin\Desktop\ThingsBoard>dir
 Directory of c:\Users\Admin\Desktop\ThingsBoard
 
30.01.2023  10:59    <DIR>          .
30.01.2023  10:59    <DIR>          ..
27.01.2023  15:09             2 448 keystore.p12
27.01.2023  15:36             2 434 mqttserver.p12
30.01.2023  10:59            68 846 thingsboard.yml
               3 File(s)         73 728 bytes
               2 Dir(s)  50 901 626 880 bytes free
c:\Users\Admin\Desktop\ThingsBoard>sftp admin@192.168.88.1
admin@192.168.88.1's password:
Connected to 192.168.88.1.
sftp> cd ThingsBoard\usr\share\thingsboard\conf
sftp> dir
banner.txt          i18n                logback.xml         templates           thingsboard.conf    thingsboard.yml
```

用 `put` 命令上传这些文件:

```shell
sftp> put thingsboard.yml
Uploading thingsboard.yml to /ThingsBoard/usr/share/thingsboard/conf/thingsboard.yml
thingsboard.yml                                                                       100%   67KB   2.2MB/s   00:00
sftp> put keystore.p12
Uploading keystore.p12 to /ThingsBoard/usr/share/thingsboard/conf/keystore.p12
keystore.p12                                                                          100% 2448     1.2MB/s   00:00
sftp> put mqttserver.p12
Uploading mqttserver.p12 to /ThingsBoard/usr/share/thingsboard/conf/mqttserver.p12
mqttserver.p12                                                                        100% 2434   608.5KB/s   00:00
sftp> dir
banner.txt          i18n                keystore.p12        logback.xml         mqttserver.p12      templates          
thingsboard.conf    thingsboard.yml
```

重启容器:

`[admin@MikroTik] > /container/stop 0`

`[admin@MikroTik] > /container/start 0`

确保容器已停止（用 `/container/print` 命令后应显示 `status=stopped`），然后再启动它。

## 确认HTTPS访问

现在可以访问 [https://your_IP:9090](https://192.168.88.1/)（这里的IP地址是DNAT规则中使用的地址）:

![](https://help.mikrotik.com/docs/download/attachments/166920348/image-2023-1-30_13-10-45.png?version=1&modificationDate=1675077028174&api=v2)

由于用的是一个不是由受信任的机构签发的自签名证书，可能会出现一个错误，表明连接不安全，但可以通过浏览器查看该证书（确认就是那个），接受风险，然后继续。

## 确认ssl mqtt连接

**不要忘记改变端口转发规则**，该规则显示在 "网络"部分，将 `dst-port` 和 `to-ports` 从1883（标准非SSL MQTT端口）**改为8883**（**SSL MQTT端口**）。

在这个例子中将测试 [单向SSL通信访问令牌场景](https://help.mikrotik.com/docs/display/ROS/MQTT+and+ThingsBoard+configuration#MQTTandThingsBoardconfiguration-One-waySSLcommunicationscenario.1)。

### 用正在运行容器的设备进行测试

MQTT证书应该已经安装到设备的系统中（是设备产生的）。

添加MQTT broker:

`/iot/mqtt/brokers/ add name =tbssl address =172.18.0.2 port =8883 username =YOUR_TOKEN ssl =yes`

以JSON格式发布一个静态测试MQTT消息：

`/iot/mqtt/publish broker="tbssl" topic="v1/devices/me/telemetry" message="{"test\":\"123\"}"`。

确认被MQTT broker收到：

![](https://help.mikrotik.com/docs/download/attachments/166920348/image-2023-1-30_13-55-53.png?version=1&modificationDate=1675079736611&api=v2)

### 用另一台设备进行测试

当有两台RouterOS设备，一台正在运行容器（在这个例子中是生成证书的同一台设备），另一台希望从那里测试MQTT连接（比如 [LTAP](https://mikrotik.com/product/ltap) 或任何其他安装了IoT包的RouterOS设备），要把证书导入第二台设备中。

将导出的证书（**mqttserver.p12**）拖放到设备的 "文件列表 "中:

`[admin@LTAP] > /file/ print`

`Columns : NAME, TYPE, SIZE, CREATION-TIME`

`0  mqttserver.p12  .p12 file 2438  jan /30/2023 13:28:11`

`1  flash           disk             jul /06/2021 14:51:53`

`2  flash /pub       directory        jul/06/2021 14:51:53`

`3  flash /skins     directory        jan/01/1970 02:00:07`

`[admin@LTAP] >`

导入证书:

`[admin@LTAP] > /certificate/ import file-name =mqttserver.p12 passphrase =thingsboard_mqttcert_password`

添加MQTT broker，地址是ThingsBoard-container路由器上TCP 8883端口转发规则中使用的IP地址 "`dst-address`" 。

`/iot/mqtt/brokers/ add name =tbssl address =192.168.88.1 port =8883 username =YOUR_TOKEN ssl =yes`

以JSON格式发布一个静态测试MQTT消息。

`/iot/mqtt/publish broker="tbssl" topic="v1/devices/me/telemetry" message="{"test\":\"123\"}"`

确认broker收到它，在ThingsBoard上的 "Latest Telemetry"部分。
