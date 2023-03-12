# 介绍

屏蔽电缆安装设施（塔和桅杆）以及天线和路由器本身必须正确接地，所有外部天线电缆上必须安装避雷器（靠近天线或天线本身），防止设备损坏和人员受伤。注意，如果不接地，避雷器不会有任何效果。

使用带有抗腐蚀接头的1 AWG（直径7mm）电线接地。一定要检查使用的接地设施是否确实是功能性的（而不是在一些场地上存在的装饰性接地）。对于较小的设备，可以使用更细的电线。

1. 只应该用屏蔽和户外使用的以太网电缆，磁屏蔽层要通过屏蔽RJ-45连接器或焊接到RJ45或接地线的额外电线接地。
2. 接地线应连接到RouterBOARD（到电路板固定在室外箱体上的安装点），此线连接到塔的底部，与塔的连接符合标准。天线接地线连接在RouterBOARD户外箱附近，此线可与RouterBOARD接地线相同。
3. 不建议使用以太网端口防雷器，因为大多数防雷器不适合用于PoE（它们会缩短PoE供电）。如果使用保护器，可以放置在室外机箱上，在那里连接RouterBOARD和接地垫。

户外机箱上的接地线连接螺丝示例。

![](https://help.mikrotik.com/docs/download/thumbnails/53444613/image2021-1-26_11-31-35.png?version=1&modificationDate=1611653495315&api=v2)

![](https://help.mikrotik.com/docs/download/attachments/53444613/image2021-1-26_11-29-10.png?version=1&modificationDate=1611653350390&api=v2)

## RouterBOARD设备的ESD保护

1. 三个箭头标志以太网端口内部的接地，屏蔽电缆通过金属以太网连接器把屏蔽层连接到这两个接地引脚。
2. 中间的箭头指向端口内的金属板，将接地引脚连接到电路板上。板子需要在安装孔处接地（当你把板子安装在机箱内时，把接地线放在螺丝上）。任何电涌都会从接地引脚到接地板，再到电路板，然后再到接地。
3. 两个独立的箭头显示了电路板上的ESD保护芯片-在没有屏蔽线的情况下，用来保护CPU和电路板的其他部分。

如果只用屏蔽线，而不把板子接地，保护效果就不太好。需要做这两件事才能成功。可能的方法见下文，建议采用方案1。

![](https://help.mikrotik.com/docs/download/attachments/53444613/image2021-1-26_11-35-26.png?version=1&modificationDate=1611653727262&api=v2)

## RouterBOARD接地

有两种方法，其中一种更有效。

有屏蔽的PoE连接器:

![](https://help.mikrotik.com/docs/download/thumbnails/53444613/image2021-1-26_11-45-18.png?version=1&modificationDate=1611654318712&api=v2)

1. **用屏蔽电缆+板子接地**。如果把接地连接到RB711的安装点（或SXT门内的安装环），不一定要在屏蔽电缆的另一端对设备进行接地。只要使用屏蔽电缆就可以了。也不需要特殊的PoE。这是防止所有ESD的最佳选择。
2. **只用屏蔽电缆**。如果不能把RB711/SXT/本身接地，可以把屏蔽电缆另一端的设备（交换机、路由器等）接地。如果要用PoE，则需要用连接器周围有金属屏蔽的注入器，因为它可以用屏蔽电缆。不建议用这种方法，最好将电路板本身也接地（选项1）。

## 上述方法的说明

方法1（屏蔽电缆+设备接地）：

![](https://help.mikrotik.com/docs/download/attachments/53444613/Option-1.jpg?version=1&modificationDate=1611654917863&api=v2)

方法2（只有屏蔽电缆）:

![](https://help.mikrotik.com/docs/download/attachments/53444613/Option-2.jpg?version=1&modificationDate=1611654924756&api=v2)

如果PSE为MikroTik设备供电，不该把正极连接到PE上使用。否则可能会造成短路，伤害你和设备。

即使不把室外的无线设备接地，而只使用屏蔽电缆，仍然应该把所连接的设备在室内接地。例如，交换机、路由器板或PC。
