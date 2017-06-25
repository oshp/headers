#!/usr/bin/env bash
cd /opt/headers/
docker stack deploy -c docker-compose-swarm.yml oshp
