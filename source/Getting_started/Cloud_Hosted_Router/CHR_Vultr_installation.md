## CHR Vultr 安装

Vultr 拥有超过 [20 个数据中心位置](https://www.vultr.com/features/datacenter-locations/)，你可以选择部署 MikroTik CHR 以获得最佳[速率和延迟](https:// nj-us-ping.vultr.com/）。
按照以下步骤在 Vultr 上安装 MikroTik CHR。

## 第一步：在救援模式下部署服务器

在此步骤中，用 SystemRescue（一个可启动的 Linux ISO）在 Vultr 上部署一个新服务器。

1. [部署](https://my.vultr.com/deploy/) 一个新的[云计算](https://www.vultr.com/products/cloud-compute/)实例。
2. 根据你的需要选择性能最佳的位置。 你可以使用 Vultr 的 [network-looking glass](https://nj-us-ping.vultr.com/) 来测试任何位置的速率和延迟。
3. 在 **Server Image** 中选择 **ISO Library** 选项卡。
4. 选择 **SystemRescue x64**。
5. 根据要求选择具有[足够带宽限额](https://www.vultr.com/resources/faq/?query=bandwidth#bandwidthcalculation) 的服务器。
6. 给服务器一个主机名和标签，然后单击**立即部署**。

服务器完成部署后，继续下一步。

## 第二步：将CHR映像写入磁盘

1. 在网络浏览器中，导航至 [MikroTik 下载页面](https://mikrotik.com/download)。
2. 找到最新的 Stable RAW CHR 磁盘映像。 Vultr 需要版本 **7.2.3 Stable** 或更高版本。
3. 右击软盘图标复制网址。 现在不要下载映像，在稍后的步骤中下载到服务器。

    ![](https://help.mikrotik.com/docs/download/attachments/146997259/DownloadCHR.png?version=1&modificationDate=1662979208247&api=v2)
4. 导航至 [Vultr 客户门户](https://my.vultr.com/) 中的服务器信息页面。
5. 连接到 [网络控制台](https://www.vultr.com/docs/vultr-web-console-faq/)。
    ![](https://help.mikrotik.com/docs/download/attachments/146997259/ViewConsole.png?version=1&modificationDate=1662979233108&api=v2)
6. 在 Web 控制台中，使用 wget 将 CHR 映像下载到服务器。 如果你把下载 URL 复制到剪贴板，则可以用 Web 控制台 [发送到服务器](https://www.vultr.com/docs/vultr-web-console-faq/)。

    在以下示例中用你的版本替换 x.x.x。

    `# wget https://download.mikrotik.com/routeros/x.x.x/chr-x.x.x.img.zip`

7. 解压缩下载的文件。

    `# unzip chr-x.x.x.img.zip`

8. 使用dd 将MikroTik CHR 映像写入服务器的磁盘。

    `# dd if=chr-x.x.x.img of=/dev/vda`

     - **if** 是你在上一步中解压缩的映像。
     - **of** 是服务器的磁盘：/dev/vda。

这个过程需要几分钟； 完成后继续下一步。

## 第三步：连接到 MikroTik CHR

1. 导航至服务器的 [设置页面](https://my.vultr.com/)。
2. 选择 **Custom ISO** 菜单，然后单击 **Remove ISO**。 服务器会重新启动。
3. 连接到 [网络控制台](https://www.vultr.com/docs/vultr-web-console-faq/)。
4. 以管理员身份登录。 因为没有设置密码，所以出现提示时按 **Enter**。
5. 查看软件许可证，然后选择一个新的强密码。
6. 关闭 web 控制台，然后在本地计算机上打开一个终端。
7. 以管理员身份通过 SSH 访问服务器的 IP 地址。
8. 输入上一步设置的强密码。

这样就完成了基本安装。 请 [保护你的 MicroTik CHR 路由器](https://wiki.mikrotik.com/wiki/Manual:Securing_Your_Router)  并查阅 [文档](https://help.mikrotik.com/docs/display/ROS/Getting+started) 来配置服务器以供生产使用。
