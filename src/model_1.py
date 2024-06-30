from pyannote.audio import Pipeline
import torch
import torchaudio
from pyannote.audio.pipelines.utils.hook import ProgressHook
from pydub import AudioSegment
import os
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip, concatenate_videoclips
load_dotenv() #if running locally uncomment and use ur own key 
import streamlit as st

device = None

# load model
def load_model(modeltype = "base"):
    global device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # print(device , os.getenv("use_auth_token"))
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",use_auth_token=os.getenv("use_auth_token")) # running locally then use ur own key else comment this line
    pipeline = pipeline.to(device)
    return pipeline

# transcribe audio
def auidodiarization(model, path,audio):
    audio_patth = None
    video_path = None
    if(audio == True):
        audio_path = path
    elif(audio == False):
        video_path = path[1]
        audio_path = path[0]
    waveform, sample_rate = torchaudio.load(audio_path)
    dz = None
    with ProgressHook() as hook:
        dz = model({"waveform": waveform, "sample_rate": sample_rate}, hook=hook)


    with open("diarization.txt", "w") as text_file:
        text_file.write(str(dz))
    # Read the text file
    with open("diarization.txt", "r") as file:
        diarization_data = file.readlines()

    # Initialize a dictionary to store speaker timestamps
    speaker_timestamps = {}
    # Parse each line in the text file
    for line in diarization_data:
        # Extract speaker and timestamp information
        parts = line.split()
        # print(parts[1:4].split( '' ))
        temp1 = str(parts[1:2])
        temp2 = str(parts[3:4])
        # print((temp))
        temp3 = temp1.strip("[]'")
        temp4 = temp2.strip("[]'")
        speaker = parts[-1]

        timestamp = temp3 + " -> " + temp4
        # print(f"{speaker}: {timestamp}\n")
        # print("timestamp", timestamp)

        # Append the timestamp to the corresponding speaker in the dictionary
        if speaker not in speaker_timestamps:
            speaker_timestamps[speaker] = []
        speaker_timestamps[speaker].append(timestamp)
    # Write formatted speaker timestamps to a new file
    with open("final_diarization.txt", "w") as file:
        for speaker, timestamps in speaker_timestamps.items():
            file.write(f"{speaker}: {timestamps}\n")
    # Preparing audio files according to the diarization
            
    # Read the text file of final diarization
    file_path = "final_diarization.txt"
    speaker_data = {}
    with open(file_path, "r") as file:
        for line in file:
            speaker, time_ranges = line.strip().split(": ")
            time_ranges = [time_range.strip("[]").split(" -> ") for time_range in time_ranges.split(", ")]
            speaker_data[speaker] = time_ranges
    
    if(audio == True):
        input_audio_path = audio_path
        # Output folder for split audio files
        output_folder = "segmented_audio"
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        split_audio(input_audio_path, output_folder, speaker_data)
    elif(audio == False):
        input_audio_path = video_path
        output_folder = "segmented_audio"
        os.makedirs(output_folder, exist_ok=True)
        split_video(input_audio_path, output_folder, speaker_data)


        




# ----------------------------------------------------------------
#extra function #change to mili sec
def time_to_ms(timeStr):
  spl = timeStr.split(":")

  s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
  return s
def parse_time_strings(time_strings):
    start_time = time_strings[0].strip("'")
    end_time = time_strings[1].strip("'")
    return start_time, end_time
def time_to_sec(timeStr):
    spl = timeStr.split(":")
    return int(spl[0]) * 3600 + int(spl[1]) * 60 + float(spl[2])

# Function to split audio file
def split_audio(input_audio_path, output_folder, speaker_data):
    audio = AudioSegment.from_file(input_audio_path)

    for speaker, time_ranges in speaker_data.items():
        speaker_audio = AudioSegment.empty()

        for i, time_range in enumerate(time_ranges):
            start, end = parse_time_strings(time_range)
            start = time_to_ms(start)
            end = time_to_ms(end)
            segment = audio[start:end]

            speaker_audio += segment

        output_path = os.path.join(output_folder, f"{speaker}.wav")

        speaker_audio.export(output_path, format="wav")

def split_video(input_video_path, output_folder, speaker_data):
    video = VideoFileClip(input_video_path)
    
    for speaker, time_ranges in speaker_data.items():

        speaker_clips = []
        
        for i, time_range in enumerate(time_ranges):
            start_time, end_time = parse_time_strings(time_range)
            start = time_to_sec(start_time)
            end = time_to_sec(end_time)
            print("start time" + str(start_time) ,"end time" + str(end_time) , "duration of video" + str(video.duration))
            segment_clip = video.subclip(start, end)
            speaker_clips.append(segment_clip)
        final_video = concatenate_videoclips(speaker_clips)
        output_path = os.path.join(output_folder, f"{speaker}.mp4")
        final_video.write_videofile(output_path, codec="libx264", fps=video.fps)