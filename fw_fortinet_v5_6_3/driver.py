import sys
import requests
import socket
import errno
import re
from socket import error as socket_error
import pdb

from oslo_config import cfg
from ast import literal_eval

print("enter into fw_fortinet_v5_6_3/driver.py")


class Driver(object):

    def __init__(self, conf):
        print 'Init Driver Fortinet v5.6.3....'
        self.fw_identities = self.identity = self.apiurl_logincheck = \
            self.apiurl_cmdb_firewall_address = self.payload_add_addr = ''
        self._header = self._headers = self._params = {}
        self.index = int('0')
        self.access_token = self.http_scheme = self.http_host = self.http_port = self.http_account = \
            self.http_password = self.ssh_host = self.ssh_port = self.ssh_account = \
            self.ssh_password = ''

        self.load_conf(conf)
        self.conf = conf

    def load_conf(self, conf):

        fw_default_opts = [
            cfg.StrOpt('test1',
                       help='test1')
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
            cfg.StrOpt('access_token',
                       default='',
                       help='restful api for restful api'),
            cfg.StrOpt('http_scheme',
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

    def login(self, index=None, identity=None):
        self.index = index
        self.identity = identity

        if self.index is None and self.identity is None:
            print "Error: you need to specify index or identity to use firewall!"
            sys.exit(1)

        if self.identity is None:
            self.access_token = self.conf.get(self.fw_identities[self.index]).access_token
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
            self.access_token = self.conf.get(self.identity).access_token
            self.http_scheme = self.conf.get(self.identity).http_scheme
            self.http_host = self.conf.get(self.identity).http_host
            self.http_port = self.conf.get(self.identity).http_port
            self.http_account = self.conf.get(self.identity).http_account
            self.http_password = self.conf.get(self.identity).http_password
            self.ssh_host = self.conf.get(self.identity).ssh_host
            self.ssh_port = self.conf.get(self.identity).ssh_port
            self.ssh_account = self.conf.get(self.identity).ssh_account
            self.ssh_password = self.conf.get(self.identity).ssh_password

        payload_login = {
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
                             data=payload_login)

        if resp.status_code != requests.codes.ok:
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
        self._header['X-CSRFTOKEN'] = self.cookies['ccsrftoken'].replace("\"", "")
        self._headers = {
                         #   "Authorization": self._header['Authorization'],
                         "X-CSRFTOKEN": self._header['X-CSRFTOKEN']
                         }

        self._params = {
                        # "global": 1,
                        "access_token": self.access_token
                        }

        print "api key is generated"

    def use(self, index=None, identity=None):
        self.login(index, identity)
        self.generate_api_key()

    def info(self):
        print "Function : This is info method:"
        if self.identity is None:
            print "fw_identities[%s] %s" % (self.index, self.fw_identities[self.index])
            print 'http_host : %s' % self.conf.get(self.fw_identities[self.index]).http_host
            return 0
        else:
            print "identity : %s" % self.identity
            print 'http_host : %s' % self.conf.get(self.identity).http_host
            return 0

    def get_addr(self, vdom='root'):
        self._params["vdom"] = vdom
        print "Function : This is get_addr method, vdom=%s" % vdom
        self.apiurl_cmdb_firewall_address = (self.http_scheme + '://' + self.http_host +
                                             ':' + str(self.http_port) +
                                             '/api/v2/cmdb/firewall/address')
        resp = requests.get(self.apiurl_cmdb_firewall_address,
                            params=self._params,
                            verify=False,
                            headers=self._headers)
        re_resp = re.findall(r'^<TITLE>4[0-9][0-9]', resp.text, flags=re.MULTILINE)
        if len(re_resp) != 0:
            print "Error: There is no data return! Respond code is 4xx"
            return resp.raise_for_status()

        try:
            content = literal_eval(resp.text)
            print(content)
            return content  # Tony: you can use - content['results'][10]  to get value
        except:
            return resp.raise_for_status()

    def add_addr(self, vdom='root', add_addr=None):
        if add_addr is None:
            print "Error: you need to provide ip/subnet/fqdn and type \
                   to add address into firewall!"
            sys.exit(1)

        self._params["vdom"] = vdom
        print "Function : This is add_addr method, vdom=%s" % vdom
        self.apiurl_cmdb_firewall_address = (self.http_scheme + '://' + self.http_host +
                                             ':' + str(self.http_port) +
                                             '/api/v2/cmdb/firewall/address')
        # pdb.set_trace()
        resp = requests.post(self.apiurl_cmdb_firewall_address,
                             params=self._params,
                             json=add_addr,
                             verify=False,
                             headers=self._headers)
        if not resp.ok:
            print "Return Code is : %s" % resp.status_code
            print "Resp text is : %s" % resp.text
            return resp.status_code

    def del_addr(self, vdom='root', del_addr=None):
        if del_addr is None:
            print "Error: you need to provide ip/subnet/fqdn \
                   to delete address from firewall!"
            sys.exit(1)

        self._params["vdom"] = vdom
        print "Function : This is del_addr method, vdom=%s" % vdom
        self.apiurl_cmdb_firewall_address = (self.http_scheme + '://' + self.http_host +
                                             ':' + str(self.http_port) +
                                             '/api/v2/cmdb/firewall/address/') + del_addr
        # pdb.set_trace()
        resp = requests.delete(self.apiurl_cmdb_firewall_address,
                               params=self._params,
                               verify=False,
                               headers=self._headers)
        if not resp.ok:
            print "Return Code is : %s" % resp.status_code
            print "Resp text is : %s" % resp.text
            return resp.status_code

    def set_addr(self, vdom='root', set_addr=None, payload=None):
        if set_addr is None:
            print "Error: you need to provide ip/subnet/fqdn and type \
                   to update address into firewall!"
            sys.exit(1)

        self._params["vdom"] = vdom
        print "Function : This is set_addr method, vdom=%s" % vdom
        self.apiurl_cmdb_firewall_address = (self.http_scheme + '://' + self.http_host +
                                             ':' + str(self.http_port) +
                                             '/api/v2/cmdb/firewall/address/') + set_addr
        # pdb.set_trace()
        resp = requests.put(self.apiurl_cmdb_firewall_address,
                            params=self._params,
                            json=payload,
                            verify=False,
                            headers=self._headers)
        if not resp.ok:
            print "Return Code is : %s" % resp.status_code
            print "Resp text is : %s" % resp.text
            return resp.status_code
