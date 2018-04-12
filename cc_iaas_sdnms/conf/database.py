from oslo_config import cfg

url_opt = cfg.StrOpt(name='url',
                     default='mysql+mysqlconnector://root:root@192.168.99.100:32771/testdb',
                     help='''
The SQLAlchemy connection string to use to connect to the database
''',
                     required=False,
                     deprecated_for_removal=True,
                     deprecated_since='1.6.0',
                     deprecated_reason='Please use database.connection option,'
                                       'database.url is scheduled for removal '
                                       'in Pike release')

def register_opts(conf):
    conf.register_opt(url_opt, 'database')

def list_opts():
    return 'database', [url_opt]