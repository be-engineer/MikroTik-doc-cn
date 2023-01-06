## 许可证等级

安装后 RouterOS 以**试用模式**运行。 您有 24 小时的时间注册 Level1（免费演示）或购买 Level 4,5 或 6 许可证并粘贴有效密钥。

第 3 级仅包含无线站（客户端或 CPE）许可证。 _对于 x86 PC，Level3 不可单独购买。_

Level 2 是旧版（pre 2.8）许可证格式的过渡许可证。 这些许可证不再可用，如果您有此类许可证，它会起作用，但要升级它 - 您将必须购买新的许可证。

许可证级别之间的差异如下表所示。

<table><colgroup><col><col><col><col><col><col><col></colgroup><tbody><tr><th title="Background colour : Grey" data-highlight-colour="grey"><strong title="">等级号</strong></th><th title="Background colour : Grey" data-highlight-colour="grey"><strong title="">0 (试用)</strong></th><th title="Background colour : Grey" data-highlight-colour="grey"><strong title="">1 (免费演示)</strong></th><th title="Background colour : Grey" data-highlight-colour="grey"><strong title="">3 (WISP CPE)</strong></th><th title="Background colour : Grey" data-highlight-colour="grey"><strong title="">4 (WISP)</strong></th><th title="Background colour : Grey" data-highlight-colour="grey"><strong title="">5 (WISP)</strong></th><th title="Background colour : Grey" data-highlight-colour="grey"><strong title="">6 (控制器)</strong></th></tr><tr><td><strong>Price</strong></td><td><a href="https://www.mikrotik.com/download.html" rel="nofollow">no key</a></td><td><a href="https://mikrotik.com/client/" rel="nofollow">registration required</a></td><td><span>not for sale</span></td><td><span>$45</span></td><td><span>$95</span></td><td><span>$250</span></td></tr><tr><td><strong>Wireless AP mode (PtM)</strong></td><td>24h trial</td><td>-</td><td>no</td><td>yes</td><td>yes</td><td>yes</td></tr><tr><td><strong>PPPoE tunnels</strong></td><td>24h trial</td><td>1</td><td>200</td><td>200</td><td>500</td><td>unlimited</td></tr><tr><td><strong>PPTP tunnels</strong></td><td>24h trial</td><td>1</td><td>200</td><td>200</td><td>500</td><td>unlimited</td></tr><tr><td><strong>L2TP tunnels</strong></td><td>24h trial</td><td>1</td><td>200</td><td>200</td><td>500</td><td>unlimited</td></tr><tr><td><strong>OVPN tunnels</strong></td><td>24h trial</td><td>1</td><td>200</td><td>200</td><td>unlimited</td><td>unlimited</td></tr><tr><td colspan="1"><strong>EoIP tunnels</strong></td><td colspan="1">24h trial</td><td colspan="1">1</td><td colspan="1">unlimited</td><td colspan="1">unlimited</td><td colspan="1">unlimited</td><td colspan="1">unlimited</td></tr><tr><td colspan="1"><strong>VLAN interfaces</strong></td><td colspan="1">24h trial</td><td colspan="1">1</td><td colspan="1">unlimited</td><td colspan="1">unlimited</td><td colspan="1">unlimited</td><td colspan="1">unlimited</td></tr><tr><td colspan="1"><strong>Queue rules</strong></td><td colspan="1">24h trial</td><td colspan="1">1</td><td colspan="1">unlimited</td><td colspan="1">unlimited</td><td colspan="1">unlimited</td><td colspan="1">unlimited</td></tr><tr><td><strong>HotSpot active users</strong></td><td>24h trial</td><td>1</td><td>1</td><td>200</td><td>500</td><td>unlimited</td></tr><tr><td><strong>User manager active sessions</strong></td><td>24h trial</td><td>1</td><td>10</td><td>20</td><td>50</td><td>Unlimited</td></tr></tbody></table>

所有许可证：

- 永不过期（正在运行和许可的路由器可以无限期使用）
- 可以使用无限数量的接口
- 每个可安装一次
- 提供无限的软件升级

___

## CHR 许可证等级  

前面描述的许可证级别不适用于云托管路由器 (CHR)。 CHR 是用于作为虚拟机运行的 RouterOS 版本。 它有自己的 4 个许可级别以及试用版，您可以在其中测试任何付费许可级别 60 天。

