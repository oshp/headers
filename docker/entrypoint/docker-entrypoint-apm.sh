#!/bin/sh
set -e

NEW_RELIC_CONFIG_FILE=./newrelic.ini newrelic-admin run-program \
gunicorn -w 2 -b 0.0.0.0:5000 web.webui:app
