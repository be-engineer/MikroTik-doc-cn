# 概述

以下步骤是关于如何用配置好的 [强大防火墙规则](https://help.mikrotik.com/docs/display/ROS/Building+Your+First+Firewall) 来额外保护设备的建议。

## RouterOS版本

首先要升级RouterOS版本。一些旧版本有某些弱点或漏洞已经被修复。保持设备最新以确保安全。在Winbox或Webfig中点击 "检查更新"进行升级。建议关注 [安全公告博客](https://blog.mikrotik.com/) 上的公告了解新的安全问题。

## 访问路由器

### 访问用户名

把默认的用户名 _admin_ 改成一个不同的名字。如果有人直接访问你的路由器，一个自定义的名字有助于保护对你路由器的访问。

`/user add name =myname password =mypassword group =full`
`/user disable admin`

### 访问密码

MikroTik路由器需要配置密码，建议使用密码生成工具来创建安全且不重复的密码。安全的密码意思是：

- 至少12个字符。
- 包括数字、符号、大写和小写字母。
- 不是字典中的字或字典中字的组合。

`/user set myname password = "!={Ba3N!" 40TуX+GvKBz?jTLIUcx /,"`

### RouterOS MAC访问

RouterOS有内置的选项，可以方便地对网络设备进行管理访问。在生产网络中应关闭特定的服务。**MAC-Telnet, MAC-Winbox,** 和 **MAC-Ping:**

`/tool mac-server set allowed-interface-list =none`

`/tool mac-server mac-winbox set allowed-interface-list =none`

`/tool mac-server ping set enabled =no`

### 邻居发现

MikroTik邻居发现协议用于显示和识别网络中的其他MikroTik路由器，禁用所有接口上的邻居发现。

`/ip neighbor discovery-settings set discover-interface-list =none`

### 带宽服务器

带宽服务器用于测试两个MikroTik路由器之间的吞吐量。在生产环境中禁用它。

`/tool bandwidth-server set enabled =no`

### DNS 缓存

路由器可能启用了 DNS 缓存，它减少了客户端对远程服务器的 DNS 请求的解析时间。如果路由器不需要 DNS 缓存，或者其他路由器用于这种目的，请禁用它。

`/ip dns set allow-remote-requests =no`

### 其他客户端服务

RouterOS可能启用了其他服务（默认的RouterOS配置中被禁用）。MikroTik缓存代理、socks、UPnP和云服务。

`/ip proxy set enabled =no`

`/ip socks set enabled =no`

`/ip upnp set enabled =no`

`/ip cloud set ddns-enabled =no update-time =no`

更安全的SSH访问

可以用这个命令启用更严格的SSH设置（添加aes-128-ctr，不允许hmac sha1和带sha1的组）。

`/ip ssh set strong-crypto =yes`

## 路由器接口

### 以太网/SFP接口

禁用路由器上所有未使用的接口是一个很好的做法，减少对路由器的非法访问。

`/interface print`

`/interface set X disabled =yes`

其中**X**是未使用的接口数量。

### LCD

有些RouterBOARD有一个LCD模块，用于提供信息，设置一个pin码或禁用:

`/lcd/pin/ set pin-number =3659 hide-pin-number =yes`
