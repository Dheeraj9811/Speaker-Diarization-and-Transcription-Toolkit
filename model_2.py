import whisper
import os

def fn_transcribe(model ,filepath ="audio.wav" , language = "en"):
    # check audio path exists and have audio file
    if not os.path.exists(filepath):
        return "Audio file not found"
    # print(dir(model))
    transcription = model.transcribe(filepath, language=language,verbose=True)
    return transcription

def load_model(modeltype = "base"):
    model = whisper.load_model(modeltype)
    return model
