# Introduction

RouterOS uses data from the TZ database, Most of the time zones from this database are included, and have the same names. Because local time on the router is used mostly for timestamping and time-dependent configuration, and not for historical date calculations, time zone information about past years is not included. Currently, only information starting from 2005 is included.

Following settings are available in the **/system clock** console path and in the "Time" tab of the "System > Clock" WinBox window.

Startup date and time is **jan/02/1970 00:00:00** \[+|-\]gmt-offset. 

# Properties

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

|     |
| --- |  |
|     |

**time** (_HH:MM:SS);_

 | 

where _HH_ \- hour 00..24, _MM_ \- minutes 00..59, _SS_ \- seconds 00..59).

 |
| **date** (_mmm/DD/YYYY);_ | where _mmm_ \- month, one of _jan_, _feb_, _mar_, _apr_, _may_, _jun_, _jul_, _aug_, _sep_, _oct_, _nov_, _dec_, _DD_ \- date, 00..31, _YYYY_ \- year, 1970..2037): **date** and **time** show current local time on the router. These values can be adjusted using the **set** command. Local time cannot, however, be exported, and is not stored with the rest of the configuration. |
| **time-zone-name** (_manual_, or name of time zone; default value: _manual_); | Name of the time zone. As most of the text values in RouterOS, this value is case sensitive. Special value _manual_ applies [manually configured GMT offset](https://wiki.mikrotik.com/wiki/Manual:System/Time#Manual_time_zone_configuration), which by default is _00:00_ with no daylight saving time. |
| **time-zone-autodetect** (_yes_ or _no_; default: yes); | Feature available from v6.27. If enabled, the time zone will be set automatically. |

 Time-zone-autodetect by default is enabled on new RouterOS installation and after configuration reset. The time zone is detected depending on the router's public IP address and our Cloud servers database. Since RouterOS v6.43 your device will use [cloud2.mikrotik.com](http://cloud2.mikrotik.com) to communicate with MikroTik's Cloud server. Older versions will use [cloud.mikrotik.com](http://cloud.mikrotik.com) to communicate with the MikroTik's Cloud server.

Configuration

## Active time zone information

-   **dst-active** (_yes_ or _no_\>; read-only property): This property has the value _yes_ while daylight saving time of the current time zone is active.
-   **gmt-offset** (\[_+_|_\-_\]_HH:MM_ \- offset in hours and minutes; read-only property): This is the current value of GMT offset used by the system, after applying base time zone offset and active daylight saving time offset.

## Manual time zone configuration

These settings are available in **/system clock manual** console path and in the "Manual Time Zone" tab of the "System > Clock" WinBox window. These settings have an effect only when **time-zone-name**\=_manual_. It is only possible to manually configure single daylight saving time period.

-   **time-zone**, **dst-delta** (\[_+_|_\-_\]_HH:MM_ \- time offset in hours and minutes, leading plus sign is optional; default value: _+00:00_) : While DST is not active use GMT offset **time-zone**. While DST is active use GMT offset **time-zone** + **dst-delta**.
-   **dst-start**, **dst-end** (_mmm/DD/YYYY HH:MM: SS_ \- date and time, either date or time can be omitted in the **set** command; default value: _jan/01/1970 00:00:00_): Local time when DST starts and ends.