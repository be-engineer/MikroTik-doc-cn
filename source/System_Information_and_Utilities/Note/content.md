## Summary

[?](https://help.mikrotik.com/docs/display/ROS/Note#)

<table border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="code"><div class="container" title="Hint: double-click to select code"><div class="line number1 index0 alt2" data-bidi-marker="true"><code class="ros constants">/system note</code></div></div></td></tr></tbody></table>

  
The system note feature allows you to assign arbitrary text notes or messages that will be displayed on each login right after the banner. For example, you may distribute warnings between system administrators this way, or describe what does that particular router actually do. To configure system note, you may upload a plain text file named **sys-note.txt** on the router's FTP server, or, additionally, edit the settings in this menu

## Properties

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
| ------------------------------ | ---------------------------- |
| **note** (_string_; Default: ) | Note that will be displayed. |
| **show-at-login** (_yes        | no_; Default: **yes**)       | whether to show system note on each login |

  

## Example

It is possible to add multi-line notes using an embedded text editor ( _/system note edit note_), for example, add ASCII art to your home router:

  

```
system/note/set note=
```

```
                                       .&                                                                            @&   @&                                                                         @@   @#                                                                           @@&                                                                      ,      @@@      .                                                               @@@@@@@@@@@@@@@@@                                                                      @@@                                                                             @@@                                                                             @@@                                                                ,@           @@@           &                                                   @@@@          @@@          @@@@                                                  @@           @@@           @(                                                    &@@         @@@         @@@                                                       @@@@@     @@@     &@@@&                                                            &@@@@@@@@@@@@@@@&                                                                     @@@@@             
```