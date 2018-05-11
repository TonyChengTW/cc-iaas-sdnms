import sys
import requests
import socket
import errno
from socket import error as socket_error
import pdb

from oslo_config import cfg
from ast import literal_eval

print("enter into fw_fortinet_v5_6_3/driver.py")


class Driver(object):

    def __init__(self, conf):
        print 'Init Driver Fortinet v5.6.3....'
        self.fw_identities = self.identity = self.apiurl_logincheck = \
            self.apiurl_cmdb_firewall_address = ''
        self._header = self._headers = self._params = {}
        self.index = int('0')
        self._access_token = self.http_scheme = self.http_host = self.http_port = self.http_account = \
            self.http_password = self.ssh_host = self.ssh_port = self.ssh_account = \
            self.ssh_password = ''

        self.load_conf(conf)
        self.conf = conf

    def load_conf(self, conf):

        fw_default_opts = [
            cfg.StrOpt('access_token',
                       help='Firewall API token')
            ]
        conf.register_opts(fw_default_opts)

        fwid_opts = [
            cfg.StrOpt('fw',
                       help='firewalls list'),
            ]
        conf.register_opts(fwid_opts, group='identities')
        fw_identities_str = conf.identities.fw
        fw_identities = [x for x in fw_identities_str.split(',')]
        self.fw_identities = fw_identities

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

    def login(self, index=0, identity=None):
        self.index = index
        self.identity = identity

        if self.identity is None:
            self.http_scheme = self.conf.get(self.fw_identities[self.index]).http_scheme
            self.http_host = self.conf.get(self.fw_identities[self.index]).http_host
            self.http_port = self.conf.get(self.fw_identities[self.index]).http_port
            self.http_account = self.conf.get(self.fw_identities[self.index]).http_account
            self.http_password = self.conf.get(self.fw_identities[self.index]).http_password
            self.ssh_host = self.conf.get(self.fw_identities[self.index]).ssh_host
            self.ssh_port = self.conf.get(self.fw_identities[self.index]).ssh_port
            self.ssh_account = self.conf.get(self.fw_identities[self.index]).ssh_account
            self.ssh_password = self.conf.get(self.fw_identities[self.index]).ssh_password
        else:
            self.http_scheme = self.conf.get(self.identity).http_scheme
            self.http_host = self.conf.get(self.identity).http_host
            self.http_port = self.conf.get(self.identity).http_port
            self.http_account = self.conf.get(self.identity).http_account
            self.http_password = self.conf.get(self.identity).http_password
            self.ssh_host = self.conf.get(self.identity).ssh_host
            self.ssh_port = self.conf.get(self.identity).ssh_port
            self.ssh_account = self.conf.get(self.identity).ssh_account
            self.ssh_password = self.conf.get(self.identity).ssh_password

        payload = {
            "username": self.http_account,
            "secretkey": self.http_password,
            "ajax": 1
        }
        print("Auth account and password via API:logincheck")
        try:
            self.apiurl_logincheck = (self.http_scheme + '://' + self.http_host +
                                      ':' + str(self.http_port) + '/logincheck')
        except socket.error, msg:
            print "Couldnt connect with the firewall: %s\n terminating program" % msg
            sys.exit(1)
        except socket_error:
            if socket.error.errno != errno.ECONNREFUSED:
                print "Connection refused: %s\n , terminating program" % socket_error
                sys.exit(1)

        resp = requests.post(self.apiurl_logincheck,
                             verify=False,
                             data=payload)

        if str(resp.status_code) != '200':
            raise('Error: API: /logincheck status code is not 200')
        else:
            self.cookies = resp.cookies

    def generate_api_key(self):

        """"
        self._headers = {}
        self._content = {}

        print "begin to generate api key..."
        if self.cookies == {}:
            return False
        
        headers = {
            "Content-Type": "application/json",
            "X-CSRFTOKEN": self.cookies['ccsrftoken'].replace("\"","")
        }
        payload = {
            "api-user": "api-admin1"
        }
        resp = requests.post("https://172.16.100.254:10443/api/v2/monitor/system/api-user/generate-key",
                           params={"vdom": "root"},
                           verify=False,
                           cookies=self.cookies,
                           headers=headers,
                           json=payload)
                                            
        self._content = json.loads(resp.text)
        self._api_token = str(self._content['results']['access_token'])
        self._header['Authorization'] = "Bearer " + self._api_token
        """
        self._access_token = self.conf.access_token
        self._header['X-CSRFTOKEN'] = self.cookies['ccsrftoken'].replace("\"", "")
        self._headers = {
                         #   "Authorization": self._header['Authorization'],
                         "X-CSRFTOKEN": self._header['X-CSRFTOKEN']
                         }

        self._params = {
                        "global": 1,
                        "access_token": self._access_token
                        }

        print "api key is generated"

    def use(self, index=0, identity=None):
        self.login(index, identity)
        self.generate_api_key()

    def info(self):
        print "Function : This is info method:"
        print "%s %s" % (self.index, self.fw_identities[self.index])
        print 'http_host : %s' % self.conf.get(self.fw_identities[self.index]).http_host
        return "return value: %s %s" % (self.index, self.fw_identities[self.index])

    def get_addr(self, vdom='root'):
        self._params["vdom"] = vdom
        print "Function : This is get_addr method, vdom=%s" % vdom
        self.apiurl_cmdb_firewall_address = (self.http_scheme + '://' + self.http_host +
                                             ':' + str(self.http_port) +
                                             '/api/v2/cmdb/firewall/address')
        _resp = requests.get(self.apiurl_cmdb_firewall_address,
                             params=self._params,
                             verify=False,
                             headers=self._headers)
        content = literal_eval(_resp.text)
        # content = resp.text.encode('utf-8')
        print(content)
        return content  # Tony: you can use - content['results'][10]  to get value
