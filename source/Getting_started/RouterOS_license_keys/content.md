# 概述

运行 RouterOS 的 MikroTik 硬件路由器预装了 RouterOS 许可证，如果你购买了基于 RouterOS 的设备，则无需对许可证进行任何操作。

对于 X86 系统（即 PC 设备），你需要获得许可证密钥。

许可证密钥是一个符号块，需要从你的 [mikrotik.com](https://mikrotik.com) 帐户或你收到的电子邮件中复制，然后将其粘贴到路由器中。 你可以将密钥粘贴到终端中的任意位置，或者单击 Winbox 许可证菜单中的“粘贴密钥”。 密钥需要重新启动才能生效。

![](https://help.mikrotik.com/docs/download/attachments/328149/licence.png?version=1&modificationDate=1574161824111&api=v2)

> RouterOS 许可方案基于软件 ID / 系统 ID，其中：  
- RouterBOARD software-id 绑定到存储介质（HDD、NAND）。
- x86 软件 ID 绑定到 MBR 
- CHR system-id 绑定到 MBR 和 UUID

可以从 CLI 系统控制台查看许可信息：

```shell
[admin@RB1100] > /system license print
    software-id: "43NU-NLT9"
         nlevel: 6
       features:
[admin@RB1100] >
```

或者从 [WinBox](https://help.mikrotik.com/docs/display/ROS7/Winbox),  [WebFig](https://help.mikrotik.com/docs/display/ROS7/Webfig) 菜单查看.

## 许可证等级

安装后 RouterOS 以 **试用模式** 运行。 你有 24 小时的时间注册 Level1（免费演示）或购买 Level 4,5 或 6 许可证并粘贴有效密钥。

第 3 级仅包含无线站（客户端或 CPE）许可证。 _对于 x86 PC，Level3 不能单独购买。_

Level 2 是旧版（pre 2.8）许可证格式的过渡许可证。 这些许可证不再可用，如果你有此类许可证，也可以用，但如果要升级 - 则必须购买新的许可证。

许可证级别之间的差异如下表所示。

| 等级号                       | 0 (试用)                                         | 1 (免费演示)                                          | 3 (WISP CPE) | 4 (WISP)  | 5 (WISP)  | 6 (控制器) |
| ---------------------------- | ------------------------------------------------ | ----------------------------------------------------- | ------------ | --------- | --------- | ---------- |
| 价格                         | [no key](https://www.mikrotik.com/download.html) | [registration required](https://mikrotik.com/client/) | not for sale | $45       | $95       | $250       |
| Wireless AP mode (PtM)       | 24h trial                                        | -                                                     | no           | yes       | yes       | yes        |
| PPPoE tunnels                | 24h trial                                        | 1                                                     | 200          | 200       | 500       | unlimited  |
| PPTP tunnels                 | 24h trial                                        | 1                                                     | 200          | 200       | 500       | unlimited  |
| L2TP tunnels                 | 24h trial	1                                      | 200                                                   | 200          | 500       | unlimited |
| OVPN tunnels                 | 24h trial                                        | 1                                                     | 200          | 200       | unlimited | unlimited  |
| EoIP tunnels                 | 24h trial                                        | 1                                                     | unlimited    | unlimited | unlimited | unlimited  |
| VLAN interfaces              | 24h trial                                        | 1                                                     | unlimited    | unlimited | unlimited | unlimited  |
| Queue rules                  | 24h trial                                        | 1                                                     | unlimited    | unlimited | unlimited | unlimited  |
| HotSpot active users         | 24h trial                                        | 1                                                     | 1            | 200       | 500       | unlimited  |
| User manager active sessions | 24h trial                                        | 1                                                     | 10           | 20        | 50        | Unlimited  |

所有许可证：

- 永不过期（正在运行的路由器可以无限期使用）
- 可以使用无限数量的接口
- 每个许可只能安装一次
- 提供无限的软件升级

___

## CHR 许可证等级  

前面描述的许可证级别不适用于云托管路由器 (CHR)。 CHR 是用于作为虚拟机运行的 RouterOS 版本。 它有自己的 4 个许可级别以及试用版，你可以在其中测试任何付费许可级别 60 天。

所有付费许可级别均提供 60 天免费试用。 要获得免费试用许可证，必须在 [MikroTik.com](https://mikrotik.com/) 上拥有一个帐户，所有许可证都在那里管理。

Perpetual 是终身许可证（一次购买，永久使用）。 可以将永久许可证转移到另一个 CHR 实例。 正在运行的 CHR 实例会指示必须访问帐户服务器以更新其许可证的时间。 如果 CHR 实例无法续订许可证，它将表现为试用期结束，不再允许将 RouterOS 升级到新版本。

授权正在运行的试用系统，**必须** 从 CHR 手动运行“/system license renew”命令以激活。 否则系统将不知道你已在帐户中获取了许可证。 如果你不在系统试用时间之前执行此操作，试用就会结束，只能进行全新的 CHR 安装，请求新的试用，然后使用获得的许可证对其进行授权。

| 许可证       | 速度限制  | 价格                                                                          | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------ | --------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Free         | 1Mbit     | FREE                                                                          | 免费许可证允许 CHR 无限期运行。每个接口的上传速度限制为 1Mbps。 CHR 提供的所有其他功能都可以不受限制地使用。要使用它，要做的就是从我们的下载页面下载磁盘映像文件并创建一个虚拟客户机。                                                                                                                                                                                                                                                                                                                                                                                                          |
| P1           | 1Gbit     | $45                                                                           | P1（perpetual-1）许可证级别允许 CHR 无限期运行。每个接口的上传速度限制为 1Gbps。 CHR 提供的所有其他功能都可以不受限制地使用。可以将 p1 升级到 p10 或 p-unlimited，购买升级后，以前的许可证将可供以后在你的帐户上使用。                                                                                                                                                                                                                                                                                                                                                                          |
| P10          | 10Gbit    | $95                                                                           | P10 (perpetual-10) 许可证级别允许 CHR 无限期运行。每个接口的上传速度限制为 10Gbps。 CHR 提供的所有其他功能都可以不受限制地使用。购买升级后，可以将 p10 升级到 p-unlimited ，以前的许可证可供以后在你的帐户上使用。                                                                                                                                                                                                                                                                                                                                                                              |
| P-Unlimited  | Unlimited | $250                                                                          | p-unlimited（perpetual-unlimited）许可证级别允许 CHR 无限期运行。它是最高级别的许可证，没有强制限制。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 60-day Trial | FREE      | 除了有限的免费安装，你还可以通过 60 次试用来测试 P1/P10/PU 许可证的提升速度。 | 必须在 MikroTik.com 上注册一个帐户。然后从路由器请求所需的试用许可级别，这会把路由器 ID 分配给你的帐户，并允许从该帐户购买许可证。 所有付费许可证均可试用。 试用期为从获取之日起的 60 天，超过此时间后，你的许可证菜单会显示“限制升级”，意味着 RouterOS 无法再升级。<br>注意，如果你计划购买所选许可证，则必须在 60 天试用期结束前购买。 如果试用已结束，并且在 2 个月内没有购买，该设备将不再出现在你的 MikroTik 帐户中。 必须在规定的时间内购买新的 CHR 来安装。<br>要申请试用许可证，必须从 CHR 设备命令行运行命令“/system license renew”。 系统将要求提供 mikrotik.com 帐户的用户名和密码。 |

> **警告：** 如果你计划使用多个相同类型的虚拟系统，下一台机器可能具有与原始机器相同的 SystemID。 这可能会发生在某些云提供商身上，例如 Linode。 为避免这种情况，请在首次启动后运行命令“`/system license generate-new-id`”，然后再申请试用许可证。 请注意，只有当 CHR 在免费类型的 RouterOS 许可证上运行时，才能使用此功能。 如果你已经获得付费或试用许可证，请不要使用该功能，因为无法再更新当前密钥。<br>要使用多个虚拟机，请从我们的网页下载磁盘映像，并根据你需要的虚拟机制作尽可能多的副本。 然后从每个虚拟磁盘映像制作新的虚拟机系统。<br>确保在运行或注册下载的文件之前制作磁盘映像的副本。

___

## 更换密钥

如果你在运行 RouterOS 的 x86 实例上不小心丢失了许可证，并且 Mikrotik 支持员工认为这不是你的问题，那么会由 MikroTik 支持团队颁发特殊密钥。 它的价格为 10 美元，和丢失的密钥有相同的功能。

请注意，在发布此类密钥之前，Mikrotik 支持人员可能会要求你证明旧驱动器发生故障，在某些情况下，可能需要把坏驱动器发送给我们。

### 更换密钥请求

**1)** 转到 [mikrotik.com](https://mikrotik.com/) 中的帐户管理并填写 “[支持联系表](https://mikrotik.com/client/support)” 或直接写邮件至 [support@mikrotik.com](mailto:support@mikrotik.com)
- 请提供有关为什么需要更换钥匙的详细信息

**2)** 将所需信息发送给 MikroTik 支持部门。
**3)** 在支持人员确认替换密钥已添加到你的帐户后，重新检查你的帐户。 选择“Make a key from replacement key”

![](https://help.mikrotik.com/docs/download/thumbnails/328149/Replacement_license_1.png?version=1&modificationDate=1571228257006&api=v2)

**4)** 选择你希望执行更换的适当许可级别
**5)** 输入新的“software-ID”
**6)** 按照“Add license replacement to cart”说明结帐并完成付款

![](https://help.mikrotik.com/docs/download/attachments/328149/Replacement_license_2.png?version=1&modificationDate=1571228301481&api=v2)

**7)** 一封包含新许可证的电子邮件将发送到你的邮箱。

- 你还可以在“Purchased YYYY”文件夹下的“Search and view all keys”部分找到新生成的密钥，其中“YYYY”是当前年份

> _我们只为每个原始密钥发放一次替换密钥，不会为一个密钥使用两次替换密钥程序。 在此情况下，必须购买此 RouterOS 设备的新密钥。_

___

## 获取许可证并使用

### 我在哪里可以买到 RouterOS 许可证密钥？

MikroTik 设备预装了许可证，无需购买。

要获得更高级别的许可证，或获得 x86 PC 安装的许可证，必须注册一个 [网页上的帐户](https://www.mikrotik.com/client)，然后在其中选择“ Purchase a RouterOS license key”。

### 如果我在别处购买了密钥

联系向你出售许可证的公司，他们会提供支持。

### 如果我有许可证并想把它放在另一个帐户上？

可以在 [虚拟文件夹](https://wiki.mikrotik.com/wiki/Virtual_Folders "虚拟文件夹") 的帮助下授予对密钥的访问权限

唯一一种可以转移到另一个帐户的许可证是预付费密钥，它是从 MUM 购买或获得的。 培训赠送的预付密钥不可转让。
要转移购买的预付费密钥，请导航至 MikroTik 帐户上“ROUTEROS KEYS”部分中的“Transfer prepaid keys”。

### 如果丢失了设备上的许可证怎么办？

如果由于某种原因你丢失了路由器的许可证，请将路由器升级到可用的最新 RouterOS 版本并在你的 [mikrotik.com](https://mikrotik.com/) 帐户中使用“请求许可证密钥”。 申请许可证时，请使用 RouterOS 系统/许可证菜单下可用的软件ID和序列号。 如果请求功能不起作用，请用收到的许可证或联系 [support@mikrotik.com](mailto:support@mikrotik.com)。

_如果许可证因维修而丢失，并且不在保修期内，则你将必须以全价购买新的 RouterOS 许可证！_

## 使用许可证

### 我可以格式化驱动器吗？

使用非 MikroTik 工具（如 DD 和 Fdisk）格式化和重新映像驱动器将破坏你的许可证！ 在执行此操作之前要非常小心并联系 mikrotik 支持。 不建议这样做，因为 MikroTik 支持可能会拒绝你的更换许可证请求。 为此，MikroTik 提供了可从我们的下载页面免费获得的工具 Netinstall 或 CD 安装。

### 我可以在几台电脑上使用许可证？

RouterOS 许可证只能在一个系统中使用。 许可证绑定到安装它的 HDD，但你可以将 HDD 移动到另一个计算机系统。 不能将许可证移动到另一个硬盘，也不能用 RouterOS 许可证格式化或覆盖硬盘， 否则它将从驱动器中删除，这样你只能获取一个新的。 如果你不小心删除了许可证，请联系支持团队寻求帮助。

### 除了 RouterOS，我可以临时将 HDD 用于其他用途吗？

如上所述，不行。

### 我可以将许可证移动到另一个 HDD 吗？

如果你当前的 HDD 驱动器损坏或无法再使用，则可以将许可证转移到另一个 HDD。 你必须申请更换密钥（见下文），费用为 10 美元

### 我必须将整个密钥输入路由器吗？

只需将其复制并粘贴到菜单 **System** \--> **License**，

![](https://help.mikrotik.com/docs/download/attachments/328149/ApplyLicenseWinbox.png?version=1&modificationDate=1571228726339&api=v2)

### 我可以在我的驱动器上安装另一个操作系统，然后再安装 RouterOS 吗？

不行，因为如果你使用格式化、分区实用程序或对 MBR 执行某些操作的工具，将丢失许可证，只能制作一个新许可证。 这个过程不是免费的（见上面的更换密钥）

### 我丢失了我的 RouterBOARD，能给我在另一个系统上使用的许可证吗？

MikroTik 硬件带有嵌入式许可证。 你不能以任何方式将此许可证移动到新系统，包括在 MikroTik 路由器仍在工作时应用的任何升级。

### 从经销商处购买的许可证

你从其他供应商和经销商处购买的密钥不在你的帐户中。 你的 [mikrotik.com](https://mikrotik.com/) 帐户仅包含直接从 MikroTik 购买的许可证。 但是，你可以使用你帐户中的“Request key”链接将密钥获取到你的帐户中以供参考，或用于某些升级（如果可用）。

**我没有使用该软件，你们可以终止我的许可吗？**

许可证是独立密钥，MikroTik 无法远程控制你的设备。 因此，我们无法验证你是否使用你的许可证。 这就是为什么 MikroTik 不能终止任何已颁发的许可证。
