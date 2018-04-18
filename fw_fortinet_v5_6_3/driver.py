from oslo_config import cfg


class Driver(object):

    def __init__(self, config_file=None):

        if config_file is None:
            config_file = '/etc/sdnms_api/backends/fw_fortinet_v5.6.3.ini'

        cfg.CONF(args=[],
                project='FortiOS',
                version="5.6.3",
                default_config_files=[config_file],
                description='FortiOS RESTful API')

        ftg_opts = [
            cfg.StrOpt('http_scheme',
                       default='https',
                       help='http or https protocol for restful api'),
            cfg.StrOpt('http_host',
                       help='backend IP which provides restful api endpoint'),
            cfg.PortOpt('http_port',
                        default=443,
                        help='The backend port where listen on'),
            cfg.StrOpt('http_account',
                       help='The backend restful api login account'),
            cfg.StrOpt('http_password',
                       help='The backend password for restful api login'),
            cfg.StrOpt('ssh_host',
                       help='backend IP which provides CLI endpoint'),
            cfg.PortOpt('ssh_port',
                        default=22,
                        help='The backend port where ssh listen on'),
            cfg.StrOpt('ssh_account',
                       help='The backend ssh login account'),
            cfg.StrOpt('ssh_password',
                       help='The backend password for ssh login'),
        ]
        ftg_group = cfg.OptGroup(name='fw0001', title='ftg')

        cfg.CONF.register_group(ftg_group)
        cfg.CONF.register_opts(ftg_opts, ftg_group)

        print('%s' % (cfg.CONF.fw0001.http_scheme))
        print('%s' % (cfg.CONF.fw0001.http_host))
        print('%s' % (cfg.CONF.fw0001.http_port))

    def query(self, ):
