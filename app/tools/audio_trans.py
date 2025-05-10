from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
openai = OpenAI(api_key=API_KEY)
# def transcribe_audio(file_path: str) -> str:

#     transcription = openai.audio.transcriptions.create(
#         model="gpt-4o-transcribe", 
#         file=file_path
#     )

#     return transcription.text

def transcribe_audio(audio_fp) -> str:
    response = openai.audio.transcriptions.create(
        model="whisper-1",
        file=audio_fp,
        response_format="text"
    )
    return response