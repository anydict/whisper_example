#!/bin/bash

# Run instance with number 0 with version image Vosk GPU Small
# bsh 0 small
# or Vosk GPU 0.42
# bash docker_run_vosk_gpu.sh 0 0.42
# or Vosk GPU 0.22
# bash docker_run_vosk_gpu.sh 0 0.22


if [ -z "$1" ]; then
  echo "No instance number. Use 0-9. Example docker_run_asterisk 2" && exit 0
else
  instance_name=vosk_gpu-$1
fi

if [ -z "$2" ]; then
  echo "No version (choose small or 0.42 or 0.22)" && exit 0
elif [ "$2" = "small" ]; then
  host_model_path="/opt/vosk/model/vosk-model-small-ru-0.22"
elif [ "$2" = "0.22" ]; then
  host_model_path="/opt/vosk/model/vosk-model-ru-0.22"
elif [ "$2" = "0.42" ]; then
  host_model_path="/opt/vosk/model/vosk-model-ru-0.42"
else
  echo "No found version=$2. Choose small or 0.42 or 0.22" && exit 0
fi

echo "host_model_path=$host_model_path"

docker stop "$instance_name"
docker rm "$instance_name"

# host_model_path="/opt/vosk/model/vosk-model-en-us-0.22"
# host_model_path="/opt/vosk/model/vosk-model-ru-0.42"
# host_model_path="/opt/vosk/model/vosk-model-ru-0.22"
# host_model_path="/opt/vosk/model/vosk-model-small-ru-0.22"


docker run \
  -d \
  --runtime=nvidia \
  --restart=always \
  --net=host \
  -v "$host_model_path":/opt/vosk-server/websocket-gpu-batch/model \
  -v /tmp/:/tmp/ \
  --name "$instance_name" \
  anydict/vosk_gpu:1.0.0 \
  python3 asr_server_gpu.py

#  sleep infinity
# -p 2700:2700
