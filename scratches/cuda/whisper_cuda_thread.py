import threading
import time
import whisper
path_sound = '/opt/scripts/whisper_example/scratches/'


def transcribe_file(name: str, language: str):
    model = whisper.load_model("tiny", device='cuda')  # load for every thread
    cpu_time_start = time.process_time()
    real_time_start = time.time()
    decode_options = dict(language=language, fp16=True)
    transcribe_options = dict(task="transcribe", **decode_options)
    transcription = model.transcribe(name, **transcribe_options)

    print(transcription["text"])
    print(f"real_time={(time.time() - real_time_start)} for {name}")
    print(f'process_time={(time.process_time() - cpu_time_start)} for {name}\n')


# first call for load cpu
transcribe_file(f'{path_sound}long/example_1.mp3', "ru")

# second call for compare
transcribe_file(f'{path_sound}long/example_1.mp3', "ru")

t1 = threading.Thread(target=transcribe_file, args=(f'{path_sound}long/example_1.mp3', "ru"))
t1.start()

t2 = threading.Thread(target=transcribe_file, args=(f'{path_sound}long/example_1.mp3', "ru"))
t2.start()

t3 = threading.Thread(target=transcribe_file, args=(f'{path_sound}long/example_1.mp3', "ru"))
t3.start()
