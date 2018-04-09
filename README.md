# Arch.

```
----------------------------------------------
|                   CMP                      |
----------------------------------------------
                      |
                    -----
                    |vip|
                    -----
                /           \
            /                   \
        /                           \
-----------------            -----------------
| RESTful API   |            | RESTful API   |
|               |            |               |
| [ Active ]    | -> sync -> | [ Standby ]   |
|               |            |               |
|-----          |            |-----          |
| DB |          |            | DB |          |
-----------------            -----------------
    \                               /
        \                       /
            \               /
                \       /
                    \/
----------------------------------------------
|   |   |   |   |   Backends     |   |   |   |
----------------------------------------------
```

# Milestones

1. Prototype of AP mode stateful RESTful API Server (1 ~ 2 weeks)
2. Implementation of Backends client librabry (1 ~ 2 weeks)
3. RESTful API Spec and DB Schema (4 ~ 8 weeks)

# Milestone 1 :: AP mode stateful RESTful API Server

vip : keepalived

RESTful API Framework : Falcon v1.4.x (TBD)

DB : SQLite (TBD)

sync : rynsc (TBD)

OS : CentOS 7.x (TBD)

# Milestone 2 :: Implementation of Backends client librabry

Backends List

* 1 ~ N WAF
* 1 ~ N FW
* N SWITCH
* 1 Neo?
* 1 ~ N Neutron Server?

# Milestone 3 :: RESTful API Spec and DB Schema

API Category

* init 
* user

CMP Use Cases

* ?
