from oslo_config import cfg
from oslo_log import log

CONF = cfg.CONF
LOG = log.getLogger(__name__)


dispatcher_opts = [
    cfg.StrOpt('health',
               default='cc_iaas_sdnms.resources.health:HealthResource',
               help='HealthResource controller'),
]

dispatcher_group = cfg.OptGroup(name='dispatcher', title='dispatcher')

CONF.register_group(dispatcher_group)
CONF.register_opts(dispatcher_opts, dispatcher_group)

def init(argv=None, config_file=None):
    log.set_defaults()
    log.register_options(CONF)
    args = []
    CONF(args=args,
         prog='api',
         project='SDNMS',
         version="1.0",
         default_config_files=[config_file] if config_file else None,
         description='SDNMS RESTful API')
