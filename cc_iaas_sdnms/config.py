import sys

from oslo_config import cfg
from oslo_log import log

from cc_iaas_sdnms import conf

CONF = conf.CONF
LOG = log.getLogger(__name__)

_CONF_LOADED = False
_GUNICORN_MARKER = 'gunicorn'

def parse_args(argv=None, config_file=None):
    """Loads application configuration.
    Loads entire application configuration just once.
    """
    global _CONF_LOADED
    if _CONF_LOADED:
        LOG.debug('Configuration has been already loaded')
        return

    log.set_defaults()
    log.register_options(CONF)

    argv = (argv if argv is not None else sys.argv[1:])
    args = ([] if _is_running_under_gunicorn() else argv or [])

    CONF(args=args,
         prog='api',
         project='SDNMS',
         version="1.0",
         default_config_files=[config_file] if config_file else None,
         description='SDNMS RESTful API')

    conf.register_opts()

    _CONF_LOADED = True

def _is_running_under_gunicorn():
    """Evaluates if api runs under gunicorn."""
    content = filter(lambda x: x != sys.executable and _GUNICORN_MARKER in x,
                     sys.argv or [])
    return len(list(content) if not isinstance(content, list) else content) > 0