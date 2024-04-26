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
from streamlit_extras.mention import mention
import streamlit.components.v1 as components


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
                return [audio_file_path, False]
            except Exception as e:
                st.warning("An error occurred while processing the video file.")
                st.warning("Please try uploading the file again.")
                st.warning(e)
            
            
        elif is_audio_file(uploaded_file.name):
            st.success("Audio file uploaded successfully!")
            # convert the file to wave
            try:
                
                audio_file_path = audio_convert_to_wav(uploaded_file)
                return [audio_file_path, True]
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
        return [audio_path,video_file_path]
    except Exception as e:
        st.warning("An error occurred while extracting audio from the video file.")
        st.warning("Please try uploading the file again.")
        st.warning(e)


# Define function for home page
def home():
    st.title("VoiceVerse 🗣️")
    st.header("Welcome to VoiceVerse!!")
    st.text("Unlock Clarity, Embrace Precision")
    my_expander1 = st.expander("**What is VoiceVerse?**")
    my_expander1.write("VoiceVerse is a reliable, secure and innovative platform revolutionizing the way we interact with audio and video content. With cutting-edge technology, VoiceVerse offers advanced features like audio/video diarisation, allowing users to effortlessly organize and navigate through their recordings. Additionally, our text-to-speech functionality breaks language barriers by providing accurate subtitles in multiple languages. Whether you're a seasoned user or new to the scene, VoiceVerse empowers everyone to engage with audio and video content seamlessly")
    my_expander2 = st.expander("**What is Segment Audio and How does it work**")
    my_expander2.write('''Using cutting-edge algorithms, VoiceVerse automatically divides the audio or video into separate segments corresponding to different speakers, making it easier to analyze and transcribe.\n 
**How does it work:**
1. Upload your audio or video file to VoiceVerse.
2. VoiceVerse utilizes advanced speaker diarization algorithms to analyze the recording.
3. Individual speakers within the recording are identified and isolated using these algorithms.
4. Each segment corresponding to a different speaker is assigned a unique identifier.
5. This unique identifier allows users to easily differentiate between speakers and analyze their respective segments.
6. You can download the audio or video of the specific speaker that you want to use''')
    my_expander3 = st.expander("**Whaat is Speech to Text and how does it work**")
    my_expander3.write('''With VoiceVerse's text-to-speech feature, you can effortlessly generate subtitles for your audio and video content.\n
**How does it work:**
1. Upload your audio or video file to VoiceVerse.
2. Choose from our range of text-to-speech models—tiny, base, or small—each offering a different balance between speed and accuracy. Additionally, select the target language for your subtitles. VoiceVerse supports multiple languages, allowing you to create subtitles in any language, regardless of the original audio content's language.
3. VoiceVerse will generate subtitles for your audio or video content in the specified language.''')


    # Add any additional content or instructions here

# Define function for segmenting audio
def segment_audio():
    st.title("Segment Audio by Speaker")
    st.subheader("You can segment audio & video files speakerwise here.")
    # make varibale flag and store it value inside cache and if avaliale in cache then take it from there else make it none 
    if 'available' not in st.session_state: 
        st.session_state["available"] = False
    
    if(st.session_state.available == False):
        
        
        uploaded_file = st.file_uploader("Upload a video or audio file", type=['mp4', 'mkv', 'avi', 'mp3', 'ogg', 'flac', 'wav'])
        
        file = check(uploaded_file)

        # if file is not none load the model_1 file
        if file is not None:
            if os.path.exists("segmented_audio"):
                shutil.rmtree("segmented_audio")
                print("deleted segmented_audio folder")
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
                        model_1.auidodiarization(model, file[0], file[1])
                        st.write("Audio segmented successfully!")
                        st.session_state["available"] = True
                        st.button("Go to next page...")
                                                
                    else:
                        st.write("Model not loaded successfully! Please try again")
                # selected_file = st.selectbox("Select a file:", list_files("segmented_audio")) 

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
            # if st.button("Go to previous Page"):
            #     st.session_state.availabl = False
            # 
                
                

        elif selected_file.endswith(('.mp4', '.mkv', '.avi')):
            video_file = open(os.path.join("segmented_audio", selected_file), 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes) 
            st.download_button(
            label="Download File",
            data=open(os.path.join("segmented_audio", selected_file), 'rb').read(),
            file_name=selected_file )
        
   
                
        
        
        

        
        
    

