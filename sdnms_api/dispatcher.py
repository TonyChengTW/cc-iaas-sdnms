from oslo_config import cfg

dispatcher_opts = [
    cfg.StrOpt('scores',
               default='cc_iaas_sdnms.resources.scores:ScoresResource',
               help='ScoresResource controller'),
]

dispatcher_group = cfg.OptGroup(name='dispatcher', title='dispatcher')

def register_opts(conf):
    conf.register_group(dispatcher_group)
    conf.register_opts(dispatcher_opts, dispatcher_group)

def list_opts():
    return dispatcher_group, dispatcher_opts