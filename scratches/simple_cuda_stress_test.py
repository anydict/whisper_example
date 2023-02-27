import concurrent.futures as pool
import time
import whisper


def transcribe_file(name: str):
    model = whisper.load_model("tiny", device='cuda')  # load for every thread
    cpu_time_start = time.process_time()
    real_time_start = time.time()
    decode_options = dict(language="ru", fp16=True)
    transcribe_options = dict(task="transcribe", **decode_options)
    transcription = model.transcribe(name, **transcribe_options)

    print(transcription["text"])
    print(f"real_time={(time.time() - real_time_start)} for {name}")
    print(f'process_time={(time.process_time() - cpu_time_start)} for {name}\n')


# first call for load gpu
transcribe_file('long/example_1.mp3')

# second call for compare
transcribe_file('long/example_1.mp3')

data = []
for rec in range(0, 200):
    data.append('long/example_1.mp3')

try:
    with pool.ThreadPoolExecutor(max_workers=20) as executor:
        res = executor.map(transcribe_file, data)
except Exception as e:
    print(e)

