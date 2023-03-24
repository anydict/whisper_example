import os
import time
import concurrent.futures as pool


path_sound = '/opt/scripts/whisper_example/scratches/stress_test/sounds/16khz5second'
path_convert = '/opt/scripts/whisper_example/scratches/stress_test/convert_wav'
files = []
MAX_INSTANCE = 1
for i in range(0, 1000):
    files.append([f'{path_sound}/{i%10}.wav', f'{path_convert}/{i}.wav'])


def convert(filepaths):
    source_file = filepaths[0]
    output_file = filepaths[1]

    # cmd_str = f"yes | ffmpeg -i {source_file} -acodec pcm_s16le -ac 1 -ar 16000 {output_file}"
    cmd_str = f'sox {source_file} -r 16000 -c 1 -b 16 {output_file}'
    print(cmd_str)
    os.system(cmd_str)


print('start')
try:
    start_time = time.time()
    with pool.ThreadPoolExecutor(max_workers=MAX_INSTANCE) as executor:
        res = executor.map(convert, files)
    print(f"full_time={(time.time() - start_time)}")
    # full_time=2.3565127849578857
except Exception as e:
    print(e)
