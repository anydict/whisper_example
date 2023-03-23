import concurrent.futures as pool
import random
import threading
import time

# from nemo.collections.asr.models import EncDecCTCModel
import nemo.collections.asr as nemo_asr

path_sound = '/opt/scripts/whisper_example/scratches/stress_test/sounds/16khz5'
MAX_INSTANCE = 2
quartznet = nemo_asr.models.EncDecCTCModel.restore_from("/home/anydict/QuartzNet15x5_golos.nemo")  # SberRuModel
names = []

for i in range(0, 100):
    names.append([f'{path_sound}/{num%10}.wav' for num in range(0, 10)])


def transcribe_file(model):
    th_name = threading.current_thread().name

    while len(names) > 0:
        files = names.pop()
        print(f'run th_name={th_name} with and m={model}')
        try:
            first_time = time.time()
            for file, transcription in zip(files, quartznet.transcribe(paths2audio_files=files)):
                pass
                print(f'end th_name={th_name} with filepath={file} and text={transcription}')
            print(f"end_time={(time.time() - first_time)}")
        except Exception as exp:
            print(exp)



models = []
for rec in range(0, MAX_INSTANCE):
    print(rec)

    # quartznet = nemo_asr.models.EncDecCTCModel.restore_from("/home/anydict/QuartzNet15x5_golos.nemo")  # SberRuModel
    # the model from below is worse (bigger WER)
    # quartznet = EncDecCTCModel.from_pretrained("stt_ru_quartznet15x5") # Default Nvidia RuModel

    models.append('')
    # WARMUP
    warmup_files = [f'{path_sound}/0.wav']  # file duration should be less than 25 seconds
    for _, warmup_transcription in zip(warmup_files, quartznet.transcribe(paths2audio_files=warmup_files)):
        pass
        print(warmup_transcription)

try:
    start_time = time.time()
    with pool.ThreadPoolExecutor(max_workers=MAX_INSTANCE) as executor:
        res = executor.map(transcribe_file, models)
    print(f"full_time={(time.time() - start_time)}")
except Exception as e:
    print(e)
