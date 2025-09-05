import modal
from pathlib import Path
import tempfile
import os
from vietvoicetts import synthesize

# This is the central object that defines our Modal application.
app = modal.App("vietvoice-tts")

# This is a one-time setup function that runs during the image build process.
# It pre-downloads the model weights and caches them in the image, so they
# don't need to be downloaded every time a container starts.
def download_model():
    """
    Downloads the model weights into the image.
    This function runs as a build step.
    """
    from vietvoicetts.api import TTSApi
    TTSApi().engine

# Define the container image for our Modal application.
# This image contains all the necessary system packages, Python libraries,
# and local source code required to run the TTS model.
image = (
    # Start from a basic Debian Linux image with Python 3.10.
    modal.Image.debian_slim(python_version="3.10")
    # Install system packages required by the application.
    # - libsndfile1 is for reading/writing audio files.
    # - ffmpeg is for audio processing.
    .apt_install("libsndfile1", "ffmpeg")
    # Install the required Python packages using pip.
    .pip_install(
        "numpy>=1.21.0",
        "soundfile>=0.10.3",
        "pydub>=0.25.0",
        "tqdm>=4.64.0",
        "onnxruntime-gpu>=1.15.0",
        "torch",
    )
    # Include the local `vietvoicetts` source code in the image.
    # `copy=True` ensures the files are copied into the image layer,
    # making them available to subsequent build steps like `run_function`.
    .add_local_python_source("vietvoicetts", copy=True)
    # Execute the `download_model` function as a build step.
    # This requires a GPU and extra memory to initialize the model successfully.
    .run_function(
        download_model,
        gpu="T4",
        memory=8192,
    )
)

# Assign the configured image to our application.
app.image = image

# This is the core remote function that performs the text-to-speech synthesis.
# It runs on a L4 GPU for hardware acceleration.
@app.function(gpu="L4")
def synthesize(text: str, gender: str = "female", area: str = "northern", emotion: str = "neutral", group: str = "story") -> bytes:
    """
    Synthesizes audio from text using the VietVoice-TTS model on a L4 GPU.
    """
    from vietvoicetts.api import synthesize_to_bytes
    
    wav_bytes, _ = synthesize_to_bytes(
        text=text,
        gender=gender,
        area=area,
        emotion=emotion,
        group=group
    )
    return wav_bytes


@app.function(gpu="L4")
def clone_voice(text: str, reference_audio_bytes: bytes, reference_text: str) -> bytes:
    """
    Synthesizes audio from text using voice cloning.
    """
    import tempfile
    import os
    
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            tmpfile.write(reference_audio_bytes)
            tmp_path = tmpfile.name

        # Synthesize the audio
        duration = synthesize(
            text,
            "cloned_voice.wav",
            reference_audio=tmp_path,
            reference_text=reference_text
        )

        # Read the synthesized audio
        with open("cloned_voice.wav", "rb") as f:
            wav_bytes = f.read()

    finally:
        # Delete the temporary file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        if os.path.exists("cloned_voice.wav"):
            os.remove("cloned_voice.wav")

    return wav_bytes
