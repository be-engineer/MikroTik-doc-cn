# Introduction

The spectral scan can scan all frequencies supported by your wireless card, and plot them directly in the console. The exact frequency span depends on the card. Allowed ranges on r52n: \[4790; 6085\], \[2182; 2549\].

A wireless card can generate 4us long spectral snapshots for any 20mhz wide channel. This is considered a single spectral sample.

To improve data quality spectrum is scanned with 10mhz frequency increments, which means doubled sample coverage at each specific frequency (considering 20mhz wide samples).

Currently, is NOT supported for Atheros 802.11ac chips (e.g. QCA98xx, IPQ-4018). See [https://mikrotik.com/products](https://mikrotik.com/products) determine the wireless chip on your device.

# Console

## Spectral History

![](https://help.mikrotik.com/docs/download/attachments/139526162/Spectral-history.png?version=1&modificationDate=1658911224048&api=v2)

[?](https://help.mikrotik.com/docs/display/ROS/Spectral+scan#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface wireless spectral-history &lt;wireless interface name&gt;</code></div></div></td></tr></tbody></table>

  

Plots spectrogram. Legend and frequency ruler is printed every 24 lines. Numbers in the ruler correspond to the value at their leftmost character position. Power values that fall in different ranges are printed as different colored characters with the same foreground and background color, so it is possible to copy and paste the terminal output of this command.

-   _value_ \-- select value that is plotted on the output. 'interference' is special as it shows detected interference sources (affected by the 'classify-samples' parameter) instead of power readings, and cannot be made audible;
-   _interval_ \-- interval at which spectrogram lines are printed;
-   _duration_ \-- terminate command after a specified time. default is indefinite;
-   _buckets_ \-- how many values to show in each line of a spectrogram. This value is limited by the number of columns in the terminal. It is useful to reduce this value if using 'audible';
-   _average-samples_ \-- Number of 4us spectral snapshots to take at each frequency, and calculate average and maximum energy over them. (default 10);
-   _classify-samples_ \-- Number of spectral snapshots taken at each frequency and processed by the interference classification algorithm. Generally, more samples give more chance to spot certain types of interference (default 50);
-   _range_ \--
    -   2.4ghz - scan the whole 2.4ghz band;
    -   5ghz - scan the whole 5ghz band;
    -   current-channel - scan current channel only (20 or 40 MHz wide);
    -   range - scan specific range;

-   _audible=yes_ \-- play each line as it is printed. There is a short silence between the lines. Each line is played from left to right, with higher frequencies corresponding to higher values in the spectrogram.

## Spectral Scan

![](https://help.mikrotik.com/docs/download/attachments/139526162/Spectral-scan.png?version=1&modificationDate=1658911497641&api=v2)

[?](https://help.mikrotik.com/docs/display/ROS/Spectral+scan#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/interface wireless spectral-</code><code class="ros functions">scan </code><code class="ros plain">&lt;wireless interface name&gt;</code></div></div></td></tr></tbody></table>

Continuously monitor spectral data. This command uses the same data source as 'spectral-history', and thus shares many parameters.

Each line displays one spectrogram bucket -- frequency, the numeric value of power average, and a character graphic bar. A bar shows average power value with ':' characters and average peak hold with '.' characters. Maximum is displayed as a lone floating ':' character.

-   _show-interference_ \-- add a column that shows detected interference sources;

Types of possibly classified interference:

-   Bluetooth-headset
-   Bluetooth-stereo
-   cordless-phone
-   microwave-oven
-   CWA
-   video-bridge
-   wifi

# The Dude

The Dude is a free network monitoring and management program by MikroTik. You [can download it here](http://www.mikrotik.com/thedude.php).

The Dude has a built-in capability to run graphical Spectral Scan from any of your RouterOS devices with a supported wireless card. Simply select this device in your Dude map, right click and choose Tools -> Spectral Scan.

![](https://help.mikrotik.com/docs/download/attachments/139526162/Spectral1.png?version=1&modificationDate=1658911632889&api=v2)

This will bring up the Spectral Scan GUI with various options and different view modes:

![](https://help.mikrotik.com/docs/download/attachments/139526162/Spectral-scan-dude.png?version=1&modificationDate=1658911642856&api=v2)