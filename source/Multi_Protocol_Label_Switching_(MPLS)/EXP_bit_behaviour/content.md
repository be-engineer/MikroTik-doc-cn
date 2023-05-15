# Overview

When the MPLS label is attached to the packet, it increases packet length by 32 bits (4 bytes). These 32 bits are broken down as follows:

-   label value itself (20 bits)
-   EXP ("experimental") field (3 bits)
-   time to live field (8 bits)
-   bottom of stack field (1 bit)

The use of "experimental" bits is not specified by MPLS standards, but the most common use is to carry QoS information, similar to 802.1q priority in the VLAN tag. Note that the EXP field is 3 bits only therefore it can carry values from 0 to 7 only, which allows having 8 traffic classes.

# EXP field treatment in RouterOS

When RouterOS receives an MPLS packet, it sets the "ingress priority" value for the packet to that carried inside the top label. Note that "ingress priority" **is not** a field inside packet headers - it can be thought of as an additional mark assigned to a packet while being processed by the router. When RouterOS labels an MPLS packet, it sets EXP bits to "priority" (not "ingress priority"!) assigned to the packet. When RouterOS switches MPLS packet, "ingress priority" is automatically copied to "priority", this way regular MPLS switching communicates priority info over the whole label switched path.

Additional info on "ingress priority" and "priority" handling is also in [WMM and VLAN priority](https://help.mikrotik.com/docs/display/ROS/WMM+and+VLAN+priority).

Therefore what happens to the EXP field depends based on what action is taken on the packet:

-   if the packet is MPLS switched (by popping the label off the packet and pushing on the new one), the EXP field in the new label will be the same as in the received label, because:
    -   RouterOS sets "ingress priority" to EXP bits in the received label
    -   Switching automatically sets "priority" to "ingress priority"
    -   RouterOS labels the packet with a new label and sets its EXP bits to value in "priority".
-   if the packet is MPLS switched by using penultimate-hop-popping (the received label is popped off and no new one is pushed on), the EXP field of received priority stays in the "priority" field of the packet and may be used by some other MAC protocol, e.g. WMM or 802.1q VLAN, for example:
    -   RouterOS sets "ingress priority" to EXP bits in the received label
    -   Switching automatically sets "priority" to "ingress priority"
    -   RouterOS switches the packet to the next hop (without pushing on the label) and that happens over the VLAN interface
    -   VLAN interface sets 802.1q priority in the VLAN header to the "priority" value of the packet.

Note that penultimate-hop-popping can therefore lose QoS information carried over label switched path at the last hop. In cases where this is not desirable, penultimate-hop-popping behavior should be disabled by using the Explicit NULL label instead of the Implicit NULL label for the last hop in the label switched path. Using an Explicit NULL label for the last hop is the default behavior for MPLS TE tunnels.

-   if a packet is supposed to be sent over label switched path (the first label will get pushed on the packet), EXP bits will be set to value in "priority", which in turn can be set up properly using firewall rules or other means (e.g. from DSCP field in IP header)
-   if a packet is received for local processing, "ingress priority" is set to the EXP field of the received packet and can therefore be used to update the DSCP field of the packet or set "priority" from "ingress priority" using firewall rules