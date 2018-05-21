#!/bin/bash
gunicorn -w 10 --worker-class gevent -b 0.0.0.0:5000 application:app
