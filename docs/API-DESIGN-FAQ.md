# Project structure

Q: Where is the entrypoint module which is loaded by mod_wsgi?

```
app/wsgi.py

The entrypoint module must return an application object.
```

Q: Where is the main module which creates `application` object?

```
app/server.py

The main module must
* load configuration file
* register RESTful API routes
* register WSGI middlewares
* launche dev http server if needed
```

Q: How do we organize the backend via some sort of plugin mechanism?

About plugin invocation patterns see [this](https://docs.openstack.org/stevedore/latest/user/essays/pycon2013.html)

```
Use driver pattern

Each driver has its own configuration file in which specifies backend endpoint and access credential.

There are 3 driver types
* FW
* WAF
* SWITCH
```

Q: How do we organize the configuration file?

```
There is are a main configuraiton file and many backend configuraiton files.

The main configuration file specifies db connection string and log file location.

These configuraiton files are .ini files.
```

Q: How do we load the configuration file?

```
mod app/server.py

We leverage oslo.config to load the configuration file.

Alternative methods are
* python import for .py file
* ? for .yml file
```

Q: How do we organize the routing code?

```
All routing code are put in the resources/ folder.

If you need create a new resource e.g., my_resource
add resources/my_resource.py
```

Q: How do we load the routing code?

```
mod conf/dispatcher.py
mod app/server.py
```

Q: How do we organize the middleware code?

```
All middleware code are put in the middleware/ folder.

If you need create a new middleware e.g., my_middleware
add middleware/my_middleware.py
```

Q: How do we load the middleware code?

```
mod app/server.py
```

Q: How do we use the logging function?

```
We leverage oslo.log.
```