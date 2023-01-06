- 根据需要使用系统盘和其他设备创建新的guest。

- 然后你必须在 ProxMox 主机上手动上传 CHR 磁盘（qcow 格式）。

- 使用 _scp_ 或任何其他类似工具，因为它将使用 SSH 进行上传，并且不需要任何额外配置。

- 将文件复制到服务器然后手动编辑 VM 的 .conf 文件或替换之前创建的用于引导客户机的系统映像文件。

- ProxMox 上的本地存储位于 _/var/lib/vz_ 目录中。 应该有一个名为 _images_ 的子目录，其中包含每个 VM 的目录（以 VM 编号命名）。 您可以直接在那里复制文件。

- 要将现有文件添加到 VM，请直接编辑 VM 的 .conf 文件。 在 _/etc/pve/qemu-server/_ 中查找带有 VM 编号后跟 .conf 的文件。

**注意：** 创建第二个测试 VM 是个好主意，这样您就可以参考它的 .conf 文件以确保语法正确

#### 替代方法

- 通过 ProxMox Web GUI 创建基本虚拟机。
- 确保 VM 存储在本地（这样就不需要使用 LVM 配置，并且磁盘映像可以稍后移动到 LVM 或其他需要的存储）。
- 通过 SSH 登录 ProxMox 主机并导航到 VM 映像目录。 默认本地存储位于：_var/lib/vz/images/(VM\_ID)_
- 通过 scp、wget 或任何其他工具将 CHR 原始映像（.img 文件）下载到此目录中。
- 现在使用 qemu-img 工具将 CHR 原始映像转换为 qcow2 格式：

```
qemu-img convert -f raw -O qcow2 chr-6.40.3.img vm-(VM_ID)-disk-1.qcow2
```

#### Bash 脚本方法

如果您有权访问 ProxMox 主机，则还可以通过 BASH 脚本快速创建 CHR VM。 下面是一个这样的脚本的例子。

该脚本的作用：

- 将 tmp 文件存储在：_/root/temp_ 目录中。
- 从 MikroTik 下载页面下载原始映像存档。
- 将映像文件转换为 qcow 格式。
- 创建依附到 MGMT 网桥的基本 VM。

```
#!/bin/bash

#vars
version="nil"
vmID="nil"

echo "############## Start of Script ##############

## Checking if temp dir is available..."
if [ -d /root/temp ] 
then
    echo "-- Directory exists!"
else
    echo "-- Creating temp dir!"
    mkdir /root/temp
fi
# Ask user for version
echo "## Preparing for image download and VM creation!"
read -p "Please input CHR version to deploy (6.38.2, 6.40.1, etc):" version
# Check if image is available and download if needed
if [ -f /root/temp/chr-$version.img ] 
then
    echo "-- CHR image is available."
else
    echo "-- Downloading CHR $version image file."
    cd  /root/temp
    echo "---------------------------------------------------------------------------"
    wget https://download.mikrotik.com/routeros/$version/chr-$version.img.zip
    unzip chr-$version.img.zip
    echo "---------------------------------------------------------------------------"
fi
# List already existing VM's and ask for vmID
echo "== Printing list of VM's on this hypervisor!"
qm list
echo ""
read -p "Please Enter free vm ID to use:" vmID
echo ""
# Create storage dir for VM if needed.
if [ -d /var/lib/vz/images/$vmID ] 
then
    echo "-- VM Directory exists! Ideally try another vm ID!"
    read -p "Please Enter free vm ID to use:" vmID
else
    echo "-- Creating VM image dir!"
    mkdir /var/lib/vz/images/$vmID
fi
# Creating qcow2 image for CHR.
echo "-- Converting image to qcow2 format "
qemu-img convert \
    -f raw \
    -O qcow2 \
    /root/temp/chr-$version.img \
    /var/lib/vz/images/$vmID/vm-$vmID-disk-1.qcow2
# Creating VM
echo "-- Creating new CHR VM"
qm create $vmID \
  --name chr-$version \
  --net0 virtio,bridge=vmbr0 \
  --bootdisk virtio0 \
  --ostype l26 \
  --memory 256 \
  --onboot no \
  --sockets 1 \
  --cores 1 \
  --virtio0 local:$vmID/vm-$vmID-disk-1.qcow2
echo "############## End of Script ##############"

```

#### 提示

- 用于从 Windows 格式中清除 BASH 脚本的有用片段，如果在 Windows 工作站上编辑它可能会干扰脚本：

```
sed -i -e 's/\r$//' *.sh
```