# General
build_and_run_dev:
	./scripts/build_and_run.sh dev

build_and_run_prod:
	./scripts/build_and_run.sh prod

build_baseimage:
	./scripts/buildx_baseimage.sh

# Formatter
black:
	python3 -m black .
