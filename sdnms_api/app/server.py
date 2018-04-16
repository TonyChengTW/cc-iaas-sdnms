
import os
import falcon

from oslo_log import log

from cc_iaas_sdnms.models.manager import DBManager
from cc_iaas_sdnms.middleware.context import ContextMiddleware
from cc_iaas_sdnms.util import simport
from cc_iaas_sdnms.resources import scores
from cc_iaas_sdnms import config

LOG = log.getLogger(__name__)
CONF = config.CONF

def launch():
    #config.parse_args()

    mgr = DBManager(CONF.database.url)
    mgr.setup()

    app = falcon.API()
    scores = simport.load(CONF.dispatcher.scores)(mgr)
    app.add_route("/scores", scores)

    LOG.debug('Dispatcher drivers have been added to the routes!')
    return app

def get_wsgi_app():

    return launch()

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 8070, launch())
    httpd.serve_forever()
