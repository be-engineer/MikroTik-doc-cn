# 概述

MikroTik RouterOS对HTTP和HTTP-proxy（用于FTP和HTTP协议）请求进行代理。代理服务器执行互联网对象缓存功能，将请求的互联网对象，即通过HTTP和FTP协议提供的数据存储在定位更接近接收者的系统上，通过以本地网络速度从代理缓存中交付客户请求的文件副本，从而加快客户的浏览速度。MikroTik RouterOS实现了以下代理服务器功能：

- 常规HTTP代理--客户（本身）指定什么是代理服务器；
- 透明代理--客户不知道代理的启用，也没有必要对客户端的网络浏览器进行任何额外的配置；
- 按来源、目的地、URL和请求方法（HTTP防火墙）的访问列表；
- 缓存访问列表，指定哪些对象需要缓存，哪些不需要；
- 直接访问列表-指定哪些资源应该直接访问，哪些--通过另一个代理服务器；
- 日志设施-允许获取和存储有关代理操作的信息；
- 父代理-允许指定另一个代理服务器，（如果他们没有要求的对象，就问他们的父代理，或者问原始服务器）；

  
代理服务器通常放置在用户和互联网上的目标服务器（也称为原点服务器）之间的不同位置。

![](https://help.mikrotik.com/docs/download/attachments/132350000/Image10002.jpg?version=1&modificationDate=1658409074627&api=v2)

网络代理（缓存）观察来自客户端的请求，为自己保存响应的副本。然后，如果有另一个对同一URL的请求，它可以使用它所拥有的响应，而不是再次向原服务器请求。如果代理没有请求文件，它就从原服务器下载。

代理服务器可能有许多潜在的目的：

- 提高资源的访问速度（客户端获得对象所需的时间更短）；
- 作为HTTP防火墙工作（拒绝访问不希望看到的网页）；

允许过滤网页内容（通过特定的参数，如源地址、目标地址、端口、URL、HTTP请求方法）扫描出站内容，例如，用于数据泄漏保护。

当你想用它作为HTTP和FTP防火墙（例如，拒绝访问不需要的网页或拒绝特定类型的文件，如.mp3文件）或透明地将请求重定向到外部代理（可能是具有缓存功能的代理）时，即使没有缓存，它也可能是有用的。

# 配置示例

`/ip/proxy`

在MikroTik RouterOS中，代理配置是在/ip/proxy菜单中进行的。请看下面如何在8080端口启用代理，并将192.168.88.254设置为代理源地址：

```shell
[admin@MikroTik] > ip/proxy/set enabled=yes port=8080 src-address=192.168.88.254
[admin@MikroTik] > ip/proxy/print
                 enabled: yes
             src-address: 192.168.88.254
                    port: 8080
               anonymous: no
            parent-proxy: ::
       parent-proxy-port: 0
     cache-administrator: webmaster
          max-cache-size: unlimited
   max-cache-object-size: 2048KiB
           cache-on-disk: no
  max-client-connections: 600
  max-server-connections: 600
          max-fresh-time: 3d
   serialize-connections: no
       always-from-cache: no
          cache-hit-dscp: 4
              cache-path: web-proxy
```

在设置常规代理服务时，要确保它只为客户提供服务，并通过建立防火墙，只允许客户使用代理，防止未经授权的访问，否则，它可能被当作一个开放的代理。

## 透明的代理配置实例

RouterOS也可以作为一个透明的缓存服务器，在客户的网络浏览器中不需要配置。一个透明的代理不会修改请求的URL或响应。RouterOS将接收所有的HTTP请求并将其重定向到本地代理服务。这个过程对用户来说将是完全透明的（用户可能对位于他们和原始服务器之间的代理服务器一无所知），对他们来说唯一的区别是浏览速度的提高。

为了启用透明模式，必须在目标NAT中添加防火墙规则，指定哪些连接（到哪些端口）应该透明地重定向到代理。检查上面的代理设置，将用户（192.168.1.0/24）重定向到代理服务器：

  

```shell
[admin@MikroTik] ip firewall nat> add chain=dstnat protocol=tcp src-address=192.168.1.0/24 dst-port=80 action=redirect to-ports=8080
[admin@MikroTik] ip firewall nat> print
Flags: X - disabled, I - invalid, D - dynamic
 0   chain=dstnat protocol=tcp dst-port=80 action=redirect to-ports=8080
```

 网络代理可以同时作为透明和普通网络代理使用。在透明模式下，它也可以作为一个标准的网络代理使用。然而，在这种情况下，代理用户可能难以到达透明访问的网页。

## 基于代理的防火墙 - 访问列表

访问列表的实现方式与MikroTik防火墙规则从上到下的处理方式相同。第一条匹配规则规定了对该连接的处理决定。连接可以通过其源地址、目标地址、目标端口、请求的URL（统一资源定位器）的子字符串或请求方法进行匹配。如果没有指定这些参数，每一个连接都将匹配这个规则。

如果一个连接被一个规则匹配，这个规则的动作属性指定是否允许连接（拒绝）。如果一个连接不匹配任何规则，则会被允许。

在这个例子中，假设配置了一个透明的代理服务器，它将阻止网站 [http://www.facebook.com](http://www.facebook.com/)，可以通过给出src-address对不同的网络进行阻止：

`/ip proxy access add src-address=192.168.1.0/24 dst-host=www.facebook.com action=deny`

来自网络192.168.1.0/24的用户将不能访问网站 [www.facebook.com](http://www.facebook.com/)。

也可以阻止URL中包含特定单词的网站：

`/ip proxy access add dst-host=:mail action=deny`

该声明将阻止所有URL中包含 "邮件 "一词的网站。如 [www.mail.com](http://www.mail.com/), [www.hotmail.com](http://www.hotmail.com/), [mail.yahoo.com](http://mail.yahoo.com), 等等。

还可以阻止下载特定类型的文件，如.flv, .avi, .mp4, .mp3, .exe, .dat, ...等等。

```shell
/ip proxy access
add path=*.flv action=deny
add path=*.avi action=deny
add path=*.mp4 action=deny
add path=*.mp3 action=deny
add path=*.zip action=deny
add path=*.rar action=deny
```

这里也有不同的通配符创建特定的条件，并通过代理访问列表来匹配它们。通配符属性（dst-host和dst-path）匹配一个完整的字符串（例如，如果它们被设置为 "example"，它们将不会匹配 [example.com](http://example.com)）。可用的通配符是'*'（匹配任意数量的任意字符）和'?'（匹配任意一个字符）。

也接受正则表达式，但如果该属性应被视为正则表达式，它应该以冒号（':'）开始。

为了表明在给定的模式之前不允许有任何符号，在模式的开头使用^符号。

为了说明在给定模式之后不允许有任何符号，在模式的末尾使用$符号。

# 启用RAM或基于存储的缓存

在这个例子中，假定已经配置了代理，并且正在工作，想启用缓存。如果需要命令参数的详细说明，请查看位于例子下面的参考。

- 基于RAM的缓存：
    - 如果设备有很多RAM用于缓存，则很好。在内存为256MB或更少的设备上启用这个功能，不会给网络带来任何好处。
    - 缓存的写入/读取速度比存储在USB或SATA连接介质上的快。

- 基于存储的高速缓存：
    - 仅仅由于介质容量的不同，可以使用更大的代理缓存。

## RAM代理缓存

重要命令：

-   max-cache-size=
-   max-cache-object-size=
-   cache-on-disk=

```shell

[admin@MikroTik] /ip proxy> set max-cache-size=unlimited max-cache-object-size=50000KiB cache-on-disk=no
...
[admin@MikroTik] /ip proxy> print
                 enabled: yes
             src-address: ::
                    port: 8080
               anonymous: no
            parent-proxy: 0.0.0.0
       parent-proxy-port: 0
     cache-administrator: webmaster
          max-cache-size: unlimited  <-------
   max-cache-object-size: 500000KiB  <-------
           cache-on-disk: no  <-------
  max-client-connections: 600
  max-server-connections: 600
          max-fresh-time: 3d
   serialize-connections: no
       always-from-cache: no
          cache-hit-dscp: 4
              cache-path: proxy-cache
```

## 存储代理缓存

重要命令：

-   max-cache-size=
-   max-cache-object-size=
-   cache-on-disk=
-   cache-path=

```shell
[admin@MikroTik] > ip proxy set cache-on-disk=yes cache-path=/usb1/proxy/cache
 
[admin@MikroTik] > ip proxy print                                               
                 enabled: yes
             src-address: ::
                    port: 8080
               anonymous: no
            parent-proxy: 0.0.0.0
       parent-proxy-port: 0
     cache-administrator: webmaster
          max-cache-size: unlimited  <-------
   max-cache-object-size: 50000KiB  <-------
           cache-on-disk: yes  <-------
  max-client-connections: 600
  max-server-connections: 600
          max-fresh-time: 3d
   serialize-connections: no
       always-from-cache: no
          cache-hit-dscp: 4
              cache-path: usb1/proxy/cache  <-------
 
[admin@MikroTik] > file print                                                   
 # NAME                                                           TYPE             
 0 skins                                                          directory       
 5 usb1/proxy                                                     directory          
 6 usb1/proxy/cache                                               web-proxy store   <-------     
 7 usb1/lost+found                                                directory
```

**检查缓存是否在工作：**

```shell
[admin@MikroTik] > ip proxy monitor
                 status: running
                 uptime: 2w20h28m25s
     client-connections: 15
     server-connections: 7
               requests: 79772
                   hits: 30513
             cache-used: 481KiB
         total-ram-used: 1207KiB
  received-from-servers: 4042536KiB
        sent-to-clients: 4399757KiB
   hits-sent-to-clients: 176934KiB
```

# 参考资料

每个菜单的所有可用参数和命令的列表。

### 常规命令

`/ip/proxy`

  

| 属性                                                                                             | 说明                                                                                                                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **always-from-cache** (_yes\| no_; Default: **no**)                                              | 如果内容被认为是新鲜的，则忽略客户端的刷新请求。                                                                                                                                                                                                              |
| **anonymous** (_yes \| no_; Default: **no**)                                                     | 如果不设置，客户端的IP地址将通过X-Forwarded-For头（可以在远程服务器中使用HTTP_X_FORWARDED_FOR环境变量访问）。                                                                                                                                                 |
| **cache-administrator** (_string_; Default: **webmaster**)                                       | 管理员的电子邮件显示在代理错误页面                                                                                                                                                                                                                            |
| **cache-hit-dscp** (_integer: 0..63_; Default: **4**)                                            | 自动用提供的DSCP值来标记缓存的命中率                                                                                                                                                                                                                          |
| **cache-on-disk** (_yes \| no_; Default: **no**)                                                 | 是否将缓存存储在磁盘上。                                                                                                                                                                                                                                      |
| **cache-path** (_string_; Default: **web-proxy**)                                                | 启用磁盘上缓存时，缓存存储的路径。                                                                                                                                                                                                                            |
| **max-cache-object-size** (_integer: 0..4294967295[KiB]_; Default: **2048KiB**)                  | 指定最大的缓存对象大小，以千字节为单位。                                                                                                                                                                                                                      |
| **max-cache-size** (_none \| unlimited \| integer: 0...4294967295[KiB]_; Default: **unlimited**) | 指定最大的缓存大小，以千字节为单位。                                                                                                                                                                                                                          |
| **max-client-connections** (_integer: Dynamic_ ; Default: **600**)                               | 接受来自客户端的最大连接数（任何进一步的连接将被拒绝）。                                                                                                                                                                                                      |
| **max-fresh-time** (_time_; Default: **3d**)                                                     | 存储一个缓存对象的最大时间。对象的有效期通常由对象本身定义，但如果它设置得太高，会覆盖最大的值。                                                                                                                                                              |
| **max-server-connections** (_integer: Dynamic_ ; Default: **600**)                               | 与服务器的最大连接数（任何来自客户端的进一步连接将被搁置，直到服务器连接终止）。                                                                                                                                                                              |
| **parent-proxy** (_Ip4 \| ip6_; 默认: **0.0.0.0**)                                               | 另一个HTTP代理的IP地址和端口，将所有请求重定向到该代理。如果设置为0.0.0.0，则不使用父代理。                                                                                                                                                                   |
| **parent-proxy-port** (_integer: 0..65535_; Default: **0**)                                      | 父代理监听的端口。                                                                                                                                                                                                                                            |
| **port** (_integer: 0...65535_; Default: **8080**)                                               | 代理服务器将监听的TCP端口。这个端口必须在所有想使用服务器作为HTTP代理的客户上指定。通过使用目标NAT功能将HTTP请求重定向到IP防火墙的这个端口，可以实现透明的（对客户的零配置）代理设置。                                                                        |
| **serialize-connections** (_yes\| no_; Default: **no**)                                          | 如果可能的话，不要为多个客户的连接与服务器建立多个连接（即服务器支持持久的HTTP连接）。按照先进先出的原则为客户提供服务；当对前客户的响应传输完成后，再处理下一个客户。如果客户闲置时间过长（默认情况下最长为5秒），它将放弃等待，并打开另一个与服务器的连接。 |
| **src-address** (_Ip4 \| Ip6_; Default: **0.0.0.0**)                                             | 代理在连接上级代理或网站时将使用指定地址。如果设置为0.0.0.0，那么适当的IP地址将从路由表中获取。                                                                                                                                                               |

### 访问列表

`/ip/proxy/access`

访问列表的配置与普通防火墙规则一样。规则从上到下进行处理。第一个匹配规则指定决定如何处理这个连接。总共有6个分类器，指定匹配的约束条件。如果没有指定这些分类器，特定的规则将匹配每个连接。

如果一个连接被一个规则匹配，这个规则的动作属性就指定是否允许连接。如果特定的连接不匹配任何规则，它将被允许。

  
| Property                                                                                                    | Description                                                                                                 |
| ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **action** (_allow                                                            \| deny_; Default: **allow**) | 指定是通过还是拒绝匹配的数据包                                                                              |
| **dst-address** (_Ip4[-Ip4 \| /0..32] \| Ip6/0..128_; Default: )                                            | 目标服务器的目标地址。                                                                                      |
| **dst-host** (_string_; Default: )                                                                          | 用于与目标服务器建立连接的IP地址或DNS名称（这是用户在指定特定网页的端口和路径之前在浏览器中写入的字符串）。 |
| **dst-port** (_integer[-integer[,integer[,...]]]: 0...65535_; Default: )                                    | 数据包去往的端口列表或范围                                                                                  |
| **local-port** (_integer: 0...65535_; Default: )                                                            | 指定接收数据包的网络代理的端口。这个值应该与网络代理正在监听的端口之一相匹配。                              |
| **method** (_any \|\| delete\| get\| head \| options \| post \| put \| trace_; Default: )                   | 请求中使用的HTTP方法（见本文末尾的HTTP方法部分）                                                            |
| **path** (_string_; Default: )                                                                              | 目标服务器中被请求的页面的名称（即某一网页或文件的名称，但不包括其所在的服务器的名称）。                    |
| **redirect-to** (_string_; Default: )                                                                       | 如果此规则拒绝访问，用户将被重定向到这里指定的URL。                                                         |
| **src-address** (_Ip4[-Ip4 \| /0..32] \| Ip6/0..128_; Default: )                                            | 连接发起者的源地址。                                                                                        |

  
只读属性：

| 属性                 | 说明                 |
| -------------------- | -------------------- |
| **hits** (_integer_) | 此规则匹配的请求数量 |

  
通配符属性（dst-host和dst-path）匹配一个完整的字符串（即，如果设置为 "example"，将不会匹配 [example.com](http://example.com)）。可用的通配符是'*'（匹配任意数量的任意字符）和'?'（匹配任意一个字符）。这里也接受正则表达式，但如果该属性应被视为正则表达式，它应该以冒号（':'）开始。

使用正则表达式的小提示：

- \\\符号序列是用来在控制台中输入字符\\的；
- \\.pattern means. only （在正则表达式中，模式中的单点意味着任何符号）；
- 为了表明在给定的模式之前不允许有任何符号，在模式的开头使用^符号；
- 为了说明在给定的模式之后不允许有任何符号，在模式的结尾处使用$符号；
- 要输入 [or] 符号，应该用反斜杠"\\"转义；

强烈建议拒绝所有的IP地址，除了路由器后面的那些，因为代理仍然可能被用来访问只在内部使用的（intranet）Web服务器。另外，请参考《防火墙手册》中关于如何保护路由器的例子。

### 直接访问

`/ip/proxy/direct`

如果指定了parent-proxy属性，就可能告诉代理服务器是尝试将请求传递给父代理，还是通过直接连接到被请求的服务器来解决。直接访问列表的管理与前一章描述的代理访问列表一样，除了动作参数与访问列表不同，直接代理访问列表有一个默认的动作等于拒绝。当没有指定规则或某一请求不符合任何规则时，它就会起作用。

  

| 属性                                                                                                  | 说明                                                                                                                                                          |
| ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **action** (_allow \| deny_; Default: **allow**)                                                      | 指定对匹配的数据包进行的操作：<br>- 允许 - 始终绕过父级路由器直接解决匹配的请求<br>- deny - 通过父代理解决匹配的请求。如果没有指定，则与allow具有相同的效果。 |
| **dst-address** (_Ip4[-Ip4 \| /0..32] \| Ip6/0..128_; Default: )                                      | 目标服务器的目标地址。                                                                                                                                        |
| **dst-host** (_string_; Default: )                                                                    | 用于与目标服务器连接的IP地址或DNS名称（这是用户在指定端口和特定网页路径之前在浏览器中写的字符串）。                                                           |
| **dst-port** (_integer[-integer[,integer[,...]]]: 0..65535_; Default: )                               | List or range of ports used by connection to the target server.                                                                                               |
| **local-port** (_integer: 0..65535_; Default: )                                                       | 指定接收数据包的网络代理的端口。该值应与网络代理正在监听的端口之一相匹配。                                                                                    |
| **method** (_any \| connect \| delete \| get \| head \| options \| post \| put \| trace_; Default： ) | 请求中使用的HTTP方法(见本文末尾的 [HTTP方法](https://wiki.mikrotik.com/wiki/Manual:IP/Proxy#HTTP_Methods)部分)                                                |
| **path** (_string_; Default: )                                                                        | 目标服务器中被请求的页面名称（即某一网页或文档的名称，但不包括其所在的服务器名称）                                                                            | **src-address** (_string_; Default: ) |
| **src-address** (_Ip4[-Ip4 \| /0..32] \| Ip6/0..128_; Default: )                                      | 连接发起者的源地址。                                                                                                                                          |

  
只读属性：

| 属性                 | 说明               |
| -------------------- | ------------------ |
| **hits** (_integer_) | 规则匹配的请求数量 |

### 缓存管理

`/ip/proxy/cache`

缓存访问列表指定哪些请求（域、服务器、页面）必须由Web代理本地缓存，哪些不需要。这个列表的实现方式与网络代理访问列表完全相同。默认动作是缓存一个对象（如果没有找到匹配的规则）。

  
| 属性                                                                                                 | 说明                                                                                                   |
| ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **action** (_allow \| deny_; Default: **allow**)                                                     | 指定要对匹配的数据包执行的操作： <br>- allow - 缓存匹配请求中的对象<br>- deny - 不缓存匹配请求中的对象 |
| **dst-address** (_Ip4[-Ip4 \| /0..32] \| Ip6/0..128_; Default: )                                     | 目标服务器的目标地址                                                                                   |
| **dst-host** (_string_; Default: )                                                                   | 用于与目标服务器建立连接的IP地址或DNS名称（这是用户在指定端口和特定网页路径之前在浏览器中写的字符串）  |
| **dst-port** (_integer[-integer[,integer[,...]]]: 0...65535_; Default: )                             | 数据包所指向的端口列表或范围。                                                                         |
| **local-port** (_integer: 0...65535_; Default: )                                                     | 指定接收数据包的网络代理的端口。这个值应该与网络代理监听的端口之一相匹配。                             |
| **method** (_any \| connect \| delete \| get \| head \| options \| post \| put \| trace_; Default: ) | 请求中使用的HTTP方法（见本文末尾的HTTP方法部分）。                                                     |
| **path** (_string_; Default: )                                                                       | 目标服务器中被请求的页面名称（即某一网页或文件的名称，但不包括其所在服务器的名称）                     |
| **src-address** (_Ip4[-Ip4 \| /0..32] \| Ip6/0..128_; Default: )                                     | 连接发起者的源地址。                                                                                   |

  

只读属性：

| 属性                 | 说明                 |
| -------------------- | -------------------- |
| **hits** (_integer_) | 此规则匹配的请求数量 |

  

### 连接

`/ip/proxy/connections`

菜单包含代理正在服务的当前连接列表。

只读属性：

| 属性                                                                                                                                            | 说明                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **client** ()                                                                                                                                   |
| **dst-address** (_Ip4    \| Ip6_)                                                                                                               | 连接的IPv4/Ipv6目标地址                                                                                                                                                                                                                                                                                                                                                                                                           |
| **protocol** (_string_)                                                                                                                         | 协议名称                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **rx-bytes** (_integer_)                                                                                                                         | 客户端接收的字节数                                                                                                                                                                                                                                                                                                                                                                                                                |
| **server** ()                                                                                                                                   |
| **src-address** (_Ip4 \| Ip6_)                                                                                                                  | 连接发起者的IPv4/IPv6地址                                                                                                                                                                                                                                                                                                                                                                                                         |
| **state** (_closing      \| connecting \| converting\| hotspot \| idle \| resolving \| rx-header \| tx-body \| tx-eof \| tx-header \| waiting_) | 连接状态： <br>- 关闭 - 数据传输已经完成，连接正在结束<br>- 连接--建立脚趾连接<br>- 转换 - 替换响应或请求数据包中的头和脚字段<br>- 热点 - 检查热点认证是否允许继续（对于热点代理）<br>- 闲置--保持闲置<br>- 解析--解析服务器的DNS名称<br>- rx-header - 接收HTTP头<br>- tx-body--向客户端传输HTTP正文<br>- tx-eof - 写入chunk-end(当转换为chunked响应时)<br>- tx-header - 将HTTP头传输给客户端<br>- waiting - 等待来自对等体的传输 |
| **tx-bytes** (_integer_)                                                                                                                        | 客户端发送的字节数                                                                                                                                                                                                                                                                                                                                                                                                                |

  

### 缓存插入

`/ip/proxy/inserts`

这个菜单显示了存储在缓存中的对象的统计数据（缓存插入）。

只读属性：

| 属性                      | 说明                                 |
| ------------------------- | ------------------------------------ |
| **denied** (_integer_)    | 一些插入被缓存列表拒绝了。           |
| **errors** (_integer_)    | 磁盘或其他系统相关的错误数量         |
| **no-memory** (_integer_) | 没有足够的内存而没有存储的对象数量。 |
| **successes** (_integer_) | 成功插入缓存的数量。                 |
| **too-large** (_integer_) | 太大而无法存储的对象的数量。         |

### 缓存查找

`/ip/proxy/lookup`

这个菜单显示了从缓存中读取的对象的统计数据（缓存查询）。

只读属性：

| 属性                               | 说明                                                                           |
| ---------------------------------- | ------------------------------------------------------------------------------ |
| **denied** (_integer_)             | 被访问列表拒绝的请求的数量。                                                   |
| **expired** (_integer_)            | 在缓存中发现的请求数，但已经过期，因此，从外部服务器请求。                     |
| **no-expiration-info** (_integer_) | 收到的有条件的请求，该页面没有信息，无法与请求进行比较。                       |
| **non-cacheable** (_integer_)      | 从外部服务器无条件请求的数量（因为缓存被访问列表拒绝了）。                     |
| **not-found** (_integer_)          | 在缓存中未找到的请求，因此从外部服务器（或父级代理，如果相应配置）请求的数量。 |
| **successes** (_integer_)          | 缓存中找到的请求数。                                                           |

### 缓存内容

`/ip/proxy/cache-contents`

该菜单显示缓存的内容。


只读属性：

| 属性                            | 说明           |
| ------------------------------- | -------------- |
| **file-size** (_integer_)       | 缓存对象的大小 |
| **last-accessed** (_time_)      |                |
| **last-accessed-time** (_time_) |                |
| **last-modified** (_time_)      |                |
| **last-modified-time** (_time_) |                |
| **uri** (_string_)              |                |

  

# HTTP方法

#### 选项

该方法是对客户和Request-URI所确定的服务器之间的链上可用的通信选项信息的请求。该方法允许客户端确定选项和（或）与资源相关的要求，而无需启动任何资源检索。

#### GET

该方法检索由Request-URI确定的任何信息。如果Request-URI指的是一个数据处理过程，那么对GET方法的响应应该包含该过程产生的数据，而不是过程的源代码（-s），除非源代码是该过程的结果。

如果请求信息包括If-Modified-Since、If-Unmodified-Since、If-Match、If-None-Match或If-Range头域，GET方法可以成为有条件的GET。有条件的GET方法被用来减少网络流量，指定实体的传输应该只在有条件的头域（-s）描述的情况下发生。

如果请求信息包括一个范围头字段，GET方法可以成为部分GET。部分GET方法旨在通过只请求实体的部分内容而不传输客户端已经持有的数据来减少不必要的网络使用。

当且仅当GET请求的响应满足HTTP缓存的要求时，它是可缓存的。

#### HEAD

这个方法共享GET方法的所有特征，除了服务器必须在响应中不返回消息体。它检索了请求所暗示的实体的元信息，这导致它被广泛用于测试超文本链接的有效性、可访问性和最近的修改。

对HEAD请求的响应可能是可缓存的，因为响应中包含的信息可能被用来更新先前由该Request-URI识别的缓存实体。

#### POST

这个方法请求源服务器接受请求中所包含的实体作为Request-URI所标识的资源的新下级。

POST方法所执行的实际操作由源服务器决定，通常与Request-URI有关。

对POST方法的响应是不可缓存的，除非该响应包括适当的Cache-Control或Expires头域。

#### PUT

该方法请求将所附实体存储在所提供的Request-URI下。如果在指定的Request-URI下存在另一个实体，那么所包含的实体应该被认为是驻留在源服务器上的一个更新（较新）的版本。如果Request-URI没有指向一个现有的资源，起源服务器应该用该URI创建一个资源。

如果请求通过了缓存，并且Request-URI标识了一个或多个当前缓存的实体，这些条目应该被视为过时的。对这种方法的响应是不可缓存的。

#### TRACE

这个方法调用了一个远程的、应用层的请求消息的回环。请求的最终接收者应该将收到的消息作为200（OK）响应的实体主体反馈给客户端。最终接收者是原服务器或在请求中收到Max-Forwards值为0的第一个代理或网关。TRACE请求必须不包括实体。

对该方法的响应不得被缓存。