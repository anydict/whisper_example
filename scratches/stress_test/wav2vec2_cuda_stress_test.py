import concurrent.futures as pool
import threading
import time

from huggingsound import SpeechRecognitionModel
path_sound = '/opt/scripts/whisper_example/scratches/stress_test/sounds/2'
MAX_INSTANCE = 4
names = list(range(0, 1000))


def transcribe_file(model):
    th_name = threading.current_thread().name
    while len(names) > 0:
        filename = names.pop() % 10
        filepath = f'{path_sound}/{filename}.wav'
        print(f'run th_name={th_name} with filepath={filepath}')
        try:
            transcription = model.transcribe([f'{path_sound}/0.wav'])
            text = transcription[0]['transcription']

            print(f'end th_name={th_name} with filepath={filepath} and text={text}')
        except Exception as exp:
            print(exp)


models = []
for rec in range(0, MAX_INSTANCE):
    print(rec)
    gpu_model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-russian", device='cuda:0')
    models.append(gpu_model)
    # WARMUP
    warmup_transcription = gpu_model.transcribe([f'{path_sound}/0.wav'])


try:
    start_time = time.time()
    with pool.ThreadPoolExecutor(max_workers=MAX_INSTANCE) as executor:
        res = executor.map(transcribe_file, models)
    print(f"full_time={(time.time() - start_time)}")
except Exception as e:
    print(e)
