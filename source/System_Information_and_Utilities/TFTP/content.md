# 介绍

简单文件传输协议(Trivial File Transfer Protocol，简称TFTP)是一个用于传输文件的非常简单的协议。每个非终端包分别被确认。

`ip/tftp/`

该菜单包含所有TFTP访问规则。如果该菜单中没有任何规则，则表示在RouterOS启动时不启动TFTP服务器。与创建规则时可以设置的属性相比，该菜单只显示一个额外的属性。

# 参数

| 属性                              | 说明                                                                                                                                                                                                                                                                       |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ip-address** _(required)_       | 如果为空，将使用0.0.0.0/0作为客户端接受的IP地址范围                                                                                                                                                                                                                        |
| **allow-rollover** _(default:No)_ | 如果设置为yes TFTP服务器将允许序列号在达到最大值时滚转。这用于使用TFTP服务器启用大型下载。                                                                                                                                                                                 |
| **req-filename**                  | 请求的文件名为正则表达式(regex)，如果字段为空，则默认为.*                                                                                                                                                                                                                  |
| **real-filename**                 | 如果设置了 **req-filename** 和 **real-filename** 值并且有效，则请求的文件名将被替换为匹配的文件。这个字段必须设置。如果在req-filename_指定了多个regex，则可以使用该字段设置应该匹配哪些regex，从而验证该规则。使用多个_regex_的_real-filename_格式是 **filename\\0\\5\\6** |
| **allow** (_default: yes_)        | 如果设置了以上字段，则允许连接。如果为no，连接将中断                                                                                                                                                                                                                       |
| **read-only** (_default: no_)     | 设置文件是否可以写入，如果设置为“yes”，则写入尝试将失败并出现错误                                                                                                                                                                                                          |
| **hits** _(read-only)_            | 这个访问规则项被使用了多少次(只读)                                                                                                                                                                                                                                         |

## 设置

`/ip/tftp/settings`

该菜单包含了所有TFTP的设置

| 属性                                | 说明                                                                     |
| ----------------------------------- | ------------------------------------------------------------------------ |
| **max-block-size** (_default:4096_) | 可接受的最大块大小值。在传输协商阶段，RouterOS设备不会协商大于该值的值。 |

# Regexp

Req-filename字段允许的regexp，该字段允许的regexp有:

**()** 标记分段:

```
    example 1 a(sd|fg) will match asd or afg

```

**\*** 匹配0次或多次前面的符号:

```
    example 1 a* will match any length name consisting purely of symbols a or no symbols at all
    example 2 .* will match any length name, also, empty field
    example 3 as*df will match adf, asdf, assdf, asssdf etc.

```

**+** 将与前面的符号匹配一次或多次:

```
    example: as+df will match asdf, assdf etc.

```

**.** 匹配任意符号:

```
    example as.f will match asdf, asbf ashf etc.

```

**[]** - variation between:

```
    example as[df] will match asd and asf

```

**?** 匹配一个或不匹配符号:

```
    example asd?f will match asdf and asf

```

**^** 表示该行的开头

**$** 表示该行的结尾

# 例子

如果请求了一个文件，则从名为sata1的存储区返回该文件:

`/ip tftp add req-filename=file.txt real-filename=/sata1/file.txt allow=yes read-only=yes`

如果不管用户请求什么都给出一个特定的文件:

`/ip tftp add req-filename=.* real-filename=/sata1/file.txt allow=yes read-only=yes`

如果用户请求aaa.bin或bbb.bin，则给他们ccc.bin:

```shell
/ip tftp add req-filename="(aaa.bin)|(bbb.bin)" real-filename="/sata1/ccc.bin\\0" allow=yes read-only=yes
```
  

RouterOS收到TFTP请求，客户端传输超时?

一些嵌入式客户端请求较大的块大小，但不能正确处理碎片包。对于这些客户端，建议将RouterOS端的“max-block-size”或客户端的“blksize”设置为网络上最小的MTU值减去32字节(IP为20字节，UDP为8字节，TFTP为4字节)，如果您在网络上使用IP选项，则建议设置为更大的值。