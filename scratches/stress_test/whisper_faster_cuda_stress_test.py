import concurrent.futures as pool
import random
import threading
import time

from faster_whisper import WhisperModel
path_sound = '/opt/scripts/whisper_example/scratches/stress_test/sounds/2'
MAX_INSTANCE = 5
names = []

for i in range(0, 1000):
    names.append(random.randrange(0, 10))


def transcribe_file(model):
    th_name = threading.current_thread().name
    while len(names) > 0:
        filename = names.pop() % 10
        filepath = f'{path_sound}/{filename}.wav'
        print(f'run th_name={th_name} with filepath={filepath}')
        try:
            decode_options = dict(language='ru', beam_size=1)
            transcribe_options = dict(task="transcribe", **decode_options)
            segments, info = model.transcribe(filepath, **transcribe_options)

            text = ''
            for segment in segments:
                text = text + ' ' + segment.text

            print(f'end th_name={th_name} with filepath={filepath} and text={text}')
        except Exception as exp:
            print(exp)


models = []
for rec in range(0, MAX_INSTANCE):
    print(rec)
    model_path = "/opt/scripts/whisper_example/whisper-small-float16/"
    gpu_model = WhisperModel(model_path, device="cuda", compute_type="float16")
    models.append(gpu_model)
    # WARMUP
    warmup_decode_options = dict(language='ru', beam_size=1)
    warmup_transcribe_options = dict(task="transcribe", **warmup_decode_options)
    warmup_segments, warmup_info = gpu_model.transcribe(f'{path_sound}/0.wav', **warmup_transcribe_options)


try:
    start_time = time.time()
    with pool.ThreadPoolExecutor(max_workers=MAX_INSTANCE) as executor:
        res = executor.map(transcribe_file, models)
    print(f"full_time={(time.time() - start_time)}")
except Exception as e:
    print(e)