所有付费许可证级别均提供 60 天免费试用许可。 要获得免费试用许可证，您必须在 [MikroTik.com](https://mikrotik.com/) 上拥有一个帐户，因为所有许可证管理都在那里完成。

Perpetual 是终身许可证（一次购买，永久使用）。 可以将永久许可证转移到另一个 CHR 实例。 正在运行的 CHR 实例将指示它必须访问帐户服务器以更新其许可证的时间。 如果 CHR 实例无法续订许许可证，它将表现为试用期用完，并且不允许将 RouterOS 升级到更新版本。

许可正在运行的试用系统，您**必须**从 CHR 手动运行“/system license renew”命令以使其激活。 否则系统将不知道您已在帐户中获取了许可证。 如果您不在系统截止时间之前执行此操作，试用将结束，您将必须进行全新的 CHR 安装，请求新的试用，然后使用您获得的许可证对其进行许可证。

<table><colgroup><col><col><col><col></colgroup><tbody><tr><th>许可证</th><th>速度限制</th><th>价格</th><th colspan="1">说明</th></tr><tr><td>Free</td><td>1Mbit</td><td>FREE</td><td colspan="1">免费许可证级别允许 CHR 无限期运行。每个接口的上传速度限制为 1Mbps。 CHR 提供的所有其他功能都可以不受限制地使用。要使用它，您所要做的就是从我们的下载页面下载磁盘映像文件并创建一个虚拟客户机。</td></tr><tr><td>P1</td><td>1Gbit</td><td>$45</td><td colspan="1">P1（perpetual-1）许可证级别允许 CHR 无限期运行。每个接口的上传速度限制为 1Gbps。 CHR 提供的所有其他功能都可以不受限制地使用。可以将 p1 升级到 p10 或 p-unlimited 购买升级后，以前的许可证将可供您以后在您的帐户上使用。</td></tr><tr><td>P10</td><td>10Gbit</td><td>$95</td><td colspan="1">P10 (perpetual-10) 许可证级别允许 CHR 无限期运行。每个接口的上传速度限制为 10Gbps。 CHR 提供的所有其他功能都可以不受限制地使用。购买升级后，可以将 p10 升级到 p-unlimited ，以前的许可证将可供您以后在您的帐户上使用。</td></tr><tr><td>P-Unlimited</td><td>Unlimited</td><td><p>$250</p></td><td colspan="1">p-unlimited（perpetual-unlimited）许可证级别允许 CHR 无限期运行。它是最高级别的许可证，没有强制限制。</td></tr><tr><td colspan="1">60-day Trial</td><td colspan="1"><br></td><td colspan="1">FREE</td><td colspan="1"><p>除了有限的免费安装，您还可以通过 60 次试用来测试 P1/P10/PU 许可证的提升速度。

您必须在 MikroTik.com 上注册一个帐户。 然后可以从路由器请求所需的试用许可级别，这会将您的路由器 ID 分配给您的帐户，并允许从您的帐户购买许可证。 所有付费许可证均可试用。 试用期为从获取之日起的 60 天，超过此时间后，您的许可证菜单将开始显示“有限升级”，这意味着 RouterOS 无法再升级。

请注意，如果您计划购买所选许可证，则必须在 60 天试用期结束前购买。 如果您的试用已结束，并且在 2 个月内没有购买，该设备将不再出现在您的 MikroTik 帐户中。 必须在规定的时间内购买新的 CHR 安装。

要申请试用许可证，您必须从 CHR 设备命令行运行命令“/system license renew”。 系统将要求提供 mikrotik.com 帐户的用户名和密码。</p></td></tr></tbody></table>

!!!warning **警告：**如果您计划使用多个相同类型的虚拟系统，则下一台机器可能具有与原始机器相同的 SystemID。 这可能发生在某些云提供商身上，例如 Linode。 为避免这种情况，请在首次启动后运行命令“`/system license generate-new-id`”，然后再申请试用许可证。 请注意，只有当 CHR 在免费类型的 RouterOS 许可证上运行时，才能使用此功能。 如果您已经获得付费或试用许可证，请不要使用重新生成功能，因为您将无法再更新当前密钥

要使用多个虚拟机，请从我们的网页下载磁盘映像，并根据您需要的虚拟机制作尽可能多的副本。 然后从每个虚拟磁盘映像制作新的虚拟机系统。

确保在运行或注册下载的文件之前制作磁盘映像的副本。

___

## 更换密钥

如果您在运行 RouterOS 的 x86 实例上不小心丢失了许可证，并且 Mikrotik 支持员工认为这不是您的错，那么会由 MikroTik 支持团队颁发特殊密钥。 它的价格为 10 美元，和丢失的密钥有相同的功能。

请注意，在发布此类密钥之前，Mikrotik 支持人员可能会要求您证明旧驱动器发生故障，在某些情况下，这意味着将坏驱动器发送给我们。

#### 更换密钥请求

**1)** 转到 [mikrotik.com](https://mikrotik.com/) 中的帐户管理并填写“[支持联系表](https://mikrotik.com/client/support)” 或直接写邮件至[support@mikrotik.com](mailto:support@mikrotik.com)

- 请提供有关为什么需要更换钥匙的详细信息

**2)** 将所需信息发送给 MikroTik 支持部门。

**3)** 在支持人员确认替换密钥已添加到您的帐户后，重新检查您的帐户。 选择“Make a key from replacement key”

![](https://help.mikrotik.com/docs/download/thumbnails/328149/Replacement_license_1.png?version=1&modificationDate=1571228257006&api=v2)

**4)** 选择您希望执行更换的适当许可级别

**5)** 输入新的“软件 ID”

