Cloud Hosted Router (CHR) 是一个 RouterOS 版本，支持虚拟机运行。 它支持 x86 64 位架构，可用于大多数流行的管理软件，如 VMWare、Hyper-V、VirtualBox、KVM 等。 CHR默认启用完整的 RouterOS 功能，但和其他 RouterOS 版本有不同的许可模型。

# 系统要求

- 软件包版本:RouterOS v6.34 或更新版本
- 主机 CPU:64 位，支持虚拟化
- 内存:128MB 或更多（最大:128GB）
- 磁盘:CHR 虚拟硬盘驱动器的 128MB 磁盘空间（最大:16GB）

最小 RAM 取决于接口数量和 CPU 数量。 可以使用以下公式得到一个大概的数字:

- RouterOS v6 - RAM = 128 + [ 8 * (CPU_COUNT) * (INTERFACE_COUNT - 1) ]
- RouterOS v7 - RAM = 256 + [ 8 * (CPU_COUNT) * (INTERFACE_COUNT - 1) ]

**注意:**建议为 CHR 实例分配至少 1024MiB 的 RAM。

## CHR 已经在以下平台上进行了测试:

- VirtualBox 6 on Linux and OS X
- VMWare Fusion 7 and 8 on OS X
- VMWare ESXi 6.5
- Qemu 2.4.0.1 on Linux and OS X
- Hyper-V on Windows Server 2008r2, 2012 and Windows 10 _(Only Generation 1 Hyper-V virtual machine is supported at the moment)_
- Xen Server 7.1

**警告:** 不支持提供准虚拟化的管理程序。

## 各种管理软件上可用的网络和磁盘接口:

- ESX:
  - Network: vmxnet3, E1000
  - Disk: IDE, VMware paravirtual SCSI, LSI Logic SAS, LSI Logic Parallel

- Hyper-V:
  - Network: Network adapter, Legacy Network adapter
  - Disk: IDE, SCSI

- Qemu/KVM:
  - Network: Virtio, E1000, vmxnet3 (optional)
  - Disk: IDE, Sata, Virtio

- VirtualBox
  - Network: E1000, rtl8193
  - Disk: IDE, Sata, SCSI, SAS

**注意:** SCSI 控制器 Hyper-V 和 ESX 仅可用于辅助磁盘，系统映像必须与 IDE 控制器一起使用！

**警告:** 如果特定管理软件上有更好的接口选项，则不建议使用 E1000 网络接口！

## 如何使用 CHR 映像安装虚拟 RouterOS 系统

我们提供 4 种不同的虚拟磁盘映像供选择。 注意，它们只是磁盘映像，不能简单地运行。

- RAW disk image (.img file)
- VMWare disk image (.vmdk file)
- Hyper-V disk image (.vhdx file)
- VirtualBox disk image (.vdi file)

### 安装CHR步骤

