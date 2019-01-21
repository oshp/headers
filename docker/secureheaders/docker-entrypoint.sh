#!/bin/sh
set -e

# explicit call without APM
# gunicorn -w 2 -b 0.0.0.0:5000 web.webui:app

# call with APM support
# > used on production <http://oshp.bsecteam.com>
# notice: no changes needed for local use
NEW_RELIC_CONFIG_FILE=./newrelic.ini exec newrelic-admin run-program \
gunicorn -w 2 -b 0.0.0.0:5000 web.webui:app
