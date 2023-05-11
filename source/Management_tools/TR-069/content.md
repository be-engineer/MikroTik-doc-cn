TR069-client实现了用于远程设备管理的CPE WAN管理协议（CWMP），该协议是由宽带论坛（BBF）标准化的。CWMP通过IP网络工作，使用HTTP(S)与自动配置服务器(ACS)通信，它可以监测、配置属性并更新远程设备的固件。通常由ISP用于管理CPE，但也可用于网络基础设施设备管理。

## 配置设置

TR069-client菜单参数。当软件包被安装时（首次在RouterOS 6.38中提供）。配置在 _/tr069-client_ 中。

### 可写设置

客户端配置设置。

| 属性                          | 说明                                                                                                                                                                   |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **enabled**                       | 启用/禁用CWMP协议                                                                                                                                                             |
| **acs-url**                       | ACS的URL例子: [https://example.com:8080/path/](https://example.com:8080/path/), [https://192.168.1.100/](https://192.168.1.100/)                                              |
| **username**                      | HTTP认证用户名(CPE用来 "登录 "ACS)                                                                                                                                            |
| **password**                      | HTTP认证密码（CPE用来 "登录 "ACS）。                                                                                                                                          |
| **periodic-inform-enabled**       | 启用/禁用CPE周期性会话启动。计时器在每次成功的会话后启动。当会话以周期性间隔启动时，信息RPC包含 "2 PERIODIC "事件。映射到 "Device.ManagementServer.PeriodicInformEnable "参数 |
| **periodic-information-interval** | 周期性信息的定时器间隔时间。映射到 "Device.ManagementServer.PeriodicInformInterval "参数。                                                                                    |
| **client-certificate**            | 客户端/CPE的证书，ACS可以使用它来进行额外的认证。                                                                                                                             |

### 只读设置

只读参数用于监控客户的状态。

| 属性                   | 说明                                                                                                                                            |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **status**             | CWMP的信息状态。<br>- disabled - 协议禁用<br>- waiting-URL - 协议已启用，但ACS URL未配置<br>- running - CWMP配置正确，将在事件发生时与ACS通信。 |
| **last-session-error** | 用户友好的错误描述，表明为什么前一个会话没有成功完成。                                                                                          |
| **retry-count**        | 连续不成功的会话数。如果>0，那么last-session-error应该表示错误。在一个成功的会话、禁用的协议或重启时重设为0。                                   |

### 命令

| 命令                   | 说明                                                                                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **reset-tr069-config** | 完全重置并忘记tr069-client的配置和状态（不影响其他ROS的配置）。当CWMP进入无响应/挂起状态，并且应该在不重新安装RouterOS的情况下恢复时使用。 |

## CWMP会话

CWMP客户端通常在不同的事件中开始与ACS通信（会话）-首次启动、重启、周期性间隔、远程请求、数值变化等。在每个会话中，CPE和ACS可以调用RPC，在另一方 "执行"。CPE总是以Inform RPC开始，其中包含连接原因、设备信息和一些参数值，这取决于配置。当CPE没有什么可说的了，ACS就会执行它的RPC（大多数情况下是参数管理RPC）。

## 参数和数据模型

参数是简单的名称+值对，每个供应商可以决定在其设备中支持哪些参数。所有支持的参数的组合被称为数据模型（DM）。BBF定义了三个根数据模型(TR-098, TR-181:1, TR-181:2)，供应商应在此基础上支持其参数。**RouterOS数据模型是基于 "TR-181 Issue 2 Amendment 11"**，这是最新的DM，由BBF推荐。

[RouterOS TR069客户端支持的参数参考](https://wiki.mikrotik.com/tr069ref/current.html)

## 下载RPC

### RouterOS更新(1个固件升级镜像)

CWMP标准规定，CPE的固件可以使用Download RPC进行更新，FileType="1 Firmware Upgrade Image "和可下载文件的URL（支持HTTP和HTTPS）。标准还指出，下载的文件可以是任何类型，并且可以应用供应商的特定流程来完成固件更新。因为MikroTik的更新是基于软件包的（也是为了获得额外的灵活性），所以使用XML文件来描述固件升级或降级。目前，XML配置支持提供多个文件的URL，这些文件将被下载并应用，就像常规的RouterOS更新通过固件包文件上传一样。

一个RouterOS捆绑包和tr069-client包更新的例子（别忘了也要更新tr069-client包）。一个XML文件应该放在某个HTTP服务器上，可以从CPE上访问，以供下载。另外，可下载的RouterOS包文件也应以同样的方式访问（可以在任何HTTP服务器上）。使用ACS执行下载RPC，URL指向XML文件（例如：[https://example.com/path/upgrade.xml](https://example.com/path/upgrade.xml)），内容是：

```
<upgrade version="1" type="links">
   <config/>
   <links>
       <link>
          <url>https://example.com/routeros-mipsbe-X.Y.Z.npk</url>
       </link>
       <link>
          <url>https://example.com/tr069-client-X.Y.Z-mipsbe.npk</url>
       </link>
   </links>
</upgrade>

```

CPE将下载XML，解析验证其内容，从提供的URL下载文件并尝试升级。结果将通过TransferComplete RPC报告。

注意

始终使固件更新增量 - 首先，更新本地测试的设备，并确保CWMP通信以新的版本恢复，并且所需的ROS功能可以工作。其次，重复步骤，渐进地更新CPE组。不建议一次性更新所有远程设备。

**警告：** 在生产中使用HTTPS进行固件管理。

### 配置更改 (3个供应商配置文件)

同样的下载RPC可以用来执行完整的配置覆盖（按照标准的意图）或配置更改（当URL的文件名扩展名为".alter "时）。

### 改动配置

RouterOS有很多配置属性，不是所有的东西都可以移植到CWMP参数中，这就是为什么RouterOS提供了执行其强大的脚本语言来配置任何属性的可能性。可以使用下载RPC FileType="3 Vendor Configuration File "和可下载的文件扩展名".alter "来执行配置更改（这实际上是一个常规的脚本执行）。这个强大的功能可用于配置任何ROS属性，这些属性不能通过CWMP参数获得。

### 覆盖所有配置

完整的ROS配置可以通过使用下载RPC FileType="3 Vendor Configuration File "和任何URL文件名（扩展名为".alter "的除外）进行覆盖。

**警告：** 提供的配置文件（脚本）必须足够 "聪明"，以便在重启后正确应用配置。当使用上传的配置文件与Upload RPC时，这一点尤其重要，因为它只包含导出的值。有些东西应该手动添加：

- 开始时的延迟，以便接口显示出来；
- 用户的隐藏密码；
- 证书。

### RouterOS默认配置更改 (X MIKROTIK出厂配置文件)

这个供应商特定的文件类型允许改变RouterOS默认配置脚本，该脚本在 **/system reset-configuration** 命令被执行时（或路由器配置被重置时的其他方式）被执行。

注意

如果默认配置脚本被改变，它将不会被 **/system default-configuration print** 显示出来，因为如果该脚本被Netinstall工具改变，就会出现这种情况。该命令将始终显示MikroTik设置的默认脚本。

**警告：** 谨慎使用，因为上传脚本的失败可能会导致设备无法操作或无法被ACS访问。

## FactoryReset RPC

这是CWMP标准RPC，执行RouterOS配置的工厂复位。重置过程的执行方式与执行命令的方式相同：

```
/system reset-configuration skip-backup=yes

```

请注意，每个设备的默认出厂配置可能不同（见 [1](https://wiki.mikrotik.com/wiki/Manual:Default_Configurations) ），执行此命令会删除所有配置并执行内部存储的默认配置脚本。

为TR069准备具有自定义出厂设置的CPE的最佳实践指南 [https://wiki.mikrotik.com/wiki/Tr069-best-practices](https://wiki.mikrotik.com/wiki/Tr069-best-practices)

## 上传RPC

### 上传当前配置(1个供应商配置文件)

其结果是上传到ACS的文件与RouterOS中 **/export** 命令的输出相同。

### 上传日志文件 (2 Vendor Log File)

这是上传到ACS的文件，其结果与RouterOS中 **/log print** 命令的输出相似。

### 上传默认配置 (X MIKROTIK Factory Configuration File)

这个结果是上传到ACS的文件，其中有当前设置的默认配置脚本的内容，如果 **/system reset-configuration** 命令被执行，将被执行。它可能与使用 **/system default-configuration print** 返回的文件不同。

## 安全

- HTTP只能在安全/私人网络中测试初始设置时使用，因为中间人攻击者可以读取/改变配置参数。**在生产环境中，HTTPS是必须的**。
- CWMP的传入连接验证在设计上是安全的，因为除了先前配置的ACS，CPE不会与任何其他设备通信。连接请求只提示CPE与先前配置的ACS开始一个新的连接+新的会话。

## 经测试的ACS

顺序是按字母顺序排列的。MikroTik并不意味着任何一个供应商比另一个供应商优越。如果缺少某些ACS，可以通知我们它的存在，可能会被添加到列表中。

### 商业

我们已经测试并验证了以下商业ACS解决方案的有效性：

- [AVSystem](https://www.avsystem.com)
- [Axiros](https://axiros.com)
- [Friendly Tech](https://friendly-tech.com)

### 开放源代码

- [GenieACS](https://github.com/zaidka/genieacs)

注意：下面这些ACS系统没有维护，不建议作为有用的选择。

- [FreeACS](https://www.freeacs.com)
- [LibreACS](https://github.com/navisidhu/libreacs)
