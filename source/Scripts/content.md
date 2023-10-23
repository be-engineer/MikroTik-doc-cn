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

不允许使用空白字符

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
and       or       in

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

| 运算符 | 描述                  | 示例                           |
| ------ | --------------------- | ------------------------------ |
| **+**  | binary addition       | `:put (3+4);`                  |
| **-**  | binary subtraction    | `:put (1-6);`                  |
| **\*** | binary multiplication | `:put (4*5);`                  |
| **/**  | binary division       | `:put (10 / 2); :put ((10)/2)` |
| **%**  | modulo operation      | `:put (5 % 3);`                |
| **-**  | unary negation        | `{ :local a 1; :put (-a); }`   |

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

| 运算符 | 描述                                                                                                                                                                              | 示例                                                             |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **~**  | bit inversion                                                                                                                                                                     | :put (~0.0.0.0) <br> :put (~::ffff)                              |
| **\|** | bitwise OR. Performs logical OR operation on each pair of corresponding bits. In each pair the result is “1” if one of the bits or both bits is “1”, otherwise the result is “0”. | :put (192.168.88.0                                               | 0.0.0.255)  <br> :put (2001::1 | ::ffff) |
| **^**  | bitwise XOR. The same as OR, but the result in each position is “1” if two bits are not equal, and “0” if the bits are equal.                                                     | :put (1.1.1.1^255.255.0.0) <br>:put (2001::ffff:1^::ffff:0)      |
| **&**  | bitwise AND. In each pair, the result is “1” if the first and second bit is “1”. Otherwise, the result is “0”.                                                                    | :put (192.168.88.77&255.255.255.0)  <br>:put (2001::1111&ffff::) |
| **<<** | left shift by a given amount of bits, not supported for IPv6 address data type                                                                                                    | :put (192.168.88.77<<8)                                          |
| **>>** | right shift by a given amount of bits, not supported for IPv6 address data type                                                                                                   | :put (192.168.88.77>>24)                                         |

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

| 运算符 | 描述                                                                             | 示例                                                                                                                        |
| ------ | -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **[]** | command substitution. Can contain only a single command line                     | `:put [ :len "my test string"; ];`                                                                                          |
| **()** | subexpression or grouping operator                                               | `:put ( "value is " . (4+5));`                                                                                              |
| **$**  | substitution operator                                                            | `:global a 5; :put $a;`                                                                                                     |
| **~**  | the binary operator that matches value against POSIX extended regular expression | Print all routes whose gateway ends with 202  <br>`/ip route print where gateway~"^[0-9 \\.]*202\$"`                        |
| **->** | Get an array element by key                                                      | [admin@x86] >:global aaa {a=1;b=2} <br>[admin@x86] >:put (\$aaa->"a") <br> 1 <br>[admin@x86] > :put ($aaa->"b") <br> 2 <br> |

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

如果变量最初定义时没有值，则将 [变量数据类型](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-Datatypes) 设置为 _nil_ ，否则，脚本引擎将自动确定数据类型。有时需要从一种数据类型转换为另一种数据类型。可以使用 [数据转换命令](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-Globalcommands) 实现。例子:

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

| 命令            | 语法                                                            | 说明                                                                                                                                                                                                                                                                                                                                                                                                  | 示例                                                                                                                                                                                           |
| --------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **/**           |                                                                 | go to the root menu                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                                                                |
| **..**          |                                                                 | go back by one menu level                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                                                |
| **?**           |                                                                 | list all available menu commands and brief descriptions                                                                                                                                                                                                                                                                                                                                               |                                                                                                                                                                                                |
| **global**      | `:global <var> [<value>]`                                       | define a global variable                                                                                                                                                                                                                                                                                                                                                                              | `:global myVar "something"; :put $myVar;`                                                                                                                                                      |
| **local**       | `:local <var> [<value>]`                                        | define the local variable                                                                                                                                                                                                                                                                                                                                                                             | `{ :local myLocalVar "I am local"; :put $myVar; }`                                                                                                                                             |
| **beep**        | `:beep <freq> <length>`                                         | beep built-in speaker                                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                                                |
| **convert**     | `:convert from=[arg] to=[arg]`                                  | <br>Converts specified value from one format to another. By default uses an automatically parsed value, if the "from" format is not specified (for example, "001" becomes "1", "10.1" becomes "10.0.0.1", etc.).<br>**from** specifies the format of the value - _base32, base64, hex, raw, rot13, url_.<br>**to** specifies the format of the output value - _base32, base64, hex, raw, rot13, url_. | <br>`:put [:convert 001 to=hex ]`<br>`31`<br>`:put [:convert [/ip dhcp-client/option/get hostname raw-value] from=hex to=raw ]`<br>`MikroTik`                                                  |
| **delay**       | `:delay <time>`                                                 | do nothing for a given period of time                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                                                |
| **environment** | `:environment print <start>`                                    | print initialized variable information                                                                                                                                                                                                                                                                                                                                                                | `:global myVar true; :environment print;`                                                                                                                                                      |
| **error**       | `:error <output>`                                               | Generate console error and stop executing the script                                                                                                                                                                                                                                                                                                                                                  |                                                                                                                                                                                                |
| **execute**     | `:execute <expression>`                                         | <br>Execute the script in the background. The result can be written in the file by setting a "file" parameter or printed to the CLI by setting "as-string"<br>When using the "as-string" parameter executed script is blocked (not executed in the background).                                                                                                                                       | <br>{<br>:local j [:execute {/interface print follow where [:log info ~Sname~]}];<br>:delay 10s;<br>:do { /system script job remove $j } on-error={}<br>}                                      |
| **find**        | `:find <arg> <arg> <start>`                                     | return position of a substring or array element                                                                                                                                                                                                                                                                                                                                                       | `:put [:find "abc" "a" -1];`                                                                                                                                                                   |
| **jobname**     | :jobname                                                        | return current script name                                                                                                                                                                                                                                                                                                                                                                            | **Limit script execution to single instance** <br>:if ([/system script job print count-only as-value where script=[:jobname] ] > 1) do={<br>  :error "script instance already running"<br>  }` |
| **len**         | `:len <expression>`                                             | return string length or array element count                                                                                                                                                                                                                                                                                                                                                           | `:put [:len "length=8"];`                                                                                                                                                                      |
| **log**         | `:log <topic> <message>`                                        | write a message to the [system log](https://help.mikrotik.com/docs/display/ROS/Log). Available topics are `"debug, error, info and warning"`                                                                                                                                                                                                                                                          | `:log info "Hello from script";`                                                                                                                                                               |
| **parse**       | `:parse <expression>`                                           | parse the string and return parsed console commands. Can be used as a function.                                                                                                                                                                                                                                                                                                                       | `:global myFunc [:parse ":put hello!"];   $myFunc;`                                                                                                                                            |
| **pick**        | `:pick <var> <start>[<count>]`                                  | return range of elements or substring. If the count is not specified, will return only one element from an array.<br>- var - value to pick elements from<br>- start - element to start picking from (the first element index is 0)<br>- count - number of elements to pick starting from the first element with index=0                                                                               | [admin@MikroTik] > :put [:pick "abcde" 1 3]<br>bc                                                                                                                                              |
| **put**         | `:put <expression>`                                             | put the supplied argument into the console                                                                                                                                                                                                                                                                                                                                                            | :put "Hello world"                                                                                                                                                                             |
| **resolve**     | `:resolve <arg>`                                                | return the IP address of the given DNS name                                                                                                                                                                                                                                                                                                                                                           | `:put [:resolve "[www.mikrotik.com](http://www.mikrotik.com)"];`                                                                                                                               |
| **retry**       | :retry command=<expr> delay=\[num\] max=\[num\] on-error=<expr> | Try to execute the given command "max" amount of times with a given "delay" between tries. On failure, execute the expression given in the "on-error" block                                                                                                                                                                                                                                           | :retry command={abc} delay=1 max=2 on-error={:put "got error"}  <br>got error                                                                                                                  |
| **typeof**      | `:typeof <var>`                                                 | the return data type of variable                                                                                                                                                                                                                                                                                                                                                                      | `:put [:typeof 4];`                                                                                                                                                                            |
| **rndnum**      | `:rndnum from=[num] to=[num]`                                   | random number generator                                                                                                                                                                                                                                                                                                                                                                               | `:put [:rndnum from=1 to=99];`                                                                                                                                                                 |
| **rndstr**      | `:rndstr from=[str] length=[num]`                               | Random string generator.<br>**from** specifies characters to construct the string from and defaults to all ASCII letters and numerals.  <br> **length** specifies the length of the string to create and defaults to 16.                                                                                                                                                                              | `:put [:rndnum from="abcdef%^&``" length=33];`                                                                                                                                                 |
| **set**         | `:set <var> [<value>]`                                          | assign value to a declared variable.                                                                                                                                                                                                                                                                                                                                                                  | `:global a; :set a true;`                                                                                                                                                                      |
| **terminal**    | :terminal                                                       | terminal related commands                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                                                |
| **time**        | `:time <expression>`                                            | return interval of time needed to execute the command                                                                                                                                                                                                                                                                                                                                                 | `:put [:time {:for i from=1 to=10 do={ :delay 100ms }}];`                                                                                                                                      |
| **timestamp**   | `:timestamp`                                                    | returns the time since epoch, where epoch is January 1, 1970 (Thursday), not counting leap seconds                                                                                                                                                                                                                                                                                                    | <br>[admin@MikroTik] > :put [:timestamp]<br>2735w21:41:43.481891543<br>or<br>[admin@MikroTik] > :put [:timestamp]<br>2735w1d21:41:43.481891543<br>with the day offset                          |
| **toarray**     | `:toarray <var>`                                                | convert a variable to the array                                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                |
| **tobool**      | `:tobool <var>`                                                 | convert a variable to boolean                                                                                                                                                                                                                                                                                                                                                                         |                                                                                                                                                                                                |
| **toid**        | `:toid <var>`                                                   | convert a variable to internal ID                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                                                                                                |
| **toip**        | `:toip <var>`                                                   | convert a variable to IP address                                                                                                                                                                                                                                                                                                                                                                      |                                                                                                                                                                                                |
| **toip6**       | `:toip6 <var>`                                                  | convert a variable to IPv6 address                                                                                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                |
| **tonum**       | `:tonum <var>`                                                  | convert a variable to an integer                                                                                                                                                                                                                                                                                                                                                                      |                                                                                                                                                                                                |
| **tostr**       | `:tostr <var>`                                                  | convert a variable to a string                                                                                                                                                                                                                                                                                                                                                                        |                                                                                                                                                                                                |
| **totime**      | `:totime <var>`                                                 | convert a variable to time                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                                                                                                                |

### 菜单特定命令

#### 常用命令

以下命令在大多数子菜单中可用:

| 命令        | 语法                                        | 说明                                                                                                                                                                                                                                                                                                                                                          |
| ----------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **add**     | `add <param>=<value>..<param>=<value>`      | add new item                                                                                                                                                                                                                                                                                                                                                  |
| **remove**  | `remove <id>`                               | remove selected item                                                                                                                                                                                                                                                                                                                                          |
| **enable**  | `enable <id>`                               | enable selected item                                                                                                                                                                                                                                                                                                                                          |
| **disable** | `disable <id>`                              | disable selected item                                                                                                                                                                                                                                                                                                                                         |
| **set**     | `set <id> <param>=<value>..<param>=<value>` | change selected items parameter, more than one parameter can be specified at the time. The parameter can be unset by specifying '!' before the parameter.<br>Example:  <br>`/ip firewall filter add chain=blah action=accept protocol=tcp port=123 nth=4,2   print   set 0 !port chain=blah2 !nth protocol=udp`                                               |
| **get**     | `get <id> <param>=<value>`                  | get the selected item's parameter value                                                                                                                                                                                                                                                                                                                       |
| **print**   | `print <param><param>=[<value>]`            | print menu items. Output depends on the print parameters specified. The most common print parameters are described [here](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-printparameters)                                                                                                                                                     |
| **export**  | `export [file=<value>]`                     | export configuration from the current menu and its sub-menus (if present). If the file parameter is specified output will be written to the file with the extension '.rsc', otherwise the output will be printed to the console. Exported commands can be imported by [import command](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-import) |
| **edit**    | `edit <id> <param>`                         | edit selected items property in the built-in text editor                                                                                                                                                                                                                                                                                                      |
| **find**    | `find <expression>`                         | Returns list of internal numbers for items that are matched by given expression. For example:  `:put [/interface find name~"ether"]`                                                                                                                                                                                                                          |

#### 导入

import命令可从根菜单中使用，从 [export](https://help.mikrotik.com/docs/display/ROS/Scripting#Scripting-Commoncommands) 命令创建的文件或手工编写的文件中导入配置。

#### 打印参数

print命令有几个参数:

| 参数               | 说明                                                                                                                 | 例子                                       |
| ------------------ | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| **append**         |                                                                                                                      |                                            |
| **as-value**       | print output as an array of parameters and its values                                                                | `:put [/ip address print as-value]`        |
| **brief**          | print brief description                                                                                              |                                            |
| **detail**         | print detailed description, the output is not as readable as brief output but may be useful to view all parameters   |
| **count-only**     | print only count of menu items                                                                                       |                                            |
| **file**           | print output to a file                                                                                               |
| **follow**         | print all current entries and track new entries until ctrl-c is pressed, very useful when viewing log entries        | `/log print follow`                        |
| **follow-only**    | print and track only new entries until ctrl-c is pressed, very useful when viewing log entries                       | `/log print follow-only`                   |
| **from**           | print parameters only from specified item                                                                            | `/user print from=admin`                   |
| **interval**       | continuously print output in a selected time interval, useful to track down changes where `follow` is not acceptable | `/interface print interval=2`              |
| **terse**          | show details in a compact and machine-friendly format                                                                |                                            |
| **value-list**     | show values single per line (good for parsing purposes)                                                              |                                            |
| **without-paging** | If the output does not fit in the console screen then do not stop, print all information in one piece                |                                            |
| **where**          | expressions followed by where parameters can be used to filter outmatched entries                                    | `/ip route print where interface="ether1"` |

一次可以指定多个参数，例如: /ip route print count-only interval=1 where interface="ether1"

## 循环和条件语句

### 循环

| 命令          | 语法                                                                                    | 说明                                               |
| ------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------- |
| **do..while** | `:do { <commands> } while=( <conditions> ); :while ( <conditions> ) do={ <commands> };` | execute commands until a given condition is met.   |
| **for**       | `:for <var> from=<int> to=<int> step=<int> do={ <commands> }`                           | execute commands over a given number of iterations |
| **foreach**   | `:foreach <var> in=<array> do={ <commands> };`                                          | execute commands for each element in a list        |

### 条件语句

| 命令   | 语法                                                               | 说明                                                                                                                                 |
| ------ | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| **if** | `:if (<condition>) do={<commands>} else={<commands>} <expression>` | If a given condition is `true` then execute commands in the `do` block, otherwise execute commands in the `else` block if specified. |

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
/system script add name=myScript source=":put \"Hello $myVar !\""
 
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

## Operations with Arrays

**Warning:** Key name in the array contains any character other than a lowercase character, it should be put in quotes

For example:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@ce0] &gt; {</code><code class="ros constants">:</code><code class="ros functions">local </code><code class="ros plain">a { </code><code class="ros string">"aX"</code><code class="ros plain">=1&nbsp;</code><code class="ros plain">;; </code><code class="ros value">ay</code><code class="ros plain">=2</code> <code class="ros plain">};&nbsp;</code><code class="ros constants">:</code><code class="ros functions">put </code><code class="ros plain">(</code><code class="ros keyword">$a</code><code class="ros plain">-&gt;</code><code class="ros string">"aX"</code><code class="ros plain">)}</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">1</code></div></div></td></tr></tbody></table>

**Loop through keys and values**

"foreach" command can be used to loop through keys and elements:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@ce0] &gt;&nbsp;</code><code class="ros constants">:</code><code class="ros functions">foreach </code><code class="ros plain">k,v </code><code class="ros value">in</code><code class="ros plain">=</code><code class="ros plain">{2; </code><code class="ros string">"aX"</code><code class="ros plain">=1&nbsp;</code><code class="ros plain">;; </code><code class="ros value">y</code><code class="ros plain">=2</code><code class="ros plain">; 5} </code><code class="ros value">do</code><code class="ros plain">=</code><code class="ros plain">{</code><code class="ros constants">:</code><code class="ros functions">put </code><code class="ros plain">(</code><code class="ros string">"$k=$v"</code><code class="ros plain">)}</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros value">0</code><code class="ros plain">=2</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros value">1</code><code class="ros plain">=5</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros value">aX</code><code class="ros plain">=1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros value">y</code><code class="ros plain">=2</code></div></div></td></tr></tbody></table>

If the "foreach" command is used with one argument, then the element value will be returned:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@ce0] &gt;&nbsp;</code><code class="ros constants">:</code><code class="ros functions">foreach </code><code class="ros plain">k </code><code class="ros value">in</code><code class="ros plain">=</code><code class="ros plain">{2; </code><code class="ros string">"aX"</code><code class="ros plain">=1&nbsp;</code><code class="ros plain">;; </code><code class="ros value">y</code><code class="ros plain">=2</code><code class="ros plain">; 5} </code><code class="ros value">do</code><code class="ros plain">=</code><code class="ros plain">{</code><code class="ros constants">:</code><code class="ros functions">put </code><code class="ros plain">(</code><code class="ros string">"$k"</code><code class="ros plain">)}</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">2</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">5</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">1</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">2</code></div></div></td></tr></tbody></table>

**Note:** If the array element has a key then these elements are sorted in alphabetical order, elements without keys are moved before elements with keys and their order is not changed (see example above).

**Change the value of a single array element**

```
[admin@MikroTik] > :global a {x=1; y=2}
[admin@MikroTik] > :set ($a->"x") 5 
[admin@MikroTik] > :environment print 
a={x=5; y=2}

