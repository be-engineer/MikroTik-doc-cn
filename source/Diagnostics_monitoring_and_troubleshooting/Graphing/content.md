图形化是一种工具，用于监测不同时间的RouterOS参数，并将收集到的数据放在图表中。 
可观看 [关于此功能的视频](https://youtu.be/FTQEnDZVHNc)。

图表工具可以显示以下内容。

- Routerboard的健康状况（电压和温度）
- 资源使用情况（CPU、内存和磁盘使用情况）
- 通过接口传输的流量
- 通过简单队列传输的流量

图表由两部分组成 - 第一部分收集信息，另一部分在网页上显示数据。要访问图表，请输入https://[Router_IP_address]/graphs/，在Web浏览器中选择一个图表显示。

内存图表的例子。

![](https://help.mikrotik.com/docs/download/attachments/22773810/Graphing-mem.png?version=2&modificationDate=1585904641333&api=v2)

## 配置

配置在"/tool graphing "菜单下完成，默认是禁用的。可以在各自的子菜单中配置接口、资源和简单队列的图表。

 如果简单队列的目标地址被设置为0.0.0.0/0，即使允许地址设置为特定地址，每个人也都能访问队列图表。这是因为默认情况下，队列图表也可以从目标地址访问。

## 在WinBox中的图表

Winbox允许查看与网页上相同的信息。打开 **Tools->Graphing** 窗口。双击想看图表的条目。

下面的图片显示了WinBox的内存使用图表。

![](https://help.mikrotik.com/docs/download/attachments/22773810/Graphing-mem-winbox.png?version=1&modificationDate=1585904657607&api=v2)