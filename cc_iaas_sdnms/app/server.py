
import os
import falcon

import cc_iaas_sdnms.util.simport
from oslo_config import cfg
from oslo_log import log

from cc_iaas_sdnms.db.manager import DBManager
from cc_iaas_sdnms.middleware.context import ContextMiddleware
from cc_iaas_sdnms.resources import scores


def launch(conf):
    config.parse_args()

    app = falcon.API(request_type=request.Request)

    scores = simport.load(cfg.CONF.dispatcher.metrics)()
    app.add_route("/scores", scores)


    # LOG.debug('Dispatcher drivers have been added to the routes!')
    return app

def get_wsgi_app(config_base_path=None, **kwargs):

    return launch()

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 8070, launch())
    httpd.serve_forever()