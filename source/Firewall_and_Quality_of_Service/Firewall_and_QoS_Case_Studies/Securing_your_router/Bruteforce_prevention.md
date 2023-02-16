# 预防暴力攻击

下面是一个防御ssh端口暴力攻击的例子。请注意，ssh允许每个连接有3次登录尝试，而且登录成功后地址列表不会被清除，所以可能不小心把自己列入黑名单。

```shell
/ip firewall filter
add action =add-src-to-address-list address-list =bruteforce_blacklist address-list-timeout =1d chain =input comment =Blacklist connection-state =new dst-port =22 protocol =tcp src-address-list =connection3
add action =add-src-to-address-list address-list =connection3 address-list-timeout =1h chain =input comment = "Third attempt" connection-state =new dst-port =22 protocol =tcp src-address-list =connection2,!secured
add action =add-src-to-address-list address-list =connection2 address-list-timeout =15m chain =input comment = "Second attempt" connection-state =new dst-port =22 protocol =tcp src-address-list =connection1
add action =add-src-to-address-list address-list =connection1 address-list-timeout =5m chain =input comment = "First attempt" connection-state =new dst-port =22 protocol =tcp
add action =accept chain =input dst-port =22 protocol =tcp src-address-list =!bruteforce_blacklist
```

如果所有三个列表的超时都保持在1分钟-connection1/2/3-那么某人每分钟可以进行9次猜测，这样每5分钟最多可以进行3次猜测。
