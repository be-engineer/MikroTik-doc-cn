# 基于架构的特性支持

所有设备都支持相同的功能，但有一些例外，如下表所示：

| 架构   | 不支持                                                       | 独家支持            |
| ------ | ------------------------------------------------------------ | ------------------- | --- |
| ARM    |                                                              | Zerotier, Container |
| ARM64  |                                                              | Zerotier, Container |
| MIPSBE | Zerotier, Dude server                                        |                     |
| MMIPS  | Zerotier                                                     |                     |     |
| SMIPS  | Zerotier, DOT1X, BGP, MPLS, PIMSM, Dude server, User manager |                     |
| TILE   | Zerotier                                                     |                     |
| PPC    | Zerotier, Dude server                                        |                     |
| X86 PC | Zerotier, Cloud                                              | Container           |
| CHR VM |                                                              |                     |

除了功能之外，根据设备的特定型号，硬件功能也存在一些差异。对于这些差异，请参阅以下文章：

- WiFi Wave2 [https://help.mikrotik.com/docs/display/ROS/WifiWave2](https://help.mikrotik.com/docs/display/ROS/WifiWave2)
- L3 Hardware offloading [https://help.mikrotik.com/docs/display/ROS/L3+Hardware+Offloading#L3HardwareOffloading-L3HWDeviceSupport](https://help.mikrotik.com/docs/display/ROS/L3+Hardware+Offloading#L3HardwareOffloading-L3HWDeviceSupport)
- PTP [https://help.mikrotik.com/docs/display/ROS/Precision+Time+Protocol](https://help.mikrotik.com/docs/display/ROS/Precision+Time+Protocol)
- Switch chip features [https://help.mikrotik.com/docs/display/ROS/Switch+Chip+Features](https://help.mikrotik.com/docs/display/ROS/Switch+Chip+Features)
