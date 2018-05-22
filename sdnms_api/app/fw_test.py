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

    vdom = 'root'
    # m.call_firewall(method='info')

    # -------- Add VDOM ------------------------------------------------------
    name = 'tony3'
    m.call_firewall(method='add_vdom', name=name)

    # m.call_firewall(method='get_vdom')


    """
    # -------- Get Addr -------------------------------------------------
    m.call_firewall(method='get_addr', vdom=vdom)


    # -------- Add Addr -------------------------------------------------
    payload = {
        'name': "11.11.11.178",
        'type': "ipmask",
        'comment' : "test add method",
        'subnet': "11.11.11.178 255.255.255.255"
    }
    m.call_firewall(method='add_addr', vdom=vdom, payload=payload)

    # -------- Del Addr -------------------------------------------------
    name = '11.11.11.178'
    m.call_firewall(method='del_addr', vdom=vdom, name=name)

    # -------- Set Addr -------------------------------------------------
    name = '11.11.11.178'
    payload = {
        'name': "11.11.11.179",
        'type': "ipmask",
        'comment': "test set method",
        'subnet': "11.11.11.179 255.255.255.255"
    }
    m.call_firewall(method='set_addr', vdom=vdom, name=name,
                    payload=payload)

    # ------------  Get VIP -----------------------------------------------
    m.call_firewall(method='get_vip', vdom=vdom)

    # ------------  Add/Set VIP -----------------------------------------------
    name = "vm3-icmp"
    payload = {
       "name":"vm3-ssh-update",
       "comment":"",
       "type":"static-nat",
       "extip":"100.100.100.104",
       "mappedip":[
         {
           "range":"11.11.11.103"
         }
       ],
       "extintf":"port1",
       "nat-source-vip":"disable",
       "portforward":"enable",
       "protocol":"telnet",
       "extport":"23",
       "mappedport":"23",
       "portmapping-type":"1-to-1"
    }
    m.call_firewall(method='add_vip', vdom=vdom, payload=payload)
    m.call_firewall(method='set_vip', vdom=vdom, payload=payload, name=name)

    name = 'vm3-ssh'
    m.call_firewall(method='del_vip', vdom=vdom, name=name)
    """
    #m.call_firewall(method='get_vipgrp', vdom=vdom)
    m.call_firewall(method='logout')

if __name__ == '__main__':
    run_test()