get_yolov4_weights:
	wget \
	https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights \
	-P ./icarus-detector/assets

convert_darknet_to_onnx:
	python3 -m scripts.python.darknet_to_onnx \
	--cfg_file /home/prominendt/repos/ICARUS-python-detector/icarus-detector/assets/yolov4-tiny.cfg \
	--weights_file /home/prominendt/repos/ICARUS-python-detector/icarus-detector/assets/yolov4-tiny.weights \
	--output_file /home/prominendt/repos/ICARUS-python-detector/icarus-detector/assets/yolov4-tiny.onnx

build_and_run:
	./scripts/build_and_run.sh