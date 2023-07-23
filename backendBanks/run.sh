#!/bin/bash

# Detener y eliminar contenedores así como volúmenes
docker-compose down -v

# Iniciar contenedores para PostgreSQL
docker-compose up -d
# Container name para banco 1: bank_container_1
# Container name para banco 2: bank_container_2

# Esperar a que los contenedores para PostgreSQL estén en línea
while ! docker exec -t bank_container_1 pg_isready -U postgres -d bank_1 -h localhost > /dev/null 2>&1; do
  sleep 1
done

while ! docker exec -t bank_container_2 pg_isready -U postgres -d bank_2 -h localhost > /dev/null 2>&1; do
  sleep 1
done

#
python main.py 8080 5432 "backendBanks/data/user1.json"
python main.py 8081 5433 "backendBanks/data/user2.json"