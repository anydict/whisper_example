import time
import whisper
import warnings
warnings.filterwarnings("ignore")  # ignore transcribe warning CUDA available


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
transcribe_file('long/example_1.wav', "ru")
transcribe_file('long/example_1.mp3', "ru")
transcribe_file('long/example_2.wav', "ru")
transcribe_file('long/example_2.mp3', "ru")

transcribe_file('short/no_do_not_want_with_silence.mp3', "ru")
transcribe_file('short/no_do_not_want_without_silence.mp3', "ru")
transcribe_file('short/no_do_not_want_with_noise.mp3', "ru")
transcribe_file('short/no_do_not_want_with_beep.mp3', "ru")
transcribe_file('short/yes_good.mp3', "ru")
