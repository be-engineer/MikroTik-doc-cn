-   1 [Installing the root CA](https://help.mikrotik.com/docs/display/ROS/IKEv2+EAP+between+NordVPN+and+RouterOS#IKEv2EAPbetweenNordVPNandRouterOS-InstallingtherootCA)
-   2 [Finding out the server's hostname](https://help.mikrotik.com/docs/display/ROS/IKEv2+EAP+between+NordVPN+and+RouterOS#IKEv2EAPbetweenNordVPNandRouterOS-Findingouttheserver'shostname)
-   3 [Setting up the IPsec tunnel](https://help.mikrotik.com/docs/display/ROS/IKEv2+EAP+between+NordVPN+and+RouterOS#IKEv2EAPbetweenNordVPNandRouterOS-SettinguptheIPsectunnel)
-   4 [Choosing what to send over the tunnel](https://help.mikrotik.com/docs/display/ROS/IKEv2+EAP+between+NordVPN+and+RouterOS#IKEv2EAPbetweenNordVPNandRouterOS-Choosingwhattosendoverthetunnel)
    -   4.1 [Option 1: Sending all traffic over the tunnel](https://help.mikrotik.com/docs/display/ROS/IKEv2+EAP+between+NordVPN+and+RouterOS#IKEv2EAPbetweenNordVPNandRouterOS-Option1:Sendingalltrafficoverthetunnel)
    -   4.2 [Option 2: Accessing certain addresses over the tunnel](https://help.mikrotik.com/docs/display/ROS/IKEv2+EAP+between+NordVPN+and+RouterOS#IKEv2EAPbetweenNordVPNandRouterOS-Option2:Accessingcertainaddressesoverthetunnel)

从RouterOS v6.45开始，可以通过EAP认证方式建立到NordVPN服务器的IKEv2安全隧道。本手册介绍了如何配置它。

![](https://help.mikrotik.com/docs/download/attachments/125992982/IPsec.png?version=1&modificationDate=1652681600039&api=v2)

## 安装根CA

首先下载并导入NordVPN根CA证书。

```
/tool fetch url="https://downloads.nordvpn.com/certificates/root.der"
/certificate import file-name=root.der

```

在System/Certificates菜单中现在应该有受信任的NordVPN根CA证书。

```shell
[admin@MikroTik] > /certificate print where name~"root.der"
Flags: K - private-key, L - crl, C - smart-card-key, A - authority, I - issued, R - revoked, E - expired, T - trusted 
 #         NAME            COMMON-NAME            SUBJECT-ALT-NAME                                         FINGERPRINT           
 0       T root.der_0      NordVPN Root CA                                                                 8b5a495db498a6c2c8c...

```

## 服务器的主机名

导航到 [https://nordvpn.com/servers/tools/](https://nordvpn.com/servers/tools/) 并找出推荐的服务器的主机名。在本例中是 [lv20.nordvpn.com](http://lv20.nordvpn.com)。

![](https://help.mikrotik.com/docs/download/attachments/125992982/Nordvpn_hostname.png?version=1&modificationDate=1652439438089&api=v2)

## 建立IPsec隧道

建议将第一阶段安全框架和第二阶段安全提议的配置单独创建，以免影响现有或未来的IPsec配置。

```shell
/ip ipsec profile
add name=NordVPN
/ip ipsec proposal
add name=NordVPN pfs-group=none

```

虽然可以使用默认策略模板生成策略，但最好创建一个新的策略组和模板，将此配置与任何其他IPsec配置分开。

```shell
/ip ipsec policy group
add name=NordVPN
/ip ipsec policy
add dst-address=0.0.0.0/0 group=NordVPN proposal=NordVPN src-address=0.0.0.0/0 template=yes

```

创建一个带有responder=no的新模式配置项，它将从服务器请求配置参数。

```shell
/ip ipsec mode-config
add name=NordVPN responder=no

```

最后，创建对等体和身份配置。在用户名和密码参数中指定NordVPN凭据。

```shell
/ip ipsec peer
add address=lv20.nordvpn.com exchange-mode=ike2 name=NordVPN profile=NordVPN
/ip ipsec identity
add auth-method=eap certificate="" eap-methods=eap-mschapv2 generate-policy=port-strict mode-config=NordVPN peer=NordVPN policy-template-group=NordVPN username=support@mikrotik.com password=secret

```

验证连接是否成功建立。

```
/ip ipsec
active-peers print
installed-sa print

```

## 选择通过隧道发送的内容

如果查看生成的动态策略，会看到只有具有特定(由模式配置接收)源地址的流量才会通过隧道发送。但在大多数情况下，路由器需要通过隧道路由特定的设备或网络。在这种情况下，可以使用源NAT修改报文的源地址，使其与mode配置地址匹配。由于mode配置地址是动态的，所以不能创建静态源NAT规则。在RouterOS中，可以为配置模式的客户端生成动态源NAT规则。

### 选项1:通过隧道发送所有流量

在本例中，在路由器后面有一个本地网络10.5.8.0/24，希望来自该网络的所有流量都通过隧道发送。首先，必须创建一个包含本地网络的新IP/Firewall/Address lis。

```
/ip firewall address-list
add address=10.5.8.0/24 list=local

```

也可以只指定单个主机，所有流量将从该主机通过隧道发送。例子:

```shell
/ip firewall address-list
add address=10.5.8.120 list=local
add address=10.5.8.23 list=local

```

完成后，可以将新创建的IP/Firewall/Address list 分配到模式配置。

```
/ip ipsec mode-config
set [ find name=NordVPN ] src-address-list=local

```

验证隧道建立时动态生成正确的源NAT规则。

```shell
[admin@MikroTik] > /ip firewall nat print 
Flags: X - disabled, I - invalid, D - dynamic 
 0  D ;;; ipsec mode-config
      chain=srcnat action=src-nat to-addresses=192.168.77.254 src-address-list=local dst-address-list=!local

```

警告

确保动态模式配置地址不是本地网络的一部分。

也可以将两个选项(1和2)结合起来，以允许只对特定的本地地址/网络访问特定的地址

### 选项2:通过隧道访问特定地址

通过使用Mangle防火墙中的connection-mark参数，也可以只在隧道上发送特定的流量。它的工作原理与选项1类似，在mode config下根据配置的连接标记参数生成动态NAT规则。

首先，在模式配置配置中设置连接标记。

```
/ip ipsec mode-config
set [ find name=NordVPN ] connection-mark=NordVPN

```

完成后，使用服务器提供的动态地址生成一个NAT规则:

```shell
[admin@MikroTik] > /ip firewall nat print 
Flags: X - disabled, I - invalid, D - dynamic 
 0  D ;;; ipsec mode-config
      chain=srcnat action=src-nat to-addresses=192.168.77.254 connection-mark=NordVPN 

```

之后，可以将此连接标记应用于使用Mangle防火墙的任何流量。在本例中，通过隧道授予对 [mikrotik.com](http://mikrotik.com) 和8.8.8.8的访问权限。

创建一个新的地址列表:

```shell
/ip firewall address-list
add address=mikrotik.com list=VPN
add address=8.8.8.8 list=VPN

```

对匹配创建的地址列表的流量应用连接标记:

```shell
/ip firewall mangle
add action=mark-connection chain=prerouting dst-address-list=VPN new-connection-mark=NordVPN passthrough=yes

```

也可以将两个选项(1和2)结合起来，以允许只对特定的本地地址/网络访问特定的地址