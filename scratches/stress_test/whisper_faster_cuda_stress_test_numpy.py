import concurrent.futures as pool
import threading
import time
import numpy as np
import ffmpeg
from faster_whisper import WhisperModel

path_sound = '/opt/scripts/whisper_example/scratches/stress_test/sounds/5second'
MAX_INSTANCE = 5


def exact_div(x, y):
    assert x % y == 0
    return x // y


# hard-coded audio
SAMPLE_RATE = 16000
N_FFT = 400
HOP_LENGTH = 160
CHUNK_LENGTH = 30
N_SAMPLES = CHUNK_LENGTH * SAMPLE_RATE  # 480000: number of samples in a chunk
N_FRAMES = exact_div(N_SAMPLES, HOP_LENGTH)  # 3000: number of frames in a mel spectrogram input


def load_audio(file: str, sr: int = SAMPLE_RATE):
    """
    Open an audio file and read as mono waveform, resampling as necessary

    Parameters
    ----------
    file: str
        The audio file to open

    sr: int
        The sample rate to resample the audio if necessary

    Returns
    -------
    A NumPy array containing the audio waveform, in float32 dtype.
    """
    try:
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input(file, threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
            .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as exp:
        raise RuntimeError(f"Failed to load audio: {exp.stderr.decode()}") from exp

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


names = []

for i in range(0, 1000):
    filename = i % 10
    filepath = f'{path_sound}/{filename}.wav'
    np_file = load_audio(filepath)
    names.append(np_file)


def transcribe_file(model):
    th_name = threading.current_thread().name
    while len(names) > 0:
        numpy_file = names.pop()
        print(f'run th_name={th_name}')
        try:
            decode_options = dict(language='ru', beam_size=1)
            transcribe_options = dict(task="transcribe", **decode_options)
            segments, info = model.transcribe(numpy_file, **transcribe_options)

            text = ''
            for segment in segments:
                text = text + ' ' + segment.text

            print(f'end th_name={th_name} and text={text}')
        except Exception as exp:
            print(exp)


models = []
for rec in range(0, MAX_INSTANCE):
    print(rec)
    model_path = "/opt/scripts/whisper_example/whisper-tiny-float16/"
    gpu_model = WhisperModel(model_path, device="cuda", compute_type="float16")
    models.append(gpu_model)
    # WARMUP
    warmup_decode_options = dict(language='ru', beam_size=1)
    warmup_transcribe_options = dict(task="transcribe", **warmup_decode_options)
    warmup_segments, warmup_info = gpu_model.transcribe(f'{path_sound}/0.wav', **warmup_transcribe_options)

try:
    start_time = time.time()
    with pool.ThreadPoolExecutor(max_workers=MAX_INSTANCE) as executor:
        res = executor.map(transcribe_file, models)
    print(f"full_time={(time.time() - start_time)}")
except Exception as e:
    print(e)
