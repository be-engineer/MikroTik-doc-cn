TR069-client实现了用于远程设备管理的CPE WAN管理协议（CWMP），该协议是由宽带论坛（BBF）标准化的。CWMP通过IP网络工作，使用HTTP(S)与自动配置服务器(ACS)通信，它可以监测、配置属性并更新远程设备的固件。通常由ISP用于管理CPE，但也可用于网络基础设施设备管理。

## 配置设置

TR069-client菜单参数。当软件包被安装时（首次在RouterOS 6.38中提供）。配置在 _/tr069-client_ 中。

### 可写设置

客户端配置设置。

| Property                          | Description                                                                                                                                                                   |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **enabled**                       | 启用/禁用CWMP协议                                                                                                                                                             |
| **acs-url**                       | ACS的URL例子: "[https://example.com:8080/path/](https://example.com:8080/path/)", "[https://192.168.1.100/](https://192.168.1.100/)"                                          |
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

[RouterOS TR069 client supported parameter reference document](https://wiki.mikrotik.com/tr069ref/current.html)

## 下载RPC

### RouterOS更新(1个固件升级图像)

CWMP标准规定，CPE的固件可以使用Download RPC进行更新，FileType="1 Firmware Upgrade Image "和可下载文件的单一URL（支持HTTP和HTTPS）。标准还指出，下载的文件可以是任何类型，并且可以应用供应商的特定流程来完成固件更新。因为MikroTik的更新是基于软件包的（也是为了获得额外的灵活性），所以使用XML文件来描述固件升级/降级。目前，XML配置支持提供多个文件的URL，这些文件将被下载并应用，就像常规的RouterOS更新通过固件/包文件上传一样。

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

CPE将下载XML，解析/验证其内容，从提供的URL下载文件并尝试升级。结果将通过TransferComplete RPC报告。

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

### RouterOS default configuration change (X MIKROTIK Factory Configuration File)

This vendor specific FileType allows the change of the RouterOS default configuration script that is executed when **/system reset-configuration** command is executed (or the other means when router configuration is beeing reset).

Note

If the default configuration script is changed it will not be displayed by **/system default-configuration print** as it is the case if that script is altered via Netinstall tool. That command will always show the default script set up by MikroTik

**Warning:** Use this with caution as the failure of uploaded script may render device inoperable and/or inaccessible by the ACS

## FactoryReset RPC

This is CWMP standard RPC, which performs RouterOS configuration factory-reset. The reset process is performed in the same way as executing the command:

```
/system reset-configuration skip-backup=yes

```

Note that the default factory configuration can be different for each device (see [[1]](https://wiki.mikrotik.com/wiki/Manual:Default_Configurations)) and execution of this command removes all configurations and executes internally stored default-configuration script.

[Best Practices Guide for preparing CPE with custom factory settings for TR069 [https://wiki.mikrotik.com/wiki/Tr069-best-practices](https://wiki.mikrotik.com/wiki/Tr069-best-practices)]

## Upload RPC

### Upload current configuration (1 Vendor Configuration File)

The result of this is file uploaded to the ACS same as the output of **/export** command in the RouterOS

### Upload log file (2 Vendor Log File)

The result of this is file uploaded to the ACS is similar to the output of **/log print** command in the RouterOS

### Upload default configuration (X MIKROTIK Factory Configuration File)

The result of this is file uploaded to the ACS that has contents of the current set default configuration script that will be executed if **/system reset-configuration** command is executed. It may differ from one returned using **/system default-configuration print**.

## Security

-   HTTP should only be used when testing initial setup in the secured/private network because Man-in-the-middle attacker could read/change configuration parameters. **In the production environment, HTTPS is a MUST**.
-   CWMP's incoming connection validation by design is safe because CPE will not communicate with any other device except previously configured ACS. Connection Request only signals CPE to start a new connection + new session with previously configured ACS.

## Tested ACSs

Ordering is alphabetical. MikroTik does not imply any one vendor superiority of another. If some ACS is missing you can notify us of the existence of it and it might be added to the list.

### Commercial

We have tested and verified to be working the following commercial ACS solutions:

-   [AVSystem](https://www.avsystem.com)
-   [Axiros](https://axiros.com)
-   [Friendly Tech](https://friendly-tech.com)

### Open Source

-   [GenieACS](https://github.com/zaidka/genieacs)

Note: these ACS systems below seem to be not maintained and thus is not suggested as useful options

-   [FreeACS](https://www.freeacs.com)
-   [LibreACS](https://github.com/navisidhu/libreacs)