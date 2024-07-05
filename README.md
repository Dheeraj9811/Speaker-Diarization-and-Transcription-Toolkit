# VoiceVerse- Redefining Audio Content {Speaker Diarization and Transcription Toolkit}

VoiceVerse Toolkit is a Streamlit-based application that enables users to perform speaker diarization, divide audio and video into different speaker segments, listen to individual speakers, and generate speaker transcriptions using the Pyannote.audio and Whisper models.

## Getting Started

The project has been developed and tested on Ubuntu 20.04 and Windows (Note: For Windows, ffmpeg needs to be installed separately from the internet). Alternatively, you can use the provided Dockerfile. Feel free to modify the Dockerfile as needed. If not using GPU, you can opt for a lighter image version like Python 3.8 without CUDA and Ubuntu full version.

To begin with the project, follow these steps:




### Prerequisites
```bash
#install streamlit
-   pip install streamlit
-   pip install torch torchvision torchaudio
-   apt update && apt install ffmpeg -y
-   pip install setuptools-rust && \
-   python3 -m pip install moviepy && \
-   python3 -m pip install pydub && \
-   python3 -m pip install -U openai-whisper && \
-   python3 -m pip install pyannote.audio && \
-   python3 -m pip install python-dotenv && \
-   python3 -m pip install streamlit-extras

```
### Installation

1. Clone this repository to your local machine:
    git clone <https://github.com/Dheeraj9811/Speaker-Diarization-and-Transcription-Toolkit>

2. Navigate to the project directory: Speaker-Diarization-and-Transcription-Toolkit/src


### Running the Application

# To run the application, execute the following command:
```bash 
streamlit run main.py --server.maxUploadSize 2000
```



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

<!-- images of project -->
<img src="/img/projectimg1.png" alt="cmd">
<img src="/img/projectimg2.png" alt="homepage">
<img src="/img/projectimg3.png" alt="Diarization page">
<img src="/img/projectimg4.png" alt="project image">
<img src="/img/projectimg5.png" alt="mobile view">


