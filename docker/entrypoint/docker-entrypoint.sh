#!/bin/sh
set -e

#python -m flask run --host='0.0.0.0' --port=5000
gunicorn -w 2 -b 0.0.0.0:5000 web.webui:app
