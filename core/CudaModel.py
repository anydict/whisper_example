import numpy as np
import whisper

from core.BaseModel import BaseModel


class CudaModel(BaseModel):
    def _load_model_in_memory(self):
        self._model = whisper.load_model(self._name, device='cuda')

    def file_transcribe(self, filepath: str):
        # decode_options = dict(language=self._language, condition_on_previous_text=False)
        decode_options = dict(language=self._language, condition_on_previous_text=True)
        transcribe_options = dict(task="transcribe", **decode_options)
        transcription = self._model.transcribe(filepath, **transcribe_options)
        print(transcription)
        transcription = self._model.transcribe(filepath, **transcribe_options)
        print(transcription)
        transcription = self._model.transcribe(filepath, **transcribe_options)
        print(transcription)
        transcription = self._model.transcribe(filepath, **transcribe_options)
        print(transcription)
        transcription = self._model.transcribe(filepath, **transcribe_options)
        print(transcription)
        transcription = self._model.transcribe(filepath, **transcribe_options)
        print(transcription)

        return transcription

    def ndarray_transcribe(self, buffer: np.ndarray):
        transcription = self._model.transcribe(buffer)

        return transcription
