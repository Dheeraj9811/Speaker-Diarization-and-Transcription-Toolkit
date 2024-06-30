import whisper
import os

def fn_transcribe(model ,filepath ="audio.wav" ,audio = None, language = "en"):
    # check audio path exists and have audio file
    audio_patth = None
    video_path = None
    if(audio == True):
        audio_path = filepath
    elif(audio == False):
        video_path = filepath[1]
        audio_path = filepath[0]
    if not os.path.exists(audio_path):
        return "Audio file not found"
    # print(dir(model))
    
    transcription = model.transcribe(audio_path, language=language,verbose=True)
    return transcription

def load_model(modeltype = "base"):
    model = whisper.load_model(modeltype)
    return model
