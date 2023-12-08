# 文件

文件菜单显示路由器上的所有用户空间文件。可以查看和编辑文件内容或删除文件。从RouterOS 7.9beta2开始可以创建文件。RouterOS上传“.Npk”包后，文件菜单也会显示包的特定信息，例如，架构，构建日期和时间等。

```shell
[admin@MikroTik] > file print detail
 0 name="routeros-mipsbe-6.45.7.npk" type="package" size=11.5MiB creation-time=oct/29/2019 11:36:15
   package-name="routeros-mipsbe" package-version="6.45.7" package-build-time=oct/24/2019 08:44:35
   package-architecture="mips"
 
 1 name="flash" type="directory" creation-time=jan/01/1970 02:00:03
 
 2 name="flash/skins" type="directory" creation-time=jan/01/1970 02:00:04
 
 3 name="flash/rw" type="directory" creation-time=sep/06/2019 14:01:16
 
 4 name="flash/rw/pckg" type="directory" creation-time=sep/06/2019 14:01:16
```

创建新文件(RouterOS 7.9beta2中增加的命令):

`[admin@MikroTik] > file add name=lala`

如果设备的文件列表中有一个名为“flash”的目录，您希望在系统重启/电源周期后保留的文件必须存储在该目录中。因为它之外的任何东西都保存在RAM磁盘中，并且在重新启动时将丢失。这并不包括.npk升级文件，因为它们将在系统丢弃RAM驱动器内容之前由升级过程应用。

对于带有NAND闪存的多核设备(例如CCR系列路由器，rb4011g)， RouterOS使用回写，将文件更改缓存到RAM存储器中，而不是直接将其写入闪存介质中。文件更改将在绝对必要时存储在闪存上，写入可以延迟40秒。这有助于减少CPU占用，从而获得更好的性能。但是，当设备突然断电时，可能会导致空文件或零长度文件，因为文件没有完全保存在闪存上。

## 属性

| 属性                                  | 说明                                             |
| ------------------------------------- | ------------------------------------------------ |
| **contents** (_string_; Default: )    | 文件的实际内容                                   |
| **create-time** (_time_)            | 文件创建的时间                                   |
| **name** (_string_)                   | 文件名称                                         |
| **package-Architecture** (_string_) | 构建包的架构。只适用于RouterOS“.Npk”文件         |
| **package- build -time** (_string_)   | 包被构建的时间。只适用于RouterOS".Npk”文件       |
| **package-Name** (_string_)         | 配置文件的可安装包名。只适用于RouterOS".Npk”文件 |
| **package-version** (_string_)        | 可安装包的版本。只适用于RouterOS".Npk”文件       |
| **size** (_integer_)                  | 文件大小                                         |
| **file type** (_string_)              | 文件类型。对于文件夹，文件类型为 _directory_     |

# 备份

RouterOS备份功能允许您保存当前设备的配置，然后可以在相同或不同的相同型号上重新应用这些配置。这非常有用，因为它允许您毫不费力地恢复设备的配置或在备份设备上重新应用相同的配置。系统备份文件中还包含设备的MAC地址，在加载备份文件时也会恢复设备的MAC地址。

如果路由器上安装了The Dude和user-manager，那么系统备份将不包含这些服务的配置。因此，在保存这些服务中的配置时应格外小心，例如配置导出。

系统备份包含有关您的设备及其配置的敏感信息，请始终考虑加密备份文件并将备份文件保存在安全的地方。

要保存备份，请配置以下信息:

```shell
[admin@MikroTik] >  system backup save name=/flash/backup1 password=StrongPass encryption=aes-sha256
Saving system configuration
Configuration backup saved
```

请注意，在带有闪存的设备上，在实际备份名称之前使用“/flash/”。如上所述，保存在flash文件夹外的备份将在重新启动或重新上电后删除:

```shell
[admin@MikroTik] > system backup save name=backup2 password=StrongPass encryption=aes-sha256        
Saving system configuration
Configuration backup saved
[admin@MikroTik] > file print detail
 0 name="flash" type="directory" creation-time=jan/01/1970 02:00:03
 
 1 name="flash/skins" type="directory" creation-time=jan/01/1970 02:00:04
 
 2 name="flash/rw" type="directory" creation-time=sep/06/2019 14:01:16
 
 3 name="flash/rw/pckg" type="directory" creation-time=sep/06/2019 14:01:16
 
 4 name="backup2.backup" type="backup" size=22.4KiB creation-time=oct/29/2019 11:40:33
 
 5 name="flash/backup1.backup" type="backup" size=22.4KiB creation-time=oct/29/2019 11:40:11
```

要加载备份，只需配置以下内容:

```shell
[admin@MikroTik] > system backup load name=/flash/backup1 password=StrongPass
Restore and reboot? [y/N]:
Y
```