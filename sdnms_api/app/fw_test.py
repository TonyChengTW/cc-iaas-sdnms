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

    vdom = 'tony3'


    # m.call_firewall(method='info')


    """
    # -------- Add VDOM ------------------------------------------------------
    name = 'tony3'
    m.call_firewall(method='add_vdom', name=name)

    m.call_firewall(method='get_vdom')

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
    # name = '11.11.11.178'
    # m.call_firewall(method='del_addr', vdom=vdom, name=name)


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
    name = "test1"
    payload = {
       "name":"test1",
       "comment":"",
       "type":"static-nat",
       "extip":"103.103.103.103",
       "mappedip":[
         {
           "range":"13.13.13.103"
         }
       ],
       "extintf":"any",
       "nat-source-vip":"disable",
       "portforward":"enable",
       "protocol":"telnet",
       "extport":"23",
       "mappedport":"23",
       "portmapping-type":"1-to-1"
    }
    # m.call_firewall(method='add_vip', vdom=vdom, payload=payload)

    # m.call_firewall(method='set_vip', vdom=vdom, payload=payload, name=name)

    name = 'test1'
    m.call_firewall(method='del_vip', vdom=vdom, name=name)
    #m.call_firewall(method='get_vipgrp', vdom=vdom)
    m.call_firewall(method='logout')
    """

    # ------------  Get Policy -----------------------------------------------
    m.call_firewall(method='get_policy', vdom=vdom)

    # ------------  Add Policy -----------------------------------------------
    payload = {
                'name':'deny-vm2',
                'srcintf': [
                    {
                        'name': 'port1'
                    }
                    ],
                'dstintf':[
                    {
                        'name':'port2'
                    }
                    ],
                'srcaddr':[
                    {
                        'name':'all'
                    }
                    ],
                'dstaddr': [
                    {
                        'name': 'vip group1'
                    }
                    ],
                'service': [
                    {
                        'name': 'HTTP'
                    }
                    ],
                'nat':'disable',
                'action': 'deny',
                'schedule': 'always',
                'logtraffic': 'all',
                'status':'enable',
                'comments': 'test add/set policy via API'
            }
    # m.call_firewall(method='add_policy', payload=payload, vdom=vdom)

    mkey = '4'
    vdom = 'root'
    # m.call_firewall(method='set_policy', mkey=mkey, payload=payload, vdom=vdom)

    
    # ------------  Delete Policy -----------------------------------------------
    # m.call_firewall(method='del_policy', mkey=mkey, vdom=vdom)


    """
    # ------------  Get Service -----------------------------------------------
    # m.call_firewall(method='get_service', vdom=vdom)

    # ------------  Add Service -----------------------------------------------
    vdom = 'tony3'
    payload1 = {'name': 'add service1',
                'comment': '',
                'protocol': 'TCP\\/UDP\\/SCTP',   # protocol : 'ICMP' for only icmp
                'iprange': '1.2.3.4',
                'category': 'Web Access',   # need specify with a defined category
                'protocol-number': 6,     # ICMP=1, TCP=6 , UDP=17 , SCTP=132
                'tcp-portrange': '80'
                #'udp-portrange': '514
               }

    payload2 = {'name': 'add service2',
                'comment': '',
                'protocol': 'TCP\\/UDP\\/SCTP',  # protocol : 'ICMP' for only icmp
                'iprange': '5.6.7.8',
                'category': '',     # need specify with a defined category, a null value will be 'Uncategorized' cat.
                'protocol-number': 17,  # ICMP=1, TCP=6 , UDP=17 , SCTP=132
                # 'tcp-portrange': '80',
                'udp-portrange': '3389'
                }

    # m.call_firewall(method='add_service', payload=payload1, vdom=vdom)
    m.call_firewall(method='add_service', payload=payload2, vdom=vdom)


# ------------  Delete Service -----------------------------------------------
    name = 'add service1'
    vdom = 'tony3'
    m.call_firewall(method='del_service', name=name, vdom=vdom)

# ------------  Set Service -----------------------------------------------
    name = 'add service2'
    vdom = 'tony3'
    payload = {'name': 'set service2',
                'comment': '',
                'protocol': 'TCP\\/UDP\\/SCTP',  # protocol : 'ICMP' for only icmp
                'iprange': '5.6.7.8',
                'category': '',  # need specify with a defined category, a null value will be 'Uncategorized' cat.
                'protocol-number': 17,  # ICMP=1, TCP=6 , UDP=17 , SCTP=132
                # 'tcp-portrange': '80',
                'udp-portrange': '3390'
                }
    m.call_firewall(method='set_service', name=name, payload=payload, vdom=vdom)
    """
# ----------------- Get VIP Group ----------------------------------------------------------
    vdom = 'tony3'

    # m.call_firewall(method='get_vipgrp', vdom=vdom)

# ----------------- Add/Set VIP Group ----------------------------------------------------------
    name = 'vipgrp1-add'
    payload = {'name': 'vipgrp1-add',
               'interface': 'any',
               'member': [
                   # {'name': 'vm1-icmp'},
                   # {'name': 'vm2-http'},
                   # {'name': 'vm2-ssh'},
                   {'name': 'vip1'},
                   {'name': 'vip2'},
               ]
               }
    # m.call_firewall(method='add_vipgrp', payload=payload, vdom=vdom)
    # m.call_firewall(method='set_vipgrp', name=name, payload=payload, vdom=vdom)
    name = 'vipgrp1-add'
    # m.call_firewall(method='del_vipgrp', name=name, vdom=vdom)

if __name__ == '__main__':
    run_test()
