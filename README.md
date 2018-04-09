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
-------------------            -------------------
| RESTful API -|  |            | RESTful API -|  |
|              |  |            |              |  |
| [ Active ]   |  | -> sync -> | [ Standby ]  |  |
|              |  |            |              |  |
|-----         |  |            |-----         |  |
| DB | <-------|  |            | DB | <-------|  |
-------------------            -------------------
    \                               /
        \                       /
            \               /
                \       /
                    \/
----------------------------------------------
|   |   |   |   |   Backends     |   |   |   |
----------------------------------------------
```

Lifecycle

```
AP mode -> Master fails -> Auto-failover (promote the slave to master) -> Manually turn the failed master to new slave -> |
^                                                                                                                         |
|-------------------------------------------------------------------------------------------------------------------------|
```

# Milestones

1. Prototype of AP mode stateful RESTful API Server (1 ~ 2 weeks)
2. Implementation of Backends client librabry (1 ~ 2 weeks)
3. RESTful API Spec and DB Schema (4 ~ 8 weeks)
4. Implementation of RESTful API (2 ~ 4 weeks)

# Milestone 1 :: AP mode stateful RESTful API Server

vip : keepalived

RESTful API Framework : Falcon v1.4.x (TBD)

DB replication & failover solution (TBD)

* ~~SQLite + rsync~~
* MySQL + mysqlfailover

OS : CentOS 7.x (TBD)

References

* Why don't we use rsync + SQLite as our DB replication & failover solution? see https://serverfault.com/questions/89329/rsync-sqlite-database

# Milestone 2 :: Implementation of Backends client librabry

Backends List

* 1 ~ N WAF
* 1 ~ N FW
* N SWITCH
* 1 Neo?
* 1 ~ N Neutron Server?

# Milestone 3 :: RESTful API Spec, DB Schema, Sub-sequence APIs

RESTful API Category

* init 
* user

CMP Use Cases and Sub-sequence APIs (one case one sequence diagram)

* ?

# Milestone 4 :: Implementation of RESTful API
