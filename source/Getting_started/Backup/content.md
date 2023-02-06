# 概述

RouterOS 备份功能可以保存当前设备的配置，然后可以在相同或不同的设备（具有相同的型号名称/编号）上重新应用。这非常有用，因为它允许毫不费力地恢复设备的配置或在备份设备上重新应用相同的配置。系统的备份文件还包含设备的 MAC 地址，这些地址也会在加载备份文件时恢复。

> 如果路由器上安装了 The Dude 和 user-manager，则系统备份不包含这些服务的配置，因此应注意单独保存这些服务的配置。如果要保存配置，请使用提供的工具保存/导出配置。

> 系统备份包含设备及其配置的敏感信息，请考虑加密备份文件并将备份文件保存在安全的地方。

## 保存备份

**子菜单:** `/system backup save`

| 属性                                                                                 | 说明                                                                                                       |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| dont-encrypt (yes                                       \| no; Default: no)          | 禁用备份文件加密。注意，由于RouterOS v6.43没有提供密码 ，备份文件不会加密。                                |
| encryption (aes-sha256                                  \| rc4; Default: aes-sha256) | 用于加密备份文件的加密算法。注意，这不认为是一种安全的加密方法，仅出于与旧 RouterOS 版本兼容的原因才可用。 |
| name (string; Default: [identity]-[date]-[time].backup)                              | 备份文件名。                                                                                               |
| password (string; Default: )                                                         | 备份文件的密码。注意，由于RouterOS v6.43没有提供密码 ，备份文件不会加密。                                  |

> 如果在早于 v6.43 的 RouterOS 版本中未提供密码，则备份文件将使用当前用户的密码加密，除非使用了 dont-encrypted 属性或当前用户的密码为空。

备份文件将保存在 `/file` 菜单下，可以使用 FTP 或 Winbox 下载。

## 载入备份

载入没有密码的备份:

`[admin@MikroTik] > system` `/backup/load name=auto-before-reset.backup password=""`

| 属性                               | 说明               |
| ---------------------------------- | ------------------ |
| **name** (_string_; Default: )     | 备份文件名         |
| **password** (_string_; Default: ) | 加密备份文件的密码 |

### 示例

将路由器的配置保存到文件test并加上密码：

`[admin@MikroTik] >` `/system backup save name=test password=<YOUR_PASSWORD>`

`Configuration backup saved`

`[admin@MikroTik] >` `/system backup`

查看保存在路由器上的文件:

`[admin@MikroTik] >` `/` `file` `print`

`0 test.backup backup 12567 sep` `/08/2018 21:07:50`

`[admin@MikroTik] >`

加载保存的备份文件test:

`[admin@MikroTik] >` `/system backup load name=test`

`password` `: <YOUR_PASSWORD>`

`Restore` `and` `reboot? [y` `/N]: y`

`Restoring system configuration`

`System configuration restored, rebooting now`

## 云备份

从 RouterOS v6.44 开始，可以将设备的备份文件安全地存储在 MikroTik 的云服务器上，请在 [IP/Cloud](https://help.mikrotik.com/docs/display/ROS/Cloud) 页面上阅读更多信息。
