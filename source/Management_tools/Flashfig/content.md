## Description

Flashfig is an application for mass router configuration. It can be used by MikroTik distributors, ISPs, or any other companies who need to apply RouterOS configuration to many routers in the shortest possible time.

Flashfig applies MikroTik RouterOS **configuration** to any RouterBOARD within **3 seconds**. You can perform Flashfig on a batch of routers, the only thing you need is to **connect** RouterBOARD to a Layer 2 network running Netinstall and to **power** a Flashfig enabled RouterBOARD up.

Running Netinstall in Flashfig mode only runs on a Windows computer and Netinstall is available from the [downloads](http://www.mikrotik.com/download) page.

Flashfig mode is supported by all [RouterBOARDs](http://www.routerboard.com/). It works between a Windows computer running Netinstall with Flasfig mode enabled and a RouterBOARD in the same broadcast domain (direct Layer 2 Ethernet network connection is required).

Flashfig support is enabled on every new RouterBOARD manufactured since March 2010 by default from the factory. For older models, Flashfig can be enabled via RouterBOOT or from MikroTik RouterOS console (E.g. /system routerboard settings set boot-device=flash-boot-once-then-nand or /system routerboard settings set boot-device=flash-boot).

After Flashfig is used once on a brand new RouterBOARD, it is disabled on further boots to avoid unwanted reconfiguration at a later time. To use Flashfig a second time on the same router, you need to enable **flash-boot** in Bootloader settings.

If RouterOS _reset-configuration_ command is used later, Flashfig configuration is loaded. (To permanently overwrite, use the Netinstall process and check to apply default configuration or us -r flag in Linux-based command line).

Flashfig diagram shows the procedure of Flashfig,

![](https://help.mikrotik.com/docs/download/attachments/139526145/Flashfigdiagramm.png?version=1&modificationDate=1658906901697&api=v2)

## Flashfig Example

This is a step-by-step example of how to use the Flashfig process to apply a chosen MikroTik RouterOS configuration to a 'factory fresh' RouterBOARD.

#### Introduction

Flashfig is an option available from within the Netinstall program, on the latest ROS releases Flashfig is removed from Netinstall and can be downloaded as a standalone application from [https://mikrotik.com/download](https://mikrotik.com/download)

![](https://help.mikrotik.com/docs/download/attachments/139526145/Flashfig.png?version=1&modificationDate=1658907016942&api=v2)

#### Requirements

The Windows computer must be equipped with the following ports and contain the following files:

-   A working Ethernet port;
-   Valid .rsc file(s) with MikroTik RouterOS configuration similar to an export/import file. (Be aware of the text editor's treatment of CR/LF characters and test that the config has no errors when normally applied onto an identical version of RouterOS before applying via Flashfig as run-time errors will not be visible!);
-   Always use the latest NetInstall/Flashfig program available from the [downloads](http://www.mikrotik.com/download.html) page;

The RouterBOARD:

-   Flashfig is supported by the first-time boot of RouterBOARD;

#### Pre-Configuration

##### Windows Computer

-   Run Flashfig;
-   Prepare **.rsc** file, **.rsc** file is regular/import file, it accepts valid MikroTik RouterOS CLI commands. You can create .rsc file with any text editor program (Notepad, Notepad++, Texteditor, TextEdit, Microsoft Word, OpenOffice Writer)

![](https://help.mikrotik.com/docs/download/attachments/139526145/Flashfig2.png?version=1&modificationDate=1658907059195&api=v2)

-   Assign **Boot Client Address**, which should be an address within the same subnet as that configured on the computer's Ethernet interface,

![](https://help.mikrotik.com/docs/download/attachments/139526145/Flashfig3.png?version=1&modificationDate=1658907107861&api=v2)

-   **Browse** for **.rsc** MikroTik RouterOS configuration file to apply to the RouterBOARD, highlight the file and **Select** to approve it,

![](https://help.mikrotik.com/docs/download/attachments/139526145/Flashfig4.png?version=1&modificationDate=1658907118530&api=v2)

-   Activate Flashfig server, now it is ready to Flashfig. Note, any RouterBOARD will be flashfig'ed within the network when they are powered on with boot-device configured to **flash-boot** or **flash-boot-once-then-nand**,

![](https://help.mikrotik.com/docs/download/attachments/139526145/Flashfig5.png?version=1&modificationDate=1658907127709&api=v2)

##### RouterBOARD

-   Flashfig mode is enabled on every RouterBOARD from the factory by default, which means **no configuration** is required on RouterBOARD.

-   If Flashfig is not enabled on your router, access the RouterBOARD with Winbox/Console and set the configuration,

[?](https://help.mikrotik.com/docs/display/ROS/Flashfig#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">system</code><code class="ros constants">/routerboard/settings/</code><code class="ros functions">set </code><code class="ros value">boot-device</code><code class="ros plain">=flash-boot</code></div></div></td></tr></tbody></table>

or use a more preferable option,

[?](https://help.mikrotik.com/docs/display/ROS/Flashfig#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">system</code><code class="ros constants">/routerboard/settings/</code><code class="ros functions">set </code><code class="ros value">boot-device</code><code class="ros plain">=flash-boot-once-then-nand</code></div></div></td></tr></tbody></table>

Your router is now ready for Flashfig.

#### Connect

Connect Ether1 of RouterBOARD and Flashfig computer to the same Local Area Network. (Exceptions are RB1xxx and CCR devices which support network booting from the last ethernet port).

#### Run Flashfig

-   Plug-in power for RouterBOARD
-   Check the status on Flashfig program,

![](https://help.mikrotik.com/docs/download/attachments/139526145/Flashfig6.png?version=1&modificationDate=1658907156898&api=v2)

Messages log shows "Flashfigged" and RouterBOARD should repeatedly make the morse code sound for the character "/" ("\_..\_." and flash the LED - it is now safe to unplug / power down the router.

-   Flashfig **configuration** was applied to the RouterBOARD and it is **ready** to be used in production with this new config.

## Troubleshoot

### Flashfig Configuration is not applied

If all procedures went successfully, but RouterOS configuration from .rsc file is not applied. Add :delay 20s to \*.rsc configuration file. The reason might be, that the configuration script is executed before RouterOS is booted successfully.

### Flashfig can not find the router is not applied

Make sure that the computer on which Flashfig is running has only one network interface active.

### Not enough flash space, ignoring

Flashfig configuration maximum file size is up to 4000 bytes, otherwise program will return an error as above.