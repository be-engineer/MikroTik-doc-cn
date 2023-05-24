## Summary


This example shows how to configure transparent wireless bridge in CLI from one W60G device to another.

Example is done from empty configuration state with [[WinBox](https://mikrotik.com/download) utility

## Connect to the device step by step



1.  After configuration reset - only mac-telnet is possible.  
    Connect to device by connecting to it's MAC address or use WinBox New terminal to find device MAC address of the W60G device by issuing command:
    
    | 
    ```
    /ip neighbor print
    ```
    
    |     |
    | --- |
    |     |
    
    ```
    /ip neighbor print
    ```
    
    |     |
    | --- |
    
2.  To connect to the W60G device issue a command:
    
    | 
    ```
    /tool mac-telnet mac-address
    ```
    
    |     |
    | --- |
    |     |
    
    ```
    /tool mac-telnet mac-address
    ```
    
    |     |
    | --- |
    
3.  Enter username and password. By default username is **admin** and no password is set
    
    | 
    ```
    [admin@KD_GW] > /tool mac-telnet C4:AD:34:84:EE:5DLogin: adminPassword: Trying C4:AD:34:84:EE:5D...Connected to C4:AD:34:84:EE:5D
    ```
    
    |     |
    | --- |
    |     |
    
    ```
    [admin@KD_GW] > /tool mac-telnet C4:AD:34:84:EE:5DLogin: adminPassword: Trying C4:AD:34:84:EE:5D...Connected to C4:AD:34:84:EE:5D
    ```
    
    |     |
    | --- |
    

## Configure bridge

___

1.  Add new bridge and assign bridge members to it by issuing the following command:
    
    | 
    ```
    /interface bridge add name=bridge
    ```
    
    |     |
    | --- |
    |     |
    
    ```
    /interface bridge add name=bridge
    ```
    
    |     |
    | --- |
    
    To check if the bridge has been created issue a command:
    
    | 
    ```
    [admin@MikroTik] > /interface bridge printFlags: X - disabled, R - running 0 R name="bridge" mtu=auto actual-mtu=1500 l2mtu=65535 arp=enabled arp-timeout=auto mac-address=1A:7F:BB:41:B0:94 protocol-mode=rstp fast-forward=yes igmp-snooping=no auto-mac=yes ageing-time=5m priority=0x8000 max-message-age=20s forward-delay=15s transmit-hold-count=6 vlan-filtering=no dhcp-snooping=no 
    ```
    
    |     |
    | --- |
    |     |
    
    ```
    [admin@MikroTik] > /interface bridge printFlags: X - disabled, R - running 0 R name="bridge" mtu=auto actual-mtu=1500 l2mtu=65535 arp=enabled arp-timeout=auto mac-address=1A:7F:BB:41:B0:94 protocol-mode=rstp fast-forward=yes igmp-snooping=no auto-mac=yes ageing-time=5m priority=0x8000 max-message-age=20s forward-delay=15s transmit-hold-count=6 vlan-filtering=no dhcp-snooping=no 
    ```
    
    |     |
    | --- |
    
2.  Add interface members (ether1 and wlan60-1) to newly created bridge. 
    
    | 
    ```
    [admin@MikroTik] > /interface bridge port add interface=ether1 bridge=bridge [admin@MikroTik] > /interface bridge port add interface=wlan60-1 bridge=bridge [admin@MikroTik] > /interface bridge port printFlags: X - disabled, I - inactive, D - dynamic, H - hw-offload  #     INTERFACE                              BRIDGE                              HW   PVID PRIORITY  PATH-COST INTERNAL-PATH-COST    HORIZON 0     ether1                                 bridge                             yes     1     0x80         10                 10       none 1 I   wlan60-1                               bridge                                     1     0x80         10                 10       none
    ```
    
    |     |
    | --- |
    |     |
    
    ```
    [admin@MikroTik] > /interface bridge port add interface=ether1 bridge=bridge [admin@MikroTik] > /interface bridge port add interface=wlan60-1 bridge=bridge [admin@MikroTik] > /interface bridge port printFlags: X - disabled, I - inactive, D - dynamic, H - hw-offload  #     INTERFACE                              BRIDGE                              HW   PVID PRIORITY  PATH-COST INTERNAL-PATH-COST    HORIZON 0     ether1                                 bridge                             yes     1     0x80         10                 10       none 1 I   wlan60-1                               bridge                                     1     0x80         10                 10       none
    ```
    
    |     |
    | --- |
    

## Set up wireless connection

___

All previously explained steps are identical to Bridge and Station devices. When configuring wireless interface different modes needs to be used.  
  
**_For bridge device -_**

-   Choose SSID, Password, frequency and choose bridge mode option that will act as a **bridge** for the setup, please see the example.
-   Enable W60G interface after required parameters have been set.
    
    | 
    ```
    [admin@MikroTik] > interface w60g set wlan60-1 mode=bridge frequency=auto ssid=MySSID password=choosepassword put-stations-in-bridge=bridge isolate-stations=yes  [admin@MikroTik] > interface w60g printFlags: X - disabled, R - running 0 X name="wlan60-1" mtu=1500 l2mtu=1600 mac-address=C4:AD:34:84:EE:5E arp=enabled arp-timeout=auto region=no-region-set mode=bridge ssid="MySSID" frequency=auto default-scan-list=58320,60480,62640,64800 password="choosepassword" tx-sector=auto put-stations-in-bridge=bridge isolate-stations=yes[admin@MikroTik] > interface w60g enable wlan60-1
    ```
    
    |     |
    | --- |
    |     |
    
    ```
    [admin@MikroTik] > interface w60g set wlan60-1 mode=bridge frequency=auto ssid=MySSID password=choosepassword put-stations-in-bridge=bridge isolate-stations=yes  [admin@MikroTik] > interface w60g printFlags: X - disabled, R - running 0 X name="wlan60-1" mtu=1500 l2mtu=1600 mac-address=C4:AD:34:84:EE:5E arp=enabled arp-timeout=auto region=no-region-set mode=bridge ssid="MySSID" frequency=auto default-scan-list=58320,60480,62640,64800 password="choosepassword" tx-sector=auto put-stations-in-bridge=bridge isolate-stations=yes[admin@MikroTik] > interface w60g enable wlan60-1
    ```
    
    |     |
    | --- |
    

_**For Station device -**_

-   Choose the same SSID, Password, frequency as the bridge device and choose station-bridge mode option that will act as a **station** for the setup, please see the example.
-   Enable W60G interface after required parameters have been set.
    
    | 
    ```
    [admin@MikroTik] > interface w60g set wlan60-1 mode=station-bridge frequency=auto ssid=MySSID password=choosepassword                              [admin@MikroTik] > interface w60g printFlags: X - disabled, R - running 0 X name="wlan60-1" mtu=1500 l2mtu=1600 mac-address=C4:AD:34:84:EE:5E arp=enabled arp-timeout=auto region=no-region-set mode=station-bridge ssid="MySSID" frequency=auto default-scan-list=58320,60480,62640,64800 password="choosepassword" tx-sector=auto put-stations-in-bridge=bridge isolate-stations=yes[admin@MikroTik] > /interface w60g enable wlan60-1
    ```
    
    |     |
    | --- |
    |     |
    
    ```
    [admin@MikroTik] > interface w60g set wlan60-1 mode=station-bridge frequency=auto ssid=MySSID password=choosepassword                              [admin@MikroTik] > interface w60g printFlags: X - disabled, R - running 0 X name="wlan60-1" mtu=1500 l2mtu=1600 mac-address=C4:AD:34:84:EE:5E arp=enabled arp-timeout=auto region=no-region-set mode=station-bridge ssid="MySSID" frequency=auto default-scan-list=58320,60480,62640,64800 password="choosepassword" tx-sector=auto put-stations-in-bridge=bridge isolate-stations=yes[admin@MikroTik] > /interface w60g enable wlan60-1
    ```
    
    |     |
    | --- |
    

## Additional configuration

___

Link should be established after all previously explained steps are done. It's recommended to set up administrators password on both devices.

##   
Troubleshooting

___

Ensure connection is established to the correct device by checking the device settings like serial number and model name by issuing a command:

| 
```
[admin@MikroTik] > /system routerboard print
```

|     |
| --- |
|     |

```
[admin@MikroTik] > /system routerboard print
```

|     |
| --- |

  
If bridge wlan60-1 interface in bridge settings is inactive and configuration is done properly  to enable the interface on a device - issue a command:

| 
```
[admin@MikroTik] > /interface w60g enable wlan60-1
```

|     |
| --- |
|     |

```
[admin@MikroTik] > /interface w60g enable wlan60-1
```

|     |
| --- |