# General
build_and_run_dev:
	./scripts/build_and_run.sh dev


buildx_baseimage:
	./scripts/buildx_baseimage.sh

buildx_image:
	./scripts/buildx_image.sh

# Formatter
black:
	python3 -m black .