**6)** 按照“将许可证更换添加到购物车”说明结帐并完成付款

![](https://help.mikrotik.com/docs/download/attachments/328149/Replacement_license_2.png?version=1&modificationDate=1571228301481&api=v2)

**7)** 一封包含新许可证的电子邮件将发送到您的邮箱。

- 您还可以在“Purchased YYYY”文件夹下的“Search and view all keys”部分找到新生成的密钥，其中“YYYY”是当前年份

!!!info _我们只为每个原始密钥发放一次替换密钥，不会为一个密钥使用两次替换密钥程序。 在此情况下，必须购买此 RouterOS 设备的新密钥。_

___

## 获取许可证并使用

#### 我在哪里可以买到 RouterOS 许可证密钥？

MikroTik 设备预装了许可证，无需购买。

要获得更高级别的许可证，或获得 x86 PC 安装的许可证，必须注册一个[我们网页上的帐户](https://www.mikrotik.com/client)，然后在其中使用选项“ 购买 RouterOS 许可证密钥”。

#### 如果我在别处购买了密钥

您必须联系向您出售许可证的公司，他们将提供支持。

#### 如果我有许可证并想把它放在另一个帐户上？

您可以在 [虚拟文件夹](https://wiki.mikrotik.com/wiki/Virtual_Folders "虚拟文件夹") 的帮助下授予对密钥的访问权限

唯一一种可以转移到另一个帐户的许可证是预付费密钥，它是从 MUM 购买或获得的。 培训赠送的预付密钥不可转让。
要转移购买的预付费密钥，请导航至 MikroTik 帐户上“ROUTEROS KEYS”部分中的“转移预付费密钥”。

#### 如果我丢失了设备上的许可证？

如果由于某种原因您丢失了路由器的许可证，请将路由器升级到可用的最新 RouterOS 版本并在您的 [mikrotik.com](https://mikrotik.com/) 帐户中使用“请求许可证密钥”。 申请许可证时，请使用 RouterOS 系统/许可证菜单下可用的软 ID 和序列号。 如果请求功能不起作用，请用收到的许可证或联系 [support@mikrotik.com](mailto:support@mikrotik.com)。

_如果许可证因维修而丢失，并且不是在保修期内完成的，您将必须以全价购买新的 RouterOS 许可证！_
___

## 使用许可证

#### 我可以格式化或重新闪存驱动器吗？

使用非 MikroTik 工具（如 DD 和 Fdisk）格式化和重新映像驱动器将破坏您的许可证！ 在执行此操作之前要非常小心并联系 mikrotik 支持。 不建议这样做，因为 MikroTik 支持可能会拒绝您的更换许可证请求。 为此，MikroTik 提供了可从我们的下载页面免费获得的工具 Netinstall 或 CD 安装。

#### 我可以在多少台电脑上使用许可证？

RouterOS 许可证只能在一个系统中使用。 许可证绑定到安装它的 HDD，但您可以将 HDD 移动到另一个计算机系统。 您不能将许可证移动到另一个硬盘，也不能用 RouterOS 许可证格式化或覆盖硬盘。 它将从驱动器中删除，这样您只能获取一个新的。 如果您不小心删除了许可证，请联系支持团队寻求帮助。

#### 除了 RouterOS，我可以临时将 HDD 用于其他用途吗？

如上所述，不行。

#### 我可以将许可证移动到另一个 HDD 吗？

如果您当前的 HDD 驱动器损坏或无法再使用，则可以将许可证转移到另一个 HDD。 您必须申请更换密钥（见下文），费用为 10 美元

#### 我必须将整个密钥输入路由器吗？

只需将其复制并粘贴到菜单 **System** \--> **License**，

![](https://help.mikrotik.com/docs/download/attachments/328149/ApplyLicenseWinbox.png?version=1&modificationDate=1571228726339&api=v2)

#### 我可以在我的驱动器上安装另一个操作系统，然后再安装 RouterOS 吗？

不行，因为如果您使用格式化、分区实用程序或对 MBR 执行某些操作的工具，将丢失许可证，必须制作一个新许可证。 这个过程不是免费的（见上面的更换密钥）

#### 我丢失了我的 RouterBOARD，能给我在另一个系统上使用的许可证吗？

MikroTik 硬件带有嵌入式许可证。 您不能以任何方式将此许可证移动到新系统，这包括在 MikroTik 路由器仍在工作时应用的任何升级。

#### 从经销商处购买的许可证

您从其他供应商和经销商处购买的密钥不在您的帐户中。 您的 [mikrotik.com](https://mikrotik.com/) 帐户仅包含直接从 MikroTik 购买的许可证。 但是，您可以使用您帐户中的“请求密钥”链接，将密钥获取到您的帐户中以供参考，或用于某些升级（如果可用）。

**我没有使用该软件，你们可以终止我的许可吗？**

许可证是独立密钥，MikroTik 无法远程控制您的设备。 因此，我们无法验证您是否使用您的许可证。 这就是为什么 MikroTik 不能终止任何已颁发的许可证。