#!/bin/bash
WORKDIR="/opt/headers"

echo "[*] ajustando permissoes..."
cd $WORKDIR

chown -R ubuntu.ubuntu *

echo "[*] iniciando containers..."
docker-compose build
docker-compose up -d
