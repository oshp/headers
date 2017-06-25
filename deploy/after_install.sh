#!/usr/bin/env bash
cd /opt/headers
docker rmi -f $(docker images | grep -i secureheaders | awk '{print $3}')
docker build -f docker/secureheaders/Dockerfile -t oshp/secureheaders:3.1.1
