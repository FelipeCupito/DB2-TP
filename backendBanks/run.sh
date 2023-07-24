#!/bin/bash

# Detener y eliminar contenedores así como volúmenes
docker-compose down -v

# Iniciar contenedores para PostgreSQL
docker-compose up -d

# Esperar a que los contenedores para PostgreSQL estén en línea
while ! docker exec -t bank_1 pg_isready -U postgres -d postgres -h localhost > /dev/null 2>&1; do
  sleep 1
done

while ! docker exec -t bank_2 pg_isready -U postgres -d postgres -h localhost > /dev/null 2>&1; do
  sleep 1
done

#

#pip install -r requirements.txt

python3 main.py 8080 5432 "data/user1.json" &
python3 main.py 8090 5433 "data/user2.json" &