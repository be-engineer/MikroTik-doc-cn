# 介绍

WebFig是一个基于网络的RouterOS工具，允许监控、配置和排除路由器的故障。它设计成WinBox的替代品，两者都有类似的布局，都可以访问RouterOS的几乎所有功能。

由于Webfig是独立于平台的，可以直接从各种设备上配置路由器，而不需要为特定平台开发软件。换句话说，不需要安装额外的软件。

WebFig允许执行三个基本动作：

- 配置 - 查看和编辑当前配置；
- 监控 - 显示路由器的当前状态、路由信息、接口统计、日志等；
- 故障排除 - RouterOS内置了许多故障排除工具（如ping、traceroute、数据包嗅探器、流量生成器等），它们都可以与WebFig一起使用。

# 连接到路由器

正如在 [首次配置](https://help.mikrotik.com/docs/display/ROS/First+Time+Configuration) 部分已经知道的，设备默认配置了用户名 **admin** 和 **无密码**。只要打开一个Web浏览器，在搜索栏中输入设备的IP地址，默认为 **192.168.88.1.**，确保设备有同一网络的IP地址，例如192.168.88.2，否则第三层通信将无法工作。

![](https://help.mikrotik.com/docs/download/attachments/328131/webfig.png?version=3&modificationDate=1571210992820&api=v2)

在下面的例子中，使用IP地址10.155.126.250来通过WebFig.Level3连接到设备。

# 启用HTTPS

为了使HTTPS正常工作，要指定一个Webfig可以使用的有效证书。可以用由受信任的证书颁发机构（CA）颁发的证书，或者创建自己的根CA并生成自签名证书。 

Webfig 支持通配符证书。可以通过在通用名称属性中指定通配符来生成这样的证书，例如，_通用名称=*. [mikrotik.com](https://mikrotik.com)._

要生成自己的证书并启用HTTPS访问，必须配置以下内容：

在路由器上创建自己的根CA，并签署它

```shell
[admin@MikroTik] > certificate add name=local-cert common-name=local-cert key-usage=key-cert-sign,crl-sign
[admin@MikroTik] > certificate sign local-cert
  progress: done
```

如果已经建立了自己的 CA，或者用的是为你签署证书的服务，那么就在远程创建并签署证书，然后再把证书导入路由器上。如果正在导入证书，请确保把证书标记为受信任。

为Webfig创建一个新证书（非root证书）

```shell
[admin@MikroTik] > certificate add name=webfig common-name=192.168.88.1
[admin@MikroTik] > certificate sign webfig
  progress: done
[admin@MikroTik] > certificate print
Flags: K - private-key; A - authority; T - trusted
Columns:NAME        COMMON-NAME     FINGERPRINT                                                    
0  KAT  local-cert  local-cert      9b6363d033c4b2e6893c340675cfb8d1e330977526dba347a440fabffd983c5d
1  KAT  webfig      192.168.88.1    9f84ac2979bea65dccd02652056e5559bcdf866f8da5f924139d99453402bd02
```

启用 **www-ssl**，并指定为Webfig使用新创建的证书。

```shell
[admin@MikroTik] > ip service
set www-ssl certificate=webfig disabled=no
```

现在可以访问 [https://192.168.88.1](https://192.168.88.1) 并安全地配置路由器了。

默认情况下，浏览器不信任自签证书，需要在第一次访问浏览器的页面时，将证书添加为受信任的。另一种方法是导出根CA证书，将其作为受信任的根证书导入电脑，这样一来，由该路由器签署的所有证书都会被认为是有效的，也会使网络中的证书管理变得更加容易。

大多数互联网浏览器都有自己的证书信任链，并独立于操作系统的证书信任链工作，这意味着可能要在浏览器设置中添加自己的根CA的证书作为信任证书，因为在操作系统的设置中信任证书在使用互联网浏览器时可能没有任何效果。

# 皮肤

WebFig设计皮肤是一个方便的工具，使界面更加友好。它不是一个安全工具。如果用户有足够的权限，就有可能通过其他方式访问隐藏的功能。

## 设计皮肤

如果用户有足够的权限（该组有编辑权限的策略），**设计皮肤** 按钮就可以使用。按下该切换按钮将打开界面编辑选项。 可能的操作有：

- 隐藏菜单 - 这将隐藏菜单和其子菜单中的所有项目；
- 隐藏子菜单 - 只有某些子菜单会被隐藏；
- 隐藏标签 - 如果子菜单的细节有几个标签，可以用这种方式隐藏它们；
- 重命名菜单和项目--使某些功能更明显，或将它们翻译成你的语言；
- 为项目添加注释（在详细视图中）--在字段上添加注释；
- 使项目成为只读（在详细视图中）--为了用户安全，非常敏感的字段可以成为只读；
- 隐藏标志（在详细视图中）--虽然只能在详细视图中隐藏一个标志，但这个标志在列表视图和详细视图中是不可见的；
- 为字段添加限制--（在详细视图中），其中是以逗号或换行分隔的允许值的时间列表：
    - 数字间隔'...'例如：1...10将允许带数字的字段的值从1到10，例如，MTU大小。
    - 字段前缀（文本字段、MAC地址、设置字段、组合框）。如果需要限制前缀长度，_\$_ 应该加在最后。例如，将无线接口只限制为 "站"，"添加限制 "将包含 "station$"

![](https://help.mikrotik.com/docs/download/attachments/328131/image-2022-11-8_15-57-32.png?version=1&modificationDate=1667915851247&api=v2)

- 添加 _标签_ - 将添加一个带有可编辑标签的灰色丝带，将字段分开。色带将被添加到它所添加的字段之前；
- Add _Separator_ - 在被添加到的字段之前添加一个低高度的水平分隔符。

**注意：** 数字间隔不能被设置为扩展RouterOS为该字段设置的限制。

**注意:** 设置字段是由一组复选框组成的参数，例如，为用户组、RADIUS "服务 "设置策略

**注意：** 为组合框设置的限制将从下拉菜单中选择值。

## 皮肤设计实例

如果需要为某些服务限制用户 

![](https://help.mikrotik.com/docs/download/attachments/328131/image-2022-11-8_16-47-4.png?version=1&modificationDate=1667918823526&api=v2)

为RADIUS服务添加一个限制。

![](https://help.mikrotik.com/docs/download/attachments/328131/image-2022-11-8_17-6-52.png?version=1&modificationDate=1667920010786&api=v2)

结果将是只有那些服务在"限制"字段中被指出。

![](https://help.mikrotik.com/docs/download/attachments/328131/image-2022-11-8_17-7-15.png?version=1&modificationDate=1667920033833&api=v2)

## 使用皮肤

要使用皮肤，必须将皮肤分配给组。完成后，该组的用户在登录WebFig或Winbox时将自动使用选定的皮肤作为默认皮肤。

`/user/group/set your_group_name skin=your_skin`。

如果需要在另一个路由器上使用创建的皮肤，可以把文件复制到另一个路由器的皮肤文件夹中。在新路由器上把复制的皮肤添加到用户组才能使用。
