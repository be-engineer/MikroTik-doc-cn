# 队列突发介绍

Burst is a feature that allows satisfying queue requirements for additional bandwidth even if the required rate is bigger than **MIR** (**max-limit**) for a limited period of time.

Burst can occur only if **average-rate** of the queue for the last **burst-time** seconds is smaller than **burst-threshold**. Burst will stop if **average-rate** of the queue for the last **burst-time** seconds is bigger or equal to **burst-threshold.**

The burst mechanism is simple - if a burst is allowed **max-limit** value is replaced by the **burst-limit** value. When the burst is disallowed **max-limit** value remains unchanged.

1. **burst-limit** (NUMBER) : maximal upload/download data rate which can be reached while the burst is allowed;
2. **burst-time** (TIME) : period of time, in seconds, over which the average data rate is calculated. (This is NOT the time of actual burst);
3. **burst-threshold** (NUMBER) : this is value of burst on/off switch;
4. **average-rate** (read-only) : Every 1/16 part of the **burst-time**, the router calculates the average data rate of each class over the last **burst-time** seconds;
5. **actual-rate** (read-only) : actual traffic transfer rate of the queue;

## Example

Values: **limit-at=1M** , **max-limit=2M** , **burst-threshold=1500k** , **burst-limit=4M**

The client will try to download two 4MB (32Mb) blocks of data, the first download will start at zero seconds, and the second download will start at 17th second. Traffic was unused at the last minute.

### Burst-time=16s

