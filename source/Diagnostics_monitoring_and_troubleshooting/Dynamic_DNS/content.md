# 介绍

`/tool dns-update`

**标准:** `RFC 2136, RFC 3007`

服务器有一个区域需要更新

## 属性

| 属性                               | 说明                                         |
| ---------------------------------- | -------------------------------------------- |
| **address** (_IP_; Default: )      | 定义与域名相关的IP地址。                     |
| **dns-server** (_IP_; Default: )   | 发送更新的DNS服务器。                        |
| **key** (_string_; Default: )      | 访问服务器的授权密钥。                       |
| **key-name** (_string_; Default: ) | 访问服务器的授权密钥名称（比如一个用户名）。 |
| **name** (_string_; Default: )     | 和IP地址关联的名称。                         |
| **ttl** (_integer_; Default: )     | 项目的生存时间（以秒为单位）。               |
| **zone** (_string_; Default: )     | 更新域名的DNS区域。                          |

路由器上的系统时间与DNS服务器的时间不能相差超过5分钟。否则DNS服务器会忽略这个请求。

## 例子

告诉 23.34.45.56 DNS 服务器将 myzone.com 区域中的 mydomain 名称与 68.42.14.4 IP 地址联系起来，指定密钥的名称为 dns-update-key，实际的密钥更新：

```shell
[admin@MikroTik] tool> dns-update dns-server=23.34.45.56 name=mydomain \
\... zone=myzone.com address=68.42.14.4 key-name=dns-update-key key=update
```
