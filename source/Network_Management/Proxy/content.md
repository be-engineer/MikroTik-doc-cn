# Summary

MikroTik RouterOS performs proxying of HTTP and HTTP-proxy (for FTP and HTTP protocols) requests. The proxy server performs the Internet object cache function by storing requested Internet objects, i.e., data available via HTTP and FTP protocols on a system positioned closer to the recipient in the form of speeding up customer browsing by delivering them requested file copies from the proxy cache at local network speed. MikroTik RouterOS implements the following proxy server features:

-   Regular HTTP proxy – customer (itself) specifies what is a proxy server for him;
-   Transparent proxy – the customer does not know about the proxy being enabled and there isn’t a necessity for any additional configuration for the web browser of the client;
-   Access list by source, destination, URL, and requested method (HTTP firewall);
-   Cache access list to specify which objects to cache, and which not;
-   Direct Access List – to specify which resources should be accessed directly, and which - through another proxy server;
-   Logging facility – allows to get and store information about the proxy operation;
-   Parent proxy support – allows to specify another proxy server, _(if they don’t have the requested object ask their parents, or to the original server);_

  
A proxy server usually is placed at various points between users and the destination server (_also known as the origin server_) on the Internet.

![](https://help.mikrotik.com/docs/download/attachments/132350000/Image10002.jpg?version=1&modificationDate=1658409074627&api=v2)

A _Web proxy (cache)_ watches requests coming from clients, saving copies of the responses for itself. Then, if there is another request for the same URL, it can use the response that it has, instead of asking the origin server for it again. If the proxy has not requested a file, it downloads that from the original server.

There can be many potential purposes of proxy servers:

-   To increase access speed to resources (it takes less time for the client to get the object);
-   Works as HTTP firewall (deny access to undesirable web pages);

Allows filtering web content (by specific parameters, like source address, a destination address, port, URL, HTTP request method) scan outbound content, e.g., for data leak protection.

It may be useful to have a Web proxy running even with no cache when you want to use it only as something like an HTTP and FTP firewall (for example, denying access to undesired web pages or denying a specific type of files e.g. .mp3 files) or to redirect requests to external proxy (possibly, to a proxy with caching functions) transparently.

# Configuration examples

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/proxy</code></div></div></td></tr></tbody></table>

In MikroTik RouterOS, a proxy configuration is performed in the _/ip/proxy_ menu. See below how to enable the proxy on port 8080 and set up 192.168.88.254 as the proxy source address:

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; ip</code><code class="ros constants">/proxy/</code><code class="ros functions">set </code><code class="ros value">enabled</code><code class="ros plain">=yes</code> <code class="ros value">port</code><code class="ros plain">=8080</code> <code class="ros value">src-address</code><code class="ros plain">=192.168.88.254</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; ip</code><code class="ros constants">/proxy/</code><code class="ros functions">print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">enabled</code><code class="ros constants">: yes</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">src-address</code><code class="ros constants">: 192.168.88.254</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">port</code><code class="ros constants">: 8080</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">anonymous</code><code class="ros constants">: no</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">parent-proxy</code><code class="ros constants">: ::</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">parent-proxy-port</code><code class="ros constants">: 0</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">cache-administrator</code><code class="ros constants">: webmaster</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">max-cache-size</code><code class="ros constants">: unlimited</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">max-cache-object-size</code><code class="ros constants">: 2048KiB</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">cache-on-disk</code><code class="ros constants">: no</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">max-client-connections</code><code class="ros constants">: 600</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">max-server-connections</code><code class="ros constants">: 600</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">max-fresh-time</code><code class="ros constants">: 3d</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">serialize-connections</code><code class="ros constants">: no</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">always-from-cache</code><code class="ros constants">: no</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">cache-hit-dscp</code><code class="ros constants">: 4</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">cache-path</code><code class="ros constants">: web-proxy</code></div></div></td></tr></tbody></table>

When setting up a regular proxy service, make sure it serves only your clients and prevents unauthorized access to it by creating a firewall that allows only your clients to use a proxy, otherwise, it may be used as an open proxy.

## Transparent proxy configuration example

RouterOS can also act as a Transparent Caching server, with no configuration required in the customer’s web browser. A transparent proxy does not modify the requested URL or response. RouterOS will take all HTTP requests and redirect them to the local proxy service. This process will be entirely transparent to the user (users may not know anything about a proxy server that is located between them and the original server), and the only difference to them will be the increased browsing speed.

To enable the transparent mode, the firewall rule in destination NAT has to be added, specifying which connections (to which ports) should be transparently redirected to the proxy. Check proxy settings above and redirect us users (192.168.1.0/24) to a proxy server:

  

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] ip firewall nat&gt; </code><code class="ros functions">add </code><code class="ros value">chain</code><code class="ros plain">=dstnat</code> <code class="ros value">protocol</code><code class="ros plain">=tcp</code> <code class="ros value">src-address</code><code class="ros plain">=192.168.1.0/24</code> <code class="ros value">dst-port</code><code class="ros plain">=80</code> <code class="ros value">action</code><code class="ros plain">=redirect</code> <code class="ros value">to-ports</code><code class="ros plain">=8080</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] ip firewall nat&gt; print</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - invalid, D - dynamic</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;&nbsp; </code><code class="ros value">chain</code><code class="ros plain">=dstnat</code> <code class="ros value">protocol</code><code class="ros plain">=tcp</code> <code class="ros value">dst-port</code><code class="ros plain">=80</code> <code class="ros value">action</code><code class="ros plain">=redirect</code> <code class="ros value">to-ports</code><code class="ros plain">=8080</code></div></div></td></tr></tbody></table>

 The web proxy can be used as a transparent and normal web proxy at the same time. In transparent mode, it is possible to use it as a standard web proxy, too. However, in this case, proxy users may have trouble reaching web pages that are accessed transparently.

