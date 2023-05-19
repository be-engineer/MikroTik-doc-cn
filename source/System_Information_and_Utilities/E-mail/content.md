# E-mail

-   [Properties](https://help.mikrotik.com/docs/display/ROS/E-mail#Email-Properties)
-   2[Sending Email](https://help.mikrotik.com/docs/display/ROS/E-mail#Email-SendingEmail)
-   3[Basic examples](https://help.mikrotik.com/docs/display/ROS/E-mail#Email-Basicexamples)

电子邮件工具是允许从路由器发送电子邮件的实用程序。该工具可用于向网络管理员发送常规配置备份和导出。

Email工具只使用明文认证和TLS加密。不支持其他方法。

# 属性

`/tool e-mail`

该子菜单允许设置要用的SMTP服务器

| 属性                                                  | 说明                                                                                                                                                                      |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_IP/IPv6 address_; Default: **0.0.0.0**) | SMTP服务器IP地址                                                                                                                                                          |
| **from** (_string_; Default: **<>**)                  | 将显示为收件人的姓名或电子邮件地址。                                                                                                                                      |
| **password** (_string_; Default: **""**)              | 验证SMTP服务器身份时使用的密码。                                                                                                                                          |
| **port** (_integer[0..65535]_; Default: **25**)       | SMTP服务器端口                                                                                                                                                            |
| **tls** (_no \| yes\| starttls_; Default: **no**)     | 是否使用TLS加密:<br>- yes - 发送STARTTLS，如果服务器上没有TLS，则丢弃会话<br>- no - 不发送STARTTLS<br>- starttls - 发送starttls，如果服务器响应TLS不可用，则继续不使用TLS |
| **user** (_string_; Default: **""**)                  | 用于SMTP服务器认证的用户名                                                                                                                                                |
| **vrf** (_VRF name_; default value: **main**)         | 设置服务创建出站连接的VRF。                                                                                                                                               |

  

**注意:** 所有服务器的配置(如果指定)可以被send命令覆盖。

# 发送电子邮件

`/tool e-mail send`

Send命令接受以下参数:

| 属性                                              | 说明                                                                                                                                                                      |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **body** (_string_; Default: )                    | 电子邮件消息的实际正文                                                                                                                                                    |
| **cc** (_string_;Default:)                        | 向列出的收件人发送副本。允许多个地址，使用“，”分隔                                                                                                                        |
| **file** (_File[, file]_;Default:)                | 将附加到邮件的文件名列表，以逗号分隔。                                                                                                                                    |
| **from** (_string_;Default:)                      | 姓名或电子邮件地址将显示为发件人。如果使用了服务器配置中未指定的值。                                                                                                      |
| **password** (_string_;Default:)                  | 验证SMTP服务器的密码。如果使用了服务器配置中未指定的值。                                                                                                                  |
| **port** (_integer[0..65535]_;Default:)           | SMTP服务器端口号。如果未指定，则使用服务器配置中的值。                                                                                                                    |
| **server** (_IP/IPv6地址_;Default:)               | SMTP服务器的Ip地址或IPv6地址。如果未指定，则使用服务器配置中的值。                                                                                                        |
| **tls** (_yes\| no \| starttls_; Default: **no**) | 是否使用TLS加密:<br>- yes - 发送STARTTLS，如果服务器上没有TLS，则丢弃会话<br>- no - 不发送STARTTLS<br>- starttls - 发送starttls，如果服务器响应TLS不可用，则继续不使用TLS |
| **subject** (_string_; Default: )                 | 消息的主题。                                                                                                                                                              |
| **to** (_string_;Default:)                        | 目的邮箱地址。允许单一地址。                                                                                                                                              |
| **user** (_string_;Default:)                      | 验证SMTP服务器的用户名。如果未指定，则使用服务器配置的值。                                                                                                                |

# 基本例子

**本示例介绍如何每24小时发送一次配置导出邮件**

1. 配置SMTP服务器

`[admin@MikroTik] /tool e-mail> set server=10.1.1.1 port=25 from="router@mydomain.com"`

2. 添加一个名为export-send的新脚本:

```shell
/export file=export
/tool e-mail send to="config@mydomain.com" subject="$[/system identity get name] export" \
body="$[/system clock get date] configuration file" file=export.rsc
```

3. 添加计划运行我们的脚本:

·/system scheduler add on-event="export-send" start-time=00:00:00 interval=24h

  

使用TLS/SSL加密发送电子邮件到服务器。例如，谷歌邮件需要这样做

谷歌邮件添加了一个新的安全政策，不允许第三方设备认证使用你的标准Gmail密码,你需要生成一个16位的应用程序”密码，并用它代替你的Gmail密码。要进行配置，请导航到“安全>登录到谷歌”部分设置，然后:

- 启用两步验证
- 生成App密码

在如下所示的set password=**mypassword** 设置中使用新生成的App密码。

1. 配置客户端连接到正确的服务器:

```shell
/tool e-mail
set address=smtp.gmail.com
set port=465
set tls=yes
set from=myuser@gmail.com
set user=myuser
set password=mypassword
```

2. 使用Send命令发送电子邮件:

`/tool e-mail send to=myuser@anotherdomain.com subject="email test" body="email test"`
