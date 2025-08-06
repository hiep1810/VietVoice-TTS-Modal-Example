# VietVoice-TTS API Server

This project provides a text-to-speech (TTS) API server for Vietnamese, powered by the VietVoice-TTS model and Modal.

## Features

- High-quality Vietnamese speech synthesis.
- API server built with FastAPI.
- GPU-accelerated synthesis using Modal.

## Prerequisites

- Python 3.10 or later
- Modal account and CLI configured

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/hiep1810/VietVoice-TTS-Modal-Example.git
   cd VietVoice-TTS-Modal-Example
   ```

2. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Deploy the Modal application:**

   This command deploys the `synthesize` function to Modal.

   ```bash
   modal deploy modal_app.py
   ```

2. **Run the local API server:**

   This command starts the local FastAPI server.

   ```bash
   uvicorn api:web_app --host 0.0.0.0 --port 8000
   ```

3. **Send a synthesis request:**

   You can use the provided `test_api.py` script to send a test request to the API server.

   ```bash
   python test_api.py
   ```

   This will send a request to the API server and save the synthesized audio to `output.wav`.

## API Endpoint

### `POST /synthesize`

Synthesizes speech from text.

**Request Body:**

- `text` (str): The text to synthesize.
- `gender` (str, optional): The gender of the voice. Defaults to `"female"`.
- `area` (str, optional): The regional accent. Defaults to `"northern"`.
- `emotion` (str, optional): The emotion of the voice. Defaults to `"neutral"`.
- `group` (str, optional): The voice group. Defaults to `"story"`.

**Response:**

- `200 OK`: The synthesized audio in WAV format.
