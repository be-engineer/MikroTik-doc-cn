User Manager version 5 ( available for RouterOS v7 ) supports user authentication via the Extensible Authentication Protocol (EAP).

This guide will explain the steps needed to configure User Manager v5 as the authentication server for MikroTik wireless access points with users being offered PEAP and EAP-TLS authentication methods.

The guide assumes a standalone device running User Manager at the network address 10.0.0.10 and 2 Access Points - one at 10.0.0.11 and the other at 10.0.0.12

# Installing User Manager

User Manager v5 can be found in the 'Extra packages' archive for the [latest release of RouterOS v7](https://mikrotik.com/download).

Download the archive for the appropriate CPU architecture, extract it, upload the User Manager package to  the router and reboot it.

# Generating TLS certificates

When using secure EAP methods, the client device (supplicant) verifies the identity of the authenication server before sending its own credentials to it.  
For this to happen, the authentication server needs a TLS certificate.

This certificate should:

1.  Be valid and signed by a certificate authority which is trusted by the client device
2.  Have a fully qualified domain name in the Common Name (CN) and Subject Alt Name fields
3.  Have the Extended Key Usage attribute indicating that it is authorized for authentcating a TLS server
4.  Have Validity period of no more than 825 days

The EAP-TLS method requires the client device to have a TLS certificate (instead of a password).

To be considered valid by User Manager, a client certificate must:

1.  Be valid and signed by an authority, which is trusted by the device running User Manager
2.  Have the user name in the Subject Alt Name (SAN) field. For backward compatibility, you can also add it in the CN field. For more information please see: [https://datatracker.ietf.org/doc/html/rfc5216#section-5.2](https://datatracker.ietf.org/doc/html/rfc5216#section-5.2) 

Finally, the [WPA3 enterprise specification](https://www.wi-fi.org/download.php?file=/sites/default/files/private/WPA3_Specification_v3.0.pdf) includes an extra secure mode, which provides 192-bit cryptographic security.

This mode requires using EAP-TLS with certificates that:

1.  Use either P-384 elliptic curve keys or RSA keys which are at least 3072 bits in length
2.  Use SHA384 as the digest (hashing) algorithm

For the sake of brevity (and to showcase more of RouterOS' capabilities), this guide will show how to generate all the certificates on the device running User Manager, but in a large scale enterprise environment, the authentication server and client devices would each generate private keys and certificate signing requests locally, then upload CSRs to a certificate authority for signing.

**Commands executed on device running User Manager**

[?](https://help.mikrotik.com/docs/display/ROS/Enterprise+wireless+security+with+User+Manager+v5#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros comments"># Generating a Certificate Authority</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/certificate</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=radius-ca</code> <code class="ros value">common-name</code><code class="ros plain">=</code><code class="ros string">"RADIUS CA"</code> <code class="ros value">key-size</code><code class="ros plain">=secp384r1</code> <code class="ros value">digest-algorithm</code><code class="ros plain">=sha384</code> <code class="ros value">days-valid</code><code class="ros plain">=1825</code> <code class="ros value">key-usage</code><code class="ros plain">=key-cert-sign,crl-sign</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">sign radius-ca </code><code class="ros value">ca-crl-host</code><code class="ros plain">=radius.mikrotik.test</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros comments"># Generating a server certificate for User Manager</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=userman-cert</code> <code class="ros value">common-name</code><code class="ros plain">=radius.mikrotik.test</code> <code class="ros value">subject-alt-name</code><code class="ros plain">=DNS:radius.mikrotik.test</code> <code class="ros value">key-size</code><code class="ros plain">=secp384r1</code> <code class="ros value">digest-algorithm</code><code class="ros plain">=sha384</code> <code class="ros value">days-valid</code><code class="ros plain">=800</code> <code class="ros value">key-usage</code><code class="ros plain">=tls-server</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">sign userman-cert </code><code class="ros value">ca</code><code class="ros plain">=radius-ca</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros comments"># Generating a client certificate</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=maija-client-cert</code> <code class="ros value">common-name</code><code class="ros plain">=maija@mikrotik.test</code> <code class="ros value">key-usage</code><code class="ros plain">=tls-client</code> <code class="ros value">days-valid</code><code class="ros plain">=800</code> <code class="ros value">key-size</code><code class="ros plain">=secp384r1</code> <code class="ros value">digest-algorithm</code><code class="ros plain">=sha384</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">sign maija-client-cert </code><code class="ros value">ca</code><code class="ros plain">=radius-ca</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros comments"># Exporting the public key of the CA as well as the generated client private key and certificate for distribution to client devices</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros plain">export-certificate radius-ca </code><code class="ros value">file-name</code><code class="ros plain">=radius-ca</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros comments"># A passphrase is needed for the export to include the private key</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros plain">export-certificate maija-client-cert </code><code class="ros value">type</code><code class="ros plain">=pkcs12</code> <code class="ros value">export-passphrase</code><code class="ros plain">=</code><code class="ros string">"true zebra capacitor ziptie"</code></div></div></td></tr></tbody></table>

# Configuring User Manager

**Commands executed on device running User Manager**

[?](https://help.mikrotik.com/docs/display/ROS/Enterprise+wireless+security+with+User+Manager+v5#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros comments"># Enabling User Manager and specifying, which certificate to use</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/user-manager</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">enabled</code><code class="ros plain">=yes</code> <code class="ros value">certificate</code><code class="ros plain">=userman-cert</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments"># Enabling CRL checking to avoid accepting revoked user certificates</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/certificate settings</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">crl-download</code><code class="ros plain">=yes</code> <code class="ros value">crl-use</code><code class="ros plain">=yes</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros comments"># Adding access points</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros constants">/user-manager router</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ap1</code> <code class="ros value">address</code><code class="ros plain">=10.0.0.11</code> <code class="ros value">shared-secret</code><code class="ros plain">=</code><code class="ros string">"Use a secure password generator for this"</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=ap2</code> <code class="ros value">address</code><code class="ros plain">=10.0.0.12</code> <code class="ros value">shared-secret</code><code class="ros plain">=</code><code class="ros string">"Use a secure password generator for this too"</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros comments"># Limiting allowed authentication methods</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros constants">/user-manager user group</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros plain">where </code><code class="ros value">name</code><code class="ros plain">=default]</code> <code class="ros value">outer-auths</code><code class="ros plain">=eap-tls,eap-peap</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=certificate-authenticated</code> <code class="ros value">outer-auths</code><code class="ros plain">=eap-tls</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros comments"># Adding users</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros constants">/user-manager user</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=maija@mikrotik.test</code> <code class="ros value">group</code><code class="ros plain">=certificate-authenticated</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=paija@mikrotik.test</code> <code class="ros value">group</code><code class="ros plain">=default</code> <code class="ros value">password</code><code class="ros plain">=</code><code class="ros string">"right mule accumulator nail"</code></div></div></td></tr></tbody></table>

# Configuring access points

## AP running regular wireless package

**Commands executed on ap1**

[?](https://help.mikrotik.com/docs/display/ROS/Enterprise+wireless+security+with+User+Manager+v5#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros comments"># Configuring radius client</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/radius</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.0.0.10</code> <code class="ros value">secret</code><code class="ros plain">=</code><code class="ros string">"Use a secure password generator for this"</code> <code class="ros value">service</code><code class="ros plain">=wireless</code> <code class="ros value">timeout</code><code class="ros plain">=1s</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments"># Adding a security profile and applying it to wireless interfaces</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wireless/security-pro</code><code class="ros plain">file</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=radius</code> <code class="ros value">mode</code><code class="ros plain">=dynamic-keys</code> <code class="ros value">authentication-types</code><code class="ros plain">=wpa2-eap</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wireless</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">[find] </code><code class="ros value">security-profile</code><code class="ros plain">=radius</code></div></div></td></tr></tbody></table>

## AP running wifiwave2 package

**Commands executed on ap2**

[?](https://help.mikrotik.com/docs/display/ROS/Enterprise+wireless+security+with+User+Manager+v5#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros comments"># Configuring radius client</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/radius</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">address</code><code class="ros plain">=10.0.0.10</code> <code class="ros value">secret</code><code class="ros plain">=</code><code class="ros string">"Use a secure password generator for this too"</code> <code class="ros value">service</code><code class="ros plain">=wireless</code> <code class="ros value">timeout</code><code class="ros plain">=1s</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments"># Configuring enabled authentication types. Can also be done via a security profile, but note that interface properties, if specified, override profile properties</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">/interface/wifiwave2 </code><code class="ros functions">set </code><code class="ros plain">[find] </code><code class="ros value">security.authentication-types</code><code class="ros plain">=wpa2-eap,wpa3-eap</code></div></div></td></tr></tbody></table>

A wifiwave2 AP can  also be configured to use the extra secure wpa3-eap-192 mode, but note that it requires that all client devices support the GCMP-256 cipher and use EAP-TLS authentication.

# Notes on client device configuration

## Windows

When manually installing a CA in Windows, make sure to explicitly place it in the 'Trusted Root Certification Authorities' certificate store. It will not be placed there automatically.

## Android

When connecting to a network with EAP authentication, Android devices ask the user to specify a 'domain'. This refers to the expected domain of the host name included in the RADIUS server's TLS certificate ( 'mikrotik.test' in our example).

By default, Android devices use the device's built-in root CA list for validating the RADIUS server's certificate. When using your own CA, it needs to be selected in the appropriate dropdown menu.

## iOS

Apple iOS does not appear to actually trust a manually imported CA to authenticate RADIUS servers. The server certificate is marked as 'Not Trusted' unless the CA was imported using Apple's proprietary 'Configurator' utility or an approved third party MDM tool.