# Define function for speech to text translation
    
model = None
transcription = None

def speech_to_text():
    st.title("Speech to Text Transcription")
    languages_reverse = {v: k for k, v in languages.items()}
    st.subheader("You can Transcribe audio & video here.")
    st.write('''We have 3 different models that you can choose from:
1. Tiny - Fastest but Low Accuracy
2. Base - Balanced between Speed and Accuracy
3. Small - Slowest but High Accuracy''')

    modeltype = st.selectbox("Select Model Type", ["Tiny", "Base","Small"])
    modeltype = modeltype.lower()
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
                transcription = model_2.fn_transcribe(model, file[0],file[1], selected_language_code)
                 
                # data = format_translation(transcription)
                st.write("Transcription completed!")
                srt_entries = [
                    f"{index}\n{ms_to_time(dic['start'])} --> {ms_to_time(dic['end'])}\n{dic['text']}\n\n"
                    for index, dic in enumerate(transcription['segments'], start=1)
                ]

                # Join the segment information strings with newline characters
                result_string = "\n".join(srt_entries)

                # Now, result_string contains all the information concatenated together
                # print(result_string)


                if transcription is not None:
                    # give dowload option
                    st.markdown(f"# Translation")
                    # st.markdown(f"### Download")
                    # st.title("Download Text File Example")
                    st.write("Click the button below to download the text file.")

                    download_text_file(transcription['text'])
                    download_text_file_withtime(result_string)

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
        label="Download Transcript File",
        data=buffer,
        file_name=filename,
        mime="text/plain"
    )
def download_text_file_withtime(data, filename='transcript_with_time.srt'):
    # Create a BytesIO object
    buffer = BytesIO()
    # Write the string data to the buffer
    buffer.write(data.encode())
    # Set the cursor to the beginning of the buffer
    buffer.seek(0)
    # Return the buffer for download
    st.download_button(
        label="Download Transcript in SRT Format",
        data=buffer,
        file_name=filename,
        mime="text/plain"
    )

    
def Creators():
    tab1, tab2, tab3, tab4 = st.tabs(["Dheeraj", "Kartik Jain", "Ritwick Pal", "Rohit Kumar"])
    with tab1:
        st.header("Dheeraj Kumar")
        st.write("Hello! I'm Dheeraj, I'm an engineering enthusiast currently based in New Delhi. My expertise lies in the realms of Machine Learning and Deep Learning. While honing these skills, I've also ventured into the dynamic field of web development. Let's connect and explore the possibilities in the tech world!")
        st.write("Socials:")
        mention(label="Github", icon="github", url="https://github.com/Dheeraj9811/")
        mention(label="Linkedin", icon="🔗", url="https://www.linkedin.com/in/dheeraj-deshwal/")
        st.write("Dheeraj20194@iiitd.ac.in")

    with tab2:
        st.header("Kartik Jain")
        st.write("I am a 4-year Computer Science and Social Science Undergraduate at IIIT Delhi. I am an academically goal-driven individual who has strong problem-solving skills. I am open to new experiences and opportunities.")
        st.write("Socials:")
        mention(label="Github", icon="github", url="https://github.com/Kartik20440")
        mention(label="Linkedin", icon="🔗", url="https://www.linkedin.com/in/kartikxjain/")
        st.write("kartik20440@iiitd.ac.in")

    with tab3:
        st.header("Ritwick Pal")
        st.write("As a passionate 4th year Computer Science student, I love exploring the fascinating worlds of data structures and algorithms, mathematics, and cognitive science. I find it thrilling to dive deep into complex concepts and uncover their practical applications, always striving to learn and grow as a problem-solver.")
        st.write("Socials:")
        mention(label="Github", icon="github", url="https://github.com/Ritwick01")
        mention(label="Linkedin", icon="🔗", url="https://www.linkedin.com/in/ritwickpal/")
        st.write("rishabh20459@iiitd.ac.in")

    with tab4:
        st.header("Rohit")
        st.write("As a Senior at IIIT Delhi, I have a strong interest in data structures and algorithms, and I am passionate about solving real-world problems through programming. I have completed several projects where I have applied my skills in software development.")
        st.write("Socials:")
        mention(label="Github", icon="github", url="https://github.com/rohit21755")
        mention(label="Linkedin", icon="🔗", url="https://www.linkedin.com/in/rohit-kumar-534919201/")
        st.write("Rohit@iiitd.ac.in")
    
