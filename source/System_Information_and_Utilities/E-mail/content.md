-   [Properties](https://help.mikrotik.com/docs/display/ROS/E-mail#Email-Properties)
-   2[Sending Email](https://help.mikrotik.com/docs/display/ROS/E-mail#Email-SendingEmail)
-   3[Basic examples](https://help.mikrotik.com/docs/display/ROS/E-mail#Email-Basicexamples)

An E-mail tool is a utility that allows sending e-mails from the router. The tool can be used to send regular configuration backups and exports to a network administrator.

Email tool uses only plain authentication and TLS encryption. Other methods are not supported.

___

# Properties

[?](https://help.mikrotik.com/docs/display/ROS/E-mail#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/tool e-mail</code></div></div></td></tr></tbody></table>

This submenu allows setting SMTP server that will be used.

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

|                                                       |
| ----------------------------------------------------- |  |
| **address** (_IP/IPv6 address_; Default: **0.0.0.0**) |

SMTP server's IP address.

 |
| **from** (_string_; Default: **<>**) | Name or email address that will be shown as a receiver. |
| **password** (_string_; Default: **""**) | Password used for authenticating to an SMTP server. |
| **port** (_integer\[0..65535\]_; Default: **25**) | SMTP server's port. |
| **tls** (_no|yes|starttls_; Default: **no**) | Whether to use TLS encryption:

-   yes - sends STARTTLS and drops the session if TLS is not available on the server
-   no \- do not send STARTTLS
-   starttls \- sends STARTTLS and continue without TLS if a server responds that TLS is not available

 |
| **user** (_string_; Default: **""**) | The username used for authenticating to an SMTP server. |
| 

**vrf** (_VRF name_; default value: **main**)

 | Set VRF on which service is creating outgoing connections. |

  

**Note:** All server's configurations (if specified) can be overridden by send command.

___

# Sending Email

[?](https://help.mikrotik.com/docs/display/ROS/E-mail#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/tool e-mail </code><code class="ros functions">send</code></div></div></td></tr></tbody></table>

Send command takes the following parameters:

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

|                                             |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **body** (_string_; Default: )              | The actual body of the email message                                                                                     |
| **cc** (_string_; Default: )                | Send a copy to listed recipients. Multiple addresses allowed, use "," to separate entries                                |
| **file** (_File\[,File\]_; Default: )       | List of the file names that will be attached to the mail separated by a comma.                                           |
| **from** (_string_; Default: )              | Name or email address which will appear as the sender. If a not specified value from the server's configuration is used. |
| **password** (_string_; Default: )          | Password used to authenticate to an SMTP server. If a not specified value from the server's configuration is used.       |
| **port** (_integer\[0..65535\]_; Default: ) | Port of SMTP server. If not specified, a value from the server's configuration is used.                                  |
| **server** (_IP/IPv6 address_; Default: )   | Ip or IPv6 address of SMTP server. If not specified, a value from the server's configuration is used.                    |
| **tls** (_yes                               | no                                                                                                                       | starttls_; Default: **no**) | Whether to use TLS encryption: |

-   yes - sends STARTTLS and drops the session if TLS is not available on the server
-   no \- do not send STARTTLS
-   starttls \- sends STARTTLS and continue without TLS if a server responds that TLS is not available

 |
| **subject** (_string_; Default: ) | The subject of the message. |
| **to** (_string_; Default: ) | Destination email address. Single address allowed. |
| **user** (_string_; Default: ) | The username used to authenticate to an SMTP server. If not specified, a value from the server's configuration is used. |

___

# Basic examples

**This example will show how to send an email with configuration export every 24hours.**

1\. Configure SMTP server

[?](https://help.mikrotik.com/docs/display/ROS/E-mail#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@MikroTik] </code><code class="ros constants">/tool e-mail&gt; </code><code class="ros functions">set </code><code class="ros value">server</code><code class="ros plain">=10.1.1.1</code> <code class="ros value">port</code><code class="ros plain">=25</code> <code class="ros value">from</code><code class="ros plain">=</code><code class="ros string">"router@mydomain.com"</code></div></div></td></tr></tbody></table>

2\. Add a new script named "export-send":

[?](https://help.mikrotik.com/docs/display/ROS/E-mail#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/</code><code class="ros functions">export </code><code class="ros value">file</code><code class="ros plain">=export</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/tool e-mail </code><code class="ros functions">send </code><code class="ros value">to</code><code class="ros plain">=</code><code class="ros string">"config@mydomain.com"</code> <code class="ros value">subject</code><code class="ros plain">=</code><code class="ros string">"$[/system identity get name] export"</code> <code class="ros plain">\</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros value">body</code><code class="ros plain">=</code><code class="ros string">"$[/system clock get date] configuration file"</code> <code class="ros value">file</code><code class="ros plain">=export.rsc</code></div></div></td></tr></tbody></table>

3\. Add scheduler to run our script:

[?](https://help.mikrotik.com/docs/display/ROS/E-mail#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system scheduler </code><code class="ros functions">add </code><code class="ros value">on-event</code><code class="ros plain">=</code><code class="ros string">"export-send"</code> <code class="ros value">start-time</code><code class="ros plain">=00:00:00</code> <code class="ros value">interval</code><code class="ros plain">=24h</code></div></div></td></tr></tbody></table>

  

**Send e-mail to a server using TLS/SSL encryption. For example, Google mail requires that.**

After the Google mail added **a new security policy** that **does not allow 3d-party devices to authenticate** **using** your standard **Gmail** **password** → you need to generate a 16-digit passcode ("App" password) and use it instead of your Gmail password. To configure this, navigate to the "**Security>Signing in to Google**" section settings and:

-   **Enable 2-Step Verification;**
-   **Generate an App password**.

Use the newly generated App password in the "set password=**mypassword**" setting shown below.

1\. configure a client to connect to the correct server:

[?](https://help.mikrotik.com/docs/display/ROS/E-mail#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/tool e-mail</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">address</code><code class="ros plain">=smtp.gmail.com</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">port</code><code class="ros plain">=465</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">tls</code><code class="ros plain">=yes</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">from</code><code class="ros plain">=myuser@gmail.com</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">user</code><code class="ros plain">=myuser</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros functions">set </code><code class="ros value">password</code><code class="ros plain">=mypassword</code></div></div></td></tr></tbody></table>

2\. send e-mail using send command:

[?](https://help.mikrotik.com/docs/display/ROS/E-mail#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/tool e-mail </code><code class="ros functions">send </code><code class="ros value">to</code><code class="ros plain">=myuser@anotherdomain.com</code> <code class="ros value">subject</code><code class="ros plain">=</code><code class="ros string">"email test"</code> <code class="ros value">body</code><code class="ros plain">=</code><code class="ros string">"email test"</code></div></div></td></tr></tbody></table>

-   无标签

概览

内容工具