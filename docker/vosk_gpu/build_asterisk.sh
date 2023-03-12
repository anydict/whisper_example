#!/bin/bash

# Сборка контейнера Vosk-Gpu

echo Build docker of Vosk GPU
version=1.0.0

docker build -t anydict/vosk_gpu:${version} \
-f Dockerfile .
