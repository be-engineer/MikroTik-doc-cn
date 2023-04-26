# SSH Server

RouterOS has built in SSH server that is enabled by default and is listening for incoming connections on port TCP/22. It is possible to change the port and disable the server under [Services](https://help.mikrotik.com/docs/display/ROS/Services) menu.

## Properties

**Sub-menu:** `/ip ssh   `

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

 |                                       |
 | ------------------------------------- | --------------------- |
 | **allow-none-crypto** (_yes           | no_; Default: **no**) | Whether to allow connection if cryptographic algorithms are set to none.                      |
 | **always-allow-password-login** (_yes | no_; Default: **no**) | Whether to allow password login at the same time when public key authorization is configured. |
 | **forwarding-enabled** (_both         | local                 | no                                                                                            | remote_; Default: **no**) | Allows to control which SSH forwarding method to allow: |

-   no - SSH forwarding is disabled;
-   local - Allow SSH clients to originate connections from the server(router), this setting controls also dynamic forwarding;
-   remote - Allow SSH clients to listen on the server(router) and forward incoming connections;
-   both - Allow both local and remote forwarding methods.

 |
| **host-key-size** (_1024 | 1536 | 2048 | 4096 | 8192_; Default: **2048**) | What RSA key size to use when host key is being regenerated. |
| **strong-crypto** (_yes | no_; Default: **no**) | Use stronger encryption, HMAC algorithms, use bigger DH primes and disallow weaker ones:

-   prefer 256 and 192 bit encryption instead of 128 bits;
-   disable null encryption;
-   prefer sha256 for hashing instead of sha1;
-   disable md5;
-   use 2048bit prime for Diffie Hellman exchange instead of 1024bit.

 |

**Commands**

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

 |                                         |
 | --------------------------------------- | ----------------------------------------------------------------------------- |
 | **export-host-key** (_key-file-prefix_) | Export public and private RSA/DSA keys to files. Command takes one parameter: |

-   **key-file-prefix** - used prefix for generated files, for example, prefix 'my' will generate files 'my\_rsa', 'my\_rsa.pub' etc.

 |
| **import-host-key** (_private-key-file_) | Import and replace private DSA/RSA key from specified file. Command takes one parameter:

-   **private-key-file** - name of the private RSA/DSA key file

 |
| **regenerate-host-key** () | Generated new and replace current set of private keys (DSA, RSA) on the router. Be aware that previously imported keys might stop working. |

## Enabling PKI authentication

Example of importing public key for user _admin_

[Generate SSH keys on the client device](https://help.mikrotik.com/docs/display/ROS/SSH#SSH-Log-inusingRSApublic/privatekey) (the device you will connect from). Upload the public SSH key to the router and import it.

[?](https://help.mikrotik.com/docs/display/ROS/SSH#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user ssh-keys </code><code class="ros functions">import </code><code class="ros value">public-key-file</code><code class="ros plain">=id_rsa.pub</code> <code class="ros value">user</code><code class="ros plain">=admin</code></div></div></td></tr></tbody></table>

# SSH Client

**Sub-menu:** `/system ssh`

## **Simple log-in to remote host**

It is able to connect to remote host and initiate ssh session. IP address supports both IPv4 and IPv6.

[?](https://help.mikrotik.com/docs/display/ROS/SSH#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system ssh 192.168.88.1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/system ssh 2001:db8:add:1337::beef</code></div></div></td></tr></tbody></table>

In this case user name provided to remote host is one that has logged into the router. If other value is required, then _user=<username>_ has to be used.

[?](https://help.mikrotik.com/docs/display/ROS/SSH#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system ssh 192.168.88.1 user=lala</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/system ssh 2001:db8:add:1337::beef user=lala</code></div></div></td></tr></tbody></table>

## **Log-in from certain IP address of the router**

For testing or security reasons it may be required to log-in to other host using certain source address of the connection. In this case _src-address=<ip address>_ argument has to be used. Note that IP address in this case supports both, IPv4 and IPv6.

[?](https://help.mikrotik.com/docs/display/ROS/SSH#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system ssh 192.168.88.1 src-address=192.168.89.2</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/system ssh 2001:db8:add:1337::beef src-address=2001:db8:bad:1000::2</code></div></div></td></tr></tbody></table>

in this case, ssh client will try to bind to address specified and then initiate ssh connection to remote host.

## **Log-in using RSA public/private key**

Example of importing private key for user _admin_

First of all, export currently generated SSH keys to a file:

[?](https://help.mikrotik.com/docs/display/ROS/SSH#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip ssh export-host-key key-file-prefix=admin</code></div></div></td></tr></tbody></table>

Two files _admin\_rsa_ and _admin\_rsa.pub_ will be generated. The pub file needs to be trusted on the SSH server side ([how to enable SSH PKI on RouterOS](https://help.mikrotik.com/docs/display/ROS/SSH#SSH-EnablingPKIauthentication)) The private key has to be added for the particular user.

[?](https://help.mikrotik.com/docs/display/ROS/SSH#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/user ssh-keys private </code><code class="ros functions">import </code><code class="ros value">user</code><code class="ros plain">=admin</code> <code class="ros value">private-key-file</code><code class="ros plain">=admin_rsa</code></div></div></td></tr></tbody></table>

Only user with full rights on the router can change 'user' attribute value under _/user ssh-keys private_

After the public key is installed and trusted on the SSH server, a PKI SSH session can be created.

[?](https://help.mikrotik.com/docs/display/ROS/SSH#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system ssh 192.168.1.1</code></div></div></td></tr></tbody></table>

## **Executing remote commands**

To execute remote command it has to be supplied at the end of log-in line

[?](https://help.mikrotik.com/docs/display/ROS/SSH#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system ssh 192.168.88.1 "/ip address print"</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">/system ssh 192.168.88.1 command="/ip address print"</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/system ssh 2001:db8:add:1337::beef "/ip address print"</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">/system ssh 2001:db8:add:1337::beef command="/ip address print"</code></div></div></td></tr></tbody></table>

_If the server does not support pseudo-tty (ssh -T or ssh host command), like mikrotik ssh server, then it is not possible to send multiline commands via SSH_

For example, sending command `"/ip address \n add address=1.1.1.1/24"` to MikroTik router will fail.

If you wish to execute remote commands via **scripts** or **scheduler**, use command **ssh-exec**.

# SSH exec

**Sub-menu:** `/system ssh-exec`

Command _ssh-exec_ is a non-interactive ssh command, thus allowing to execute commands remotely on a device via scripts and scheduler.

## **Retrieve information**

The command will return two values:

-   **exit-code**: returns 0 if the command execution succeeded
-   **output**: returns the output of remotely executed command

  
**Example:** Code below will retrieve interface status of ether1 from device 10.10.10.1 and output the result to "Log"

[?](https://help.mikrotik.com/docs/display/ROS/SSH#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">:</code><code class="ros functions">local </code><code class="ros plain">Status ([</code><code class="ros constants">/system ssh-exec address=10.10.10.1 user=remote command=":</code><code class="ros functions">put </code><code class="ros plain">([</code><code class="ros constants">/interface ethernet </code><code class="ros functions">monitor </code><code class="ros plain">[</code><code class="ros functions">find </code><code class="ros plain">where </code><code class="ros value">name</code><code class="ros plain">=ether1]</code> <code class="ros plain">once as-value]-&gt;\"status\")" as-value]-&gt;</code><code class="ros string">"output"</code><code class="ros plain">)</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">:</code><code class="ros functions">log </code><code class="ros functions">info </code><code class="ros keyword">$Status</code></div></div></td></tr></tbody></table>

For security reasons, plain text password input is not allowed. To ensure safe execution of the command remotely, use SSH PKI authentication for users on both sides.

  

the user group and script policy executing the command requires **test** permission