![](https://help.mikrotik.com/docs/download/attachments/137986091/Burst_time.16.part1.jpg?version=1&modificationDate=1658488555129&api=v2)![](https://help.mikrotik.com/docs/download/attachments/137986091/Burst_time.16.part2.jpg?version=2&modificationDate=1658488571361&api=v2)

As we can see as soon as the client requested bandwidth it was able to get 4Mpbs burst for 6 seconds. This is longest possible burst with given values _(longest-burst-time = burst-threshold \* burst-time / burst-limit)_. As soon as the burst runs out rest of the data will be downloaded with 2Mbps. This way block of data was downloaded in 9 seconds - without burst, it would take 16 seconds. Burst has 7 seconds to recharge before the next download will start.

Note that burst is still disallowed when download started and it kicks in only afterward - in the middle of a download. So with this example, we proved that a burst may happen in the middle of a download. The burst was ~4 seconds long and the second block was downloaded 4 seconds faster than without burst.

The average rate is calculated every 1/16 of burst time so in this case 1s

| Time | average-rate                                  | burst                                                  | actual-rate |
| ---- | --------------------------------------------- | ------------------------------------------------------ | ----------- |
| 0    | (0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+0)/16=0Kbps    | average-rate < burst-threshold → Burst is allowed      | 4Mbps       |
| 1    | (0+0+0+0+0+0+0+0+0+0+0+0+0+0+0+4)/16=250Kbps  | average-rate < burst-threshold → Burst is allowed      | 4Mbps       |
| 2    | (0+0+0+0+0+0+0+0+0+0+0+0+0+0+4+4)/16=500Kbps  | average-rate < burst-threshold → Burst is allowed      | 4Mbps       |
| 3    | (0+0+0+0+0+0+0+0+0+0+0+0+0+4+4+4)/16=750Kbps  | average-rate < burst-threshold → Burst is allowed      | 4Mbps       |
| 4    | (0+0+0+0+0+0+0+0+0+0+0+0+4+4+4+4)/16=1000Kbps | average-rate < burst-threshold → Burst is allowed      | 4Mbps       |
| 5    | (0+0+0+0+0+0+0+0+0+0+0+4+4+4+4+4)/16=1250Kbps | average-rate < burst-threshold → Burst is allowed      | 4Mbps       |
| 6    | (0+0+0+0+0+0+0+0+0+0+4+4+4+4+4+4)/16=1500Kbps | average-rate = burst-threshold → Burst **not** allowed | **2Mbps**   |
| 7    | (0+0+0+0+0+0+0+0+0+4+4+4+4+4+4+2)/16=1625Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps       |
| 8    | (0+0+0+0+0+0+0+0+4+4+4+4+4+4+2+2)/16=1750Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps       |
| 9    | (0+0+0+0+0+0+0+4+4+4+4+4+4+2+2+2)/16=1875Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps       |
| 10   | (0+0+0+0+0+0+4+4+4+4+4+4+2+2+2+2)/16=2Mbps    | average-rate > burst-threshold → Burst not allowed     | **0Mbps**   |
| 11   | (0+0+0+0+0+4+4+4+4+4+4+2+2+2+2+0)/16=2Mbps    | average-rate > burst-threshold → Burst not allowed     | 0Mbps       |
| 12   | (0+0+0+0+4+4+4+4+4+4+2+2+2+2+0+0)/16=2Mbps    | average-rate > burst-threshold → Burst not allowed     | 0Mbps       |
| 13   | (0+0+0+4+4+4+4+4+4+2+2+2+2+0+0+0)/16=2Mbps    | average-rate > burst-threshold → Burst not allowed     | 0Mbps       |
| 14   | (0+0+4+4+4+4+4+4+2+2+2+2+0+0+0+0)/16=2Mbps    | average-rate > burst-threshold → Burst not allowed     | 0Mbps       |
| 15   | (0+4+4+4+4+4+4+2+2+2+2+0+0+0+0+0)/16=2Mbps    | average-rate > burst-threshold → Burst not allowed     | 0Mbps       |
| 16   | (4+4+4+4+4+4+2+2+2+2+0+0+0+0+0+0)/16=2Mbps    | average-rate > burst-threshold → Burst not allowed     | 0Mbps       |
| 17   | (4+4+4+4+4+2+2+2+2+0+0+0+0+0+0+0)/16=1750Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps       |
| 18   | (4+4+4+4+2+2+2+2+0+0+0+0+0+0+0+2)/16=1500Kbps | average-rate = burst-threshold → Burst not allowed     | 2Mbps       |
| 19   | (4+4+4+2+2+2+2+0+0+0+0+0+0+0+2+2)/16=1375Kbps | average-rate < burst-threshold → Burst **is** allowed  | 4Mbps       |
| 20   | (4+4+2+2+2+2+0+0+0+0+0+0+0+2+2+4)/16=1375Kbps | average-rate < burst-threshold → Burst is allowed      | 4Mbps       |
| 21   | (4+2+2+2+2+0+0+0+0+0+0+0+2+2+4+4)/16=1375Kbps | average-rate < burst-threshold → Burst is allowed      | 4Mbps       |
| 22   | (2+2+2+2+0+0+0+0+0+0+0+2+2+4+4+4)/16=1375Kbps | average-rate < burst-threshold → Burst is allowed      | 4Mbps       |
| 23   | (2+2+2+0+0+0+0+0+0+0+2+2+4+4+4+4)/16=1500Kbps | average-rate = burst-threshold → Burst **not** allowed | 2Mbps       |
| 24   | (2+2+0+0+0+0+0+0+0+2+2+4+4+4+4+2)/16=1500Kbps | average-rate = burst-threshold → Burst not allowed     | 2Mbps       |
| 25   | (2+0+0+0+0+0+0+0+2+2+4+4+4+4+2+2)/16=1500Kbps | average-rate = burst-threshold → Burst not allowed     | 2Mbps       |
| 26   | (0+0+0+0+0+0+0+2+2+4+4+4+4+2+2+2)/16=1500Kbps | average-rate = burst-threshold → Burst not allowed     | 2Mbps       |
| 27   | (0+0+0+0+0+0+2+2+4+4+4+4+2+2+2+2)/16=1625Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps       |
| 28   | (0+0+0+0+0+2+2+4+4+4+4+2+2+2+2+2)/16=1750Kbps | average-rate > burst-threshold → Burst not allowed     | 2Mbps       |
| 29   | (0+0+0+0+2+2+4+4+4+4+2+2+2+2+2+2)/16=1875Kbps | average-rate > burst-threshold → Burst not allowed     | 0Mbps       |
| 30   | (0+0+0+2+2+4+4+4+4+2+2+2+2+2+2+0)/16=1875Kbps | average-rate > burst-threshold → Burst not allowed     | 0Mbps       |
| 31   | (0+0+2+2+4+4+4+4+2+2+2+2+2+2+0+0)/16=1875Kbps | average-rate > burst-threshold → Burst not allowed     | 0Mbps       |

### Burst-time=8s

![](https://help.mikrotik.com/docs/download/attachments/137986091/Burst_time.8.part1.jpg?version=1&modificationDate=1658488707444&api=v2)![](https://help.mikrotik.com/docs/download/attachments/137986091/Burst_time.8.part2.jpg?version=1&modificationDate=1658488716549&api=v2)

If we decrease burst-time to 8 seconds - we are able to see that in this case, bursts are only at the beginning of downloads The average rate is calculated every 1/16th of burst time, so in this case every 0.5 seconds.

| Time | average-rate                                 | burst                                                  | actual-rate                |
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