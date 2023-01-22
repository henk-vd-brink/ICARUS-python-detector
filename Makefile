# General
build_and_run_dev:
	./scripts/build_and_run.sh dev

# Build base image on amd64
buildx_baseimage:
	./scripts/buildx_baseimage.sh

# Formatter
black:
	python3 -m black .
