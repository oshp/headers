#!/usr/bin/env bash
cd /opt/headers && \
docker stack rm oshp && \
docker stop $(docker ps -q) && \
docker rmi -f $(docker images | grep -i secureheaders | awk '{print $3}')
