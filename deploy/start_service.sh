#!/usr/bin/env bash
WORKDIR="/opt/headers"

echo "[*] ajustando permissoes..."
cd /opt

chown -R ubuntu.ubuntu *

echo "[*] iniciando containers..."
cd $WORKDIR
docker-compose build
docker-compose up -d
