# 路由参考

`/routing/id`

全局Router ID选举配置。ID可以显式配置，也可以设置为从路由器的一个IP地址中选出。

对于每个VRF表，RouterOS添加动态ID实例，从属于特定VRF的一个IP地址中选择ID:

```shell
[admin@rack1_b33_CCR1036] /routing/id> print
Flags: D - DYNAMIC, I - INACTIVE
Columns: NAME, DYNAMIC-ID, SELECT-DYNAMIC-ID, SELECT-FROM-VRF
#   NAME   DYNAMIC-ID      SELECT-D   SELE
0 D main   111.111.111.2   only-vrf   main
```

## 配置选项

| 属性                                                                                              | 说明                                                                                                                                                                                                                                                                                 |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **comment** (_string_)                                                                            |                                                                                                                                                                                                                                                                                      |
| **disabled** (_yes \| no_)                                                                        | 没有用ID引用。                                                                                                                                                                                                                                                                       |
| **id**(_IP_)                                                                                      | 参数显式设置Router id。如果没有显式指定ID，则可以从路由器上配置的IP地址中选择一个。参见参数select-dynamic-id和select-from-vrf。                                                                                                                                                      |
| **name** (_string_)                                                                               | 引用名                                                                                                                                                                                                                                                                               |
| **select-dynamic-id**(_any \| lowest \| only-active \| only-loopback \| only-static \| only-vrf_) | 说明在选举ID时用的IP地址:<br>- any - 在路由器上找到的任何地址都可以被选为router ID。<br>- lowest - 选择最低的IP地址。<br>- only-active - 只从主IP地址中选择。<br>- only-loopback -只从loopback地址中选择ID。<br>- only- VRF - 只从选定的VRF中选择ID。与select-from-vrf属性一起工作。 |
| **select-from-vrf** (_name_)                                                                      | 选择IP地址进行ID选举的VRF。                                                                                                                                                                                                                                                          |

**只读属性**

| 属性                       | 说明                                             |
| -------------------------- | ------------------------------------------------ |
| **dynamic** (_yes \| no_)  |                                                  |
| **dynamic-id** (_IP_)      | 当前选择的ID。                                   |
| **inactive** (_yes \| no_) | 如果获取有效ID有问题，那么项目可以变为inactive。 |