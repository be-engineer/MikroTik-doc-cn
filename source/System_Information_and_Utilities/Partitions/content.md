# Summary

Partitioning is supported on ARM, ARM64, MIPS, TILE, and PowerPC RouterBOARD type devices.

It is possible to partition NAND flash, allowing to install own OS on each partition and specify primary and fallback partitions.

If a partition should fail for some reason (failed upgrade, problematic configuration introduced, software problem), the next partition will boot instead. This can be used as an interactive backup where you keep a verified working installation and upgrade only some secondary partition. If you upgrade your configuration, and it proves to be good, you can use the "save config" button to copy it over to other partitions. 

 Repartitioning of the NAND requires the latest bootloader version

Minimum partition sizes:

-   32MB on MIPS
-   40MB on PowerPC
-   48MB on TILE

The maximum number of allowed partitions is 8.

[?](https://help.mikrotik.com/docs/display/ROS/Partitions#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros plain">[admin@1009up] &gt; </code><code class="ros constants">/partitions/</code><code class="ros plain">print</code></div><div class="line number2 index1 alt1" data-bidi-marker="true"><code class="ros plain">Flags</code><code class="ros constants">: A - ACTIVE; R - RUNNING</code></div><div class="line number3 index2 alt2" data-bidi-marker="true"><code class="ros plain">Columns</code><code class="ros constants">: NAME, FALLBACK-TO, VERSION, SIZE</code></div><div class="line number4 index3 alt1" data-bidi-marker="true"><code class="ros comments"># NAME FALL VERSION SIZE</code></div><div class="line number5 index4 alt2" data-bidi-marker="true"><code class="ros plain">0 AR part0 next RouterOS v7.1beta4 Dec</code><code class="ros constants">/15/2020 15:55:11 128MiB</code></div></div></td></tr></tbody></table>

# Commands

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

|                                         |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **repartition** (_integer_)             | Will reboot the router and reformat the NAND, leaving only active partition.                                         |
| **copy-to** (_<partition>_)             | Clone **running** OS with the config to specified partition. Previously stored data on the partition will be erased. |
| **save-config-to** (_<partition>_)      | Clone **running-config** on a specified partition. Everything else is untouched.                                     |
| **restore-config-from** (_<partition>_) | Copy config from specified partition to **running** partition                                                        |

# Properties

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

|                                |
| ------------------------------ | --------------------- |
| **name** (_string_; Default: ) | Name of the partition |
| **fallback-to** (_etherboot    | next                  | <partition-name>_; Default: **next**) | What to do if an active partition fails to boot: |

-   **etherboot** - switch to etherboot
-   **next'** - try next partition
-   fallback to the specified partition

 |

## Read-only

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

|                             |
| --------------------------- | --------------------------------------------------- |
| **active** (_yes            | no_)                                                | Partition is active         |
| **running** (_yes           | no_)                                                | Currently running partition |
| **size** (_integer\[MiB\]_) | Partition size                                      |
| **version** (_string_)      | Current RouterOS version installed on the partition |