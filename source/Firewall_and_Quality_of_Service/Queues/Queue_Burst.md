# 队列突发介绍

突发是一种功能，可以满足队列对额外带宽的要求，即使所要求的速率在有限的时间内大于 **MIR** （**max-limit**）。

只有在最后 **burst-time** 时间内队列的 **average-rate** 小于 **burst-threshold** 时，才能发生突发。如果最后 **burst-time** 时间内队列的 **average-rate** 大于或等于 **burst-threshold**，突发就会停止。

突发机制很简单-如果允许突发，**max-limit** 值将被 **burst-limit** 值取代。当突发被禁止时，**max-limit** 值保持不变。

1. **burst-limit** （数字）：允许突发时可达到的最大上传/下载数据速率。
2. **burst-time** （时间）：计算平均数据速率的时间段，以秒为单位。(这不是实际突发的时间）。
3. **burst-threshold** (数字)：这是突发开/关的值。
4. **average-rate** （只读）。在 **burst-time** 的每1/16，路由器会计算出每个等级在过去 **burst-time** 时间内的平均速率。
5. **actual-rate** （只读）：队列的实际流量传输率。

## 例子

Values: **limit-at=1M** , **max-limit=2M** , **burst-threshold=1500k** , **burst-limit=4M**

客户端尝试下载两个4MB（32Mb）的数据块，第一个下载将在0秒开始，第二个下载将在17秒开始。流量在最后一分钟没有使用。

### Burst-time=16s

![](https://help.mikrotik.com/docs/download/attachments/137986091/Burst_time.16.part1.jpg?version=1&modificationDate=1658488555129&api=v2)![](https://help.mikrotik.com/docs/download/attachments/137986091/Burst_time.16.part2.jpg?version=2&modificationDate=1658488571361&api=v2)

一旦客户端请求带宽，就能在 6 秒内获得 4Mpbs 的突发流量。 这是具有给定值的最长可能突发 _(longest-burst-time = burst-threshold \* burst-time / burst-limit)_。 一旦突发用完，其余数据将以 2Mbps 的速度下载。 这样，数据块在 9 秒内下载完毕—如果没有突发，则需要 16 秒。 在下一次下载开始之前，突发有 7 秒的充电时间。

注意，在下载开始时不允许突发，只会在之后开始 - 在下载过程中。 通过这个例子证明了在下载过程中可能会发生突发。 突发大约 4 秒长，第二个块的下载速度比没有突发时快 4 秒。

平均速率每 1/16 的突发时间计算一次，因此在这种情况下为 1s

| 时间 | 平均速率                                      | 突发                                                   | 实际速率  |
| ---- | --------------------------------------------- | ------------------------------------------------------ | --------- |
| 0    | (0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0)/16=0Kbps    | average-rate < burst-threshold → Burst is allowed      | 4Mbps     |
| 1    | (0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+4)/16=250Kbps  | average-rate < burst-threshold → Burst is allowed      | 4Mbps     |
| 2    | (0+0+0+0+0+0+0+0+0+0+0+0+0+0+4+4)/16=500Kbps  | average-rate < burst-threshold → Burst is allowed      | 4Mbps     |
| 3    | (0+0+0+0+0+0+0+0+0+0+0+0+0+4+4+4)/16=750Kbps  | average-rate < burst-threshold → Burst is allowed      | 4Mbps     |
| 4    | (0+0+0+0+0+0+0+0+0+0+0+0+4+4+4+4)/16=1000Kbps | average-rate < burst-threshold → Burst is allowed      | 4Mbps     |
| 5    | (0+0+0+0+0+0+0+0+0+0+0+4+4+4+4+4)/16=1250Kbps | average-rate < burst-threshold → Burst is allowed      | 4Mbps     |
| 6    | (0+0+0+0+0+0+0+0+0+0+4+4+4+4+4+4)/16=1500Kbps | average-rate = burst-threshold → Burst **not** allowed | **2Mbps** |
| 7    | (0+0+0+0+0+0+0+0+0+4+4+4+4+4+4+2)/16=1625Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps     |
| 8    | (0+0+0+0+0+0+0+0+4+4+4+4+4+4+2+2)/16=1750Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps     |
| 9    | (0+0+0+0+0+0+0+4+4+4+4+4+4+2+2+2)/16=1875Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps     |
| 10   | (0+0+0+0+0+0+4+4+4+4+4+4+2+2+2+2)/16=2Mbps    | average-rate > burst-threshold → Burst not allowed     | **0Mbps** |
| 11   | (0+0+0+0+0+4+4+4+4+4+4+2+2+2+2+0)/16=2Mbps    | average-rate > burst-threshold → Burst not allowed     | 0Mbps     |
| 12   | (0+0+0+0+4+4+4+4+4+4+2+2+2+2+0+0)/16=2Mbps    | average-rate > burst-threshold → Burst not allowed     | 0Mbps     |
| 13   | (0+0+0+4+4+4+4+4+4+2+2+2+2+0+0+0)/16=2Mbps    | average-rate > burst-threshold → Burst not allowed     | 0Mbps     |
| 14   | (0+0+4+4+4+4+4+4+2+2+2+2+0+0+0+0)/16=2Mbps    | average-rate > burst-threshold → Burst not allowed     | 0Mbps     |
| 15   | (0+4+4+4+4+4+4+2+2+2+2+0+0+0+0+0)/16=2Mbps    | average-rate > burst-threshold → Burst not allowed     | 0Mbps     |
| 16   | (4+4+4+4+4+4+2+2+2+2+0+0+0+0+0+0)/16=2Mbps    | average-rate > burst-threshold → Burst not allowed     | 0Mbps     |
| 17   | (4+4+4+4+4+2+2+2+2+0+0+0+0+0+0+0)/16=1750Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps     |
| 18   | (4+4+4+4+2+2+2+2+0+0+0+0+0+0+0+2)/16=1500Kbps | average-rate = burst-threshold → Burst not allowed     | 2Mbps     |
| 19   | (4+4+4+2+2+2+2+0+0+0+0+0+0+0+2+2)/16=1375Kbps | average-rate < burst-threshold → Burst **is** allowed  | 4Mbps     |
| 20   | (4+4+2+2+2+2+0+0+0+0+0+0+0+2+2+4)/16=1375Kbps | average-rate < burst-threshold → Burst is allowed      | 4Mbps     |
| 21   | (4+2+2+2+2+0+0+0+0+0+0+0+2+2+4+4)/16=1375Kbps | average-rate < burst-threshold → Burst is allowed      | 4Mbps     |
| 22   | (2+2+2+2+0+0+0+0+0+0+0+2+2+4+4+4)/16=1375Kbps | average-rate < burst-threshold → Burst is allowed      | 4Mbps     |
| 23   | (2+2+2+0+0+0+0+0+0+0+2+2+4+4+4+4)/16=1500Kbps | average-rate = burst-threshold → Burst **not** allowed | 2Mbps     |
| 24   | (2+2+0+0+0+0+0+0+0+2+2+4+4+4+4+2)/16=1500Kbps | average-rate = burst-threshold → Burst not allowed     | 2Mbps     |
| 25   | (2+0+0+0+0+0+0+0+2+2+4+4+4+4+2+2)/16=1500Kbps | average-rate = burst-threshold → Burst not allowed     | 2Mbps     |
| 26   | (0+0+0+0+0+0+0+2+2+4+4+4+4+2+2+2)/16=1500Kbps | average-rate = burst-threshold → Burst not allowed     | 2Mbps     |
| 27   | (0+0+0+0+0+0+2+2+4+4+4+4+2+2+2+2)/16=1625Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps     |
| 28   | (0+0+0+0+0+2+2+4+4+4+4+2+2+2+2+2)/16=1750Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps     |
| 29   | (0+0+0+0+2+2+4+4+4+4+2+2+2+2+2+2)/16=1875Kbps | average-rate > burst-threshold → Burst not allowed     | 0Mbps     |
| 30   | (0+0+0+2+2+4+4+4+4+2+2+2+2+2+2+0)/16=1875Kbps | average-rate > burst-threshold → Burst not allowed     | 0Mbps     |
| 31   | (0+0+2+2+4+4+4+4+2+2+2+2+2+2+0+0)/16=1875Kbps | average-rate > burst-threshold → Burst not allowed     | 0Mbps     |

### Burst-time=8s

![](https://help.mikrotik.com/docs/download/attachments/137986091/Burst_time.8.part1.jpg?version=1&modificationDate=1658488707444&api=v2)![](https://help.mikrotik.com/docs/download/attachments/137986091/Burst_time.8.part2.jpg?version=1&modificationDate=1658488716549&api=v2)

如果将突发时间减少到8秒-可以看到突发只是在下载的开始阶段，平均速率是以每1/16突发时间计算的，在这种情况下，每0.5秒计算一次。

| 时间 | 平均速率                                     | 突发                                                   | 实际速率                   |
| ---- | -------------------------------------------- | ------------------------------------------------------ | -------------------------- |
| 0.0  | (0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0)/8=0Kbps    | average-rate < burst-threshold → Burst is allowed      | 4Mbps (2Mb per 0,5sek)     |
| 0.5  | (0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+2)/8=250Kbps  | average-rate < burst-threshold → Burst is allowed      | 4Mbps (2Mb per 0,5sek)     |
| 1.0  | (0+0+0+0+0+0+0+0+0+0+0+0+0+0+2+2)/8=500Kbps  | average-rate < burst-threshold → Burst is allowed      | 4Mbps (2Mb per 0,5sek)     |
| 1.5  | (0+0+0+0+0+0+0+0+0+0+0+0+0+2+2+2)/8=750Kbps  | average-rate < burst-threshold → Burst is allowed      | 4Mbps (2Mb per 0,5sek)     |
| 2.0  | (0+0+0+0+0+0+0+0+0+0+0+0+2+2+2+2)/8=1000Kbps | average-rate < burst-threshold → Burst is allowed      | 4Mbps (2Mb per 0,5sek)     |
| 2.5  | (0+0+0+0+0+0+0+0+0+0+0+2+2+2+2+2)/8=1250Kbps | average-rate < burst-threshold → Burst is allowed      | 4Mbps (2Mb per 0,5sek)     |
| 3.0  | (0+0+0+0+0+0+0+0+0+0+2+2+2+2+2+2)/8=1500Kbps | average-rate = burst-threshold → Burst **not** allowed | **2Mbps** (1Mb per 0,5sek) |
| 3.5  | (0+0+0+0+0+0+0+0+0+2+2+2+2+2+2+1)/8=1625Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 4.0  | (0+0+0+0+0+0+0+0+2+2+2+2+2+2+1+1)/8=1750Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 4.5  | (0+0+0+0+0+0+0+2+2+2+2+2+2+1+1+1)/8=1875Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 5.0  | (0+0+0+0+0+0+2+2+2+2+2+2+1+1+1+1)/8=2000Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 5.5  | (0+0+0+0+0+2+2+2+2+2+2+1+1+1+1+1)/8=2125Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 6.0  | (0+0+0+0+2+2+2+2+2+2+1+1+1+1+1+1)/8=2250Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 6.5  | (0+0+0+2+2+2+2+2+2+1+1+1+1+1+1+1)/8=2375Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 7.0  | (0+0+2+2+2+2+2+2+1+1+1+1+1+1+1+1)/8=2500Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 7.5  | (0+2+2+2+2+2+2+1+1+1+1+1+1+1+1+1)/8=2625Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 8.0  | (2+2+2+2+2+2+1+1+1+1+1+1+1+1+1+1)/8=2750Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 8.5  | (2+2+2+2+2+1+1+1+1+1+1+1+1+1+1+1)/8=2625Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 9.0  | (2+2+2+2+1+1+1+1+1+1+1+1+1+1+1+1)/8=2500Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 9.5  | (2+2+2+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2375Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 10.0 | (2+2+1+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2250Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 10.5 | (2+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2125Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 11.0 | (1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2000Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 11.5 | (1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2000Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 12.0 | (1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2000Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 12.5 | (1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2000Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 13.0 | (1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2000Kbps | average-rate > burst-threshold → Burst not allowed     | **0Mbps** (0Mb per 0,5sek) |
| 13.5 | (1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+0)/8=1875Kbps | average-rate > burst-threshold → Burst not allowed     | 0Mbps (0Mb per 0,5sek)     |
| 14.0 | (1+1+1+1+1+1+1+1+1+1+1+1+1+1+0+0)/8=1750Kbps | average-rate > burst-threshold → Burst not allowed     | 0Mbps (0Mb per 0,5sek)     |
| 14.5 | (1+1+1+1+1+1+1+1+1+1+1+1+1+0+0+0)/8=1625Kbps | average-rate > burst-threshold → Burst not allowed     | 0Mbps (0Mb per 0,5sek)     |
| 15.0 | (1+1+1+1+1+1+1+1+1+1+1+1+0+0+0+0)/8=1500Kbps | average-rate > burst-threshold → Burst not allowed     | 0Mbps (0Mb per 0,5sek)     |
| 15.5 | (1+1+1+1+1+1+1+1+1+1+1+0+0+0+0+0)/8=1375Kbps | average-rate < burst-threshold → Burst **is** allowed  | 0Mbps (0Mb per 0,5sek)     |
| 16.0 | (1+1+1+1+1+1+1+1+1+1+0+0+0+0+0+0)/8=1250Kbps | average-rate < burst-threshold → Burst is allowed      | 0Mbps (0Mb per 0,5sek)     |
| 16.5 | (1+1+1+1+1+1+1+1+1+0+0+0+0+0+0+0)/8=1125Kbps | average-rate < burst-threshold → Burst is allowed      | 0Mbps (0Mb per 0,5sek)     |
| 17.0 | (1+1+1+1+1+1+1+1+0+0+0+0+0+0+0+0)/8=1000Kbps | average-rate < burst-threshold → Burst is allowed      | **2Mbps** (1Mb per 0,5sek) |
| 17.5 | (1+1+1+1+1+1+1+0+0+0+0+0+0+0+0+1)/8=1000Kbps | average-rate < burst-threshold → Burst is allowed      | **4Mbps** (2Mb per 0,5sek) |
| 18.0 | (1+1+1+1+1+1+0+0+0+0+0+0+0+0+1+2)/8=1125Kbps | average-rate < burst-threshold → Burst is allowed      | 4Mbps (2Mb per 0,5sek)     |
| 18.5 | (1+1+1+1+1+0+0+0+0+0+0+0+0+1+2+2)/8=1250Kbps | average-rate < burst-threshold → Burst is allowed      | 4Mbps (2Mb per 0,5sek)     |
| 19.0 | (1+1+1+1+0+0+0+0+0+0+0+0+1+2+2+2)/8=1375Kbps | average-rate < burst-threshold → Burst is allowed      | 4Mbps (2Mb per 0,5sek)     |
| 19.5 | (1+1+1+0+0+0+0+0+0+0+0+1+2+2+2+2)/8=1500Kbps | average-rate = burst-threshold → Burst **not** allowed | 2Mbps (1Mb per 0,5sek)     |
| 20.0 | (1+1+0+0+0+0+0+0+0+0+1+2+2+2+2+1)/8=1500Kbps | average-rate = burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 20.5 | (1+0+0+0+0+0+0+0+0+1+2+2+2+2+1+1)/8=1500Kbps | average-rate = burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 21.0 | (0+0+0+0+0+0+0+0+1+2+2+2+2+1+1+1)/8=1500Kbps | average-rate = burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 21.5 | (0+0+0+0+0+0+0+1+2+2+2+2+1+1+1+1)/8=1625Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 22.0 | (0+0+0+0+0+0+1+2+2+2+2+1+1+1+1+1)/8=1750Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 22.5 | (0+0+0+0+0+1+2+2+2+2+1+1+1+1+1+1)/8=1875Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 23.0 | (0+0+0+0+1+2+2+2+2+1+1+1+1+1+1+1)/8=2000Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 23.5 | (0+0+0+1+2+2+2+2+1+1+1+1+1+1+1+1)/8=2125Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 24.0 | (0+0+1+2+2+2+2+1+1+1+1+1+1+1+1+1)/8=2250Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 24.5 | (0+1+2+2+2+2+1+1+1+1+1+1+1+1+1+1)/8=2375Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 25.0 | (1+2+2+2+2+1+1+1+1+1+1+1+1+1+1+1)/8=2500Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 25.5 | (2+2+2+2+1+1+1+1+1+1+1+1+1+1+1+1)/8=2500Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 26.0 | (2+2+2+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2375Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 26.5 | (2+2+1+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2250Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 27.0 | (2+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2125Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 27.5 | (1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2000Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 28.0 | (1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2000Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 28.5 | (1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2000Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 29.0 | (1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2000Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 29.5 | (1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2000Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 30.0 | (1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2000Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps (1Mb per 0,5sek)     |
| 30.5 | (1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1)/8=2000Kbps | average-rate > burst-threshold → Burst not allowed     | 0Mbps (0Mb per 0,5sek)     |
| 31.0 | (1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+0)/8=1875Kbps | average-rate > burst-threshold → Burst not allowed     | 0Mbps (0Mb per 0,5sek)     |
