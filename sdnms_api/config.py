from oslo_config import cfg

CONF = cfg.CONF

default_opts = [
    cfg.StrOpt('name',
                default='cc_iaas_sdnms',
                help='Process name.'),
]

database_opts = [
    cfg.StrOpt('address',
                default='127.0.0.1',
                help='Binding address'),
    cfg.IntOpt('port', default=3306,
               help='The database port where listen on'),
    cfg.StrOpt('username', default='root',
               help='The database user of login'),
    cfg.StrOpt('password', default='root',
               help='The database password of login'),
]
database_group = cfg.OptGroup(name='database', title='database')

dispatcher_opts = [
    cfg.StrOpt('health',
               default='sdnms_api.resources.health:HealthResource',
               help='HealthResource controller'),
]
dispatcher_group = cfg.OptGroup(name='dispatcher', title='dispatcher')


def init(args=None, config_file=None):
    cfg.CONF(args=args,
         project='SDNMS',
         version="1.0",
         default_config_files=[config_file],
         description='SDNMS RESTful API')

    cfg.CONF.register_opts(default_opts)
    cfg.CONF.register_group(database_group)
    cfg.CONF.register_opts(database_opts, database_group)
    cfg.CONF.register_group(dispatcher_group)
    cfg.CONF.register_opts(dispatcher_opts, dispatcher_group)
