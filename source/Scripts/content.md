# 脚本语言手册

本手册介绍了RouterOS内置的强大脚本语言。

脚本主机提供了一种自动化一些路由器维护任务的方法，方法是执行用户定义的绑定到某些事件发生的脚本。

脚本可以存储在 [脚本存储库](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-Scriptrepository) 中，也可以直接写入 [控制台](https://help.mikrotik.com/docs/display/ROS/Console) 。用于触发脚本执行的事件包括但不限于 [系统调度程序](https://help.mikrotik.com/docs/display/ROS/Scheduler) 、[流量监控工具](https://help.mikrotik.com/docs/display/ROS/Interface+stats+and+monitor-traffic) 和 [网络监视工具](https://help.mikrotik.com/docs/display/ROS/Netwatch) 生成的事件。

如果你已经熟悉了RouterOS中的脚本，你可能会想看看 [提示和技巧](https://wiki.mikrotik.com/wiki/Manual:Scripting_Tips_and_Tricks)。

## 行结构

RouterOS脚本分为多个命令行。命令行一个接一个地执行，直到脚本结束或发生运行时错误。

### 命令行

RouterOS控制台的命令格式如下:

`[prefix] [path] command [uparam] [param=[value]] .. [param=[value]]`

- [prefix]-“:”或“/”字符表示命令是 [ICE](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-Commands) 还是路径。这可能不是必需的。
- [path] - 所需菜单级别的相对路径。这可能不是必需的。
- command - 指定菜单级别上可用的 [命令](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-Commands) 之一。
- [uparam] - 未命名参数，命令需要时必须指定。
- [params] - 命名参数序列，后面跟着相应的值

命令行末尾由令牌  ";"  或 _NEWLINE_ 表示。有时不需要使用  ";"  或 _NEWLINE_ 来结束命令行。

在 ()，[]或{} 内的单个命令不需要任何命令结束字符。命令的结尾由整个脚本的内容决定

```shell
:if ( true ) do={ :put "lala" }
```

每个命令行在另一个命令行中以方括号“[]” [命令连接](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-OtherOperators) 开始和结束。

```shell
:put [/ip route get [find gateway=1.1.1.1]];
```

注意，上面的代码包含三个命令行:

- :put
- /ip route get
- find gateway=1.1.1.1

通过遵循 [行连接规则](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-Linejoining)，可以从多个物理行构造命令行。

### 物理行

物理行是由行尾(EOL)序列结束的字符序列。任何标准的行终止序列都可以使用:

- **Unix** – ASCII LF;
- **Windows** – ASCII CR LF;
- **mac** – ASCII CR;

可以使用换行符的标准C约定(\\n字符)。

### 注释

以下规则适用于注释:

- 注释以散列字符(#)开始，以物理行结尾结束。
- RouterOS不支持多行注释。
- 如果字符串中出现 **#** 字符，则不认为是注释。

#### 例子

```shell
# this is a comment
# next line comment
:global a; # another valid comment
 
:global myStr "part of the string # is not a comment"
```

### 行连接

两个或多个物理行可以使用反斜杠字符(\)连接成逻辑行。

以下规则适用于使用反斜杠作为行连接工具:

- 以反斜杠结尾的行不能包含注释。
- 反斜杠不能继续注释。
- 反斜杠不能继续标记，除了字符串字面值。
- 在字符串字面值以外的行中使用反斜杠是非法的。

#### 例子

```shell
:if ($a = true \
    and $b=false) do={ :put "$a $b"; }
:if ($a = true \ # bad comment
    and $b=false) do={ :put "$a $b"; }
# comment \
    continued - invalid (syntax error)
```

### 标记之间的空白

空格可用于分隔令牌。只有当两个标记的连接可以被解释为不同的标记时，才需要在它们之间使用空白。例子:

```shell
{  
    :local a true; :local b false;
# whitespace is not required
    :put (a&&b);
# whitespace is required  
    :put (a and b);
}
```

不允许使用空白字符的地方

- between '<parameter>='
- between 'from=' 'to=' 'step=' 'in=' 'do=' 'else='

例子:

```shell
#incorrect:
:for i from = 1 to = 2 do = { :put $i }
#correct syntax:
:for i from=1 to=2 do={ :put $i }
:for i from= 1 to= 2 do={ :put $i }
 
#incorrect
/ip route add gateway = 3.3.3.3
#correct
/ip route add gateway=3.3.3.3
```

#### 范围

变量只能在脚本中称为作用域的特定区域中使用。这些区域决定变量的可见性。作用域有两种类型——全局作用域和局部作用域。在块中声明的变量只能在该块及其所包含的块中访问，并且只能在声明点之后访问。

##### 全局作用域

全局作用域或根作用域是脚本的默认作用域。它是自动创建的，不能关闭。

##### 局部作用域

用户可以定义自己的组来阻止对某些变量的访问，这些作用域称为局部作用域。每个局部作用域都用大括号(“{}”)括起来。

```shell
{  
    :local a 3;
    {  
        :local b 4;  
        :put ($a+$b);
    } #line below will show variable b in light red color since it is not defined in scope  
    :put ($a+$b);
}
```

在上面变量的代码中，b具有局部作用域，在右花括号之后无法访问。

写入终端的每一行都被视为局部作用域

因此，定义的局部变量在下一个命令行中将不可见，并将产生语法错误

```shell
[admin@MikroTik] > :local myVar a;
[admin@MikroTik] > :put $myVar
syntax error (line 1 column 7)

```

不要在局部范围内定义全局变量。

注意，即使变量可以定义为全局的，它也只能在其作用域中可用，除非它没有被引用为在作用域外可见。

```shell
{  
    :local a 3;
    {  
        :global b 4;
    }  
    :put ($a+$b);
}
```

上面的代码将输出3，因为在作用域之外b是不可见的。

下面的代码将修复这个问题并输出7:

```shell
{  
    :local a 3;
    {  
        :global b 4;
    }
    :global b;  
    :put ($a+$b);
}
```

## 关键字

以下词语为关键字，不能用作变量名和函数名:

```
and  or   in

```

## 分隔符

以下符号在语法中用作分隔符:

```
()  []  {}  :   ;   $   / 

```

## 数据类型

RouterOS脚本语言的数据类型如下:

| 类型               | 说明                                                              |
| ------------------ | ----------------------------------------------------------------- |
| **num (number)**   | - 64位带符号整数，可用十六进制;                                   |
| **bool (boolean)** | - 值可以为“真”或“假”;                                             |
| **str (string)**   | - 字符序列;                                                       |
| **ip**             | - ip地址;                                                         |
| **IP -prefix**     | - IP前缀;                                                         |
| **ip6**            | - IPv6地址                                                        |
| **IPv6 -prefix**   | - IPv6前缀                                                        |
| **id(内部id)**     | - “*”号前缀的十六进制值。每个菜单项都有一个分配的唯一编号-内部ID; |
| **time**           | -日期和时间值;                                                    |
| **array**          | - 在数组中组织的值序列;                                           |
| **nil**            | - 没有赋值时默认的变量类型;                                       |

### 常量转义序列

以下转义序列可用于定义字符串中的某些特殊字符:

|          |                                                            |
| -------- | ---------------------------------------------------------- |
| **\\"**  | 插入双引号                                                 |
| **\\**   | 插入反斜杠                                                 |
| **\\n**  | 插入新行                                                   |
| **\\r**  | 插入换行                                                   |
| **\\t**  | 插入制表                                                   |
| **\\$**  | 输出$符。或者用$来链接变量。                               |
| **\\?**  | ~~输出?符号。否则?用在控制台中打印“帮助”。~~ 自v7.1rc2删除 |
| **\\_**  | - 空格                                                     |
| **\\a**  | - BEL (0x07)                                               |
| **\\b**  | -退格(0x08)                                                |
| **\\f**  | - form feed (0xFF)                                         |
| **\\v**  | 插入垂直制表符                                             |
| **\\xx** | 从十六进制值中打印字符。十六进制数字应该使用大写字母。     |

#### 例子

```shell
:put "\48\45\4C\4C\4F\r\nThis\r\nis\r\na\r\ntest";

```

将显示

`HELLO   This   is   a   test   `

## 运算符

### 算术运算符

RouterOS脚本语言支持常用的算术运算符

| 运算符 | 描述     | 示例                           |
| ------ | -------- | ------------------------------ |
| **+**  | 二进制加 | `:put (3+4);`                  |
| **-**  | 二进制减 | `:put (1-6);`                  |
| **\*** | 二进制乘 | `:put (4*5);`                  |
| **/**  | 二进制除 | `:put (10 / 2); :put ((10)/2)` |
| **%**  | 取模操作 | `:put (5 % 3);`                |
| **-**  | 一元否定 | `{ :local a 1; :put (-a); }`   |

注意: 为了运行除法，必须使用大括号或者除数周围加空格，这样就不会被误认为是一个 IP 地址

### 关系运算符

| 运算符 | 描述             | 示例          |
| ------ | ---------------- | ------------- |
| **<**  | less             | `:put (3<4);` |
| **>**  | greater          | `:put (3>4);` |
| **=**  | equal            | `:put (2=2);` |
| **<=** | less or equal    |               |
| **>=** | greater or equal |               |
| **!=** | not equal        |               |

### 逻辑运算符

| 运算符      | 描述        | 示例                              |
| ----------- | ----------- | --------------------------------- |
| **!**       | logical NOT | `:put (!true);`                   |
| **&&, and** | logical AND | `:put (true&&true)`               |
| **\|\|,or** | logical OR  | `:put (true                       |  | false);` |
| **in**      |             | `:put (1.1.1.1/32 in 1.0.0.0/8);` |

### 位运算符

位运算符处理数字、IP和IPv6地址 [数据类型](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-Datatypes)。

| 运算符 | 描述                                                                                                | 示例                                                             |
| ------ | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **~**  | 位反转                                                                                              | :put (~0.0.0.0) <br> :put (~::ffff)                              |
| **\|** | 位或。对每一对应的位进行逻辑或运算。在每一对中，如果其中一位或两位为“1”，结果为“1”，否则结果为“0”。 | :put (192.168.88.0                                               | 0.0.0.255)  <br> :put (2001::1 | ::ffff) |
| **^**  | 按位异或。与OR相同，但如果两位不相等，则结果为“1”，如果两位相等，则为“0”。                          | :put (1.1.1.1^255.255.0.0) <br>:put (2001::ffff:1^::ffff:0)      |
| **&**  | 位与。在每一对中，如果第一个和第二个位都是“1”，则结果为“1”。否则，结果为“0”。                       | :put (192.168.88.77&255.255.255.0)  <br>:put (2001::1111&ffff::) |
| **<<** | 左移给定数量的位，不支持IPv6地址数据类型                                                            | :put (192.168.88.77<<8)                                          |
| **>>** | 右移给定数量的位，不支持IPv6地址数据类型                                                            | :put (192.168.88.77>>24)                                         |

使用“&”运算符从给定的IP和CIDR Netmask计算子网地址:

```shell
{
:local IP 192.168.88.77;
:local CIDRnetmask 255.255.255.0;
:put ($IP&$CIDRnetmask);
}
```

从给定的IP地址中获取最后8位:

```shell
:put (192.168.88.77&0.0.0.255);
```

使用“|”运算符和反向CIDR掩码计算广播地址:

```shell
{
:local IP 192.168.88.77;
:local Network 192.168.88.0;
:local CIDRnetmask 255.255.255.0;
:local InvertedCIDR (~$CIDRnetmask);
:put ($Network|$InvertedCIDR)
}
```

### 连接操作符

| 运算符 | 描述                                                    | 示例                                     |
| ------ | ------------------------------------------------------- | ---------------------------------------- |
| **.**  | concatenates two strings                                | `:put ("concatenate" . " " . "string");` |
| **,**  | concatenates two arrays or adds an element to the array | `:put ({1;2;3} , 5 );`                   |

可以在没有连接操作符的情况下向字符串添加变量值:

```shell
:global myVar "world";
 
:put ("Hello " . $myVar);
# next line does the same as above
:put "Hello $myVar";
```

通过在字符串中使用$[]和$()，可以在字符串中添加表达式:

```shell
:local a 5;
:local b 6;
:put " 5x6 = $($a * $b)";
 
:put " We have $[ :len [/ip route find] ] routes";
```

### 其他运算符

| 运算符 | 描述                                        | 示例                                                                                                                        |
| ------ | ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **[]** | 命令替换。只能包含一个命令行                | `:put [ :len "my test string"; ];`                                                                                          |
| **()** | 子表达式或分组操作符                        | `:put ( "value is " . (4+5));`                                                                                              |
| **$**  | 替换操作符                                  | `:global a 5; :put $a;`                                                                                                     |
| **~**  | 根据POSIX扩展正则表达式匹配值的二进制运算符 | 打印网关以202结尾的所有路由  <br>`/ip route print where gateway~"^[0-9 \\.]*202\$"`                                         |
| **->** | 根据关键字获取数组元素                      | [admin@x86] >:global aaa {a=1;b=2} <br>[admin@x86] >:put (\$aaa->"a") <br> 1 <br>[admin@x86] > :put ($aaa->"b") <br> 2 <br> |

## 变量

脚本语言有两种类型的变量:

- global - 可以从当前用户创建的所有脚本访问，由 [global](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-Scopes) 关键字定义;
- local - 只能在当前 [scope](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-Scopes) 内访问，由 [local](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-Scopes) 关键字定义。

当变量未定义时，解析器将尝试查找由 [DHCP](https://help.mikrotik.com/docs/display/ROS/DHCP)  lease-script或 [Hotspot](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=56459266) on-login设置的变量

除了内置的RouterOS变量，每个变量都必须在局部或全局关键字使用之前声明。未定义的变量将被标记为未定义，并将导致编译错误。例子:

```shell
# following code will result in compilation error, because myVar is used without declaration
:set myVar "my value";
:put $myVar
```

正确的代码:

```shell
:local myVar;
:set myVar "my value";
:put $myVar;
```

例外情况是使用由DHCP lease-script设置的变量

```shell
/system script
add name=myLeaseScript policy=\
    ftp,reboot,read,write,policy,test,winbox,password,sniff,sensitive,api \
    source=":log info \$leaseActIP\r\
    \n:log info \$leaseActMAC\r\
    \n:log info \$leaseServerName\r\
    \n:log info \$leaseBound"
 
/ip dhcp-server set myServer lease-script=myLeaseScript
```

变量名中的有效字符是字母和数字。如果变量名包含任何其他字符，则变量名应放在双引号中。例子:

```shell
#valid variable name
:local myVar;
#invalid variable name
:local my-var;
#valid because double quoted
:global "my-var";
```

如果变量最初定义时没有值，则将 [变量数据类型](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-Datatypes) 设置为 _nil_ ，否则，脚本引擎将自动确定数据类型。有时需要从一种数据类型转换为另一种数据类型。可以使用 [数据转换命令](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-Globalcommands) 实现。

例子:

```shell
#convert string to array
:local myStr "1,2,3,4,5";
:put [:typeof $myStr];
:local myArr [:toarray $myStr];
:put [:typeof $myArr]
```

变量名区分大小写。

```shell
:local myVar "hello"
# following line will generate error, because variable myVAr is not defined
:put $myVAr
# correct code
:put $myVar
```

不带值的Set命令将取消对变量的定义(从环境中删除，v6.2新增功能)

```shell
#remove variable from environment
:global myVar "myValue"
:set myVar;
```

当变量名中包含操作符时，要在完整的变量名上使用引号。例子:

```shell
:local "my-Var";
:set "my-Var" "my value";
:put $"my-Var";
```

### 保留变量名

所有内置的RouterOS属性都是保留变量。与RouterOS内置属性定义相同的变量可能会导致错误。为避免此类错误，请使用自定义名称。

例如，下面的脚本将不起作用:

```shell
{
:local type "ether1";
/interface print where name=$type;
}
```

但是可以使用不同定义的变量:

```shell
{
:local customname "ether1";
/interface print where name=$customname;
}
```

## 命令

### 全局命令

每个全局命令都应该以 _":"_ 标记开头，否则将被视为一个变量。

| 命令            | 语法                                                        | 说明                                                                                                                                                                                                                                                                                       | 示例                                                                                                                                                                          |
| --------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **/**           |                                                             | 返回根菜单                                                                                                                                                                                                                                                                                 |                                                                                                                                                                               |
| **..**          |                                                             | 返回到一个菜单级                                                                                                                                                                                                                                                                           |                                                                                                                                                                               |
| **?**           |                                                             | 列出所有可用的菜单命令和简要说明                                                                                                                                                                                                                                                           |                                                                                                                                                                               |
| **global**      | `:global <var> [<value>]`                                   | 定义全局变量                                                                                                                                                                                                                                                                               | `:global myVar "something"; :put $myVar;`                                                                                                                                     |
| **local**       | `:local <var> [<value>]`                                    | 定义局部变量                                                                                                                                                                                                                                                                               | `{ :local myLocalVar "I am local"; :put $myVar; }`                                                                                                                            |
| **beep**        | `:beep <freq> <length>`                                     | 内置扬声器响铃                                                                                                                                                                                                                                                                             |                                                                                                                                                                               |
| **convert**     | `:convert from=[arg] to=[arg]`                              | <br>将指定的值从一种格式转换为另一种格式。默认情况，如果没有指定"from"格式，则使用自动解析的值(例如，"001"变成"1"，"10.1"变成"10.0.0.1"，等等)。<br>**from** 指定值的格式- _base32, base64, hex, raw, rot13, url_ 。<br>**to** 指定输出值的格式- _base32, base64, hex, raw, rot13, url_ 。 | <br>`:put [:convert 001 to=hex ]`<br>`31`<br>`:put [:convert [/ip dhcp-client/option/get hostname raw-value] from=hex to=raw ]`<br>`MikroTik`                                 |
| **delay**       | `:delay <time>`                                             | 在一段时间内什么都不做                                                                                                                                                                                                                                                                     |                                                                                                                                                                               |
| **environment** | `:environment print <start>`                                | 打印初始化变量信息                                                                                                                                                                                                                                                                         | `:global myVar true; :environment print;`                                                                                                                                     |
| **error**       | `:error <output>`                                           | 生成控制台错误并停止执行脚本                                                                                                                                                                                                                                                               |                                                                                                                                                                               |
| **execute**     | `:execute <expression>`                                     | <br>在后台执行脚本。可以通过设置“file”参数将结果写入文件，也可以通过设置“as-string”参数将结果打印到CLI <br>当使用“as-string”参数时，执行的脚本会被阻塞(不在后台执行)。                                                                                                                     | <br>{<br>:local j [:execute {/interface print follow where [:log info ~Sname~]}];<br>:delay 10s;<br>:do { /system script job remove $j } on-error={}<br>}                     |
| **find**        | `:find <arg> <arg> <start>`                                 | 返回子字符串或数组元素的位置                                                                                                                                                                                                                                                               | `:put [:find "abc" "a" -1];`                                                                                                                                                  |
| **jobname**     | :jobname                                                    | 返回当前脚本名称                                                                                                                                                                                                                                                                           | **将脚本执行限制为单个实例** <br>:if ([/system script job print count-only as-value where script=[:jobname] ] > 1) do={<br>  :error "script instance already running"<br>  }` |
| **len**         | `:len <expression>`                                         | 返回字符串长度或数组元素计数值                                                                                                                                                                                                                                                             | `:put [:len "length=8"];`                                                                                                                                                     |
| **log**         | `:log <topic> <message>`                                    | 写一条消息到 [系统日志](https://help.mikrotik.com/docs/display/ROS/Log) 。可用的主题是“调试、错误、信息和警告”。                                                                                                                                                                           | `:log info "Hello from script";`                                                                                                                                              |
| **parse**       | `:parse <expression>`                                       | 解析字符串并返回解析后的控制台命令。可以作为函数使用。                                                                                                                                                                                                                                     | `:global myFunc [:parse ":put hello!"];   $myFunc;`                                                                                                                           |
| **pick**        | `:pick <var> <start>[<count>]`                              | 返回元素或子字符串的范围。如果未指定计数，则只返回数组中的一个元素。<br>- start -开始选择的元素(第一个元素索引为0)<br>- count -从索引为0的第一个元素开始选择的元素数量                                                                                                                     | [admin@MikroTik] > :put [:pick "abcde" 1 3]<br>bc                                                                                                                             |
| **put**         | `:put <expression>`                                         | 将提供的参数放入控制台中                                                                                                                                                                                                                                                                   | :put "Hello world"                                                                                                                                                            |
| **resolve**     | `:resolve <arg>`                                            | 返回指定DNS名称的IP地址                                                                                                                                                                                                                                                                    | `:put [:resolve "[www.mikrotik.com](http://www.mikrotik.com)"];`                                                                                                              |
| **retry**       | :retry command=<expr> delay=[num] max=[num] on-error=<expr> | 在两次尝试之间以指定的“延迟”执行命令的次数为“max”。如果失败，执行"On -error"块中给出的表达式                                                                                                                                                                                               | :retry command={abc} delay=1 max=2 on-error={:put "got error"}  <br>got error                                                                                                 |
| **typeof**      | `:typeof <var>`                                             | 变量的返回数据类型                                                                                                                                                                                                                                                                         | `:put [:typeof 4];`                                                                                                                                                           |
| **rndnum**      | `:rndnum from=[num] to=[num]`                               | 随机数发生器                                                                                                                                                                                                                                                                               | `:put [:rndnum from=1 to=99];`                                                                                                                                                |
| **rndstr**      | `:rndstr from=[str] length=[num]`                           | 随机字符串生成器。<br> **from** 指定要构造字符串from的字符，默认为所有ASCII字母和数字。<br> **length** 指定要创建的字符串的长度，默认为16。                                                                                                                                                | `:put [:rndnum from="abcdef%^&``" length=33];`                                                                                                                                |
| **set**         | `:set <var> [<value>]`                                      | 为声明的变量赋值。                                                                                                                                                                                                                                                                         | `:global a; :set a true;`                                                                                                                                                     |
| **terminal**    | :terminal                                                   | 终端相关命令                                                                                                                                                                                                                                                                               |                                                                                                                                                                               |
| **time**        | `:time <expression>`                                        | 返回执行命令所需的时间间隔                                                                                                                                                                                                                                                                 | `:put [:time {:for i from=1 to=10 do={ :delay 100ms }}];`                                                                                                                     |
| **timestamp**   | `:timestamp`                                                | 返回自epoch以来的时间，其中epoch为1970年1月1日(星期四)，不包括闰秒                                                                                                                                                                                                                         | <br>[admin@MikroTik] > :put [:timestamp]<br>2735w21:41:43.481891543<br>or<br>[admin@MikroTik] > :put [:timestamp]<br>2735w1d21:41:43.481891543<br>with the day offset         |
| **toarray**     | `:toarray <var>`                                            | 将变量转换为数组                                                                                                                                                                                                                                                                           |                                                                                                                                                                               |
| **tobool**      | `:tobool <var>`                                             | 将变量转换为布尔值                                                                                                                                                                                                                                                                         |                                                                                                                                                                               |
| **toid**        | `:toid <var>`                                               | 将变量转换为内部ID                                                                                                                                                                                                                                                                         |                                                                                                                                                                               |
| **toip**        | `:toip <var>`                                               | 将变量转换为IP地址                                                                                                                                                                                                                                                                         |                                                                                                                                                                               |
| **toip6**       | `:toip6 <var>`                                              | 将变量转换为IPv6地址                                                                                                                                                                                                                                                                       |                                                                                                                                                                               |
| **tonum**       | `:tonum <var>`                                              | 将变量转换为整数                                                                                                                                                                                                                                                                           |                                                                                                                                                                               |
| **tostr**       | `:tostr <var>`                                              | 将变量转换为字符串                                                                                                                                                                                                                                                                         |                                                                                                                                                                               |
| **totime**      | `:totime <var>`                                             | 将变量转换为时间                                                                                                                                                                                                                                                                           |                                                                                                                                                                               |

### 菜单特定命令

#### 常用命令

以下命令在大多数子菜单中可用:

| 命令        | 语法                                        | 说明                                                                                                                                                                                                                                      |
| ----------- | ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **add**     | `add <param>=<value>..<param>=<value>`      | 添加新项                                                                                                                                                                                                                                  |
| **remove**  | `remove <id>`                               | 删除选中项                                                                                                                                                                                                                                |
| **enable**  | `enable <id>`                               | 启用已选项                                                                                                                                                                                                                                |
| **disable** | `disable <id>`                              | 禁止已选项                                                                                                                                                                                                                                |
| **set**     | `set <id> <param>=<value>..<param>=<value>` | 更改所选项目参数时，可以同时指定多个参数。该参数可以通过指定'!'来取消设置。<br>示例:  <br>`/ip firewall filter add chain=blah action=accept protocol=tcp port=123 nth=4,2   print   set 0 !port chain=blah2 !nth protocol=udp`            |
| **get**     | `get <id> <param>=<value>`                  | 获取所选项的参数值                                                                                                                                                                                                                        |
| **print**   | `print <param><param>=[<value>]`            | 打印菜单项。输出取决于指定的打印参数。最常见的打印参数描述见 [这里](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-printparameters)                                                                                       |
| **export**  | `export [file=<value>]`                     | 从当前菜单及其子菜单(如果存在)导出配置。如果指定了file参数，输出将被写入扩展名为".rsc"的文件。否则输出将被打印到控制台。导出的命令可以通过 [import command](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-import) 导入。 |
| **edit**    | `edit <id> <param>`                         | 在内置文本编辑器中编辑选定项属性                                                                                                                                                                                                          |
| **find**    | `find <expression>`                         | 返回与给定表达式匹配项的内部数字列表。例如:  `:put [/interface find name~"ether"]`                                                                                                                                                        |

#### 导入

import命令可从根菜单中使用，从 [export](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-Commoncommands) 命令创建的文件或手工编写的文件中导入配置。

#### 打印参数

print命令有几个参数:

| 参数               | 说明                                                                     | 例子                                       |
| ------------------ | ------------------------------------------------------------------------ | ------------------------------------------ |
| **append**         |                                                                          |                                            |
| **as-value**       | 输出数组的参数和值                                                       | `:put [/ip address print as-value]`        |
| **brief**          | 打印主要说明                                                             |                                            |
| **detail**         | 打印详细描述，不如简短输出可读，但有助于查看所有参数                     |
| **count-only**     | 只打印菜单项的计数                                                       |                                            |
| **file**           | 打印到文件                                                               |
| **follow**         | 打印所有当前条目并跟踪新条目，直到按下ctrl-c，这在查看日志条目时非常有用 | `/log print follow`                        |
| **follow-only**    | 只打印和跟踪新条目，直到按下ctrl-c，这在查看日志条目时非常有用           | `/log print follow-only`                   |
| **from**           | 仅从指定项打印参数                                                       | `/user print from=admin`                   |
| **interval**       | 在选定的时间间隔内连续打印输出，对跟踪不接受“follow”的更改非常有用       | `/interface print interval=2`              |
| **terse**          | 以紧凑和机器友好的格式显示详细信息                                       |                                            |
| **value-list**     | 每行显示一个值(有利于解析)                                               |                                            |
| **without-paging** | 如果输出不适合控制台屏幕，则将所有信息打印在一起                         |                                            |
| **where**          | 表达式后面的参数可用于过滤不匹配的项                                     | `/ip route print where interface="ether1"` |

一次可以指定多个参数，例如: /ip route print count-only interval=1 where interface="ether1"

## 循环和条件语句

### 循环

| 命令          | 语法                                                                                    | 说明                           |
| ------------- | --------------------------------------------------------------------------------------- | ------------------------------ |
| **do..while** | `:do { <commands> } while=( <conditions> ); :while ( <conditions> ) do={ <commands> };` | 执行命令，直到满足给定的条件。 |
| **for**       | `:for <var> from=<int> to=<int> step=<int> do={ <commands> }`                           | 执行给定的迭代次数             |
| **foreach**   | `:foreach <var> in=<array> do={ <commands> };`                                          | 对列表中的每个元素执行命令     |

### 条件语句

| 命令   | 语法                                                               | 说明                                                                         |
| ------ | ------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| **if** | `:if (<condition>) do={<commands>} else={<commands>} <expression>` | 如果给定条件为“true”，则在“do”块中执行命令，否则在指定的“else”块中执行命令。 |

例子:

```shell
{  
    :local myBool true;  
    :if ($myBool = false) do={ :put "value is false" } else={ :put "value is true" }
}
```

## 函数

脚本语言不允许直接创建函数，但是可以使用:parse命令作为解决方案。

从v6.2开始，添加了新的语法，更容易定义这类函数，甚至传递参数。也可以使用 **:return** 命令返回函数值。

请看下面的例子:

```shell
#define function and run it
:global myFunc do={:put "hello from function"}
$myFunc
 
output:
hello from function
 
#pass arguments to the function
:global myFunc do={:put "arg a=$a"; :put "arg '1'=$1"}
$myFunc a="this is arg a value" "this is arg1 value"
 
output:
arg a=this is arg a value
arg '1'=this is arg1 value
```

注意，有两种传递参数的方式:

- 传递具有特定名称的参数(在我们的示例中为"a")
- 传递没有arg名称的值，在这种情况下，arg "1"， "2" ..使用“n”。

**返回示例**

```shell
:global myFunc do={ :return ($a + $b)}
:put [$myFunc a=6 b=2]
 
output:
8
```

甚至可以从脚本环境中克隆一个现有的脚本，并将其作为函数使用。

```shell
#add script
/system script add name=myScript source=":put "Hello $myVar !""
 
:global myFunc [:parse [/system script get myScript source]]
$myFunc myVar=world
 
output:
Hello world !
```

如果函数包含一个定义的全局变量，该变量的名称与传递的参数的名称匹配，那么全局定义的变量将被忽略，以便与为旧版本编写的脚本兼容。这个特性在以后的版本中可能会改变。**避免使用与全局变量同名的参数**

例如:

```shell
:global my2 "123"
 
:global myFunc do={ :global my2; :put $my2; :set my2 "lala"; :put $my2 }
$myFunc my2=1234
:put "global value $my2"
```

输出是:

```shell
1234
lala
global value 123

```

**嵌套函数示例**

**注意:** 要调用另一个函数，要声明名称(与变量相同)

```shell
:global funcA do={ :return 5 }
:global funcB do={  
    :global funcA;  
    :return ([$funcA] + 4)
}
:put [$funcB]
 
Output:
9
```

## 捕获运行错误

从v6.2开始，脚本具有捕获运行时错误的能力。

例如，[code]: resolve [/code]命令如果失败，将抛出错误并中断脚本。

```shell
[admin@MikroTik] > { :put [:resolve www.example.com]; :put "lala";}
failure: dns name does not exist

```

现在想要捕获这个错误并继续脚本:

```shell
:do {  
    :put [:resolve www.example.com];
} on-error={ :put "resolver failed"};
:put "lala"
 
output:
 
resolver failed
lala
```

## 数组操作

**警告:** 数组中的键名包含非小写字符，需要用引号括起来

例如:

```shell
[admin@ce0] > {:local a { "aX"=1 ;; ay=2 }; :put ($a->"aX")}
1
```

**循环键和值**

"foreach"命令可用于遍历键和元素:

```shell
[admin@ce0] > :foreach k,v in={2; "aX"=1 ;; y=2; 5} do={:put ("$k=$v")}
 
0=2
1=5
aX=1
y=2
```

如果"foreach"命令只带一个参数，则返回元素值:

```shell
[admin@ce0] > :foreach k in={2; "aX"=1 ;; y=2; 5} do={:put ("$k")}
 
2
5
1
2
```

**注意:** 如果数组元素有键，则这些元素按字母顺序排序，没有键的元素在有键的元素之前移动，并且它们的顺序不会改变(参见上面的例子)。

**修改单个数组元素的值**

```shell
[admin@MikroTik] > :global a {x=1; y=2}
[admin@MikroTik] > :set ($a->"x") 5 
[admin@MikroTik] > :environment print 
a={x=5; y=2}

```

# 脚本仓库

**Sub-menu:** `/system script`

包含所有用户创建的脚本。脚本可以通过几种不同的方式执行:

- **on event** -脚本在一些设施事件 ([scheduler](https://help.mikrotik.com/docs/display/ROS/Scheduler)， [netwatch](https://help.mikrotik.com/docs/display/ROS/Netwatch)， [VRRP](https://help.mikrotik.com/docs/display/ROS/VRRP)) 上自动执行。
- **by another script** -允许在脚本中运行脚本
- **manually** -从控制台执行运行命令或在winbox中

**注:** 具有同等或更高权限的脚本(包括scheduler, netwatch等)才能执行其他脚本。

| 属性                                                                                             | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **comment** (_string_; Default: )                                                                | 脚本的注释                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **dont-require-permissions** (_yes \| no_; Default: _no_)                                        | 当脚本被执行时绕过权限检查，当脚本从权限有限的服务执行时很有用，例如 [Netwatch](https://wiki.mikrotik.com/wiki/Manual:Tools/Netwatch "Manual:Tools/Netwatch")                                                                                                                                                                                                                                                                                         |
| **name** (_string_; Default: _"Script[num]"_)                                                    | 脚本名称                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **policy** (_string_; Default: ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon) | 适用政策一览表:<br>- **ftp** -可以通过ftp远程登录并从路由器发送和检索文件<br>- **password** -更改密码<br>- **policy** -管理用户策略，添加和删除用户<br>- **read** -可以检索配置<br>- **reboot** -可以重启路由器<br>- **sensitive** -允许更改“隐藏敏感”参数<br>- **sniff** -运行嗅探器，torch等<br>- **test** -可以运行ping, traceroute，带宽测试<br>- **write** -改变配置<br> [阅读更详细的策略说明](https://help.mikrotik.com/docs/display/ROS/User) |
| **source** (_string_;)                                                                           | 脚本源码                                                                                                                                                                                                                                                                                                                                                                                                                                              |

只读状态属性:

| 属性                      | 说明                       |
| ------------------------- | -------------------------- |
| **last-started** (_date_) | 上次调用脚本的日期和时间。 |
| **owner** (_string_)      | 创建脚本的用户             |
| **run-count** (_integer_) | 脚本执行次数计数器         |

菜单特定命令

| 命令                         | 说明                     |
| ---------------------------- | ------------------------ |
| **run** (_run [id \| name]_) | 按ID或名称执行指定的脚本 |

## 环境

**Sub-menu:**

- `/system script environment`
- `/environment`

包含所有用户定义的变量及其分配的值。

```shell
[admin@MikroTik] > :global example;
[admin@MikroTik] > :set example 123
[admin@MikroTik] > /environment print  
"example"=123

```
  
只读状态属性:

| 属性                | 说明           |
| ------------------- | -------------- |
| **name** (_string_) | 变量名         |
| **user** (_string_) | 定义变量的用户 |
| **value**()         | 变量的值       |

## 任务

**Sub-menu:** `/system script job`

包含所有当前正在运行的脚本的列表。

只读状态属性:

| 属性                 | 说明                     |
| -------------------- | ------------------------ |
| **owner** (_string_) | 运行脚本的用户           |
| **policy** (_array_) | 应用于脚本的所有策略列表 |
| **started** (_date_) | 启动脚本的本地日期和时间 |

# 另外参见

- [Scripting Examples](https://help.mikrotik.com/docs/display/ROS/Scripting+examples)
- [Manual: Scripting Tips and Tricks](https://wiki.mikrotik.com/wiki/Manual:Scripting_Tips_and_Tricks "Manual:Scripting Tips and Tricks")