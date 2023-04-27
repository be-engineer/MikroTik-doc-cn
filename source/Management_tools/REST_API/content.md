# 概述

观看 [关于此功能的视频](https://youtu.be/dwEcUa2KXNc)。

术语 "REST API "通常是指通过HTTP协议在一组预定义的面向资源的URL上访问API。 
从 **RouterOS v7.1beta4** 开始，作为控制台 [API](https://help.mikrotik.com/docs/display/ROS/API) 的一个JSON封装接口来实现。允许创建、读取、更新和删除资源以及调用任意的控制台命令。

要使用REST API，必须配置并运行 `www-ssl` 服务（[链接到IP服务]）。当SSL服务被启用时，REST服务可以通过连接到 `https://<routers_IP>/rest` 来访问。

最简单的方法是使用cURL、wget或任何其他HTTP客户端，甚至是RouterOS [fetch tool](https://help.mikrotik.com/docs/display/ROS/Fetch)。

```shell
$ curl -k -u admin: https://10.155.101.214/rest/system/resource
[{"architecture-name":"tile","board-name":"CCR1016-12S-1S+",
"build-time":"Dec/04/2020 14:19:51","cpu":"tilegx","cpu-count":"16",
"cpu-frequency":"1200","cpu-load":"1","free-hdd-space":"83439616",
"free-memory":"1503133696","platform":"MikroTik",
"total-hdd-space":"134217728","total-memory":"2046820352",
"uptime":"2d20h12m20s","version":"7.1beta4 (development)"}]
```

# 认证

对REST API的认证是通过 [HTTP Basic Auth](http://en.wikipedia.org/wiki/Basic_access_authentication) 进行的。提供用户名和密码与控制台用户相同（默认为 "admin"，没有密码）。

必须设置 [证书](https://help.mikrotik.com/docs/display/ROS/Certificates) 以使用安全的HTTPS，如果使用自签的证书，那么必须将CA导入到受信任的根中。然而，为了测试目的，可以用不安全的连接（对于cUrl使用-k标志，对于wget使用\--no-check-certificate）。

## JSON格式

服务器大致遵循ECMA-404标准，并有以下说明：

- 在JSON回复中，所有对象的值都编码为字符串，即使基础数据是一个数字或布尔值。
- 服务器也接受八进制格式（以0开头）和十六进制格式（以0x开头）的数字。如果数字是以字符串格式发送的，则假定它们是十进制格式的。
- 不支持带有指数的数字。

# HTTP方法

下面是一个支持的HTTP方法的表格

| HTTP Verv | CRUD      | ROS  | 说明                         |
| --------- | --------- | ---- | ---------------------------- |
| GET       | 读取      | 打印 | 获得记录                     |
| PATCH     | 更新/修改 | 设置 | 更新一条记录                 |
| PUT       | 创建      | 添加 | 创建一个新的记录             |
| DELETE    | 删除      | 删除 | 删除一条记录                 |
| POST      |           |      | 获取所有控制台命令的通用方法 |

## URL格式


## GET

这个方法允许从URL编码的指定菜单中获得所有记录的列表或单一记录。 
例如，获取所有IP地址（相当于CLI中的 `ip/address/print` 命令）：

```shell
$ curl -k -u admin: https://10.155.101.214/rest/ip/address
[{".id":"*1","actual-interface":"ether2","address":"10.0.0.111/24","disabled":"false",
"dynamic":"false","interface":"ether2","invalid":"false","network":"10.0.0.0"},
{".id":"*2","actual-interface":"ether3","address":"10.0.0.109/24","disabled":"true",
"dynamic":"false","interface":"ether3","invalid":"false","network":"10.0.0.0"}]
```

要返回一条记录，在URL的末尾加上ID：

```shell
$ curl -k -u admin: https://10.155.101.214/rest/ip/address/*1
{".id":"*1","actual-interface":"ether2","address":"10.0.0.111/24","disabled":"false",
"dynamic":"false","interface":"ether2","invalid":"false","network":"10.0.0.0"}
```

如果表包含命名的参数，那么可以使用名称而不是ID，例如，获取ether1：

`$ curl -k -u admin: https://10.155.101.214/rest/interface/ether1`

  
也可以对输出进行过滤，例如，只返回属于10.155.101.0网络的有效地址：

```shell
$ curl -k -u admin: "https://10.155.101.214/rest/ip/address?network=10.155.101.0&dynamic=true"
[{".id":"*8","actual-interface":"sfp12","address":"10.155.101.214/24","disabled":"false",
"dynamic":"true","interface":"sfp12","invalid":"false","network":"10.155.101.0"}]
```

另一个例子只返回 "哑巴 "接口上的地址，并带有 "测试 "注释：

```shell
$ curl -k -u admin: 'https://10.155.101.214/rest/ip/address?comment=test&interface=dummy'
[{".id":"*3","actual-interface":"dummy","address":"192.168.99.2/24","comment":"test",
"disabled":"false","dynamic":"false","interface":"dummy","invalid":"false","network":"192.168.99.0"}]
```

如果想只返回特定的属性，可以使用 '.proplist'，后面是 '=' 和一个用逗号分隔的属性列表。例如，要显示地址和是否禁用：

```shell
$ curl -k -u admin: https://10.155.101.214/rest/ip/address?.proplist=address,disabled
[{"address":"10.0.0.111/24","disabled":"false"},{"address":"10.0.0.109/24","disabled":"true"}]
```

## PATCH

该方法用于更新一条记录。设置PATCH调用主体为JSON对象，其中包含要更新的属性的字段和值。例如，添加一个注释：  

```shell
$ curl -k -u admin: -X PATCH https://10.155.101.214/rest/ip/address/*3 \
  --data '{"comment": "test"}' -H "content-type: application/json"
{".id":"*3","actual-interface":"dummy","address":"192.168.99.2/24","comment":"test",
"disabled":"false","dynamic":"false","interface":"dummy","invalid":"false","network":"192.168.99.0"}
```

在更新成功的情况下，服务器返回更新的对象及其所有参数。

## PUT

方法用于在URL编码的菜单中创建新记录。主体应该被设置为一个JSON对象，包含应用于新创建记录的参数。

在成功的情况下，服务器会返回带有所有参数的创建对象。

在一个请求中只能创建一个资源。

例如，为一个假的接口添加一个IP地址：

```shell
$ curl -k -u admin: -X PUT https://10.155.101.214/rest/ip/address \
  --data '{"address": "192.168.111.111", "interface": "dummy"}' -H "content-type: application/json"
{".id":"*A","actual-interface":"dummy","address":"192.168.111.111/32","disabled":"false",
"dynamic":"false","interface":"dummy","invalid":"false","network":"192.168.111.111"}
```
 

## DELETE

这个方法用来从URL编码的菜单中删除具有指定ID的记录。如果删除成功，服务器会以一个空的响应来回应。例如，调用删除记录两次，在第二次调用时路由器将返回404错误：

```shell
$ curl -k -u admin: -X DELETE https://10.155.101.214/rest/ip/address/*9
$ curl -k -u admin: -X DELETE https://10.155.101.214/rest/ip/address/*9
{"error":404,"message":"Not Found"}
```


## POST

所有的 [API](https://help.mikrotik.com/docs/display/ROS/API) 功能都可以通过 `POST` 方法实现。命令词在头中编码，可选参数在JSON对象中传递，有相应的字段和值。例如，要改变活动用户的密码，发送

```shell
POST https://router/rest/password
{"old-password":"old","new-password":"N3w", "confirm-new-password":"N3w"}
```

REST响应的结构与API响应类似： 

- 如果响应包含 `!re` 句子（记录），JSON回复将包含一个对象的列表。
- 如果 `!done` 句子包含数据，JSON回复将包含一个包含数据的对象。
- 如果 `!done` 句子中没有记录或数据，响应将包含一个空列表。

有两个特殊的键： `.proplist` 和 `.query`，它们与 `print` 命令词一起使用。在 [API](https://help.mikrotik.com/docs/display/ROS/API) 文档中阅读更多关于API响应、道具列表和查询的信息。

### Proplist

`.proplist` 键用于创建 `.proplist` 属性词。这些值可以是用逗号分隔的单个字符串：

```POST https://router/rest/interface/print
{".proplist":"name,type"}
```

或者字符串列表:

`POST https://router/rest/interface/print
{".proplist":["name","type"]}`

例如，从ip/address列表中返回地址和接口属性：

```shell
$ curl -k -u admin: -X POST https://10.155.101.214/rest/ip/address/print\
  --data '{"_proplist": ["address","interface"]}' -H "content-type: application/json"
[{"address":"192.168.99.2/24","interface":"dummy"},
{"address":"172.16.5.1/24","interface":"sfpplus1"},
{"address":"172.16.6.1/24","interface":"sfp2"},
{"address":"172.16.7.1/24","interface":"sfp3"},
{"address":"10.155.101.214/24","interface":"sfp12"},
{"address":"192.168.111.111/32","interface":"dummy"}]
```

### 查询

`.query` 键用于创建一个查询栈。值是一个查询词的列表。例如，这个POST请求：

```
POST https://router/rest/interface/print
{".query":["type=ether","type=vlan","#|!"]}
```

等于这个API句子

```
/interface/print
?type=ether
?type=vlan
?#|!
```

例如，结合 _query_ 和 _proplist_，来返回所有动态记录和网络为192.168.111.111的记录的 `.id`、`地址` 和 `接口` 属性

```shell
$ curl -k -u admin: -X POST https://10.155.101.214/rest/ip/address/print \
  --data '{".proplist": [".id","address","interface"], ".query": ["network=192.168.111.111","dynamic=true","#|"]}'\
  -H "content-type: application/json"
[{".id":"*8","address":"10.155.101.214/24","interface":"sfp12"},
{".id":"*A","address":"192.168.111.111/32","interface":"dummy"}]
```

### 超时

如果该命令无限期地运行，它将超时，并且连接将以错误的方式关闭。目前的超时时间间隔是60秒。为了避免超时错误，请添加一个参数，充分限制命令的执行时间。

超时不受传递给命令的参数的影响。如果命令被设置为运行一个小时，它将提前终止并返回错误信息。

例如，当ping命令超过超时时看看会得到什么，以及如何通过添加一个计数参数来防止这种情况：

```shell
$ curl -k -u admin: -X POST https://10.155.101.214/rest/ping \
  --data '{"address":"10.155.101.1"}' \
  -H "content-type: application/json"
{"detail":"Session closed","error":400,"message":"Bad Request"}
 
$ curl -k -u admin: -X POST https://10.155.101.214/rest/ping \
  --data '{"address":"10.155.101.1","count":"4"}' \
  -H "content-type: application/json"
[{"avg-rtt":"453us","host":"10.155.101.1","max-rtt":"453us","min-rtt":"453us","packet-loss":"0","received":"1","sent":"1","seq":"0","size":"56","time":"453us","ttl":"64"},
{"avg-rtt":"417us","host":"10.155.101.1","max-rtt":"453us","min-rtt":"382us","packet-loss":"0","received":"2","sent":"2","seq":"1","size":"56","time":"382us","ttl":"64"},
{"avg-rtt":"495us","host":"10.155.101.1","max-rtt":"650us","min-rtt":"382us","packet-loss":"0","received":"3","sent":"3","seq":"2","size":"56","time":"650us","ttl":"64"},
{"avg-rtt":"461us","host":"10.155.101.1","max-rtt":"650us","min-rtt":"359us","packet-loss":"0","received":"4","sent":"4","seq":"3","size":"56","time":"359us","ttl":"64"}]
```

另一个例子是一个带宽测试工具，通过运行时间来限制：

```shell
$ curl -k -u admin: -X POST 'https://10.155.101.214/rest/tool/bandwidth-test' \
  --data '{"address":"10.155.101.1","duration":"2s"}' \
  -H "content-type: application/json"
[{".section":"0","connection-count":"20","direction":"receive","lost-packets":"0",
"random-data":"false","rx-10-second-average":"0","rx-current":"0","rx-size":"1500",
"rx-total-average":"0",
"status":"connecting"},
{".section":"1","connection-count":"20","direction":"receive","duration":"1s",
"lost-packets":"0","random-data":"false","rx-10-second-average":"0","rx-current":"0",
"rx-size":"1500","rx-total-average":"0",
"status":"running"},
{".section":"2","connection-count":"20","direction":"receive","duration":"2s",
"lost-packets":"581175","random-data":"false","rx-10-second-average":"854372352",
"rx-current":"854372352","rx-size":"1500","rx-total-average":"854372352",
"status":"running"},
{".section":"3","connection-count":"20","direction":"receive","duration":"3s",
"lost-packets":"9014","random-data":"false","rx-10-second-average":"891979008",
"rx-current":"929585664","rx-size":"1500","rx-total-average":"891979008",
"status":"done testing"}]
```

# 错误

API调用的成功或失败在HTTP状态代码中显示。在失败的情况下（状态代码400或更大），响应的主体包含一个JSON对象，包含错误代码、错误描述和可选的错误细节。例如，试图删除一个接口将返回

`{"error":406,"message":"Not Acceptable","detail":"no such command or directory (remove)"}`