from oslo_config import cfg

import pdb
import requests
import json

print("enter into fw_fortinet_v5_6_3/driver.py")

class Driver(object):

    def __init__(self, conf):
        print 'Init Driver Fortinet v5.6.3....'
        self.load_conf(conf)
        self.conf = conf

    def load_conf(self, conf):
        fwid_opts = [
            cfg.StrOpt('fw',
                       help='firewalls list'),
            ]

        conf.register_opts(fwid_opts, group='identities')
        fw_identities_str = conf.identities.fw
        fw_identities = [x for x in fw_identities_str.split(',')]
        self.fw_identities = fw_identities
        #self.use(1)

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

        for group_name in self.fw_identities:
            conf.register_opts(ftg_opts, group=group_name)


    def use(self, index=0, identity=None):
        self._index = index
        self._identity = identity


    def info(self):
        print "This is info method:"
        print "%s %s" % (self._index, self.fw_identities[self._index])
        print('http_scheme : %s' % (self.conf.get(self.fw_identities[0]).http_scheme))
        return "return value: %s %s" % (self._index, self.fw_identities[self._index])


