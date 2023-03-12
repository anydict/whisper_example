from nemo.collections.asr.models import EncDecCTCModel
from time import time, process_time
import nemo.collections.asr as nemo_asr

real_time = []
cpu_time = []
path_sound = '/opt/scripts/whisper_example/scratches/'
# quartznet = EncDecCTCModel.from_pretrained("stt_ru_quartznet15x5") # Default Nvidia RuModel
quartznet = nemo_asr.models.EncDecCTCModel.restore_from("/home/anydict/QuartzNet15x5_golos.nemo")  # SberRuModel


def timer_func(func):
    def wrap_func(*args, **kwargs):
        real_t1 = time()
        cpu_t1 = process_time()
        result = func(*args, **kwargs)
        real_t2 = time()
        cpu_t2 = process_time()
        print(f'Function {func.__name__!r} real executed in {(real_t2-real_t1):.4f}s')
        print(f'Function {func.__name__!r} cpu executed in {(cpu_t2 - cpu_t1):.4f}s')
        real_time.append(real_t2 - real_t1)
        cpu_time.append(cpu_t2 - cpu_t1)
        return result
    return wrap_func


@timer_func
def transcribe_file(name: str):
    files = [name]  # file duration should be less than 25 seconds

    for filepath, transcription in zip(files, quartznet.transcribe(paths2audio_files=files)):
        print(f"Audio in {filepath} was recognized as: {transcription}")


# warmup
real_time.clear()
cpu_time.clear()
transcribe_file(f'{path_sound}long/example_1.wav')


real_time.clear()
cpu_time.clear()
for i in range(0, 20):
    transcribe_file(f'{path_sound}short/yes_good.wav')
print(f'real={sum(real_time)/len(real_time)} cpu={sum(cpu_time)/len(cpu_time)}\n\n')

real_time.clear()
cpu_time.clear()
for i in range(0, 20):
    transcribe_file(f'{path_sound}short/yes_good_agree_3sec.wav')
print(f'real={sum(real_time)/len(real_time)} cpu={sum(cpu_time)/len(cpu_time)}\n\n')

real_time.clear()
cpu_time.clear()
for i in range(0, 20):
    transcribe_file(f'{path_sound}short/yes_good_agree_say_about_all_5sec.wav')
print(f'real={sum(real_time)/len(real_time)} cpu={sum(cpu_time)/len(cpu_time)}\n\n')


real_time.clear()
cpu_time.clear()
for i in range(0, 20):
    transcribe_file(f'{path_sound}short/yes_good_agree_say_about_all_blabla_10sec.wav')
print(f'real={sum(real_time)/len(real_time)} cpu={sum(cpu_time)/len(cpu_time)}\n\n')


real_time.clear()
cpu_time.clear()
for i in range(0, 20):
    transcribe_file(f'{path_sound}long/text_to_voice_30sec.wav')
print(f'real={sum(real_time)/len(real_time)} cpu={sum(cpu_time)/len(cpu_time)}\n\n')


real_time.clear()
cpu_time.clear()
for i in range(0, 20):
    transcribe_file(f'{path_sound}long/text_to_voice_60sec.wav')
print(f'real={sum(real_time)/len(real_time)} cpu={sum(cpu_time)/len(cpu_time)}\n\n')


real_time.clear()
cpu_time.clear()
for i in range(0, 20):
    transcribe_file(f'{path_sound}long/fast_news_600sec.wav')
print(f'real={sum(real_time)/len(real_time)} cpu={sum(cpu_time)/len(cpu_time)}\n\n')
