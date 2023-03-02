import datetime
import json
import concurrent.futures as pool

from core.CpuModel import CpuModel
from core.CudaModel import CudaModel


def run_analyze(cm):
    try:
        res = cm.file_transcribe('/opt/scripts/whisper_example/scratches/short/yes_good.mp3')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    with open('config.json') as config_file:
        data = json.load(config_file)

    width = data['width']
    height = data['height']

    data = [CudaModel(model_id=idx) for idx in range(0, 22)]

    # run_analyze(1)
    try:
        print(datetime.datetime.now())
        with pool.ThreadPoolExecutor(max_workers=25) as executor:
            executor.map(run_analyze, data)
        print(datetime.datetime.now())
    except Exception as e:
        print(e)

# 2023-03-02 01:27:57.551309
# 2023-03-02 01:29:11.599411
# 286 == 74 sec
# 286 == 13 sec

# 2023-03-02 01:31:38.887952
# 2023-03-02 01:31:51.224226


# 2023-03-02 01:42:05.440880
# 2023-03-02 01:42:18.055162
# 285 == 13 sec


# склеивать в один большой файл с промежутками с тишиной и анализировать
