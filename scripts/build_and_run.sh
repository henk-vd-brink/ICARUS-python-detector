#!/bin/bash

docker-compose -f docker-compose.ci.build.yaml build icarus-edge-detector
docker-compose --env-file .env.example up