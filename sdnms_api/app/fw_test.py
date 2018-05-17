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

    log.register_options(CONF)
    config.init(config_file = config_file)
    # pdb.set_trace()
    loader.setup(CONF)

    log.setup(CONF, 'test1')

    from sdnms_api.backends.manager import BackendManager
    m = BackendManager()
    # -------- Use Firewall -------------------------------------------------
    # m.use_firewall(index=1)
    m.use_firewall(identity='fortivm2')
    # m.use_firewall(identity='fw1')
    # m.use_firewall()
    m.call_firewall(method='info')
    vdom = 'root'

    """
    # -------- Get Addr -------------------------------------------------

    m.call_firewall(method='get_addr', vdom=vdom)
    # -------- Add Addr -------------------------------------------------
    add_addr = {
        'name': "11.11.11.178",
        'type': "ipmask",
        'comment' : "test add method",
        'subnet': "11.11.11.178 255.255.255.255"
    }
    m.call_firewall(method='add_addr', vdom=vdom, add_addr=add_addr)

    # -------- Del Addr -------------------------------------------------
    del_addr = '11.11.11.178'
    m.call_firewall(method='del_addr', vdom=vdom, del_addr=del_addr)

    # -------- Set Addr -------------------------------------------------
    set_addr = '11.11.11.178'
    payload = {
        'name': "11.11.11.179",
        'type': "ipmask",
        'comment': "test set method",
        'subnet': "11.11.11.179 255.255.255.255"
    }
    m.call_firewall(method='set_addr', vdom=vdom, set_addr=set_addr,
                    payload=payload)
    """
    # ------------  Get VIP -----------------------------------------------
    m.call_firewall(method='get_vip', vdom=vdom)

    """
    # ------------  Add VIP -----------------------------------------------
    payload = {
       "name":"vm3-ssh",
       "comment":"",
       "type":"static-nat",
       "extip":"100.100.100.103",
       "mappedip":[
         {
           "range":"11.11.11.103"
         }
       ],
       "extintf":"port1",
       "nat-source-vip":"disable",
       "portforward":"enable",
       "protocol":"ssh",
       "extport":"22",
       "mappedport":"22",
       "portmapping-type":"1-to-1"
    }
    m.call_firewall(method='add_vip', vdom=vdom, payload=payload)
    """
    m.call_firewall(method='logout')
if __name__ == '__main__':
    run_test()