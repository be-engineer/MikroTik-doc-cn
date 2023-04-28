# 概述

可以把GSM调制解调器连接到RouterOS设备上，用它来发送和接收短信。RouterOS将这种调制解调器列为串口，出现在 _/port print_ 列表中。GSM标准定义了发送SMS信息的AT命令，并定义了这些命令中信息的编码方式。

高级工具包提供了命令 _/tool sms send_，使用标准的GSM AT命令来发送短信。

# 发送

`/tool sms send`

## 例子

为ppp接口发送命令：

`/tool sms send usb3 "20000000" \ message="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#\$%^&*(){}[]\"'~"`

对于LTE接口，在端口栏中使用LTE接口名称：

`/tool sms send lte1 "20000000" \ message="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#\$%^&*(){}[]\"'~"`

| 参数                        | 说明                                                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **port** (_string_)         | GSM调制解调器所连接的 _/port_ 列表中的端口名称。                                                                          |
| **phone-number** (_string_) | 接收方电话号码。允许的字符是 "0123456789*#abc"。如果第一个字符是 "+"，则电话号码类型被设置为 _国际_，否则被设置为_未知_。 |
| **channel** (_integer_)     | 发送时使用哪个调制解调器频道。                                                                                            |
| **message** (_string_)      | 信息内容。它使用GSM 7编码（目前不支持UCS2），所以消息长度限制在160个字符（字符^{}\\[]~                                    |  |
| **smsc** (_string_)         |                                                                                                                           |
| **type** (_string_)         | 如果设置为 _class-0_，则发送0类短信。它会立即显示，而不存储在手机中。                                                     |

# USSD信息

USSD（非结构化补充服务数据）信息可用于与移动网络供应商沟通，以接收额外的信息，启用额外的服务或向预付卡添加资金。USSD信息可以通过使用AT命令来处理（命令可能不同，甚至可能在某些调制解调器上被阻止）。

**必须激活3G或GSM网络模式才能使用这一功能**，因为仅在LTE模式下不支持这一功能（**R11e-LTE** 调制解调器自动切换到3G模式来发送USSD消息）。

PDU（协议数据单元）消息及其解密版本会在LTE调试日志中打印出来。

## 示例

检查LTE调试日志是否激活：

```shell
/system logging print
Flags: X - disabled, I - invalid, * - default
# TOPICS ACTION PREFIX
0 * info memory
1 * error memory
2 * warning memory
3 * critical echo
```

如果没有日志条目，则运行命令来添加：

```shell
/system logging add topics=lte,!raw
 
/system logging print
Flags: X - disabled, I - invalid, * - default
# TOPICS ACTION PREFIX
0 * info memory
1 * error memory
2 * warning memory
3 * critical echo
4 lte,!raw memory
```

要从*245#接收账户状态 

```shell
/interface lte at-chat lte1 input="AT+CUSD=1,\"*245#\",15"
output: OK
/log print
11:51:20 lte,async lte1: sent AT+CUSD=1,"*245#",15
11:51:20 lte,async lte1: rcvd OK
11:51:23 lte,async,event +CUSD: 0,"EBB79B1E0685E9ECF4BADE9E03", 0
11:51:23 gsm,info USSD: konta atlikums
```

# 接收

从v3.24开始，RouterOS也支持接收短信，并且可以执行脚本，甚至回复发件人。

在路由器可以接收短信之前，需要在一般的 **/tool sms** 菜单中进行相关配置。以下是可配置的参数：

| 参数                                               | 说明                                                                                                                                                                               |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **allowed-number** (_string_; Default: "")         | 允许运行命令的发送者号码，必须指定国家代码，如：+371XXXXXXX。                                                                                                                      |
| **channel** (_integer_; Default: **0**)            | 接收时使用哪个调制解调器频道。                                                                                                                                                     |
| **keep-max-sms** (_integer_; Default: **0**)       | 将保存的最大信息数量。如果设置的这个数字大于SIM卡支持的数字，新的信息将不会接收 从RouterOS v6.44.6开始被 **自动擦除** 参数所取代。                                                 |
| **auto-erase** (_yes \| no_; Default: **no**)      | 自动读取SIM卡存储大小。当 **auto-erase=no**时，如果存储空间已满，将不会收到新的短信。设置 **auto-erase=yes**，可以自动删除收到的最旧短信，为新短信释放空间。从6.44.6版本开始可用。 |
| **port** (_string_; Default: (**unknown**))        | 调制解调器端口（调制解调器只能由一个进程使用 "/port> print" ）                                                                                                                     |
| **receive-enabled** (_yes \| no_; Default: **no**) | 必须打开才能接收信息。                                                                                                                                                             |
| **secret** (_string_; Default: "")                 | 秘密密码，必须打开。                                                                                                                                                               |

**Basic Example configuration to be able to view received messages:**

```shell
/tool sms set receive-enabled=yes port=lte1
 
/tool/sms/print
           status: running
  receive-enabled: yes
             port: lte1
          channel: 0
           secret:
   allowed-number:
       auto-erase: no
          sim-pin:
        last-ussd:
```

## Inbox

`/tool sms inbox`

如果启用了阅读器，会在这个子菜单中看到收到的信息：

只读属性：

| 属性                   | 描述                                                           |
| ---------------------- | -------------------------------------------------------------- |
| **phone** (_string_)   | 发送者的电话号码。                                             |
| **message** (_string_) | 信息主体                                                       |
| **timestamp** (_time_) | 收到信息的时间。它是运营商发送的时间，而不是路由器的本地时间。 |
| **type** (_string_)    | 消息类型                                                       |

## 语法

`:cmd SECRET script NAME [[ VAR[=VAL] ] ... ]`

- **SECRET** - 密码
- **NAME** - 脚本的名称，可在"/system script "中找到。
- **VAR** - 传递给脚本的变量（以VAR或VAR=value的形式传递），用空格分隔。

其他需要记住的事情：

- 如果有必要，参数可以放在引号中 "VAR"="VAL"
- 不支持值的转义（VAR="\"）
- 不支持组合短信，每条短信都会被单独处理
- 不支持16位的unicode信息
- 短信是用标准的GSM7字母解码的，所以你不能用其他编码发送，否则会被错误地解码

## 例子

**错误:**

```shell
:cmd script mans_skripts
:cmd slepens script mans skripts
:cmd slepens script mans_skripts var=
:cmd slepens script mans_skripts var= a
:cmd slepens script mans_skripts var=a a
```

**正确:**

```shell
:cmd slepens script mans_skripts
:cmd slepens script "mans skripts"
:cmd slepens script mans_skripts var
:cmd slepens script mans_skripts var=a
:cmd slepens script mans_skripts var="a a"
```

# 调试

_/tool sms send_ 命令正在记录写入和读取的数据。它用标签 _gsm,debug,write_ 和 _gsm,debug,read_ 来记录，更多信息见系统日志。

# 实施细节

使用 _AT+CMGS_ 和 _AT+CMGF_ 命令。端口在命令执行期间被获取，不能被其他RouterOS组件同时使用。信息发送过程可能需要很长的时间，在最初的AT命令交换过程中，一分钟后和两秒钟后就会超时。