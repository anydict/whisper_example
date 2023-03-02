import numpy as np
import whisper


class BaseModel:
    def __init__(self, model_id: int, name: str = 'tiny', language: str = 'ru'):
        self._model_id = model_id
        self._name = name
        self._language = language
        self._model = None
        self._load_model_in_memory()

    def _load_model_in_memory(self):
        self._model = whisper.load_model(self._name)

    def file_transcribe(self, filepath: str):
        transcription = self._model.transcribe(filepath)

        return transcription

    def ndarray_transcribe(self, buffer: np.ndarray):
        transcription = self._model.transcribe(buffer)

        return transcription
