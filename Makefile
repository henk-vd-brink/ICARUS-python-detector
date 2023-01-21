# General
build_and_run:
	./scripts/build_and_run.sh

build_baseimage:
	./scripts/build_baseimage.sh

push_baseimage:
	./scripts/push_baseimage.sh

# Formatter
black:
	python3 -m black .
