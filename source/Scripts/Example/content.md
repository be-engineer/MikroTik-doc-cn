# 介绍

本节包含一些有用的脚本，展示了所有可用的脚本特性。本节中使用的脚本示例使用最新的3.x版本。

# 创建文件

不能直接创建文件，但是有一个解决方案:

```shell
/file print file=myFile
/file set myFile.txt contents=""
```

# 检查接口上的IP是否改变

有些提供商提供动态IP地址。此脚本将比较动态IP地址是否更改。

```shell
:global currentIP;
 
:local newIP [/ip address get [find interface="ether1"] address];
 
:if ($newIP != $currentIP) do={
    :put "ip address $currentIP changed to $newIP";
    :set currentIP $newIP;
}
```

# 剥离掩码

如果需要一个没有子网掩码的IP地址(例如在防火墙中使用它)，而" / IP address get [id] address"会返回IP地址和子网掩码，因此这个脚本很有用。

```shell
:global ipaddress 10.1.101.1/24
 
:for i from=( [:len $ipaddress] - 1) to=0 do={
    :if ( [:pick $ipaddress $i] = "/") do={
        :put [:pick $ipaddress 0 $i]
    }
}
```

另一种更简单的方法:

```shell
:global ipaddress 10.1.101.1/24
:put [:pick $ipaddress 0 [:find $ipaddress "/"]]
```

# 解析主机名

许多用户要求在radius服务器、防火墙规则等方面使用DNS名称而不是IP地址。

下面是一个如何解析RADIUS服务器IP的示例。

假设已经配置了radius服务器:

````shell
/radius
add address=3.4.5.6 comment=myRad
````

下面是一个解析IP地址的脚本，将解析的IP地址与配置的IP地址进行比较，如果不相等，则替换它:

```shell
/system script add name="resolver" source= {
 
:local resolvedIP [:resolve "server.example.com"];
:local radiusID [/radius find comment="myRad"];
:local currentIP [/radius get $radiusID address];
 
:if ($resolvedIP != $currentIP) do={
   /radius set $radiusID address=$resolvedIP;
   /log info "radius ip updated";
}
 
}
```

将此脚本添加到调度器中，例如每5分钟运行一次

```shell
/system scheduler add name=resolveRadiusIP on-event="resolver" interval=5m
```

# 在多个文件中写入简单的队列统计

考虑队列命名是“一些文本”。可以通过“."后面的最后一个数字来搜索队列。

```shell
:local entriesPerFile 10;
:local currentQueue 0;
:local queuesInFile 0;
:local fileContent "";
#determine needed file count
:local numQueues [/queue simple print count-only] ;
:local fileCount ($numQueues / $entriesPerFile);
:if ( ($fileCount * $entriesPerFile) != $numQueues) do={
   :set fileCount ($fileCount + 1);
}
 
#remove old files
/file remove [find name~"stats"];
 
:put "fileCount=$fileCount";
 
:for i from=1 to=$fileCount do={
#create file
   /file print file="stats$i.txt";
#clear content
   /file set [find name="stats$i.txt"] contents="";
 
   :while ($queuesInFile < $entriesPerFile) do={
     :if ($currentQueue < $numQueues) do={
         :set currentQueue ($currentQueue +1);
         :put $currentQueue ;
         /queue simple
         :local internalID [find name~"\\.$currentQueue\$"];
         :put "internalID=$internalID";
         :set fileContent ($fileContent . [get $internalID target-address] . \
           " " . [get $internalID total-bytes] . "\r\n");
     }
     :set queuesInFile ($queuesInFile +1);
      
   }
   /file set "stats$i.txt" contents=$fileContent;
   :set fileContent "";
   :set queuesInFile 0;
 
}
```

# 生成备份并通过电子邮件发送

该脚本生成一个备份文件并将其发送到指定的电子邮件地址。邮件主题包含路由器的名称、当前日期和时间。

