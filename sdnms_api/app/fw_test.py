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
    #m.use_firewall(index=1)
    m.use_firewall(identity='fw1')
    m.call_firewall(method='info')
    m.call_firewall(method='get_addr')

if __name__ == '__main__':
    run_test()