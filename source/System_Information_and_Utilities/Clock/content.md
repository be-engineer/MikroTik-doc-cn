# 介绍

RouterOS使用来自TZ数据库的数据，该数据库中的大部分时区都包含在内，并且具有相同的名称。由于路由器上的本地时间主要用于时间戳和与时间相关的配置，而不是用于历史日期计算，因此不包括过去年份的时区信息。目前只包括2005年以后的资料。

以下设置可在/system clock控制台路径和system > clock WinBox窗口的Time选项卡中进行。

启动日期和时间为jan/02/1970 00:00:00 [+|-]gmt-offset。

# Properties

| Property                                                                      | Description                                                                                                                                                                                                                                                                                |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **time** (_HH:MM:SS);_                                                        | _HH_ - 小时 00..24, _MM_ - 分钟 00..59, _SS_ - 秒 00..59                                                                                                                                                                                                                                   |
| **date** (_mmm/DD/YYYY);_                                                     | _mmm_ - 月, 为 _jan_, _feb_, _mar_, _apr_, _may_, _jun_, _jul_, _aug_, _sep_, _oct_, _nov_, _dec_ 之一, _DD_ - 日期, 00..31, _YYYY_ - 年, 1970..2037: **date** 和 **time** 显示路由器上当前的本地时间。这些值可以用 **set** 命令进行调整。但是，本地时间不能导出，也不与其他配置一起存储。 |
| **time-zone-name** (_manual_, or name of time zone; default value: _manual_); | 时区名称。和RouterOS中的大多数文本值一样，该值区分大小写。特殊值手动应用 [手动配置的GMT偏移](https://wiki.mikrotik.com/wiki/Manual:System/Time#Manual_time_zone_configuration)，默认值为 _00:00_，没有夏令时。                                                                             |
| **time-zone-autodetect** (_yes_ or _no_; default: yes);                       | 从v6.27开始提供的特性。如果启用，将自动设置时区。                                                                                                                                                                                                                                          |

在新安装的RouterOS和重置配置后，默认启用Time-zone-autodetect。根据路由器的公共IP地址和我们的云服务器数据库检测时区。从RouterOS v6.43开始，你的设备将使用 [cloud2.mikrotik.com](http://cloud2.mikrotik.com) 与MikroTik的云服务器进行通信。旧版本将使用 [cloud.mikrotik.com](http://cloud.mikrotik.com) 与MikroTik的云服务器进行通信。

配置

## 活动时区信息

- **dst-active** (_yes_ 或 _no_>;只读属性):当当前时区的夏令时处于激活状态时，该属性的值为 _yes_。
- **gmt-offset** ([+|-] HH: MM -小时和分钟的偏移;只读属性):这是在应用基本时区偏移量和现行夏令时偏移量之后，系统使用的GMT偏移量的当前值。

## 手动配置时区

这些设置可在 **/system clock manual** 控制台路径和“system > clock”WinBox窗口的“manual Time Zone”选项卡中看到。这些设置只有当 **time-zone-name**\= _manual_ 时才可用。只能手动配置单个夏令时时段。

- **time-zone** ， **dst-delta** ([+|-]HH:MM -以小时和分钟为单位的时间偏移量，前导加号可选;默认值:_+00:00_):当夏令时未激活时，使用GMT偏移量 **时区**。当夏令时有效时，使用GMT偏移量 **时区** + **DST-delta** 。
- **dst-start** ， **dst-end** (_mmm/DD/YYYY HH:MM: SS_ -日期和时间，在 **set** 命令中可以省略日期或时间;默认值:_jan/01/1970 00:00:00_):夏令时开始和结束的本地时间。