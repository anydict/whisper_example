
from time import time, process_time
from huggingsound import SpeechRecognitionModel
time_list = []


def timer_func(func):
    def wrap_func(*args, **kwargs):
        real_t1 = time()
        cpu_t1 = process_time()
        result = func(*args, **kwargs)
        real_t2 = time()
        cpu_t2 = process_time()
        print(f'Function {func.__name__!r} real executed in {(real_t2-real_t1):.4f}s')
        print(f'Function {func.__name__!r} cpu executed in {(cpu_t2 - cpu_t1):.4f}s')
        time_list.append(real_t2-real_t1)
        return result
    return wrap_func


@timer_func
def transcribe_file(name: str):
    transcriptions = model.transcribe([name])
    print(transcriptions)
    

model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-russian", device='cuda:0')
# warmup
time_list.clear()
transcribe_file('long/example_1.wav')


time_list.clear()
for rec in range(0, 27):
    transcribe_file('/opt/scripts/whisper_example/scratches/short/yes_good.wav')
print(time_list)
print(sum(time_list)/len(time_list))

time_list.clear()
for rec in range(0, 27):
    transcribe_file('/opt/scripts/whisper_example/scratches/short/yes_good_agree_3sec.wav')
print(time_list)
print(sum(time_list)/len(time_list))

time_list.clear()
for rec in range(0, 27):
    transcribe_file('/opt/scripts/whisper_example/scratches/short/yes_good_agree_say_about_all_5sec.wav')
print(time_list)
print(sum(time_list)/len(time_list))


time_list.clear()
for rec in range(0, 27):
    transcribe_file('/opt/scripts/whisper_example/scratches/short/yes_good_agree_say_about_all_blabla_10sec.wav')
print(time_list)
print(sum(time_list)/len(time_list))


time_list.clear()
for rec in range(0, 27):
    transcribe_file('/opt/scripts/whisper_example/scratches/long/text_to_voice_30sec.wav')
print(time_list)
print(sum(time_list)/len(time_list))


time_list.clear()
for rec in range(0, 27):
    transcribe_file('/opt/scripts/whisper_example/scratches/long/text_to_voice_60sec.wav')
print(time_list)
print(sum(time_list)/len(time_list))


time_list.clear()
for rec in range(0, 27):
    transcribe_file('/opt/scripts/whisper_example/scratches/long/fast_news_600sec.wav')
print(time_list)
print(sum(time_list)/len(time_list))

