FROM alphacep/kaldi-vosk-server-gpu:latest

LABEL maintainer=FAV

ENV TZ Europe/Moscow
RUN echo $TZ > /etc/timezone

WORKDIR /opt/vosk-server/websocket-gpu-batch
CMD ["python3" "./asr_server_gpu.py"]
