# GPIO

**注**： 为了访问GPIO设置，确保事先安装了 **iot** [包](https://help.mikrotik.com/docs/display/ROS/Packages)。

可以按照 [链接](https://en.wikipedia.org/wiki/General-purpose_input/output) 找到更多关于GPIO的信息。

GPIO是通用输入/输出的意思。它是路由器板上的一个数字信号引脚，允许发送/接收信号。可以在不同的情况下发挥作用，比如：

1.  通过ADC输入测量电压
2.  读取从另一个设备收到的0和1信号--"干触点"
3.  通过向引脚发送逻辑0或1信号来控制连接的继电器

## RouterOS配置

**注**:  GPIO设置只能使用CLI。

**Sub-menu:** `/iot gpio`

GPIO设置分为：

- 模拟 (/iot gpio analog)
- 数字 (/iot gpio digital)

**注**：在下面的例子中使用 [KNOT](https://mikrotik.com/product/knot) 作为一个参考设备。其他设备可能有不同的引脚布局，但同样的原则适用。

请注意长期版（6.47.10）和稳定版（6.48.3），必须使用"/system gpio"命令，与"/iot gpio "例子中的相同，除了 "模拟 "和 "数字"子菜单，这是在后来的版本中添加的。6.49beta54以上版本和RouterOS v7，使用"/iot gpio "子菜单。

### /iot gpio analog

**注**：请在产品页上检查你的硬件是否支持模拟输入。

在 "模拟"设置中，可以测量模拟输入/ADC输入引脚上的电压：

```shell
[admin@device] /iot gpio analog> print
 # NAME                                                                                     VALUE       OFFSET
 0 pin2                                                                                       0mV          0mV
 1 pin3                                                                                      32mV          0mV
```

"OFFSET "可用于手动补偿导线上的电压降。"VALUE "的测量方法是：

value=adc_input+offset

其中adc_input是引脚上的电压。

"OFFSET "配置实例如下：

```shell
[admin@device] /iot gpio analog> set pin2 offset 
 
Offset ::= [-]Num[mV]
  Num ::= -2147483648..2147483647    (integer number)
 
[admin@device] /iot gpio analog> set pin2 offset 2  
[admin@device] /iot gpio analog> print           
 # NAME                                                                                           VALUE       OFFSET
 0 pin2                                                                                             2mV          2mV
 1 pin3                                                                                             0mV          0mV
```

### /iot gpio digital

 "数字 "部分可以使用数字输出/输入引脚发送/接收一个逻辑0或1信号（输出引脚是 "漏极开路"）：

```shell
[admin@device] /iot gpio digital> print            
Flags: X - disabled
 #   NAME                                        DIRECTION OUTPUT INPUT SCRIPT                                  
 0   pin5                                        input     0      0   
 1   pin4                                        output    0    
 2   pin6                                        output    0    
```

引脚的 "方向 "可以是 "输入"（接收信号的引脚）或 "输出"（发送信号的引脚）。

当引脚的方向被设置为 "输出 "时，可以配置 "OUTPUT "值。改变 "OUTPUT "值可以将信号发送到该引脚。

```shell
[admin@device] /iot gpio digital> set pin4 output=
 
Output ::= 0 | 1
 
 
[admin@device] /iot gpio digital> set pin4 output=1       
[admin@device] /iot gpio digital> print           
Flags: X - disabled
 #   NAME                                        DIRECTION OUTPUT INPUT SCRIPT                                     
 0   pin5                                        input     0      0   
 1   pin4                                        output    1    
 2   pin6                                        output    0    
```

"SCRIPT "字段允许配置一个脚本，每当 "INPUT "或 "OUTPUT "值发生变化（从0到1或从1到0）时，该脚本就会启动。

```shell
[admin@device] /iot gpio digital> set pin4 script=script1
[admin@device] /iot gpio digital> set pin5 script="/system .."  
[admin@device] /iot gpio digital> print                      
Flags: X - disabled
 #   NAME                                        DIRECTION OUTPUT INPUT SCRIPT                                     
 0   pin5                                        input     0      0     /system ..                                 
 1   pin4                                        output    1            script1                                    
 2   pin6                                        output    0    
```
## 不同的场景

### 控制继电器

GPIO实现的场景之一是使用数字输出引脚 "控制其他继电器"。基本上，发送 "0 "或 "1 "信号给连接到该引脚的单元。为了使这个过程自动化，你可以使用一个 [时间表](https://wiki.mikrotik.com/wiki/Manual:System/Scheduler)，它将在特定时间运行脚本。

例如，可以添加第一个 [脚本](https://help.mikrotik.com/docs/display/ROS/Scripting) （如下图所示的单行）并命名为 "output=0"：

> /iot gpio digital set pin4 output=0

然后添加第二个脚本（如下图所示的单行）并命名为 "output=1"：

> /iot gpio digital set pin4 output=1

有了这两个脚本，你就可以配置一个时间表：

`[admin@device] /system scheduler> add name=run-30s interval=30s on-event="output=0"`

上图所示的时间表配置将每隔30秒运行名称为 "output=0 "的脚本。

`[admin@device] /system scheduler> add name=run-45s interval=45s on-event="output=1"`

上图所示的时间表配置将每隔45秒运行名称为 "output=1 "的脚本。

因此，设备将每隔30秒自动向第4针（数字输出针）发送一个输出值为0的信号，每隔45秒发送一个输出值为1的信号。

可以根据需要改变预定的时间。

### 监控输入信号

另一种情况是使用数字输入引脚来 "监测输入信号"。需要一个脚本，每当direction="input "的引脚的 "INPUT "值发生变化时（RouterOS设备从连接到该引脚的另一个设备接收到 "0或1 "的信号时），就会启动电子邮件通知或MQTT/HTTPS获取发布。

_E-mail提示脚本:_

`/tool e-mail send to=config@[mydomain.com](http://mydomain.com) subject=[/system identity get name] body="$[/iot gpio digital get pin5 input]"`

创建脚本后，将其应用/设置到 "输入 "引脚：

```shell
[admin@device] /iot gpio digital> set pin5 script=script1
[admin@device] /iot gpio digital> print                 
Flags: X - disabled
 #   NAME                     DIRECTION OUTPUT INPUT SCRIPT                   
 0   pin5                     input     0      0     script1                  
 1   pin4                     output    0            script1                  
 2   pin6                     output    0    
 ```

在上面的例子中，电子邮件通知脚本被命名为 "script1"。

因此，每当输入值发生变化（从0到1或从1到0），脚本就会自动启动一个电子邮件通知，在电子邮件正文中显示输入值。

不要忘记修改脚本行，并相应地配置电子邮件设置（[/tool e-mail](https://help.mikrotik.com/docs/display/ROS/E-mail)）：

> /tool e-mail send to="config@[mydomain.com](http://mydomain.com)" subject="[/system identity get name]" body="$[/iot gpio digital get pin5 input] "

配置使用的电子邮件地址，也可以根据你的需要改变邮件的主题和正文。

_MQTT 发布脚本:_

> :local broker "name"
> 
> :local topic "topic"
> 
> :local message "{\"inputVALUE\":$[/iot gpio digital get pin5 input]}"  
> /iot mqtt publish broker=$broker topic=$topic message=$message

这个脚本的工作方式与"e-mail notification"脚本相同，只是当输入值发生变化时，脚本会启动MQTT发布（而不是电子邮件通知），并以JSON格式发送针脚上收到的输入值。

不要忘记设置MQTT代理（/iot mqtt brokers add ...），并事先修改几行脚本：

> :local broker "name"

broker 的 "名字 "也要相应地改变（可以用CLI命令/iot mqtt brokers print来检查所有创建的broker 和名字）。

> :local topic "topic"

主题也要改变。主题本身是在服务器端配置的，所以要确保使用正确的主题。

不要忘记应用脚本到pin5（/iot gpio digital set pin5 script=script_name），如上面的 "电子邮件通知 "例子所示。

如果使用机械开关来发送信号到GPIO引脚，建议使用下面的脚本来代替（ 防止在引脚上收到信号时，脚本启动不止一次）：

```shell
 :global gpioscriptrunning;  
 if (!$gpioscriptrunning) do={:set $gpioscriptrunning true;  
 :log info "script started - GPIO changed";  
 :do {if ([/iot gpio digital get pin5 input] = "0") do={/tool e-mail send to="config@[mydomain.com](http://mydomain.com)" subject=[/system identity get name] body="pin5 received logical 0"} else {/tool e-mail send to="config@[mydomain.com](http://mydomain.com)" subject=[/system identity get name]  body="pin5 received logical 1"};  
 :delay 1s;  
 :set $gpioscriptrunning false} on-error={:set $gpioscriptrunning false;  
 :log info "e-mail error, resetting script state..."}}
```

如果GPIO引脚的状态在mili/microseconds内变化超过一次 - 上面的脚本将确保电子邮件通知不会被发送超过一次。

### 监测电压

最后但并非不重要的是，使用模拟引脚来 "监测电压"。 需要一个脚本，按计划读取监测电压，然后通过电子邮件、MQTT或HTTPS（获取）发送数据。

创建一个脚本，如下图所示。在这个例子中使用MQTT发布（可以用"/tool e-mail ... "创建一个类似的脚本来使用电子邮件通知）：

> :local broker "name"
> 
> :local topic "topic"
> 
> :local message "{\"voltage(mV)\":$[/iot gpio analog get pin3 value]}"  

> /iot mqtt publish broker=$broker topic=$topic message=$message

该脚本读取测量引脚3的电压，并将数据发布到MQTT代理。

不要忘记设置MQTT代理（/iot mqtt brokers add ...），并事先改变几行脚本：

> :local broker "name"

 broker的 "名字 "也应该相应地改变（可以用CLI命令/iot mqtt brokers print检查所有创建的broker和名字）。

> :local topic "topic"

主题也要改变。主题本身是在服务器端配置的，所以要确保使用正确的主题。

保存脚本并命名，例如，"voltagepublish"。为了使这个过程自动化，可以使用 [计划表](https://wiki.mikrotik.com/wiki/Manual:System/Scheduler)。

`[admin@device] /system scheduler> add name=run-45s interval=45s on-event="voltagepublish"`

上面显示的时间表配置将每45秒运行一次脚本。
