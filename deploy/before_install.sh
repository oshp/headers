#!/usr/bin/env bash
docker rmi -f $(docker images | awk '{print $3}')
