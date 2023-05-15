# Summary

Allows defining a set of interfaces for easier interface management in the different interface-based configuration sections such as Neighbor Discovery, Firewall, Bridge, and Internet Detect. 

# Lists

**Sub-menu:** `/interface list   `

This menu contains information about all interface lists available on the router. There are three predefined lists - _all_ (contains all interfaces), _none_ (contains no interfaces), _dynamic_ (contains dynamic interfaces), and _static_ (contains static interfaces). It is also possible to create additional interface lists.

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

|                        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **name** (_string_)    | Name of the interface list                                                                                                |
| **include** (_string_) | Defines interface list which members are included in the list. It is possible to add multiple lists separated by commas   |
| **exclude** (_string_) | Defines interface list which members are excluded from the list. It is possible to add multiple lists separated by commas |

  
Members are added to the interface list in the following order:

1.  include members are added to the interface list
2.  exclude members are removed from the list
3.  Statically configured members are added to the list

# Members

**Sub-menu:** `/interface list member`

This sub-menu contains information about statically configured interface members to each interface list. Note that dynamically added interfaces by include and exclude statements are not represented in this sub-menu.

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

|                          |
| ------------------------ | -------------------------- |
| **interface** (_string_) | Name of the interface      |
| **list** (_string_)      | Name of the interface list |