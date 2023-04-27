## 说明

Flashfig是一个用于大规模配置路由器的应用程序。它可以被MikroTik分销商、ISP或任何其他需要在最短的时间内将RouterOS配置应用于许多路由器的公司使用。

Flashfig在3秒内将MikroTik RouterOS的配置应用于任何RouterBOARD。你可以在一批路由器上执行Flashfig，唯一需要的是 **连接** RouterBOARD到一个运行Netinstall的二层网络，并给启用Flashfig的RouterBOARD供电。

在Flashfig模式下运行Netinstall只能在Windows电脑上运行，Netinstall可以从[下载](http://www.mikrotik.com/download)页面获得。

所有 [RouterBOARDs](http://www.routerboard.com/)都支持Flashfig模式。在运行Netinstall并启用Flasfig模式的Windows电脑和同一广播域中的RouterBOARD之间工作（需要直接的第二层以太网连接）。

自2010年3月以来，每台新生产的RouterBOARD在出厂时都默认启用了Flashfig支持。对于旧型号，Flashfig可以通过RouterBOOT或从MikroTik RouterOS控制台启用（例如，/system routerboard settings set boot-device=flash-boot-once-then-nand或/system routerboard settings set boot-device=flash-boot）。

当Flashfig在一个全新的RouterBOARD上使用一次后，它将在以后的启动中被禁用，以避免在以后的时间里进行不必要的重新配置。要在同一台路由器上第二次使用Flashfig，你需要在Bootloader设置中启用 **flash-boot**。

如果以后使用 RouterOS _reset-configuration_ 命令，Flashfig 配置会被加载。(要永久覆盖，请使用Netinstall程序并检查应用默认配置或在基于Linux的命令行中使用-r标志)。

Flashfig图显示了Flashfig的程序

![](https://help.mikrotik.com/docs/download/attachments/139526145/Flashfigdiagramm.png?version=1&modificationDate=1658906901697&api=v2)

## Flashfig实例

这个例子说明如何使用Flashfig程序将所选择的MikroTik RouterOS配置应用于 "出厂时 "的RouterBOARD。

### 介绍

Flashfig是Netinstall程序中的一个选项，在最新的ROS版本中，Flashfig从Netinstall中移除，可以作为一个独立的应用程序从 [https://mikrotik.com/download](https://mikrotik.com/download)下载。

![](https://help.mikrotik.com/docs/download/attachments/139526145/Flashfig.png?version=1&modificationDate=1658907016942&api=v2)

### 要求

Windows计算机必须配备以下端口并包含以下文件：

- 一个工作的以太网端口；
- 有效的.rsc文件，其中有类似于出口/进口文件的MikroTik RouterOS配置。(注意文本编辑器对CR/LF字符的处理，在通过Flashfig应用之前，测试配置在正常应用于相同版本的RouterOS时没有错误，因为运行时的错误是不可见的！）；
- 始终使用最新的NetInstall/Flashfig程序，可从 [下载](http://www.mikrotik.com/download.html) 页面获得；

RouterBOARD：

- Flashfig是由RouterBOARD的首次启动支持的；

### 预配置

#### Windows电脑

- 运行Flashfig；
- 准备 **.rsc** 文件，**.rsc** 文件是常规/导入文件，它接受有效的MikroTik RouterOS CLI命令。你可以用任何文本编辑器程序（Notepad、Notepad++、Texteditor、TextEdit、Microsoft Word、OpenOffice Writer）创建.rsc文件。

![](https://help.mikrotik.com/docs/download/attachments/139526145/Flashfig2.png?version=1&modificationDate=1658907059195&api=v2)

- 指定 **启动客户端地址**，这是一个与计算机以太网接口上配置的地址在同一子网内的地址

![](https://help.mikrotik.com/docs/download/attachments/139526145/Flashfig3.png?version=1&modificationDate=1658907107861&api=v2)

- **浏览.rsc** MikroTik RouterOS配置文件应用于RouterBOARD，突出显示该文件并 **选择** 

![](https://help.mikrotik.com/docs/download/attachments/139526145/Flashfig4.png?version=1&modificationDate=1658907118530&api=v2)

- 激活Flashfig服务器，现在它已经准备好Flashfig了。注意，任何RouterBOARD在网络中都会被flashfig，在启动设备配置为 **flash-boot** 或 **flash-boot-once-then-nand** 的情况下打开

![](https://help.mikrotik.com/docs/download/attachments/139526145/Flashfig5.png?version=1&modificationDate=1658907127709&api=v2)

#### RouterBOARD

- 每个RouterBOARD出厂时都默认启用了Flashfig模式，这意味着不需要对RouterBOARD进行配置。

- 如果你的路由器没有启用Flashfig，请用Winbox/Console访问RouterBOARD并设置配置

```shell
system/routerboard/settings/set boot-device=flash-boot
```

或者使用一个更可取的选项

```shell
system/routerboard/settings/set boot-device=flash-boot-once-then-nand
```

路由器现在已经准备好使用Flashfig了。

#### 连接

将RouterBOARD的Ether1和Flashfig电脑连接到同一个局域网。(例外情况是RB1xxx和CCR设备，它们支持从最后一个以太网端口进行网络启动）。

#### 运行Flashfig

- 为RouterBOARD插上电源
- 检查Flashfig程序的状态

![](https://help.mikrotik.com/docs/download/attachments/139526145/Flashfig6.png?version=1&modificationDate=1658907156898&api=v2)

信息日志显示 "Flashfigged"，RouterBOARD应反复发出"/"（"_..._."字符的摩尔斯码声音，并闪烁LED - 现在可以安全地拔掉路由器的插头/电源。

- Flashfig **配置** 应用到RouterBOARD上，准备好在生产中使用这个新配置。

## 故障排除

### Flashfig配置未被应用

如果所有程序都成功了，但是.rsc文件中的RouterOS配置没有应用。将:delay 20s添加到*.rsc配置文件中。原因可能是，配置脚本在RouterOS启动成功之前就被执行了。

### Flashfig找不到路由器，没有应用。

确保运行Flashfig的计算机上只有一个网络接口处于活动状态。

### 闪存空间不足，忽略

Flashfig配置最大文件大小不超过4000字节，否则程序将返回上述错误。