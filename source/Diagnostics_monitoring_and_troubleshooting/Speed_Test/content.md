# 介绍

速度测试是一个简单的测试工具，用于测量从一个MikroTik设备到另一个设备的ping、jitter、TCP和UDP的吞吐率。“Speed-test "命令基于Ping工具和带宽测试。为了使用这个命令--需要访问带宽测试服务器。

## 一般接口属性

速度测试基于五个可配置的属性。

- address - 主机 IP 地址。
- connection-count - 如果一个设备有超过20个核，将使用核数（默认为20）。
- password - 远程设备的密码。
- test-duration - 每次测试的持续时间（ _默认：5次测试*10秒持续时间+每次测试之间的1秒停顿=55秒_ ）。
- user - 远程设备的用户名。

## 配置实例

带宽和速度测试要在设备间进行，而不是在本地设备上进行以确保模拟真实的情况，避免产生的流量不会使被测设备的CPU过载（DUT）。

从设备A（192.168.88.1）到设备B（192.168.88.2）进行一个简单的测试。

```shell
[admin@MikroTik] > /tool/speed-test address=192.168.88.1
              status: done
      time-remaining: 0s
    ping-min-avg-max: 541us / 609us / 3.35ms
  jitter-min-avg-max: 0s / 76us / 2.76ms
                loss: 0% (0/100)
        tcp-download: 921Mbps local-cpu-load:30%
          tcp-upload: 920Mbps local-cpu-load:30% remote-cpu-load:25%
        udp-download: 917Mbps local-cpu-load:6% remote-cpu-load:21%
          udp-upload: 916Mbps local-cpu-load:20% remote-cpu-load:6%
```

如果测试期间任何设备的CPU利用率达到100%，就会出现警告信息。

```shell
[admin@MikroTik]] > /tool/speed-test address=192.168.88.1
                  ;;; results can be limited by cpu, note that traffic generation/termination
                      performance might not be representative of forwarding performance
              status: done
      time-remaining: 0s
    ping-min-avg-max: 541us / 609us / 3.35ms
  jitter-min-avg-max: 0s / 76us / 2.76ms
                loss: 0% (0/100)
        tcp-download: 721Mbps local-cpu-load:78%
          tcp-upload: 820Mbps local-cpu-load:100% remote-cpu-load:84%
        udp-download: 906Mbps local-cpu-load:10% remote-cpu-load:54%
          udp-upload: 895Mbps local-cpu-load:55% remote-cpu-load:12%
```

"test-duration"参数允许改变全部5项测试的持续时间:

- Ping test with 50ms delay
- TCP receive
- TCP send
- UDP receive
- UDP send
