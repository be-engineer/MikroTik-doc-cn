## 概述

调度程序可以在指定的时间间隔或两者兼而有之的特定时间时刻触发脚本执行。

## 特性

 -  **Interval** （时间;默认值：0s）-两个脚本执行之间的间隔，如果将时间间隔设置为零，则仅在开始时间执行脚本，否则在时间间隔内重复执行它 指定的
 -  **名称** （名称）-任务名称
 -  **on-event** （名称）-执行脚本的名称。 必须在 /系统脚本上显示
 -  **run-count** （仅读取：integer）-要监视脚本用法，每次执行脚本时，此计数器都会增加
 -  **开始日期** （日期）-第一个脚本执行的日期
 -  **开始时间** （时间）-第一个脚本执行时间的时间
 -  **启动**  - 系统启动后3秒执行脚本。

## 说明

重启路由器将重置运行计数计数器。

如果必须同时执行多个脚本，则按照它们在调度器配置中出现的顺序执行。如果使用一个调度脚本禁用另一个调度脚本，这一点可能很重要。

如果需要更复杂的执行模式，通常可以通过调度多个脚本，并使它们相互启用和禁用来完成。

**注意:** 如果调度器项的启动时间设置为startup，它的行为就好像启动时间和开始日期设置为控制台启动后3秒的时间。这意味着所有具有' start-time is startup'和'interval is 0'的脚本将在每次路由器启动时执行一次。如果间隔设置为0以外的值，调度器将不在启动时运行

  

## 例子

添加一个任务，每小时执行一次log-test脚本:

```shell
[admin@MikroTik] system script> add name=log-test source=":log info message=test"
[admin@MikroTik] system script> print
Flags: I - invalid
0 name="log-test" owner="admin" policy=ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon dont-require-permissions=no run-count=0
source=:log info message=test
[admin@MikroTik] system script> .. scheduler
[admin@MikroTik] system scheduler> add name=run-1h interval=1h
on-event=log-test
[admin@MikroTik] system scheduler> print
Flags: X - disabled
# NAME ON-EVENT START-DATE START-TIME INTERVAL RUN-COUNT
0 run-1h log-test mar/30/2004 06:11:35 1h 0
[admin@MikroTik] system scheduler>
```

  

在另一个示例中，将添加两个脚本，它们将更改队列规则“Cust0”的带宽设置。每天上午9点，队列将设置为64Kb/s，下午5点，队列将设置为128Kb/s。队列规则、脚本和调度器任务如下:

```shell
[admin@MikroTik] queue simple> add name=Cust0 interface=ether1 \
\... dst-address=192.168.0.0/24 limit-at=64000
 [admin@MikroTik] queue simple> print
 Flags: X - disabled, I - invalid 0 name="Cust0" target-address=0.0.0.0/0 dst-address=192.168.0.0/24
 interface=ether1 limit-at=64000 queue=default priority=8 bounded=yes
[admin@MikroTik] queue simple> /system script
[admin@MikroTik] system script> add name=start_limit source={/queue simple set \
 \... Cust0 limit-at=64000}
[admin@MikroTik] system script> add name=stop_limit source={/queue simple set \
\... Cust0 limit-at=128000}
[admin@MikroTik] system script> print
0 name="start_limit" source="/queue simple set Cust0 limit-at=64000"
owner=admin run-count=0
1 name="stop_limit" source="/queue simple set Cust0 limit-at=128000"
owner=admin run-count=0
[admin@MikroTik] system script> .. scheduler
[admin@MikroTik] system scheduler> add interval=24h name="set-64k" \
\... start-time=9:00:00 on-event=start_limit
[admin@MikroTik] system scheduler> add interval=24h name="set-128k" \
 \... start-time=17:00:00 on-event=stop_limit
[admin@MikroTik] system scheduler> print
 Flags: X - disabled
# NAME ON-EVENT START-DATE START-TIME INTERVAL RUN-COUNT
 0 set-64k start... oct/30/2008 09:00:00 1d 0
1 set-128k stop_... oct/30/2008 17:00:00 1d 0
[admin@MikroTik] system scheduler>
```

  

下面的示例调度一个脚本，该脚本每周通过电子邮件发送路由器配置的备份。

```shell
[admin@MikroTik] system script> add name=e-backup source={/system backup
{... save name=email; /tool e-mail send to="root@host.com" subject=([/system
{... identity get name] . " Backup") file=email.backup}
[admin@MikroTik] system script> print
0 name="e-backup" source="/system backup save name=ema... owner=admin run-count=0
 
[admin@MikroTik] system script> .. scheduler
[admin@MikroTik] system scheduler> add interval=7d name="email-backup" \
 \... on-event=e-backup
[admin@MikroTik] system scheduler> print
 Flags: X - disabled
 # NAME ON-EVENT START-DATE START-TIME INTERVAL RUN-COUNT
0 email-... e-backup oct/30/2008 15:19:28 7d 1
[admin@MikroTik] system scheduler>
```

  

不要忘记设置电子邮件，即/tool e-mail下的SMTP服务器和From地址。例如:

```shell
[admin@MikroTik] tool e-mail> set server=159.148.147.198 from=SysAdmin@host.com
[admin@MikroTik] tool e-mail> print
 server: 159.148.147.198
from: SysAdmin@host.com
[admin@MikroTik] tool e-mail>
```

  

下面的例子每个小时把'x'从午夜到中午放入日志中:

```shell
[admin@MikroTik] system script> add name=enable-x source={/system scheduler
{... enable x}
[admin@MikroTik] system script> add name=disable-x source={/system scheduler
{... disable x}
[admin@MikroTik] system script> add name=log-x source={:log info message=x}
[admin@MikroTik] system script> .. scheduler
[admin@MikroTik] system scheduler> add name=x-up start-time=00:00:00 \
\... interval=24h on-event=enable-x
[admin@MikroTik] system scheduler> add name=x-down start-time=12:00:00
 \... interval=24h on-event=disable-x
[admin@MikroTik] system scheduler> add name=x start-time=00:00:00 interval=1h \
\... on-event=log-x
[admin@MikroTik] system scheduler> print
Flags: X - disabled
 # NAME ON-EVENT START-DATE START-TIME INTERVAL RUN-COUNT
0 x-up enable-x oct/30/2008 00:00:00 1d 0
1 x-down disab... oct/30/2008 12:00:00 1d 0
2 x log-x oct/30/2008 00:00:00 1h 0
[admin@MikroTik] system scheduler>
```