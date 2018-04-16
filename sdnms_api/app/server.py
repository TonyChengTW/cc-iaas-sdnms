import os
import falcon

from oslo_log import log

from sdnms_api.models.manager import DBManager
from sdnms_api.util import simport
from sdnms_api.resources import health
from sdnms_api import config

LOG = log.getLogger(__name__)
CONF = config.CONF

def launch(config_file):
    config.init()

    mgr = None
    #mgr = DBManager(CONF.database.url)
    #mgr.setup()

    app = falcon.API()
    health = simport.load(CONF.dispatcher.health)(mgr)
    app.add_route("/health", health)

    LOG.debug('Dispatcher drivers have been added to the routes!')
    return app

def get_wsgi_app(config_base_path=None, **kwargs):
    config_file = kwargs.get('config', 'sdnms_api.ini')

    if config_base_path is None:
        config_base_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), '../../../etc/sdnms_api')

    config_file = os.path.join(config_base_path, config_file)
    return launch(config_file)

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 8000, launch())
    httpd.serve_forever()
