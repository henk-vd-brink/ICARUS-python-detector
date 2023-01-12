#!/bin/bash

docker-compose -f docker-compose.ci.build.yaml --env-file .env.example build
docker-compose --env-file .env.example up