```

# Script repository

**Sub-menu level:** `/system script`

Contains all user-created scripts. Scripts can be executed in several different ways:

- **on event** \- scripts are executed automatically on some facility events ( [scheduler](https://help.mikrotik.com/docs/display/ROS/Scheduler), [netwatch](https://help.mikrotik.com/docs/display/ROS/Netwatch), [VRRP](https://help.mikrotik.com/docs/display/ROS/VRRP))
- **by another script** \- running script within the script is allowed
- **manually** \- from console executing a run command or in winbox

**Note:** Only scripts (including schedulers, netwatch, etc) with equal or higher permission rights can execute other scripts.

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                                                                                                  |
 | ------------------------------------------------------------------------------------------------ | ---------------------------------- |
 | **comment** (_string_; Default: )                                                                | Descriptive comment for the script |
 | **dont-require-permissions** (_yes                                                               | no_; Default: _no_)                | Bypass permissions check when the script is being executed, useful when scripts are being executed from services that have limited permissions, such as [Netwatch](https://wiki.mikrotik.com/wiki/Manual:Tools/Netwatch "Manual:Tools/Netwatch") |
 | **name** (_string_; Default: _"Script\[num\]"_)                                                  | name of the script                 |
 | **policy** (_string_; Default: ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon) | list of applicable policies:       |

- **ftp** \- can log on remotely via FTP and send and retrieve files from the router
- **password** \- change passwords
- **policy** \- manage user policies, add and remove user
- **read** \- can retrieve the configuration
- **reboot** \- can reboot the router
- **sensitive** \- allows changing "hide sensitive" parameter
- **sniff** \- can run sniffer, torch, etc
- **test** \- can run ping, traceroute, bandwidth test
- **write** \- can change the configuration

Read more detailed policy descriptions [here](https://help.mikrotik.com/docs/display/ROS/User)

 |
| **source** (_string_;) | Script source code |

Read-only status properties:

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                           |
 | ------------------------- | --------------------------------------------------------------- |
 | **last-started** (_date_) | Date and time when the script was last invoked.                 |
 | **owner** (_string_)      | The user who created the script                                 |
 | **run-count** (_integer_) | Counter that counts how many times the script has been executed |

Menu specific commands

| 
Command

 | 

Description

 |     |
 | --- |  |
 |     |

Command

 | 

Description

 |                    |
 | ------------------ | -------- |
 | **run** (_run \[id | name\]_) | Execute the specified script by ID or name |

## Environment

**Sub-menu level:**

- `/system script environment`
- `/environment`

Contains all user-defined variables and their assigned values.

```
[admin@MikroTik] > :global example;
[admin@MikroTik] > :set example 123
[admin@MikroTik] > /environment print  
"example"=123

```

  
Read-only status properties:

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                     |
 | ------------------- | -------------------------------- |
 | **name** (_string_) | Variable name                    |
 | **user** (_string_) | The user who defined variable    |
 | **value** ()        | The value assigned to a variable |

## Job

**Sub-menu level:** `/system script job`

Contains a list of all currently running scripts.  
Read-only status properties:

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                      |
 | -------------------- | ----------------------------------------------- |
 | **owner** (_string_) | The user who is running the script              |
 | **policy** (_array_) | List of all policies applied to the script      |
 | **started** (_date_) | Local date and time when the script was started |

# See also

- [Scripting Examples](https://help.mikrotik.com/docs/display/ROS/Scripting+examples)
- [Manual: Scripting Tips and Tricks](https://wiki.mikrotik.com/wiki/Manual:Scripting_Tips_and_Tricks "Manual:Scripting Tips and Tricks")