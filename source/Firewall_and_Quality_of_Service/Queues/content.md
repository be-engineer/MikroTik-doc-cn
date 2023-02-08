# Overview

A queue is a collection of data packets collectively waiting to be transmitted by a network device using a pre-defined structure methodology. Queuing works almost on the same methodology used at banks or supermarkets, where the customer is treated according to its arrival.

Queues are used to:

- limit data rate for certain IP addresses, subnets, protocols, ports, etc.;
- limit peer-to-peer traffic;
- packet prioritization;
- configure traffic bursts for traffic acceleration;
- apply different time-based limits;
- share available traffic among users equally, or depending on the load of the channel

Queue implementation in MikroTik RouterOS is based on Hierarchical Token Bucket (HTB). HTB allows to the creation of a hierarchical queue structure and determines relations between queues. These hierarchical structures can be attached at two different places, the [Packet Flow diagram](https://help.mikrotik.com/docs/display/ROS/Packet+Flow+in+RouterOS) illustrate both _input_ and _postrouting_ chains.

There are two different ways how to configure queues in RouterOS:

- **/queue simple** menu - designed to ease configuration of simple, every day queuing tasks (such as single client upload/download limitation, p2p traffic limitation, etc.).
- **/queue tree** menu - for implementing advanced queuing tasks (such as global prioritization policy, user group limitations). Requires marked packet flows from [**/ip firewall mangle**](https://help.mikrotik.com/docs/display/ROS/Basic+Concepts) facility.

## Rate limitation principles

  

Rate limiting is used to control the rate of traffic flow sent or received on a network interface. Traffic which rate that is less than or equal to the specified rate is sent, whereas traffic that exceeds the rate is dropped or delayed.

Rate limiting can be performed in two ways:

1.  discard all packets that exceed rate limit – _**rate-limiting (dropper or shaper)**_ _(100% rate limiter when queue-size=0)_
2.  delay packets that exceed specific rate limit in the queue and transmit its when it is possible – _**rate equalizing (scheduler)**_ (100% rate equalizing when _queue-size=unlimited_)

Next figure explains the difference between _rate limiting_ and rate _equalizing_:

![](https://help.mikrotik.com/docs/download/attachments/328088/Image8001.png?version=2&modificationDate=1615377025309&api=v2)

As you can see in the first case all traffic exceeds a specific rate and is dropped. In another case, traffic exceeds a specific rate and is delayed in the queue and transmitted later when it is possible, but note that the packet can be delayed only until the queue is not full. If there is no more space in the queue buffer, packets are dropped.

For each queue we can define two rate limits:

- **CIR** (Committed Information Rate) – (**limit-at** in RouterOS) worst-case scenario, the flow will get this amount of traffic rate regardless of other traffic flows. At any given time, the bandwidth should not fall below this committed rate.
- **MIR** (Maximum Information Rate) – (**max-limit** in RouterOS) best-case scenario, the maximum available data rate for flow, if there is free any part of the bandwidth.

## Simple Queue

  

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/queue simple</code></div></div></td></tr></tbody></table>

A simple queue is a plain way how to limit traffic for a particular target. Also, you can use simple queues to build advanced QoS applications. They have useful integrated features:

- peer-to-peer traffic queuing;
- applying queue rules on chosen time intervals;
- prioritization;
- using multiple packet marks from _/ip firewall mangle_
- traffic shaping (scheduling) of bidirectional traffic (one limit for the total of upload + download)

Simple queues have a strict order - each packet must go through every queue until it reaches one queue which conditions fit packet parameters or until the end of the queues list is reached. For example, In the case of 1000 queues, a packet for the last queue will need to proceed through 999 queues before it will reach the destination. 

### Configuration example

In the following example, we have one SOHO device with two connected units PC and Server.

![](https://help.mikrotik.com/docs/download/attachments/328088/Simple%20Queue.jpg?version=1&modificationDate=1571740133102&api=v2)

We have a 15 Mbps connection available from ISP in this case. We want to be sure the server receives enough traffic, so we will configure a simple queue with a _limit-at_ parameter to guarantee a server to receive 5Mbps:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/queue simple</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">limit-at</code><code class="ros plain">=5M/5M</code> <code class="ros value">max-limit</code><code class="ros plain">=15M/15M</code> <code class="ros value">name</code><code class="ros plain">=queue1</code> <code class="ros value">target</code><code class="ros plain">=192.168.88.251/32</code></div></div></td></tr></tbody></table>

That is all. The server will get 5 Mbps of traffic rate regardless of other traffic flows. If you are using the default configuration, be sure the FastTrack rule is disabled for this particular traffic, otherwise, it will bypass Simple Queues and they will not work.

## Queue Tree

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/queue tree</code></div></div></td></tr></tbody></table>

The queue tree creates only a one-directional queue in one of the HTBs. It is also the only way how to add a queue on a separate interface. This way it is possible to ease mangle configuration - you don't need separate marks for download and upload - only the upload will get to the Public interface and only the download will get to a Private interface. The main difference from Simple Queues is that the Queue tree is not ordered - all traffic passes it together.

### Configuration example

In the following example, we will mark all the packets coming from preconfigured _in-interface-list=LAN_ and will limit the traffic with a queue tree based on these packet marks.

Let\`s create a firewall address-list:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/ip firewall address-list</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=www.youtube.com</code> <code class="ros value">list</code><code class="ros plain">=Youtube</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; ip firewall address-list print</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, D - dynamic</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments">#&nbsp;&nbsp; LIST&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ADDRESS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; CREATION-TIME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TIMEOUT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;&nbsp; Youtube&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; www.youtube.com&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; oct</code><code class="ros constants">/17/2019 14:47:11</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1 D ;;; www.youtube.com</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">Youtube&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 216.58.211.14&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; oct</code><code class="ros constants">/17/2019 14:47:11</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">2 D ;;; www.youtube.com</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">Youtube&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 216.58.207.238&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; oct</code><code class="ros constants">/17/2019 14:47:11</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">3 D ;;; www.youtube.com</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">Youtube&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 216.58.207.206&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; oct</code><code class="ros constants">/17/2019 14:47:11</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">4 D ;;; www.youtube.com</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">Youtube&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 172.217.21.174&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; oct</code><code class="ros constants">/17/2019 14:47:11</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">5 D ;;; www.youtube.com</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">Youtube&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 216.58.211.142&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; oct</code><code class="ros constants">/17/2019 14:47:11</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">6 D ;;; www.youtube.com</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">Youtube&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 172.217.22.174&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; oct</code><code class="ros constants">/17/2019 14:47:21</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">7 D ;;; www.youtube.com</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">Youtube&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 172.217.21.142&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; oct</code><code class="ros constants">/17/2019 14:52:21</code></div></div></td></tr></tbody></table>

Mark packets with firewall mangle facility:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/ip firewall mangle</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">action</code><code class="ros plain">=mark-packet</code> <code class="ros value">chain</code><code class="ros plain">=forward</code> <code class="ros value">dst-address-list</code><code class="ros plain">=Youtube</code> <code class="ros value">in-interface-list</code><code class="ros plain">=LAN</code> <code class="ros value">new-packet-mark</code><code class="ros plain">=pmark-Youtube</code> <code class="ros value">passthrough</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Configure the queue tree based on previously marked packets:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/queue tree</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">max-limit</code><code class="ros plain">=5M</code> <code class="ros value">name</code><code class="ros plain">=Limiting-Youtube</code> <code class="ros value">packet-mark</code><code class="ros plain">=pmark-Youtube</code> <code class="ros value">parent</code><code class="ros plain">=global</code></div></div></td></tr></tbody></table>

Check Queue tree stats to be sure traffic is matched:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; queue tree </code><code class="ros functions">print </code><code class="ros plain">stats</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - invalid</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;&nbsp; </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"Limiting-Youtube"</code> <code class="ros value">parent</code><code class="ros plain">=global</code> <code class="ros value">packet-mark</code><code class="ros plain">=pmark-Youtube</code> <code class="ros value">rate</code><code class="ros plain">=0</code> <code class="ros value">packet-rate</code><code class="ros plain">=0</code> <code class="ros value">queued-bytes</code><code class="ros plain">=0</code> <code class="ros value">queued-packets</code><code class="ros plain">=0</code> <code class="ros value">bytes</code><code class="ros plain">=67887</code> <code class="ros value">packets</code><code class="ros plain">=355</code> <code class="ros value">dropped</code><code class="ros plain">=0</code></div></div></td></tr></tbody></table>

  

## Queue Types

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/queue type</code></div></div></td></tr></tbody></table>

This sub-menu list by default created queue types and allows to add of new user-specific ones.

By default RouterOS creates the following pre-defined queue types:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/queue type </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: * - default</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0 * </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"default"</code> <code class="ros value">kind</code><code class="ros plain">=pfifo</code> <code class="ros value">pfifo-limit</code><code class="ros plain">=50</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1 * </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"ethernet-default"</code> <code class="ros value">kind</code><code class="ros plain">=pfifo</code> <code class="ros value">pfifo-limit</code><code class="ros plain">=50</code></div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">2 * </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"wireless-default"</code> <code class="ros value">kind</code><code class="ros plain">=sfq</code> <code class="ros value">sfq-perturb</code><code class="ros plain">=5</code> <code class="ros value">sfq-allot</code><code class="ros plain">=1514</code></div><div class="line number8 index7 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">3 * </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"synchronous-default"</code> <code class="ros value">kind</code><code class="ros plain">=red</code> <code class="ros value">red-limit</code><code class="ros plain">=60</code> <code class="ros value">red-min-threshold</code><code class="ros plain">=10</code> <code class="ros value">red-max-threshold</code><code class="ros plain">=50</code> <code class="ros value">red-burst</code><code class="ros plain">=20</code> <code class="ros value">red-avg-packet</code><code class="ros plain">=1000</code></div><div class="line number10 index9 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">4 * </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"hotspot-default"</code> <code class="ros value">kind</code><code class="ros plain">=sfq</code> <code class="ros value">sfq-perturb</code><code class="ros plain">=5</code> <code class="ros value">sfq-allot</code><code class="ros plain">=1514</code></div><div class="line number12 index11 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">5 * </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"pcq-upload-default"</code> <code class="ros value">kind</code><code class="ros plain">=pcq</code> <code class="ros value">pcq-rate</code><code class="ros plain">=0</code> <code class="ros value">pcq-limit</code><code class="ros plain">=50KiB</code> <code class="ros value">pcq-classifier</code><code class="ros plain">=src-address</code> <code class="ros value">pcq-total-limit</code><code class="ros plain">=2000KiB</code> <code class="ros value">pcq-burst-rate</code><code class="ros plain">=0</code> <code class="ros value">pcq-burst-threshold</code><code class="ros plain">=0</code> <code class="ros value">pcq-burst-time</code><code class="ros plain">=10s</code> <code class="ros value">pcq-src-address-mask</code><code class="ros plain">=32</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">pcq-dst-address-mask</code><code class="ros plain">=32</code> <code class="ros value">pcq-src-address6-mask</code><code class="ros plain">=128</code> <code class="ros value">pcq-dst-address6-mask</code><code class="ros plain">=128</code></div><div class="line number15 index14 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">6 * </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"pcq-download-default"</code> <code class="ros value">kind</code><code class="ros plain">=pcq</code> <code class="ros value">pcq-rate</code><code class="ros plain">=0</code> <code class="ros value">pcq-limit</code><code class="ros plain">=50KiB</code> <code class="ros value">pcq-classifier</code><code class="ros plain">=dst-address</code> <code class="ros value">pcq-total-limit</code><code class="ros plain">=2000KiB</code> <code class="ros value">pcq-burst-rate</code><code class="ros plain">=0</code> <code class="ros value">pcq-burst-threshold</code><code class="ros plain">=0</code> <code class="ros value">pcq-burst-time</code><code class="ros plain">=10s</code> <code class="ros value">pcq-src-address-mask</code><code class="ros plain">=32</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">pcq-dst-address-mask</code><code class="ros plain">=32</code> <code class="ros value">pcq-src-address6-mask</code><code class="ros plain">=128</code> <code class="ros value">pcq-dst-address6-mask</code><code class="ros plain">=128</code></div><div class="line number18 index17 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">7 * </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"only-hardware-queue"</code> <code class="ros value">kind</code><code class="ros plain">=none</code></div><div class="line number20 index19 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number21 index20 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">8 * </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"multi-queue-ethernet-default"</code> <code class="ros value">kind</code><code class="ros plain">=mq-pfifo</code> <code class="ros value">mq-pfifo-limit</code><code class="ros plain">=50</code></div><div class="line number22 index21 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">9 * </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"default-small"</code> <code class="ros value">kind</code><code class="ros plain">=pfifo</code> <code class="ros value">pfifo-limit</code><code class="ros plain">=10</code></div></div></td></tr></tbody></table>

All RouterBOARDS have default queue type "**only-hardware-queue"** with "kind=none". "only-hardware-queue" leaves interface with only hardware transmit descriptor ring buffer which acts as a queue in itself. Usually, at least 100 packets can be queued for transmit in transmit descriptor ring buffer. Transmit descriptor ring buffer size and the number of packets that can be queued in it varies for different types of ethernet MACs. Having no software queue is especially beneficial on SMP systems because it removes the requirement to synchronize access to it from different CPUs/cores which is resource-intensive. Having the possibility to set "only-hardware-queue" requires support in an ethernet driver so it is available only for some ethernet interfaces mostly found on RouterBOARDs.

A **"multi-queue-ethernet-default"** can be beneficial on SMP systems with ethernet interfaces that have support for multiple transmit queues and have a Linux driver support for multiple transmit queues. By having one software queue for each hardware queue there might be less time spent on synchronizing access to them.

Improvement from only-hardware-queue and multi-queue-ethernet-default is present only when there is no "/queue tree" entry with a particular interface as a parent.

### Kinds

Queue kinds are packet processing algorithms. Kind describe which packet will be transmitted next in the line. RouterOS supports the following Queueing kinds:

- FIFO (BFIFO, PFIFO, MQ PFIFO)
- RED
- SFQ
- PCQ

#### FIFO

These kinds are based on the FIFO algorithm (First-In-First-Out). The difference between **PFIFO** and **BFIFO** is that one is measured in packets and the other one in bytes. These queues use **pfifo-limit** and **bfifo-limit** parameters.

Every packet that cannot be enqueued (if the queue is full), is dropped. Large queue sizes can increase latency but utilize the channel better.

**MQ-PFIFO** is _pfifo_ with support for multiple transmit queues. This queue is beneficial on SMP systems with ethernet interfaces that have support for multiple transmit queues and have a Linux driver support for multiple transmit queues (mostly on x86 platforms). This kind uses the **mq-pfifo-limit** parameter.

#### RED

Random Early Drop is a queuing mechanism that tries to avoid network congestion by controlling the average queue size. The average queue size is compared to two thresholds: a minimum (min<sub>th</sub>) and maximum (max<sub>th</sub>) threshold. If the average queue size (avg<sub>q</sub>) is less than the minimum threshold, no packets are dropped. When the average queue size is greater than the maximum threshold, all incoming packets are dropped. But if the average queue size is between the minimum and maximum thresholds packets are randomly dropped with probability P<sub>d</sub> where probability is exact a function of the average queue size: P<sub>d</sub> = P<sub>max</sub>(avg<sub>q</sub> – min<sub>th</sub>)/ (max<sub>th</sub> - min<sub>th</sub>). If the average queue grows, the probability of dropping incoming packets grows too. P<sub>max</sub> - ratio, which can adjust the packet discarding probability abruptness, (the simplest case P<sub>max</sub> can be equal to one. The 8.2 diagram shows the packet drop probability in the RED algorithm.

![](https://help.mikrotik.com/docs/download/attachments/328088/Image8002.png?version=2&modificationDate=1615377059686&api=v2)

#### SFQ

Stochastic Fairness Queuing (SFQ) is ensured by hashing and round-robin algorithms. SFQ is called "Stochastic" because it does not really allocate a queue for each flow, it has an algorithm that divides traffic over a limited number of queues (1024) using a hashing algorithm.

Traffic flow may be uniquely identified by 4 options (_src-address, dst-address, src-port,_ and _dst-port_), so these parameters are used by the SFQ hashing algorithm to classify packets into one of 1024 possible sub-streams. Then round-robin algorithm will start to distribute available bandwidth to all sub-streams, on each round giving **sfq-allot** bytes of traffic. The whole SFQ queue can contain 128 packets and there are 1024 sub-streams available. The 8.3 diagram shows the SFQ operation:

![](https://help.mikrotik.com/docs/download/attachments/328088/Image8003.png?version=2&modificationDate=1615377078449&api=v2)

#### PCQ

PCQ algorithm is very simple - at first, it uses selected classifiers to distinguish one sub-stream from another, then applies individual FIFO queue size and limitation on every sub-stream, then groups all sub-streams together and applies global queue size and limitation.

PCQ parameters:

- **pcq-classifier** (dst-address | dst-port | src-address | src-port; default: "") : selection of sub-stream identifiers
- **pcq-rate** (number): maximal available data rate of each sub-steam
- **pcq-limit** (number): queue size of single sub-stream (in KiB)
- **pcq-total-limit** (number): maximum amount of queued data in all sub-streams (in KiB)

 It is possible to assign a speed limitation to sub-streams with the **pcq-rate** option. If "pcq-rate=0" sub-streams will divide available traffic equally.

![](https://help.mikrotik.com/docs/download/attachments/328088/PCQ_Alg.png?version=3&modificationDate=1615377092954&api=v2)

For example, instead of having 100 queues with 1000kbps limitation for download, we can have one PCQ queue with 100 sub-streams

PCQ has burst implementation identical to Simple Queues and Queue Tree:

- **pcq-burst-rate** (number): maximal upload/download data rate which can be reached while the burst for substream is allowed
- **pcq-burst-threshold** (number): this is the value of burst on/off switch
- **pcq-burst-time** (time): a period of time (in seconds) over which the average data rate is calculated. (This is NOT the time of actual burst)

PCQ also allows using different size IPv4 and IPv6 networks as sub-stream identifiers. Before it was locked to a single IP address. This is done mainly for IPv6 as customers from an ISP point of view will be represented by /64 network, but devices in customers network will be /128. PCQ can be used for both of these scenarios and more. PCQ parameters:

- **pcq-dst-address-mask** (number): the size of the IPv4 network that will be used as a dst-address sub-stream identifier
- **pcq-src-address-mask** (number): the size of the IPv4 network that will be used as an src-address sub-stream identifier
- **pcq-dst-address6-mask** (number): the size of the IPV6 network that will be used as a dst-address sub-stream identifier
- **pcq-src-address6-mask** (number): the size of the IPV6 network that will be used as an src-address sub-stream identifier

  

The following queue kinds CoDel, FQ-Codel, and CAKE available since RouterOS version 7.1beta3.

#### CoDel

CoDel (Controlled-Delay Active Queue Management) algorithm uses the local minimum queue as a measure of the persistent queue, similarly, it uses a minimum delay parameter as a measure of the standing queue delay. Queue size is calculated using packet residence time in the queue.

**Properties**

| 
**Property**

 | 

**Description**

 |     |
 | --- |  |
 |     |

**Property**

 | 

**Description**

 |                                      |
 | ------------------------------------ |  |
 | **codel-ce-threshold** (_default_: ) |

Marks packets above a configured threshold with ECN.

 |
| **codel-ecn** (_default_: **no**) | 

An option is used to mark packets instead of dropping them.

 |
| **codel-interval** (_default_: **100ms**) | 

Interval should be set on the order of the worst-case RTT through the bottleneck giving endpoints sufficient time to react.

 |
| **codel-limit** (_default_: **1000**) | Queue limit, when the limit is reached, incoming packets are dropped. |
| **codel-target** (_default_: **5ms**) | 

Represents an acceptable minimum persistent queue delay.

 |

#### FQ-Codel

CoDel - Fair Queuing (FQ) with Controlled Delay (CoDel) uses a randomly determined model to classify incoming packets into different flows and is used to provide a fair share of the bandwidth to all the flows using the queue. Each flow is managed using CoDel queuing discipline which internally uses a FIFO algorithm.

**Properties**

| 
**Property**

 | 

**Description**

 |     |
 | --- |  |
 |     |

**Property**

 | 

**Description**

 |                                         |
 | --------------------------------------- | ----------------------------------------------------------- |
 | **fq-codel-ce-threshold** (_default_: ) | Marks packets above a configured threshold with ECN.        |
 | **fq-codel-ecn** (_default_: **yes**)   | An option is used to mark packets instead of dropping them. |
 | **fq-codel-flows** (default: **1024**)  |

A number of flows into which the incoming packets are classified.

 |
| **fq-codel-interval** (_default_: **100ms**) | Interval should be set on the order of the worst-case RTT through the bottleneck giving endpoints sufficient time to react. |
| **fq-codel-limit** (_default_: **10240**) | Queue limit, when the limit is reached, incoming packets are dropped. |
| **fq-codel-memlimit** (default: **32.0MiB**) | 

A total number of bytes that can be queued in this FQ-CoDel instance. Will be enforced from the _fq-codel-limit_ parameter.

 |
| **fq-codel-quantum** (_default_: **1514**) | 

A number of bytes used as 'deficit' in the fair queuing algorithm. Default (1514 bytes) corresponds to the Ethernet MTU plus the hardware header length of 14 bytes.

 |
| **fq-codel-target** (_default_: **5ms**) | Represents an acceptable minimum persistent queue delay. |

#### CAKE

CAKE - Common Applications Kept Enhanced (CAKE) implemented as a _queue discipline_ (qdisc) for the Linux kernel uses COBALT (AQM algorithm combining Codel and BLUE) and a variant of DRR++ for flow isolation. In other words, Cake’s fundamental design goal is user-friendliness. All settings are optional; the default settings are chosen to be practical in most common deployments. In most cases, the configuration requires only a bandwidth parameter to get useful results,

**Properties**

| 
**Property**

 | 

**Description**

 |     |
 | --- |  |
 |     |

**Property**

 | 

**Description**

 |                                            |
 | ------------------------------------------ |  |
 | **cake-ack-filter** _(default:_ **none** ) |
 |                                            |
 | **cake-atm** _(default:_ )                 |

Compensates for ATM cell framing, which is normally found on ADSL links.

 |
| **cake-autorate-ingress** _(yes/no, default:_ ) | 

Automatic capacity estimation based on traffic arriving at this qdisc. This is most likely to be useful with cellular links, which tend to change quality randomly.  The Bandwidth Limit parameter can be used in conjunction to specify an initial estimate. The shaper will periodically be set to a bandwidth slightly below the estimated rate.  This estimator cannot estimate the bandwidth of links downstream of itself.

 |
| **cake-bandwidth** _(default:_ ) | Sets the shaper bandwidth. |
| **cake-diffserv** _(default:_ **diffserv3**) | 

CAKE can divide traffic into "tins" based on the Diffserv field:

- **diffserv4** Provides a general-purpose Diffserv implementation with four tins: Bulk (CS1), 6.25% threshold, generally low priority. Best Effort (general), 100% threshold. Video (AF4x, AF3x, CS3, AF2x, CS2, TOS4, TOS1), 50% threshold. Voice (CS7, CS6, EF, VA, CS5, CS4), 25% threshold.
    
- **diffserv3** (default) Provides a simple, general-purpose Diffserv implementation with three tins: Bulk (CS1), 6.25% threshold, generally low priority. Best Effort (general), 100% threshold. Voice (CS7, CS6, EF, VA, TOS4), 25% threshold, reduced Codel interval.
    

 |
| **cake-flowmode** _(dsthost/dual-dsthost/dual-srchost/flowblind/flows/hosts/srchost/triple-isolate, default:_ **triple-isolate**) | 

- **flowblind** - Disables flow isolation; all traffic passes through a single queue for each tin.
- **srchost** - Flows are defined only by source address. 
- **dsthost** Flows are defined only by destination address. 
- **hosts** - Flows are defined by source-destination host pairs. This is host isolation, rather than flow isolation.
- **flows** - Flows are defined by the entire 5-tuple of source address, a destination address, transport protocol, source port,and destination port. This is the type of flow isolation performed by SFQ and fq\_codel.
- **dual-srchost** Flows are defined by the 5-tuple, and fairness is applied first over source addresses, then over individual flows. Good for use on egress traffic from a LAN to the internet, where it'll prevent anyone LAN host from monopolizing the uplink, regardless of the number of flows they use.
- **dual-dsthost** Flows are defined by the 5-tuple, and fairness is applied first over destination addresses, then over individual flows. Good for use on ingress traffic to a LAN from the internet, where it'll prevent anyone LAN host from monopolizing the downlink, regardless of the number of flows they use.
- **triple-isolate** \- Flows are defined by the 5-tuple, and fairness is applied over source \*and\* destination addresses intelligently (ie. not merely by host-pairs), and also over individual flows.
- **nat** Instructs Cake to perform a NAT lookup before applying flow- isolation rules, to determine the true addresses and port numbers of the packet, to improve fairness between hosts "inside" the NAT. This has no practical effect in "flowblind" or "flows" modes, or if NAT is performed on a different host.
- **nonat** (default) The cake will not perform a NAT lookup. Flow isolation will be performed using the addresses and port numbers directly visible to the interface Cake is attached to.

 |
| **cake-memlimit** _(default:_ ) | 

Limit the memory consumed by Cake to LIMIT bytes. By default, the limit is calculated based on the bandwidth and RTT settings.

 |
| **cake-mpu** _( -64 ... 256, default:_ ) | 

Rounds each packet (including overhead) up to a minimum length BYTES. 

 |
| **cake-nat** _(default:_ **no)** | 

Instructs Cake to perform a NAT lookup before applying a flow-isolation rule.

 |
| **cake-overhead** _( -64 ... 256, default:_ ) | 

Adds BYTES to the size of each packet. BYTES may be negative.

 |
| **cake-overhead-scheme** _(default:_ ) |   
 |
| **cake-rtt** _(default:_ **100ms** ) | 

Manually specify an RTT. Default 100ms is suitable for most Internet traffic.

 |
| **cake-rtt-scheme** _(datacentre/internet/interplanetary/lan/metro/none/oceanic/regional/satellite, default:_ ) | 

- **datacentre** - For extremely high-performance 10GigE+ networks only. Equivalent to **RTT 100us.**
- **lan** - For pure Ethernet (not Wi-Fi) networks, at home or in the office. Don't use this when shaping for an Internet access link. Equivalent to **RTT 1ms.**
- **metro** - For traffic mostly within a single city. Equivalent to **RTT** **10ms.** **regional** For traffic mostly within a European-sized country. Equivalent to **RTT 30ms.**
- **internet** (default) This is suitable for most Internet traffic. Equivalent to **RTT 100ms.**
- **oceanic** - For Internet traffic with generally above-average latency, such as that suffered by Australasian residents. Equivalent to **RTT 300ms.**
- **satellite** - For traffic via geostationary satellites. Equivalent to **RTT** **1000ms.**
- **interplanetary** - So named because Jupiter is about 1 light-hour from Earth. Use this to (almost) completely disable AQM actions. Equivalent to **RTT 3600s.**

 |
| **cake-wash** _(default:_ **no** ) | 

Apply the wash option to clear all extra DiffServ (but not ECN bits), after priority queuing has taken place.

 |

## Interface Queue

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/queue interface</code></div></div></td></tr></tbody></table>

Before sending data over an interface, it is processed by the queue. This sub-menu lists all available interfaces in RouterOS and allows to change queue type for a particular interface. The list is generated automatically.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; queue interface print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: INTERFACE, QUEUE, ACTIVE-QUEUE</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros comments"># INTERFACE QUEUE ACTIVE-QUEUE</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">0 ether1 only-hardware-queue only-hardware-queue</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">1 ether2 only-hardware-queue only-hardware-queue</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">2 ether3 only-hardware-queue only-hardware-queue</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">3 ether4 only-hardware-queue only-hardware-queue</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">4 ether5 only-hardware-queue only-hardware-queue</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">5 ether6 only-hardware-queue only-hardware-queue</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">6 ether7 only-hardware-queue only-hardware-queue</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros plain">7 ether8 only-hardware-queue only-hardware-queue</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">8 ether9 only-hardware-queue only-hardware-queue</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros plain">9 ether10 only-hardware-queue only-hardware-queue</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros plain">10 sfp-sfpplus1 only-hardware-queue only-hardware-queue</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros plain">11 wlan1 wireless-default wireless-default</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros plain">12 wlan2 wireless-default wireless-default&nbsp;</code></div></div></td></tr></tbody></table>