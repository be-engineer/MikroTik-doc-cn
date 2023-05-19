# 概述

允许定义一组接口，以便在不同的基于接口的配置部分(如邻居发现、防火墙、网桥和Internet检测)中更容易地管理接口。

# 列表

**Sub-menu:** `/interface list `

此菜单包含有关路由器上所有可用接口列表的信息。预定义列表有三个: _all_(包含所有接口)、_none_(不包含接口)、_dynamic_ (包含动态接口)和 _static_ (包含静态接口)。也可以创建额外的接口列表。

| 属性                   | 说明                                                           |
| ---------------------- | -------------------------------------------------------------- |
| **name** (_string_)    | 接口列表名称                                                   |
| **include** (_string_) | 定义包含在列表中的成员的接口列表。可以添加多个以逗号分隔的列表 |
| **exclude** (_string_) | 定义从列表中排除成员的接口列表。可以添加多个以逗号分隔的列表   |

  
Members are added to the interface list in the following order:

1.  include members are added to the interface list
2.  exclude members are removed from the list
3.  Statically configured members are added to the list

# 成员

**Sub-menu:** `/interface list member`

该子菜单包含每个接口列表中静态配置的接口成员的信息。注意，通过include和exclude语句动态添加的接口不会在此子菜单中表示。

| 属性                     | 说明         |
| ------------------------ | ------------ |
| **interface** (_string_) | 接口名称     |
| **list** (_string_)      | 接口列表名称 |