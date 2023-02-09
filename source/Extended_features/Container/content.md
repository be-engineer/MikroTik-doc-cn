# 概述

**Sub-menu:** `/container`
**Packages required:** `container`

容器是MikroTik对Linux容器的实现，允许用户在RouterOS中运行容器化环境。容器功能是在RouterOS v7.4beta4中添加的。

## 免责声明

- 要对路由器进行物理访问以启用对容器功能的支持，默认情况下是禁用的。
- 一旦容器功能被启用，容器可以被远程添加、配置、启动、停止、移除
- 如果路由器被破坏，容器可以用来在路由器和网络上轻松安装恶意软件。
- 路由器和容器中运行的任何东西一样安全。
- 如果运行容器，没有任何形式的安全保证。
- 在路由器上运行一个第三方的容器镜像，可能会打开一个安全漏洞、攻击媒介、攻击面。
- 掌握了建立漏洞的专家将能够越狱或提升到root。

## 安全风险

当安全专家发布了他的漏洞研究，任何人都可以应用这种漏洞。 
有人会建立一个docker镜像，该镜像可以进行攻击并提供Linux root shell。 
通过使用root shell，有人可能会在你的RouterOS系统中留下永久的后门/漏洞，即使在docker镜像被删除和容器功能被禁用之后。 
如果一个漏洞被注入到主要或次要的路由器启动项（或供应商的预加载器），那么即使netinstall也可能无法修复它。

## 要求

容器包与 **arm arm64** 和 **x86** 架构兼容。使用remote-image（类似于docker pull）功能需要主内存中有大量的空闲空间，16MB的SPI闪存可以用USB或其他磁盘介质上的预构建镜像。

强烈建议使用外部磁盘

需要安装容器包

## 属性

## 容器使用实例

先决条件。

1. 使用RouterOS v7.4beta或更高版本的RouterOS设备，并且 **安装了容器包**。 
2. 对设备进行物理访问以启用容器模式
3. 连接的硬盘或USB驱动器用于存储--格式化为ext3/ext4

## 启用容器模式

