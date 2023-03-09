Once you have installed the lora package on your router and created an account on `[The Things Network](https://thethingsnetwork.org) you can set up a running gateway`

-   Login into your account and go to Console and select Gateways

![](https://help.mikrotik.com/docs/download/attachments/16351627/L1.png?version=1&modificationDate=1582031630567&api=v2)

  

-   Select __register gateway__ and fill in the blank spaces. Gateway EUI can be found in your lora interface

![](https://help.mikrotik.com/docs/download/attachments/16351627/L5.png?version=2&modificationDate=1582034145426&api=v2)

  

-   You will have to manually add the Network Servers, or you can upgrade your router to the stable version **6.48.2** and these servers will be added automatically (highly recommended)  
    [https://wiki.mikrotik.com/wiki/Manual:Upgrading\_RouterOS](https://wiki.mikrotik.com/wiki/Manual:Upgrading_RouterOS)

![](https://help.mikrotik.com/docs/download/attachments/16351627/image2021-5-19_9-22-15.png?version=1&modificationDate=1621405335830&api=v2)

  

/lora servers

add address=eu1.cloud.thethings.industries down-port=1700 name="TTS Cloud (eu1)" up-port=1700  
add address=nam1.cloud.thethings.industries down-port=1700 name="TTS Cloud (nam1)" up-port=1700  
add address=au1.cloud.thethings.industries down-port=1700 name="TTS Cloud (au1)" up-port=1700

  

![](https://help.mikrotik.com/docs/download/attachments/16351627/image2021-5-18_12-9-23.png?version=1&modificationDate=1621328963704&api=v2)

-   After everything is filled press Register Gateway at the bottom of the page. If you have set everything accordingly to the previous steps you should see that your lora gateway is now connected

![](https://help.mikrotik.com/docs/download/attachments/16351627/L9.png?version=4&modificationDate=1582035206074&api=v2)

-   At this point everything is set and you have a working lora gateway. You can monitor incoming packets in Traffic section

![](https://help.mikrotik.com/docs/download/attachments/16351627/L10.png?version=1&modificationDate=1582035498832&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/16351627/L11.png?version=1&modificationDate=1582035719531&api=v2)

  

\*Later this year, The Things Network will be migrating to a new version of network server, called [The Things Stack](https://console.cloud.thethings.network/).