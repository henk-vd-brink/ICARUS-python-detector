#!/bin/bash

docker-compose -f docker-compose.build.yaml build icarus-edge-detector
docker-compose --env-file .env.example up