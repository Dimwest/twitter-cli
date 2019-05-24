#!/usr/bin/env bash

if [ -x "$(command -v docker)" ]; then
    echo "Docker is already installed, checking for Postgres image..."
else
    echo "Installing Docker ..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
fi

docker inspect --type=image postgres:latest
if [ $? -eq 0 ] ; then
    echo "Postgres image already exists, starting..."
else
    docker pull postgres:latest && echo "Postgres image successfully pulled..." || echo "Error: failed pulling Postgres image !"
fi

echo "Running Postgres image..."
docker run --rm  --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data postgres
