## LoRa card installation

LtAP LTE kit will be used as example in this guide

Open your routers case. Once you have removed all the screws carefully move the upper case to the left side, as the LTE antennas are attached to the inner side of it.

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/1.png?version=1&modificationDate=1609848720368&api=v2)

  

Insert R11e-LoRa card into the mini-PCIe slot and apply two screws to the threaded inserts.

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/OpenCaseNoCard.jpeg?version=1&modificationDate=1609922446595&api=v2)

  

Attach antenna to the card (UFL connector) 

In this case UFL → SMA cable is also used, as the LtAP's case has a specific slot for it.

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/OpenCase.jpeg?version=1&modificationDate=1609922460528&api=v2)

  

Once the previous steps are done, you can close the routers case and move on to configuration.

## Configuration

### GUI setup

Connect to your router via Winbox or WebFig.

Winbox can be downloaded in the link given below:

[https://mikrotik.com/download](https://mikrotik.com/download)

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/WinboxLogin.png?version=2&modificationDate=1609922552358&api=v2)

  

It is Highly recommended to upgrade your RouterOS version to the latest available. Installing the version will perform a reboot.

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/rosUpgrade.png?version=1&modificationDate=1609921627894&api=v2)

  

Download extra packages specifically for your routers architecture and rOS version. You can see the type of your routers architecture at the top of Winbox window or in System →  Resources → Architecture Name

[https://mikrotik.com/download](https://mikrotik.com/download)

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/ExtraPackages.png?version=1&modificationDate=1609923306859&api=v2)

  

Once the package is downloaded and extracted, upload the LoRa package to your router. It can be done via drag & drop as well. It should appear in the files folder after the upload is complete, reboot your router (System → Reboot) to install the package.

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/LoraUpload.png?version=3&modificationDate=1609929801527&api=v2)

  

After the reboot, the package should be visible in the Package list

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/LoRaInstalled.png?version=1&modificationDate=1609929836867&api=v2)

  

Check if the LoRa gateway has initialized, If not, check if the USB Type is set to Mini-PCIe

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/LoraPackageVisible.png?version=2&modificationDate=1609932721368&api=v2)

  

Once the gateway has shown up select it, choose Network Servers from the default ones or add your own and enable it

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/Server.png?version=2&modificationDate=1609940527272&api=v2)

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/LoraEnabling.png?version=3&modificationDate=1609940543598&api=v2)

  

Navigate to Traffic tab to monitor the surrounding nodes sending requests.

  

![](https://help.mikrotik.com/docs/download/attachments/50692141/Traffic.png?version=2&modificationDate=1609933802611&api=v2)

  

This concludes basic installation and configuration of LoRa mini-PCIe cards. For additional settings check: [General Properties](https://help.mikrotik.com/docs/display/ROS/General+Properties)
