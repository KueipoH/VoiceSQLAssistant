# transcriber/whisper.py
from openai import OpenAI
from utils.logger import setup_logger

logger = setup_logger(__name__)

def transcribe_audio(client: OpenAI, audio_file_path: str):
    """
    Transcribes audio using the OpenAI Whisper model.
    You need to set the OPENAI_API_KEY in environment variables or specify the api_key in the client.
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        return None

