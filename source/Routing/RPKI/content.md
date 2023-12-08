<!--
 * @Author: be-engineer 41234995@qq.com
 * @Date: 2023-05-16 17:31:38
 * @LastEditors: be-engineer 41234995@qq.com
 * @LastEditTime: 2023-05-19 23:04:43
 * @FilePath: /MikroTik-doc-cn/source/Routing/RPKI/content.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# 概述

RouterOS实现了 [RFC8210](https://tools.ietf.org/html/rfc8210) 中定义的到路由器协议的RPKI (Resource Public Key Infrastructure)。RTR是一种非常轻量级的低内存占用协议，用于从RPKI验证器可靠地获取前缀验证数据。
关于RPKI和如何设置验证器的更多信息可以在RIPE博客中找到:
[https://blog.apnic.net/2019/10/28/how-to-installing-an-rpki-validator/](https://blog.apnic.net/2019/10/28/how-to-installing-an-rpki-validator/)

# 基本示例

假设网络上有自己的RTR服务器，IP地址为192.168.1.1:

`/routing/bgp/rpki
add group=myRpkiGroup address=192.168.1.1 port=8282 refresh-interval=20`

如果连接建立，并且从验证器接收到数据库，可以检查前缀的有效性:

```shell
[admin@rack1_b33_CCR1036] /routing> rpki-check group=myRpkiGroup prfx=70.132.18.0/24 origin-as=16509
    valid
```

现在，路由过滤器可以使用缓存的数据库来根据RPKI有效性接受拒绝前缀。首先需要设置一个过滤器规则，该规则定义哪个RPKI组执行验证。之后，过滤器准备好匹配来自RPKI数据库的状态。Status可以有三个值:

- **valid** -数据库中有记录且原始AS有效。
- **invalid** -数据库中有记录，源AS无效。
- **unknown** -数据库中没有前缀AS和原始AS的信息。
- **unverified** -当RPKI组的所有RPKI会话都没有同步过数据库时设置。此值可用于处理RPKI的总故障。

```shell
/routing/filter/rule
add chain=bgp_in rule="rpki-verify myRpkiGroup"
add chain=bgp_in rule="if (rpki invalid) { reject } else { accept }"
```

# 配置选项

**Sub-Menu:** `/routing/rpki`
 

| 属性                                                       | 说明                                                                |
| ---------------------------------------------------------- | ------------------------------------------------------------------- |
| **address** (_IPv4/6_) mandatory                           | RTR服务器地址                                                       |
| **disabled**(_yes\| no_;Default:**no**)                    | 是否忽略该项。                                                      |
| **expire-interval** (_integer [600..172800]_;Default:7200) | 时间间隔[s]轮询数据在验证器没有进行有效的后续更新时被认为是有效的。 |
| **group** (_string_) mandatory                             | 数据库被分配给的组名。                                              |
| **port** (_integer [0..65535]_;Default:323)                | 连接端口号                                                          |
| **preference** (_integer [0..4294967295]_;Default:0)       | 如果有多个RTR源，则优先级号表示更优先的RTR源。越少越好。            |
| **refresh-interval** (_integer [1..86400]_;Default:3600)   | 从验证器轮询最新数据的时间间隔[s]                                   |
| **retry-interval** (_integer [1..7200]_;Default:600)       | 验证器轮询失败后重试的时间间隔[s]。                                 |
| **vrf** (_name_;Default:main)                              | 用于绑定连接的VRF表名。                                             |