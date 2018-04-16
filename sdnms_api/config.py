from oslo_config import cfg

CONF = cfg.CONF

dispatcher_opts = [
    cfg.StrOpt('health',
               default='sdnms_api.resources.health:HealthResource',
               help='HealthResource controller'),
]
dispatcher_group = cfg.OptGroup(name='dispatcher', title='dispatcher')

def init(args=[], config_file=None):
    cfg.CONF(args=args,
         project='SDNMS',
         version="1.0",
         default_config_files=[config_file],
         description='SDNMS RESTful API')

    cfg.CONF.register_group(dispatcher_group)
    cfg.CONF.register_opts(dispatcher_opts, dispatcher_group)
