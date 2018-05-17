import requests
import urllib3
import socket
import errno
import re

from ast import literal_eval
from socket import error as socket_error

from oslo_config import cfg
from oslo_log import log


LOG = log.getLogger(__name__)
LOG.info("Enter into fw_fortinet_v5_6_3/driver.py")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Driver(object):
    def __init__(self, conf):
        LOG.debug("Init Driver Fortinet v5.6.3...")
        self.fw_identities = self.identity = self.apiurl = self.payload_add_addr = ''
        self._header = self._headers = self._params = {}
        self.index = int('0')
        self.cookies = {}
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
            LOG.error("You need to specify index or identity to use firewall!")

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
        LOG.info("Auth account and password via logincheck api....")
        try:
            self.apiurl = (self.http_scheme + '://' + self.http_host +
                           ':' + str(self.http_port) + '/logincheck')
        except socket.error, msg:
            LOG.error("Could not connect with the firewall: %s\n terminating program" % msg)
        except RuntimeError:
            if socket.error.errno != errno.ECONNREFUSED:
                LOG.error("Connection refused: %s\n , terminating program" % socket_error)

        resp = requests.post(self.apiurl,
                             verify=False,
                             data=payload_login)

        if resp.status_code != requests.codes.ok:
            LOG.error("Error: API: /logincheck status code is not 200")
        else:
            self.cookies = resp.cookies
            LOG.info("Auth account and password successed!")

    def generate_api_key(self):

        """
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

        LOG.info("FortiOS API key is ready to use")

    def use(self, index=None, identity=None):
        self.login(index, identity)
        self.generate_api_key()

    def info(self):
        LOG.info("This is 'info' method:")
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
        LOG.info("This is 'get_addr' method, vdom=%s" % vdom)
        self.apiurl = (self.http_scheme + '://' + self.http_host +
                       ':' + str(self.http_port) +
                       '/api/v2/cmdb/firewall/address')
        resp = requests.get(self.apiurl,
                            params=self._params,
                            verify=False,
                            headers=self._headers)
        re_resp = re.findall(r'^<TITLE>4[0-9][0-9]', resp.text, flags=re.MULTILINE)
        if len(re_resp) != 0:
            LOG.error("There is no data return! Respond code is 4xx")
            return resp.raise_for_status()

        try:
            content = literal_eval(resp.text)
            print(content)

            # NOTE(tonycheng): You can use "content['results'][10]" to get value
            return content
        except RuntimeError:
            return resp.raise_for_status()

    def add_addr(self, vdom='root', payload=None):
        if payload is None:
            LOG.error("Error: you need to provide ip/subnet/fqdn and type \
                   to add address into firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is 'add_addr' method, vdom=%s" % vdom)
        self.apiurl = (self.http_scheme + '://' + self.http_host +
                       ':' + str(self.http_port) +
                       '/api/v2/cmdb/firewall/address')

        resp = requests.post(self.apiurl,
                             params=self._params,
                             json=payload,
                             verify=False,
                             headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            return resp.status_code

    def del_addr(self, vdom='root', name=None):
        if name is None:
            LOG.error("you need to provide ip/subnet/fqdn \
                   to delete address from firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is 'del_addr' method, vdom=%s" % vdom)
        self.apiurl = (self.http_scheme + '://' + self.http_host +
                       ':' + str(self.http_port) +
                       '/api/v2/cmdb/firewall/address/') + name

        resp = requests.delete(self.apiurl,
                               params=self._params,
                               verify=False,
                               headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            return resp.status_code

    def set_addr(self, vdom='root', name=None, payload=None):
        if name is None or payload is None:
            LOG.error("you need to provide ip/subnet/fqdn and type \
                   to update address into firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is set_addr method, vdom=%s" % vdom)
        self.apiurl = (self.http_scheme + '://' + self.http_host +
                       ':' + str(self.http_port) +
                       '/api/v2/cmdb/firewall/address/') + name

        resp = requests.put(self.apiurl,
                            params=self._params,
                            json=payload,
                            verify=False,
                            headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            return resp.status_code

    def get_vip(self, vdom='root'):
        self._params["vdom"] = vdom
        LOG.info("This is 'get_vip' method, vdom=%s" % vdom)
        self.apiurl = (self.http_scheme + '://' + self.http_host +
                       ':' + str(self.http_port) +
                       '/api/v2/cmdb/firewall/vip/vm3-icmp')
        resp = requests.get(self.apiurl,
                            params=self._params,
                            verify=False,
                            headers=self._headers)
        re_resp = re.findall(r'^<TITLE>4[0-9][0-9]', resp.text, flags=re.MULTILINE)
        if len(re_resp) != 0:
            LOG.error("There is no data return! Respond code is 4xx")
            return resp.raise_for_status()

        try:
            content = literal_eval(resp.text)
            print(content)

            # NOTE(tonycheng): You can use "content['results'][10]" to get value
            return content
        except RuntimeError:
            return resp.raise_for_status()

    def add_vip(self, vdom='root', payload=None):
        if payload is None:
            LOG.error("you need to provide something \
                   to add virtual IP into firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is add_vip method, vdom=%s" % vdom)
        self.apiurl = (self.http_scheme + '://' + self.http_host +
                       ':' + str(self.http_port) +
                       '/api/v2/cmdb/firewall/vip/')

        resp = requests.post(self.apiurl,
                             params=self._params,
                             json=payload,
                             verify=False,
                             headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            LOG.error("Resp reason is : %s" % resp.reason)
            return resp.status_code

    def logout(self):
        self.apiurl = (self.http_scheme + '://' + self.http_host +
                       ':' + str(self.http_port) + '/logout')
        resp = requests.post(self.apiurl,
                             verify=False,
                             headers=self._headers)
        resp.cookies.clear()
        LOG.info("Log-out and clear cookies : %s" % resp.text)
