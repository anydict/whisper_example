import concurrent.futures as pool
import time
import whisper

mm = []
for rec in range(0, 25):
    mm.append(whisper.load_model("tiny", device='cuda'))


def transcribe_file(name: str, num: int):
    try:
        print(num)
        # model = whisper.load_model("tiny", device='cuda')  # load for every thread
        model = mm[num % 30]
        cpu_time_start = time.process_time()
        real_time_start = time.time()
        decode_options = dict(language="ru", fp16=True)
        transcribe_options = dict(task="transcribe", **decode_options)
        transcription = model.transcribe(name, **transcribe_options)

        print(transcription["text"])
        print(transcription)
        print(f"real_time={(time.time() - real_time_start)} for {name}")
        print(f'process_time={(time.process_time() - cpu_time_start)} for {name}\n')
    except Exception as e:
        print(e)


# first call for load gpu
transcribe_file('long/example_1.mp3', 0)
#
# # second call for compare
# transcribe_file('long/example_1.mp3')

data = []
nn = []
for rec in range(0, 1000):
    data.append('long/example_1.mp3')
    nn.append(rec)


try:
    with pool.ThreadPoolExecutor(max_workers=25) as executor:
        res = executor.map(transcribe_file, data, nn)
except Exception as e:
    print(e)

