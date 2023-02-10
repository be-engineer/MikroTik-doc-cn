# PCQ 示例

Per Connection Queue (PCQ) 是一种排队规则，可用于动态均衡或调整多个用户的流量，只需很少的管理。 可以将PCQ场景分为三大类：多个用户的带宽均等分配、用户之间的特定带宽均等分配和用户之间未知带宽的均等分配。

## 多个用户的带宽相等

当要为多个用户均衡带宽 [并设置最大限制] 时，使用 PCQ 类型队列。 这里将设置 64kbps 下载和 32kbps 上传限制。

![](https://help.mikrotik.com/docs/download/attachments/137986099/PCQ.jpg?version=1&modificationDate=1658488911159&api=v2)

有两种方法可以做到这一点：使用 mangle 和队列树，或者使用简单队列。

1. 用 packet-marks upload/download 标记所有数据包：（假设 ether1-WAN 是互联网的公共接口，ether2-LAN 是客户端连接的本地接口）：

```shell
/ip firewall mangle add chain =prerouting action =mark-packet 

   in-interface =ether2-LAN new-packet-mark =client_upload

/ip firewall mangle add chain =prerouting action =mark-packet 

   in-interface =ether1-WAN new-packet-mark =client_download
```

2. 设置两种 PCQ 队列类型 - 一种用于下载，一种用于上传。 _dst-address_ 是用户下载流量的分类器，_src-address_ 是上传流量的分类器：

`/queue type add name = "PCQ_download" kind =pcq pcq-rate =64000 pcq-classifier =dst-address`

`/queue type add name = "PCQ_upload" kind =pcq pcq-rate =32000 pcq-classifier =src-address`
  
3、最后需要两条队列规则，一条用于下载，一条用于上传：

`/queue tree add parent =global queue =PCQ_download packet-mark =client_download`

`/queue tree add parent =global queue =PCQ_upload packet-mark =client_upload`

如果不喜欢使用 mangle 和队列树，可以跳过第 1 步，执行第 2 步，第 3 步将创建一个简单的队列，如下所示：

`/queue simple add target =192.168.0.0/24 queue =PCQ_upload/PCQ_download`
