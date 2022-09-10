get_yolov4_weights:
	wget \
	https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights \
	-P ./icarus-detector/assets

build_and_run:
	./scripts/build_and_run.sh