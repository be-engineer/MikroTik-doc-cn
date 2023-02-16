# 概述

**Sub-menu:** `/ip kid-control`

"儿童控制 "是一种家长控制功能，用于限制局域网设备的互联网连接。

## 属性描述

在这个菜单中，可以为每个孩子创建一个配置文件，并限制互联网的访问。

| 属性                                                                 | 说明                                                   |
| -------------------------------------------------------------------- | ------------------------------------------------------ |
| **name** (_string_)                                                  | 孩子的资料名称                                         |
| **mon,tue,wed,tu,fri,sat,sun** (_time_)                              | 一周中的每一天。选择一天中的时间，这时允许互联网访问。 |
| **disabled** (_yes \| no_)                                           | 是否启用限制功能                                       |
| **rate-limit** (_string_)                                            | 流量的最大可用速率。                                   |
| **tur-mon,tur-tue,tur-wed,tur-thu,tur-fri,tur-sat,tur-sun** (_time_) | 无限时速率。选择一天中的时间，这时上网无限制。         |

无时间限制的速率比速率限制参数有更高的优先权。

## 设备

**Sub-menu：** `/ip kid-control device`。

如果有多个设备连接到互联网（手机、平板电脑、游戏机、电视等），该子菜单会包含信息。设备是通过ARP表中检索的MAC地址来识别的，IP地址从那里获取。

| 属性                              | 说明                           |
| --------------------------------- | ------------------------------ |
| **name** (_string_)               | 设备名称                       |
| **mac-address** (_string_)        | 设备mac-address                |
| **user** (_string_)               | 将设备附加到哪个配置文件中     |
| **reset-counters** (_[id, name]_) | 重置字节数增加和减少的计数器。 |

## 应用例子

以下例子将限制Peters手机的访问。

- 禁止在周一、周三和周五访问互联网
- 允许在以下时间段无限制上网。
  - 星期二
  - 星期四11:00-22:00
  - 周日15:00-22:00
- 周六18:30-21:00，Peters移动电话的带宽限制为3Mbps。

`[admin@MikroTik] > /ip kid-control add name =Peter mon = "" tur-tue = "00:00-24h" wed = "" tur-thu = "11:00-22:00" fri = "" sat = "18:30-22:00" tur-sun = "15h-21h" rate-limit =3M`

`[admin@MikroTik] > /ip kid-control device add name =Mobile-phone user =Peter mac-address =FF:FF:FF:ED:83:63`

互联网访问限制是通过添加动态防火墙过滤规则或简单的队列规则实现的。下面是防火墙过滤规则的例子:

```shell
[admin@MikroTik] > /ip firewall filter print
1  D ;;; Mobile-phone, kid-control
      chain =forward action =reject src-address =192.168.88.254
2  D ;;; Mobile-phone, kid-control
      chain =forward action =reject dst-address =192.168.88.254
```

动态创建的简单队列:

```shell
[admin@MikroTik] > /queue simple print
Flags : X - disabled, I - invalid, D - dynamic
 1  D ;;; Mobile-phone, kid-control
      name = "queue1" target =192.168.88.254/32 parent =none packet-marks = "" priority =8/8 queue =default-small/default-small limit-at =3M/3M max-limit =3M/3M burst-limit =0/0
      burst-threshold =0/0 burst-time =0s/0s bucket-size =0.1/0.1
```

可以监控特定设备的数据使用量:

```shell
[admin@MikroTik] > /ip kid-control device print stats
Flags : X - disabled, D - dynamic, B - blocked, L - limited, I - inactive
 1 BI Mobile-phone                                                                                                               30s         0bps      0bps    3438.1KiB       8.9KiB
```

也可以 **暂停** 所有的限制，然后在你想要的时候 **恢复** 它们:

```shell
[admin@MikroTik] > /ip kid-control pause Peter
[admin@MikroTik] > /ip kid-control print
Flags : X - disabled, P - paused, B - blocked, L - rate-limited
 0 PB Peter                                                                                                                 15h-21h                             11h-22h          18 :30h-22h
```
