# 概述

可编程接口（API）允许用户创建自定义的软件解决方案，与RouterOS通信，以收集信息、调整配置和管理路由器。API严格遵循命令行界面（CLI）的语法。它可以用来创建翻译或定制的配置工具，以帮助方便使用RouterOS运行和管理路由器。

在尝试建立API连接之前，必须先启用API服务。默认情况下，API使用TCP: _8728_ 和TCP: _8729_（安全）。 

API-ssl服务能够以两种模式工作-有证书和无证书。如果在 _/ip service_ 设置中没有使用证书，那么必须使用匿名的Diffie-Hellman密码来建立连接。如果使用了证书，就可以建立TLS会话。

## 协议

与路由器的通信是通过发送句子和接收一个或多个句子作为回应完成的。句子是一个由零长度的字终止的字序列。字是以某种方式编码的句子的一部分--编码的长度和数据。通信是通过向路由器发送句子和接收对句子的回复来实现的。使用API发送给路由器的每个句子应该包含一个命令作为第一个词，后面是没有特定顺序的词，句子的结尾由一个零长度的词来标记。当路由器收到一个完整的句子（命令词，没有或更多的属性词，以及零长度的词），它被评估和执行，然后形成一个回复并返回。

### API词

词是句子的一部分。每个单词都必须以一定的方式进行编码-单词长度，然后是单词的内容。词的长度应该以将要发送的字节数的形式给出。

词的长度的编码方式如下：

| 值长度                       | 字节数 | 编码                       |
| ---------------------------- | ------ | -------------------------- |
| 0 <= len <= 0x7F             | 1      | len, lowest byte           |
| 0x80 <= len <= 0x3FFF        | 2      | len                        | 0x8000, two lower bytes     |
| 0x4000 <= len <= 0x1FFFFF    | 3      | len                        | 0xC00000, three lower bytes |
| 0x200000 <= len <= 0xFFFFFFF | 4      | len                        | 0xE0000000                  |
| len >= 0x10000000            | 5      | 0xF0 and len as four bytes |

 
- 每个词都被编码为长度，后面有很多字节的内容；
- 单词被分组到句子。句子的结尾是由零长度的字来结束；
- 该方案允许将长度编码到 **0x7FFFFFFFFF**，只支持四字节长度；
- **len** 字节先发送最重要的字节（按网络顺序）；
- 如果字的第一个字节是 **>=0xF8**，那么就是一个保留控制字节。在收到未知的控制字节后，API客户端无法继续，因为不知道如何解释下面的字节；
- 目前控制字节不使用；

