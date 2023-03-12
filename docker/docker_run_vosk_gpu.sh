#!/bin/bash

# Run instance with number 2 with version image Vosk GPU
# bash docker_run_vosk_gpu.sh 2 1.0.0

if [ -z "$1" ]; then
  echo "No instance number. Use 0-9. Example docker_run_asterisk 2" && exit 0
else
  instance_name=vosk_gpu-$1
fi

if [ -z "$2" ]; then
  echo "No version" && exit 0
else
  version=$2
fi

docker stop "$instance_name"
docker rm "$instance_name"

# host_model_path="/opt/vosk/model/vosk-model-en-us-0.22"
host_model_path="/opt/vosk/model/vosk-model-ru-0.42"
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
  anydict/vosk_gpu:"$version" \
  sleep infinity

# -p 2700:2700
