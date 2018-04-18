from oslo_config import cfg


class Driver(object):

    @staticmethod
    def __init__(self, config_file):

        if config_file is None:
            config_file = '/etc/sdnms_api/backends/fw_fortinet_v5.6.3.ini'

        cfg.CONF(project='FortiOS',
                 version="5.6.3",
                 default_config_files=[config_file],
                 description='FortiOS RESTful API')

        CONF = cfg.CONF

        ftg_opts = [
            cfg.StrOpt('http_scheme',
                       default='https',
                       help='http or https protocol for restful api'),
            cfg.StrOpt('http_host',
                       required=True,
                       help='backend IP which provides restful api endpoint'),
            cfg.PortOpt('http_port',
                        default=443,
                        help='The backend port where listen on'),
            cfg.StrOpt('http_account',
                       required=True,
                       help='The backend restful api login account'),
            cfg.StrOpt('http_password',
                       required=True,
                       help='The backend password for restful api login'),
            cfg.StrOpt('ssh_host',
                       required=True,
                       help='backend IP which provides CLI endpoint'),
            cfg.PortOpt('ssh_port',
                        default=22,
                        help='The backend port where ssh listen on'),
            cfg.StrOpt('ssh_account',
                       required=True,
                       help='The backend ssh login account'),
            cfg.StrOpt('ssh_password',
                       required=True,
                       help='The backend password for ssh login'),
        ]
        ftg_group = cfg.OptGroup(name='fw0001', title='ftg')

        cfg.CONF.register_group(ftg_group)
        cfg.CONF.register_opts(ftg_opts)

        fw0001_http_scheme = CONF.fw0001.http_scheme



