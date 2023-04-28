# Overview

The Point-to-Point Protocol (PPP) provides a standard method for transporting multi-protocol datagrams over point-to-point links. PPP in RouterOS is based on [RFC 1661 standard.](https://tools.ietf.org/html/rfc1661)

# Introduction

The basic purpose of PPP at this point is to transport Layer-3 packets across a Data Link layer point-to-point link.  Packets between both peers are assumed to deliver in order. 

PPP is comprised of three main components:

1.   A method for encapsulating multi-protocol datagrams.
2.   A Link Control Protocol (LCP) for establishing, configuring, and testing the data-link connection. 
3.  A family of Network Control Protocols (NCPs) for establishing and configuring different network-layer protocols.

Detailed PPP packet processing in RouterOS you can see in the [Packet Flow Diagram](https://help.mikrotik.com/docs/display/ROS/Packet+Flow+in+RouterOS).

## PPP Client

[?](https://help.mikrotik.com/docs/display/ROS/PPP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ppp-client</code></div></div></td></tr></tbody></table>

## PPP Client example

This is an example of how to add a client using an exposed serial port from an LTE modem.

[?](https://help.mikrotik.com/docs/display/ROS/PPP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ppp-client </code><code class="ros functions">add </code><code class="ros value">apn</code><code class="ros plain">=yourapn</code> <code class="ros value">dial-on-demand</code><code class="ros plain">=no</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">port</code><code class="ros plain">=usb2</code></div></div></td></tr></tbody></table>

The dial-on-demand should to be set to 'no' for a continuous connection.

## PPP Server

[?](https://help.mikrotik.com/docs/display/ROS/PPP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface ppp-server</code></div></div></td></tr></tbody></table>