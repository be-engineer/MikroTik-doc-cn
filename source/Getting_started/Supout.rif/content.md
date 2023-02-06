# 什么是supout.rif文件?

支持文件用于调试 MikroTik RouterOS 并更快地解决支持问题。 MikroTik Router的所有信息都保存在一个二进制文件中，该文件保存在路由器中，可以使用FTP从路由器上下载。 如果需要，你还可以在具有闪存类型内存或外部存储驱动器的设备上的“/flash”文件夹中生成文件，方法是指定文件“name=flash/supout.rif”的完整路径。 你可以在你的 [Mikrotik 帐户](https://www.mikrotik.com/) 中查看此文件的内容，只需单击左侧栏中的“Supout.rif 查看器”并上传文件。

此文件包含你的所有路由器配置、日志和一些其他详细信息，可帮助 MikroTik 支持人员解决你的问题。 该文件不包含敏感信息或路由器密码。

## 创建支持输出文件

### Winbox

要在 Winbox 中生成此文件，请单击“Make Supout.rif”。

要将文件保存到你的计算机，请用鼠标右键单击文件并选择“Download”获取文件，或者只需将文件拖到桌面即可。

![](https://help.mikrotik.com/docs/download/attachments/328106/download.PNG?version=1&modificationDate=1570622754782&api=v2)

### Webfig

要在 Webfig 中生成此文件，请单击“制作 Supout.rif”，然后单击“Download”下载到你的计算机。

![](https://help.mikrotik.com/docs/download/attachments/328106/makesupout.PNG?version=1&modificationDate=1570622561004&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/328106/webfig.PNG?version=1&modificationDate=1570622962040&api=v2)

### 控制台

要生成此文件，请在命令行中键入：

`/system sup-out put name =supout.rif`
