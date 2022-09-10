get_weights:
	wget \
	https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights \
	-P ./assets

build_and_run:
	./scripts/build_and_run.sh