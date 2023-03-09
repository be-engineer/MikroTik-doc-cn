_**note**: In order to access GPIO settings, make sure that **iot** [package](https://help.mikrotik.com/docs/display/ROS/Packages) is installed beforehand._

You can find more information about GPIO following the [link](https://en.wikipedia.org/wiki/General-purpose_input/output).

GPIO stands for General-Purpose Input/Output. It is a digital signal pin/pins on the routerboard that allows you to send/receive the signal. It can be useful in different scenarios, like:

1.  Measuring voltage through ADC input
2.  Reading 0 and 1 signal received from another device - "dry contact"
3.  Controlling connected relays by sending logical 0 or 1 signal to the pin

## RouterOS configuration

_**note**:_ GPIO settings are available only using CLI.

**Sub-menu:** `/iot gpio`

GPIO settings are divided into:

-   analog (/iot gpio analog)
-   digital (/iot gpio digital)

_**note**:_ in our examples, we are using [KNOT](https://mikrotik.com/product/knot) as a reference device. Other devices may have a different pinout but the same principles apply.

Please note that long-term (6.47.10) and stable (6.48.3) versions, you have to use "/system gpio", command structure remains the same as in "/iot gpio" examples, aside from "analog" and "digital" sub-menus, which were added in later versions. Versions 6.49beta54+ and RouterOS v7, use "/iot gpio" sub-menu.

### /iot gpio analog

_**note**:_ please check on a product page whether your hardware supports analog input or not.

In the "analog" setting you can measure voltages on the analog input/ADC input pins:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot gpio analog&gt; </code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments"># NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; VALUE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; OFFSET</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0 pin2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0mV&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0mV</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1 pin3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 32mV&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0mV</code></div></div></td></tr></tbody></table>

"OFFSET" can be used to manually compensate voltage drop on the wires. "VALUE" is measured with:

`value = adc_input + offset`

, where adc\_input is the voltage on the pin.

"OFFSET" configuration example is shown below:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot gpio analog&gt; </code><code class="ros functions">set </code><code class="ros plain">pin2 offset&nbsp;</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Offset </code><code class="ros constants">::= [-]Num[mV]</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;&nbsp;</code><code class="ros plain">Num </code><code class="ros constants">::= -2147483648..2147483647&nbsp;&nbsp;&nbsp; (integer number)</code></div><div class="line number5 index4 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number6 index5 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot gpio analog&gt; </code><code class="ros functions">set </code><code class="ros plain">pin2 offset 2&nbsp;&nbsp;</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot gpio analog&gt; </code><code class="ros functions">print </code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments"># NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; VALUE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; OFFSET</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0 pin2&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2mV&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2mV</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1 pin3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0mV&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0mV</code></div></div></td></tr></tbody></table>

### /iot gpio digital

In the "digital" section you can send/receive a logical 0 or 1 signal using the digital output/input pins (output pins are "open drain"):

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot gpio digital&gt; </code><code class="ros functions">print </code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disab</code><code class="ros plain">led</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments">#&nbsp;&nbsp; NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DIRECTION OUTPUT INPUT SCRIPT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;&nbsp; pin5&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; input&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1&nbsp;&nbsp; pin4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; output&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">2&nbsp;&nbsp; pin6&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; output&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;</code></div></div></td></tr></tbody></table>

"DIRECTION" for the pin can be either "input" (a pin that can receive the signal) or "output" (a pin that can send the signal).

When the pin's direction is set to "output", you can configure the "OUTPUT" value. Changing the "OUTPUT" value sends the signal to the pin.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot gpio digital&gt; </code><code class="ros functions">set </code><code class="ros plain">pin4 </code><code class="ros value">output</code><code class="ros plain">=</code></div><div class="line number2 index1 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Output </code><code class="ros constants">::= 0 | 1</code></div><div class="line number4 index3 alt1" data-bidi-marker="true">&nbsp;</div><div class="line number5 index4 alt2" data-bidi-marker="true">&nbsp;</div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot gpio digital&gt; </code><code class="ros functions">set </code><code class="ros plain">pin4 </code><code class="ros value">output</code><code class="ros plain">=1</code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot gpio digital&gt; </code><code class="ros functions">print </code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disab</code><code class="ros plain">led</code></div><div class="line number9 index8 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments">#&nbsp;&nbsp; NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DIRECTION OUTPUT INPUT SCRIPT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number10 index9 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;&nbsp; pin5&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; input&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;</code></div><div class="line number11 index10 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1&nbsp;&nbsp; pin4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; output&nbsp;&nbsp;&nbsp; 1&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number12 index11 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">2&nbsp;&nbsp; pin6&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; output&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;</code></div></div></td></tr></tbody></table>

The "SCRIPT" field allows you to configure a script, that will be initiated whenever the "INPUT" or "OUTPUT" value changes (from 0 to 1 or from 1 to 0).

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot gpio digital&gt; </code><code class="ros functions">set </code><code class="ros plain">pin4 </code><code class="ros value">script</code><code class="ros plain">=script1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot gpio digital&gt; </code><code class="ros functions">set </code><code class="ros plain">pin5 </code><code class="ros value">script</code><code class="ros plain">=</code><code class="ros string">"/system .."</code>&nbsp;&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot gpio digital&gt; </code><code class="ros functions">print </code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disab</code><code class="ros plain">led</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments">#&nbsp;&nbsp; NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DIRECTION OUTPUT INPUT SCRIPT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;&nbsp; pin5&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; input&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; </code><code class="ros constants">/system ..&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1&nbsp;&nbsp; pin4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; output&nbsp;&nbsp;&nbsp; 1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; script1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number8 index7 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">2&nbsp;&nbsp; pin6&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; output&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;</code></div></div></td></tr></tbody></table>

## Different scenarios

### Controlling relays

One of the scenarios for the GPIO implementation is "controlling other relays" using digital output pins. Basically, sending "0" or "1" signal to the unit that is connected to the pin. To automate the process, you can use a [scheduler](https://wiki.mikrotik.com/wiki/Manual:System/Scheduler), which will run the script at specific times.

For example, you can add the first [script](https://help.mikrotik.com/docs/display/ROS/Scripting) (a single line shown below) and name it "output=0":

> /iot gpio digital set pin4 output=0

Then add a second script (a single line shown below) and name it "output=1":

> /iot gpio digital set pin4 output=1

Having both scripts, you can configure a schedule:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/system scheduler&gt; </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=run-30s</code> <code class="ros value">interval</code><code class="ros plain">=30s</code> <code class="ros value">on-event</code><code class="ros plain">=</code><code class="ros string">"output=0"</code></div></div></td></tr></tbody></table>

The schedule configuration shown above will run the script with the name "output=0", every 30 seconds.

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/system scheduler&gt; </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=run-45s</code> <code class="ros value">interval</code><code class="ros plain">=45s</code> <code class="ros value">on-event</code><code class="ros plain">=</code><code class="ros string">"output=1"</code></div></div></td></tr></tbody></table>

The schedule configuration shown above will run the script with the name "output=1", every 45 seconds.

As a result, the device will automatically send a signal to the 4th pin (digital output pin) with output value=0 every 30 seconds and a signal with output value=1 every 45 seconds.

You can change the scheduled time as you see fit (depending on the requirements).

### Monitoring input signal

Another scenario is to "monitor input signal" using the digital input pins. You need a script that will initiate e-mail notification or MQTT/HTTPS (fetch) publish whenever the "INPUT" value changes for the pin with the direction="input" (whenever the RouterOS device receives a signal "0 or 1" from another device connected to the pin).

_E-mail notification script:_

> /tool e-mail send to=config@[mydomain.com](http://mydomain.com) subject=\[/system identity get name\] body="$\[/iot gpio digital get pin5 input\]"

After creating a script, apply/set it to the "input" pin:

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot gpio digital&gt; </code><code class="ros functions">set </code><code class="ros plain">pin5 </code><code class="ros value">script</code><code class="ros plain">=script1</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/iot gpio digital&gt; </code><code class="ros functions">print </code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: X - disab</code><code class="ros plain">led</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros comments">#&nbsp;&nbsp; NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DIRECTION OUTPUT INPUT SCRIPT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">0&nbsp;&nbsp; pin5&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; input&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp; script1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number6 index5 alt1" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">1&nbsp;&nbsp; pin4&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; output&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; script1&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</code></div><div class="line number7 index6 alt2" data-bidi-marker="true"><code class="ros spaces">&nbsp;</code><code class="ros plain">2&nbsp;&nbsp; pin6&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; output&nbsp;&nbsp;&nbsp; 0&nbsp;&nbsp;&nbsp;&nbsp;</code></div></div></td></tr></tbody></table>

In the example above, the e-mail notification script is named "script1".

As a result, whenever the input value changes (from 0 to 1 or from 1 to 0), the script automatically initiates an e-mail notification that will display the input value in the e-mail body.

Do not forget to change the script line and configure the e-mail settings ([/tool e-mail](https://help.mikrotik.com/docs/display/ROS/E-mail)) accordingly:

> /tool e-mail send to="config@[mydomain.com](http://mydomain.com)" subject="\[/system identity get name\]"  body="$\[/iot gpio digital get pin5 input\]"

Configure the actual e-mail address that you use. You can also change the subject and the body for the mail as you see fit.

  

_MQTT publish script:_

> :local broker "name"
> 
> :local topic "topic"
> 
> :local message "{\\"inputVALUE\\":$\[/iot gpio digital get pin5 input\]}"  
> /iot mqtt publish broker=$broker topic=$topic message=$message

This script works the same way as the "_e-mail notification_" script, only when the input value changes the script initiates MQTT publish (instead of e-mail notification) and sends the input value received on the pin in the JSON format.

Do not forget to set up MQTT broker (_/iot mqtt brokers add .._) and alter a few script lines beforehand:

> :local broker "name"

The broker's "name" should be changed accordingly (you can check all created brokers and their names using CLI command /_iot mqtt brokers print_).

> :local topic "topic"

The topic should be changed as well. The topic itself is configured on the server-side, so make sure that the correct topic is used.

Do not forget to apply/set the script to pin5 (/iot gpio digital set pin5 script=script\_name), as shown in the "email notification" example above.

  

If the mechanical switch is used to send the signal to the GPIO pin, it is suggested to use the following script instead (in case the script is initiated more than once when the signal is received on the pin):

> :global gpioscriptrunning;  
> if (!$gpioscriptrunning) do={:set $gpioscriptrunning true;  
> :log info "script started - GPIO changed";  
> :do {if (\[/iot gpio digital get pin5 input\] = "0") do={/tool e-mail send to="config@[mydomain.com](http://mydomain.com)" subject=\[/system identity get name\] body="pin5 received logical 0"} else {/tool e-mail send to="config@[mydomain.com](http://mydomain.com)" subject=\[/system identity get name\]  body="pin5 received logical 1"};  
> :delay 1s;  
> :set $gpioscriptrunning false} on-error={:set $gpioscriptrunning false;  
> :log info "e-mail error, resetting script state..."}}

If the GPIO pin state changes more than once within mili/microseconds - the script above is going to make sure that e-mail notification is not sent more than once.

### Monitoring voltage

Last but not least - is to "monitor voltage" using the analog pins.  You need a script that will read/monitor voltage on schedule and then send the data via e-mail, MQTT or HTTPS (fetch).

Create a script, as shown below. In this example, we will be using MQTT publish (but you can create a similar script with "/tool e-mail .." to use e-mail notifications):

> :local broker "name"
> 
> :local topic "topic"
> 
> :local message "{\\"voltage(mV)\\":$\[/iot gpio analog get pin3 value\]}"  
> /iot mqtt publish broker=$broker topic=$topic message=$message

The script will read/measure the voltage on pin3 and publish the data to the MQTT broker.

Do not forget to set up MQTT broker (_/iot mqtt brokers add .._) and alter a few script lines beforehand:

> :local broker "name"

The broker's "name" should be changed accordingly (you can check all created brokers and their names using CLI command /_iot mqtt brokers print_).

> :local topic "topic"

The topic should be changed as well. The topic itself is configured on the server-side, so make sure that the correct topic is used.

Save the script and name it, for example, "voltagepublish". To automate the process, you can use the [scheduler](https://wiki.mikrotik.com/wiki/Manual:System/Scheduler).

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@device] </code><code class="ros constants">/system scheduler&gt; </code><code class="ros functions">add </code><code class="ros value">name</code><code class="ros plain">=run-45s</code> <code class="ros value">interval</code><code class="ros plain">=45s</code> <code class="ros value">on-event</code><code class="ros plain">=</code><code class="ros string">"voltagepublish"</code></div></div></td></tr></tbody></table>

The schedule configuration shown above will run the script every 45 seconds.
