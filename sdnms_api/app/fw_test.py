import falcon
import os
import sys

from oslo_log import log
from sdnms_api.models.manager import DBManager
from sdnms_api.utils import simport
from sdnms_api.resources import health
from sdnms_api.resources import firewall
from sdnms_api import config
from sdnms_api.driver import loader

import pdb

LOG = log.getLogger(__name__)
CONF = config.CONF


def run_test(config_file=None):
#    config_files = ['/home/tony/proj/cc-iaas-sdnms/etc/sdnms_api/sdnms_api.ini',
#                   '/home/tony/proj/cc-iaas-sdnms/etc/sdnms_api/backends/fw_fortinet_v5.6.3.ini'
#                   ]
    if config_file is None:
        config_file = '/etc/sdnms_api/sdnms_api.ini'

    log.set_defaults()
    log.register_options(CONF)

    config.init(config_file = config_file)
    loader.setup(CONF)

    from sdnms_api.backends.manager import BackendManager
    m = BackendManager()
    # m.use_firewall(index=1)
    m.use_firewall(identity='fortivm2')
    # m.use_firewall(identity='fw1')
    # m.use_firewall()
    m.call_firewall(method='info')

    vdom = 'root'
    m.call_firewall(method='get_addr')

    add_addr = {
        'name': "11.11.11.178",
        'type': "ipmask",
        'comment' : "test add method",
        'subnet': "11.11.11.178 255.255.255.255"
    }
    # m.call_firewall(method='add_addr', vdom=vdom, add_addr=add_addr)

    del_addr = '11.11.11.178'
    # m.call_firewall(method='del_addr', vdom=vdom, del_addr=del_addr)

    set_addr = '11.11.11.178'
    payload = {
        'name': "11.11.11.179",
        'type': "ipmask",
        'comment': "test set method",
        'subnet': "11.11.11.179 255.255.255.255"
    }
    m.call_firewall(method='set_addr', vdom=vdom, set_addr=set_addr,
                    payload=payload)

if __name__ == '__main__':
    run_test()