注意，在使用此脚本之前，必须先配置SMTP服务器。有关配置选项，请参见 [/tool e-mail](https://help.mikrotik.com/docs/display/ROS/E-mail) 。
  
```shell
/system backup save name=email_backup
/tool e-mail send file=email_backup.backup to="me@test.com" body="See attached file" \
   subject="$[/system identity get name] $[/system clock get time] $[/system clock get date] Backup")
```

备份文件中包含密码等敏感信息。因此，要访问生成的备份文件，脚本或调度程序必须具有“敏感”策略。

使用string作为函数

```shell
:global printA [:parse ":local A; :put \$A;" ];  
$printA
```

# 检查带宽并添加限制

该脚本检查接口上的下载是否超过512kbps，如果是，则添加队列以将速度限制为256kbps。

```shell
:foreach i in=[/interface find] do={
    /interface monitor-traffic $i once do={
        :if ($"received-bits-per-second" > 0 ) do={
            :local tmpIP [/ip address get [/ip address find interface=$i] address] ;
#            :log warning $tmpIP ;
            :for j from=( [:len $tmpIP] - 1) to=0 do={
                :if ( [:pick $tmpIP $j] = "/") do={
                    /queue simple add name=$i max-limit=256000/256000 dst-address=[:pick $tmpIP 0 $j] ;
                }
            }
        }
    }
}
```
  

# 阻止访问特定网站

如果想阻止某些网站，但不想使用web代理，可以用这个脚本。

本例查看DNS缓存中的“Rapidshare”和“youtube”条目，并将ip添加到名为“restricted”的地址列表中。在开始之前，必须设置一个路由器来捕获所有DNS请求:

```shell
/ip firewall nat
add action=redirect chain=dstnat comment=DNS dst-port=53 protocol=tcp to-ports=53
add action=redirect chain=dstnat dst-port=53 protocol=udp to-ports=53
```

添加防火墙

```shell
/ip firewall filter
add chain=forward dst-address-list=restricted action=drop
```

现在可以编写一个脚本每30秒运行一次。

脚本代码:

```shell
:foreach i in=[/ip dns cache find] do={
    :local bNew "true";
    :local cacheName [/ip dns cache all get $i name] ;
#    :put $cacheName;
 
    :if (([:find $cacheName "rapidshare"] >= 0) || ([:find $cacheName "youtube"] >= 0)) do={
 
        :local tmpAddress [/ip dns cache get $i address] ;
#   :put $tmpAddress;
 
# if address list is empty do not check
        :if ( [/ip firewall address-list find list="restricted" ] = "") do={
            :log info ("added entry: $[/ip dns cache get $i name] IP $tmpAddress");
            /ip firewall address-list add address=$tmpAddress list=restricted comment=$cacheName;
        } else={
            :foreach j in=[/ip firewall address-list find list="restricted"] do={
                :if ( [/ip firewall address-list get $j address] = $tmpAddress ) do={
                    :set bNew "false";
                }
            }
            :if ( $bNew = "true" ) do={
                :log info ("added entry: $[/ip dns cache get $i name] IP $tmpAddress");
                /ip firewall address-list add address=$tmpAddress list=restricted comment=$cacheName;
            }
        }
    }
}
```

# 解析文件添加ppp

该脚本要求文件中的条目采用以下格式:

username,password,local\_address,remote\_address,profile,service

例如:

```shell
janis,123,1.1.1.1,2.2.2.1,ppp_profile,myService
juris,456,1.1.1.1,2.2.2.2,ppp_profile,myService
aija,678,1.1.1.1,2.2.2.3,ppp_profile,myService
```

```shell
:global content [/file get [/file find name=test.txt] contents] ;
:global contentLen [ :len $content ] ;
 
:global lineEnd 0;
:global line "";
:global lastEnd 0;
 
 
:do {
       :set lineEnd [:find $content "\r\n" $lastEnd ] ;
       :set line [:pick $content $lastEnd $lineEnd] ;
       :set lastEnd ( $lineEnd + 2 ) ;
 
       :local tmpArray [:toarray $line] ;
    :if ( [:pick $tmpArray 0] != "" ) do={
    :put $tmpArray;
         /ppp secret add name=[:pick $tmpArray 0] password=[:pick $tmpArray 1] \
             local-address=[:pick $tmpArray 2] remote-address=[:pick $tmpArray 3] \
             profile=[:pick $tmpArray 4] service=[:pick $tmpArray 5];
}
} while ($lineEnd < $contentLen)
```

# 检测新日志条目

这个脚本检查一个新的日志条目是否被添加到一个特定的缓冲区。

在这个例子中使用PPPoE日志:

```shell
/system logging action
add name="pppoe"
/system logging
add action=pppoe topics=pppoe,info,!ppp,!debug
```

日志缓冲区看起来类似这样:

```shell
[admin@mainGW] > /log print where buffer=pppoe
13:11:08 pppoe,info PPPoE connection established from 00:0C:42:04:4C:EE
```

现在可以编写一个脚本来检测是否添加了新条目。

```shell
:global lastTime;
 
:global currentBuf [ :toarray [ /log find buffer=pppoe  ] ] ;
:global currentLineCount [ :len $currentBuf ] ;
:global currentTime [ :totime [/log get [ :pick $currentBuf ($currentLineCount -1) ] time   ] ];
 
:global message "";
 
:if ( $lastTime = "" ) do={
    :set lastTime $currentTime ;
    :set message [/log get [ :pick $currentBuf ($currentLineCount-1) ] message];
 
} else={
    :if ( $lastTime < $currentTime ) do={
        :set lastTime $currentTime ;
        :set message [/log get [ :pick $currentBuf ($currentLineCount-1) ] message];
    }
}
```

检测到新项后，将其保存在message变量中，以后可以使用该变量解析日志消息，例如获取PPPoE client的mac地址。

# 允许使用 [ntp.org](http://ntp.org) 池服务作为NTP

此脚本解析两个NTP服务器的主机名，将结果与当前NTP设置进行比较，如果不一致则更改地址。由于RouterOS不允许在NTP配置中使用主机名，所以要使用该脚本。用了两个脚本，第一个定义了一些在其他脚本中使用的系统变量，第二个完成基本工作:

```shell
# System configuration script - "GlobalVars"
 
:put "Setting system globals";
 
# System name
:global SYSname [/system identity get name];
 
# E-mail address to send notifications to
:global SYSsendemail "mail@my.address";
 
# E-mail address to send notifications from
:global SYSmyemail "routeros@my.address";
 
# Mail server to use
:global SYSemailserver "1.2.3.4";
 
# NTP pools to use (check www.pool.ntp.org)
:global SYSntpa "0.uk.pool.ntp.org";
:global SYSntpb "1.uk.pool.ntp.org";
```

```shell
# Check and set NTP servers - "setntppool"
 
# We need to use the following globals which must be defined here even
# though they are also defined in the script we call to set them.
:global SYSname;
:global SYSsendemail;
:global SYSmyemail;
:global SYSmyname;
:global SYSemailserver;
:global SYSntpa;
:global SYSntpb;
 
# Load the global variables with the system defaults
/system script run GlobalVars
 
# Resolve the two ntp pool hostnames
:local ntpipa [:resolve $SYSntpa];
:local ntpipb [:resolve $SYSntpb];
 
# Get the current settings
:local ntpcura [/system ntp client get primary-ntp];
:local ntpcurb [/system ntp client get secondary-ntp];
 
# Define a variable so we know if anything's changed.
:local changea 0;
:local changeb 0;
 
# Debug output
:put ("Old: " . $ntpcura . " New: " . $ntpipa);
:put ("Old: " . $ntpcurb . " New: " . $ntpipb);
 
# Change primary if required
:if ($ntpipa != $ntpcura) do={
    :put "Changing primary NTP";
    /system ntp client set primary-ntp="$ntpipa";
    :set changea 1;
    }
 
# Change secondary if required
:if ($ntpipb != $ntpcurb) do={
    :put "Changing secondary NTP";
    /system ntp client set secondary-ntp="$ntpipb";
    :set changeb 1;
    }
 
# If we've made a change, send an e-mail to say so.
:if (($changea = 1) || ($changeb = 1)) do={
    :put "Sending e-mail.";
    /tool e-mail send \
        to=$SYSsendemail \
        subject=($SYSname . " NTP change") \
        from=$SYSmyemail \
        server=$SYSemailserver \
        body=("Your NTP servers have just been changed:\n\nPrimary:\nOld: " . $ntpcura . "\nNew: " \
          . $ntpipa . "\n\nSecondary\nOld: " . $ntpcurb . "\nNew: " . $ntpipb);
    }
```

调度器条目:

```shell
/system scheduler add \
  comment="Check and set NTP servers" \
  disabled=no \
  interval=12h \
  name=CheckNTPServers \
  on-event=setntppool \
  policy=read,write,test \
  start-date=jan/01/1970 \
  start-time=16:00:00
```

# 其他脚本

- [Dynamic_DNS_Update_Script_for_EveryDNS](https://wiki.mikrotik.com/wiki/Dynamic_DNS_Update_Script_for_EveryDNS "Dynamic DNS Update Script for EveryDNS")
- [Dynamic_DNS_Update_Script_for_ChangeIP.com](https://wiki.mikrotik.com/wiki/Dynamic_DNS_Update_Script_for_ChangeIP.com "Dynamic DNS Update Script for ChangeIP.com")
- [UPS Script](https://wiki.mikrotik.com/wiki/UPS_scripts#version_for_ROS_3.x "UPS scripts")