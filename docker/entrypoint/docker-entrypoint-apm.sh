#!/bin/sh
set -e

NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program python -m flask run --host='0.0.0.0' --port=5000
