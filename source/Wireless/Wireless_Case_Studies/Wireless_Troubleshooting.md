# Wireless Debug Logs

Debugging wireless problems using Logs.

By default RouterOS wireless log shows that client connects and disconnects as simple entries:

[?](https://help.mikrotik.com/docs/display/ROS/Wireless+Troubleshooting#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">22</code><code class="ros constants">:32:18 wireless,</code><code class="ros functions">info </code><code class="ros plain">00</code><code class="ros constants">:80:48:41:AF:2A@wlan1: connected</code></div></div></td></tr></tbody></table>

It is enough for regular users to know that the wireless client with MAC address "00:80:48:41:AF:2A" is connected to wireless interface "wlan1". But actually there are more log entries available than are shown in standard logging. They are called 'debug' logs which give more detailed information. In the following Debug Log example you will see the same client connecting to the AP in more detail than found in typical logging:

[?](https://help.mikrotik.com/docs/display/ROS/Wireless+Troubleshooting#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">22</code><code class="ros constants">:33:20 wireless,debug wlan1: 00:80:48:41:AF:2A attempts to connect</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">22</code><code class="ros constants">:33:20 wireless,debug wlan1: 00:80:48:41:AF:2A not in </code><code class="ros functions">local </code><code class="ros plain">ACL, by default accept</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">22</code><code class="ros constants">:33:20 wireless,</code><code class="ros functions">info </code><code class="ros plain">00</code><code class="ros constants">:80:48:41:AF:2A@wlan1: connected</code></div></div></td></tr></tbody></table>

Debug Logs will give you more specific information on each step of the Client wireless connection and disconnection. The first line shows that the wireless client tried to connect to the AP. On the second line the AP checked to see if that client is allowed to connect to the AP and the resulting action. And only on the third line do you see that the client is connected. This is merely one example of the debug log messages. The description of all debug entries is written below.

To enable the wireless debug logs you should execute such commands:

[?](https://help.mikrotik.com/docs/display/ROS/Wireless+Troubleshooting#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/system logging&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] system logging&gt; </code><code class="ros functions">add </code><code class="ros value">topics</code><code class="ros plain">=wireless,debug</code> <code class="ros value">action</code><code class="ros plain">=memory</code></div></div></td></tr></tbody></table>

This will help you understand and fix wireless problems with ease and with less interaction with the support team.

## STATION MODE

**<MAC>@<DEV>: lost connection, <REASON>**

Station has lost connection to AP because of <REASON>

**<MAC>@<DEV>: failed to connect, <REASON>**

Station attempted to connect to AP, but failed due to <REASON>

**<MAC>@<DEV>: established connection on <FREQ>, SSID <SSID>**

Station attempted and succesfully connected to AP with SSID <SSID> on frequency <FREQ>.

**<MAC>@<DEV>: MIC failure!!!**

TKIP message integrity check failure, somebody must be trying to break into or DOS network, If more than 1 MIC failure is encountered during 60s period, "TKIP countermeasures" state is entered.

**<MAC>@<DEV>: enter TKIP countermeasures**

Entered TKIP countermeasures state, this means that Station will disconnect from AP and keep silence for 60s.

## AP MODE

**<DEV>: radar detected on <FREQ>**

Radar detected on frequency <FREQ>, AP will look for other channel

**<DEV>: data from unknown device <MAC>, sent deauth \[(XXX events suppressed, YYY deauths suppressed)\]**

Data frame from unknown device (read - not registered to this AP) with mac address <MAC> received, AP sent deauthentication frame to it (as per 802.11). XXX is number of events that are not logged so that the log does not become too large (logs are limited to 1 entry per 5s after first 5 entries), YYY is the number of deauthentication frames that should have been sent, but were not sent, so that resources are not wasted sending too many deauthentication frames (only 10 deauth frames per second are allowed).

The likely cause of such a message is that the Station previously connected to the AP, which does not yet know it has been dropped from AP registration table, sending data to AP. Deauthentication message tells the Station that it is no longer connected.

  
**<DEV>: denying assoc to <MAC>, failed to setup compression**

Failed to initialize compression on AP, most likely because there are too many clients attempting to connect and use compression.

  
**<DEV>: <MAC> is new WDS master**

WDS slave has established connection to WDS master, this means that WDS slave starts accepting clients and acting as AP.

  
**<DEV>: <MAC> was WDS master**

This message appears after connection with <MAC> is lost, means that WDS slave will disconnect all clients and start scanning to find new WDS master.

  
**<MAC>@<DEV>: connected \[, is AP\]\[, wants WDS\]**

Station with address <MAC> connected. if "is AP" present - remote device is AP, if "is WDS" presents, remote device wants to establish WDS link.

  
**<MAC>@<DEV>: disconnected, <REASON>**

Connection with Station with address <MAC> terminated due to <REASON>

  
**<DEV>: TKIP countermeasures over, resuming**

TKIP countermeasures (60s silence period) over, AP resumes acting as AP.

  
**<DEV>: starting TKIP countermeasures**

Entering TKIP countermeasures state (60s silence period), all clients will be lost.

## <REASON>

**"joining failed"** - can only happen on Prism cards in station mode, failed to connect to AP due to some reason

**"join timeout"** - happens on Station, failed to synchronize to AP (receive first beacon frame). Most likely weak signal, remote turned off, strong interference, some other RF related issue that makes communication impossible.

**"no beacons"** - no beacons received from remote end of WDS link. Most likely weak signal, remote turned off, strong interference, some other RF related issue that makes communication impossible.

**"extensive data loss"** - local interface decided to drop connection to remote device because of inability to send data to remote after multiple failures at lowest possible rate. Possible causes - too weak signal, remote device turned off, strong interference, some other RF related issue that makes communication impossible.

**"decided to deauth, <802.11 reason>"** - local interface decided do deauthenticate remote device using 802.11 reason <802.11 reason>.

**"inactivity"** - remote device was inactive for too long

**"device disabled"** - local interface got disabled

**"got deauth, <802.11 reason>"** - received deauthentication frame from remote device, 802.11 reason code is reported in <802.11 reason>

**"got disassoc, <802.11 reason>"** - received disassociation frame from remote device, 802.11 reason code is reported in <802.11 reason>

**"auth frame from AP"** - authentication frame from remote device that is known to be AP, most likely mode changes on remote device from AP to Station.

**"bad ssid"** - bad ssid for WDS link

**"beacon from non AP"** - received beacon frame from remote device that is known to be non-AP node, most likely mode changes on remote device from Station to AP.

**"no WDS support"** - does not report WDS support

**"failed to confirm SSID"** - failed to confirm SSID of other end of WDS link.

**"hardware failure"** - some hardware failure or unexpected behavior. Not likely to be seen.

**"lost connection"** - can only happen on Prism cards in station mode, connection to AP lost due to some reason.

**"auth failed <802.11 status>"** - happens on Station, AP denies authentication, 802.11 status code is reported in <802.11 status>.

**"assoc failed <802.11 status>"** - happens on Station, AP denies association, 802.11 status code is reported in <802.11 status>.

**"auth timeout"** - happens on Station, Station does not receive response to authentication frames, either bad link or AP is ignoring this Station for some reason.

**"assoc timeout"** - happens on Station, Station does not receive response to association frames, either bad link or AP is ignoring this Station for some reason.

**"reassociating"** - happens on AP: connection assumed to be lost, because Station that is considered already associated attempts to associate again. All connection related information must be deleted, because during association process connection parameters are negotiated (therefore "disconnected"). The reason why Station reassociates must be looked for on Station (most likely cause is that Station for some reason dropped connection without telling AP - e.g. data loss, configuration changes).

**"compression setup failure"** - connection impossible, because not enough resources to do compression (too many stations that want to use compression already connected)

**"control frame timeout"** - AP was unable to transmit to the client (similar to error message that you see in the 802.11 protocol - extensive data loss)

## <802.11 reason> and <802.11 status>

These are numeric reason/status codes encoded into 802.11 management messages. Log messages include numeric code and textual description from appropriate standard in 802.11 standards group. Although these are intended to be as descriptive as possible, it must be taken into account that actual reason/status code that appears in management frames depends solely on equipment or software manufacturer - where one device sends 802.11 management frame including proper reason/status code for situation that caused the frame, other may send frame with "unspecified" reason/status code. Therefore reason/status code should only be considered informational.

As 802.11 standards evolve, RouterOS may miss textual descriptions for reason/status codes that some devices use. In such case numeric value should be used to lookup meaning in 802.11 standards.

In order to properly interpret reason/status code, good understanding of 802.11 group standards is necessary. Most of the textual descriptions are self-explaining. Explanation for some of most commonly seen reson/status codes follows.

**class 2 frame received (6)** - device received "class 2" frame (association/reassociation management frame) before completing 802.11 authentication process;

**class 3 frame received (7)** - device received "class 3" frame (data frame) before completing association process;

# Wireless FAQ

## Settings

**Why I can't connect to MikroTik 802.11n AP with Apple Mac devices?**

This problem is only seen on Mac devices based on Broadcom wireless chipsets. In order to connect with such wireless device to MikroTik 802.11n AP make sure that you don't use 'short' preamble-mode. Use 'long' or 'both' preamble-mode and Mac wireless devices will be able to connect.

**By changing some wireless settings the wireless link works unstable**

Sometimes when you change some wireless setting for tuning the links you got so far that the link isn't establishing any more or works unstable and you don't remember what settings you had in the beginning. In this case, you can use the _reset-configuration_ command in the wireless menu - it will reset the all the wireless settings for the specific wireless interface and you will be able to configure the interface from the start. Note that executing this command also disables the interface, so please be careful not to execute this command if you are configuring router remotely using that wireless link that you want to reset the configuration.

**What are wireless retransmits and where to check them?**

Wireless retransmission occur when an interface sends out a frame and doesn't receive back an acknowledgment (ACK), causing it to try sending the frame again until an acknowledgment is received or the maximum allowed retransmission count for a packet is reached. Wireless retransmits increase the latency and lower the throughput of a wireless link. The number of retransmissions taking place can be determined by subtracting the value of the **frames** parameter from the value of the 'hw-frames **parameter for a given entry in the registration table. Some number of retransmissions is to be expected, but if the value of** frames **exceeds the value of** frames **multiple times, there is an issue with the wireless link that requires troubleshooting.**

**Can I compare frames with hw-frames also on Nstreme links?**

The **frames** counts only those which contain actual data. In the case of Nstreme, only the ACK can be transmitted in a single frame, if there is no other data to send. These ACK frames will not be added to the **frames** count, but they will appear at **hw-frames**. If there is traffic on both directions at maximum speed (eg. there will be no only-ack frames), then you can't compare **frames** to **hw-frames** as in case of regular wireless links.

**What TX-power values can I use?**

The tx-power default setting is the maximum tx-power that the card can use and is taken from the cards eeprom. If you want to use larger tx-power values, you are able to set them, but **do it at your own risk**, as it will probably damage your card eventually! Usually, one should use this parameter only to reduce the tx-power.

In general, tx-power controlling properties should be left at the default settings. Changing the default setting may help with some cards in some situations, but without testing, the most common result is the degradation of range and throughput. Some of the problems that may occur are:

-   overheating of the power amplifier chip and the card which will cause lower efficiency and more data errors;
-   overdriving the amplifier which will cause more data errors;
-   excessive power usage for the card and this may overload the 3.3V power supply of the board that the card is located on resulting in voltage drop and reboot or excessive temperatures for the board.

**What TX-power-mode is the best?**

_TX-power-mode_ tells the wireless card which tx-power values should be used. By default, this setting is set to _default_.

-   **default** means that the card will use the tx-power values from the cards eeprom and will ignore the setting what is specified by the user in the _tx-power_ field.
-   **card-rates** means that for different data rates the tx-power is calculated according to the cards transmit power algorithm from the cards eeprom and as an argument it takes _tx-power_ value specified by the user.
-   **all-rates-fixed** means that that the card will use one tx-power value for all data rates which is specified by the user in _tx-power_ field.

Note that it is not recommended to use 'all-rates-fixed' mode as the wireless card tx-power for the higher data rates is lower and by forcing to use the fixed tx-power rates also for the higher data rates might result in the same problems like in the previous question about tx-power setting. In the case of MikroTik Radio devices, the power will not be higher than the power written in the EEPROM. For most of the cases if you want to change the tx-power settings it is recommended to use the _tx-power-mode=card-rates_ and it is recommended to lower and not to raise tx-power. In case of AR9300 and newer Atheros wireless chipsets "tx-power-mode=all-rate-fixed" is the only option as "card-rates" option isn't working on those chipsets.

**What is CCQ and how are the values determined?**

Client Connection Quality (CCQ) is a value in percent that shows how effective the bandwidth is used regarding the theoretically maximum available bandwidth. CCQ is weighted average of values Tmin/Treal, that get calculated for every transmitted frame, where Tmin is time it would take to transmit given frame at highest rate with no retries and Treal is time it took to transmit frame in real life (taking into account necessary retries it took to transmit frame and transmit rate).

**What is hw-retries setting?**

Number of times sending frame is retried without considering it a transmission failure. The data rate is decreased upon failure and frame is sent again. Three sequential failures on lowest supported rate suspend transmission to this destination for the duration of _on-fail-retry-time_. After that, the frame is sent again. The frame is being retransmitted until transmission success, or until the client is disconnected after _disconnect-timeout_. The frame can be discarded during this time if _frame-lifetime_ is exceeded. In case of Nstreme "on-fail-retry-time", "disconnect-timeout" and "frame-lifetime" settings are not used. So after three sequential failures on the lowest supported rate, the wireless link is disconnected with "extensive data loss" message.

**What is disconnect-timeout setting?**

This interval is measured from the third sending failure on the lowest data rate. At this point 3 \* (_hw-retries_ + 1) frame transmits on the lowest data rate had failed. During _disconnect-timeout_ packet transmission will be retried with _on-fail-retry-time_ interval. If no frame can be transmitted successfully during _disconnect-timeout_, the connection is closed, and this event is logged as "extensive data loss". Successful frame transmission resets this timer.

**What is adaptive-noise-immunity setting?**

Adaptive Noise Immunity (ANI) adjusts various receiver parameters dynamically to minimize interference and noise effect on the signal quality. This setting is added in the wireless driver for Atheros AR5212 and newer chipset cards

**How does wireless device measure signal strength, when access-list or connect-list are used ?**

The reported signal level is exponentially weighted moving average with a smoothing factor of 50%.

**What error correction methods are supported in the RouterOS wireless?**

ARQ method is supported in nstreme protocols. Regular 802.11 standard does not include ARQ - retransmission of corrupt frames is based on acknowledgment protocol. RouterOS supports forward error correction coding (convolutional coding) with coding rates: 1/2, 2/3, or 3/4.

**Configuring RouterOS device for 160MHz use**

If the RouterOS device supports 4x4 transmission, additionally to setting 160MHz channel width, make sure to set "rate-set=default" on the wireless interface so all streams are available

If the client does not support Extended NSS and can only perform 2x2 transmission, set "vht-supported-mcs=mcs0-9,mcs0-9,none"

## Setups

**Will an amplifier improve the speed on my link?**

It depends on your signal quality and noise. Remember that you can probably get a better link with low output power setting, and a good antenna. An amplifier increases the noise and will only cause problems with the link.

The amplifier gets a boost on both the transmitted **and** received signal. Thus, in "silent" areas, where you are alone or with very few "noise" or "competition", you might get excellent results. On the other side, in crowded areas, with lots of wireless activity, you will also increase signal received from every other competitor or noise source, which may dramatically lower the overall quality of the link. Also, take in account the EIRP to see if your link remains in legal limits.

You could also get a better signal on "11b only" radios, which see most of 802.11g as "noise", thus filtering better the usable signal.

**How to fine-tune the wireless link with hw-retries?**

You should understand that for 802.11 devices there is a really limited amount of information (or "feedback" from the environment) that devices can use to tune their behavior:

-   signal strength, which could be used to figure out best transmit rate knowing receiver sensitivity. Sill this is not reliable taking into account that sensitivity for different receivers varies (e.g. changes over time), path conditions are not symmetric (and device can only measure signal strength it receives), etc.
-   by receiving/not receiving acknowledgment for frame sent.

Taking into account that using signal strength is not reliable, 802.11 devices are essentially left with only one "feedback" to tune its operation - success/failure of transmission. When transmission fails (ACK not received in time), there is no way how sender can figure out why it failed - either because of noise, multipath, direct interference (and whether that disturbed actual data frame or the ACK itself) - frame just did not make it and in general it does not matter "why". All that matters is the packet error rate.

Therefore RouterOS implements an algorithm to try to use medium most efficiently in any environment by using only this limited information, giving users the ability to control how the algorithm works and describing the algorithm. And there are only a few usage guidelines, not a set of values you should use in a particular situation.

In general - the larger _hw-retries_, the better "feedback" device gets about medium ability to deliver frame at particular rate (e.g. if sending frame with rate 54mbps fails 16 times, it is telling you more than if it fails with 2 retries) and the better it can figure out optimal transmit rate, at the expense of latency it can introduce in network - because during all those failing retries, other devices in this channel cannot send. So **bigger** _hw-retries_ can be suggested for ptp backbone links - where it is known that link must be always on. **Less** _hw-retries_ make rate selection adapt faster at the expense of some accuracy (going below 2 is not reasonable in most cases), this can be suggested for ptmp links, where it is normal for links to connect/disconnect and keeping latency down is important.

_on-fail-retry-time_ and _disconnect-timeout_ controls how hard device will try to consider remote party "connected". Larger _disconnect-timeout_ will make the device not "disconnect" other party, even if there are lots of loss at the smallest possible transmission rate. This again is most useful for "weak" links that are known that they "must" be established (e.g. backbone links). In ptmp networks large _disconnect-timeout_ will again increase latency in the network during the time e.g. AP will attempt to send data to some client that has just been disabled (AP will try to do this for the whole _disconnect-timeout_).

_frame-lifetime_ allows to tune for how long AP is attempting to use frame for transmitting before considering that it is not worth delivering it (for example, if sending frame fails at lowest possible rate, _on-fail-retry-time_ timer is enabled, if during this timer _frame-lifetime_ expires, particular frame is dropped and the next transmission attempt will happen with the next frame. Disabled _frame-lifetime_ means that wireless will ensure in order delivery of "all" data frames, no matter how long it takes, "or" will drop the connection if everything fails). This allows optimizing for different types of traffic e.g. for real-time traffic - if the primary use of the wireless network is e.g. voip, then it can be reasonable to limit _frame-lifetime_, because voip tolerates small loss better than high latency.

**Is it possible to use the wireless repeater only with one radio interface?**

This setup it possible by using WDS on the wireless interface which is running in ap-bridge mode. And in newer RouterOS versions it is possible to configure wireless repeater mode.

**Nv2 wireless link disconnects very often**

When Nv2 wireless link experiences disconnections and in log section most of the messages are 'control frame timeout', you can try to lower the transmit output power of the wireless cards if the signal of the link is strong. We suggest using tx-power-mode=card-rates for lowering the tx-power of the wireless card. If the problem continues to try to use a different wireless frequency that might have less interference. If that also didn't help, please contact [support@mikrotik.com](mailto:support@mikrotik.com) with a support output file from the affected AP and the Station which are made after those disconnections.