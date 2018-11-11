nvidia-docker run --rm -it --ipc=host \
	-p 18888:18888 \
	-v "$(pwd)":/app \
	-v /tmp:/tmp \
	climate-topic-modeling:latest
