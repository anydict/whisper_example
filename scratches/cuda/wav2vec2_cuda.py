import datetime
from huggingsound import SpeechRecognitionModel
path_sound = '/opt/scripts/whisper_example/scratches/'

# model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-russian", device='cuda:0')
model = SpeechRecognitionModel("emre/wav2vec2-xls-r-300m-Russian-small", device='cuda:0')

audio_paths = [f'{path_sound}short/music_yes_good_2sec.wav']
print(datetime.datetime.now())
transcriptions = model.transcribe(audio_paths)
print(transcriptions)
print(datetime.datetime.now())

print('#####')

audio_paths = [f'{path_sound}short/music_yes_good_music_3sec.wav']
print(datetime.datetime.now())
transcriptions = model.transcribe(audio_paths)
print(transcriptions)
print(datetime.datetime.now())

print('#####')

audio_paths = [f'{path_sound}short/music_yes_good_music_4sec.wav']
print(datetime.datetime.now())
transcriptions = model.transcribe(audio_paths)
print(transcriptions)
print(datetime.datetime.now())

print('#####')

audio_paths = [f'{path_sound}short/no_do_not_want_with_beep.mp3']
print(datetime.datetime.now())
transcriptions = model.transcribe(audio_paths)
print(transcriptions)
print(datetime.datetime.now())
