#!/usr/bin/env bash
docker rmi -f $(docker images | grep -i none | awk '{print $3}')
