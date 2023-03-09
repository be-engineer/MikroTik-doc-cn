# Summary

MQTT is an open OASIS and ISO standard lightweight, publish-subscribe network protocol that transports messages between devices. A typical MQTT communication topology consists of:

-   an MQTT publisher → a device that sends information to the server;
-   an MQTT broker → a server where the data is stored;
-   an MQTT subscriber → a device that reads/monitors the data published on the server.

Currently, RouterOS can act as an MQTT publisher and you can also run an MQTT broker via the [container](https://help.mikrotik.com/docs/display/ROS/Container) feature.

# Configuration

**Sub-menu:** `/iot mqtt`

_**note**:_  **iot** package is required.

IoT package is available with RouterOS version 6.48.3. You can get it from our [download page](https://mikrotik.com/download) - under "Extra packages".

You can find more application examples for MQTT publish scenarios below:

a) [MQTT/HTTPS example with AWS cloud platform](https://help.mikrotik.com/docs/pages/viewpage.action?pageId=63045633)

b) [MQTT example with Azure cloud platform](https://help.mikrotik.com/docs/display/UM/MQTT+and+Azure+configuration)

c) [MQTT and ThingsBoard configuration](https://help.mikrotik.com/docs/display/ROS/MQTT+and+ThingsBoard+configuration)

The settings shown in the examples above apply to any RouterOS device. The only thing to keep in mind is that AWS's and Azure's examples showcase scripts that structure MQTT messages out of the Bluetooth payloads and, currently, only the [KNOT](https://mikrotik.com/product/knot) supports Bluetooth. For RouterOS devices other than KNOT, you will need to change the script per your requirements (for example, you can use a basic script from this guide).

## Broker

To add a new broker, run the following command:

[?](https://help.mikrotik.com/docs/display/ROS/MQTT#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot mqtt brokers </code><code class="ros functions">add</code></div></div></td></tr></tbody></table>

Configurable properties are shown below:

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
 | ------------------------------------- | --------------------------------------------------------------- |
 | **address** (_IP                      | hostname_; Default: )                                           | IP address or hostname of the broker |
 | **certificate** (_string_; Default: ) | The certificate that is going to be used for the SSL connection |
 |                                       |

**client-id** (_string_; Default: )

 | A unique ID used for the connection. The broker uses this ID to identify the client. |
| 

**name** (_string_; Default: )

 | Descriptive name of the broker |
| 

**password** (_string_; Default: )

 | Password for the broker (if required by the broker) |
| 

**port** (_integer:_0..4294967295__; Default: **1883**)

 | Network port used by the broker |
| 

**ssl** (_yes | no_; Default: **no**)

 | Secure Socket Layer configuration |
| **username** (_string_; Default: ) | Username for the broker (if required by the broker) |

## Publish

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

 |                                  |
 | -------------------------------- | ----------------------------------------------- |
 | **broker** (_string_; Default: ) | Select the broker, where to publish the message |
 |                                  |

**message** (_string_; Default: )

 | The message that you wish to publish to the broker |
| 

**qos** (_integer:_0..4294967295__; Default: **0**)

 | Quality of service parameter, as defined by the broker |
| 

**retain** (_yes | no_; Default: **no**)

 | Whether to retain the message or to discard it if no one is subscribed to the topic. This parameter is defined by the broker. |
| 

**topic** (_string_; Default: )

 | Topic, as defined by the broker |

An example of MQTT publish would look like this:

[?](https://help.mikrotik.com/docs/display/ROS/MQTT#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot mqtt&gt; publish broker=AWS topic=my/test/topic message="{\"temperature\":15}"</code></div></div></td></tr></tbody></table>

In this case, **AWS** is a broker's name that was configured in the broker section, **my/test/topic** is a topic (as it is configured on the server-side/on the broker itself) and **"{\\"temperature\\":15}"** is the message you wish to publish (in this specific example, in the JSON format). Retain and QoS parameters are optional - both are defined by the broker.

In this scenario, our broker is [AWS](https://aws.amazon.com/iot/).

In order to see the displayed message, you need to subscribe to the topic beforehand (in our case, **my/test/topic**).

Once you are subscribed to the topic, you can publish the message. AWS (or any other broker) should display the message:

![](https://help.mikrotik.com/docs/download/attachments/46759978/image2021-5-26_8-34-1.png?version=1&modificationDate=1622007236280&api=v2)

  

You can also use scripts (to automate the process). For example, you can run a script like this:

> \# Required packages: iot
> 
> ################################ Configuration ################################  
> \# Name of an existing MQTT broker that should be used for publishing  
> :local broker "AWS"
> 
> \# MQTT topic where the message should be published  
> :local topic "my/test/topic"
> 
> #################################### System ###################################  
> :put ("\[\*\] Gathering system info...")  
> :local cpuLoad \[/system resource get cpu-load\]  
> :local freeMemory \[/system resource get free-memory\]  
> :local usedMemory (\[/system resource get total-memory\] - $freeMemory)  
> :local rosVersion \[/system package get value-name=version \\  
>     \[/system package find where name ~ "^routeros"\]\]  
> :local model \[/system routerboard get value-name=model\]  
> :local serialNumber \[/system routerboard get value-name=serial-number\]  
> :local upTime \[/system resource get uptime\]
> 
> #################################### MQTT #####################################  
> :local message \\  
>     "{\\"model\\":\\"$model\\",\\  
>                 \\"sn\\":\\"$serialNumber\\",\\  
>                 \\"ros\\":\\"$rosVersion\\",\\  
>                 \\"cpu\\":$cpuLoad,\\  
>                 \\"umem\\":$usedMemory,\\  
>                 \\"fmem\\":$freeMemory,\\  
>                 \\"uptime\\":\\"$upTime\\"}"
> 
> :log info "$message";  
> :put ("\[\*\] Total message size: $\[:len $message\] bytes")  
> :put ("\[\*\] Sending message to MQTT broker...")  
> /iot mqtt publish broker=$broker topic=$topic message=$message  
> :put ("\[\*\] Done")

The script collects the data from the RouterOS device (model name, serial number, RouterOS version, current CPU, used memory, free memory, and uptime) and publishes the message (the data) to the broker in the JSON format:

![](https://help.mikrotik.com/docs/download/attachments/46759978/image2021-5-26_9-33-13.png?version=1&modificationDate=1622010788772&api=v2)

Do not forget to change the "Configuration" part of the script based on your settings.