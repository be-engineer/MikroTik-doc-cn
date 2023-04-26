# Introduction

WebFig is a web-based RouterOS utility that allows you to monitor, configure and troubleshoot the router. It is designed as an alternative of WinBox, both have similar layouts and both have access to almost any feature of RouterOS.

As Webfig is platform-independent, it can be used to configure a router directly from various devices without the need for software developed for specific platforms. In other words, there is no need to install additional software.

WebFig allows performing three basic actions:

-   Configuration - view and edit current configuration;
-   Monitoring - display the current status of the router, routing information, interface stats, logs, etc;
-   Troubleshooting - RouterOS has built-in many troubleshooting tools (like ping, traceroute, packet sniffers, traffic generators, etc) and all of them can be used with WebFig

# Connecting to a Router

As we already know from the [First Time Configuration](https://help.mikrotik.com/docs/display/ROS/First+Time+Configuration) section, the device by default has username **admin** and **no password** configured. Simply open a Web browser and in the search bar type device IP address which by default is **192.168.88.1.** Be sure your device has IP address from the same network, for example, 192.168.88.2 otherwise Layer3 communication will not work.

![](https://help.mikrotik.com/docs/download/attachments/328131/webfig.png?version=3&modificationDate=1571210992820&api=v2)In our example, we will use IP address 10.155.126.250 to connect to the device via WebFig.

# Enable HTTPS

For HTTPS to work properly, you need to specify a valid certificate that Webfig can use. You can use a certificate that is issued by a trusted Certificate Authority (CA) or you can create your own root CA and generate self-signed certificates. 

Webfig supports wildcard certificates. You can generate such a certificate by specifying a wildcard in the common-name property, for example, _common-name=\*.[mikrotik.com](https://mikrotik.com)._

To generate your own certificates and enable HTTPS access, you must configure the following:

Create your own root CA on your router and sign it

[?](https://help.mikrotik.com/docs/display/ROS/Webfig#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; certificate </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=local-cert</code> <code class="ros value">common-name</code><code class="ros plain">=local-cert</code> <code class="ros value">key-usage</code><code class="ros plain">=key-cert-sign,crl-sign</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; certificate sign local-cert</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">progress</code><code class="ros constants">: done</code></div></div></td></tr></tbody></table>

In case you already have set up your own CA or you are using a service that signs certificates for you, then you create and sign the certificate remotely and import the certificate on the router later. In case you are importing a certificate, then make sure you mark the certificate as trusted.

Create a new certificate for Webfig (non-root certificate)

[?](https://help.mikrotik.com/docs/display/ROS/Webfig#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; certificate </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=webfig</code> <code class="ros value">common-name</code><code class="ros plain">=192.168.88.1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; certificate sign webfig</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">progress</code><code class="ros constants">: done</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; certificate print</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: K - private-key; A - authority; T - trusted</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">:NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; COMMON-NAME&nbsp;&nbsp;&nbsp;&nbsp; FINGERPRINT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">0&nbsp; KAT&nbsp; local-cert&nbsp; local-cert&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 9b6363d033c4b2e6893c340675cfb8d1e330977526dba347a440fabffd983c5d</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">1&nbsp; KAT&nbsp; webfig&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 192.168.88.1&nbsp;&nbsp;&nbsp; 9f84ac2979bea65dccd02652056e5559bcdf866f8da5f924139d99453402bd02</code></div></div></td></tr></tbody></table>

Enable **www-ssl** and specify to use the newly created certificate for Webfig

[?](https://help.mikrotik.com/docs/display/ROS/Webfig#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; ip service</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros plain">www-ssl </code><code class="ros value">certificate</code><code class="ros plain">=webfig</code> <code class="ros value">disabled</code><code class="ros plain">=no</code></div></div></td></tr></tbody></table>

You can now visit [https://192.168.88.1](https://192.168.88.1) and securely configure your router.

By default browsers will not trust self-signed certificates, you will need to add the certificate as trusted on the first time you visit the page in your browser. Another approach is to export the root CA certificate and import it as a trusted root certificate on your computer, this way all certificates signed by this router will be considered as valid and will make it easier to manage certificates in your network.

Most Internet browsers have their own certificate trust chain and work independently from the operating system's certificate trust chain, this means that you may have to add your own root CA's certificate as a trusted certificate in your browser settings since trusting the certificate in your operating system's settings might not have any effect when using your Internet browser.

# Skins

WebFig Design Skin is a handy tool to make the interface more user friendly. It is not a security tool. If the user has sufficient rights it is possible to access hidden features by other means.

#### Designing skins

If the user has sufficient permissions (the group has the policy to edit permissions) **Design Skin** button becomes available. Pressing that toggle button will open interface editing options. Possible operations are:

-   Hide menu - this will hide all items from the menu and its submenus;
-   Hide submenu - only certain submenu will be hidden;
-   Hide tabs - if submenu details have several tabs, it is possible to hide them this way;
-   Rename menus and items - make certain features more obvious or translate them into your language;
-   Add a note to the item (in detail view) - to add comments on the field;
-   Make item read-only (in detail view) - for user safety very sensitive fields can be made read only;
-   Hide flags (in detail view) - while it is only possible to hide a flag in detail view, this flag will not be visible in list view and in detailed view;
-   Add limits for the field - (in detail view) where it is the list of times that are comma or newline separated list of allowed values:
    -   number interval '..' example: 1..10 will allow values from 1 to 10 for fields with numbers, for example, MTU size.
    -   field prefix (Text fields, MAC address, set fields, combo-boxes). If it is required to limit prefix length _$_ should be added to the end. For example, limiting the wireless interface to "station" only, "Add limit" will contain "station$"

![](https://help.mikrotik.com/docs/download/attachments/328131/image-2022-11-8_15-57-32.png?version=1&modificationDate=1667915851247&api=v2)

-   Add _Tab_ \- will add a grey ribbon with an editable label that will separate the fields. Ribbon will be added before the field it is added to;
-   Add _Separator_ \- will add a low height horizontal separator before the field it is added to.

  

**Note:** Number interval cannot be set to extend limitations set by RouterOS for that field

**Note:** Set fields are arguments that consist of a set of check-boxes, for example, setting up policies for user groups, RADIUS "Service"

**Note:** Limitations set for combo-boxes will values selectable from the dropdown

#### Skin design examples

If you need to limit the user for some services 

![](https://help.mikrotik.com/docs/download/attachments/328131/image-2022-11-8_16-47-4.png?version=1&modificationDate=1667918823526&api=v2)

Add a limit to the RADIUS Service.

![](https://help.mikrotik.com/docs/download/attachments/328131/image-2022-11-8_17-6-52.png?version=1&modificationDate=1667920010786&api=v2)

The result will be only those services, that are pointed in the "Limit" field.

![](https://help.mikrotik.com/docs/download/attachments/328131/image-2022-11-8_17-7-15.png?version=1&modificationDate=1667920033833&api=v2)

#### Using skins

To use skins you have to assign skin to the group. When that is done users of that group will automatically use the selected skin as their default when logging into WebFig or Winbox.

[?](https://help.mikrotik.com/docs/display/ROS/Webfig#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user/group/</code><code class="ros functions">set </code><code class="ros plain">your_group_name </code><code class="ros value">skin</code><code class="ros plain">=your_skin</code></div></div></td></tr></tbody></table>

If it is required to use created skin on another router you can copy files to the skins folder on the other router. On the new router, it is required to add copied skin to the user group to use it.