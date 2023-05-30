# 概述

点对点协议（PPP）提供了一种在点对点链接上传输多协议数据包的标准方法。RouterOS中的PPP是基于 [RFC 1661标准](https://tools.ietf.org/html/rfc1661)

# 介绍

PPP的基本目的是在数据链路层的点对点链接上传输第三层数据包。 两个对等体之间的数据包被认为是按顺序传送的。 

PPP是由三个主要部分组成的：

1.   一种封装多协议数据报的方法。
2.   用于建立、配置和测试数据链路连接的链路控制协议（LCP）。 
3.  用于建立和配置不同网络层协议的网络控制协议（NCP）系列。

在RouterOS中详细的PPP数据包处理，可以在 [数据包流程图](https://help.mikrotik.com/docs/display/ROS/Packet+Flow+in+RouterOS) 中查看。

## PPP客户端

`/interface ppp-client`

## PPP客户端例子

这是一个如何使用LTE调制解调器的裸露串行端口添加客户端的例子。

`/interface ppp-client add apn=yourapn dial-on-demand=no disabled=no port=usb2`

按需拨号应该设置为 "no"获得连续的连接。

## PPP服务器

`/interface ppp-server`