import concurrent.futures as pool
import threading
import time

# from nemo.collections.asr.models import EncDecCTCModel
import nemo.collections.asr as nemo_asr
path_sound = '/opt/scripts/whisper_example/scratches/stress_test/sounds'
MAX_INSTANCE = 5
names = list(range(0, 1000))


def transcribe_file(model):
    th_name = threading.current_thread().name
    while len(names) > 0:
        filename = names.pop() % 2
        filepath = f'{path_sound}/{filename}.wav'
        print(f'run th_name={th_name} with filepath={filepath}')

        try:
            files = [filepath]
            for _, transcription in zip(files, model.transcribe(paths2audio_files=files)):
                pass
                print(f'end th_name={th_name} with filepath={filepath} and text={transcription}')
        except Exception as exp:
            print(exp)


models = []
for rec in range(0, MAX_INSTANCE):
    print(rec)

    quartznet = nemo_asr.models.EncDecCTCModel.restore_from("/home/anydict/QuartzNet15x5_golos.nemo")  # SberRuModel
    # the model from below is worse (bigger WER)
    # quartznet = EncDecCTCModel.from_pretrained("stt_ru_quartznet15x5") # Default Nvidia RuModel

    models.append(quartznet)
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
