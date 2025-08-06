from fastapi import FastAPI, Response
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
    
    return Response(content=wav_data, media_type="audio/wav")

# To run this local server, you would use a command like:
# uvicorn api:web_app --reload
