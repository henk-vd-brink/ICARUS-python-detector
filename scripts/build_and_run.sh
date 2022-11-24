#!/bin/bash

docker-compose -f docker-compose.ci.build.yaml build
docker-compose --env-file .env.example up