[Device-mode](https://help.mikrotik.com/docs/display/ROS/Device-mode) limits container use by default, before granting container mode access - make sure your device is fully secured.

启用容器模式

`/system/device-mode/update container=yes`

如果在X86上使用容器，需要按一下复位按钮来确认设备模式，或者冷重启。

## 创建网络

为容器添加 veth 接口。

`/interface/veth/ add name =veth1 address =172.17.0.2/24 gateway =172.17.0.1`。

为容器创建一个网桥，并将 veth 添加到其中。

`/interface/bridge/add name=dockers`。

`/ip/address/add address =172.17.0.1/24 interface =dockers`。

`/interface/bridge/port add bridge =dockers interface =veth1`。

为出站流量设置NAT。

`/ip/firewall/nat/ add chain =srcnat action =masquerade src-address =172.17.0.0/24`。

## 添加环境变量和挂载(可选)

为容器创建环境变量（可选）。

`/container/envs/ add name =pihole_envs key =TZ value = "Europe/Riga"`

`/container/envs/ add name =pihole_envs key =WEBPASSWORD value = "mysecurepassword"`

`/container/envs/ add name =pihole_envs key =DNSMASQ_USER value = "root"`

定义挂载 (可选):

`/container/mounts/ add name =etc_pihole src =disk1/etc dst =/etc/pihole`

`/container/mounts/ add name =dnsmasq_pihole src =disk1/etc-dnsmasq.d dst =/etc/dnsmasq.d`

`src=` 指向RouterOS的位置（也可以是 `src=disk1/etc_pihole`，如果，你决定把配置文件放在外部USB上），`dst=` 指向定义的位置（查阅容器手册/wiki/github了解指向何处）。如果第一次使用时 `src` 目录不存在，那么它将被填充到 `dst` 位置的任何容器中。

添加容器镜像

如果你希望在日志中看到容器的输出--在创建容器时添加 `logging=yes`，root-dir应该指向ext3或ext4格式的外部驱动器。不建议为容器使用内部存储。 
有多种方法来添加容器。

### a) 从外部库获取镜像

设置注册表-url（用于从Docker注册表下载容器），并将提取目录（tmpdir）设置为附加的USB介质。

拉取镜像。

`/container/ add remote-image =pihole/pihole:latest interface =veth1 root-dir =disk1/pihole mounts =dnsmasq_pihole,etc_pihole envlist =pihole_envs`

镜像将被自动拉出并提取到root-dir，状态可以通过以下方式检查

### b) 从PC导入镜像

这些链接是截至2022年6月16日的 "最新 "版本。请确保下载符合你RouterOS设备架构的正确版本。  
从docker hub更新sha256和以获得最新的镜像文件

```shell
arm64:

    docker pull pihole /pihole :latest@sha256:4cef8a7b32d318ba218c080a3673b56f396d2e2c74d375bef537ff5e41fc4638

    docker save pihole /pihole > pihole. tar

arm

    docker pull pihole /pihole :latest@sha256:684c59c7c057b2829d19d08179265c79a9ddabf03145c1e2fad2fae3d9c36a94

    docker save pihole /pihole > pihole. tar

amd64

    docker pull pihole /pihole :latest@sha256:f56885979dcffeb902d2ca51828c92118199222ffb8f6644505e7881e11eeb85

    docker save pihole /pihole > pihole. tar
```

文件被下载和解压后，上传到RouterOS设备上。从tar镜像创建一个容器

`/container/ add file =pihole.tar interface =veth1 envlist =pihole_envs root-dir =disk1/pihole mounts =dnsmasq_pihole,etc_pihole hostname =PiHole`

### c) 在PC上建立一个镜像

#### Linux系统的步骤

要使用Dockerfile制作docker包--需要安装docker以及buildx或其他构建工具。

最简单的方法是下载并安装Docker引擎。
[https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

安装后检查是否有额外的架构可用。

应该返回:

```shell
NAME /NODE DRIVER /ENDPOINT STATUS  PLATFORMS

default * docker

  default default         running linux /amd64 , linux /arm64 , linux /riscv64 , linux /ppc64le , linux /s390x , linux /386 , linux /arm/v7 , linux /arm/v6

If not - install extra architectures:

docker run --privileged -- rm tonistiigi /binfmt -- install all

pull or create your project with Dockerfile included  and build, extract image:

git clone https: //github .com /pi-hole/docker-pi-hole .git

cd docker-pi-hole

docker buildx build  --no-cache --platform arm64 -t pihole .

docker save pihole > pihole. tar
```

上传 _pihole.tar_ 到RouterOS设备。

Linux系统上的镜像和对象可以是 [pruned](https://docs.docker.com/engine/reference/commandline/system_prune/)

从tar镜像创建一个容器

`/container/ add file =pihole.tar interface =veth1 envlist =pihole_envs mounts =dnsmasq_pihole,etc_pihole hostname =PiHole`

## 启动容器

通过使用 `/container/print` 来确保容器已经被添加并且 `status=stopped`。

可以通过网络浏览器导航到 `http://172.17.0.2` 来访问PiHole的网络面板。

## 转发端口到内部Docker

端口可以使用dst-nat（其中192.168.88.1路由器的IP地址）进行转发。

`/ip firewall nat`

`add action =dst-nat chain =dstnat dst-address =192.168.88.1 dst-port =80 protocol =tcp to-addresses =172.17.0.2 to-ports =80`

对于Pihole容器--将DNS服务器设置为容器veth接口的IP地址：

`/ip dns set servers =172.17.0.2`

或改变DHCP服务器的设置以服务于Pihole的DNS

## 技巧和窍门

- 容器会占用大量的磁盘空间，强烈建议使用USB/SATA,NVMe连接的媒体。对于有USB端口的设备--USB到SATA适配器可以使用2.5 "驱动器--用于额外的存储和更快的文件操作。
- 内存的使用可以通过下面命令来限制：

`/container/config/ set ram-high =200M`

这将软限制RAM的使用-如果RAM的使用超过了边界值，c组的进程就会被节制，并承受回收压力。

- 要在路由器重启后启动容器，使用start-on-boot选项（从7.6beta6开始）。
    
    ```shell
    /container/ print
    
     0 name = "2e679415-2edd-4300-8fab-a779ec267058" tag = "test_arm64:latest" os = "linux" arch = "arm" interface =veth2
    
       root-dir =disk1/alpine mounts = "" dns = "" logging =yes start-on-boot =yes status =running
    
    /container/ set 0 start-on-boot =yes
    ```
    
- 可以进入到 **运行中的** 容器shell。
    
- 启用日志获得容器的输出。
    
   `/container/ set 0 logging =yes`
   