# import streamlit as st

# # Function to check if the file extension is valid for videos
# def is_video_file(filename):
#     valid_extensions = ['.mp4', '.mkv', '.avi']
#     return any(filename.endswith(ext) for ext in valid_extensions)

# # Function to check if the file extension is valid for audio
# def is_audio_file(filename):
#     valid_extensions = ['.mp3', '.ogg', '.flac', '.wav']
#     return any(filename.endswith(ext) for ext in valid_extensions)

# # Main code
# # use markdown and write in bold making life easier
# st.markdown("#  Making Life Easier")

# # Title of the app in samll format

# st.markdown("### File Uploader")


import streamlit as st
import os
import shutil
from moviepy.editor import AudioFileClip
from pydub import AudioSegment
import time
import model_2
import model_1
from io import BytesIO
from moviepy.editor import VideoFileClip

# List of supported languages with their full names
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Mandarin Chinese": "zh",
    "Japanese": "ja",
    "Korean": "ko",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Arabic": "ar",
    "Dutch": "nl",
    "Turkish": "tr",
    "Hindi": "hi",
    "Bengali": "bn",
    "Urdu": "ur",
    "Vietnamese": "vi",
    "Thai": "th",
    "Greek": "el",
    "Swedish": "sv"
}

# extra common function 
def list_files(directory):
    files = os.listdir(directory)
    return [file for file in files if file.endswith(('.mp4', '.mkv', '.avi', '.mp3', '.ogg', '.flac', '.wav'))]

def is_video_file(filename):
    valid_extensions = ['.mp4', '.mkv', '.avi' ]
    return any(filename.endswith(ext) for ext in valid_extensions)

# Function to check if the file extension is valid for audio
def is_audio_file(filename):
    valid_extensions = ['.mp3', '.ogg', '.flac', '.wav']
    return any(filename.endswith(ext) for ext in valid_extensions)

def ms_to_time(ms):
    total_seconds = ms / 1000
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"

# function to format the translation
def format_translation(transcription):
    formatted_translation = ""
    for data in transcription['segments']:
        start_time = ms_to_time(data['start'])
        end_time = ms_to_time(data['end'])
        formatted_translation += f"{start_time} -> {end_time}: {data['text']}\n"
    
    return formatted_translation


def check(uploaded_file):
    

    if uploaded_file is not None:
        if is_video_file(uploaded_file.name):
            st.success("Video file uploaded successfully!")
            # extract audio from video
            
            try:

                audio_file_path = video_extract_audio(uploaded_file)
                return audio_file_path
            except Exception as e:
                st.warning("An error occurred while processing the video file.")
                st.warning("Please try uploading the file again.")
                st.warning(e)
            
            
        elif is_audio_file(uploaded_file.name):
            st.success("Audio file uploaded successfully!")
            # convert the file to wave
            try:
                
                audio_file_path = audio_convert_to_wav(uploaded_file)
                return audio_file_path
            except Exception as e:
                st.warning("An error occurred while processing the audio file.")
                st.warning("Please try uploading the file again.")
                st.warning(e)

            # Process the audio file
        else:
            st.warning("File format not supported. Please upload a valid video or audio file.")
            st.warning("Supported video formats: .mp4, .mkv, .avi")
            st.warning("Supported audio formats: .mp3, .ogg, .flac, .wav")

def audio_convert_to_wav(audio_file):
    if audio_file.name.lower().endswith('.wav'):
        with open(os.path.join("uploads", audio_file.name), "wb") as f:
            f.write(audio_file.getbuffer())
        return os.path.join("uploads", audio_file.name)
    else:
        audio = AudioSegment.from_file(audio_file)
        wav_path = os.path.join("uploads", os.path.splitext(audio_file.name)[0] + ".wav")
        audio.export(wav_path, format="wav")
        return wav_path
    
def video_extract_audio(video_file):
    # Extract audio from video file
    try:
        audio_path = os.path.join("uploads", os.path.splitext(video_file.name)[0] + ".wav")

    # Save the uploaded video file
        video_file_path = os.path.join("uploads", video_file.name)
        with open(video_file_path, "wb") as f:
            f.write(video_file.getbuffer())

        # Load the video file and extract audio
        video_clip = VideoFileClip(video_file_path)
        audio_clip = video_clip.audio

        # Write the audio file
        audio_clip.write_audiofile(audio_path)
        return audio_path
    except Exception as e:
        st.warning("An error occurred while extracting audio from the video file.")
        st.warning("Please try uploading the file again.")
        st.warning(e)


# Define function for home page
def home():
    st.title("Welcome to our App")
    st.write("This is the home page where you can find instructions and information about us.")
    # Add any additional content or instructions here

