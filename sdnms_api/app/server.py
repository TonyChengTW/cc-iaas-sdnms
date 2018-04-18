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

LOG = log.getLogger(__name__)
CONF = config.CONF


def launch(config_file=None):
    if config_file is None:
        config_file = '/etc/sdnms_api/sdnms_api.ini'

    log.set_defaults()
    log.register_options(CONF)

    config.init(config_file=config_file)
    loader.setup(CONF)

    db = "mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(
            CONF.database.username, CONF.database.password,
            CONF.database.address, CONF.database.port, CONF.database.database_name)
    mgr = DBManager(db)
    mgr.setup()

    app = falcon.API()
    health = simport.load(CONF.dispatcher.health)(mgr)
    app.add_route("/health", health)
    firewall_address = simport.load(CONF.dispatcher.firewall_address)(mgr)
    app.add_route("/firewall/address", firewall_address)
    firewall_device = simport.load(CONF.dispatcher.firewall_device)(mgr)
    app.add_route("/firewall/device", firewall_device)

    LOG.debug('Dispatcher drivers have been added to the routes!')
    return app

def get_wsgi_app(config_base_path=None, **kwargs):
    return launch()

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 8000, get_wsgi_app())
    httpd.serve_forever()
