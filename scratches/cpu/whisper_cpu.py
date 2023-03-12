import time
import whisper
import warnings
warnings.filterwarnings("ignore")  # ignore transcribe warning CUDA available
path_sound = '/opt/scripts/whisper_example/scratches/'


def transcribe_file(name: str, language: str):
    cpu_time_start = time.process_time()
    real_time_start = time.time()
    decode_options = dict(language=language, fp16=False)
    transcribe_options = dict(task="transcribe", **decode_options)
    transcription = model.transcribe(name, **transcribe_options)

    print(transcription["text"])
    print(f"real_time={(time.time() - real_time_start)} for {name}")
    print(f'process_time={(time.process_time() - cpu_time_start)} for {name}\n')


model = whisper.load_model("tiny", device='cpu')
transcribe_file(f'{path_sound}long/example_1.wav', "ru")
transcribe_file(f'{path_sound}long/example_1.mp3', "ru")
transcribe_file(f'{path_sound}long/example_2.wav', "ru")
transcribe_file(f'{path_sound}long/example_2.mp3', "ru")

transcribe_file(f'{path_sound}short/no_do_not_want_with_silence.mp3', "ru")
transcribe_file(f'{path_sound}short/no_do_not_want_without_silence.mp3', "ru")
transcribe_file(f'{path_sound}short/no_do_not_want_with_noise.mp3', "ru")
transcribe_file(f'{path_sound}short/no_do_not_want_with_beep.mp3', "ru")
transcribe_file(f'{path_sound}short/no_do_not_want_with_music.mp3', "ru")
transcribe_file(f'{path_sound}short/yes_good.mp3', "ru")