一般来说，_字_ 可以这样描述《编码的字长》《字内容》。字内容可以分成5个部分： [命令词](https://help.mikrotik.com/docs/display/ROS/API#API-heading-Commandword), [属性词](https://help.mikrotik.com/docs/display/ROS/API#API-heading-Attributeword), [API属性词](https://help.mikrotik.com/docs/display/ROS/API#API-heading-APIattributeword). [查询词](https://help.mikrotik.com/docs/display/ROS/API#API-heading-Queryword),和 [回复词](https://help.mikrotik.com/docs/display/ROS/API#API-heading-Replyword)。

#### 命令词

句子中的第一个词必须是命令，后面是属性词和一个零长度的词或终止词。命令词的名称应该以'/'开头。命令的名称紧跟CLI，空格用'/'代替。有一些命令是专门针对API的；

命令词结构严格按照顺序排列：

- 编码长度
- 内容前缀 /
- CLI转换的命令
  
API特定命令：

```
login
cancel

```

命令词示例：

```
/login

```

```
/user/active/listen

```

```
/interface/vlan/remove

```

```
/system/reboot

```

#### 属性词

每个 _命令词_ 都有自己的 _属性词_ 列表，取决于内容。

_属性词_ 结构由5个部分组成，顺序如下：

- 编码长度
- 内容前缀等号 - _COPY=_
- 属性名称
- 分开的等号 - _=_
- 如果有一个属性的值的话。属性有可能没有值

由于字的编码方式，值可以在 _属性字的值中持有多个_ 等号。

值可以是空的。

没有编码的长度前缀的例子：

```
=address=10.0.0.1

```

```
=name=iu=c3Eeg

```

```
=disable-running-check=yes

```

  

属性词和API参数的顺序并不重要，不应依赖。

#### API属性词

API属性词的结构是按照严格的顺序：

- 编码长度
- 内容前缀为点 _._
- 属性名称
- 名称后缀为等号 _=_
- 属性值

目前，唯一这样的API属性是 _tag_。

如果句子包含一个 _API属性词_ 标签，那么从路由器返回的每个句子都会被标记为相同的标签。

#### 查询词

句子可以有额外的查询参数来限制其范围。详细解释在 [查询部分](https://help.mikrotik.com/docs/display/ROS/API#API-heading-Queries)。

使用查询词属性的例子：

```
/interface/print
?type=ether
?type=vlan
?#|!

```

- 查询词以"?"开头。
- 目前，只有 _print_ 命令处理查询词。

查询词的顺序是很重要的

#### 回复词

它只由路由器在回应从客户端收到的完整句子时发送。

- 回复词的第一个字以!开头；
- 每个句子的发送都会产生至少一个回复（如果连接没有被终止）；
- 每个句子的最后一个回复是有第一个字!done的那个回复；
- 错误和特殊情况以!Trap开头；
- 数据回复以!re开头
- 如果API连接被关闭，RouterOS会发送带有原因的!fatal作为回复，然后关闭连接；

### API句子

API句子是使用API进行通信的主要对象。

- 空的句子会被忽略。
- 句子在收到零长度的单词后被处理。
- 客户端在登录之前可以发送的句子的数量和大小是有限制的。
- 属性词的顺序不应该被依赖。因为顺序和数量是可以通过 _.proplist_ 属性改变的。
- 句子结构如下：
    - 第一个词应包含一个 _命令词_；
    - 应包含 _零长度的词_ 来终止句子；
    - 可以不包含或包含几个 _属性词_。属性词在句子中的发送顺序没有特别规定，顺序对 _属性词_ 来说并不重要；
    - 可以不包含或包含几个 _查询词_。句子中的_查询词_的顺序很重要。

零长度词是句子的终点。如果没有提供这个词，路由器将不评估发送的词，并将所有的输入视为同一个句子的一部分。

## 初始登录

**注意：** 每个命令和响应都以一个空字结束。

v6.43之后的登录方法：

`/login
=name=admin
=password=
 !done`
 
- 现在，客户在第一条信息中发送一个用户名和密码。
- 密码是以纯文本形式发送的。
- 如果出现错误，回复中包含 =message= error message。
- 在登录成功的情况下，客户端可以开始发布命令。

## 标签

- 可以同时运行几个命令，而不等待前一个命令的完成。如果API客户端这样做，并且需要区分命令响应，它可以在命令句子中使用 'tag' API参数。
- 如果你在命令句子中包含了具有非空值的 'tag' 参数，那么具有完全相同值的 'tag' 参数将被包含在这个命令产生的所有响应中。
- 如果你不包括'tag'参数或其值为空，那么这个命令的所有响应将没有 'tag' 参数。

## 命令描述

- /cancel
    - 可选参数：=tag=要取消的命令标签，没有它，会取消所有正在运行的命令。
    - 不会取消自己
    - 所有被取消的命令都会被打断，在通常情况下会产生"！陷阱 "和"！完成 "的响应。
    - 请注意，/cancel是单独的命令，可以有它自己独特的".tag "参数，与本命令的"=tag "参数无关。

- 听
    - 在有控制台打印命令的地方可以使用listen命令，但它并不是在所有地方都有预期的效果（也就是说，可能无法工作）。
    - 当某一项目列表中的某些内容发生变化时，会产生"！re "句子
    - 当一个项目被删除或以任何其他方式消失时，'！re'句子包括'=.dead=yes'的值。
    - 这个命令不会终止。要终止它，请使用/cancel命令。

- getall
    - getall命令在有控制台打印命令的地方可用（getall是print的一个别名）。
    - 回复包含=.id=_Item internal number_属性。

- 打印
    - API打印命令在以下方面与控制台的对应命令不同：
        - 在一个参数不被支持的地方。项目可以使用查询词进行过滤（见下文）。
        - .proplist参数是一个逗号分隔的属性名称列表，应该包括返回的项目。
            - 返回的项目可能有额外的属性。
            - 没有定义返回属性的顺序。
            - 如果一个列表中包含重复的条目，对这些条目的处理没有被定义。
            - 如果一个属性出现在".proplist "中，但没有出现在项目中，那么该项目就没有这个属性值（?name对该项目来说将评估为false）。
            - 如果".proplist "不存在，那么所有的属性都会按照打印命令的要求包括在内，即使是那些访问时间较慢的属性（如文件内容和性能计数器）。因此，我们鼓励使用.proplist。如果设置了"=detail="参数，省略.proplist可能会产生高性能的惩罚。

### 查询

print命令接受限制返回句子集的查询词。 

- 查询词以"？"开头。
- 查询词的顺序很重要。一个查询从第一个词开始评估。
- 对列表中的每个项目都要进行查询。如果查询成功，该项目被处理，如果查询失败，该项目被忽略。
- 一个查询是用一个布尔值的堆栈来评估的。最初，堆栈包含无限量的 "真 "值。在评估结束时，如果堆栈中至少有一个 "假 "值，则查询失败。
- 查询词按照以下规则操作：

| 查询               | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **?name**          | 如果一个项目有属性 _name_ 值，则推送'true'，如果没有则推送'false'。                                                                                                                                                                                                                                                                                                                                                                                               |
| **?-name**         | 如果一个项目没有属性 _name_ 值，则推送'true'，否则推送'false'。                                                                                                                                                                                                                                                                                                                                                                                                   |
| **?_name_=_x_**    | **?                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **?=_name_=_x_**   | 如果属性 _name_ 的值等于 _x_，则推送'true'，否则推送'false'。                                                                                                                                                                                                                                                                                                                                                                                                     |
| **?<name=_x_**     | 如果属性 _name_ 的值小于 _x_，则推送'true'，否则推送'false'。                                                                                                                                                                                                                                                                                                                                                                                                     |
| **?>name=_x_**     | 如果属性 _name_ 的值大于 _x_，则推送'true'，否则推送'false'。                                                                                                                                                                                                                                                                                                                                                                                                     |
| **?#_operations_** | 将操作用于堆栈中的值。<br>- 操作字符串从左到右进行评估。<br>- 小数点后的任何其他字符或字尾的序列被解释为堆栈索引。 最上面的值有索引0。<br>- 后面是一个字符的索引，推送该索引的值的副本。<br>- 后面是字尾的索引，用该索引的值替换所有的值。<br>- **!** 字符用相反的值替换顶部的值。<br>- & 弹出两个值并推送逻辑 "和 "操作的结果。<br>- \| 弹出两个值，并推送逻辑 "或 "操作的结果。<br>- . 在一个索引之后不做任何事情。<br>- . 在另一个字符后推送一个顶层值的副本。 |

  

API中不支持正则表达式，所以不要用 **~** 符号来查询。
 
例子：

- 获取所有以太网和VLAN接口：

```
/interface/print
?type=ether
?type=vlan
?#|

```

- 获取所有非空注释的路由：

```
/ip/route/print
?>comment=

```

-   [论坛主题，对查询的使用进行了详细解释](http://forum.mikrotik.com/viewtopic.php?f=2&t=72298)

### OID

打印命令可以返回SNMP中可用的属性的OID值。 

在控制台中，OID值可以通过运行'print oid'命令看到。在API中，这些属性的名称以".oid "结尾，可以把名称添加到'.proplist'的值中来检索。例子如下：

```shell
/system/resource/print
=.proplist=uptime,cpu-load,uptime.oid,cpu-load.oid
 !re
=uptime=01:22:53
=cpu-load=0
=uptime.oid=.1.3.6.1.2.1.1.3.0
=cpu-load.oid=.1.3.6.1.2.1.25.3.3.1.2.1

 !done
!trap
```

### !trap

当某些原因导致API句子失败时，陷阱就会被送回，并伴随着 **消息** 属性，在某些情况下还会有 **类别** 参数。

#### 消息

当一个API句子失败时，会返回一些通用信息或来自所使用的内部程序的信息以提供关于失败的更多细节。

```shell
<<< /ip/address/add
<<< =address=192.168.88.1
<<< =interface=asdf <<<
 
>>> !trap
>>> =category=1
>>> =message=input does not match any value of interface
```

#### 类别

如果是一般的错误，就会被分类，并返回错误类别。这个属性的值有

- 0 - 缺少项目或命令
- 1 - 参数值失败
- 2 - 命令的执行被打断
- 3 - 与脚本有关的失败
- 4 - 一般性故障
- 5--与API相关的故障
- 6-与TTY相关的故障
- 7 - 用:return命令生成的值

## 命令实例

### /system/package/getall

```shell
/system/package/getall

 !re
=.id=*5802
=disabled=no
=name=routeros-x86
=version=3.0beta2
=build-time=oct/18/2006 16:24:41
=scheduled=

 !re
=.id=*5805
=disabled=no
=name=system
=version=3.0beta2
=build-time=oct/18/2006 17:20:46
=scheduled=

... more !re sentences ...
 !re
=.id=*5902
=disabled=no
=name=advanced-tools
=version=3.0beta2
=build-time=oct/18/2006 17:20:49
=scheduled=

 !done

```

### /user/active/listen

```shell
/user/active/listen

 !re
=.id=*68
=radius=no
=when=oct/24/2006 08:40:42
=name=admin
=address=0.0.0.0
=via=console

 !re
=.id=*68
=.dead=yes

... more !re sentences ...
```

### /cancel, simultaneous commands

```shell
/login

 !done
=ret=856780b7411eefd3abadee2058c149a3

/login
=name=admin
=response=005062f7a5ef124d34675bf3e81f56c556

 !done
-- first start listening for interface changes (tag is 2)
/interface/listen
.tag=2
-- disable interface (tag is 3)
/interface/set
=disabled=yes
=.id=ether1
.tag=3
-- this is done for disable command (tag 3)
 !done
.tag=3

-- enable interface (tag is 4)
/interface/set
=disabled=no
=.id=ether1
.tag=4
-- this update is generated by change made by first set command (tag 3)
 !re
=.id=*1
=disabled=yes
=dynamic=no
=running=no
=name=ether1
=mtu=1500
=type=ether
.tag=2

-- this is done for enable command (tag 4)
 !done
.tag=4

-- get interface list (tag is 5)
/interface/getall
.tag=5

-- this update is generated by change made by second set command (tag 4)
 !re
=.id=*1
=disabled=no
=dynamic=no
=running=yes
=name=ether1
=mtu=1500
=type=ether
.tag=2

-- these are replies to getall command (tag 5)
 !re
=.id=*1
=disabled=no
=dynamic=no
=running=yes
=name=ether1
=mtu=1500
=type=ether
.tag=5

 !re
=.id=*2
=disabled=no
=dynamic=no
=running=yes
=name=ether2
=mtu=1500
=type=ether
.tag=5

-- here interface getall ends (tag 5)
 !done
.tag=5

-- stop listening - request to cancel command with tag 2, cancel itself uses tag 7
/cancel
=tag=2
.tag=7

-- listen command is interrupted (tag 2)
 !trap
=category=2
=message=interrupted
.tag=2

-- cancel command is finished (tag 7)
 !done
.tag=7

-- listen command is finished (tag 2)
 !done
.tag=2
```

## 客户端实例

一个简单的 [Python3中的API客户端](https://help.mikrotik.com/docs/display/ROS/Python3+Example)

输出示例：

```shell
debian@localhost:~/api-test$ ./api.py 10.0.0.1 admin ''
<<< /login
<<<
>>> !done
>>> =ret=93b438ec9b80057c06dd9fe67d56aa9a
>>>
<<< /login
<<< =name=admin
<<< =response=00e134102a9d330dd7b1849fedfea3cb57
<<<
>>> !done
>>>
/user/getall
 
<<< /user/getall
<<<
>>> !re
>>> =.id=*1
>>> =disabled=no
>>> =name=admin
>>> =group=full
>>> =address=0.0.0.0/0
>>> =netmask=0.0.0.0
>>>
>>> !done
>>>
```

```

```

## 参见

### API examples

不同语言的API实现，由不同来源提供。不以特定顺序排列。

-   [in Python3](https://help.mikrotik.com/docs/display/ROS/Python3+Example) by MikroTik
-   [in .NET (C#) high-level API solution](https://github.com/danikf/tik4net) [forum thread](http://forum.mikrotik.com/viewtopic.php?f=9&t=99954) [additional info](https://github.com/danikf/tik4net/wiki) by danikf
-   [in PHP](https://sourceforge.net/projects/netrouteros/) by boen_robot
-   [in C](https://github.com/haakonnessjoen/librouteros-api) by Håkon Nessjøen
-   [in Java](https://github.com/GideonLeGrange/mikrotik-java) by Gideon LeGrange
-   [in Erlang](https://github.com/comtihon/erotik) by Valery Comtihon
-   [in GO](https://github.com/go-routeros/routeros) by André Luiz dos Santos
-   [in Python3](https://github.com/LaiArturs/RouterOS_API) by Arturs Laizans
-   [in C++17](https://github.com/aymanalqadhi/tikpp) by Ayman Al-Qadhi