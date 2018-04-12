# Scope

* relay API call from CMP to backends (one to one. **DO NOT issue subsequent APIs i.e. DO NOT control workflow !!!**)
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
AP mode -> Master fails (unplanned outage) -> Auto-failover (promote the slave to master) -> Manually turn the original master to new slave -> |
^       \                                                                               /                                                      |
|        \ -> Planned outage for master -> Switchover (promote the slave to master) -> /                                                       |
|                                                                                                                                              |
|----------------------------------------------------------------------------------------------------------------------------------------------|
```

Notice

* The unplanned outage may lose 1 or 2 transacation(s).
* CMP need implement some sort of retry during the failover.
* RESTful API layer need issue a query to confirm whether write commit is replicated to slave or not during the failover

# Milestones

1. Prototype of AP mode stateful RESTful API server (1 ~ 2 weeks)
2. Implementation of backends client librabry (1 ~ 2 weeks)
3. Definition of CMP use cases, RESTful API spec, DB schema, backend API (4 ~ 8 weeks)
4. Implementation of RESTful API (2 ~ 4 weeks)

# Milestone 1 :: Prototype of AP mode stateful RESTful API server

vip : keepalived v1.3.5 (the built-in python version of CentOS v7.4)

Programming Language : python v2.7.5 (the built-in python version of CentOS v7.4)

RESTful API Framework : Falcon v1.4.1

Web Server : Apache httpd v2.4.6 (the built-in httpd version of CentOS v7.4)

DB replication & failover solution

* ~~SQLite + rsync~~
* MariaDB v10.2 + MariaDB Transaction-based Async Replication + Keepalived tracking script + Keepalived notification script
  * Topology : master(rw) - - async - - > backup master(ro)

OS : CentOS v7.4

References

* [Why don't we use rsync + SQLite as our DB replication & failover solution?](https://serverfault.com/questions/89329/rsync-sqlite-database)
* [Two Node Planned Manual Failover for the MySQL Database Administrator](https://www.databasejournal.com/features/mysql/article.php/3890596/Two-Node-Planned-Manual-Failover-for-the-MySQL-Database-Administrator.htm)

# Milestone 2 :: Implementation of backends client librabry

Backends List

* 1 ~ N WAF
* 1 ~ N FW
* N SWITCH
* 1 Neo?
* 1 ~ N Neutron Server?

Note

* use super administrator privilege to access backend API

# Milestone 3 :: Definition of CMP use cases, RESTful API spec, DB schema, backend API

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

Backend API ~~(one use case one sequence diagram)~~

* TBD
* TBD
* TBD

# Milestone 4 :: Implementation of RESTful API
