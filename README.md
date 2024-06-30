# VoiceVerse- Redifining Audio Content {Speaker Diarization and Transcription Toolkit}

VoiceVerse Toolkit is a Streamlit-based application that enables users to perform speaker diarization, divide audio and video into different speaker segments, listen to individual speakers, and generate speaker transcriptions using the Pyannote.audio and Whisper models.

## Getting Started

To get started with the project, follow these steps:

### Prerequisites
    
    #install streamlit
    pip install streamlit


# install pytorch

-  

#Project file
```bash
-   pip install torch torchvision torchaudio
-   apt update && apt install ffmpeg -y
-   pip install setuptools-rust && \
-   python3 -m pip install moviepy && \
-   python3 -m pip install pydub && \
-   python3 -m pip install -U openai-whisper && \
-   python3 -m pip install pyannote.audio && \
-   python3 -m pip install python-dotenv && \
-   python3 -m pip install streamlit-extras

#install pytorch
pip3 install torch torchvision torchaudio

#Project file
RUN apt update && apt install ffmpeg -y
RUN pip install setuptools-rust && \
	python3 -m pip install moviepy && \
	python3 -m pip install pydub && \
	python3 -m pip install -U openai-whisper && \
	python3 -m pip install pyannote.audio && \
	python3 -m pip install python-dotenv && \
	python3 -m pip install streamlit-extras
```
### Installation

1. Clone this repository to your local machine:
    git clone <https://github.com/Dheeraj9811/Speaker-Diarization-and-Transcription-Toolkit>

2. Navigate to the project directory: Speaker-Diarization-and-Transcription-Toolkit/src


### Running the Application

To run the application, execute the following command:
--- streamlit run main.py --server.maxUploadSize 2000
<!-- images of project -->
<img src="/img/projectimg1.png" alt="cmd">
<img src="/img/projectimg2.png" alt="homepage">
<img src="/img/projectimg3.png" alt="Diarization page" width="500" height="300">
<img src="/img/projectimg4.png" alt="project image" width="500" height="300">
<img src="/img/projectimg5.png" alt="mobile view">




# Dockerversion also available 
 **Note Docker is made to use gpu so if you dont have gpu install on system comment line 16 to 29**
- git clone git clone https://github.com/Dheeraj9811/Speaker-Diarization-and-Transcription-Toolkit
- cd Speaker-Diarization-and-Transcription-Toolkit
- docker build -t toolkit .
- docker run -it --name mytoolkit \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --env="XAUTHORITY=$XAUTH" \
    --net=host \
    --privileged \
    --runtime=nvidia \
    --gpus all \
    toolkit




## Usage

Once the application is running, open your web browser and navigate to the URL provided by Streamlit (usually `localhost:8501`). You will see the Speaker Diarization and Transcription Toolkit interface, where you can upload audio or video files, perform speaker diarization, listen to individual speakers, and generate speaker transcriptions.

## Contributing

Contributions are welcome! If you have any ideas for improvements, features you'd like to see, or bug fixes, feel free to open an issue or submit a pull request.

## License



## Acknowledgments

- Pyannote.audio: A toolkit for speaker diarization.
- Whisper models: State-of-the-art models for speaker diarization and transcription.

