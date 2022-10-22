get_yolov4_weights:
	wget \
	https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights \
	-P ./icarus-detector/assets

get_yolov4_onnx:
	wget \
	https://github.com/onnx/models/raw/main/vision/object_detection_segmentation/yolov4/model/yolov4.onnx \
	-P ./icarus-detector/assets

convert_darknet_to_onnx:
	python3 -m scripts.python.darknet_to_onnx \
	--cfg_file /home/prominendt/repos/ICARUS-python-detector/icarus-detector/assets/yolov4-tiny.cfg \
	--weights_file /home/prominendt/repos/ICARUS-python-detector/icarus-detector/assets/yolov4-tiny.weights \
	--output_file /home/prominendt/repos/ICARUS-python-detector/icarus-detector/assets/yolov4-tiny.onnx

build_and_run:
	./scripts/build_and_run.sh

debug:
	docker run -it --privileged -v /home/jetson/repos/ICARUS-python-detector/icarus-edge-detector/src/:/home/docker_user/src -v /home/jetson/repos/ICARUS-python-detector/icarus-edge-detector/assets/:/home/docker_user/assets --network host cricarusprod001.azurecr.io/icarus-edge-detector bash