MAC server section allows you to configure MAC Telnet Server, MAC WinBox Server and MAC Ping Server on RouterOS device.

MAC Telnet is used to provide access to a router that has no IP address set. It works just like IP telnet. MAC telnet is possible between two MikroTik RouterOS routers only.

MAC Winbox is used to provide Winbox access to the router via MAC address.

MAC Ping is used to allow MAC pings to the router's MAC address.

**MAC-server** settings are included in the "system" package.

## MAC Telnet Server

It is possible to set MAC Telnet access to specific interfaces that are a part of the [interface list](https://help.mikrotik.com/docs/display/ROS/List):

[?](https://help.mikrotik.com/docs/display/ROS/MAC+server#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/tool mac-server </code><code class="ros functions">set </code><code class="ros value">allowed-interface-list</code><code class="ros plain">=listBridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/tool mac-server </code><code class="ros plain">print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">allowed-interface-list</code><code class="ros constants">: listBridge</code></div></div></td></tr></tbody></table>

In the example above, MAC Telnet is configured for the interface list "listBridge" and, as a result, MAC Telnet will only work via the interfaces that are members of the list (you can add multiple interfaces to the list).

To disable MAC Telnet access, issue the command (set "allowed-interface-list" to "none"):

[?](https://help.mikrotik.com/docs/display/ROS/MAC+server#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/tool mac-server </code><code class="ros functions">set </code><code class="ros value">allowed-interface-list</code><code class="ros plain">=none</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/tool mac-server </code><code class="ros plain">print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">allowed-interface-list</code><code class="ros constants">: none</code></div></div></td></tr></tbody></table>

You can check active MAC Telnet sessions (that the device accepted) with the command:

[?](https://help.mikrotik.com/docs/display/ROS/MAC+server#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; tool mac-server sessions print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: INTERFACE, SRC-ADDRESS, UPTIME</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros comments">#&nbsp; INTERFACE&nbsp; SRC-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; UPTIME</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">0&nbsp; ether5&nbsp;&nbsp;&nbsp;&nbsp; 64</code><code class="ros constants">:D1:54:FB:E3:E6&nbsp; 17s</code></div></div></td></tr></tbody></table>

### MAC Telnet Client

When MAC Telnet Server is enabled, you can use another RouterOS device to connect to the server using the mac-telnet client:

[?](https://help.mikrotik.com/docs/display/ROS/MAC+server#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device2] &gt; tool mac-telnet B8</code><code class="ros constants">:69:F4:7F:F2:E7&nbsp;&nbsp;&nbsp;</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Login</code><code class="ros constants">: admin</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Password</code><code class="ros constants">:</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">Trying B8</code><code class="ros constants">:69:F4:7F:F2:E7...</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">Connected to B8</code><code class="ros constants">:69:F4:7F:F2:E7</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">MMM&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; MMM&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; KKK&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TTTTTTTTTTT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; KKK</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">MMMM&nbsp;&nbsp;&nbsp; MMMM&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; KKK&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TTTTTTTTTTT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; KKK</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">MMM MMMM MMM&nbsp; III&nbsp; KKK&nbsp; KKK&nbsp; RRRRRR&nbsp;&nbsp;&nbsp;&nbsp; OOOOOO&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TTT&nbsp;&nbsp;&nbsp;&nbsp; III&nbsp; KKK&nbsp; KKK</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">MMM&nbsp; MM&nbsp; MMM&nbsp; III&nbsp; KKKKK&nbsp;&nbsp;&nbsp;&nbsp; RRR&nbsp; RRR&nbsp; OOO&nbsp; OOO&nbsp;&nbsp;&nbsp;&nbsp; TTT&nbsp;&nbsp;&nbsp;&nbsp; III&nbsp; KKKKK</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">MMM&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; MMM&nbsp; III&nbsp; KKK KKK&nbsp;&nbsp; RRRRRR&nbsp;&nbsp;&nbsp; OOO&nbsp; OOO&nbsp;&nbsp;&nbsp;&nbsp; TTT&nbsp;&nbsp;&nbsp;&nbsp; III&nbsp; KKK KKK</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">MMM&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; MMM&nbsp; III&nbsp; KKK&nbsp; KKK&nbsp; RRR&nbsp; RRR&nbsp;&nbsp; OOOOOO&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TTT&nbsp;&nbsp;&nbsp;&nbsp; III&nbsp; KKK&nbsp; KKK</code></div><div class="line number16 index15 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">MikroTik RouterOS 7.1rc3 (c) 1999-2021&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; https</code><code class="ros constants">://www.mikrotik.com/</code></div><div class="line number18 index17 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros plain">Press F1 </code><code class="ros functions">for </code><code class="ros plain">help</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code>&nbsp;</div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt;</code></div></div></td></tr></tbody></table>

Change the MAC address accordingly (to your setup) and you should get into the server's CLI (as shown in the example above).  

### MAC Scan

Mac scan feature discovers all devices, which support MAC telnet protocol on the given network. The command requires you to select an interface that should be scanned:

[?](https://help.mikrotik.com/docs/display/ROS/MAC+server#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@Sw_Denissm] &gt; tool mac-</code><code class="ros functions">scan </code><code class="ros value">interface</code><code class="ros plain">=all</code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">MAC-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; AGE</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">B8</code><code class="ros constants">:69:F4:7F:F2:E7 192.168.69.1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 26</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">2C</code><code class="ros constants">:C8:1B:FD:F2:C3 192.168.69.3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 56</code></div></div></td></tr></tbody></table>

In the example, above, all interfaces are chosen and the scan will run infinitely unless stopped (by pressing "q").

You can also add a "duration" parameter that will dictate for how long the scan should go on:

[?](https://help.mikrotik.com/docs/display/ROS/MAC+server#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@Sw_Denissm] &gt; tool mac-</code><code class="ros functions">scan </code><code class="ros value">interface</code><code class="ros plain">=all</code> <code class="ros value">duration</code><code class="ros plain">=1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">MAC-ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; AGE</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">B8</code><code class="ros constants">:69:F4:7F:F2:E7 192.168.69.1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 48</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">2C</code><code class="ros constants">:C8:1B:FD:F2:C3 192.168.69.3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 17</code></div></div></td></tr></tbody></table>

In the example above, we set the "duration" parameter to 1 second.

## MAC Winbox Server

Same as with MAC Telnet, it is possible to set MAC Winbox access to specific interfaces that are a part of the [interface list](https://help.mikrotik.com/docs/display/ROS/List):

[?](https://help.mikrotik.com/docs/display/ROS/MAC+server#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; tool mac-server mac-winbox </code><code class="ros functions">set </code><code class="ros value">allowed-interface-list</code><code class="ros plain">=listBridge</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; tool mac-server mac-winbox </code><code class="ros functions">print </code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">allowed-interface-list</code><code class="ros constants">: listBridge</code></div></div></td></tr></tbody></table>

In the example above, MAC Winbox access is configured for the interface list "listBridge" and, as a result, MAC Winbox will only work via the interfaces that are members of the list.

To disable MAC Winbox access, issue the command (set "allowed-interface-list" to "none"):

[?](https://help.mikrotik.com/docs/display/ROS/MAC+server#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; tool mac-server mac-winbox </code><code class="ros functions">set </code><code class="ros value">allowed-interface-list</code><code class="ros plain">=none</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; tool mac-server mac-winbox </code><code class="ros functions">print </code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">allowed-interface-list</code><code class="ros constants">: none</code></div></div></td></tr></tbody></table>

## MAC Ping Server

MAC Ping Server can be either set to be "disabled" or "enabled":

[?](https://help.mikrotik.com/docs/display/ROS/MAC+server#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; tool mac-server </code><code class="ros functions">ping </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">enabled</code><code class="ros constants">: yes</code></div></div></td></tr></tbody></table>

You can enable or disable MAC ping with the help of the commands (**enable=yes** → to enable the feature; **enable=no** → to disable the feature):

[?](https://help.mikrotik.com/docs/display/ROS/MAC+server#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; tool mac-server </code><code class="ros functions">ping </code><code class="ros functions">set </code><code class="ros value">enabled</code><code class="ros plain">=yes</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; tool mac-server </code><code class="ros functions">ping </code><code class="ros functions">set </code><code class="ros value">enabled</code><code class="ros plain">=no</code></div></div></td></tr></tbody></table>

When MAC Ping is enabled, other hosts on the same broadcast domain can use ping tool to ping the mac address. For example, you can issue the following command to check MAC ping results:

[?](https://help.mikrotik.com/docs/display/ROS/MAC+server#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] &gt; </code><code class="ros constants">/</code><code class="ros functions">ping </code><code class="ros plain">00</code><code class="ros constants">:0C:42:72:A1:B0</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">HOST&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; SIZE&nbsp; TTL TIME&nbsp; STATUS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">00</code><code class="ros constants">:0C:42:72:A1:B0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 56&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0ms&nbsp;</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">00</code><code class="ros constants">:0C:42:72:A1:B0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 56&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0ms&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">sent</code><code class="ros plain">=2</code> <code class="ros value">received</code><code class="ros plain">=2</code> <code class="ros value">packet-loss</code><code class="ros plain">=0%</code> <code class="ros value">min-rtt</code><code class="ros plain">=0ms</code> <code class="ros value">avg-rtt</code><code class="ros plain">=0ms</code> <code class="ros value">max-rtt</code><code class="ros plain">=0ms</code></div></div></td></tr></tbody></table>