# General
build_and_run:
	./scripts/build_and_run.sh

build_and_push_base_image:
	./scripts/build_and_push_base_image.sh

# Formatter
black:
	python3 -m black .
