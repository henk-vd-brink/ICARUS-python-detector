build_and_run:
	./scripts/build_and_run.sh

build_and_push:
	./scripts/build_and_push.sh

build_and_deploy:
	./scripts/build_and_deploy_to_iotedge.sh

# Tests
test_build:
	docker-compose -f docker-compose.ci.build.yaml build icarus-edge-detector

test_unit: test_build
	docker-compose -f docker-compose.ci.test.yaml run --entrypoint=pytest icarus-edge-detector /home/docker_user/tests/unit

black:
	python3 -m black .
