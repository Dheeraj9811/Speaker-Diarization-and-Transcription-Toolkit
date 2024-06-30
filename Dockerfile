# Use the official Ubuntu 20.04 image
FROM ubuntu:20.04

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Install basic dependencies
RUN apt-get update && apt-get install -y build-essential cmake git wget curl ca-certificates gnupg2 lsb-release && \
    rm -rf /var/lib/apt/lists/*

# Install basic editors
RUN apt-get update && apt-get install -y vim nano

# Install CUDA 12.3.0 (driver >=545.23.06)
# Check driver version: https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html#id6
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin && \
	mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600 && \
    	wget https://developer.download.nvidia.com/compute/cuda/12.2.0/local_installers/cuda-repo-ubuntu2004-12-2-local_12.2.0-535.54.03-1_amd64.deb && \
    	dpkg -i cuda-repo-ubuntu2004-12-2-local_12.2.0-535.54.03-1_amd64.deb && \
    	cp /var/cuda-repo-ubuntu2004-12-2-local/cuda-*-keyring.gpg /usr/share/keyrings/ && \
    	apt-get update && \
    	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends cuda



# Environment setup
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

# Install pip
RUN apt-get update && apt-get install -y python3-pip

# upgrade pip to be able to install tensorrt
RUN pip install --upgrade pip
RUN pip install streamlit


#install pytorch
RUN pip3 install torch torchvision torchaudio

#Project file
RUN apt update && apt install ffmpeg -y
RUN pip install setuptools-rust && \
	python3 -m pip install moviepy && \
	python3 -m pip install pydub && \
	python3 -m pip install -U openai-whisper && \
	python3 -m pip install pyannote.audio && \
	python3 -m pip install python-dotenv && \
	python3 -m pip install streamlit-extras


# Clone the Git repository
RUN git clone https://github.com/Dheeraj9811/Speaker-Diarization-and-Transcription-Toolkit.git
# Change directory to the cloned repository
WORKDIR /Speaker-Diarization-and-Transcription-Toolkit/src

RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run Streamlit
CMD ["streamlit", "run", "main.py", "--server.maxUploadSize", "2000"]
