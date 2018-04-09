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

# Milesstones

1. Prototype of AP mode stateful RESTful API Server
2. Implementation of Backends client librabry
3. RESTful API Spec and DB Schema

# Milestone 1 :: AP mode stateful RESTful API Server

# Milestone 2 :: Implementation of Backends client librabry

Backends List

* 1 ~ N WAF
* 1 ~ N FW
* N SWITCH
* 1 Neo?
* 1 ~ N Neutron Server?

# Milestone 3 :: RESTful API Spec and DB Schema

CMP Use Cases

* ?
