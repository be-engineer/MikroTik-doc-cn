# Overview

MPLS stands for MultiProtocol Label Switching. It kind of replaces IP routing - packet forwarding decision (outgoing interface and next-hop router) is no longer based on fields in IP header (usually destination address) and routing table, but on labels that are attached to packet. This approach speeds up the forwarding process because next-hop lookup becomes very simple compared to routing lookup (finding the longest matching prefix).

The efficiency of the forwarding process is the main benefit of MPLS, but it must be taken into account that MPLS forwarding disables the processing of network layer (e.g. IP) headers, therefore no network layer-based actions like NAT and filtering can be applied to MPLS forwarded packets. Any network-layer-based actions should be taken on ingress or egress of MPLS cloud, with the preferred way being ingress - this way, e.g. traffic that is going to be dropped anyway does not travel through the MPLS backbone.

In the simplest form, MPLS can be thought of as improved routing - labels are distributed by means of LDP protocol for routes that are active and a labeled packet takes the same path it would take if it was not labeled. A router that routes unlabeled packets using some route for which it has received a label from the next hop, imposes a label on the packet, and sends it to the next hop - gets MPLS switched further along its path. A router that receives a packet with a label it has assigned to some route changes the packet label with one received from the next hop of a particular route and sends a packet to the next hop. Label switched path ensures delivery of data to the MPLS cloud egress point. Applications of MPLS are based on this basic MPLS concept of label switched paths.

Another way of establishing label switching paths is traffic engineering tunnels (TE tunnels) by means of the RSVP-TE protocol. Traffic engineering tunnels allow explicitly routed LSPs and constraint-based path selection (where constraints are interface properties and available bandwidth).

Taking into account the complexity, new protocols, and applications that MPLS introduces and the differences of concepts that MPLS adds to routed/bridged networks, it is recommended to have an in-depth understanding of MPLS concepts before implementing MPLS in a production network. Some suggested reading material:

-   Multiprotocol Label Switching [http://en.wikipedia.org/wiki/Multiprotocol\_Label\_Switching](http://en.wikipedia.org/wiki/Multiprotocol_Label_Switching)
-   RFC3031 Multiprotocol Label Switching Architecture [http://www.ietf.org/rfc/rfc3031.txt](http://www.ietf.org/rfc/rfc3031.txt)
-   MPLS Fundamentals by Luc De Ghein [http://www.amazon.com/MPLS-Fundamentals-Luc-Ghein/dp/1587051974](http://www.amazon.com/MPLS-Fundamentals-Luc-Ghein/dp/1587051974)

Feature is not supported on SMIPS devices (hAP lite, hAP lite TC and hAP mini).

# Supported Features

Currently, RouterOS supports the following MPLS related features:

-   MPLS switching with penultimate hop popping support
-   static local label bindings for IPv4 and IPv6
-   static remote label bindings for IPv4 and IPv6
-   Label Distribution Protocol (RFC 3036, RFC 5036, and RFC 7552) for IPv4 and IPv6
    -   downstream unsolicited label advertisement
    -   independent label distribution control
    -   liberal label retention
    -   targeted session establishment
    -   optional loop detection
    -   ECMP support
-   Virtual Private Lan Service
    -   VPLS LDP signaling (RFC 4762)
    -   Cisco style static VPLS pseudowires (RFC 4447 FEC type 0x80)
    -   VPLS pseudowire fragmentation and reassembly (RFC 4623)
    -   VPLS MP-BGP based autodiscovery and signaling (RFC 4761)
    -   Cisco VPLS BGP-based auto-discovery (draft-ietf-l2vpn-signaling-08)
    -   support for multiple import/export route-target extended communities for BGP based VPLS (both, RFC 4761 and draft-ietf-l2vpn-signaling-08)
-   RSVP-TE Tunnels
    -   tunnel head-end
    -   explicit paths
    -   OSPF extensions for TE tunnels
    -   CSPF path selection
    -   forwarding of VPLS and MPLS IP VPN traffic on TE tunnels
    -   Ingress TE tunnel rate limit and automatic reserved bandwidth adjustment, see [TE Tunnel Bandwidth Control](https://wiki.mikrotik.com/wiki/TE_tunnel_auto_bandwidth "TE tunnel auto bandwidth")
    -   all tunnel bandwidth settings are specified and displayed in bits per second
-   MP-BGP based MPLS IP VPN
-   Per-prefix and per-vrf label distribution policies for MP-BGP based MPLS VPN
-   OSPF extensions for MPLS TE
-   support for OSPF as CE-PE protocol
-   ping and traceroute for specified VRF
-   control over network-layer TTL propagation in MPLS
-   RIP as CE-PE protocol
-   per-VRF BGP instance redistribution settings

**MPLS features that RouterOS DOES NOT HAVE yet:**

-   LDP features:
    -   downstream on-demand label advertisement
    -   ordered label distribution control
    -   conservative label retention
-   TE features
    -   fast-reroute
    -   link/node protection
-   Support for BGP as label distribution protocol