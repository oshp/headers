#!/usr/bin/env bash
cd /opt/headers
docker build -f docker/secureheaders/Dockerfile -t oshp/secureheaders:3.1.1