# Define function for segmenting audio
def segment_audio():
    st.title("Segment Audio by Speaker")
    st.write("This page allows you to segment audio files according to different speakers.")
    # make varibale flag and store it value inside cache and if avaliale in cache then take it from there else make it none 
    if 'available' not in st.session_state: 
        st.session_state["available"] = True
    
    if(st.session_state.available == False):
        # if "segmented_audio" folder exists delete it
        # if os.path.exists("segmented_audio"):
        #     shutil.rmtree("segmented_audio")
        #     print("deleted segmented_audio folder")

        # # if "final_diarization.txt" file exists delete it
        # if os.path.exists("final_diarization.txt"):
        #     os.remove("final_diarization.txt")
        #     print("deleted final_diarization.txt file")
        # # if "uploads" folder exists delete it
        # if os.path.exists("uploads"):
        #     shutil.rmtree("uploads")
        #     print("deleted uploads folder")
        # #  if "diarization" file exists delete it
        # if os.path.exists("diarization"):
        #     os.remove("diarization")
        #     print("deleted diarization file")
        
        uploaded_file = st.file_uploader("Upload a video or audio file", type=['mp4', 'mkv', 'avi', 'mp3', 'ogg', 'flac', 'wav'])
        
        file = check(uploaded_file)

        # if file is not none load the model_1 file
        if file is not None:
            if st.button("Segment Audio"):
                with st.spinner("Segmenting audio..."):  # Show spinner while loading
                    # Load the model
                    model = model_1.load_model()
                    # Segment the audio file
                    st.write("Audio segmented successfully!")
                    # Now processing the file in background
                    if(model is not None):
                        st.write("Processing the file in the background...")
                    # Process the audio file
                        model_1.auidodiarization(model, file)
                        st.write("Audio segmented successfully!")
                        st.session_state["available"] = True
                        st.button("Go to next page...")
                                                
                    else:
                        st.write("Model not loaded successfully! Please try again")
                selected_file = st.selectbox("Select a file:", list_files("segmented_audio")) 

    elif st.session_state.available == True:

        st.title("Audio and Video Player with Download Option")
        selected_file = st.selectbox("Select a file:", list_files("segmented_audio"))
        if selected_file.endswith(('.mp3', '.ogg', '.flac', '.wav')):
            audio_file = open(os.path.join("segmented_audio", selected_file), 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')
            st.download_button(
            label="Download File",
            data=open(os.path.join("segmented_audio", selected_file), 'rb').read(),
            file_name=selected_file)

        elif selected_file.endswith(('.mp4', '.mkv', '.avi')):
            video_file = open(os.path.join("segmented_audio", selected_file), 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes) 
            st.download_button(
            label="Download File",
            data=open(os.path.join("segmented_audio", selected_file), 'rb').read(),
            file_name=selected_file )
        
        st.button("Go to prev page")
        # st.session_state["available"] = False
        # delete  the "segmented_audio" folder with all the file in it
        

        
        
    

# Define function for speech to text translation
    
model = None
transcription = None

def speech_to_text():
    st.title("Speech to Text Transcription")
    languages_reverse = {v: k for k, v in languages.items()}
    st.write("This page enables you to Transcription of auido and video.")

    modeltype = st.selectbox("Select Model Type", ["tiny", "base","small"])
    selected_language_code = st.selectbox("Select a language", list(languages.values()), format_func=lambda x: languages_reverse[x])
    
    uploaded_file = st.file_uploader("Upload a video or audio file", type=['mp4', 'mkv', 'avi', 'mp3', 'ogg', 'flac', 'wav'])

    file = check(uploaded_file)
    # make global varibale 
    global model
    global transcription

    if file is not None:
        if st.button("Load Model and Translation"):
            with st.spinner("Loading model..."):  # Show spinner while loading
                
                model = model_2.load_model(modeltype)
                st.write("Model loaded successfully!")
                print(selected_language_code)
                transcription = model_2.fn_transcribe(model, file, selected_language_code)
                 
                # data = format_translation(transcription)
                st.write("Transcription completed!")

                if transcription is not None:
                    # give dowload option
                    st.markdown(f"# Translation")
                    # st.markdown(f"### Download")
                    # st.title("Download Text File Example")
                    st.write("Click the button below to download the text file.")

                    download_text_file(transcription['text'])

                    st.markdown(transcription['text'])


# speecj to text download function  
def download_text_file(data, filename='downloaded_data.txt'):
    # Create a BytesIO object
    buffer = BytesIO()
    # Write the string data to the buffer
    buffer.write(data.encode())
    # Set the cursor to the beginning of the buffer
    buffer.seek(0)
    # Return the buffer for download
    st.download_button(
        label="Download Text File",
        data=buffer,
        file_name=filename,
        mime="text/plain"
    )

    
    
            
# -------------------------------------------------------------------------------------------------------------------------
# Main function to handle page navigation
def main():
    st.sidebar.title("Pages navigation")
    page = st.sidebar.radio("Choose", ["Home", "Segment Audio", "Speech to Text"])

    if page == "Home":
        home()
    elif page == "Segment Audio":
        # here using cache to load the audio file directly if available in segment audio folder 
        segment_audio()
    elif page == "Speech to Text":
        speech_to_text()

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    main()
