# Overview

Setting the System's Identity provides a unique identifying name for when the system identifies itself to other routers in the network and when accessing services such as DHCP, Neighbour Discovery, and default wireless SSID. The default system Identity is set to 'MikroTik'.

System Identity has a 64 maximum character length

# Configuration

To set system identity in RouterOS:

[?](https://help.mikrotik.com/docs/display/ROS/Identity#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/system identity </code><code class="ros functions">set </code><code class="ros value">name</code><code class="ros plain">=New_Identity</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@New_Identity] &gt;</code></div></div></td></tr></tbody></table>

  

The current System Identity is always displayed after the logged-in account name and with the print command:

[?](https://help.mikrotik.com/docs/display/ROS/Identity#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@New_Identity] </code><code class="ros constants">/system identity&gt;</code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">name</code><code class="ros constants">: New_Identity</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@New_Identity] </code><code class="ros constants">/system identity&gt;</code></div></div></td></tr></tbody></table>

## SNMP

It is also possible to change the router system identity by SNMP set command:

[?](https://help.mikrotik.com/docs/display/ROS/Identity#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">snmpset -c public -v 1 192.168.0.0 1.3.6.1.2.1.1.5.0 s New_Identity</code></div></div></td></tr></tbody></table>

_snmpset_ \- Linux based SNMP application used for SNMP SET requests to set information on a network entity;

-   _public_ \- router's community name;
-   _192.168.0.0_ \- IP address of the router;
-   _1.3.6.1.2.1.1.5.0_ \- SNMP value for router's identity;