## Proxy-based firewall – Access List

An access list is implemented in the same way as MikroTik firewall rules processed from the top to the bottom. The first matching rule specifies the decision of what to do with this connection. Connections can be matched by their source address, destination address, destination port, sub-string of the requested URL (Uniform Resource Locator), or request method. If none of these parameters is specified, every connection will match this rule.

If a connection is matched by a rule, the action property of this rule specifies whether a connection will be allowed or not (deny). If a connection does not match any rule, it will be allowed.

In this example assume that we have configured a transparent proxy server, it will block the website [http://www.facebook.com](http://www.facebook.com/), we can always block the same for different networks by giving src-address:

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip proxy access </code><code class="ros functions">add </code><code class="ros value">src-address</code><code class="ros plain">=192.168.1.0/24</code> <code class="ros value">dst-host</code><code class="ros plain">=www.facebook.com</code> <code class="ros value">action</code><code class="ros plain">=deny</code></div></div></td></tr></tbody></table>

Users from network 192.168.1.0/24 will not be able to access the website [www.facebook.com](http://www.facebook.com/).

You can block also websites that contain specific words in the URL:

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip proxy access </code><code class="ros functions">add </code><code class="ros value">dst-host</code><code class="ros plain">=:mail</code> <code class="ros value">action</code><code class="ros plain">=deny</code></div></div></td></tr></tbody></table>

This statement will block all websites which contain the word “mail” in the URL. Like [www.mail.com](http://www.mail.com/), [www.hotmail.com](http://www.hotmail.com/), [mail.yahoo.com](http://mail.yahoo.com), etc.

_**We can also stop downloading specific types of files like .flv, .avi, .mp4, .mp3, .exe, .dat, …etc.**_

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip proxy access</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">path</code><code class="ros plain">=*.flv</code> <code class="ros value">action</code><code class="ros plain">=deny</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">path</code><code class="ros plain">=*.avi</code> <code class="ros value">action</code><code class="ros plain">=deny</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">path</code><code class="ros plain">=*.mp4</code> <code class="ros value">action</code><code class="ros plain">=deny</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">path</code><code class="ros plain">=*.mp3</code> <code class="ros value">action</code><code class="ros plain">=deny</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">path</code><code class="ros plain">=*.zip</code> <code class="ros value">action</code><code class="ros plain">=deny</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">add </code><code class="ros value">path</code><code class="ros plain">=*.rar</code> <code class="ros value">action</code><code class="ros plain">=deny</code></div></div></td></tr></tbody></table>

  

Here are available also different wildcard characters, to create specific conditions and to match them by proxy access list. Wildcard properties (dst-host and dst-path) match a complete string (i.e., they will not match "[example.com](http://example.com)" if they are set to "example"). Available wildcards are '\*' (match any number of any characters) and '?' (match any one character).

Regular expressions are also accepted here, but if the property should be treated as a regular expression, it should start with a colon (':').

To show that no symbols are allowed before the given pattern, we use the ^ symbol at the beginning of the pattern.

To specify that no symbols are allowed after the given pattern, we use the $ symbol at the end of the pattern.

# Enabling RAM or Store-based caching.

In this example, it will presume that you already have the proxy configured and working and you just want to enable caching. If a command/parameter detailed description is required check the reference section which is located right below the example section.

-   RAM-based caching:
    -   Good if you have a device with a considerable amount of RAM for caching. Enabling this on a device with RAM 256MB or less will not give your network any benefit.
    -   Way faster cache writes/read than one that is stored on USB or SATA connected mediums.

-   Store-based caching:
    -   Larger proxy caches are available simply due to medium capacity differences.

## **RAM proxy cache:**

Important commands:

-   max-cache-size=
-   max-cache-object-size=
-   cache-on-disk=

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/ip proxy&gt; </code><code class="ros functions">set </code><code class="ros value">max-cache-size</code><code class="ros plain">=unlimited</code> <code class="ros value">max-cache-object-size</code><code class="ros plain">=50000KiB</code> <code class="ros value">cache-on-disk</code><code class="ros plain">=no</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">...</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/ip proxy&gt; </code><code class="ros functions">print</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">enabled</code><code class="ros constants">: yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">src-address</code><code class="ros constants">:&nbsp;::</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">port</code><code class="ros constants">: 8080</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">anonymous</code><code class="ros constants">: no</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">parent-proxy</code><code class="ros constants">: 0.0.0.0</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">parent-proxy-port</code><code class="ros constants">: 0</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">cache-administrator</code><code class="ros constants">: webmaster</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">max-cache-size</code><code class="ros constants">: unlimited&nbsp; &lt;-------</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">max-cache-object-size</code><code class="ros constants">: 500000KiB&nbsp; &lt;-------</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">cache-on-disk</code><code class="ros constants">: no&nbsp; &lt;-------</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">max-client-connections</code><code class="ros constants">: 600</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">max-server-connections</code><code class="ros constants">: 600</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">max-fresh-time</code><code class="ros constants">: 3d</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">serialize-connections</code><code class="ros constants">: no</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">always-from-cache</code><code class="ros constants">: no</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">cache-hit-dscp</code><code class="ros constants">: 4</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">cache-path</code><code class="ros constants">: proxy-cache</code></div></div></td></tr></tbody></table>

## **Store proxy cache:**

Important commands:

-   max-cache-size=
-   max-cache-object-size=
-   cache-on-disk=
-   cache-path=

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; ip proxy </code><code class="ros functions">set </code><code class="ros value">cache-on-disk</code><code class="ros plain">=yes</code> <code class="ros value">cache-path</code><code class="ros plain">=/usb1/proxy/cache</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; ip proxy </code><code class="ros functions">print </code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">enabled</code><code class="ros constants">: yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">src-address</code><code class="ros constants">:&nbsp;::</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">port</code><code class="ros constants">: 8080</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">anonymous</code><code class="ros constants">: no</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">parent-proxy</code><code class="ros constants">: 0.0.0.0</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">parent-proxy-port</code><code class="ros constants">: 0</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">cache-administrator</code><code class="ros constants">: webmaster</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">max-cache-size</code><code class="ros constants">: unlimited&nbsp; &lt;-------</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">max-cache-object-size</code><code class="ros constants">: 50000KiB&nbsp; &lt;-------</code></div><div class="line number13 index12 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">cache-on-disk</code><code class="ros constants">: yes&nbsp; &lt;-------</code></div><div class="line number14 index13 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">max-client-connections</code><code class="ros constants">: 600</code></div><div class="line number15 index14 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">max-server-connections</code><code class="ros constants">: 600</code></div><div class="line number16 index15 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">max-fresh-time</code><code class="ros constants">: 3d</code></div><div class="line number17 index16 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">serialize-connections</code><code class="ros constants">: no</code></div><div class="line number18 index17 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">always-from-cache</code><code class="ros constants">: no</code></div><div class="line number19 index18 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">cache-hit-dscp</code><code class="ros constants">: 4</code></div><div class="line number20 index19 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">cache-path</code><code class="ros constants">: usb1/proxy/cache&nbsp; &lt;-------</code></div><div class="line number21 index20 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number22 index21 alt1" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros functions">file </code><code class="ros functions">print </code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class="line number23 index22 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments"># NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TYPE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number24 index23 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0 skins&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; directory&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number25 index24 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">5 usb1</code><code class="ros constants">/proxy&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; directory&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number26 index25 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">6 usb1</code><code class="ros constants">/proxy/cache&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; web-proxy store&nbsp;&nbsp; &lt;-------&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number27 index26 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">7 usb1</code><code class="ros constants">/lost+found&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; directory</code></div></div></td></tr></tbody></table>

**Check if a cache is working:**

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; ip proxy </code><code class="ros functions">monitor</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">status</code><code class="ros constants">: running</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">uptime</code><code class="ros constants">: 2w20h28m25s</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">client-connections</code><code class="ros constants">: 15</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">server-connections</code><code class="ros constants">: 7</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">requests</code><code class="ros constants">: 79772</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">hits</code><code class="ros constants">: 30513</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">cache-used</code><code class="ros constants">: 481KiB</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">total-ram-used</code><code class="ros constants">: 1207KiB</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">received-from-servers</code><code class="ros constants">: 4042536KiB</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">sent-to-clients</code><code class="ros constants">: 4399757KiB</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">hits-sent-to-clients</code><code class="ros constants">: 176934KiB</code></div></div></td></tr></tbody></table>

# Reference

List of all available parameters and commands per menu.

### General

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/proxy</code></div></div></td></tr></tbody></table>

  

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                                                                                   |
 | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | **always-from-cache** (_yes                                                       | no_; Default: **no**)                                                                                                                                                                                                                                                                                                 | ignore client refresh requests if the content is considered fresh                                                                                                                                                                                                                                                                                                                                                      |
 | **anonymous** (_yes                                                               | no_; Default: **no**)                                                                                                                                                                                                                                                                                                 | If not set, the IP address of the client would be passed X-Forwarded-For header (could be accessed using HTTP\_X\_FORWARDED\_FOR environment variable in remote servers)                                                                                                                                                                                                                                               |
 | **cache-administrator** (_string_; Default: **webmaster**)                        | Administrator's e-mail displayed on proxy error page                                                                                                                                                                                                                                                                  |
 | **cache-hit-dscp** (_integer: 0..63_; Default: **4**)                             | Automatically mark cache hit with the provided DSCP value                                                                                                                                                                                                                                                             |
 | **cache-on-disk** (_yes                                                           | no_; Default: **no**)                                                                                                                                                                                                                                                                                                 | Whether to store cache on disk                                                                                                                                                                                                                                                                                                                                                                                         |
 | **cache-path** (_string_; Default: **web-proxy**)                                 | A path where the cache will be stored, when cache-on-disk is enabled.                                                                                                                                                                                                                                                 |
 | **max-cache-object-size** (_integer: 0..4294967295\[KiB\]_; Default: **2048KiB**) | Specifies the maximal cache object size, measured in kilobytes                                                                                                                                                                                                                                                        |
 | **max-cache-size** (_none                                                         | unlimited                                                                                                                                                                                                                                                                                                             | integer: 0..4294967295\[KiB\]_; Default: **unlimited**)                                                                                                                                                                                                                                                                                                                                                                | Specifies the maximal cache size, measured in kilobytes |
 | **max-client-connections** (_integer: Dynamic_ ; Default: **600**)                | Maximal number of connections accepted from clients (any further connections will be rejected)                                                                                                                                                                                                                        |
 | **max-fresh-time** (_time_; Default: **3d**)                                      | Maximal time to store a cached object. The validity period of an object is usually defined by the object itself, but in case it is set too high, you can override the maximal value                                                                                                                                   |
 | **max-server-connections** (_integer: Dynamic_ ; Default: **600**)                | Maximal number of connections made to servers (any further connections from clients will be put on hold until some server connections will terminate)                                                                                                                                                                 |
 | **parent-proxy** (_Ip4                                                            | ip6_; Default: **0.0.0.0**)                                                                                                                                                                                                                                                                                           | IP address and port of another HTTP proxy to redirect all requests to. If set to **0.0.0.0** parent proxy is not used.                                                                                                                                                                                                                                                                                                 |
 | **parent-proxy-port** (_integer: 0..65535_; Default: **0**)                       | Port that parent proxy is listening on.                                                                                                                                                                                                                                                                               |
 | **port** (_integer: 0..65535_; Default: **8080**)                                 | TCP port the proxy server will be listening on. This port has to be specified on all clients that want to use the server as an HTTP proxy. A transparent (with zero configuration for clients) proxy setup can be made by redirecting HTTP requests to this port in the IP firewall using the destination NAT feature |
 | **serialize-connections** (_yes                                                   | no_; Default: **no**)                                                                                                                                                                                                                                                                                                 | Do not make multiple connections to the server for multiple client connections, if possible (i.e. server supports persistent HTTP connections). Clients will be served on the FIFO principle; the next client is processed when the response transfer to the previous one is completed. If a client is idle for too long (max 5 seconds by default), it will give up waiting and open another connection to the server |
 | **src-address** (_Ip4                                                             | Ip6_; Default: **0.0.0.0**)                                                                                                                                                                                                                                                                                           | A proxy will use a specified address when connecting to the parent proxy or website. If set to **0.0.0.0** then the appropriate IP address will be taken from the routing table.                                                                                                                                                                                                                                       |

### Access List

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/proxy/access</code></div></div></td></tr></tbody></table>

An access list is configured like regular firewall rules. Rules are processed from the top to the bottom. The first matching rule specifies the decision of what to do with this connection. There is a total of 6 classifiers that specify matching constraints. If none of these classifiers is specified, the particular rule will match every connection.

If a connection is matched by a rule, the action property of this rule specifies whether a connection will be allowed or not. If the particular connection does not match any rule, it will be allowed.

  

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                                                                               |
 | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
 | **action** (_allow                                                            | deny_; Default: **allow**)                                                                                                                                                     | Specifies whether to pass or deny matched packets |
 | **dst-address** (_Ip4\[-Ip4                                                   | /0..32\]                                                                                                                                                                       | Ip6/0..128_; Default: )                           | The destination address of the target server.    |
 | **dst-host** (_string_; Default: )                                            | IP address or DNS name used to make a connection to the target server (this is the string user wrote in a browser before specifying the port and path to a particular web page |
 | **dst-port** (_integer\[-integer\[,integer\[,...\]\]\]: 0..65535_; Default: ) | List or range of ports the packet is destined to                                                                                                                               |
 | **local-port** (_integer: 0..65535_; Default: )                               | Specifies the port of the web proxy via which the packet was received. This value should match one of the ports the web proxy is listening on.                                 |
 | **method** (_any                                                              | connect                                                                                                                                                                        | delete                                            | get                                              | head | options | post | put | trace_; Default: ) | The HTTP method used in the request (see HTTP Methods section at the end of this document) |
 | **path** (_string_; Default: )                                                | Name of the requested page within the target server (i.e. the name of a particular web page or document without the name of the server it resides on)                          |
 | **redirect-to** (_string_; Default: )                                         | In case of access is denied by this rule, the user shall be redirected to the URL specified here                                                                               |
 | **src-address** (_Ip4\[-Ip4                                                   | /0..32\]                                                                                                                                                                       | Ip6/0..128_; Default: )                           | The source address of the connection originator. |

  
Read-only properties:

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                      |
 | -------------------- | ------------------------------------------------ |
 | **hits** (_integer_) | Count of requests that were matched by this rule |

  
Wildcard properties (dst-host and dst-path) match a complete string (i.e., they will not match "[example.com](http://example.com)" if they are set to "example"). Available wildcards are '\*' (match any number of any characters) and '?' (match any one character). Regular expressions are also accepted here, but if the property should be treated as a regular expression, it should start with a colon (':').

Small hints in using regular expressions:

-   \\\\ symbol sequence is used to enter \\ character in the console;
-   \\. pattern means. only (in regular expressions single dot in a pattern means any symbol);
-   to show that no symbols are allowed before the given pattern, we use the ^ symbol at the beginning of the pattern;
-   to specify that no symbols are allowed after the given pattern, we use the $ symbol at the end of the pattern;
-   to enter \[ or \] symbols, you should escape them with backslash "\\.";

It is strongly recommended to deny all IP addresses except those behind the router as the proxy still may be used to access your internal-use-only (intranet) web servers. Also, consult examples in Firewall Manual on how to protect your router.

### Direct Access

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/proxy/direct</code></div></div></td></tr></tbody></table>

If a **parent-proxy** property is specified, it is possible to tell the proxy server whether to try to pass the request to the parent proxy or to resolve it by connecting to the requested server directly. The direct Access List is managed just like the Proxy Access List described in the previous chapter except for the action argument. Unlike the access list, the direct proxy access list has a default action equal to deny. It takes place when no rules are specified or a particular request did not match any rule.

  

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                    |
 | ------------------ | -------------------------- |
 | **action** (_allow | deny_; Default: **allow**) | Specifies the action to perform on matched packets: |

-   allow \- always resolve matched requests directly bypassing the parent router
-   deny \- resolve matched requests through the parent proxy. If no one is specified this has the same effect as **allow**.

 |
| **dst-address** (_Ip4\[-Ip4 | /0..32\] | Ip6/0..128_; Default: ) | The destination address of the target server. |
| **dst-host** (_string_; Default: ) | IP address or DNS name used to make a connection to the target server (this is the string user wrote in a browser before specifying port and path to a particular web page |
| **dst-port** (_integer\[-integer\[,integer\[,...\]\]\]: 0..65535_; Default: ) | List or range of ports used by connection to the target server. |
| **local-port** (_integer: 0..65535_; Default: ) | Specifies the port of the web proxy via which the packet was received. This value should match one of the ports the web proxy is listening on. |
| **method** (_any | connect | delete | get | head | options | post | put | trace_; Default: ) | The HTTP method used in the request (see [HTTP Methods](https://wiki.mikrotik.com/wiki/Manual:IP/Proxy#HTTP_Methods) section at the end of this document) |
| **path** (_string_; Default: ) | Name of the requested page within the target server (i.e. the name of a particular web page or document without the name of the server it resides on) |
| **src-address** (_Ip4\[-Ip4 | /0..32\] | Ip6/0..128_; Default: ) | The source address of the connection originator. |

  
Read-only properties:

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                      |
 | -------------------- | ------------------------------------------------ |
 | **hits** (_integer_) | Count of requests that were matched by this rule |

### Cache Management

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/proxy/cache</code></div></div></td></tr></tbody></table>

The cache access list specifies, which requests (domains, servers, pages) have to be cached locally by web proxy, and which do not. This list is implemented exactly the same way as the web proxy access list. The default action is to cache an object (if no matching rule is found).

  

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                    |
 | ------------------ | -------------------------- |
 | **action** (_allow | deny_; Default: **allow**) | Specifies the action to perform on matched packets: |

-   allow \- cache objects from matched request
-   deny \- do not cache objects from matched request

 |
| **dst-address** (_Ip4\[-Ip4 | /0..32\] | Ip6/0..128_; Default: ) | The destination address of the target server |
| **dst-host** (_string_; Default: ) | IP address or DNS name used to make a connection to the target server (this is the string user wrote in a browser before specifying port and path to a particular web page |
| **dst-port** (_integer\[-integer\[,integer\[,...\]\]\]: 0..65535_; Default: ) | List or range of ports the packet is destined to. |
| **local-port** (_integer: 0..65535_; Default: ) | Specifies the port of the web proxy via which the packet was received. This value should match one of the ports the web proxy is listening on. |
| **method** (_any | connect | delete | get | head | options | post | put | trace_; Default: ) | The HTTP method used in the request (see HTTP Methods section at the end of this document) |
| **path** (_string_; Default: ) | Name of the requested page within the target server (i.e. the name of a particular web page or document without the name of the server it resides on) |
| **src-address** (_Ip4\[-Ip4 | /0..32\] | Ip6/0..128_; Default: ) | The source address of the connection originator |

  

Read-only properties:

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                      |
 | -------------------- | ------------------------------------------------ |
 | **hits** (_integer_) | Count of requests that were matched by this rule |

  

### Connections

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/proxy/connections</code></div></div></td></tr></tbody></table>

This menu contains the list of current connections the proxy is serving.

Read-only properties:

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                          |
 | ------------------------ | ------------------------------------------ |
 | **client** ()            |
 |                          |
 | **dst-address** (_Ip4    | Ip6_)                                      | IPv4/Ipv6 destination address of the connection |
 | **protocol** (_string_)  | Protocol name                              |
 | **rx-bytes** (_integer_) | The number of bytes received by the client |
 | **server** ()            |
 |                          |
 | **src-address** (_Ip4    | Ip6_)                                      | Ipv4/ipv6 address of the connection originator  |
 | **state** (_closing      | connecting                                 | converting                                      | hotspot | idle | resolving | rx-header | tx-body | tx-eof | tx-header | waiting_) | Connection state: |

-   closing \- the data transfer is finished, and the connection is being finalized
-   connecting \- establishing toe connection
-   converting \- replacing header and footer fields in response or request packet
-   hotspot \- check if hotspot authentication allows continuing (for hotspot proxy)
-   idle \- staying idle
-   resolving \- resolving the server's DNS name
-   rx-header \- receiving HTTP header
-   tx-body \- transmitting HTTP body to the client
-   tx-eof \- writing chunk-end (when converting to chunked response)
-   tx-header \- transmitting HTTP header to the client
-   waiting \- waiting for transmission from a peer

 |
| **tx-bytes** (_integer_) | The number of bytes sent by the client |

  

### Cache Inserts

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/proxy/inserts</code></div></div></td></tr></tbody></table>

This menu shows statistics on objects stored in a cache (cache inserts).

Read-only properties:

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                           |
 | ------------------------- | ---------------------------------------------------------------- |
 | **denied** (_integer_)    | A number of inserts were denied by the caching list.             |
 | **errors** (_integer_)    | Number of disk or other system-related errors                    |
 | **no-memory** (_integer_) | Number of objects not stored because there was not enough memory |
 | **successes** (_integer_) | A number of successful cache inserts.                            |
 | **too-large** (_integer_) | Number of objects too large to store                             |

### Cache Lookups

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/proxy/lookup</code></div></div></td></tr></tbody></table>

This menu shows statistics on objects read from cache (cache lookups).

Read-only properties:

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                                    |
 | ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
 | **denied** (_integer_)             | Number of requests denied by the access list.                                                                                       |
 | **expired** (_integer_)            | Number of requests found in cache, but expired, and, thus, requested from an external server                                        |
 | **no-expiration-info** (_integer_) | Conditional request received for a page that does not have the information to compare the request with                              |
 | **non-cacheable** (_integer_)      | Number of requests requested from the external servers unconditionally (as their caching is denied by the cache access list)        |
 | **not-found** (_integer_)          | Number of requests not found in the cache, and, thus, requested from an external server (or parent proxy if configured accordingly) |
 | **successes** (_integer_)          | Number of requests found in the cache.                                                                                              |

### Cache Contents

[?](https://help.mikrotik.com/docs/display/ROS/Proxy#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/proxy/cache-contents</code></div></div></td></tr></tbody></table>

This menu shows cached contents.

Read-only properties:

| 
Property

 | 

Description

 |     |
 | --- |  |
 |     |

Property

 | 

Description

 |                                 |
 | ------------------------------- | ------------------ |
 | **file-size** (_integer_)       | Cached object size |
 | **last-accessed** (_time_)      |
 |                                 |
 | **last-accessed-time** (_time_) |
 |                                 |
 | **last-modified** (_time_)      |
 |                                 |
 | **last-modified-time** (_time_) |
 |                                 |
 | **uri** (_string_)              |
 |                                 |

  

# HTTP Methods

#### Options

This method is a request for information about the communication options available on the chain between the client and the server identified by the **Request-URI**. The method allows the client to determine the options and (or) the requirements associated with a resource without initiating any resource retrieval

#### GET

This method retrieves whatever information identified by the Request-URI. If the Request-URI refers to a data processing process then the response to the GET method should contain data produced by the process, not the source code of the process procedure(-s), unless the source is the result of the process.

The GET method can become a conditional GET if the request message includes an If-Modified-Since, If-Unmodified-Since, If-Match, If-None-Match, or If-Range header field. The conditional GET method is used to reduce the network traffic specifying that the transfer of the entity should occur only under circumstances described by conditional header field(-s).

The GET method can become a partial GET if the request message includes a Range header field. The partial GET method intends to reduce unnecessary network usage by requesting only parts of entities without transferring data already held by the client.

The response to a GET request is cacheable if and only if it meets the requirements for HTTP caching.

#### HEAD

This method shares all features of GET method except that the server must not return a message-body in the response. This retrieves the metainformation of the entity implied by the request which leads to its wide usage of it for testing hypertext links for validity, accessibility, and recent modification.

The response to a HEAD request may be cacheable in the way that the information contained in the response may be used to update the previously cached entity identified by that Request-URI.

#### POST

This method requests that the origin server accept the entity enclosed in the request as a new subordinate of the resource identified by the Request-URI.

The actual action performed by the POST method is determined by the origin server and usually is Request-URI dependent.

Responses to POST method are not cacheable, unless the response includes appropriate Cache-Control or Expires header fields.

#### PUT

This method requests that the enclosed entity be stored under the supplied Request-URI. If another entity exists under specified Request-URI, the enclosed entity should be considered as an updated (newer) version of that residing on the origin server. If the Request-URI is not pointing to an existing resource, the origin server should create a resource with that URI.

If the request passes through a cache and the Request-URI identifies one or more currently cached entities, those entries should be treated as stale. Responses to this method are not cacheable.

#### TRACE

This method invokes a remote, application-layer loop-back of the request message. The final recipient of the request should reflect the message received back to the client as the entity-body of a 200 (OK) response. The final recipient is either the origin server or the first proxy or gateway to receive a Max-Forwards value of 0 in the request. A TRACE request must not include an entity.

Responses to this method MUST NOT be cached.