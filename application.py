#!/usr/bin/env python
"""
eq-address-api entry point.
"""
import logging
from structlog import configure
from structlog.processors import JSONRenderer, TimeStamper, format_exc_info
from structlog.stdlib import add_log_level, LoggerFactory
from structlog.threadlocal import wrap_dict

from app import app

def configure_logging():
    # set up some sane logging, as opposed to what flask does by default
    log_format = "%(message)s"
    handler = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO, format=log_format, handlers=[handler])

    def parse_exception(_, __, event_dict):
        exception = event_dict.get('exception')
        if exception:
            event_dict['exception'] = exception.replace("\"", "'").split("\n")
        return event_dict

    # setup file logging
    renderer_processor = JSONRenderer()
    processors = [add_log_level, TimeStamper(key='created', fmt='iso'), format_exc_info, parse_exception, renderer_processor]
    configure(context_class=wrap_dict(dict), logger_factory=LoggerFactory(), processors=processors, cache_logger_on_first_use=True)

configure_logging()

if __name__ == '__main__':
    app.run(debug=True)
