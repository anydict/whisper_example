import concurrent.futures as pool
import threading
import time
import json
import asyncio
import wave
import websockets
path_sound = '/opt/scripts/whisper_example/scratches/stress_test/sounds/5second'
MAX_INSTANCE = 4  # for small
# MAX_INSTANCE = 2  # for 0.22
# MAX_INSTANCE = 1  # for 0.44
names = list(range(0, 1000))


def transcribe_file(model):
    async def run_test(uri):

        while len(names) > 0:
            th_name = threading.current_thread().name
            filename = names.pop() % 10
            filepath = f'{path_sound}/{filename}.wav'
            print(f'run th_name={th_name} with filepath={filepath} model={model}')

            text = ""
            async with websockets.connect(uri) as websocket:
                wf = wave.open(filepath, "rb")
                await websocket.send('{ "config" : { "sample_rate" : %d } }' % (wf.getframerate()))
                buffer_size = 64000  # 0.4 seconds of audio, don't make it too small otherwise compute will be slow
                while True:
                    data = wf.readframes(buffer_size)

                    if len(data) == 0:
                        break

                    await websocket.send(data)
                    response = json.loads(await websocket.recv())
                    text += response.get('text', '')

                wf.close()

                await websocket.send('{"eof" : 1}')
                response = json.loads(await websocket.recv())
                text += response.get('text', '')
                print(text)

    return asyncio.run(run_test('ws://localhost:2700'))


models = []
for rec in range(0, MAX_INSTANCE):
    print(rec)
    models.append('')


try:
    start_time = time.time()
    with pool.ThreadPoolExecutor(max_workers=MAX_INSTANCE) as executor:
        res = executor.map(transcribe_file, models)
    print(f"full_time={(time.time() - start_time)}")
except Exception as e:
    print(e)
