from oslo_config import cfg

import requests
import json


class FirewallAuthorization:

    cookies = {}
    content = {}

    def __init__(self):
        pass

    def login(self):
        payload = {
            "username": "admin",
            "secretkey": "Abc12345",
            "ajax": 1
        }
        r = requests.post("http://192.168.120.200/logincheck",
                          data=payload)

        if str(r.text[0]) == "1":
            self.cookies = r.cookies

    def generate_api_key(self):

        if self.cookies == {}:
            return False

        headers = {
            "Content-Type": "application/json",
            "X-CSRFTOKEN": self.cookies['ccsrftoken'].replace("\"", "")
        }
        payload = {
            "api-user": "api-admin"
        }
        r = requests.post("http://192.168.120.200/api/v2/monitor/system/api-user/generate-key",
                   params={"vdom": "root"},
                   cookies=self.cookies,
                   headers=headers,
                   json=payload)

        self.content = json.loads(r.text)


class Firewall(object):

    headers = {
        "Content-Type": "application/json",
        "X-CSRFTOKEN": ""
    }
    params = {
        "vdom": "root",
        "global": 1,
        "access_token": ""
    }

    def __init__(self):
        auth = FirewallAuthorization()
        auth.login()
        auth.generate_api_key()
        self.headers["X-CSRFTOKEN"] = auth.cookies['ccsrftoken'].replace("\"", "")
        self.params["access_token"] = auth.content["results"]["access_token"]

    def use(self, index, identity):
        self._index = index
        self._identity = identity

    def info(self):
        r = requests.get("http://192.168.120.200/api/v2/cmdb/firewall/address",
                         params=self.params,
                         headers=self.headers)
        print(r.text)


class Driver(object):

    def __init__(self, conf):
        print 'Driver.__init__'

    def a__init__(self, conf):
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
        print "%s %s" % (self._index,self._identity)
        return "%s %s" % (self._index,self._identity)