1. [下载](https://www.mikrotik.com/download#chr) 用于管理软件的虚拟磁盘映像
2.创建客户虚拟机
3.使用之前下载的镜像文件作为虚拟磁盘驱动器
4.启动guest CHR虚拟机
5.登录到CHR。 默认用户是“admin”，没有密码

注意，可以克隆和复制正在运行的 CHR 系统，但副本会知道之前的试用期，因此不能通过复制 CHR 来延长试用时间。 但是，可以单独许可这两个系统。 要制作新的试用系统，需要全新安装并重新配置 RouterOS。

### 安装 CHR 指南

- [VMWare](https://wiki.mikrotik.com/wiki/Manual:CHR_VMWare_installation "Manual:CHR VMWare installation") Fusion / Workstation and ESXi 6.5
- [VirtualBox](https://wiki.mikrotik.com/wiki/Manual:CHR_VirtualBox_installation "Manual:CHR VirtualBox installation")
- [Hyper-V](https://wiki.mikrotik.com/wiki/Manual:CHR_Hyper-V_installation "Manual:CHR Hyper-V installation")
- [Amazon Web Services (AWS)](https://wiki.mikrotik.com/wiki/Manual:CHR_AWS_installation "Manual:CHR AWS installation")
- [Hetzner Cloud](https://wiki.mikrotik.com/wiki/Manual:CHR_Hetzner "Manual:CHR Hetzner")
- [Linode](https://wiki.mikrotik.com/wiki/Manual:CHR_Linode "Manual:CHR Linode")
- [Google Compute Engine](https://wiki.mikrotik.com/wiki/Manual:CHR_GCE "Manual:CHR GCE")
- [ProxMox](https://help.mikrotik.com/docs/display/ROS/CHR+ProxMox+installation)

## CHR 许可证

CHR 有 4 个许可级别:

- **free**
- **p1** _perpetual-1_ ($45)
- **p10** _perpetual-10_ ($95)
- **p-unlimited** _perpetual-unlimited_ ($250)

60 天免费试用许可证适用于所有付费许可证级别。 要获得免费试用许可证，必须在 [MikroTik.com](https://mikrotik.com/) 上拥有一个帐户，因为所有许可证管理都在那里。

Perpetual 是终身许可证（一次购买，永久使用）。 可以将永久许可证转移到另一个 CHR 实例。 正在运行的 CHR 实例将指示它必须访问帐户服务器以更新其许可证的时间。 如果 CHR 实例无法续订许可证，会表现为试用期结束，不允许将 RouterOS 升级到更新的版本。

获得运行中的试用系统许可后，**必须** 从CHR手动运行 _/system license renew_ 功能激活。 否则，系统将不知道获取了许可。 如果没有在系统截止时间之前执行此操作，试用将结束，则必须全新安装 CHR，请求新的试用，然后使用获得的许可证进行授权。

| 许可证      | 速度限制  | 价格 |
| ----------- | --------- | ---- |
| Free        | 1Mbit     | FREE |
| P1          | 1Gbit     | $45  |
| P10         | 10Gbit    | $95  |
| P-Unlimited | Unlimited | $250 |

## 付费许可证

### p1

_p1_ (perpetual-1) 许可级别允许 CHR 无限期运行。 每个接口传速度限制为 1Gbps。 CHR 提供的所有其他功能都可以不受限制地使用。 可以将 _p1_ 升级到 _p10_ 或 _p-unlimited_ （可以按标准价格购买新的许可证级别）。购买升级后，以前的许可证可供你的帐户以后使用。

### p10

_p10_（perpetual-10）许可级别允许 CHR 无限期运行。 每个接口传速度限制为 10Gbps。 CHR 提供的所有其他功能都可以不受限制地使用。 可以将 _p10_ 升级到 _p-unlimited_ ，购买升级后，以前的许可证将可供你的帐户以后使用。

### p-unlimited

_p-unlimited_ （永久无限制）许可级别允许 CHR 无限期运行。 它是最高级别的许可证，没有强制限制。

## 免费许可证

有多种选择可以免费使用和试用 CHR。

### free

_free_ 许可级别允许 CHR 无限期运行。 每个接口的上传速度限制为1Mbps。 CHR 提供的所有其他功能都可以不受限制地使用。 要使用它，要做的就是从下载页面下载磁盘映像文件并创建一个虚拟客户机。

### 60 天试用

除了有限的免费安装，还可以通过 60 天试用来测试 P1/P10/PU 许可证的速度。

你必须在 [MikroTik.com](https://mikrotik.com/) 上注册一个帐户。 然后从路由器请求所需的试用许可级别，这会将路由器 ID 分配给你的帐户，并允许从你的帐户购买许可证。 所有付费许可证均可试用。 试用期是从获取之日起的 60 天，过了这段时间后，你的许可证菜单将显示“限制升级”，意味着 RouterOS 无法再升级。

如果你计划购买所选许可证，则必须在试用结束日期后 60 天内购买。 如果试用结束，并且在结束后 2 个月内没有购买，该设备将不再出现在你的 MikroTik 帐户中。 必须进行新的 CHR 安装才能在规定的时间范围内进行购买。

要申请试用许可证，必须从 CHR 设备命令行运行命令 "**/system license renew**"。 系统会要求你提供 [mikrotik.com](https://mikrotik.com/) 帐户的用户名和密码。

如果你计划使用多个相同类型的虚拟系统，那么下一台机器可能具有与原始机器相同的系统 ID。 这可能发生在某些云提供商处，例如 Linode。 为避免这种情况，**在你请求试用许可证之前**，在你第一次启动后，运行命令"/system license generate-new-id"。 注意，只有当 CHR 在免费类型的 RouterOS 许可证上运行时，才能使用此功能。 如果你已经获得付费或试用许可证，请不要使用生成功能，因为你无法再更新当前密钥.

## 获取许可证

初始设置后，CHR 实例将分配 _free_ 许可证。 从那里可以将许可证升级到更高级别。 获得试用许可证后，所有使用许可证的工作都在 [帐户服务器](https://mikrotik.com/client) 上完成，在那里可以将许可证升级到更高级别，除非已经是 _p-unlimited_ .

### 从免费许可升级到 p1 或更高版本

从 _free_ 级别升级到任何更高层会导致在 [帐户服务器](https://mikrotik.com/client) 上注册 CHR 实例。 为此，你必须输入你的 [MikroTik.com](https://www.mikrotik.com/client/) 用户名和密码以及你想要获得的许可级别。 因此，将在帐户服务器上为你的帐户分配一个 CHR ID 号，并为该 ID 创建一个 60 天的试用期。 有 2 种方法可以获得许可证 - 使用 WinBox 或 RouterOS 命令行界面:

**使用WinBox (Sytem -> License menu):**

![](https://help.mikrotik.com/docs/download/thumbnails/18350234/CHR_Licence_01.png?version=1&modificationDate=1596783161874&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/18350234/CHR_Licence_02.png?version=1&modificationDate=1596783162276&api=v2)

**使用命令行:**

```shell
[admin@MikroTik] > /system license print 
  system-id: 6lR1ZP/utuJ
      level: free

[admin@MikroTik] > /system license renew 
account: mymikrotikcomaccount
password: *********************
level: p1 
  status: done
  
[admin@MikroTik] > /system license print 
        system-id: 6lR1ZP/utuJ
            level: p1
  next-renewal-at: jan/10/2016 21:59:59
      deadline-at: feb/09/2016 21:59:59

```

要获得更高级别的试用版，请设置一个新的 CHR 实例，续订许可证，然后选择所需的级别。

要从试用许可证升级到付费许可证，请转到 [MikroTik.com 帐户服务器](https://www.mikrotik.com/client) 并在云托管路由器 (CHR) 选择“所有密钥”:

![](https://help.mikrotik.com/docs/download/attachments/18350234/CHR_keys_01.png?version=1&modificationDate=1596783162188&api=v2)

你将看到你的 CHR 机器和许可证列表:

![](https://help.mikrotik.com/docs/download/attachments/18350234/CHR_keys_02a.PNG?version=1&modificationDate=1596783162146&api=v2)

要从试用许可证升级到付费许可证，请单击“升级”，选择所需的许可证级别（不同于试用许可证的级别），然后单击“升级密钥”:

![](https://help.mikrotik.com/docs/download/attachments/18350234/1800px-CHR_keys_03.png?version=1&modificationDate=1596783162097&api=v2)

选择付费方式:

![](https://help.mikrotik.com/docs/download/attachments/18350234/CHR_keys_04.png?version=1&modificationDate=1596783162028&api=v2)

可以使用帐户余额（存款）、信用卡 (CC)、PayPal 或使用余额（预付）密钥（如果有）进行支付。

## 许可证更新

![](https://help.mikrotik.com/docs/download/attachments/18350234/CHR_Licence_02-2.png?version=1&modificationDate=1596783161974&api=v2)

在`/system license`菜单中，路由器将指示 _next-renewal-at_ 时间，它将尝试联系位于 [licence.mikrotik.com](https://licence.mikrotik.com/) 上的服务器。 通信尝试将在 _next-renewal-at_ 日期后每小时执行一次，在服务器响应错误之前不会停止。 如果到达 _deadline-at_ 日期但仍未成功联系帐户服务器，则路由器将认为许可证已过期并将不允许进一步的软件更新。 但是，路由器将继续使用与以前相同的许可等级。

## 虚拟网络适配器

自 RouterOS v7 起支持“vmxnet3”和“virtio-net”适配器的Fast Path。

RouterOS v6 不支持Fast Path。

## 故障排除

## 在 VMware ESXi 上运行

### 改变MTU

VMware ESXi 支持最大 9000 字节的 MTU。 要从中获益，必须调整 ESXi 安装允许更高的 MTU。 ESXi 服务器正确允许 ESXi 服务器在 MTU **更改后**添加虚拟以太网接口以传输巨型帧。 在 ESXi 服务器上的 MTU 更改之前添加的接口将被 ESXi 服务器禁止（它仍将旧 MTU 报告为最大可能大小）。 如果有这个，你必须重新添加接口到虚拟客户机。

**示例** 有 2 个接口添加到 ESXi 客户机，接口上自动检测到 MTU 显示添加接口时的 MTU 大小:

```shell
[admin@chr-vm] > interface ethernet print 
Flags: X - disabled, R - running, S - slave 
 #    NAME           MTU MAC-ADDRESS       ARP       
 0 R  ether1        9000 00:0C:29:35:37:5C enabled   
 1 R  ether2        1500 00:0C:29:35:37:66 enabled

```

### 在 Linux 上使用网桥

如果 Linux 网桥支持 IGMP 侦听，并且 IPv6 流量存在问题，则需要禁用该功能，因为它与 MLD 数据包（多播）交互并且不会通过它们。

```shell
echo -n 0 > /sys/class/net/vmbr0/bridge/multicast_snooping

```

### 数据包未从客户机传递

问题:在访客 CHR 上配置软件接口（VLAN、EoIP、网桥等）后，它会停止把数据传递到路由器之外。

解决方法:检查你的VMS（Virtualization Management System）安全设置，是否允许其他MAC地址通过，是否允许带有VLAN标签的数据包通过。 根据需要调整安全设置，例如允许 MAC 欺骗或某个 MAC 地址范围。 对于 VLAN 接口，通常可以定义允许的 VLAN 标签或 VLAN 标签范围。

### 在各种管理程序中使用 CHR 上的 VLAN

某些管理软件在虚拟机上使用 VLAN 之前，需要先在管理程序本身配置。

#### ESXI

在特定 VM 的端口组或虚拟交换机中启用混杂模式。

_ESX 文档:_

- [https://kb.vmware.com/kb/1002934](https://kb.vmware.com/kb/1002934)
- [https://kb.vmware.com/kb/1004099](https://kb.vmware.com/kb/1004099)

#### Hyper-V

_Hyper-V documentation:_

- [https://technet.microsoft.com/en-us/library/cc816585(v=ws.10).aspx#Anchor\_2](https://technet.microsoft.com/en-us/library/cc816585(v=ws.10).aspx#Anchor_2)

#### bhyve hypervisor

无法在此管理软件上运行 CHR。 CHR 不能作为准虚拟化平台运行。

#### Linode

当创建多个具有相同磁盘大小的 Linode 时，新的 Linode 将具有相同的 systemID。 这会导致获得试用/付费许可证的问题。 为避免这种情况，请在首次启动后和申请试用或付费许可证之前运行命令“/system license generate-new-id”。 确保 ID 是唯一的。

_一些有用的文章:_

NIC 接口未标记特定 VLAN:

- [https://blogs.msdn.microsoft.com/adamfazio/2008/11/14/understanding-hyper-v-vlans/](https://blogs.msdn.microsoft.com/adamfazio/2008/11/14/understanding-hyper-v-vlans/)
- [https://www.aidanfinn.com/?p=10164](https://www.aidanfinn.com/?p=10164)

允许通过其他的VLAN:

- [https://social.technet.microsoft.com/Forums/windows/en-US/79d36d5b-c794-4502-8ed4-b7a4183b1891/vlan-tags-and-hyperv-switches?forum=winserverhyperv](https://social.technet.microsoft.com/Forums/windows/en-US/79d36d5b-c794-4502-8ed4-b7a4183b1891/vlan-tags-and-hyperv-switches?forum=winserverhyperv)

## VMWare

### 时间同步

必须从 GUI 启用（“与主机同步时间”）。 默认情况下禁用反向同步 - 如果客户机领先主机超过 ~5 秒，则不执行同步

### 电源操作

- _poweron_ 和 _resume_ 脚本分别在开机和恢复操作后执行（如果存在并启用）。
- _poweroff_ 和 _suspend_ 脚本分别在关机和挂起操作之前执行。
- 如果脚本花费的时间超过 30 秒或包含错误，则操作失败
- 如果失败，重试相同的操作将忽略任何错误并成功完成
- 失败的脚本输出被保存到文件（例如'poweroff-script.log'，'resume-script.log'等）
- 可以从管理程序 GUI（“运行 VMware 工具脚本”）或通过控制台启用/禁用脚本

### 暂停/备份

客户机文件系统暂停仅在请求时执行。

- _freeze_ 脚本在冻结文件系统之前执行
- 如果管理软件无法准备快照或 _freeze_ 脚本失败，则执行 _freeze-fail_ 脚本
- _thaw_ 脚本在拍摄快照后执行
- 脚本运行时间限制为 60 秒
- _freeze_ 脚本超时和错误导致备份操作中止
- FAT32 磁盘未暂停
- 将失败的脚本输出保存到文件中（例如“freeze-script.log”、“freeze-fail-script.log”、“thaw-script.log”）

### 客户机信息

网络、磁盘和操作系统信息每 30 秒向管理程序报告一次（默认情况下，GuestStats（内存）被禁用，可以通过在 VM 配置中设置“guestinfo.disable-perfmon =“FALSE””来启用）。

- 报告网络接口的顺序可以通过设置“guestinfo.exclude-nics”、“guestinfo.primary-nics”和“guestinfo.low-priority-nics”选项来控制。 可以使用标准 [wildcard](https://www.tldp.org/LDP/GNU-Linux-Tools-Summary/html/x11655.htm) 模式。

### 条款

可以使用 vim API 中的 [ProcessManager](https://www.vmware.com/support/developer/converter-sdk/conv55_apireference/vim.vm.guest.ProcessManager.html) 来执行脚本。 Python 绑定 [可用](https://github.com/vmware/pyvmomi)

- 主要数据结构:[GuestProgramSpec](https://www.vmware.com/support/developer/converter-sdk/conv55_apireference/vim.vm.guest.ProcessManager.ProgramSpec.html)
  - _workingDirectory_ 和 _envVariables_ 成员被忽略
  - _programPath_ 必须设置为“inline”或“import”
  - 如果 _programPath_ 是'**inline'**，_arguments_ 被解释为脚本文本
  - 如果 _programPath_ 是'**import'**，_arguments_ 被解释为文件路径

在将 _GuestProgramSpec_ 与 [GuestAuthentication](https://www.vmware.com/support/developer/converter-sdk/conv55_apireference/vim.vm.guest.GuestAuthentication.html) 实例一起用作 [StartProgramInGuest](https://www.vmware.com/support/developer/converter-sdk/conv55_apireference/vim.vm.guest.ProcessManager.html#startProgram) 的参数后获得唯一的 _JobID_。

可以使用 [ListProcessesInGuest](https://www.vmware.com/support/developer/converter-sdk/conv55_apireference/vim.vm.guest.ProcessManager.html#listProcesses) 命令跟踪脚本进度。 _ListProcessesInGuest_ 接受作业 ID 的数组； 传递一个空数组将报告从 API 启动的所有作业

可以使用 [ListProcessesInGuest](https://www.vmware.com/support/developer/converter-sdk/conv55_apireference/vim.vm.guest.ProcessManager.html#listProcesses) 命令跟踪脚本进度。 _ListProcessesInGuest_ 接受作业 ID 的数组； 传递一个空数组将报告从 API 启动的所有作业

- _ListProcessesInGuest_ 返回 [GuestProcessInfo](https://www.vmware.com/support/developer/converter-sdk/conv55_apireference/vim.vm.guest.ProcessManager.ProcessInfo.html) 实例数组:
  - _pid_ 字段设置为 _JobID_
  - _endTime_ 仅在完成后设置
  - 成功时 _exitCode_ 设置为 0，错误时设置为 -1
  - _name_ 设置为“inline”或“import”（与 _GuestProgramSpec_ 中的 _programPath_ 相同）

有关已完成作业的信息将保留约 1 分钟，或直到调用 _ListProcessesInGuest_（具有相应的  _JobID_ ）。 如果脚本失败，则会创建一个名为“vix\_job\_$JobID$ .txt”的文件，其中包含脚本输出。 脚本运行时间限制为 120 秒，脚本输出不会在超时时保存，

- 也可以使用 [vmrun](https://www.vmware.com/pdf/vix160_vmrun_command.pdf) 命令 _runScriptInGuest_
- [PowerCLI](https://code.vmware.com/doc/preview?id=5975#/doc/Overview.html) 命令 [Invoke-VMScript](https://code.vmware.com/doc/preview?id=5975#/doc/Invoke-VMScript.html) 不支持
- 不支持主机/客户机文件传输

#### Python示例

```shell
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,time
from pyVim import connect
from pyVmomi import vmodl,vim


def runInline(content,vm,creds,source):
    ''' Execute script source on vm '''
    if isinstance(source, list):
        source = '\n'.join(source)
    ps = vim.vm.guest.ProcessManager.ProgramSpec(
                programPath = 'console',
                arguments = source
        )
    return content.guestOperationsManager.processManager.StartProgramInGuest(vm,creds,ps)

def runFromFile(content,vm,creds,fileName):
    ''' Execute script file located on CHR '''
    ps = vim.vm.guest.ProcessManager.ProgramSpec(
                programPath = 'import',
                arguments = fileName
    )
    return content.guestOperationsManager.processManager.StartProgramInGuest(vm,creds,ps)


def findDatastore(content,name):
    sessionManager = content.sessionManager

    dcenterObjView = content.viewManager.CreateContainerView(content.rootFolder, [vim.Datacenter], True)

    datacenter = None
    datastore = None
    for dc in dcenterObjView.view:
        dstoreObjView = content.viewManager.CreateContainerView(dc, [vim.Datastore], True)
        for ds in dstoreObjView:
            if ds.info.name == name:
                datacenter = dc
                datastore = ds
                break
        dstoreObjView.Destroy()

    dcenterObjView.Destroy()

    return datacenter,datastore

def _FAILURE(s,*a):
    print(s.format(*a))
    sys.exit(-1)

#------------------------------------------------------------------------------#

if __name__ == '__main__':
    host = sys.argv[1] # ip or something
    user = 'root'
    pwd = 'MikroTik'
    vmName = 'chr-test'
    dataStoreName = 'datastore1'



    service = connect.SmartConnectNoSSL(host=host,user=user,pwd=pwd)
    if not service:
        _FAILURE("Could not connect to the specified host using specified username and password")

    content = service.RetrieveContent()


    #---------------------------------------------------------------------------
    # Find datacenter and datastore


    datacenter,datastore = findDatastore(content,dataStoreName)

    if not datacenter or not datastore:
        connect.Disconnect(service)
        _FAILURE('Could not find datastore \'{}\'',dataStorename)


    #---------------------------------------------------------------------------
    # Locate vm


    vmxPath = '[{0}] {1}/{1}.vmx'.format(dataStoreName, vmName)
    vm = content.searchIndex.FindByDatastorePath(datacenter, vmxPath)

    if not vm:
        connect.Disconnect(service)
        _FAILURE("Could not locate vm")


    #---------------------------------------------------------------------------
    # Setup credentials from user name and pasword

    creds = vim.vm.guest.NamePasswordAuthentication(username = 'admin', password = '')


    #---------------------------------------------------------------------------
    # Run script

    pm = content.guestOperationsManager.processManager

    try:
        # Run script
        src = [':ip address add address=192.168.0.1/24 interface=ether1;']
        jobID = runInline(content, vm, creds, src)

        # Or run file (from FTP root)
        # jobID = runFromFile(content,vm,creds, 'scripts/provision.rsc')


        #---------------------------------------------------------------------------
        # Wait for job to finish

        pm = content.guestOperationsManager.processManager
        jobInfo = pm.ListProcessesInGuest(vm, creds, [jobID])[0]
        while jobInfo.endTime is None:
            time.sleep(1.0)
            jobInfo = pm.ListProcessesInGuest(vm, creds, [jobID])[0]

        if jobInfo.exitCode != 0:
            _FAILURE('Script failed!')
    except:
        raise
    else:
        connect.Disconnect(service)


```

## KVM

QEMU 客户机代理可用。 可以用 guest-info 命令检索支持的代理命令。 可以用 guest-file-* 命令执行主机-客户机文件传输。 可以使用 guest-network-get-interfaces 命令检索客户机网络信息。

- 可以通过使用 guest-exec 命令和 GuestExec 数据结构来执行脚本:
  - 如果提供了 _path_ 成员，则执行相应的文件
  - 如果未设置 _path_ 成员且提供了 _input-data_ 成员，则 _input-data_ 值用作脚本输入
  - 如果设置了 _capture-output_ ，则报告脚本输出
  - _args_ 和 _env_ 成员未使用

- 可以使用 guest-exec-status 命令监控脚本作业进度。 GuestExecStatus 数据结构填充如下:
  - 成功时 _exitcode_ 成员设置为 0
  - 如果脚本超时_exitcode_设置为1
  - 如果脚本包含错误 _exitcode_ 设置为 -1
  - _signal_ 成员未设置
  - 未使用 _err-data_ 成员
  - 如果 _capture-output_ 为真，则 Base64 编码的脚本输出存储在 _out-data_ 中

- 还提供了一个额外的代理隧道（'chr.provision_channel'）
