# 概述

Fetch是microrotik RouterOS中的一个控制台工具。它用于通过HTTP、FTP或SFTP(在v6.45中添加了对SFTP的支持)向网络设备复制文件，它也可以用于发送POST/GET请求和向远程服务器发送任何类型的数据。支持HTTPS协议;默认情况下，不进行证书检查，但是将 **check-certificate** 设置为 _yes_ 将启用来自本地证书存储的信任链验证。

# 属性

| 属性                                                           | 说明                                                                                                                                                                        |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **address** (_string_; Default: )                              | 复制文件的设备IP地址。                                                                                                                                                      |
| **-value** (_set\| not-set_;Default:**not-set**)              | 将输出存储在一个变量中，应该与output属性一起使用。                                                                                                                          |
| **ascii** (_yes\| no_;Default:**no**)                          | 可用于FTP和TFTP                                                                                                                                                             |
| **check-certificate** (_yes\| no_;Default:**no**)              | 启用本地证书存储的信任链验证。                                                                                                                                              |
| **dst-path** (_string_;Default:)                               | 目标文件名和路径                                                                                                                                                            |
| **host** (_string_; Default: )                                 | 域名或虚拟域名(如果在网站上使用，您希望从中复制信息)。例如,<br>`address=wiki.mikrotik.com host=forum.mikrotik.com`<br>本例中解析后的ip地址相同(66.228.113.27)，但主机不同。 |
| **http-method** (_\|delete\|get\|post\|put_; Default: **get**) | 使用的HTTP方法                                                                                                                                                              |
| **http-data** (_string_;Default:)                              | 使用PUT或POST方法时将要发送的数据                                                                                                                                           |
| **http-header-field** (_string_;Default:**empty**)         | 所有报头字段及其值的列表，格式为' http-header-field=h1:fff,h2:yyy '                                                                                                         |
| **keep-result** (_yes \| no_;Default:**yes**)                  | 如果是，则创建一个输入文件。                                                                                                                                                |
| **mode** (_ftp\|http\|tftp {!} https_;Default:**http**)        | 选择连接协议:http、https、ftp或tftp。                                                                                                                                       |
| **output** (_none\|file\|user_; Default: **file**)             | 设置在何处存储下载的数据<br>- none 表示不存储下载的数据<br>- file 将下载的数据保存到文件中<br>-user 在data变量中存储下载的数据                                              |
| **password** (_string_; Default: **anonymous**)                | 密码，用于对远端设备进行认证。                                                                                                                                              |
| **port** (_integer_;Default:)                                  | 连接端口。                                                                                                                                                                  |
| **src-path** (_string_;Default:)                               | 需要复制的远程文件的标题。                                                                                                                                                  |
| **upload** (_yes \| no_;Default:**no**)                        | 只有(S)FTP模式支持上传。如果启用，则fetch将用于将文件上传到远程服务器。要求设置 _src-path_ 和 _dst-path_ 参数。                                                             |
| **url** (_string_;Default:)                                    | 指向文件的URL。可以用来代替 **address** 和 **src-path** 参数。                                                                                                              |
| **user** (_string_;Default:**anonymous**)                      | 用户名，用于对远端设备进行认证。                                                                                                                                            |

  

# 配置举例

下面的示例展示了如何通过FTP协议从ip地址为192.168.88.2的设备上复制文件名为“conf.rsc”的文件，并将其保存为文件名为“123.rsc”的文件。登录设备需要用户名和密码。

```shell
[admin@MikroTik] /tool> fetch address=192.168.88.2 src-path=conf.rsc \
user=admin mode=ftp password=123 dst-path=123.rsc port=21 \
host="" keep-result=yes
```

上传文件到另一个服务器的例子:

```shell
[admin@MikroTik] /tool> fetch address=192.168.88.2 src-path=conf.rsc \
user=admin mode=ftp password=123 dst-path=123.rsc upload=yes
```

另一个演示url属性用法的文件下载例子。

```shell
[admin@MikroTik] /> /tool fetch url="https://www.mikrotik.com/img/netaddresses2.pdf" mode=http
  status: finished
 
[admin@test_host] /> /file print
 # NAME                     TYPE                  SIZE                 CREATION-TIME      
 ...
 5 netaddresses2.pdf        .pdf file             11547                jun/01/2010 11:59:51
```

## 向远程主机发送信息

可以使用HTTP POST请求将信息发送到准备接受它的远程服务器。在下面的例子中，我们将地理坐标发送到一个PHP页面:

```shell
/tool fetch http-method=post http-content-type="application/json" http-data="{\"lat\":\"56.12\",\"lon\":\"25.12\"}" url="https://testserver.lv/index.php"
```

在本例中，数据以文件的形式上传。注意，由于文件来自一个变量，因此它的大小最多只能为4KB。这是RouterOS变量的限制。

```shell
/export file=export.rsc
 
:global data [/file get [/file find name=export.rsc] contents];
:global $url "https://prod-51.westeurope.logic.azure.com:443/workflows/blabla/triggers/manual/paths/invoke....";
 
/tool fetch mode=https http-method=put http-data=$data url=$url
```

## 变量返回值

可以将fetch命令的结果保存到一个变量中。例如，可以根据HTTP页面返回的结果触发特定的操作。可以在下面找到一个非常简单的例子，当PHP页面返回“0”时禁用 **ether2**:

```shell
{
    :local result [/tool fetch url=https://10.0.0.1/disable_ether2.php as-value output=user];
    :if ($result->"status" = "finished") do={
        :if ($result->"data" = "0") do={
            /interface ethernet set ether2 disabled=yes;
        } else={
            /interface ethernet set ether2 disabled=no;
        }
    }
}
```

### SFTP

自6.45beta50 _/tool fetch_ 支持SFTP (SSH文件传输协议)协议:

```shell
[admin@MikroTik] > /tool fetch url="sftp://10.155.126.200/home/x86/Desktop/50MB.zip" user=x86 password=root dst-path=disk1
      status: downloading
  downloaded: 1048KiB
       total: 51200KiB
    duration: 6s
-- [Q quit|D dump|C-z pause]
```