# 介绍

频谱扫描可以扫描无线网卡支持的所有频率，并直接在控制台中绘制它们。确切的频率范围取决于卡片。r52n上允许的范围:[4790;6085]、[2182;2549]。

无线网卡可以为任何20mhz宽信道生成4us长的频谱快照。这被认为是一个单一的光谱样本。

为了提高数据质量，频谱以10mhz的频率增量扫描，这意味着在每个特定频率下(考虑20mhz宽的样本)的采样覆盖率增加了一倍。

目前，不支持Atheros 802.11ac芯片(例如QCA98xx, IPQ-4018)。请参阅 [https://mikrotik.com/products](https://mikrotik.com/products) 确定您设备上的无线芯片。

# 控制台

## 光谱历史

![](https://help.mikrotik.com/docs/download/attachments/139526162/Spectral-history.png?version=1&modificationDate=1658911224048&api=v2)

`/interface wireless spectral-history <wireless interface name>`

  

阴谋声谱图。图例和频率标尺每24行印一次。标尺中的数字对应于其最左边字符位置的值。在不同范围内的功率值被打印为具有相同前景和背景颜色的不同颜色的字符，因此可以复制和粘贴该命令的终端输出。

- _value_ - 选择绘制在输出上的值。“interference”是特殊的，因为它显示检测到的干扰源(受“classiy -samples”参数的影响)而不是功率读数，并且不能使声音;
- _interval_ - 打印谱线的时间间隔;
- _duration_ - 在指定时间后终止命令。违约是无限期的;
- _buckets_ - 在谱图的每一行显示多少个值。该值受终端中列数的限制。如果使用“audible”，减少这个值是有用的;
- _average-samples_ - 在每个频率上拍摄的4us光谱快照的数量，并计算它们的平均和最大能量。(默认10);
- _classify-samples_ - 在每个频率下拍摄并经过干扰分类算法处理的光谱快照个数。一般来说，越多的样本越有机会发现某些类型的干扰(默认为50);
- _range_
  - 2.4ghz - 扫描整个2.4ghz频段;
  - 5ghz - 扫描整个5ghz频段;
  - 电流通道 - 仅扫描电流通道(20或40 MHz宽);
  - range - 扫描的特定范围;

- _audible=yes_ -播放打印出来的每一行。字里行间有短暂的沉默。每条线从左到右播放，频率越高，谱图中的值越高。

## 光谱扫描

![](https://help.mikrotik.com/docs/download/attachments/139526162/Spectral-scan.png?version=1&modificationDate=1658911497641&api=v2)

`/interface wireless spectral-scan <wireless interface name>`

连续监测光谱数据。该命令使用与'spectral-history'相同的数据源，因此共享许多参数。

每一行显示一个谱图桶——频率、功率平均值的数值和字符图形条。柱状图显示平均功率值，字符为“:”，平均峰值保持率为“”。的字符。Maximum显示为单个浮动':'字符。

- _show-interference_ - 增加一列显示检测到的干扰源;

可能分类干扰的类型:

-   Bluetooth-headset
-   Bluetooth-stereo
-   cordless-phone
-   microwave-oven
-   CWA
-   video-bridge
-   wifi

# Dude

Dude是一个免费的网络监控和管理程序，由MikroTik。你可以在这里 [下载](http://www.mikrotik.com/thedude.php)。

Dude具有内置功能，可以通过支持的无线网卡从任何RouterOS设备运行图形化频谱扫描。只需在您的Dude地图中选择此设备，右键单击并选择工具->光谱扫描。

![](https://help.mikrotik.com/docs/download/attachments/139526162/Spectral1.png?version=1&modificationDate=1658911632889&api=v2)

这将打开具有各种选项和不同视图模式的光谱扫描GUI:

![](https://help.mikrotik.com/docs/download/attachments/139526162/Spectral-scan-dude.png?version=1&modificationDate=1658911642856&api=v2)