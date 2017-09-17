#!/usr/bin/env bash
cd /opt/headers
git pull
docker stack rm oshp
