# 概述

MikroTik为您连接到互联网的RouterBOARD设备提供多种服务。这些服务是为了缓解在配置、设置、控制、维护或监控您的设备时的不便之处。以下是IP/云计算可以提供的更详细的服务清单。

# 服务

请注意，如果路由器有多个公共IP地址和/或多个互联网网关，那么用于与MikroTik的云端服务器进行通信的确切IP可能与预期的不一样! 

IP/云需要在云主机路由器（CHR）上有一个有效的永久许可证。 

## DDNS

DDNS或动态DNS是一种服务，它定期更新A记录的IPv4地址和AAAA记录的IPv6地址。当ISP提供了一个定期变化的动态IP地址，但你需要一个可以用来远程连接设备的地址时，这样的服务就非常有用。下面你可以找到与IP/Cloud的DDNS服务有关的操作细节：

- 检查出站的IP地址变化：每60秒一次
- 等待MikroTik的云服务器的响应： 15秒
- DDNS记录TTL：60秒
- 使用UDP/15252端口向 [cloud.mikrotik.com](http://cloud.mikrotik.com) 或 [cloud2.mikrotik.com](http://cloud2.mikrotik.com) 发送加密的数据包。

自RouterOS v6.43以来，如果设备能够使用IPv6到达 [cloud2.mikrotik.com](http://cloud2.mikrotik.com)，那么为公共IPv6地址创建一个DNS **AAAA** 记录。如果设备只能使用IPv4到达 [cloud2.mikrotik.com](http://cloud2.mikrotik.com)，那么只为公共IPv4地址创建一个DNS **A** 记录。

要启用DDNS服务：

```shell
[admin@MikroTik] /ip cloud set ddns-enabled=yes
[admin@MikroTik] /ip cloud print
         ddns-enabled: yes
 ddns-update-interval: none
          update-time: yes
       public-address: 159.148.147.196
  public-address-ipv6: 2a02:610:7501:1000::2
             dns-name: 529c0491d41c.sn.mynetname.net
               status: updated
```

当启用该服务时，DNS名称将永久储存在MikroTik的云服务器上，这个DNS名称将解析到RouterOS实例发送到MikroTik云端服务器的最后一个IP。 

禁用DDNS服务： 

`/ip cloud set ddns-enabled=no`

一旦禁用该服务，设备就会向MikroTik的云端服务器发送一个命令删除存储的DNS名称。 

要手动触发一个DNS更新： 

`[admin@MikroTik] > /ip cloud force-update`

要使用云服务器提供的DNS名称实际连接到设备，用户必须配置路由器的防火墙，允许从WAN端口进行这种访问。(默认的MikroTik配置不允许从WAN端口访问诸如WebFig、WinBox等服务)。

## 更新时间

设备上正确的时间是很重要的，否则会导致系统日志的问题，破坏HTTPS与设备的连接，隧道连接等。要让系统的时钟更新，可以使用 [NTP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=40992869) 或 [SNTP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=40992869)，要为NTP服务器指定一个IP地址。在大多数情况下，为了简单地在设备上设置一个正确的时间，NTP/SNTP是不需要的，为了简单，可以使用IP云的更新时间服务。下面可以找到与IP/云的更新时间服务有关的操作细节：

- 大约时间（精确度为几秒，取决于UDP数据包的延迟）
- 在重启后和每次DDNS更新期间（当路由器的WAN IP地址改变或使用强制更新命令后）更新时间
- 使用UDP/15252端口向 [cloud.mikrotik.com](http://cloud.mikrotik.com) 或 [cloud2.mikrotik.com](http://cloud2.mikrotik.com) 发送加密的数据包
- 根据路由器的公共IP地址和商业数据库来检测时区。

要启用时间更新服务：

`[admin@MikroTik] > /ip cloud set update-time=yes`

要启用自动时区检测： 

`[admin@MikroTik] > /system clock set time-zone-autodetect=yes`

 如果 `/ip cloud upd-time` 设置为 `auto`，那么设备的时钟将以MikroTik的云端服务器时间更新（如果没有启用 [NTP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=40992869) 或 [SNTP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=40992869) 客户端）。 

## 备份

可以将设备的 [备份](https://help.mikrotik.com/docs/display/ROS/Backup) 存储在MikroTik的云服务器上。只要设备能够到达MikroTik的云服务器，备份服务就可以让你上传加密的备份文件，下载备份文件并应用于设备。下面可以找到与IP/云的备份服务有关的操作细节：

- 每台设备有1个免费的备份槽
- 允许的备份大小：15MB
- 使用UDP/15252和TCP/15252端口向 [cloud2.mikrotik.com](http://cloud2.mikrotik.com) 发送加密的数据包

要创建一个新的备份并将其上传到MikroTik的云服务器：

```shell
[admin@MikroTik] > /system backup cloud upload-file action=create-and-upload password=test123!!!
[admin@MikroTik] > /system backup cloud print
 0 name="cloud-20180921-162649" size=13.2KiB ros-version="6.44beta9" date=sep/21/2018 16:26:49 status="ok" secret-download-key="AbCdEfGhIjKlM1234567890"
```

`create-and-upload` 命令将创建一个新的系统备份文件，使用所提供的密码用AES对备份文件进行加密并上传。对于 `upload` 动作命令，密码属性没有影响，因为 `upload` 动作命令只上传已经创建的系统备份文件。 

下载上传的备份文件并保存到设备的内存中： 

```shell
[admin@MikroTik] > /system backup cloud download-file action=download number=0
### OR
[admin@MikroTik] > /system backup cloud download-file action=download secret-download-key=AbCdEfGhIjKlM1234567890
```

**警告：**  Secret-download-key是一个独特的标识符，可用来把加密备份下载到其他设备。因为可以通过Secret-download-key从任何地点和任何设备上下载加密备份，因此要对该标识符保密。下载的备份仍然是使用AES加密的，但是，请确保使用的是一个强大的密码! 

要删除上传的备份： 

`/system backup cloud remove-file number=0`

要上传一个现有的备份文件（之前创建的）： 

```shell
[admin@MikroTik] > /system backup save encryption=aes-sha256 name=old_backup password=test123!!!
[admin@MikroTik] > /system backup cloud upload-file action=upload src-file=old_backup.backup
[admin@MikroTik] > /system backup cloud print
 0 name="cloud-20180921-164044" size=13.2KiB ros-version="6.44beta9" date=sep/21/2018 16:40:44 status="ok" secret-download-key="AbCdEfGhIjKlM1234567890"
```

确保备份是使用AES加密的，否则，IP/云会拒绝备份上传。由于每个设备只有1个空闲的备份槽，在上传新的备份之前，需要删除现有的备份。 

**警告：** 在导入备份时，所有的MAC地址都被设置为设备原来使用的MAC地址。当替换一个故障的设备时很有用，但在多个设备上应用相同的备份时，这可能不可取，因为它将在多个设备上设置相同的MAC地址，这可能导致连接问题。可以在每个接口上使用 "reset-mac-address "命令来设置回原来的MAC地址。 

# 属性

**Sub-menu:** `/ip cloud`

| 属性                                                                     | 说明                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ddns-enabled** (_yes \| no_; Default：**no**)                          | 如果设置为 "yes"，那么设备将向MikroTik的云服务器发送加密信息。然后，服务器将对信息进行解密，并验证发送者是一个真实的MikroTik设备。如果一切正常，那么MikroTik的云服务器将为该设备创建一个DDNS记录，并向该设备发送一个响应。路由器上的IP/云服务每隔一分钟就会检查广域网的IP地址是否与发送给MikroTik的云服务器的地址相符，如果IP地址发生变化，就会向云服务器发送加密的更新。    |
| **ddns-update-interval** (_time, minimum 60 seconds_; Default: **none**) | 如果设定DDNS将在设定的时间间隔内尝试连接IP云服务器。如果设置为 “none”，将继续内部检查IP地址的更新，并根据需要连接到IP云服务器。如果所使用的IP地址不在路由器本身，因此不能作为路由器内部的值进行检查则很有用。                                                                                                                                                                |
| **update-time** (_yes \| no_; Default: **yes**)                          | 如果设置为 "是"，那么路由器的时钟将被设置为云服务器提供的时间，如果没有启用 [NTP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=40992869) 或 [SNTP](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=40992869)客户端。如果设置为 "no"，那么IP/云服务将永远不会更新设备的时钟。如果更新时间设置为 "yes"，即使ddns-enabled设置为 "no"，时钟也会更新。 |
| **public-address** (_read-only: address_)                                | 显示发送到云服务器的设备的IPv4地址。这个字段只有在至少一个IP云请求成功完成后才能看到。                                                                                                                                                                                                                                                                                       |
| **public-address-ivp6** (_read-only: address_)                           | 显示发送到云服务器的设备的IPv6地址。这个字段只有在至少一个IP云请求成功完成后才能看到。                                                                                                                                                                                                                                                                                       |
| **warning** (_read-only: string_)                                        | 如果设备发送的IP地址与MikroTik的云服务器可见的UDP数据包头中的IP地址不同，则显示一条警告信息。通常情况下，如果设备在NAT后面，就会发生这种情况。例如： "DDNS服务器收到了来自IP 123.123.123.123的请求，但你的本地IP是192.168.88.23；DDNS服务可能无法工作"                                                                                                                       |
| **dns-name** (_read-only: name_)                                         | 显示分配给设备的DNS名称。名称由12个字符的序列号组成，后面加上 [sn.mynetname.net](http://sn.mynetname.net) 。这个字段只有在至少一个ddns-request成功完成后才能看到。                                                                                                                                                                                                           |
| **status** (_read-only: string_)                                         | 包含描述当前dns服务状态的文本字符串。这些信息不需要解释<br>- updating...<br>- updated<br>- Error：没有互联网连接<br>- Error：请求超时。<br>- Error： 被拒绝了。联系MikroTik支持。<br>- Error：内部错误 - 不应该发生。一个可能的原因是路由器的内存用完了。                                                                                                                    |

## 高级的

**Sub-menu:** `/ip cloud advanced`

| 属性                                                 | 说明                                                                                                                   |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **use-local-address** (_yes \| no_; Default: **no**) | 默认情况下，DNS名称分配给检测到的公共地址（来自UDP包头）。如果希望发送 "本地 "或 "内部 "IP地址，那么将此设置为 "yes"。 |

## 云备份

**Sub-menu:** `/system backup cloud`

下面可以找到与特定命令有关的命令和属性，其他属性不会有任何影响。 

- 下载文件

| 属性                               | 说明                                                                                                                                               |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **action** (_download_)            | 从MikroTik的云服务器下载一个上传的备份文件。                                                                                                       |
| **number** (_integer_)             | 指定MikroTik云服务器上的备份槽，空闲的备份槽总是在0槽。                                                                                            |
| **secret-download-key** (_string_) | 唯一标识符，可用于下载上传的备份文件。当下载上传的备份文件时，不需要使用相同的设备，因为备份是从该设备上传的。当在一个新的设备上部署备份时很有用。 |

-  删除文件

| 属性                   | 说明                                                  |
| ---------------------- | ----------------------------------------------------- |
| **number** (_integer_) | 删除指定备份槽中的备份文件，空闲的备份槽总是在0槽中。 |

-  上传文件

| 属性                             | 说明                                                                                                                                                |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **action** (_create-and-upload_) | 将备份文件上传到MikroTik的云服务器。<br>- create-and-upload - 用指定的密码创建一个新的备份文件并上传。<br>- upload - 上传一个已创建的系统备份文件。 |
| **name** (_string_)              | 指定备份的名称，会显示在上传的备份列表中。这不是源备份的名字，这个名字只用于视觉表现。                                                              |
| **src-file** (_file_)            | 使用"/system backup "创建的备份的文件名来上传。这个属性只有在动作设置为 "upload "时才有作用。                                                       |
| **password** (_string_)          | 用指定的密码创建、加密和上传备份文件。这个属性只在动作被设置为”create-and-upload“时才有效果。                                                       |