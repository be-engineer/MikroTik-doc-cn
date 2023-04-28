# Summary

It is possible to connect the GSM modem to the RouterOS device and use it to send and receive SMS messages. RouterOS lists such modem as a serial port that appears in the '_/port print_' listing. GSM standard defines AT commands for sending SMS messages and defines how messages should be encoded in these commands.

'advanced tools package provides command `'_/tool sms send_'` that uses standard GSM AT commands to send SMS.

# Sending

[?](https://help.mikrotik.com/docs/display/ROS/SMS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/tool sms </code><code class="ros functions">send</code></div></div></td></tr></tbody></table>

## **Example**

Sending command for ppp interface:

[?](https://help.mikrotik.com/docs/display/ROS/SMS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/tool sms </code><code class="ros functions">send </code><code class="ros plain">usb3 </code><code class="ros string">"20000000"</code> <code class="ros plain">\ </code><code class="ros value">message</code><code class="ros plain">=</code><code class="ros string">"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#\$%^&amp;*(){}[]\"'~"</code></div></div></td></tr></tbody></table>

For LTE interface use LTE interface name in the port field:

[?](https://help.mikrotik.com/docs/display/ROS/SMS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/tool sms </code><code class="ros functions">send </code><code class="ros plain">lte1 </code><code class="ros string">"20000000"</code> <code class="ros plain">\ </code><code class="ros value">message</code><code class="ros plain">=</code><code class="ros string">"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#\$%^&amp;*(){}[]\"'~"</code></div></div></td></tr></tbody></table>

| 
Parameter

 | 

Description

 |     |
 | --- |  |
 |     |

Parameter

 | 

Description

 |                             |
 | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | **port** (_string_)         | Name of port from _/port_ list that GSM modem is attached to.                                                                                                                    |
 | **phone-number** (_string_) | Recepient phone number. Allowed characters are "0123456789\*#abc". If first character is "+" then phone number type is set to _international_, otherwise it is set to _unknown_. |
 | **channel** (_integer_)     | Which modem channel to use for sending.                                                                                                                                          |
 | **message** (_string_)      | Message contents. It is encoded using GSM 7 encoding (UCS2 currently is not supported), so message length is limited to 160 characters (characters ^{}\\\[\]~                    |
 | **smsc** (_string_)         |
 |                             |
 | **type** (_string_)         | If set to _class-0_, then send class 0 SMS message. It is displayed immedeately and not stored in phone.                                                                         |

# USSD messages

USSD (Unstructured Supplementary Service Data) messages can be used to communicate with mobile network provider to receive additional information, enabling additional services or adding funds to prepaid cards. USSD messages can be processed by using AT commands (commands can differ or even may be blocked on some modems).

**3G or GSM network modes must be activated to use this functionality**, as it's not supported under LTE only mode (**R11e-LTE** modem auto switches to 3G mode to send out USSD message).

PDU (Protocol Data Unit) message and its decrypted version is printed under LTE debug logging.

## **Example**

Check if LTE debug logging is active:

[?](https://help.mikrotik.com/docs/display/ROS/SMS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system logging </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - invalid, * - default</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros comments"># TOPICS ACTION PREFIX</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">0 * </code><code class="ros functions">info </code><code class="ros plain">memory</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">1 * </code><code class="ros functions">error </code><code class="ros plain">memory</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">2 * </code><code class="ros functions">warning </code><code class="ros plain">memory</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">3 * </code><code class="ros functions">critical </code><code class="ros plain">echo</code></div></div></td></tr></tbody></table>

If there is no logging entry add it by running this command:

[?](https://help.mikrotik.com/docs/display/ROS/SMS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system logging </code><code class="ros functions">add </code><code class="ros value">topics</code><code class="ros plain">=lte,!raw</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/system logging </code><code class="ros plain">print</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disabled, I - invalid, * - default</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros comments"># TOPICS ACTION PREFIX</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">0 * </code><code class="ros functions">info </code><code class="ros plain">memory</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">1 * </code><code class="ros functions">error </code><code class="ros plain">memory</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">2 * </code><code class="ros functions">warning </code><code class="ros plain">memory</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros plain">3 * </code><code class="ros functions">critical </code><code class="ros plain">echo</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros plain">4 lte,!raw memory</code></div></div></td></tr></tbody></table>

To recieve account status from **\*245#**

[?](https://help.mikrotik.com/docs/display/ROS/SMS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface lte at-chat lte1 input="AT+CUSD=1,\"*245#\",15"</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">output</code><code class="ros constants">: OK</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/</code><code class="ros functions">log </code><code class="ros plain">print</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">11</code><code class="ros constants">:51:20 lte,async lte1: sent AT+CUSD=1,"*245#",15</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">11</code><code class="ros constants">:51:20 lte,async lte1: rcvd OK</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">11</code><code class="ros constants">:51:23 lte,async,event +CUSD: 0,"EBB79B1E0685E9ECF4BADE9E03", 0</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">11</code><code class="ros constants">:51:23 gsm,</code><code class="ros functions">info </code><code class="ros plain">USSD</code><code class="ros constants">: konta atlikums</code></div></div></td></tr></tbody></table>

# Receiving

Since v3.24 RouterOS also supports receiving of SMS messages, and can execute scripts, and even respond to the sender.

Before router can receive SMS, relevant configuration is required in general **/tool sms** menu. Following parameters are configurable:

| 
Parameter

 | 

Description

 |     |
 | --- |  |
 |     |

Parameter

 | 

Description

 |                                              |
 | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
 | **allowed-number** (_string_; Default: "")   | Sender number that will be allowed to run commands, must specify country code ie. +371XXXXXXX                                                                                                     |
 | **channel** (_integer_; Default: **0**)      | Which modem channel to use for receiving.                                                                                                                                                         |
 | **keep-max-sms** (_integer_; Default: **0**) | Maximum number of messages that will be saved. If you set this bigger than SIM supports, new messages will not be received! Replaced with **auto-erase** parameter starting from RouterOS v6.44.6 |
 | **auto-erase** (_yes                         | no_; Default: **no**)                                                                                                                                                                             | SIM storage size is read automatically. When **auto-erase=no** new SMS will not be received if storage is full. Set **auto-erase=yes** to delete the oldest received SMS to free space for new ones automatically. Available starting from v6.44.6 |
 | **port** (_string_; Default: (**unknown**))  | Modem port (modem can be used only by one process "/port> print" )                                                                                                                                |
 | **receive-enabled** (_yes                    | no_; Default: **no**)                                                                                                                                                                             | Must be turned on to receive messages                                                                                                                                                                                                              |
 | **secret** (_string_; Default: "")           | the secret password, mandatory                                                                                                                                                                    |

**Basic Example configuration to be able to view received messages:**

[?](https://help.mikrotik.com/docs/display/ROS/SMS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/tool sms </code><code class="ros functions">set </code><code class="ros value">receive-enabled</code><code class="ros plain">=yes</code> <code class="ros value">port</code><code class="ros plain">=lte1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">/tool/sms/</code><code class="ros functions">print</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">status</code><code class="ros constants">: running</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">receive-enabled</code><code class="ros constants">: yes</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">port</code><code class="ros constants">: lte1</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">channel</code><code class="ros constants">: 0</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">secret</code><code class="ros constants">:</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;</code><code class="ros plain">allowed-number</code><code class="ros constants">:</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">auto-erase</code><code class="ros constants">: no</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">sim-pin</code><code class="ros constants">:</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code><code class="ros plain">last-ussd</code><code class="ros constants">:</code></div></div></td></tr></tbody></table>

## **Inbox**

[?](https://help.mikrotik.com/docs/display/ROS/SMS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/tool sms inbox</code></div></div></td></tr></tbody></table>

If you have enabled the reader, you will see incoming messages in this submenu:

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

 |                        |
 | ---------------------- | --------------------------------------------------------------------------------------------- |
 | **phone** (_string_)   | Senders phone number.                                                                         |
 | **message** (_string_) | Message body                                                                                  |
 | **timestamp** (_time_) | Time when message was received. It is the time sent by operator, not the router's local time. |
 | **type** (_string_)    | Message type                                                                                  |

## **Syntax**

[?](https://help.mikrotik.com/docs/display/ROS/SMS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">:cmd SECRET script NAME [[ VAR[=VAL] ] ... ]</code></div></div></td></tr></tbody></table>

-   **SECRET** \- the password
-   **NAME** \- name of the script that's available in "/system script"
-   **VAR** \- variables that will be passed to the script (can be passed as VAR or as VAR=value), separated by spaces.

Other things to remember:

-   \*Parameters can be put into quotes "VAR"="VAL" if necessary.
-   \*Escaping of values is not supported (VAR="\\"").
-   \*Combined SMS are not supported, every SMS will be treated separately
-   \* 16Bit unicode messages are not supported
-   \* SMS are decoded with the standard GSM7 alphabet, so you can't send in other encodings, otherwise it will be decoded incorrectly

## **Examples**

****Wrong:****

[?](https://help.mikrotik.com/docs/display/ROS/SMS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">:cmd script mans_skripts</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">:cmd slepens script mans skripts</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">:cmd slepens script mans_skripts var=</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">:cmd slepens script mans_skripts var= a</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">:cmd slepens script mans_skripts var=a a</code></div></div></td></tr></tbody></table>

**Right:**

[?](https://help.mikrotik.com/docs/display/ROS/SMS#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">:cmd slepens script mans_skripts</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros constants">:cmd slepens script "mans skripts"</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros constants">:cmd slepens script mans_skripts var</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros constants">:cmd slepens script mans_skripts var=a</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros constants">:cmd slepens script mans_skripts var="a a"</code></div></div></td></tr></tbody></table>

# Debugging

_/tool sms send_ command is logging data that is written and read. It is logged with tags _gsm,debug,write_ and _gsm,debug,read_ For more information see system logging.

# Implementation details

_AT+CMGS_ and _AT+CMGF_ commands are used. Port is acquired for the duration of the command and cannot be used concurently by another RouterOS component. Message sending process can take a long time, it times out after a minute and after two seconds during initial AT command exchange.