# Branding

RouterOS allows slight system customization with the help of a branding package. This is a special system package, which you can generate from within your [mikrotik.com account](https://mikrotik.com/client/), in the account section "Branding maker". The resulting file will have a .dpk extension and can be installed by all the same means as an .npk package. The generated package can be installed in any RouterOS version. To install the package in a device you simply need to upload it and reboot the router, you can also use Netinstall tool for the same effect.

## ASCII logo

This is the text logo shown when logging into the command line interface, i.e. Telnet, SSH, Winbox Terminal. The ASCII logo you can create right there in the browser, or copy from any other plaintext editor. Make sure it is not wider than the form in the branding maker page, or your logo will be distorted.

## Default webpage

You can customize the default RouterOS information page, which shows up when accessing the router IP address, and a password is set on the device. When making the HTML file, you can use these variables:

-   %version% will change to the router's current version
-   %host% will change to the router's IP address. Use these variables in the Telnet link, or in the header.

The file must be named "index2.html". Make sure you use properly nested HTML to make your page compatible with all browsers. You can also upload images or JavaScript files, they must reference to the same path as the index file, no custom folder names can be used.

If you wish to only change the MikroTik logo, and not upload the whole HTML file, the name of the default image is mikrotik\_logo.png, uploading another file with the same name, will overwrite the original.

## Other values

-   **Router name**: this is the Identity value in RouterOS, it can only be one word, don't use spaces or special characters there.
-   **Company URL**: this is the value that appears in the console when you connect to your MikroTik device.
-   **Manual URL**: documentation link which opens with a button in Webfig in the web interface.
-   **LCD logo**: this will be displayed on devices equipped with LCD screen. Requirements for logo: no more than 160px width and no more than 72px height. CCR series have white (0xffffff) background, 2011 series have black (0x000000) background.
-   **Default configuration**: Note that when using the default configuration file, the configuration is appended when simply installing the package, but after using system reset, only the configuration in your file will be used, all other standard default config will not be used during reset. The file must be a text/rsc file with one RouterOS command per line. You can use an export file from the console as a starting point, but we recommend only leaving the exact commands you want to run. This configuration will be kept even after the RouterOS reset.
-   **Skins**: For skins, a file your\_file\_name.json must be uploaded into the "skins" directory. 

In order to apply particular skin to a specific user group, you don't need to log into the router to do that. You can do it with branding by uploading a Default configuration file.  
Or set the skin for the user group manually after reboot.

-   **Custom files**: RouterOS 6.48.3 and above also supports uploading of custom files, they will be simply copied into a folder named "branding" and will be accessible from within RouterOS.