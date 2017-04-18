#!/bin/bash
WORKDIR="/opt/headers"

echo "[*] iniciando processo de build..."
cd $WORKDIR
docker-compose stop

echo "[*] removendo imagens antigas."
docker rmi -f $(docker images | grep -i oshp/database | awk '{print $3}')
docker rmi -f $(docker images | grep -i oshp/secureheaders | awk '{print $3}')
docker rmi -f $(docker images | grep -i redis | awk '{print $3}')
