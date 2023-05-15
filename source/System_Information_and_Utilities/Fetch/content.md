# Summary

Fetch is one of the console tools in Mikrotik RouterOS. It is used to copy files to/from a network device via HTTP, FTP or SFTP (Support for SFTP added on v6.45), it can also be used to send POST/GET requests and send any kind of data to a remote server. The HTTPS protocol is supported; by default, no certificate checks are made, but setting **check-certificate** to _yes_ enables trust chain validation from the local certificate store.

# Properties

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
| ---------------------------------- | ------------------------------------------- |
| **address** (_string_; Default: )  | IP address of the device to copy file from. |
| **as-value** (_set                 | not-set_; Default: **not-set**)             | Store the output in a variable, should be used with the output property. |
| **ascii** (_yes                    | no_; Default: **no**)                       | Can be used with FTP and TFTP                                            |
| **check-certificate** (_yes        | no_; Default: **no**)                       | Enables trust chain validation from local certificate store.             |
| **dst-path** (_string_; Default: ) | Destination filename and path               |
| **host** (_string_; Default: )     |

A domain name or virtual domain name (if used on a website, from which you want to copy information). For example,

```
address=wiki.mikrotik.com host=forum.mikrotik.com
```

  
In this example the resolved ip address is the same (66.228.113.27), but hosts are different. |
| **http-method** (_|delete|get|post|put_; Default: **get**) | the HTTP method to use |
| **http-data** (_string_; Default: ) | the data, that is going to be sent, when using PUT or POST methods |
| **http-header-field** (_string_; Default: **\*empty\***) | list of all header fields and their values, in the form of `http-header-field=h1:fff,h2:yyy` |
| **keep-result** (_yes | no_; Default: **yes**) | If yes, creates an input file. |
| **mode** (_ftp|http|tftp {!} https_; Default: **http**) | Choose the protocol of connection - http, https , ftp or tftp. |
| **output** (_none|file|user_; Default: **file**) | Sets where to store the downloaded data.

-   `none` - do not store downloaded data
-   `file` - store downloaded data in a file
-   `user` - store downloaded data in the data variable

 |
| **password** (_string_; Default: **anonymous**) | Password, which is needed for authentication to the remote device. |
| **port** (_integer_; Default: ) | Connection port. |
| **src-path** (_string_; Default: ) | Title of the remote file you need to copy. |
| **upload** (_yes | no_; Default: **no**) | Only (S)FTP modes support uploads. If enabled then fetch will be used to upload files to a remote server. Requires _src-path_ and _dst-path_ parameters to be set. |
| **url** (_string_; Default: ) | URL pointing to file. Can be used instead of **address** and **src-path** parameters. |
| **user** (_string_; Default: **anonymous**) | User name, which is needed for authentication to the remote device. |

  

# Configuration Examples

The following example shows how to copy the file with filename "conf.rsc" from a device with ip address 192.168.88.2 by FTP protocol and save it as file with filename "123.rsc". User and password are needed to login into the device.

