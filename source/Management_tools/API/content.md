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

一般来说，_字_可以这样描述《编码的字长》《字内容》。字内容可以分成5个部分： [命令词](https://help.mikrotik.com/docs/display/ROS/API#API-heading-Commandword), [属性词](https://help.mikrotik.com/docs/display/ROS/API#API-heading-Attributeword), [API属性词](https://help.mikrotik.com/docs/display/ROS/API#API-heading-APIattributeword). [查询词](https://help.mikrotik.com/docs/display/ROS/API#API-heading-Queryword),和[回复词](https://help.mikrotik.com/docs/display/ROS/API#API-heading-Replyword)。

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
- 属性词的顺序不应该被依赖。因为顺序和数量是可以通过_.proplist_属性改变的。
- 句子结构如下：
    - 第一个词应包含一个 _命令词_；
    - 应包含 _零长度的词_ 来终止句子；
    - 可以不包含或包含几个 _属性词_。属性词在句子中的发送顺序没有特别规定，顺序对_属性词_来说并不重要；
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
- 如果出现错误，回复中包含=message= _error message_。
- 在登录成功的情况下，客户端可以开始发布命令。

## 标签

- 可以同时运行几个命令，而不等待前一个命令的完成。如果API客户端这样做，并且需要区分命令响应，它可以在命令句子中使用 'tag' API参数。
- 如果你在命令句子中包含了具有非空值的 'tag' 参数，那么具有完全相同值的 'tag' 参数将被包含在这个命令产生的所有响应中。
- 如果你不包括'tag'参数或其值为空，那么这个命令的所有响应将没有 'tag' 参数。

## Command description

-   /cancel
    -   optional argument: =tag=_tag of command to cancel_, without it, cancels all running commands
    -   does not cancel itself
    -   all canceled commands are interrupted and in the usual case generate '!trap' and '!done' responses
    -   please note that /cancel is separate command and can have it's own unique '.tag' parameter, that is not related to '=tag' argument of this command

-   listen
    -   listen command is available where console print command is available, but it does not have expected effect everywhere (i.e. may not work)
    -   "!re" sentences are generated as something changes in a particular item list
    -   when an item is deleted or disappears in any other way, the '!re' sentence includes the value '=.dead=yes'
    -   This command does not terminate. To terminate it, use /cancel command.

-   getall
    -   getall command is available where console print command is available (getall is an alias for print).
    -   replies contain =.id=_Item internal number_ property.

-   print
    -   API print command differs from the console counterpart in the following ways:
        -   where an argument is not supported. Items can be filtered using query words (see below).
        -   .proplist argument is a comma-separated list of property names that should be included for the returned items.
            -   returned items may have additional properties.
            -   order of returned properties is not defined.
            -   if a list contains duplicate entries, handling of such entries is not defined.
            -   if a property is present in ".proplist", but absent from the item, then that item does not have this property value (?name will evaluate to false for that item).
            -   if ".proplist" is absent, all properties are included as requested by print command, even those that have slow access time (such as file contents and performance counters). Thus the use of .proplist is encouraged. The omission of .proplist may have a high-performance penalty if the "=detail=" argument is set.

### Queries

The print command accepts query words that limit the set of returned sentences. 

-   Query words begin with '?'.
-   The order of query words is significant. A query is evaluated starting from the first word.
-   A query is evaluated for each item in the list. If the query succeeds, the item is processed, if a query fails, the item is ignored.
-   A query is evaluated using a stack of boolean values. Initially, the stack contains an infinite amount of 'true' values. At the end of the evaluation, if the stack contains at least one 'false' value, the query fails.
-   Query words operate according to the following rules:

|

Query

 | 

Description

 |                    |
 | ------------------ | ------------------------------------------------------------------------------------- |
 | **?name**          | pushes 'true' if an item has a value of property _name_, 'false' if it does not.      |
 | **?-name**         | pushes 'true' if an item does not have a value of property _name_, 'false' otherwise. |
 | **?_name_=_x_**    |
 | **?=_name_=_x_**   | pushes 'true' if the property _name_ has a value equal to _x_, 'false' otherwise.     |
 | **?<name=_x_**     | pushes 'true' if the property _name_ has a value less than _x_, 'false' otherwise.    |
 | **?>name=_x_**     | pushes 'true' if the property _name_ has a value greater than _x_, 'false' otherwise. |
 | **?#_operations_** | applies operations to the values in the stack.                                        |

-   operation string is evaluated left to right.
-   the sequence of decimal digits followed by any other character or end of the word is interpreted as a stack index. top value has index 0.
-   an index that is followed by a character pushes a copy of the value at that index.
-   an index that is followed by the end of the word replaces all values with the value at that index.
-   **!** character replaces the top value with the opposite.
-   **&** pops two values and pushes the result of logical 'and' operation.
-   **|** pops two values and pushes the result of logical 'or' operation.
-   **.** after an index does nothing.
-   **.** after another character pushes a copy of the top value.

 |

  

Regular expressions are not supported in API, so do not try to send a query with the **~** symbol

  

Examples:

-   Get all ethernet and VLAN interfaces:

```
/interface/print
?type=ether
?type=vlan
?#|

```

-   Get all routes that have a non-empty comment:

```
/ip/route/print
?>comment=

```

-   [Forum thread with a detailed explanation of the use of queries](http://forum.mikrotik.com/viewtopic.php?f=2&t=72298)

### OID

The print command can return OID values for properties that are available in SNMP. 

In console, OID values can be seen by running 'print oid' command. In API, these properties have name that ends with ".oid", and can be retrieved by adding their name to the value of '.proplist'. An example:

<table class="relative-table wrapped confluenceTable" style="width: 91.2207%;"><colgroup><col style="width: 99.9925%;"></colgroup><tbody><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">/system/resource/print</td></tr><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">=.proplist=uptime,cpu-load,uptime.oid,cpu-load.oid</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!re</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=uptime=01:22:53</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=cpu-load=0</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=uptime.oid=.1.3.6.1.2.1.1.3.0</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=cpu-load.oid=.1.3.6.1.2.1.25.3.3.1.2.1</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!done</td></tr></tbody></table>

### !trap

When for some reason API sentence fails trap is sent in return accompanied with **message** attribute and on some occasions **category** argument.

#### message

When an API sentence fails, some generic message or message from the used internal process is returned to give more details about the failure

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">&lt;&lt;&lt; /ip/address/add</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text plain">&lt;&lt;&lt; =address=192.168.88.1</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="text plain">&lt;&lt;&lt; =interface=asdf &lt;&lt;&lt;</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="text plain">&gt;&gt;&gt;&nbsp;!trap</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="text plain">&gt;&gt;&gt; =category=1</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="text plain">&gt;&gt;&gt; =message=input does not match any value of interface</code></div></div></td></tr></tbody></table>

  

#### category

if it is a general error, it is categorized and the error category is returned. possible values for this attribute are

-   0 - missing item or command
-   1 - argument value failure
-   2 - execution of command interrupted
-   3 - scripting related failure
-   4 - a general failure
-   5 - API related failure
-   6 - TTY related failure
-   7 - value generated with :return command

## Command examples

### /system/package/getall

<table class="relative-table wrapped confluenceTable" style="text-decoration: none;width: 91.6416%;"><colgroup><col style="width: 99.9831%;"></colgroup><tbody><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">/system/package/getall</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!re</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=.id=*5802</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=disabled=no</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=name=routeros-x86</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=version=3.0beta2</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=build-time=oct/18/2006 16:24:41</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=scheduled=</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!re</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=.id=*5805</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=disabled=no</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=name=system</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=version=3.0beta2</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=build-time=oct/18/2006 17:20:46</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=scheduled=</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">... more&nbsp;!re sentences ...</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!re</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=.id=*5902</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=disabled=no</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=name=advanced-tools</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=version=3.0beta2</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=build-time=oct/18/2006 17:20:49</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=scheduled=</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!done</td></tr><tr><td class="confluenceTd"><br></td></tr></tbody></table>

### /user/active/listen

<table class="relative-table wrapped confluenceTable" style="text-decoration: none;width: 91.6416%;"><colgroup><col style="width: 99.9831%;"></colgroup><tbody><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">/user/active/listen</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!re</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=.id=*68</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=radius=no</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=when=oct/24/2006 08:40:42</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=name=admin</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=address=0.0.0.0</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=via=console</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!re</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=.id=*68</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=.dead=yes</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">... more&nbsp;!re sentences ...</td></tr></tbody></table>

### /cancel, simultaneous commands

<table class="relative-table wrapped confluenceTable" style="text-decoration: none;width: 91.5815%;"><colgroup><col style="width: 99.9887%;"></colgroup><tbody><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">/login</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!done</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=ret=856780b7411eefd3abadee2058c149a3</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">/login</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=name=admin</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=response=005062f7a5ef124d34675bf3e81f56c556</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!done</td></tr><tr><td class="highlight-#c1c7d0 confluenceTd" data-highlight-colour="#c1c7d0" title="Background colour : Medium grey 45%">-- <em title="">first start listening for interface changes (tag is 2)</em></td></tr><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">/interface/listen</td></tr><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">.tag=2</td></tr><tr><td class="highlight-#c1c7d0 confluenceTd" data-highlight-colour="#c1c7d0" title="Background colour : Medium grey 45%">-- <em title="">disable interface (tag is 3)</em></td></tr><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">/interface/set</td></tr><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">=disabled=yes</td></tr><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">=.id=ether1</td></tr><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">.tag=3</td></tr><tr><td class="highlight-#c1c7d0 confluenceTd" data-highlight-colour="#c1c7d0" title="Background colour : Medium grey 45%">-- <em title="">this is done for disable command (tag 3)</em></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!done</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">.tag=3</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#c1c7d0 confluenceTd" data-highlight-colour="#c1c7d0" title="Background colour : Medium grey 45%">-- <em title="">enable interface (tag is 4)</em></td></tr><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">/interface/set</td></tr><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">=disabled=no</td></tr><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">=.id=ether1</td></tr><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">.tag=4</td></tr><tr><td class="highlight-#c1c7d0 confluenceTd" data-highlight-colour="#c1c7d0" title="Background colour : Medium grey 45%">-- <em title="">this update is generated by change made by first set command (tag 3)</em></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!re</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=.id=*1</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=disabled=yes</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=dynamic=no</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=running=no</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=name=ether1</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=mtu=1500</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=type=ether</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">.tag=2</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#c1c7d0 confluenceTd" data-highlight-colour="#c1c7d0" title="Background colour : Medium grey 45%">-- <em title="">this is done for enable command (tag 4)</em></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!done</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">.tag=4</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#c1c7d0 confluenceTd" data-highlight-colour="#c1c7d0" title="Background colour : Medium grey 45%">-- <em title="">get interface list (tag is 5)</em></td></tr><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">/interface/getall</td></tr><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">.tag=5</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#c1c7d0 confluenceTd" data-highlight-colour="#c1c7d0" title="Background colour : Medium grey 45%">-- <em title="">this update is generated by change made by second set command (tag 4)</em></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!re</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=.id=*1</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=disabled=no</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=dynamic=no</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=running=yes</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=name=ether1</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=mtu=1500</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=type=ether</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">.tag=2</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#c1c7d0 confluenceTd" data-highlight-colour="#c1c7d0" title="Background colour : Medium grey 45%">-- <em title="">these are replies to getall command (tag 5)</em></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!re</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=.id=*1</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=disabled=no</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=dynamic=no</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=running=yes</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=name=ether1</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=mtu=1500</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=type=ether</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">.tag=5</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!re</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=.id=*2</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=disabled=no</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=dynamic=no</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=running=yes</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=name=ether2</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=mtu=1500</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=type=ether</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">.tag=5</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#c1c7d0 confluenceTd" data-highlight-colour="#c1c7d0" title="Background colour : Medium grey 45%">-- <em title="">here interface getall ends (tag 5)</em></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!done</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">.tag=5</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#c1c7d0 confluenceTd" data-highlight-colour="#c1c7d0" title="Background colour : Medium grey 45%">-- <em title="">stop listening - request to cancel command with tag 2, cancel itself uses tag 7</em></td></tr><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">/cancel</td></tr><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">=tag=2</td></tr><tr><td class="highlight-#eae6ff confluenceTd" data-highlight-colour="#eae6ff" title="Background colour : Light purple 35%">.tag=7</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#c1c7d0 confluenceTd" data-highlight-colour="#c1c7d0" title="Background colour : Medium grey 45%">-- <em title="">listen command is interrupted (tag 2)</em></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!trap</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=category=2</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">=message=interrupted</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">.tag=2</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#c1c7d0 confluenceTd" data-highlight-colour="#c1c7d0" title="Background colour : Medium grey 45%">-- <em title="">cancel command is finished (tag 7)</em></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!done</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">.tag=7</td></tr><tr><td class="confluenceTd"><br></td></tr><tr><td class="highlight-#c1c7d0 confluenceTd" data-highlight-colour="#c1c7d0" title="Background colour : Medium grey 45%">-- <em title="">listen command is finished (tag 2)</em></td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">&nbsp;!done</td></tr><tr><td class="highlight-#e3fcef confluenceTd" data-highlight-colour="#e3fcef" title="Background colour : Light green 35%">.tag=2</td></tr></tbody></table>

## Example client

A simple [API client in Python3](https://help.mikrotik.com/docs/display/ROS/Python3+Example)

Example output:

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

## See also

### API examples

API implementations in different languages, provided by different sources. They are not ordered in any particular order.

-   [in Python3](https://help.mikrotik.com/docs/display/ROS/Python3+Example) by MikroTik
-   [in .NET (C#) high-level API solution](https://github.com/danikf/tik4net) [forum thread](http://forum.mikrotik.com/viewtopic.php?f=9&t=99954) [additional info](https://github.com/danikf/tik4net/wiki) by danikf
-   [in PHP](https://sourceforge.net/projects/netrouteros/) by boen\_robot
-   [in C](https://github.com/haakonnessjoen/librouteros-api) by Håkon Nessjøen
-   [in Java](https://github.com/GideonLeGrange/mikrotik-java) by Gideon LeGrange
-   [in Erlang](https://github.com/comtihon/erotik) by Valery Comtihon
-   [in GO](https://github.com/go-routeros/routeros) by André Luiz dos Santos
-   [in Python3](https://github.com/LaiArturs/RouterOS_API) by Arturs Laizans
-   [in C++17](https://github.com/aymanalqadhi/tikpp) by Ayman Al-Qadhi