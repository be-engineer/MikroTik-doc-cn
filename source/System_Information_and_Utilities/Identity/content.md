# 概述

设置系统标识为系统向网络中的其他路由器标识自己，以及访问DHCP、邻居发现和默认无线SSID等服务提供唯一的标识名称。默认的系统标识设置为“microtik”。

系统标识的最大字符长度为64

# 配置

在RouterOS中设置系统标识。

```shell
[admin@MikroTik] > /system identity set name=New_Identity
[admin@New_Identity] >
```  

当前系统标识总是显示在登录的帐户名之后，并使用print命令:

```shell
[admin@New_Identity] /system identity>print
name: New_Identity
[admin@New_Identity] /system identity>
```

## SNMP

也可以通过SNMP set命令修改路由器的系统标识:

`snmpset -c public -v 1 192.168.0.0 1.3.6.1.2.1.1.5.0 s New_Identity`

_snmpset_ - 基于Linux的SNMP应用程序，用于SNMP SET请求来设置网络实体上的信息;

- _public_ - 路由器的团体名;
- _192.168.0.0_ - 路由器的IP地址;
- _1.3.6.1.2.1.1.5.0_ - 路由器标识的SNMP值;