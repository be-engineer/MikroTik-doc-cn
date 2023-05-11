# SSH服务器

RouterOS内置的SSH服务器默认是启用的，并且在TCP/22端口监听传入的连接。可以在 [服务](https://help.mikrotik.com/docs/display/ROS/Services) 菜单下改变端口并禁用该服务器。

## 属性

**Sub-menu:** `/ip ssh   `

| 属性                                                                          | 说明                                                                                                                                                                                                                                               |
| ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **allow-none-crypto** (_yes\| no_; Default: **no**)                           | 如果加密被设置为无，是否允许连接。                                                                                                                                                                                                                 |
| **always-allow-password-login** (_yes \| no_; Default: **no**)                | 配置公钥授权时，是否同时允许密码登录。                                                                                                                                                                                                             |
| **forwarding-enabled** (_both\| local\| no\| remote_; Default: **no**)        | 允许哪种SSH转发方式： <br>- no - 禁用SSH转发；<br>- local - 允许SSH客户端从服务器（路由器）发起连接，这个设置也控制动态转发；<br>- remote - 允许SSH客户端在服务器（路由器）上监听并转发进入的连接；<br>- both - 允许本地和远程的转发方式。         |
| **host-key-size** (_1024 \| 1536 \| 2048 \| 4096 \| 8192_; Default: **2048**) | 当主机钥匙被重新生成时，要使用的RSA钥匙的大小。                                                                                                                                                                                                    |
| **strong-crypto** (_yes \| no_; Default: **no**)                              | 使用更强的加密、HMAC算法，使用更大的DH素数，不允许使用更弱的算法：<br>- 倾向于使用256和192位加密，而不是128位；<br>- 禁用空加密；<br>- 倾向于使用sha256而不是sha1进行散列；<br>- 禁用md5；<br>- 在Diffie Hellman交换中使用2048位素数而不是1024位。 |

**命令**

| 属性                                 | 说明                                                                                                                                              |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **export-host-key** (_key-file-prefix_)  | 将公共和私人RSA/DSA密钥导出到文件。命令需要一个参数： <br>- **key-file-prefix** - 用于生成文件的前缀，例如，前缀'my'将生成文件'my_rsa'，'my_rsa.pub'等。 |
| **import-host-key** (_private-key-file_) | 从指定文件中导入和替换私人DSA/RSA密钥。命令需要一个参数：<br>- **private-key-file** - 私人RSA/DSA密钥文件的名称                                          |
| **regenerate-host-key** ()               | 在路由器上生成新的替换当前的一套私钥（DSA，RSA）。请注意，以前导入的密钥可能会停止工作。                                                                 |

## 启用PKI认证

为用户 _admin_ 导入公钥的例子

[在客户端设备上生成SSH密钥](https://help.mikrotik.com/docs/display/ROS/SSH#SSH-Log-inusingRSApublic/privatekey)，将SSH公钥上传到路由器并导入。

`/user ssh-keys import public-key-file=id_rsa.pub user=admin`

# SSH客户

**Sub-menu:** `/system ssh`

## 简单登录到远程主机

它能连接到远程主机并启动ssh会话。IP地址支持IPv4和IPv6。

```shell
/system ssh 192.168.88.1
/system ssh 2001:db8:add:1337::beef
```

在这种情况下，提供给远程主机的用户名是已经登录到路由器的用户名。如果需要其他值，则必须使用 user=\<username\>。

```shell
/system ssh 192.168.88.1 user=lala
/system ssh 2001:db8:add:1337::beef user=lala
```

## 从路由器的特定IP地址登录

出于测试或安全原因，可能需要使用某些连接的源地址登录到其他主机。在这种情况下，要使用 src-address=\<ip address\> 参数。请注意，这种情况下的IP地址同时支持IPv4和IPv6。

```shell
/system ssh 192.168.88.1 src-address=192.168.89.2
/system ssh 2001:db8:add:1337::beef src-address=2001:db8:bad:1000::2
```

in this case, ssh client will try to bind to address specified and then initiate ssh connection to remote host.

## 使用RSA公钥/私钥登录

为用户 _admin_ 导入私钥的例子

首先，将当前生成的SSH密钥导出到一个文件：

`/ip ssh export-host-key key-file-prefix=admin`

生成两个文件 _admin_rsa_ 和 _admin_rsa.pub_ 。pub文件需要在SSH服务器端被信任（[如何在RouterOS上启用SSH PKI](https://help.mikrotik.com/docs/display/ROS/SSH#SSH-EnablingPKIauthentication)） 私钥必须为特定用户添加。

`/user ssh-keys private import user=admin private-key-file=admin_rsa`

只有在路由器上有完全权限的用户才能在 _/user ssh-keys private_ 下改变 "user "属性值。

在SSH服务器上安装了公钥并被信任后，可以创建一个PKI SSH会话。

`/system ssh 192.168.1.1`

## 执行远程命令

要执行远程命令，必须在登录行的最后提供。

```shell
/system ssh 192.168.88.1 "/ip address print"
/system ssh 192.168.88.1 command="/ip address print"
/system ssh 2001:db8:add:1337::beef "/ip address print"
/system ssh 2001:db8:add:1337::beef command="/ip address print"
```

如果服务器不支持pseudo-tty（ssh -T或ssh host命令），如mikrotik ssh服务器，那么就不能通过SSH发送多行命令。

例如，向MikroTik路由器发送命令 `/ip address\n add address=1.1.1.1/24` 将会失败。

如果你想通过 **脚本** 或 **调度器** 执行远程命令，请使用 **ssh-exec** 命令。

# SSH exec

**Sub-menu:** `/system ssh-exec`

_ssh-exec_ 是一个非交互式的ssh命令，因此可以通过脚本和调度器在设备上远程执行命令。

## 检索信息

该命令将返回两个值：

- **exit-code**：如果命令执行成功则返回0。
- **output**：返回远程执行命令的输出。

  
**例子：** 下面的代码从设备10.10.10.1检索ether1的接口状态，并将结果输出到"日志"中。

```shell
:local Status ([/system ssh-exec address=10.10.10.1 user=remote command=":put ([/interface ethernet monitor [find where name=ether1] once as-value]->\"status\")" as-value]->"output")
:log info $Status
```

出于安全考虑，不允许输入纯文本密码。为了确保安全地远程执行命令，对双方的用户使用SSH PKI认证。
 
执行该命令的用户组和脚本策略需要 **测试** 权限