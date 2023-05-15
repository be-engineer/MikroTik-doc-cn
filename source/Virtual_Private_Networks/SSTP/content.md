# Overview

Secure Socket Tunneling Protocol (SSTP) transports a PPP tunnel over a TLS channel. The use of TLS over TCP port 443 allows SSTP to pass through virtually all firewalls and proxy servers.

# Introduction

Let\`s take a look at the SSTP connection mechanism:

  

![](https://help.mikrotik.com/docs/download/attachments/2031645/Sstp-how-works.png?version=2&modificationDate=1615377176687&api=v2)

1.  A TCP connection is established from client to server (by default on port 443);
2.  SSL validates the server certificate. If a certificate is valid, a connection is established otherwise the connection is turned down. (But see note below);
3.  The client sends SSTP control packets within the HTTPS session which establishes the SSTP state machine on both sides;
4.  PPP negotiation over SSTP. The client authenticates to the server and binds IP addresses to the SSTP interface;

SSTP tunnel is now established and packet encapsulation can begin;

Starting from v5.0beta2 SSTP does not require certificates to operate and can use any available authentication type. This feature will work only between two MikroTik routers, as it is not in accordance with Microsoft standards. Otherwise to establish secure tunnels **mschap** authentication and client/server certificates from the same chain should be used.

# Certificates

To set up a secure SSTP tunnel, certificates are required. On the server, authentication is done only by _username_ and _password,_ but on the client - the server is authenticated using a server certificate. It is also used by the client to cryptographically bind SSL and PPP authentication, meaning - the clients send a special value over SSTP connection to the server, this value is derived from the key data that is generated during PPP authentication and server certificate, this allows the server to check if both channels are secure.

If SSTP clients are on Windows PCs then the only way to set up a secure SSTP tunnel when using a self-signed certificate is by importing the "server" certificate on the SSTP server and on the Windows PC adding a CA certificate in the [trusted root](https://technet.microsoft.com/en-us/library/dd458982.aspx).

If your server certificate is issued by a CA which is already known by Windows, then the Windows client will work without any additional certificate imports to a trusted root.

RSA key length must be at least 472 bits if a certificate is used by SSTP. Shorter keys are considered as security threats.

  

A similar configuration on RouterOS client would be to import the CA certificate and enabling the verify-server-certificate option. In this scenario, Man-in-the-Middle attacks are not possible.

Between two Mikrotik routers, it is also possible to set up an insecure tunnel by not using certificates at all. In this case, data going through the SSTP tunnel is using anonymous DH and Man-in-the-Middle attacks are easily accomplished. This scenario is not compatible with Windows clients.

It is also possible to make a secure SSTP tunnel by adding additional authorization with a client certificate. Configuration requirements are:

-   certificates on both server and client
-   verification options enabled on server and client

This scenario is also not possible with Windows clients, because there is no way to set up a client certificate on Windows.

### Certificate Error Messages

When SSL handshake fails, you will see one of the following certificate errors:

-   **certificate is not yet valid** - notBefore certificate date is after the current time;
-   **certificate has expired** - certificate expiry date is before the current time;
-   **cinvalid certificate purpose** - the supplied certificate cannot be used for the specified purpose;
-   **cself signed certificate in a chain** - the certificate chain could be built up using the untrusted certificates but the root could not be found locally;
-   **cunable to get issuer certificate locally** - CA certificate is not imported locally;
-   **cserver's IP address does not match certificate** - server address verification is enabled, but the address provided in certificate does not match the server's address;

# Quick Example

![](https://help.mikrotik.com/docs/download/attachments/2031645/sstp-setup.jpg?version=1&modificationDate=1571825575193&api=v2)

## SSTP Client

In the following configuration example, e will create a simple SSTP client without using a certificate:

[?](https://help.mikrotik.com/docs/display/ROS/SSTP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik &gt; interface sstp-client </code><code class="ros functions">add </code><code class="ros value">connect-to</code><code class="ros plain">=192.168.62.2</code> <code class="ros value">disabled</code><code class="ros plain">=no</code> <code class="ros value">name</code><code class="ros plain">=sstp-out1</code> <code class="ros value">password</code><code class="ros plain">=StrongPass</code> <code class="ros value">profile</code><code class="ros plain">=default-encryption</code> <code class="ros value">user</code><code class="ros plain">=MT-User</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik &gt; interface sstp-client print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled; R - running</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp; R </code><code class="ros value">name</code><code class="ros plain">=</code><code class="ros string">"sstp-out1"</code> <code class="ros value">max-mtu</code><code class="ros plain">=1500</code> <code class="ros value">max-mru</code><code class="ros plain">=1500</code> <code class="ros value">mrru</code><code class="ros plain">=disabled</code> <code class="ros value">connect-to</code><code class="ros plain">=192.168.62.2:443</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">http-proxy</code><code class="ros plain">=0.0.0.0:443</code> <code class="ros value">certificate</code><code class="ros plain">=none</code> <code class="ros value">verify-server-certificate</code><code class="ros plain">=no</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">verify-server-address-from-certificate</code><code class="ros plain">=yes</code> <code class="ros value">user</code><code class="ros plain">=</code><code class="ros string">"MT-User"</code> <code class="ros value">password</code><code class="ros plain">=</code><code class="ros string">"StrongPass"</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">profile</code><code class="ros plain">=default-encryption</code> <code class="ros value">keepalive-timeout</code><code class="ros plain">=60</code> <code class="ros value">add-default-route</code><code class="ros plain">=no</code> <code class="ros value">dial-on-demand</code><code class="ros plain">=no</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros value">authentication</code><code class="ros plain">=pap,chap,mschap1,mschap2</code> <code class="ros value">pfs</code><code class="ros plain">=no</code> <code class="ros value">tls-version</code><code class="ros plain">=any</code></div></div></td></tr></tbody></table>

## SSTP Server

We will configure PPP secret for a particular user, afterwards simply enable an SSTP server:

[?](https://help.mikrotik.com/docs/display/ROS/SSTP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; ppp secret </code><code class="ros functions">add </code><code class="ros value">local-address</code><code class="ros plain">=10.0.0.1</code> <code class="ros value">name</code><code class="ros plain">=MT-User</code> <code class="ros value">password</code><code class="ros plain">=StrongPass</code> <code class="ros value">remote-address</code><code class="ros plain">=10.0.0.5</code> <code class="ros value">service</code><code class="ros plain">=sstp</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; interface sstp-server server </code><code class="ros functions">set </code><code class="ros value">default-profile</code><code class="ros plain">=default-encryption</code> <code class="ros value">enabled</code><code class="ros plain">=yes</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; interface sstp-server server print</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">enabled</code><code class="ros constants">: yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">port</code><code class="ros constants">: 443</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">max-mtu</code><code class="ros constants">: 1500</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">max-mru</code><code class="ros constants">: 1500</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">mrru</code><code class="ros constants">: disab</code><code class="ros plain">led</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">keepalive-timeout</code><code class="ros constants">: 60</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">default-profile</code><code class="ros constants">: default-encryption</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">authentication</code><code class="ros constants">: pap,chap,mschap1,mschap2</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">certificate</code><code class="ros constants">: none</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">verify-client-certificate</code><code class="ros constants">: no</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">pfs</code><code class="ros constants">: no</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">tls-version</code><code class="ros constants">: any</code></div></div></td></tr></tbody></table>