[?](https://help.mikrotik.com/docs/display/ROS/Fetch#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/tool&gt; fetch address=192.168.88.2 src-path=conf.rsc \</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros value">user</code><code class="ros plain">=admin</code> <code class="ros value">mode</code><code class="ros plain">=ftp</code> <code class="ros value">password</code><code class="ros plain">=123</code> <code class="ros value">dst-path</code><code class="ros plain">=123.rsc</code> <code class="ros value">port</code><code class="ros plain">=21</code> <code class="ros plain">\</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros value">host</code><code class="ros plain">=</code><code class="ros string">""</code> <code class="ros value">keep-result</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Example to upload file to another router:

[?](https://help.mikrotik.com/docs/display/ROS/Fetch#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/tool&gt; fetch address=192.168.88.2 src-path=conf.rsc \</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros value">user</code><code class="ros plain">=admin</code> <code class="ros value">mode</code><code class="ros plain">=ftp</code> <code class="ros value">password</code><code class="ros plain">=123</code> <code class="ros value">dst-path</code><code class="ros plain">=123.rsc</code> <code class="ros value">upload</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

Another file download example that demonstrates the usage of url property.

[?](https://help.mikrotik.com/docs/display/ROS/Fetch#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/&gt; /tool fetch url="<a href="https://www.mikrotik.com/img/netaddresses2.pdf">https://www.mikrotik.com/img/netaddresses2.pdf</a>" mode=http</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">status</code><code class="ros constants">: finished</code></div><div class="line number3 index2 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">[admin@test_host] </code><code class="ros constants">/&gt; /</code><code class="ros functions">file </code><code class="ros functions">print</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments"># NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; TYPE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; SIZE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; CREATION-TIME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">...</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">5 netaddresses2.pdf&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; .pdf </code><code class="ros functions">file </code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <code class="ros plain">11547&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; jun</code><code class="ros constants">/01/2010 11:59:51</code></div></div></td></tr></tbody></table>

## Sending information to a remote host

It is possible to use an HTTP POST request to send information to a remote server, that is prepared to accept it. In the following example, we send geographic coordinates to a PHP page:

[?](https://help.mikrotik.com/docs/display/ROS/Fetch#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/tool fetch http-method=post http-content-type="application/json" http-data="{\"lat\":\"56.12\",\"lon\":\"25.12\"}" url="<a href="https://testserver.lv/index.php">https://testserver.lv/index.php</a>"</code></div></div></td></tr></tbody></table>

In this example, the data is uploaded as a file. Important note, since the file comes from a variable, it can only be in size up to 4KB. This is a limitation of RouterOS variables.

[?](https://help.mikrotik.com/docs/display/ROS/Fetch#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/</code><code class="ros functions">export </code><code class="ros value">file</code><code class="ros plain">=export.rsc</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">:</code><code class="ros functions">global </code><code class="ros plain">data [</code><code class="ros constants">/</code><code class="ros functions">file </code><code class="ros functions">get </code><code class="ros plain">[</code><code class="ros constants">/</code><code class="ros functions">file </code><code class="ros functions">find </code><code class="ros value">name</code><code class="ros plain">=export.rsc]</code> <code class="ros plain">contents];</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">:</code><code class="ros functions">global </code><code class="ros keyword">$url</code> <code class="ros string">"<a href="https://prod-51.westeurope.logic.azure.com:443/workflows/blabla/triggers/manual/paths/invoke....">https://prod-51.westeurope.logic.azure.com:443/workflows/blabla/triggers/manual/paths/invoke....</a>"</code><code class="ros plain">;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros constants">/tool fetch mode=https http-method=</code><code class="ros functions">put </code><code class="ros value">http-data</code><code class="ros plain">=$data</code> <code class="ros value">url</code><code class="ros plain">=$url</code></div></div></td></tr></tbody></table>

## Return value to a variable

It is possible to save the result of the fetch command to a variable. For example, it is possible to trigger a certain action based on the result that an HTTP page returns. You can find a very simple example below that disables **ether2** whenever a PHP page returns "0":

[?](https://help.mikrotik.com/docs/display/ROS/Fetch#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">{</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros constants">:</code><code class="ros functions">local </code><code class="ros plain">result [</code><code class="ros constants">/tool fetch url=<a href="https://10.0.0.1/disable_ether2.php">https://10.0.0.1/disable_ether2.php</a> as-value output=user];</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros constants">:</code><code class="ros functions">if </code><code class="ros plain">(</code><code class="ros keyword">$result</code><code class="ros plain">-&gt;</code><code class="ros string">"status"</code> <code class="ros plain">=</code> <code class="ros string">"finished"</code><code class="ros plain">) </code><code class="ros value">do</code><code class="ros plain">=</code><code class="ros plain">{</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros constants">:</code><code class="ros functions">if </code><code class="ros plain">(</code><code class="ros keyword">$result</code><code class="ros plain">-&gt;</code><code class="ros string">"data"</code> <code class="ros plain">=</code> <code class="ros string">"0"</code><code class="ros plain">) </code><code class="ros value">do</code><code class="ros plain">=</code><code class="ros plain">{</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros constants">/interface ethernet </code><code class="ros functions">set </code><code class="ros plain">ether2 </code><code class="ros value">disabled</code><code class="ros plain">=yes</code><code class="ros plain">;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">} </code><code class="ros value">else</code><code class="ros plain">=</code><code class="ros plain">{</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros constants">/interface ethernet </code><code class="ros functions">set </code><code class="ros plain">ether2 </code><code class="ros value">disabled</code><code class="ros plain">=no</code><code class="ros plain">;</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">}</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">}</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">}</code></div></div></td></tr></tbody></table>

### SFTP

Since 6.45beta50 _/tool fetch_ support SFTP (SSH File Transfer Protocol) protocol:

[?](https://help.mikrotik.com/docs/display/ROS/Fetch#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] &gt; </code><code class="ros constants">/tool fetch url="s<a href="ftp://10.155.126.200/home/x86/Desktop/50MB.zip">ftp://10.155.126.200/home/x86/Desktop/50MB.zip</a>" user=x86 password=root dst-path=disk1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">status</code><code class="ros constants">: downloading</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">downloaded</code><code class="ros constants">: 1048KiB</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">total</code><code class="ros constants">: 51200KiB</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">duration</code><code class="ros constants">: 6s</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">-- [Q quit|D dump|C-z pause]</code></div></div></td></tr></tbody></table>