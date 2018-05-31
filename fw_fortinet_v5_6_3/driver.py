import re
import urllib3
import socket
from socket import error as socket_error
from ast import literal_eval

import requests
from netmiko import Netmiko
from oslo_config import cfg
from oslo_log import log
from sdnms_api.models.manager import DBManager
from sdnms_api.models.firewall import FirewallAddressModel, FirewallServiceModel

import pdb

LOG = log.getLogger(__name__)
print("Enter into fw_fortinet_v5_6_3/driver.py")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Driver(object):

    def __init__(self, conf):
        self.fw_identities = self.identity = self.baseurl = self.cmdburl = ''
        self._header = self._headers = self._params = {}
        self.index = int('0')
        self.cookies = {}
        self.access_token = self.http_scheme = self.http_host = self.http_port = self.http_account = \
            self.http_password = self.ssh_host = self.ssh_port = self.ssh_account = \
            self.ssh_password = ''

        """ Load ini config from CLI parameters """
        self._load_conf(conf)
        self.conf = conf

        """ Create Tables """
        self._create_orm()

    def _create_orm(self):
        connection = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            self.db_username, self.db_password,
            self.db_address, self.db_port, self.db_name)
        dbmgr = DBManager(connection)
        dbmgr.setup()

    def _load_conf(self, conf):
        # Load sdnms_api.ini to fetch database options
        self.db_address = conf.database.address
        self.db_port = conf.database.port
        self.db_username = conf.database.username
        self.db_password = conf.database.password
        self.db_name = conf.database.database_name

        # Load fw_fortinet.ini to fetch firewall options
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

    def _login(self):
        LOG.debug("This is '_login' method")
        payload_login = {"username": self.http_account,
                         "secretkey": self.http_password,
                         "ajax": 1}
        LOG.info("Auth account and password via logincheck api....")
        endpoint = self.baseurl + '/logincheck'

        try:
            resp = requests.post(endpoint,
                                 verify=False,
                                 data=payload_login)
        except socket.error, msg:
            LOG.error("Could not connect with the firewall: %s\n terminating program" % msg)
        except OSError:
            LOG.error("Connection refused: %s\n , terminating program" % socket_error)

        if resp.status_code != requests.codes.ok:
            LOG.error("Error: API: /logincheck status code is not 200")
        else:
            self.cookies = resp.cookies
            LOG.info("Auth account and password successed!")
        return requests.codes.ok

    def logout(self):
        LOG.debug("This is 'logout' method")
        endpoint = self.baseurl + '/logout'
        resp = requests.post(endpoint,
                             verify=False,
                             headers=self._headers)
        resp.cookies.clear()
        LOG.debug("Log-out and clear cookies : %s" % resp.text)
        # self.net_connect.disconnect()
        LOG.debug("Disconnect SSH CLI")
        return requests.codes.ok

    def _add_csrftoken(self):
        LOG.debug("This is '_add_csrftoken' method")
        self._header['X-CSRFTOKEN'] = self.cookies['ccsrftoken'].replace("\"", "")
        self._headers = {"X-CSRFTOKEN": self._header['X-CSRFTOKEN']}

        self._params = {"global": 0,
                        "access_token": self.access_token}

        LOG.info("FortiOS API key is ready to use")

    def _ftg_init(self):
        ftg = {'host': self.ssh_host,
               'port': self.ssh_port,
               'username': self.ssh_account,
               'password': self.ssh_password,
               'device_type': 'fortinet',
               'verbose': False}
        self.net_connect = Netmiko(**ftg)
        self._disable_paging()

    def _disable_paging(self):
        disable_paging_commands = [
            "config global",
            "config system console",
            "set output standard",
            "end\nend"
        ]
        for command in disable_paging_commands:
            self.net_connect.send_command_timing(command)

    def use(self, index=None, identity=None):
        LOG.debug("This is 'use' method")

        self.index = index
        self.identity = identity

        if self.index is None and self.identity is None:
            LOG.error("You need to specify index or identity to use firewall!")
            raise ValueError

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

        self.baseurl = "%s://%s:%s" % (self.http_scheme, self.http_host, self.http_port)
        self.cmdburl = '/api/v2/cmdb/'

        self._login()
        self._add_csrftoken()
        # self._ftg_init()

    def info(self):
        LOG.info("This is 'info' method")

        if self.identity is None:
            print "fw_identities[%s] %s" % (self.index, self.fw_identities[self.index])
            print 'http_host : %s' % self.conf.get(self.fw_identities[self.index]).http_host
        else:
            print "identity : %s" % self.identity
            print 'http_host : %s' % self.conf.get(self.identity).http_host

        command_set = [
            'get system status'
        ]
        for command in command_set:
            output = self.net_connect.send_command_timing(command)
            print("+-----------------------------------------------------+")
            print(output)

        return 0

    def get_vdom(self):
        LOG.info("This is 'get_vdom' method")
        exist_vdoms = self._get_vdom_without_print()

        # TODO(tonycheng): Maybe we need a DB to check if the record is exist or not
        print("+--------------- Get VDOM -----------------------------------+")
        print("VDOMs:\n-------------------------------------------------------------")
        for exist_vdom in exist_vdoms:
            print exist_vdom
        return 0

    def _get_vdom_without_print(self):
        exist_vdoms = []
        output = ''
        command_set = [
            'config global',
            'config system vdom-property',
            'show | grep edit',
            'end',
            'end'
        ]
        for command in command_set:
            clioutput = self.net_connect.send_command_timing(command)
            if command == command_set[2]:
                output = clioutput.encode('utf-8')
                if 'Command fail' in output or 'Unknown action' in output:
                    LOG.error("%s" % output)
                    raise RuntimeError

        prog = re.compile('edit \"(.*)\"', re.MULTILINE)

        for result in prog.finditer(output):
            exist_vdoms.append(result.group(1))
        return exist_vdoms

    def add_vdom(self, name):
        LOG.info("This is 'add_vdom' method")

        if name is None:
            LOG.error("you need to provide VDOM name!")
            raise RuntimeError("you need to provide VDOM name")

        exist_vdoms = self._get_vdom_without_print()

        if name in exist_vdoms:
            LOG.error("This vdom : '%s' is already exist!!" % name)
            raise Exception

        sub_command = "edit %s" % name
        command_set = [
            'config vdom',
            sub_command,
            'end'
        ]
        for command in command_set:
            clioutput = self.net_connect.send_command_timing(command)
            if command == command_set[1]:
                output = clioutput.encode('utf-8')
                if 'Command fail' in output or 'Unknown action' in output:
                    LOG.error("command: %s , respond: %s" % (command, clioutput))
                    raise RuntimeError
                print("+-----------------------------------------------------+")
                print "FTG Console : %s" % output
        LOG.info("VDOM: %s Created!" % name)
        return True

    def del_vdom(self, name, vdom):
        """Not Implemented"""
        raise NotImplementedError

    def get_addr(self, vdom='root'):
        self._params["vdom"] = vdom
        LOG.info("This is 'get_addr' method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall/address'
        resp = requests.get(endpoint,
                            params=self._params,
                            verify=False,
                            headers=self._headers)
        if resp.ok:
            try:
                content = literal_eval(resp.text)
                print(content)

                # NOTE(tonycheng): You can use "content['results'][10]" to get value
                return content
            except RuntimeError:
                LOG.error("Unknown error when parsing resp.text")
            finally:
                self.logout()
        else:
            LOG.error("Resp text : %s" % resp.text)
            LOG.error("Resp reason : %s" % resp.reason)
            return resp.ok

    def add_addr(self, payload, vdom='root'):
        if payload is None:
            LOG.error("Error: you need to provide ip/subnet/fqdn and type "
                      "to add address into firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is 'add_addr' method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall/address'

        resp = requests.post(endpoint,
                             params=self._params,
                             json=payload,
                             verify=False,
                             headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            LOG.error("Resp reason is : %s" % resp.reason)
        else:
            LOG.info("Resp text is : %s" % resp.text)
        return resp.ok

    def del_addr(self, name, vdom='root'):
        if name is None:
            LOG.error("you need to provide ip/subnet/fqdn "
                      "to delete address from firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is 'del_addr' method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall/address/'

        resp = requests.delete(endpoint,
                               params=self._params,
                               verify=False,
                               headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            LOG.error("Resp reason is : %s" % resp.reason)
        else:
            LOG.info("Resp text is : %s" % resp.text)
        return resp.ok

    def set_addr(self, name, payload, vdom='root'):
        if name is None or payload is None:
            LOG.error("you need to provide ip/subnet/fqdn and type "
                      "to update address into firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is set_addr method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall/address/' + name

        resp = requests.put(endpoint,
                            params=self._params,
                            json=payload,
                            verify=False,
                            headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            LOG.error("Resp reason is : %s" % resp.reason)
        else:
            LOG.info("Resp text is : %s" % resp.text)
        return resp.ok

    def get_vip(self, vdom='root'):
        self._params["vdom"] = vdom
        LOG.info("This is 'get_vip' method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall/vip/'
        resp = requests.get(endpoint,
                            params=self._params,
                            verify=False,
                            headers=self._headers)
        if resp.ok:
            try:
                content = literal_eval(resp.text)
                print(content)

                # NOTE(tonycheng): You can use "content['results'][10]" to get value
                return content
            except RuntimeError:
                LOG.error("Unknown error when parsing resp.text")
            finally:
                self.logout()
        else:
            LOG.error("Resp text : %s" % resp.text)
            LOG.error("Resp reason : %s" % resp.reason)
            return resp.ok

    def add_vip(self, payload, vdom='root'):
        if payload is None:
            LOG.error("you need to provide something "
                      "to add virtual IP into firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is add_vip method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall/vip/'

        resp = requests.post(endpoint,
                             params=self._params,
                             json=payload,
                             verify=False,
                             headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            LOG.error("Resp reason is : %s" % resp.reason)
        else:
            LOG.info("Resp text is : %s" % resp.text)
        return resp.ok

    def del_vip(self, name, vdom='root'):
        if name is None:
            LOG.error("you need to VIP name \
                   to delete virtual ip from firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is 'del_vip' method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall/vip/' + name

        resp = requests.delete(endpoint,
                               params=self._params,
                               verify=False,
                               headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            LOG.error("Resp reason is : %s" % resp.reason)
        else:
            LOG.info("Resp text is : %s" % resp.text)
        return resp.ok

    def set_vip(self, name, payload, vdom='root'):
        if payload is None or name is None:
            LOG.error("you need to provide something \
                   to update virtual IP into firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is set_vip method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall/vip/' + name

        resp = requests.put(endpoint,
                            params=self._params,
                            json=payload,
                            verify=False,
                            headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            LOG.error("Resp reason is : %s" % resp.reason)
        else:
            LOG.info("Resp text is : %s" % resp.text)
        return resp.ok

    def get_policy(self, vdom='root'):
        self._params["vdom"] = vdom
        LOG.info("This is 'get_policy' method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall/policy/'
        resp = requests.get(endpoint,
                            params=self._params,
                            verify=False,
                            headers=self._headers)
        if resp.ok:
            try:
                session = dbmgr.session()
                content = literal_eval(resp.text)
                # pdb.set_trace()
                print(content)

                for policy in content['results']:
                    policy_id = policy['id']
                    policy_name = policy['name']
                    policy_srcintf = policy['srcintf']
                    policy_dstintf = policy['dstintf']
                    policy_srcaddr = policy['srcaddr']
                    policy_dstaddr = policy['dstaddr']
                    policy_service = policy['service']
                    policy_nat = policy['nat']
                    policy_action = policy['action']
                    policy_schedule = policy['schedule']
                    policy_logtraffic = policy['logtraffic']
                    policy_status = policy['status']
                    policy_comments = policy['comments']



                # NOTE(tonycheng): You can use "content['results'][10]" to get value
                return content
            except RuntimeError:
                LOG.error("Unknown error when parsing resp.text")
            finally:
                self.logout()
        else:
            LOG.error("Resp text : %s" % resp.text)
            LOG.error("Resp reason : %s" % resp.reason)
            return resp.ok

    def add_policy(self, payload, vdom='root'):
        if payload is None:
            LOG.error("you need to provide something "
                      "to add policy into firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is add_policy method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall/policy/'

        resp = requests.post(endpoint,
                             params=self._params,
                             json=payload,
                             verify=False,
                             headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            LOG.error("Resp reason is : %s" % resp.reason)
        else:
            LOG.info("Resp text is : %s" % resp.text)
        return resp.ok

    def del_policy(self, mkey, vdom='root'):
        if mkey is None:
            LOG.error("you need to provide policy id \
                   to delete policy from firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is 'del_policy' method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall/policy/' + mkey

        resp = requests.delete(endpoint,
                               params=self._params,
                               verify=False,
                               headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            LOG.error("Resp reason is : %s" % resp.reason)
        else:
            LOG.info("Resp text is : %s" % resp.text)
        return resp.ok

    def set_policy(self, mkey, payload, vdom='root'):
        if payload is None or mkey is None:
            LOG.error("you need to provide something \
                   to update policy into firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is set_policy method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall/policy/' + mkey

        resp = requests.put(endpoint,
                            params=self._params,
                            json=payload,
                            verify=False,
                            headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            LOG.error("Resp reason is : %s" % resp.reason)
        else:
            LOG.info("Resp text is : %s" % resp.text)
        return resp.ok

    def get_service(self, vdom='root'):
        self._params["vdom"] = vdom
        LOG.info("This is 'get_service' method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall.service/custom/'
        resp = requests.get(endpoint,
                            params=self._params,
                            verify=False,
                            headers=self._headers)
        if resp.ok:
            try:
                content = literal_eval(resp.text)
                print(content)

                # NOTE(tonycheng): You can use "content['results'][10]" to get value
                return content
            except RuntimeError:
                LOG.error("Unknown error when parsing resp.text")
            finally:
                self.logout()
        else:
            LOG.error("Resp text : %s" % resp.text)
            LOG.error("Resp reason : %s" % resp.reason)
            return resp.ok

    def add_service(self, payload, vdom='root'):
        if payload is None:
            LOG.error("you need to provide something "
                      "to add service into firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is 'add_service' method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall.service/custom/'

        resp = requests.post(endpoint,
                             params=self._params,
                             json=payload,
                             verify=False,
                             headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            LOG.error("Resp reason is : %s" % resp.reason)
        else:
            LOG.info("Resp text is : %s" % resp.text)
        return resp.ok

    def del_service(self, name, vdom='root'):
        if name is None:
            LOG.error("you need to provide service name \
                   to delete service from firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is 'del_service' method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall.service/custom/' + name

        resp = requests.delete(endpoint,
                               params=self._params,
                               verify=False,
                               headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            LOG.error("Resp reason is : %s" % resp.reason)
        else:
            LOG.info("Resp text is : %s" % resp.text)
        return resp.ok

    def set_service(self, name, payload, vdom='root'):
        if payload is None or name is None:
            LOG.error("you need to provide something \
                   to update service into firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is 'set_service' method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall.service/custom/' + name

        resp = requests.put(endpoint,
                            params=self._params,
                            json=payload,
                            verify=False,
                            headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            LOG.error("Resp reason is : %s" % resp.reason)
        else:
            LOG.info("Resp text is : %s" % resp.text)
        return resp.ok

    def get_vipgrp(self, vdom='root'):
        self._params["vdom"] = vdom
        LOG.info("This is 'get_vipgrp' method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall/vipgrp'
        resp = requests.get(endpoint,
                            params=self._params,
                            verify=False,
                            headers=self._headers)
        if resp.ok:
            try:
                content = literal_eval(resp.text)
                print(content)

                # NOTE(tonycheng): You can use "content['results'][10]" to get value
                return content
            except RuntimeError:
                LOG.error("Unknown error when parsing resp.text")
            finally:
                self.logout()
        else:
            LOG.error("Resp text : %s" % resp.text)
            LOG.error("Resp reason : %s" % resp.reason)
            return resp.ok

    def add_vipgrp(self, payload, vdom='root'):
        if payload is None:
            LOG.error("you need to provide something "
                      "to add vip group into firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is 'add_vipgrp' method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall/vipgrp/'

        resp = requests.post(endpoint,
                             params=self._params,
                             json=payload,
                             verify=False,
                             headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            LOG.error("Resp reason is : %s" % resp.reason)
        else:
            LOG.info("Resp text is : %s" % resp.text)
        return resp.ok

    def del_vipgrp(self, name, vdom='root'):
        if name is None:
            LOG.error("you need to provide vipgrp name \
                   to delete service from firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is 'del_vipgrp' method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall/vipgrp/' + name

        resp = requests.delete(endpoint,
                               params=self._params,
                               verify=False,
                               headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            LOG.error("Resp reason is : %s" % resp.reason)
        else:
            LOG.info("Resp text is : %s" % resp.text)
        return resp.ok

    def set_vipgrp(self, name, payload, vdom='root'):
        if payload is None or name is None:
            LOG.error("you need to provide something \
                   to update vip group into firewall!")

        self._params["vdom"] = vdom
        LOG.info("This is 'set_vipgrp' method, vdom=%s" % vdom)
        endpoint = self.baseurl + self.cmdburl + '/firewall/vipgrp/' + name

        resp = requests.put(endpoint,
                            params=self._params,
                            json=payload,
                            verify=False,
                            headers=self._headers)
        if not resp.ok:
            LOG.error("Return Code is : %s" % resp.status_code)
            LOG.error("Resp text is : %s" % resp.text)
            LOG.error("Resp reason is : %s" % resp.reason)
        else:
            LOG.info("Resp text is : %s" % resp.text)
        return resp.ok

    def save_config(self, vdom='root'):
        """Not Implemented"""
        raise NotImplementedError
