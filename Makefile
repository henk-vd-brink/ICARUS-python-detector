# General
build_and_run:
	./scripts/build_and_run.sh

build_baseimage:
	./scripts/build_baseimage_on_amd64.sh

# Formatter
black:
	python3 -m black .
