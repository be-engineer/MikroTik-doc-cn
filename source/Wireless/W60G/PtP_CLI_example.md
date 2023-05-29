# CLI下结合60Ghz设备配置5Ghz链路自动故障切换概述


本示例介绍了如何在CLI下结合60Ghz设备配置5Ghz链路自动故障切换(bonding)。
当60Ghz无线之间的连接丢失时，它会自动使用绑定接口。
示例是通过 [WinBox](https://mikrotik.com/download) 实用程序从空配置状态完成的

## 逐步连接设备

1.  配置复位后，只允许mac-telnet。
    通过连接设备的MAC地址连接设备，或者使用WinBox New终端通过发出命令查找W60G设备的设备MAC地址:
    
    
    ```
    /ip neighbor print
    ```
    
2.  要连接到W60G设备，用命令:
   

    ```
    /tool mac-telnet mac-address
    ```

    
3.  输入用户名和密码。默认用户名为admin，密码为空白或打印在设备贴纸上。
    

    ```
    [admin@KD_GW] > /tool mac-telnet C4:AD:34:84:EE:5DLogin: adminPassword: Trying C4:AD:34:84:EE:5D...Connected to C4:AD:34:84:EE:5D
    ```
   

## 配置网桥



1.  通过以下命令添加新桥并为其分配桥成员:
    

    ```
    /interface bridge add name=bridge
    ```
   
    要检查网桥是否已创建，用命令:
    
    
    ```shell
    [admin@MikroTik] > /interface bridge print
    Flags: X - disabled, R - running 0 R name="bridge" mtu=auto actual-mtu=1500 l2mtu=65535 arp=enabled arp-timeout=auto mac-address=1A:7F:BB:41:B0:94 protocol-mode=rstp fast-forward=yes igmp-snooping=no auto-mac=yes ageing-time=5m priority=0x8000 max-message-age=20s forward-delay=15s transmit-hold-count=6 vlan-filtering=no dhcp-snooping=no 
    ```
  

## 设置60Ghz无线连接



所有前面解释的步骤与桥和站设备相同。在配置无线接口时，需要使用不同的模式。

**用于桥接设备**

- 选择SSID，密码，频率，并选择桥接模式选项，将作为一个桥接设置，请参阅示例。
- 参数设置完成后，使能W60G接口。
    
    ```shell
    [admin@MikroTik] > /interface w60g set wlan60-1 mode=bridge frequency=auto ssid=MySSID password=choosepassword isolate-stations=yes
    [admin@MikroTik] > /interface w60g print
    Flags: X - disabled, R - running 0 X name="wlan60-1" mtu=1500 l2mtu=1600 mac-address=C4:AD:34:84:EE:5E arp=enabled arp-timeout=auto region=no-region-set mode=bridge ssid="MySSID" frequency=auto default-scan-list=58320,60480,62640,64800 password="choosepassword" tx-sector=auto put-stations-in-bridge=bridge isolate-stations=yes
    [admin@MikroTik] > /interface w60g enable wlan60-1
    ```

    

**适用于工作站设备**

- 选择与桥接设备相同的SSID，密码，频率，并选择站-桥接模式选项，将作为设置的站，请参见示例。
- 参数设置完成后，使能W60G接口。
    
    
    ```shell
    [admin@MikroTik] > /interface w60g set wlan60-1 mode=station-bridge frequency=auto ssid=MySSID password=choosepassword                           
    [admin@MikroTik] > /interface w60g print
    Flags: X - disabled, R - running 0 X name="wlan60-1" mtu=1500 l2mtu=1600 mac-address=C4:AD:34:84:EE:5E arp=enabled arp-timeout=auto region=no-region-set mode=station-bridge ssid="MySSID"frequency=auto default-scan-list=58320,60480,62640,64800password="choosepassword" tx-sector=auto put-stations-in-bridge=bridge isolate-stations=yes
    [admin@MikroTik] > /interface w60g enable wlan60-1
    ```
    

## 设置5Ghz无线连接



**用于桥接设备**

- 选择SSID，密码，频率，并选择桥接模式选项，将作为一个桥接设置，请参阅示例。
- 参数设置完成后，开启5Ghz接口。
    
    
    ```shell
    [admin@MikroTik] > /interface wireless security-profiles set [ find default=yes ] supplicant-identity=MikroTik authentication-types=wpa2-psk mode=dynamic-keys wpa2-pre-shared-key=choosepassword
    [admin@MikroTik] > /interface wireless set wlan1 frequency=auto scan-list=default installation=outdoor mode=bridge ssid=MikroTik1 channel-width=20/40/80mhz-Ceee wireless-protocol=any security-profile=default band=5ghz-a/n/ac 
    [admin@MikroTik] > /interface wireless enable wlan1
    ```
    

**适用于工作站设备**

- 选择与桥接设备相同的SSID，密码，频率，并选择站-桥接模式选项，将作为设置的**站**，请参见示例。
- 参数设置完成后，使能W60G接口。
    
    
    ```shell
    [admin@MikroTik] > /interface wireless security-profiles set [ find default=yes ] supplicant-identity=MikroTik authentication-types=wpa2-psk mode=dynamic-keys wpa2-pre-shared-key=choosepassword
    [admin@MikroTik] > /interface wireless set wlan1 frequency=auto scan-list=default installation=outdoor mode=station-bridge ssid=MikroTik1 channel-width=20/40/80mhz-Ceee wireless-protocol=any security-profile=default band=5ghz-a/n/ac
    [admin@MikroTik] > /interface wireless enable wlan1
    ```
    

## 配置桥接和绑定



1.  在此设置中配置绑定并分配从接口，它被选择为内置的wlan1接口，但在其他类型的设置中也可以是以太网接口。

    对于桥接装置，请将bonding设置为:

    ```shell
    [admin@MikroTik] > /interface bonding add comment=bondingbackup mode=active-backup name=bond1 primary=wlan60-station-1 slaves=wlan60-station-1,wlan1
    ```

    
对于站桥设备，请将bonding设置为:
    

    ```shell
    [admin@MikroTik] > /interface bonding add comment=defconf mode=active-backup name=bond1 primary=wlan60-1 slaves=wlan60-1,wlan1
    ```

    
2.  Add interface members (ether1 and bond1) to newly created bridge. 
    
    
    ```shell
    [admin@MikroTik] > /interface bridge port add interface=ether1 bridge=bridge 
    [admin@MikroTik] > /interface bridge port add interface=bond1  bridge=bridge 
    [admin@MikroTik] > /interface bridge port printFlags: X - disabled, I - inactive, D - dynamic, H - hw-offload  
    #     INTERFACE                              BRIDGE                              HW   PVID PRIORITY  PATH-COST INTERNAL-PATH-COST    HORIZON 0     ether1                                 bridge                             yes     1     0x80         10                 10       none 1     bond1                                  bridge                             yes     1     0x80         10                 10       none
    ```

    

## 附加配置



在完成前面解释的所有步骤后，应该建立链接。建议在两台设备上都设置管理员密码。

## 故障排除



通过命令检查序列号、型号等设备设置，确保与正确的设备建立连接:


```
[admin@MikroTik] > /system routerboard print
```

如果网桥wlan60-1接口在网桥设置中是不活动的，并且配置正确，用命令使能设备上的接口:


```
[admin@MikroTik] > /interface w60g enable wlan60-1
```
