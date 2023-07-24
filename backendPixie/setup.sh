#!/bin/bash
pip install -r requirements.txt

# Detener contenedores
docker-compose down -v

# Iniciar contenedores
docker-compose up -d

# Esperar a que los contenedores estén en línea
while ! docker exec -t pixie mongo --eval "db.stats()" > /dev/null 2>&1; do
  sleep 1
done


