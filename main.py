from typing import Union
from fastapi import FastAPI, HTTPException
import assemblyai as aai
from dotenv import load_dotenv
import os
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# Get environment variables
api_key = os.getenv('ASSEMBLYAI_API_KEY')
aai.settings.api_key = api_key

app = FastAPI()

# key - transcript ID, value - transcript JSON obj
transcripts = {}

@app.post("/{transcript_id}")
def register_transcript(transcript_id):
    t = aai.Transcript.get_by_id(transcript_id)

    transcript = t.json_response
    if transcript:
        transcript['sentences'] = t.get_sentences()
        transcript['paragraphs'] = t.get_paragraphs()
    transcripts[transcript_id] = transcript
    return transcript


@app.get("/{transcript_id}")
def get_transcript(transcript_id):
    transcript = transcripts[transcript_id]
    return transcript


class SentenceUpdate(BaseModel):
    text: str
    sentence_index: int

@app.patch("/{transcript_id}/sentences")
async def update_sentence(transcript_id: str, update: SentenceUpdate):
    transcript = transcripts.get(transcript_id, None)

    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    
    if update.sentence_index < 0 or update.sentence_index >= len(transcript["sentences"]):
        raise HTTPException(status_code=404, detail="Sentence not found")
    
    transcript["sentences"][update.sentence_index].text = update.text

    transcripts[transcript_id] = transcript

    return transcript