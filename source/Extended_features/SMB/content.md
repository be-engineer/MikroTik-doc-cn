# 概述

**Sub-menu:** `/ip smb`
**Packages required:** `system`

SMB 1.0服务器提供对路由器配置的文件夹文件共享访问。

RouterOS只支持SMB v1.0 和 v2.002

## 服务器设置

| 属性                                                                       | 说明                              |
| -------------------------------------------------------------------------- | --------------------------------- |
| **allow-guests** (_yes                           \| no_; Default: **yes**) | 是否允许SMB访客用户访问创建的共享 |
| **comment** (_string_; Default: **MikrotikSMB**)                           | 为服务器设置注释                  |
| **domain** (_string_; Default: **MSHOME**)                                 | 窗口工作组的名称。                |
| **enabled** (_yes                                \| no_; Default: **no**)  | 启用禁用SMB服务                   |
| **interface** (_string_; Default: **all**)                                 | SMB服务在哪些接口上运行。         |

## 共享设置

**Sub-menu:** `/ip smb share`

子菜单允许配置由SMB访问的共享名称和目录。

如果配置中提供的目录不存在，它将自动创建。

| 属性                                                                        | 说明                                                                    |
| --------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| **comment** (_string_; Default: **default share**)                          | 为共享设置一个注释。                                                    |
| **disabled** (_yes                                 \| no_; Default: **no**) | 如果禁用，共享将无法访问。                                              |
| **max-sessions** (_number_; Default: **10**)                                | 允许多少个SMB同时连接到一个共享文件夹。                                 |
| **name** (_string_; Default: )                                              | SMB共享名称。                                                           |
| **directory** (_string_; Default: )                                         | 路由器上分配给SMB共享的目录。如果 _name_ 参数的值为空，将使用根文件夹。 |

## 用户设置

**Sub-menu:** `/ip smb user`

设置可以访问路由器的SMB共享的用户。

| 属性                                        | 说明                                             |
| ------------------------------------------- | ------------------------------------------------ |
| **comment** (_string_; Default: )           | 为用户设置说明。                                 |
| **disabled** (_yes \| no_; Default: **no**) | 定义用户是启用还是禁用的                         |
| **name** (_string_; Default: )              | SMB服务用户的登录名                              |
| **password** (_string_; Default: )          | SMB用户连接到SMB服务的密码。                     |
| **只读** (_yes \| no_; Default: **yes**)    | 设置用户在访问共享时是有只读权限或完全访问权限。 |

## 示例

要通过SMB服务使RouterOS文件夹可用，请按以下步骤。

- 创建用户。

`/ip smb user add read-only=no name=mtuser password=mtpasswd`.

- 添加共享文件夹。

`/ip smb share add name=backup`。

- 启用SMB服务。

`/ip smb set enabled=yes`。

现在检查结果。

- 检查常规服务设置：

```shell
[admin@MikroTik] /ip smb> print
      enabled: yes
       domain: MSHOME
      comment: MikrotikSMB
 allow-guests: yes
   interfaces: all
```

- SMB用户设置:

```shell
[admin@MikroTik] /ip smb> users print
Flags: * - default, X - disabled
#    NAME         PASSWORD      READ-ONLY
0 *  guest                      yes
1    mtuser       mtpasswd      no
```

- 最终的SMB共享设置:

```shell
[admin@MikroTik] /ip smb> share print
Flags: X - disabled, I - inactive, * - default
#    NAME                   DIRECTORY        MAX-SESSIONS
0  * ;;; default share
     pub                   /pub              10
1    backup                /backup           10
```

可以进行额外的配置修改，如禁用默认用户和共享等。

## 不支持的功能

- SMB1扩展安全
