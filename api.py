import io
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import modal

# Define the FastAPI application
web_app = FastAPI(title="VietVoice TTS API")

class SynthesisRequest(BaseModel):
    text: str
    gender: str = "female"
    area: str = "northern"
    emotion: str = "neutral"
    group: str = "story"

def audio_response(wav_bytes: bytes):
    # Inline filename is helpful; length can improve playback reliability
    headers = {
        "Content-Disposition": 'inline; filename="tts.wav"',
        "Content-Length": str(len(wav_bytes)),
        # Some browsers like having byte serving; if you later add Range support, also set Accept-Ranges
        # "Accept-Ranges": "bytes",
    }
    return StreamingResponse(io.BytesIO(wav_bytes), media_type="audio/wav", headers=headers)

@web_app.post("/synthesize")
async def create_synthesis(request: SynthesisRequest):
    """
    API endpoint to synthesize speech.
    This function looks up the deployed Modal function and calls it to generate audio.
    """
    # Look up the remote function from the deployed "vietvoice-tts" Modal app
    synthesize_function = modal.Function.from_name("vietvoice-tts", "synthesize")
    
    # Call the remote function with the provided parameters
    wav_data = await synthesize_function.remote.aio(
        text=request.text,
        gender=request.gender,
        area=request.area,
        emotion=request.emotion,
        group=request.group,
    )
    
    return audio_response(wav_data)

# To run this local server, you would use a command like:
# uvicorn api:web_app --reload
