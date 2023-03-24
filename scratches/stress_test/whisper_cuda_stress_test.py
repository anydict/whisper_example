import concurrent.futures as pool
import threading
import time

import whisper
path_sound = '/opt/scripts/whisper_example/scratches/stress_test/sounds/5second'
MAX_INSTANCE = 3
names = list(range(0, 1000))


def transcribe_file(model):
    th_name = threading.current_thread().name
    while len(names) > 0:
        filename = names.pop() % 10
        filepath = f'{path_sound}/{filename}.wav'
        print(f'run th_name={th_name} with filepath={filepath}')
        try:
            decode_options = dict(language="ru", fp16=True)
            transcribe_options = dict(task="transcribe", **decode_options)
            transcription = model.transcribe(filepath, **transcribe_options)

            print(f'end th_name={th_name} with filepath={filepath} and text={transcription["text"]}')
        except Exception as exp:
            print(exp)


models = []
for rec in range(0, MAX_INSTANCE):
    print(rec)
    gpu_model = whisper.load_model("tiny", device='cuda')
    models.append(gpu_model)
    # WARMUP
    warmup_decode_options = dict(language="ru", fp16=True)
    warmup_transcribe_options = dict(task="transcribe", **warmup_decode_options)
    warmup_transcription = gpu_model.transcribe(f'{path_sound}/0.wav', **warmup_transcribe_options)


try:
    start_time = time.time()
    with pool.ThreadPoolExecutor(max_workers=MAX_INSTANCE) as executor:
        res = executor.map(transcribe_file, models)
    print(f"full_time={(time.time() - start_time)}")
except Exception as e:
    print(e)
