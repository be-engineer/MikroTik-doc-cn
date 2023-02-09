# 概述

**Sub-menu:** `/system watchdog`

这个菜单允许配置系统重新启动，如果特定的IP地址没有反应，或者当它检测到软件已经锁定时。这种检测有两种方式。

- 软件看门狗定时器（大多由硬件故障引起）设备可以通过重启来恢复自己。
- Ping看门狗可以监测到与特定IP地址的连接并触发重启功能。

**注意：** 这是两个不同的看门狗功能，有各自的设置。默认情况下，软件看门狗被启用，ping看门狗被禁用。可以通过指定一个IP地址来启用ping看门狗，可以取消Watchdog Timer选项来禁用软件看门狗。

## 属性

| 属性                                                                 | 说明                                                                                                                                                    |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **auto-send-supout** (_yes                 \| no_; Default: **no**)  | 输出文件自动生成后，可以通过电子邮件发送。                                                                                                              |
| **auto-supout** (_yes                      \| no_; Default：**yes**) | 当软件发生故障时，会自动生成一个名为 "autosupout.rif "的文件。之前的 "autosupout.rif "文件被重命名为 "autosupout.old.rif"。                             |
| **no-ping-delay** (_time_; Default: 5m)                              | 在试图到达监视地址之前要等待多长时间。                                                                                                                  |
| **ping-timeout** (_time_; Default: 60s)                              | 设备被ping 6次的时间间隔（在 "no-ping-delay "之后）。                                                                                                   |
| **send-email-from** (_string_; Default: )                            | 发送支持输出文件的电子邮件地址。如果没有设置，则使用/tool电子邮件中设置的值。                                                                           |
| **send-email-to** (_string_; Default: )                              | 发送支持输出文件的电子邮件地址。                                                                                                                        |
| **send-smtp-server** (_string_; Default: )                           | 发送支持输出文件的SMTP服务器地址。如果没有设置，则使用/tool电子邮件中设置的值。                                                                         |
| **watch-address** (_IP_; Default: )                                  | 系统将重启，如果连续6次ping到给定的IP地址都失败。如果设置为无，该功能将禁用。默认情况下，如果设置了watch-address并且无法到达，路由器将每6分钟重启一次。 |
| **watchdog-timer** (_yes                   \| no_; Default: **yes**) | 如果系统一分钟内没有反应，是否重启。                                                                                                                    |

## 快速例子

使系统产生一个支持输出文件，并在软件崩溃的情况下通过192.0.2.1自动发送至support@example.com。

```shell
[admin@MikroTik] system/watchdog/ set auto-send-supout=yes \
\... send-to-email=support@example.com send-smtp-server=192.0.2.1
[admin@MikroTik] system watchdog> print
      watch-address: none
     watchdog-timer: yes
      no-ping-delay: 5m
   automatic-supout: yes
   auto-send-supout: yes
   send-smtp-server: 192.0.2.1
      send-email-to: support@example.com
```
