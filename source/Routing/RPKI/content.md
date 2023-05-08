# Overview

RouterOS implements the Resource Public Key Infrastructure (RPKI) to Router Protocol defined in [RFC8210](https://tools.ietf.org/html/rfc8210). RTR is a very lightweight low memory footprint protocol, to reliably get prefix validation data from RPKI validators.  
More information on RPKI and how to set up validators can be found in the RIPE blog:  
[https://blog.apnic.net/2019/10/28/how-to-installing-an-rpki-validator/](https://blog.apnic.net/2019/10/28/how-to-installing-an-rpki-validator/)

# Basic Example

Let's consider that we have our own RTR server on our network with IP address 192.168.1.1:

[?](https://help.mikrotik.com/docs/display/ROS/RPKI#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/routing/bgp/rpki</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">group</code><code class="ros plain">=myRpkiGroup</code> <code class="ros value">address</code><code class="ros plain">=192.168.1.1</code> <code class="ros value">port</code><code class="ros plain">=8282</code> <code class="ros value">refresh-interval</code><code class="ros plain">=20</code></div></div></td></tr></tbody></table>

If the connection is established and a database from the validator is received, we can check prefix validity:

[?](https://help.mikrotik.com/docs/display/ROS/RPKI#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="text plain">[admin@rack1_b33_CCR1036] /routing&gt; rpki-check group=myRpkiGroup prfx=70.132.18.0/24 origin-as=16509</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="text spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="text plain">valid</code></div></div></td></tr></tbody></table>

Now the cached database can be used by routing filters to accept/reject prefixes based on RPKI validity. At first, we need to set up a filter rule which defines against which RPKI group performs the verification. After that filters are ready to match the status from the RPKI database. Status can have one of three values:

-   **valid** - database has a record and origin AS is valid.
-   **invalid** - the database has a record and origin AS is invalid.
-   **unknown** - database does not have information of prefix and origin AS.
-   **unverified** - set when none of the RPKI sessions of the RPKI group has synced database. This value can be used to handle the total failure of the RPKI.

  

[?](https://help.mikrotik.com/docs/display/ROS/RPKI#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/routing/filter/rule</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=bgp_in</code> <code class="ros value">rule</code><code class="ros plain">=</code><code class="ros string">"rpki-verify myRpkiGroup"</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=bgp_in</code> <code class="ros value">rule</code><code class="ros plain">=</code><code class="ros string">"if (rpki invalid) { reject } else { accept }"</code></div></div></td></tr></tbody></table>

# Configuration Options

`**Sub-Menu:** /routing/rpki`

  

| 
Property

 | 

Description

 |
| --- | --- |
| 

Property

 | 

Description

 |
| --- | --- |
| **address** (_IPv4/6_) mandatory | Address of the RTR server |
| **disabled**(_yes | no_; Default: **no**) | Whether the item is ignored. |
| **expire-interval** (_integer \[600..172800\]_; Default: 7200) | Time interval \[s\] polled data is considered valid in the absence of a valid subsequent update from the validator. |
| **group** (_string_) mandatory | Name of the group a database is assigned to. |
| **port** (_integer \[0..65535\]_; Default: 323) | Connection port number |
| **preference** (_integer \[0..4294967295\]_; Default: 0) | 

If there are multiple RTR sources, the preference number indicates a more preferred one. A lesser number is preferred.

 |
| **refresh-interval** (_integer \[1..86400\]_; Default: 3600) | Time interval \[s\] to poll the newest data from the validator. |
| **retry-interval** (_integer \[1..7200\]_; Default: 600) | Time Interval \[s\] to retry after the failed data poll from the validator. |
| **vrf**(_name_; Default: main) | Name of the VRF table used to bind the connection to. |