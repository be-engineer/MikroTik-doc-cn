# Introduction

Trivial File Transfer Protocol or simply TFTP is a very simple protocol used to transfer files. Each nonterminal packet is acknowledged separately.

[?](https://help.mikrotik.com/docs/display/ROS/TFTP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">ip</code><code class="ros constants">/tftp/</code></div></div></td></tr></tbody></table>

This menu contains all TFTP access rules. If in this menu are no rules, the TFTP server is not started when RouterOS boots. This menu only shows 1 additional attribute compared to what you can set when creating a rule.

# Parameters

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
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ip-address** _(required)_        | Range of IP addresses accepted as clients if empty _0.0.0.0/0_ will be used                                                                                                                                                                                                                                                                                                 |
| **allow-rollover** _(Default: No)_ | If set to _yes_ TFTP server will allow the sequence number to roll over when the maximum value is reached. This is used to enable large downloads using the TFTP server.                                                                                                                                                                                                    |
| **req-filename**                   | Requested filename as a _regular expression (regex)_ if a field is left empty it defaults to _.\*_                                                                                                                                                                                                                                                                          |
| **real-filename**                  | If **req-filename** and **real-filename** values are set and valid, the requested filename will be replaced with matched file. This field has to be set. If multiple _regex_ is specified in _req-filename_, with this field you can set which ones should match, so this rule is validated. The _real-filename_ format for using multiple _regex_ is **filename\\0\\5\\6** |
| **allow** (_default: yes_)         | To allow connection if the above fields are set. if _no_, a connection will be interrupted                                                                                                                                                                                                                                                                                  |
| **read-only** (_default: no_)      | Sets if a file can be written to, if set to "yes" write attempt will fail with error                                                                                                                                                                                                                                                                                        |
| **hits** _(read-only)_             | How many times this access rule entry has been used (read-only)                                                                                                                                                                                                                                                                                                             |

## Settings

[?](https://help.mikrotik.com/docs/display/ROS/TFTP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip/tftp/settings</code></div></div></td></tr></tbody></table>

This menu contains all TFTP settings.

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

|                                     |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **max-block-size** (_default:4096_) | Maximum accepted block size value. During the transfer negotiation phase, the RouterOS device will not negotiate a larger value than this. |

# Regexp

Req-filename field allowed regexp, allowed regexp in this field are:

**brackets ()** \- marking subsection:

```
    example 1 a(sd|fg) will match asd or afg

```

**asterisk "\*"** \- match zero or more times preceding symbol:

```
    example 1 a* will match any length name consisting purely of symbols a or no symbols at all
    example 2 .* will match any length name, also, empty field
    example 3 as*df will match adf, asdf, assdf, asssdf etc.

```

**plus "+"** will match one or more times the preceding symbol:

```
    example: as+df will match asdf, assdf etc.

```

**dot "."** \- matches any symbol:

```
    example as.f will match asdf, asbf ashf etc.

```

**square brackets \[\]** \- variation between:

```
    example as[df] will match asd and asf

```

**question mark "?"** will match one or no symbols:

```
    example asd?f will match asdf and asf

```

**caret "^"** \- used at the beginning of the line means that the line starts with;

**dollar "$"** \- means at the end of the line.

# Examples

If a file is requested return the file from the store called sata1:

[?](https://help.mikrotik.com/docs/display/ROS/TFTP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip tftp </code><code class="ros functions">add </code><code class="ros value">req-filename</code><code class="ros plain">=file.txt</code> <code class="ros value">real-filename</code><code class="ros plain">=/sata1/file.txt</code> <code class="ros value">allow</code><code class="ros plain">=yes</code> <code class="ros value">read-only</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

If we want to give out one specific _file_ no matter what the user is requesting:

[?](https://help.mikrotik.com/docs/display/ROS/TFTP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip tftp </code><code class="ros functions">add </code><code class="ros value">req-filename</code><code class="ros plain">=.*</code> <code class="ros value">real-filename</code><code class="ros plain">=/sata1/file.txt</code> <code class="ros value">allow</code><code class="ros plain">=yes</code> <code class="ros value">read-only</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

 If the user requests _aaa.bin_ or _bbb.bin_ then give them _ccc.bin_:

[?](https://help.mikrotik.com/docs/display/ROS/TFTP#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/ip tftp </code><code class="ros functions">add </code><code class="ros value">req-filename</code><code class="ros plain">=</code><code class="ros string">"(aaa.bin)|(bbb.bin)"</code> <code class="ros value">real-filename</code><code class="ros plain">=</code><code class="ros string">"/sata1/ccc.bin\\0"</code> <code class="ros value">allow</code><code class="ros plain">=yes</code> <code class="ros value">read-only</code><code class="ros plain">=yes</code></div></div></td></tr></tbody></table>

  

RouterOS receives TFTP requests, but the client gets a transfer timeout?

Some embedded clients request large block sizes and yet do not handle fragmented packets correctly. For these clients, it is recommended to set "max-block-size" on the RouterOS side or "blksize" on Client-side to the value of the smallest MTU on your network minus 32 bytes (20 bytes for IP, 8 for UDP, and 4 for TFTP) and more if you use IP options on your network.