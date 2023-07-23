#!/bin/bash

# Número de instancias a ejecutar
instances=5

# Puerto inicial
start_port=5433

for (( instance=1; instance<=$instances; instance++ ))
do
    port=$(($start_port + $instance - 1))
    compose_file=${compose_location}docker-compose-${port}.yml

    # Generar archivo docker-compose.yml
    /bin/cat <<EOM >$compose_file
version: "3"

services:
  postgres:
    image: postgres
    container_name: bank_container_${port}
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: mysecretpassword
      POSTGRES_DB: bank_${instance}
    ports:
      - "${port}:5432"
    volumes:
      - postgres_${instance}:/data/postgres
    restart: always

volumes:
  postgres_${instance}:
EOM

    # Ejecutar docker-compose
    docker-compose -f $compose_file up -d

done