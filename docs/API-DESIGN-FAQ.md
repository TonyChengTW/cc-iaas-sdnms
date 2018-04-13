# Project structure

Q: How do we organize the configuration file?

```
TBD

e.g., log file level and log file location
e.g., backend connection string (endpoint and credential)
e.g., db connection string (endpoint and credential)

Method 1 :: .ini + oslo.config

Method 2 :: .py + python import

```

Q: How do we load the configuration file?

```
?
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