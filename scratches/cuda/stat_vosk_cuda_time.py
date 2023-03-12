import json
from time import time, process_time
import asyncio
import websockets
import wave

real_time = []
cpu_time = []
path_sound = '/opt/scripts/whisper_example/scratches/'


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
    async def run_test(uri):
        text = ""
        async with websockets.connect(uri) as websocket:
            wf = wave.open(name, "rb")
            await websocket.send('{ "config" : { "sample_rate" : %d } }' % (wf.getframerate()))
            buffer_size = 64000  # 0.4 seconds of audio, don't make it too small otherwise compute will be slow
            while True:
                data = wf.readframes(buffer_size)

                if len(data) == 0:
                    break

                await websocket.send(data)
                response = json.loads(await websocket.recv())
                text += response.get('text', '')

            await websocket.send('{"eof" : 1}')
            response = json.loads(await websocket.recv())
            text += response.get('text', '')
            print(text)

    asyncio.run(run_test('ws://localhost:2700'))


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
