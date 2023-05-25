# AP控制器概述

CAPsMAN允许通过中央配置界面对多个microtik AP设备进行无线设置。

更具体地说，受控接入点系统管理器(CAPsMAN)允许无线网络管理的集中化，并在必要时进行数据处理。当使用CAPsMAN功能时，网络将由许多提供无线连接的“受控接入点”(CAP)和管理ap配置的“系统管理器”(CAPsMAN)组成，它还负责客户端身份验证和可选的数据转发。

当CAP由CAPsMAN控制时，只需要允许它与CAPsMAN建立连接所需的最小配置。传统上由AP执行的功能(如访问控制、客户端身份验证)现在由CAPsMAN执行。CAP设备现在只需要提供无线链路层加密/解密。

根据配置的不同，数据可以转发到CAPsMAN进行集中处理(_default_)，也可以在CAP本身进行本地转发(本地转发模式)。

  

需求

—任何拥有RouterOS 4级以上license的设备都可以成为受控无线接入点(CAP)
—CAPsMAN服务器可以安装在任何RouterOS设备上，即使设备本身没有无线接口
-无限CAPs(接入点)由CAPsMAN支持
每个CAP最多32个无线电
-每个主无线电接口最多32个虚拟接口
-不可能使用Nv2和nstream专有协议


简单设置一个CAPsMAN系统

