#!/bin/sh
set -e

gunicorn -w 2 -b 0.0.0.0:5000 web.webui:app
