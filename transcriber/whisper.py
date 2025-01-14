# transcriber/whisper.py
from openai import OpenAI
from utils.logger import setup_logger

logger = setup_logger(__name__)

def transcribe_audio(client: OpenAI, audio_file_path: str):
    """
    使用 OpenAI Whisper 模型進行語音轉錄。
    您需在環境變數中設置 OPENAI_API_KEY 或自行在 client 中指定 api_key。
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        logger.error(f"音頻轉錄出錯：{str(e)}")
        return None

