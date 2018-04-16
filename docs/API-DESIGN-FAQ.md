# Project structure

Q: Where is the entrypoint module which is loaded by mod_wsgi?

```
app/wsgi.py
```

Q: Where is the main module which loads configuration file, creates `application` object, and launches dev http server if needed?

```
app/server.py
```

Q: How do we organize the backend via some sort of plugin mechanism?

About plugin invocation patterns see (this)[https://docs.openstack.org/stevedore/latest/user/essays/pycon2013.html]

```
Use driver pattern

Each driver has its own configuration file in which specifies backend endpoint and access credential.
```

Q: How do we organize the configuration file?

```
TBD

e.g., log file level and log file location
e.g., db connection string (endpoint and credential)

Method 1 :: .ini + oslo.config

Method 2 :: .py + python import

Method 3 :: .yml

```

Q: How do we load the configuration file?

```
oslo.config
```

Q: How do we organize the routing code?

```
e.g.,

add resources/my_resource.py
```

Q: How do we load the routing code?

```
mod conf/dispatcher.py
mod app/server.py
```

Q: How do we organize the middleware code?

```
e.g.,

add middleware/my_middleware.py
```

Q: How do we load the middleware code?

```
mod app/server.py
```

Q: How do we use the logging function?

```
oslo.log
```