from oslo_config import cfg
from oslo_log import log

CONF = cfg.CONF
LOG = log.getLogger(__name__)


dispatcher_opts = [
    cfg.StrOpt('scores',
               default='cc_iaas_sdnms.resources.scores:ScoresResource',
               help='ScoresResource controller'),
]

dispatcher_group = cfg.OptGroup(name='dispatcher', title='dispatcher')

conf.register_group(dispatcher_group)
conf.register_opts(dispatcher_opts, dispatcher_group)

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