def show_privacy_policy_popup():
    privacy_policy_text = """
    <script>
        alert("User Agreement & Privacy Policy\\n\\n1. By using our service, you grant consent for the utilization of your audio and video recordings exclusively for diarization and captioning.\\n2. Your audio and video data will be used solely for intended purposes, with adherence to stringent privacy standards.\\n3. We uphold a strict policy of non-retention for your input files. Your data is promptly deleted upon closure of our website, ensuring your privacy and data security.");
    </script>
    """
    # alert("User Permissions and Data Privacy\\n\\n6. Opt-In/Opt-Out Mechanism: We respect your preferences. You have the liberty to opt in or opt out of various data processing activities, ensuring full control over your data.\\n7. Cookie Policy: Our cookie policy is transparent, informing you about cookie usage and providing options to manage your preferences regarding tracking technologies.\\n8. GDPR and Privacy Regulations Compliance: We are fully committed to compliance with GDPR and other relevant privacy regulations, ensuring the protection of your data rights and privacy.\\n9. Children's Privacy: Compliance with regulations concerning data collection from children is paramount. We adhere to all applicable laws and obtain necessary parental consent where required.\\n10. Terms of Service and Privacy Policy: Please refer to our comprehensive Terms of Service and Privacy Policy documents for detailed information on your rights, responsibilities, and our commitment to data privacy.");

    components.html(privacy_policy_text, height=100, width=100)


# function to change size of widget
def ChangeWidgetFontSize(wgt_txt, wch_font_size = '12px'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                    for (i = 0; i < elements.length; ++i) { if (elements[i].innerText == |wgt_txt|) 
                        { elements[i].style.fontSize='""" + wch_font_size + """';} } </script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)





# -------------------------------------------------------------------------------------------------------------------------
# Main function to handle page navigation
def main():
    st.set_page_config(page_title="VoiceVerse", page_icon="🗣️", layout="centered", initial_sidebar_state="expanded")

    if 'showarning' not in st.session_state: 
        st.session_state["showarning"] = False

    
                         
    st.sidebar.title("VoiceVerse 🗣️ ")
    page = st.sidebar.radio(" ", ("Home", "Segment Audio", "Speech to Text","Creators"))
    ChangeWidgetFontSize(page,'25px')
    st.sidebar.subheader("Feedback Form:")
    st.sidebar.image("QR.png", use_column_width=True)

    st.markdown(""" <style>
    #MainMenu {visibility: hidden;}
	footer {visibility: hidden;}
	</style> """, unsafe_allow_html=True)

    if st.session_state['showarning'] == False:
        st.session_state["showarning"] = True
        show_privacy_policy_popup()

    if page == "Home":
        home()
    elif page == "Segment Audio":
        segment_audio()
    elif page == "Speech to Text":
        speech_to_text()

    elif page == "Creators":
        Creators()


if __name__ == "__main__":
    # "uploads" exist then delete the folder with content
    if os.path.exists("uploads"):
        shutil.rmtree("uploads")    
        print("deleted uploads folder")


    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    main()
