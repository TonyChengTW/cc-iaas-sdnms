import falcon
import os
import sys

from oslo_log import log
from sdnms_api.models.manager import DBManager
from sdnms_api.utils import simport
from sdnms_api.resources import health
from sdnms_api import config

LOG = log.getLogger(__name__)
CONF = config.CONF


def launch(config_file=None):
    if config_file is None:
        config_file = '/etc/sdnms_api/sdnms_api.ini'

    log.set_defaults()
    log.register_options(CONF)

    config.init(config_file=config_file)

    mgr = None
    #mgr = DBManager(CONF.database.url)
    #mgr.setup()

    app = falcon.API()
    health = simport.load(CONF.dispatcher.health)(mgr)
    app.add_route("/health", health)

    LOG.debug('Dispatcher drivers have been added to the routes!')
    return app

def get_wsgi_app(config_base_path=None, **kwargs):
    return launch()

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 8000, get_wsgi_app())
    httpd.serve_forever()
