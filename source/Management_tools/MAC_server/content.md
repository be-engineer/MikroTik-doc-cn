MAC服务器部分允许在RouterOS设备上配置MAC Telnet服务器、MAC WinBox服务器和MAC Ping服务器。

MAC Telnet是用来提供对没有设置IP地址的路由器的访问。它的工作方式与IP telnet一样。MAC telnet只可以在两个MikroTik RouterOS路由器之间使用。

MAC Winbox用于通过MAC地址提供Winbox对路由器的访问。

MAC Ping用于允许MAC ping到路由器的MAC地址。

**MAC-服务器** 设置包含在 "system"包中。

## MAC Telnet 服务器

可以对作为 [接口列表](https://help.mikrotik.com/docs/display/ROS/List) 一部分的特定接口设置MAC Telnet访问：

```shell
[admin@device] /tool mac-server set allowed-interface-list=listBridge
[admin@device] /tool mac-server print
  allowed-interface-list: listBridge
```

在上面的例子中，MAC Telnet是为接口列表 "listBridge "配置的，因此，MAC Telnet只能通过列表中的接口工作（可以在列表中添加多个接口）。

要禁止MAC Telnet访问，用命令（设置 "allowed-interface-list "为 "none"）：

```shell
[admin@device] /tool mac-server set allowed-interface-list=none
[admin@device] /tool mac-server print
  allowed-interface-list: none
```

可以用命令检查活动的MAC Telnet会话：

```shell
[admin@device] > tool mac-server sessions print
列： 接口、src-address、uptime
# interface src-address uptime
0 ether5 64:D1:54:FB:E3:E6 17s
```

### MAC Telnet客户端

当MAC Telnet服务器启用时，可以用另一台RouterOS设备，用mac-telnet客户端连接到服务器：

```shell
[admin@device2] > tool mac-telnet B8:69:F4:7F:F2:E7   
Login: admin
Password:
Trying B8:69:F4:7F:F2:E7...
Connected to B8:69:F4:7F:F2:E7
 
 
 
 
  MMM      MMM       KKK                          TTTTTTTTTTT      KKK
  MMMM    MMMM       KKK                          TTTTTTTTTTT      KKK
  MMM MMMM MMM  III  KKK  KKK  RRRRRR     OOOOOO      TTT     III  KKK  KKK
  MMM  MM  MMM  III  KKKKK     RRR  RRR  OOO  OOO     TTT     III  KKKKK
  MMM      MMM  III  KKK KKK   RRRRRR    OOO  OOO     TTT     III  KKK KKK
  MMM      MMM  III  KKK  KKK  RRR  RRR   OOOOOO      TTT     III  KKK  KKK
 
  MikroTik RouterOS 7.1rc3 (c) 1999-2021       https://www.mikrotik.com/
 
Press F1 for help
   
[admin@device] >
```

进入服务器的CLI相应地改变MAC地址（根据设置），如上面的例子所示。 

### MAC扫描

MAC扫描功能可以发现所有的设备，这些设备支持给定网络上的MAC telnet协议。该命令要求选择一个被扫描的接口：

```shell
[admin@Sw_Denissm] > tool mac-scan interface=all          
MAC-ADDRESS       ADDRESS                AGE
B8:69:F4:7F:F2:E7 192.168.69.1            26
2C:C8:1B:FD:F2:C3 192.168.69.3            56
```

在上面的例子中，所有的接口都被选中，除非停止（按 "q "键），否则扫描将无限期进行。

还可以添加一个 "持续时间 "参数，规定扫描持续多长时间：

```shell
[admin@Sw_Denissm] > tool mac-scan interface=all duration=1
MAC-ADDRESS       ADDRESS                AGE
B8:69:F4:7F:F2:E7 192.168.69.1            48
2C:C8:1B:FD:F2:C3 192.168.69.3            17
```

在上面的例子中， "持续时间 "参数设置为1秒。

## MAC Winbox服务器

与MAC Telnet一样，可以将MAC Winbox设置为访问 [接口列表](https://help.mikrotik.com/docs/display/ROS/List) 中的特定接口：

```shell
[admin@device] > tool mac-server mac-winbox set allowed-interface-list=listBridge
[admin@device] > tool mac-server mac-winbox print                  
  allowed-interface-list: listBridge
```

在上面的例子中，MAC Winbox的访问是为接口列表 "listBridge "配置的，因此，MAC Winbox只能通过属于该列表的接口工作。

要禁止MAC Winbox访问，用命令（设置 "allowed-interface-list "为 "none"）：

```shell
[admin@device] > tool mac-server mac-winbox set allowed-interface-list=none
[admin@device] > tool mac-server mac-winbox print                  
  allowed-interface-list: none
```

## MAC Ping服务器

MAC Ping服务器可以设置为 "禁用 "或 "启用"：

```shell
[admin@device] > tool mac-server ping print
  enabled: yes
```

可以在命令的帮助下启用或禁用MAC ping（**enable=yes** →启用该功能；**enable=no** →禁用该功能）：

```shell
[admin@device] > tool mac-server ping set enabled=yes
[admin@device] > tool mac-server ping set enabled=no
```

当MAC Ping启用时，同一广播域的其他主机可以使用ping工具来ping mac地址。例如，可以用以下命令来检查MAC ping的结果：

```shell
[admin@device] > /ping 00:0C:42:72:A1:B0
HOST                                    SIZE  TTL TIME  STATUS                                        
00:0C:42:72:A1:B0                       56        0ms 
00:0C:42:72:A1:B0                       56        0ms 
    sent=2 received=2 packet-loss=0% min-rtt=0ms avg-rtt=0ms max-rtt=0ms
```