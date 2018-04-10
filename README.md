# Scope

* relay API call from CMP to backends (one to one. DO NOT issue subsequent APIs i.e. DO NOT control workflow !!!)
* record the relationship between CMP object and backend object

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
AP mode -> Master fails (unplanned outage) -> Auto-failover (promote the slave to master) -> Manually turn the failed master to new slave -> |
^       \                                   /                                                                                                |
|        \ -> Planned outage for master -> /                                                                                                 |
|                                                                                                                                            |
|--------------------------------------------------------------------------------------------------------------------------------------------|
```

Notice

* The unplanned outage may lose 1 or 2 transacation(s).
* CMP need implement some sort of retry during the failover.

# Milestones

1. Prototype of AP mode stateful RESTful API Server (1 ~ 2 weeks)
2. Implementation of Backends client librabry (1 ~ 2 weeks)
3. Definition of CMP Use Cases, RESTful API Spec, DB Schema, Backend APIs (4 ~ 8 weeks)
4. Implementation of RESTful API (2 ~ 4 weeks)

# Milestone 1 :: Prototype of AP mode stateful RESTful API Server

vip : keepalived

RESTful API Framework : Falcon v1.4.x (TBD)

DB replication & failover solution (TBD)

* ~~SQLite + rsync~~
* MySQL + mysqlfailover
* MySQL + keepalived script

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

# Milestone 3 :: Definition of CMP Use Cases, RESTful API Spec, DB Schema, Backend APIs

CMP Use Cases

* TBD
* TBD
* TBD

RESTful API Spec

* Category 1 :: init .. priority 2 (out of scope)
* Category 2 :: user .. priority 1
  * TBD
  * TBD
  * TBD

DB Schema

* TBD
* TBD
* TBD

Backend APIs ~~(one use case one sequence diagram)~~

* TBD
* TBD
* TBD

# Milestone 4 :: Implementation of RESTful API
