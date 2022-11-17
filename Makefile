build_and_run:
	./scripts/build_and_run.sh

dev_build_and_run:
	./scripts/build_and_run_dev.sh

# Tests
test_build:
	docker-compose -f docker-compose.ci.build.yaml build icarus-edge-detector

test_unit: test_build
	docker-compose -f docker-compose.ci.test.yaml run --entrypoint=pytest icarus-edge-detector /home/docker_user/tests/unit
