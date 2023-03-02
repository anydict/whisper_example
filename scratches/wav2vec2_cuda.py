import datetime

from huggingsound import SpeechRecognitionModel

model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-russian", device='cuda:0')

audio_paths = ["/opt/scripts/whisper_example/scratches/short/music_yes_good_2sec.wav"]
print(datetime.datetime.now())
transcriptions = model.transcribe(audio_paths)
print(transcriptions)
print(datetime.datetime.now())

print('#####')

audio_paths = ["/opt/scripts/whisper_example/scratches/short/music_yes_good_music_3sec.wav"]
print(datetime.datetime.now())
transcriptions = model.transcribe(audio_paths)
print(transcriptions)
print(datetime.datetime.now())

print('#####')

audio_paths = ["/opt/scripts/whisper_example/scratches/short/music_yes_good_music_4sec.wav"]
print(datetime.datetime.now())
transcriptions = model.transcribe(audio_paths)
print(transcriptions)
print(datetime.datetime.now())

print('#####')

audio_paths = ["/opt/scripts/whisper_example/scratches/short/no_do_not_want_with_beep.mp3"]
print(datetime.datetime.now())
transcriptions = model.transcribe(audio_paths)
print(transcriptions)
print(datetime.datetime.now())