![](https://help.mikrotik.com/docs/download/attachments/1409149/Simple_capsman_topology.png?version=2&modificationDate=1621329464382&api=v2)

在深入研究CAPsMAN操作的细节之前，让我们快速说明如何设置最基本的系统，这里有一个管理两个MikroTik AP设备的MikroTik路由器。CAPsMAN的好处是不需要配置CAP单元，所有设置都在CAPsMAN服务器中完成。

CAPsMAN设置包括定义配置模板，然后将其推送到可控制的AP设备(cap)。假设您的主路由器已经连接到互联网并且工作正常，可以按照以下步骤进行操作。

在中心设备(CAPsMAN服务器)中，仅使用基本设置(网络名称，国家，本地局域网桥接接口，无线密码)创建一个新的“Configuration”模板:

1. ![add new configuration profile](https://help.mikrotik.com/docs/download/attachments/1409149/Simple_CAPsMAN_Step2_1.png?version=1&modificationDate=1571145422722&api=v2 "add new configuration profile") 
   
2. ![](https://help.mikrotik.com/docs/download/attachments/1409149/Simple_CAPsMAN_Step2_2.png?version=1&modificationDate=1571145422560&api=v2) 
   
3. ![](https://help.mikrotik.com/docs/download/attachments/1409149/Simple_CAPsMAN_Step2_3.png?version=1&modificationDate=1571145422327&api=v2)

然后创建一个新的“Provisioning”规则，将创建的配置模板分配给CAP设备:

4. ![](https://help.mikrotik.com/docs/download/attachments/1409149/Simple_CAPsMAN_Step2_4.png?version=1&modificationDate=1571145422213&api=v2)

对于CAPsMAN，剩下要做的就是启用它:

5. ![](https://help.mikrotik.com/docs/download/attachments/1409149/Simple_CAPsMAN_Step2_8.png?version=1&modificationDate=1571145422121&api=v2)

大多数microtik AP设备已经开箱即用地支持CAP模式，所需的就是确保它们与CAPsMAN在同一网络上，然后启动它们，同时按住重置按钮。

因此，例如，在CAPsMAN设备LAN端口关闭时，将CAP设备连接到其中一个CAPsMAN设备LAN端口，然后按住复位按钮，给CAP设备上电。一直按住按钮，直到用户LED变成固体，现在释放以打开CAP模式。设备现在将寻找一个CAPsMAN服务器(总时间按住按钮，大约10秒)。

该设备现在将显示在CAPsMAN“Remote CAP”菜单中，并将根据配置设置使用配置模板进行“配置”。有关如何手动调整所有设置的更多详细信息，请继续阅读本文档。

CAP到CAPsMAN连接

为了使CAPsMAN系统发挥作用并提供无线连接，CAP必须与CAPsMAN建立管理连接。管理连接可以使用MAC或IP层协议建立，并使用“DTLS”进行保护。

CAP也可以将客户端数据连接传递给管理器，但是数据连接是不安全的。如果认为这是必要的，则需要使用其他数据安全手段，例如IPSec或加密隧道。

CAP到CAPsMAN连接可以使用2个传输协议(通过第2层和第3层)建立。

- MAC层连接特性:
    - 不需要在CAP上配置IP
    - CAP和CAPsMAN必须在同一第二层网段上——物理的或者虚拟的(通过L2隧道)
- IP层(UDP)连接特性:
    - 必要时可以遍历NAT
    - CAP必须能够通过IP协议到达CAPsMAN
    如果CAP和CAPsMAN不在同一L2网段，则必须配置CAPsMAN的IP地址，因为基于IP组播的发现不能在Layer3上工作

为了与CAPsMAN建立连接，CAP执行一个发现过程。在发现过程中，CAP尝试联系CAPsMAN并构建一个可用的CAPsMAN列表。CAP尝试使用以下命令联系可用的CAPsMAN:

- 配置的Manager IP地址列表
- 从DHCP服务器获取的CAPsMAN IP地址列表
- 在配置的接口上同时使用IP层和MAC层协议进行广播。

当建立可用CAPsMAN列表时，CAP根据以下规则选择CAPsMAN:

- 如果caps-man-names参数指定允许的管理器名称(CAPsMAN的/system identity)，CAP将优先选择列表中较早的CAPsMAN，如果列表为空，它将连接到任何可用的管理器
- 优先选择具有MAC层连通性的管理器，而不选择具有IP层连通性的管理器

选择Manager后，CAP尝试建立DTLS连接。认证方式有以下几种:

- 没有CAP和CAPsMAN证书-没有认证
- 只有Manager配置了证书—CAP检查CAPsMAN的证书，如果没有合适的可信CA证书则不会失败，CAPsMAN必须配置require-peer-certificate=no才能与没有证书的CAP建立连接
- CAP和CAPsMAN配置证书互鉴

DTLS连接建立后，CAP可以选择性地检查CAPsMAN提供的证书的CommonName字段。caps-man-certificate-common-names参数包含允许的CommonName值列表。如果此列表不为空，则CAPsMAN必须配置证书。如果该列表为空，则CAP不检查CommonName字段。

如果CAPsMAN或CAP与网络断开，大约在10-20秒内检测到CAP与CAPsMAN之间的连接丢失。

自动锁定到CAPsMAN

可以将CAP配置为自动锁定到特定的CAPsMAN服务器。锁定是通过记录CAP被锁定的CAPsMAN的证书CommonName，并在所有后续连接中检查该CommonName来实现的。由于该特性是使用证书CommonName实现的，因此必须使用证书才能使锁定生效。

使用如下命令开启锁定功能:

```
[admin@CAP] > /interface wireless cap set lock-to-caps-man=yes

```

一旦CAP连接到合适的CAPsMAN并锁定它，它就会像这样反射:

```
[admin@wtp] > /interface wireless cap print
...
        locked-caps-man-common-name: CAPsMAN-000C424C30F3

```

从现在开始，CAP将只使用此CommonName连接到CAPsMAN，直到锁定要求被清除，通过设置lock-to-caps-man=no。如果有必要强制CAP锁定到另一个CAPsMAN，则需要使用这种方法——设置lock-to-caps-man=no，然后设置lock-to-caps-man=yes。

注意，可以通过设置caps-man-certificate-common-names将CAP手动“锁定”到CAPsMAN。

### 自动证书

为了在需要证书时简化CAPsMAN和CAP的配置(例如自动锁定功能)，CAPsMAN可以配置为自动生成必要的证书，而CAP可以配置为从CAPsMAN请求证书。

自动证书不提供完整的公钥基础设施，只提供简单的设置。如果需要更复杂的PKI(支持适当的证书有效期、多级CA证书、证书续签)，则必须使用其他方法，如手动证书分发或SCEP。

CAPsMAN有以下证书设置:

- **证书** -这是CAPsMAN证书，该证书必须有私钥。如果设置为 **none**， CAPsMAN将在无证书模式下运行，并且所有需要证书的功能都不起作用。如果设置为 **auto**， CAPsMAN将尝试使用CA证书向自己颁发证书(参见CA -certificate描述)。请注意，CommonName自动颁发的证书将是“CAPsMAN-<mac地址>”，有效期将与CA证书相同。
- **CA -certificate** -这是CAPsMAN在必要时为自己颁发证书时将使用的CA证书(参见证书描述)，以及在签署来自CAPs的证书请求时使用。如果设置为 **none**， CAPsMAN将无法向自己颁发证书或签署来自CAPs的证书请求。如果设置为 **auto**， CAPsMAN将生成自签名CA证书作为CA证书使用。该证书的通用名称形式为“CAPsMAN-CA-<mac地址>”，有效期为1970年1月1日至2038年1月18日。

当CAPsMAN自动生成证书时，这将反映如下:

```
[admin@CM] /caps-man manager> pr
                   enabled: yes
               certificate: auto
            ca-certificate: auto
  require-peer-certificate: no
     generated-certificate: CAPsMAN-000C424C30F3
  generated-ca-certificate: CAPsMAN-CA-000C424C30F3

```

证书:

```
[admin@CM] /certificate> print detail
Flags: K - private-key, D - dsa, L - crl, C - smart-card-key, 
A - authority, I - issued, R - revoked, E - expired, T - trusted 
 0 K   A T name="CAPsMAN-CA-000C424C30F3" common-name="CAPsMAN-CA-000C424C30F3" key-size=2048 
           days-valid=24854 trusted=yes 
           key-usage=digital-signature,key-encipherment,data-encipherment,key-cert-sign,crl-sign 
           serial-number="1" fingerprint="69d77bbb45c50afd2d6c1785c2a3d72596b8a5f6" 
           invalid-before=jan/01/1970 00:00:01 invalid-after=jan/18/2038 03:14:07 

 1 K   I   name="CAPsMAN-000C424C30F3" common-name="CAPsMAN-000C424C30F3" key-size=2048 
           days-valid=24854 trusted=no key-usage=digital-signature,key-encipherment 
           ca=CAPsMAN-CA-000C424C30F3 serial-number="1" 
           fingerprint="e853ddb9d41fc139083a176ab164331bc24bc5ed" 
           invalid-before=jan/01/1970 00:00:01 invalid-after=jan/18/2038 03:14:07 

```

CAP可以配置为从CAPsMAN请求证书。为了使其工作，CAP必须配置为设置certificate=request， CAPsMAN必须具有可用的CA证书(在 CA -certificate设置中指定或自动生成)。

CAP将首先生成私钥和证书请求，其CommonName形式为“CAP-<mac地址>”。当CAP与CAPsMAN建立连接时，CAP将要求CAPsMAN签署其证书请求。如果成功，CAPsMAN将向CAP发送CA证书和新颁发的证书。CAP将在其证书存储库中导入这些证书:

```
[admin@CAP] > /interface wireless cap print
...
              requested-certificate: cert_2
        locked-caps-man-common-name: CAPsMAN-000C424C30F3
[admin@CAP] > /certificate print detail 
Flags: K - private-key, D - dsa, L - crl, C - smart-card-key, 
A - authority, I - issued, R - revoked, E - expired, T - trusted 
 0       T name="cert_1" issuer=CN=CAPsMAN-CA-000C424C30F3 common-name="CAPsMAN-CA-000C424C30F3" 
           key-size=2048 days-valid=24837 trusted=yes 
           key-usage=digital-signature,key-encipherment,data-encipherment,key-cert-sign,crl-sign 
           serial-number="1" fingerprint="69d77bbb45c50afd2d6c1785c2a3d72596b8a5f6" 
           invalid-before=jan/01/1970 00:00:01 invalid-after=jan/01/2038 03:14:07 

 1 K     T name="cert_2" issuer=CN=CAPsMAN-CA-000C424C30F3 common-name="CAP-000C4200C032" 
           key-size=2048 days-valid=24837 trusted=yes 
           key-usage=digital-signature,key-encipherment serial-number="2" 
           fingerprint="2c85bf2fbc9fc0832e47cd2773a6f4b6af35ef65" 
           invalid-before=jan/01/1970 00:00:01 invalid-after=jan/01/2038 03:14:07 

```

On subsequent connections to CAPsMAN, CAP will use generated certificate.



# CAP配置

当AP配置为CAPsMAN控制时，忽略AP上被管理的无线接口的配置(天线增益、天线模式除外)。相反，AP接受来自CAPsMAN的管理接口的配置。

由CAPsMAN管理的CAP无线接口，其流量被转发给CAPsMAN(即CAPsMAN)。它们不是在本地转发模式)，显示为disabled，并注明Managed by CAPsMAN。那些处于“本地转发”模式的接口(流量在本地由CAP管理，仅由CAPsMAN管理)不显示为禁用，但显示“managed by CAPsMAN”

  

AP的CAP行为在/interface wireless CAP菜单中配置。那里可以:

- 在设备上使能或禁用CAP特性
- 设置管理中心控制的无线接口列表
- 设置CAP应该尝试发现Manager的接口列表
- 设置CAP在发现过程中尝试联系的管理器IP地址列表
- 设置CAP将尝试连接的管理器名称列表
- 设置CAP将连接到的Manager证书CommonNames列表
- 配置使用本地转发方式时接口加入的桥接器


在CAPsMAN控制下的CAP上的每个无线接口在CAPsMAN上显示为一个虚拟接口。这为使用常规RouterOS功能(如路由、桥接、防火墙等)的数据转发控制提供了最大的灵活性

许多无线接口设置可以分组到命名组(“配置文件”)中，从而简化配置的重用——例如，可以在“配置文件”中配置公共配置设置，然后多个接口可以引用该配置文件。同时，任何配置文件设置都可以在接口配置中直接覆盖，以获得最大的灵活性。

目前有以下设置组:

- channel -通道相关设置，如频率和宽度
- datapath -数据转发的相关设置，例如桥接，特定的接口应该自动添加为端口
- security -安全相关设置，如允许的认证类型或密码
- configuration -主无线设置组，包括SSID等设置，并另外绑定其他设置组-即配置文件可以引用信道、安全等命名设置组。此外，任何设置都可以在配置文件中直接覆盖。

接口设置将所有设置组绑定在一起，但另外任何设置都可以在接口设置中直接覆盖。

通过设置组，以接口(配置的实际用户)为根，将配置组织成层次结构。为了计算出某些设置的有效值，以一种较高级别设置值覆盖较低级别设置值的方式咨询此结构。

例如，当需要找到特定接口使用的WPA2 passphrase时，将查询以下位置，并且配置了WPA2 passphrase的第一个位置指定有效的passphrase。"->"表示指向配置文件(如果已配置):

- 接口密码
- interface->security passphrase
- interface->configuration passphrase
- interface->configuration->security passphrase

在CAPsMAN上有2种类型的接口-“主”和“从”。主接口保存实际无线接口(无线电)的配置，而从接口链接到主接口，并用于保存Virtual-AP(支持多个SSID)的配置。有些设置只对主界面有意义，即主要是与硬件设置相关的设置，如无线电频道设置。请注意，为了使无线电接收客户端，需要启用它的主接口。只有启用了从接口，并且启用了主接口，从接口才可以运行。

CAPsMAN的接口可以是静态的，也可以是动态的。静态接口存储在RouterOS配置中，并且会在重启期间持续存在。动态接口仅在特定CAP连接到CAPsMAN时才存在。

CAPsMAN全局配置

启用CAPsMAN功能的设置在 **/caps-man manager** 菜单中找到:

| 属性                                                                                            | 说明                                                                                                                                                                                                                                       |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **enabled** (_yes\| no_; Default: **no**)                                                       | 禁用或启用CAPsMAN功能                                                                                                                                                                                                                      |
| **certificate** (_auto\|certificate name\| none_;Default:**none**)                              | 设备证书                                                                                                                                                                                                                                   |
| **ca-certificate** (_auto\|certificate name\| none_;Default:**none**)                           | 设备CA证书                                                                                                                                                                                                                                 |
| **require-peer-certificate** (_yes \| no_;Default:**no**)                                       | 要求所有连接的CAPs具有有效的证书                                                                                                                                                                                                           |
| **package-path** (_string\|_;Default:)                                                          | RouterOS包的文件夹位置。例如，使用"/upgrade"从files部分指定升级文件夹。如果设置为空字符串，则CAPsMAN可以使用内置的RouterOS包，注意在这种情况下，只有与CAPsMAN架构相同的cap才会升级。                                                       |
| **upgrade-policy** (_none \| require-same-version  \| suggest-same-upgrade_; Default: **none**) | 升级策略选项<br>- none -不升级<br>- require-same-version - CAPsMAN建议升级CAP的RouterOS版本，如果升级失败，则不会再发放CAP(手动发放仍然是可能的)。<br>- suggest-same-version - CAPsMAN建议升级CAP RouterOS版本，如果升级失败，仍会继续发放 |

## 无线电供应

CAPsMAN根据标识符来区分CAPs。该标识符的生成规则如下:

—如果CAP提供了证书，则“标识符”设置为证书中的Common Name字段
—其他标识符基于CAP提供的Base-MAC，格式为:'[XX:XX:XX:XX:XX]'。

当与CAP的DTLS连接成功建立时(这意味着CAP标识符是已知且有效的)，CAPsMAN确保使用相同标识符的与CAP的连接没有失效。当前连接的CAPs列在/CAPs-man remote-cap菜单中:

```shell
[admin@CM] /caps-man> remote-cap print
 # ADDRESS                                    IDENT           STATE               RADIOS
 0 00:0C:42:00:C0:32/27044                    MT-000C4200C032 Run                      1

```

CAPsMAN根据其内置MAC地址(radio-mac)区分实际的无线接口(无线电)。这意味着在一个CAPsMAN上管理两个具有相同MAC地址的无线电是不可能的。目前由CAPsMAN管理的无线电(由连接的CAPs提供)列在/CAPs-man radio菜单中:

```shell
[admin@CM] /caps-man> radio print
Flags: L - local, P - provisioned 
 #    RADIO-MAC         INTERFACE                               REMOTE-AP-IDENT
 0  P 00:03:7F:48:CC:07 cap1                                    MT-000C4200C032

```

当CAP连接时，CAPsMAN首先尝试将每个CAP无线电绑定到基于无线电mac的CAPsMAN主接口上。如果找到合适的接口，则使用主接口配置和引用特定主接口的从接口配置来设置无线电。此时，接口(包括主接口和从接口)被认为绑定到无线电，无线电被认为是供应的。

如果没有找到匹配的无线电主接口，CAPsMAN执行“供应规则”。供应规则是一个有序的规则列表，其中包含指定要匹配哪个无线电的设置，以及指定如果无线电匹配要采取什么操作的设置。


匹配无线电的发放规则在/caps-man Provisioning菜单中配置:

| 属性                                                                                                  | 说明                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **action** (_create-disabled \| create-enabled \| create-dynamic-enabled \| none_; Default: **none**) | 如果规则匹配由以下设置指定，则采取的操作:<br>- **create-disabled** -创建禁用的无线静态接口。即，接口将被绑定到无线电，但无线电将不会运行，直到手动启用接口;<br>- **create-enabled** -创建已启用的静态接口。也就是说，接口将被绑定到无线电，无线电将是可操作的;<br>- **create-dynamic-enabled** -创建启用的动态接口。也就是说，接口将被绑定到无线电，无线电将是可操作的;<br>- **none** -什么都不做，无线电处于未提供状态; |
| **comment** (_string_; Default: )                                                                     | 发放规则的简要说明                                                                                                                                                                                                                                                                                                                                                                                                       |
| **common-name-regexp** (_string_;Default:)                                                            | 通过通用名称                                                                                                                                                                                                                                                                                                                                                                                                             | 匹配无线电的正则表达式 |
| **hw-supported-modes**  (_a\|a-turbo\|ac\|an\|b\|g\|g-turbo\|gn_;  Default: )                         | 按支持的无线模式匹配无线电                                                                                                                                                                                                                                                                                                                                                                                               |
| **identity-regexp** (_string_;Default:)                                                               | 根据路由器标识匹配无线电的正则表达式                                                                                                                                                                                                                                                                                                                                                                                     |
| **ip-address-ranges** (_IpAddressRange[，IpAddressRanges] max 100x_;Default:**""**)                   | 在配置的地址范围内匹配CAPs和ip。                                                                                                                                                                                                                                                                                                                                                                                         |
| **master-configuration** (_string_;Default:)                                                          | 如果**action**指定创建接口，则将创建一个新的主接口，其配置设置为此配置文件                                                                                                                                                                                                                                                                                                                                               |
| **name-format** (_cap \| identity \| prefix \| prefix-identity_; Default: **cap**)                    | 指定创建CAP接口名称的语法<br>- cap -默认名称<br>- identity - CAP板的系统标识名称<br>-prefix - name从name-prefix的值中提取<br>- prefix-identity - name从name-prefix的值和CAP板的系统标识名中提取                                                                                                                                                                                                                          |
| **name-prefix** (_string_; Default: )                                                                 | 名称前缀，可以在名称格式中使用，用于创建CAP接口名称                                                                                                                                                                                                                                                                                                                                                                      |
| **radio-mac** (_MAC address_;Default:**00:00:00:00:00**)                                              | 要匹配的无线电MAC地址，空MAC(00:00:00:00:00)表示匹配所有MAC地址                                                                                                                                                                                                                                                                                                                                                          |
| **slave-configurations** (_string_;Default:)                                                          | 如果action指定创建接口，则为此列表中的每个配置文件创建一个新的从接口。                                                                                                                                                                                                                                                                                                                                                   |

如果没有匹配radio的规则，则隐式默认规则的操作create-enabled和不执行配置集。

要获取活动供应匹配器:

```shell
[admin@CM] /caps-man provisioning> print
Flags: X - disabled 
 0   radio-mac=00:00:00:00:00:00 action=create-enabled master-configuration=main-cfg 
     slave-configurations=virtual-ap-cfg name-prefix=""

```

为了方便用户，有一些命令允许对某些AP提供的某些或所有无线电重新执行配置过程:

```
[admin@CM] > caps-man radio provision 0

```

和

```
[admin@CM] > caps-man remote-cap provision 0

```

## 接口配置

CAPsMAN接口在/caps-man接口菜单中管理:

```
[admin@CM] > /caps-man interface print          
Flags: M - master, D - dynamic, B - bound, X - disabled, I - inactive, R - running 
 #      NAME                                 RADIO-MAC         MASTER-INTERFACE                               
 0 M BR cap2                                 00:0C:42:1B:4E:F5 none                                           
 1   B  cap3                                 00:00:00:00:00:00 cap2                   

```

## 主配置文件

配置文件允许将预定义的“顶级”主设置应用于所提供的CAP无线电。


配置文件在/caps-man Configuration 菜单中配置:

| 属性                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **channel** (_list_; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | 用户自定义的通道名称列表(/caps-man channels)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **channel.band** (_2ghz-b \| 2ghz-b/g\| 2ghz-b/g/n\| 2ghz-onlyg \| 2ghz-onlyn \| 5ghz-a \| 5ghz-a/n \| 5ghz-onlyn \| 5ghz-a/n/ac\| 5ghz-only-ac_; Default: )                                                                                                                                                                                                                                                                                                                                       | 定义一组使用的通道。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **channel.control-channel-width** (_40mhz-turbo\| 20mhz\| 10mhz\| 5mhz_; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                | Defines set of used channel widths.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **channel.extension-channel** (_Ce\| Ceee\| eC\| eCee\| eeCe\| eeeC   \| xx       \| xxxx       \| disabled_; Default: )                                                                                                                                                                                                                                                                                                                                                                           | 扩展通道配置。(如Ce =扩展通道在控制通道上方，eC =扩展通道在控制通道下方)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **channel.frequency** (_integer [0..4294967295]_;Default:)                                                                                                                                                                                                                                                                                                                                                                                                                                         | 以MHz为单位的信道频率值，AP将在其上工作。如果留空，CAPsMAN将自动确定占用最少的最佳频率。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **channel.reselect-interval** (_time [00:00:00]_; _[00:00:00..00:00:00];_ Default: )                                                                                                                                                                                                                                                                                                                                                                                                               | 选择占用频率最小的间隔可以定义为一个随机间隔，例如“30m..60m”。仅当**channel.frequency**为空时有效。                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **channel. save-selected** (_yes \| no_;Default:**no**)                                                                                                                                                                                                                                                                                                                                                                                                                                            | 如果自动选择通道频率和**通道。使用Reselect-interval **，然后保存最后选择的频率。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **channel. secondary-frequency** (_integer [0..4294967295]_;  Default: **auto**)                                                                                                                                                                                                                                                                                                                                                                                                                   | 用于80+80MHz配置的第二个频率。将其设置为Disabled以禁用80+80MHz能力。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **channel. skip-dfs-channels** (_yes \| no_;Default:**no**)                                                                                                                                                                                                                                                                                                                                                                                                                                        | 如果**channel.frequency**为空，选择将跳过DFS通道                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **channel. tx-power** (_integer [-30..40]_;Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                              | CAP接口的TX功率(用于整个接口，而不是单个链)，以dBm为单位。不可能设置高于国家法规或接口允许的值。缺省情况下，使用国家或接口允许的最大值。                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **channel.width** (; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | 以MHz为单位设置信道宽度。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **comment** (_string_;Default:)                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | 配置文件的简短描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **country**(_name of the country )\| no_country_set_;Default:**no_country_set**                                                                                                                                                                                                                                                                                                                                                                                                                    | 限制每个频率的可用频带，频率和最大发射功率。还指定 **scan-list** 的默认值。no_country_set是FCC兼容的通道集合。                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **datapath** (_list_;Default:)                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 用户自定义的数据路径名称列表(/caps-man Datapath )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **datapath.bridge** (_list_;Default:)                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 桥接，特定的接口应自动添加为端口                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **datapath.bridge-cost** (_integer [0..4294967295]_; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                    | 添加为桥接端口时使用的桥接端口费用                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **datapath.bridge-horizon** (_integer [0..4294967295]_;Default:)                                                                                                                                                                                                                                                                                                                                                                                                                                   | 添加为桥接端口时使用的桥接地平线                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **datapath. client-to-client-forwarding** (_yes \| no_;  Default: **no**)                                                                                                                                                                                                                                                                                                                                                                                                                          | 控制连接到接口的无线客户端之间是否允许客户端到客户端转发，在本地转发模式下，此功能由CAP执行，否则由CAPsMAN执行                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **datapath.interface-list** (; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **datapath.l2mtu** (; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | set Layer2 MTU大小                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **datapath.local-forwarding** (_yes \| no_;Default:**no**)                                                                                                                                                                                                                                                                                                                                                                                                                                         | 控制转发模式                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **datapath.mtu** (;Default:)                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | set MTU大小                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **datapath.openflow-switch** (;Default:)                                                                                                                                                                                                                                                                                                                                                                                                                                                           | OpenFlow交换机端口(启用时)添加接口                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **datapath.vlan-id** (_integer [1..4095]_; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                              | 如果VLAN模式允许使用VLAN标记，则分配给接口的VLAN ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **datapath.vlan-mode** (_use-service-tag \| use-tag_; )                                                                                                                                                                                                                                                                                                                                                                                                                                            | 启用并指定要分配给接口的VLAN标签类型(使所有接收到的数据都带有VLAN标签，并允许接口只发送带有给定标签的数据)                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **disconnect-timeout** (; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **distance** (; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **frame-lifetime** (; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **guard-interval** (_any\| long_; Default: **any**)                                                                                                                                                                                                                                                                                                                                                                                                                                                | 是否允许使用短保护间隔(请参阅802.11n MCS规范，以了解如何影响吞吐量)。“any”将根据数据速率使用short或long，“long”将仅使用long。                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **hide-ssid** (_yes \| no_; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                             | - _yes_ - AP在信标帧中不包含SSID，并且对广播SSID的探测请求不予回应。<br>-  _no_ - AP在信标帧中包含SSID，对广播SSID的探测请求进行应答。<br>此属性仅在AP模式下有效。将其设置为 _yes_ 可以将该网络从某些客户端软件显示的无线网络列表中删除。更改此设置不会提高无线网络的安全性，因为SSID包含在AP发送的其他帧中。                                                                                                                                                                                                                                                               |
| **hw-protection-mode** (; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **hw-retries** (; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **installation** (_any \| indoor \| outdoor_; Default: **any**)                                                                                                                                                                                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **keepalive-frames** (_enabled \| disabled_; Default: **enabled**)                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **load-balancing-group** (_string_; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 将接口加入负载分担组。要使客户端连接到该组中的接口，该接口应具有与组中所有其他接口相同或更少的已连接客户端数量。在cap范围大多重叠的设置中非常有用。                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **max- stat -count** (_integer [1..2007]_;Default:)                                                                                                                                                                                                                                                                                                                                                                                                                                                | 最大关联客户端数。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **mode** (;Default:**ap**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | 设置操作模式。目前仅支持ap。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **multicast-helper** (_default \| disabled \| full_; Default: **default**)                                                                                                                                                                                                                                                                                                                                                                                                                         | 当设置为full时，组播数据包将以单播目的MAC地址发送，解决了无线链路上的 [组播问题](https://wiki.mikrotik.com/wiki/Manual:Multicast_detailed_example#Multicast_and_Wireless "Manual:Multicast detailed example")。此选项应仅在接入点上启用，客户端应配置为 **站-网桥** 模式。从v5.15开始可用。<br>- disabled关闭helper功能，发送带组播目的MAC地址的组播报文<br>- full - all组播包的MAC地址在发送之前更改为单播MAC地址<br>- default -当前设置为_disabled_的默认选项。值可以在以后的版本中更改。                                                                                 |
| **name** (_string_; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | 配置文件的描述性名称                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **rate** (;Default:)                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | 用户自定义列表取自费率名称(/caps-man rate)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **rates.basic** (_1Mbps \| 2Mbps \| 5.5Mbps \| 6Mbps \| 11Mbps \| 11Mbps \| 12Mbps \| 18Mbps \| 24Mbps \| 36Mbps \| 48Mbps \| 54Mbps_; Default: )                                                                                                                                                                                                                                                                                                                                                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **rates.supported** (_1Mbps \| 2Mbps \| 5.5Mbps \| 6Mbps \| 11Mbps \| 11Mbps \| 12Mbps \| 18Mbps \| 24Mbps \| 36Mbps \| 48Mbps \| 54Mbps_; Default: )                                                                                                                                                                                                                                                                                                                                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **[rates.ht](https://rates.ht)-basic-mcs** (_list of (mcs-0 \| mcs-1 \| mcs-2 \| mcs-3 \| mcs-4 \| mcs-5 \| mcs-6 \| mcs-7 \| mcs-8 \| mcs-9 \| mcs-10 \| mcs-11 \| mcs-12 \| mcs-13 \| mcs-14 \| mcs-15 \| mcs-16 \| mcs-17 \| mcs-18 \| mcs-19 \| mcs-20 \| mcs-21 \| mcs-22 \| mcs-23)_; Default: **mcs-0; mcs-1; mcs-2; mcs-3; mcs-4; mcs-5; mcs-6; mcs-7**)                                                                                                                                   | [调制和编码方案](https://en.wikipedia.org/wiki/IEEE_802.11n-2009#Data_rates)，每个连接的客户端必须支持。MCS规范请参考802.11n。                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **[rates.ht](https://rates.ht)-supported-mcs** (_list of (mcs-0 \| mcs-1 \| mcs-2 \| mcs-3 \| mcs-4 \| mcs-5 \| mcs-6 \| mcs-7 \| mcs-8 \| mcs-9 \| mcs-10 \| mcs-11 \| mcs-12 \| mcs-13 \| mcs-14 \| mcs-15 \| mcs-16 \| mcs-17 \| mcs-18 \| mcs-19 \| mcs-20 \| mcs-21 \| mcs-22 \| mcs-23)_; Default: **mcs-0; mcs-1; mcs-2; mcs-3; mcs-4; mcs-5; mcs-6; mcs-7; mcs-8; mcs-9; mcs-10; mcs-11; mcs-12; mcs-13; mcs-14; mcs-15; mcs-16; mcs-17; mcs-18; mcs-19; mcs-20; mcs-21; mcs-22; mcs-23**) | [调制和编码方案](https://en.wikipedia.org/wiki/IEEE_802.11n-2009#Data_rates)，该设备宣布支持。MCS规范请参考802.11n。                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **rates.vht-basic-mcs** (_none \| MCS 0-7 \| MCS 0-8 \| MCS 0-9_; Default: **none**)                                                                                                                                                                                                                                                                                                                                                                                                               | [调制和编码方案](https://en.wikipedia.org/wiki/IEEE_802.11ac#Data_rates_and_speed)，每个连接的客户端必须支持。MCS规范请参考802.11ac。<br>您可以设置每个空间流的MCS间隔<br>- _none_ -将不使用选定的空间流<br>- _MCS 0-7_ - client必须支持MCS-0到MCS-7<br>- _MCS 0-8_ - client必须支持MCS-0到MCS-8<br>- _MCS 0-9_ - client必须支持MCS-0到MCS-9                                                                                                                                                                                                                                |
| **rates.vht-supported-mcs** (_none \| MCS 0-7 \| MCS 0-8 \| MCS 0-9_; Default: **none**)                                                                                                                                                                                                                                                                                                                                                                                                           | [调制和编码方案](https://en.wikipedia.org/wiki/IEEE_802.11ac#Data_rates_and_speed)，该设备宣布支持。MCS规范请参考802.11ac。<br>您可以设置每个空间流的MCS间隔<br>- _none_ -将不使用选定的空间流<br>- _MCS 0-7_ -设备将作为支持的MCS-0通告到MCS-7<br>- _MCS 0-8_ -设备将通告为支持的MCS-0到MCS-8<br>- _MCS 0-9_ -设备将作为支持的MCS-0通告到MCS-9                                                                                                                                                                                                                             |
| **rx-chains** (_list of integer [0..2]_; Default: **0**)                                                                                                                                                                                                                                                                                                                                                                                                                                           | 用哪根天线接收。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **security** (_string_;Default:**none**)                                                                                                                                                                                                                                                                                                                                                                                                                                                           | 来自/caps-man security的安全配置名称                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **security. authentication-types**  (_list of string_;Default:**none**)                                                                                                                                                                                                                                                                                                                                                                                                                            | 指定来自 wpa-psk、wpa2-psk、wpa-eap或wpa2-eap的认证类型                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **security.disable-pmkid** (; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **security.eap-methods** (_eap-tls \| passthrough_; Default: **none**)                                                                                                                                                                                                                                                                                                                                                                                                                             | <br>- EAP - TLS -使用内置的EAP TLS认证。<br>- passthrough -接入点将认证过程中继到RADIUS服务器。                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **security.eap-radius-accounting** (; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **security.encryption** (_aes-ccm \| tkip_; Default: _aes-ccm_)                                                                                                                                                                                                                                                                                                                                                                                                                                    | 设置使用的单播加密算法类型                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **security.group-encryption** (_aes-ccm \| tkip_;Default:**aes-ccm**)                                                                                                                                                                                                                                                                                                                                                                                                                              | 接入点发布这些密码中的一个，可以选择多个值。接入点使用它来加密所有广播和组播帧。客户端只尝试连接到使用指定组密码之一的接入点。<br>- tkip -临时密钥完整性协议-加密协议，与传统的WEP设备兼容，但增强以纠正一些WEP缺陷.<br>- AES -ccm -更安全的WPA加密协议，基于可靠的AES (Advanced encryption Standard)。没有WEP遗留的网络应该只使用这个密码。                                                                                                                                                                                                                                |
| **security.group-key-update** (_time: 30s..1h_; Default: **5m**)                                                                                                                                                                                                                                                                                                                                                                                                                                   | 控制访问点更新组密钥的频率。该密钥用于加密所有广播和组播帧。属性仅对接入点有效。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **security.passphrase** (_string_;Default:)                                                                                                                                                                                                                                                                                                                                                                                                                                                        | WPA或WPA2预共享密钥                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **security. tls-certificate** (_none \| name_;Default:)                                                                                                                                                                                                                                                                                                                                                                                                                                            | 当Tls-mode 设置为verify-certificate，或者设置为not -verify-certificate时接入点总是需要一个证书。                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **security.tls-mode** (_verify-certificate \| dont-verify-certificate \| no-certificates_; Default: )                                                                                                                                                                                                                                                                                                                                                                                              | 此属性仅在security. eap-methods包含eap-tls时有效。<br>- verify-certificate -要求远端设备拥有有效的证书。检查它是否由已知的证书颁发机构签名。没有额外的身份验证。证书可能包括有关其有效期间的信息。如果路由器的时间和日期不正确，它可能会因为路由器的时钟超出了时间和日期而拒绝有效的证书。另请参见 [证书](https://wiki.mikrotik.com/wiki/Manual:System/Certificates "Manual:System/Certificates") 配置。<br>- don -verify-certificate—不检查远端设备的证书。接入点不需要客户端提供证书。<br>- no-certificates—不使用证书。TLS会话采用2048位匿名Diffie-Hellman密钥交换建立。 |
| **ssid** (_string (0..32 chars)_; Default: )                                                                                                                                                                                                                                                                                                                                                                                                                                                       | SSID(服务集标识符)是在信标中广播的标识无线网络的名称。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **tx-chains** (_list of integer [0..2]_;Default:**0**)                                                                                                                                                                                                                                                                                                                                                                                                                                             | 使用哪些天线进行传输。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

## 通道组

信道组设置允许配置无线电信道相关设置的列表，例如无线电频带，频率，Tx功率扩展信道和宽度。

频道组设置在频道配置文件菜单/caps-man channels中配置

| 属性                                                                                                                   | 说明                                                                                                                                   |
| ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **band** (_2ghz-b \| 2ghz-b/g\| 2ghz-b/g/n \| 2ghz-onlyg \| 2ghz-onlyn \| 5ghz-a \| 5ghz-a/n\| 5ghz-onlyn_; Default: ) | 根据无线网卡的硬件性能，定义可操作的无线电频带和模式                                                                                   |
| **comment** (_string_;Default:)                                                                                        | 通道组配置文件的简短描述                                                                                                               |
| **extension-channel** (_Ce\| eeee \| eC\| eCee\| eeCe\| eeeC\| disabled_;Default:)                                     | 扩展通道配置。(如Ce =扩展通道在控制通道上方，eC =扩展通道在控制通道下方)                                                               |
| **frequency** (_integer [0..4294967295]_;Default:)                                                                     | 以MHz为单位的信道频率值，AP将在其上工作。                                                                                              |
| **name** (_string_;Default:)                                                                                           | 通道组配置文件的描述性名称                                                                                                             |
| **tx-power** (_integer [-30..40]_; Default: )                                                                          | CAP接口的TX功率(用于整个接口而不是单个链)，以dBm为单位。不可能设置高于国家法规或接口允许的值。缺省情况下，使用国家或接口允许的最大值。 |
| **width** (;Default:)                                                                                                  | 以MHz为单位设置通道宽度。(例20、40                                                                                                     |
| **save-selected** (;Default:**yes**)                                                                                   | 为CAP电台保存选定的频道-将在CAP重新连接到CAPsMAN后选择此频道并使用它，直到为此CAP重新优化频道。                                        |

##数据路径配置

数据路径设置控制数据转发的相关方面。在CAPsMAN中，数据路径设置在数据路径配置文件菜单 **/caps-man datapath** 中配置，或直接在配置文件或界面菜单中配置 **datapath.** 前缀。

主要有两种转发方式:

—本地转发模式，CAP在本地向无线接口转发数据
- manager转发模式，CAP将所有通过无线方式接收到的数据发送给CAPsMAN，只发送从CAPsMAN接收到的无线数据。在这种模式下，甚至客户机到客户机的转发也由CAPsMAN控制和执行。

转发模式是在每个接口的基础上配置的，所以如果一个CAP提供2个无线电接口，一个可以配置为本地转发模式，另一个可以配置为管理转发模式。Virtual-AP接口也是如此，每个接口可以与主接口或其他Virtual-AP接口具有不同的转发模式。

大多数数据路径设置仅在管理员转发模式下使用，因为在本地转发模式下，CAPsMAN无法控制数据转发。

数据路径设置如下:

- bridge - 在启用时，将接口添加为桥接端口
- bridge-cost -添加为桥接端口时使用的桥接端口成本
- bridge-horizon -添加为桥接端口时使用的桥接地平线
- client-to-client-forwarding - 控制连接到接口的无线客户端之间是否允许client-to-client转发，在本地转发模式下，此功能由CAP执行，否则由CAPsMAN执行。
- local-forwarding - 控制转发方式
- OpenFlow -switch - OpenFlow开关，当打开时，将接口添加到端口
- VLAN-ID - 当VLAN -mode使能VLAN标记时，指定给接口的VLAN ID
- VLAN-mode - VLAN标签模式指定是否给接口分配VLAN标签(使所有接收到的数据都带有VLAN标签，并允许接口只发送带有给定标签的数据)

## 本地转发模式

在这种模式下，CAP上的无线接口表现为正常接口，参与正常的数据转发。无线接口将接收/传递数据到CAP上的网络堆栈。CAPsMAN不参与数据转发，也不处理任何数据帧，它只控制接口配置和客户端关联过程。

CAP上的无线接口将其配置更改为“enabled”，其状态和一些相关参数(例如mac-address, arp, mtu)将反映CAPsMAN上的接口。请注意，无线相关配置不会反映CAPsMAN应用的实际接口配置:

```shell
[admin@CAP] /interface wireless> pr
Flags: X - disabled, R - running 
 0  R ;;; managed by CAPsMAN
      ;;; channel: 5180/20-Ceee/ac, SSID: master, local forwarding
      name="wlan2" mtu=1500 mac-address=00:03:7F:48:CC:07 arp=enabled 
      interface-type=Atheros AR9888 mode=ap-bridge ssid="merlin" 
      frequency=5240 band=5ghz-a/n channel-width=20/40mhz-eC scan-list=default
      ...

```

本地转发方式的Virtual-AP接口将显示为已启用和动态Virtual-AP接口:

```shell
[admin@CAP] /interface> pr
Flags: D - dynamic, X - disabled, R - running, S - slave 
 #     NAME                                TYPE         MTU L2MTU  MAX-L2MTU
 ...
 2  RS ;;; managed by CAPsMAN
       ;;; channel: 5180/20-Ceee/ac, SSID: master, local forwarding
       wlan2                               wlan        1500  1600
 3 DRS ;;; managed by CAPsMAN
       ;;; SSID: slave, local forwarding
       wlan6                               wlan        1500  1600
 ...
[admin@CAP] /interface> wireless pr   
Flags: X - disabled, R - running 
 ...
 2  R ;;; managed by CAPsMAN
      ;;; SSID: slave, local forwarding
      name="wlan6" mtu=1500 mac-address=00:00:00:00:00:00 arp=enabled 
      interface-type=virtual-AP master-interface=wlan2 

```

Virtual-AP接口是动态添加的，这在一定程度上限制了CAP上用于数据转发的静态配置的可能性，例如为Virtual-AP接口分配地址。这不适用于主无线接口。

为了克服这个问题，可以在CAP上使用静态虚拟设置，它将创建静态虚拟接口而不是动态接口，并允许为这些接口分配IP配置。MAC地址用于在应用CAPsMAN配置时记住每个静态接口。如果两个或多个静态接口将具有相同的MAC地址，则可以按随机顺序应用配置。

为了方便数据转发配置，CAP可以配置网桥，当CAPsMAN使能接口时，接口会自动加入网桥作为端口。这可以在/interface wireless cap菜单中完成。

## Manager转发模式

在这种模式下，CAP将所有通过无线接收到的数据发送给CAPsMAN，并且只通过无线发送从CAPsMAN接收到的数据。CAPsMAN完全控制数据转发，包括客户端到客户端转发。禁用CAP的无线接口，不参与组网;

```shell
 ...
 1 X  ;;; managed by CAPsMAN
      ;;; channel: 5180/20-Ceee/ac, SSID: master, manager forwarding
      name="wlan2" mtu=1500 mac-address=00:03:7F:48:CC:07 arp=enabled 
      interface-type=Atheros AR9888 mode=ap-bridge ssid="merlin" 
 ...

```

虚拟ap接口也被创建为“禁用”，并且不参与CAP上的数据转发。

## 访问列表

CAPsMAN上的访问列表是一个有序的规则列表，用于允许/拒绝客户端连接到CAPsMAN控制下的任何CAP。当客户端试图连接到由CAPsMAN控制的CAP时，CAP将该请求转发给CAPsMAN。作为注册过程的一部分，CAPsMAN将查询访问列表以确定是否允许客户端连接。访问列表的默认行为是允许连接。

逐个处理访问列表规则，直到找到匹配的规则。然后执行匹配规则中的操作。如果action指定应该接受客户端，则客户端被接受，可能会用访问列表规则中指定的参数重写它的默认连接参数。

访问列表在/caps-man Access -list菜单中配置。访问列表规则有以下参数:

- 客户端匹配参数:
	- address -客户端的MAC地址(或者，如果指定了掩码，则只有这些部分将根据掩码进行检查，因此，为了从“D8: 1c:79:6E:1E:FE”匹配供应商D8，只需输入一个伪造的条目，例如“D8:00:00:00:00”，然后在下一行使用掩码)
	- mask比较客户端地址时使用的MAC地址掩码。例如:FF:00:00:00:00:00只匹配指定MAC地址的第一个字节。在上面的例子中，不管输入的MAC是什么，它只匹配第一个八位字节。类似地，输入00:00:00:00:FF将只匹配假设MAC (D8:1C:79:6E:1E:FE)的最后八位字节(FE)。所以在mac行，你可以输入00:00:00:00:00:00:FE，如果你想使用这样的掩码。
	- interface -可选接口，用于与客户端实际连接的接口进行比较
	- time -规则匹配的时间
	- signal-range -客户端信号匹配规则必须匹配的范围
- 动作参数-指定客户端匹配时采取的操作:
	- accept -接受客户端
	- reject -拒绝客户端
	- query -RADIUS在允许特定客户端连接时查询RADIUS服务器
- 连接参数:
	- ap-tx-limit发送到客户端的速率限制
	- client-tx-limit -到AP方向的tx限速(仅适用于RouterOS客户端)
	- client-to-client-forwarding表示是否允许将从该客户端接收到的数据转发给连接在同一接口上的其他客户端
	- private-passphrase -当使用PSK认证算法时，该客户端使用的PSK密码
	- RADIUS-accounting -指定如果对该客户端进行RADIUS认证，是否使用RADIUS流量计费
	- VLAN-mode - VLAN标记模式指定来自客户端的流量是否被标记(去往客户端的流量不被标记)。
	- VLAN-ID配置VLAN标签时使用的VLAN ID。

## 注册表

注册表包含连接到由CAPsMAN控制的无线电的客户端列表，可在/caps-man注册表菜单中使用:

```shell
[admin@CM] /caps-man> registration-table print
 # INTERFACE                   MAC-ADDRESS       UPTIME                RX-SIGNAL
 0 cap1                        00:03:7F:48:CC:0B 1h38m9s210ms                -36

```

**例子**

## 基本配置与主和从接口

创建WPA2 PSK安全配置文件，不指定密码短语:

```shell
[admin@CM] /caps-man security>add name="wpa2psk" authentication-types=wpa2-psk encryption=aes-ccm

```

创建主接口使用的配置文件

- 在配置中指定WPA2密码
- 在配置中指定通道设置:

```
[admin@CM] /caps-man configuration> add name=master-cfg ssid=master security=wpa2psk
security.passphrase=12345678 channel.frequency=5180 channel.width=20 channel.band=5ghz-a

```

创建虚拟AP接口使用的配置文件

- 配置不同的WPA2密码:

```shell
[admin@CM] /caps-man configuration> add name=slave-cfg ssid=slave security=wpa2psk
security.passphrase=87654321

```

使用master-cfg和slave-cfg创建匹配任意无线电的配置规则，并创建动态接口:

```shell
[admin@CM] /caps-man provisioning> add action=create-dynamic-enabled master-configuration=master-cfg
slave-configurations=slave-cfg

```

现在，当AP连接并配置时，将创建2个动态接口(一个主接口和一个从接口):

```shell
[admin@CM] /caps-man interface> print detail 
Flags: M - master, D - dynamic, B - bound, X - disabled, I - inactive, R - running 
 0 MDB  name="cap1" mtu=1500 l2mtu=2300 radio-mac=00:0C:42:1B:4E:F5 master-interface=none 
        configuration=master-cfg 

 1  DB  name="cap2" mtu=1500 l2mtu=2300 radio-mac=00:00:00:00:00:00 master-interface=cap1 
        configuration=slave-cfg 

```

考虑一个AP，它不支持配置的频率连接，不能运行:

```shell
[admin@CM] /caps-man interface> pr
Flags: M - master, D - dynamic, B - bound, X - disabled, I - inactive, R - running 
 #      NAME                                 RADIO-MAC         MASTER-INTERFACE                               
 0 MDB  ;;; unsupported band or channel
        cap3                                 00:0C:42:1B:4E:FF none    
 ...

```

可以在接口设置中覆盖这个特定无线电的通道设置，而不影响master-cfg配置文件:

```shell
[admin@CM] /caps-man interface> set cap3 channel.frequency=2142 channel.band=2ghz-b/g

```

允许特定MAC地址范围匹配访问列表，例如，匹配所有Apple设备:

```shell
[admin@CM] /caps-man access-list> add mac-address=18:34:51:00:00:00 mac-address-mask=FF:FF:FF:00:00:00 action=accept

```

配置DHCP Server Option 138用于在CAP板上设置CAPsMAN地址

```shell
[admin@CM] /ip dhcp-server network set <network-id> caps-manager=<capsman-server-ip>

```

在"/ip dhcp-client print detail"中可以看到这个CAPsMAN IP的DHCP客户端

## 配置证书

您可能希望在您的CAPsMAN中配置证书，以使用_Require Peer Certificate_和_Lock to Caps Man_等选项。这些选项提高了CAPsMAN网络的安全性，在某些情况下还提高了稳定性。如果没有特定的证书，CAPs将不会连接到CAPsMAN，反之亦然。

### 快速简单的配置

这是在CAPsMAN设置中使用证书的基本配置。这个例子假设您已经有了CAPsMAN和CAP的基本配置。最好在不经常增长的CAPsMAN网络中使用这个配置。欲了解更多详情，请参阅 [CAP到CAPsMAN连接](https://wiki.mikrotik.com/wiki/Manual:CAPsMAN#CAP_to_CAPsMAN_Connection) 。

**CAPsMAN装置:**

在CAPsMAN Manager菜单中设置Certificate和CA Certificate为auto:

```
/caps-man manager
set ca-certificate=auto certificate=auto

```

打印输出:

```shell
[admin@CAPsMAN] /caps-man manager print 
                   enabled: yes
               certificate: auto
            ca-certificate: auto
              package-path: 
            upgrade-policy: none
  require-peer-certificate: no
     generated-certificate: CAPsMAN-D4CA6D987C26
  generated-ca-certificate: CAPsMAN-CA-D4CA6D987C26

```

CAPsMAN设备首先生成CA-Certificate，然后生成Certificate，这取决于CA-Certificate。

**CAP装置:**

在CAP配置中设置为 _request_ 证书:

```
/interface wireless cap
set certificate=request

```

CAP将连接到CAPsMAN并请求证书。CAP将从CAPsMAN收到CA-Certificate，并将创建另一个证书用于CAP。

**结果**

在CAP设备上的CAP菜单中设置了 _Requested Certificate_:

```shell
[admin@CAP] /interface wireless cap print
                            enabled: yes
                         interfaces: wlan1
                        certificate: request
                   lock-to-caps-man: no
               discovery-interfaces: ether1
                 caps-man-addresses: 
                     caps-man-names: 
  caps-man-certificate-common-names: 
                             bridge: none
                     static-virtual: no
         -->  requested-certificate: CAP-D4CA6D7F45BA  <--

```

此外，还获得了两个证书，可以在Certificate菜单中看到:

```shell
[admin@CAP] > /certificate print 
Flags: K - private-key, D - dsa, L - crl, C - smart-card-key, A - authority, I - issued, R - revoked, E - expired, T - trusted 
 #          NAME              COMMON-NAME              SUBJECT-ALT-NAME                                           FINGERPRINT             
 0     A  T _0                CAPsMAN-CA-D4CA6D987C26                                                             383e63d7b...
 1 K        CAP-D4CA6D7F45BA  CAP-D4CA6D7F45BA                                                                    d495d1a94...

```

在CAPsMAN设备的Certificate菜单中创建了三个证书。CAPsMAN和CAPsMAN- ca证书，以及发给CAP的证书:

```shell
[admin@CAPsMAN] > /certificate print 
Flags: K - private-key, D - dsa, L - crl, C - smart-card-key, A - authority, I - issued, R - revoked, E - expired, T - trusted 
 #          NAME                     COMMON-NAME              SUBJECT-ALT-NAME                                    FINGERPRINT         
 0 K   A  T CAPsMAN-CA-D4CA6D987C26  CAPsMAN-CA-D4CA6D987C26                                                      383e63d7b...
 1 K    I   CAPsMAN-D4CA6D987C26     CAPsMAN-D4CA6D987C26                                                         02b0f7ff4...
 2      I   issued_1                 CAP-D4CA6D7F45BA                                                             d495d1a94...

```

另外,如果您想只允许具有有效证书的CAPs连接到此CAPsMAN，您可以将CAPsMAN设备上的 _Require Peer Certificate_ 设为 _yes_:

```
/caps-man manager
set require-peer-certificate=yes

```

但是，当您想要向CAPsMAN网络添加新的CAP设备时，您必须将此选项设置为 _no_ ，然后在CAP获得证书后将其设置为 _yes_ 。每次更改此选项时，CAPsMAN将删除所有动态接口，CAPs将尝试再次连接。

如果您想将CAP锁定到特定的CAPsMAN，并确保它不会连接到其他CAPsMAN，您应该将选项_Lock to CAPsMAN_设置为 _yes_ 。另外，您可以通过在CAP设备上设置 _CAPsMAN证书通用名称_ 来指定要锁定的CAPsMAN:

```shell
/interface wireless cap
set lock-to-caps-man=yes
set caps-man-certificate-common-names=CAPsMAN-D4CA6D987C26

```

### 使用SCEP手动颁发证书

在这个示例中，您可以为CAPsMAN创建自己的证书，并控制向cap颁发证书。这种配置在大型、不断增长的CAPsMAN网络中非常有用。根据您的情况和需求，本示例的许多部分可以以不同的方式完成。在这一点上，一些关于 [证书](https://wiki.mikrotik.com/wiki/Manual:System/Certificates "Manual:System/Certificates") 和 [应用程序](https://wiki.mikrotik.com/wiki/Manual:Create_Certificates "Manual:Create Certificates") 的知识是有用的。

**CAPsMAN设备:**

在 _Certificate_ 菜单中添加CA证书和CAPsMAN服务器证书的证书模板:

```
/certificate
add name=CA-temp common-name=CA
add name=CAPsMAN-temp common-name=CAPsMAN

```

现在对证书模板进行_Sign_。首先_签署_CA证书，并使用CAPsMAN设备IP作为 _CA CRL Host_ :

```
/certificate
sign CA-temp ca-crl-host=10.5.138.157 name=CA
sign CAPsMAN-temp ca=CA name=CAPsMAN

```

或者，前两个步骤可以在CAPsMAN Manager菜单中的 _Certificate_ 和 _CA-Certificate_ 选项中自动设置，参见 [快速简单配置](https://wiki.mikrotik.com/wiki/Manual:CAPsMAN#Fast_and_easy_configuration)。

_Export_ CA证书。必须在CAP设备上Import。可以使用 _Download -> Drag&Drop_ 到CAP设备，在本例中，_fetch_ 命令稍后从CAP设备使用。建议使用较长的密码短语——如果密码落入坏人之手，较长的密码短语将花费更长的时间来破解:

```
/certificate
export-certificate CA export-passphrase=thelongerthebetterpassphrase

```

创建 _SCEP server_ ，用于向CAP设备颁发和授予证书:

```
/certificate scep-server
add ca-cert=CA path=/scep/CAPsMAN

```

在CAPsMAN Manager菜单中设置证书，并将 _Require Peer certifate_ 设置为yes:

```
/caps-man manager
set ca-certificate=CA certificate=CAPsMAN
set require-peer-certificate=yes

```

此时，只有具有有效证书的cap才能连接。

**CAP设备**

下载从CAPsMAN设备导出CA证书到CAP设备。在这个例子中使用了 _fetch_ ，但是，还有多种其他方法:

```
/tool fetch address=10.5.138.157 src-path=cert_export_CA.crt user=admin password="123" mode=ftp

```

在 _Certificate_ 菜单中从CAPsMAN设备导入CA证书:

```
/certificate> import file-name=cert_export_CA.crt passphrase=thelongerthebetterpassphrase

```

为CAP添加证书模板:

```
/certificate
add name=CAP1 common-name=CAP1

```

要求CAPsMAN设备使用SCEP使用密钥授予此证书:

```
/certificate
add-scep template=CAP1 scep-url="https://10.5.138.157/scep/CAPsMAN"

```

您必须返回CAPsMAN设备以授予此证书的密钥。

在CAP菜单中设置刚刚创建的证书:

```
/interface wireless cap
set certificate=CAP1

```

**CAPsMAN设备:**

返回到CAPsMAN设备，在 _Certificate Request_ 菜单中授予CAP证书密钥:

```
/certificate scep-server requests
grant numbers=0

```

**结果**

现在CAP应该能够连接到CAPsMAN，如果连接，请参阅 _CAPsMAN接口_ 。在CAPsMAN device  _Certificate_ 菜单中可以看到三个证书:CA、CAPsMAN和颁发给CAP的证书:

```shell
[admin@CAPsMAN] /certificate print 
Flags: K - private-key, D - dsa, L - crl, C - smart-card-key, A - authority, I - issued, R - revoked, 
E - expired, T - trusted 
 #          NAME        COMMON-NAME      SUBJECT-ALT-NAME                                   FINGERPRINT     
 0 K L A  T CA          CA                                                                  752775b457a37...
 1 K   A    CAPsMAN     CAPsMAN                                                             12911ba445b3b...
 2      I   issued_1    CAP1                                                                5b9a52b6ce3fb...

```

在CAP devices _Certificate_ 菜单中可以看到两个获得的证书:

```shell
[admin@CAP1] /interface wireless> /certificate print 
Flags: K - private-key, D - dsa, L - crl, C - smart-card-key, A - authority, I - issued, R - revoked, 
E - expired, T - trusted 
 #          NAME        COMMON-NAME      SUBJECT-ALT-NAME                                   FINGERPRINT     
 0   L A  T cert_exp... CA                                                                  752775b457a37...
 1 K      T CAP1        CAP1                                                                5b9a52b6ce3fb...
```