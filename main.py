from typing import Union, List, Tuple
from fastapi import FastAPI, HTTPException
import assemblyai as aai
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from assemblyai.types import Word, Sentence, Paragraph, Utterance, UtteranceWord
import difflib

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

class TranscriptUpdate(BaseModel):
    full_text: str

def tokenize_text(text: str): #-> Tuple[List[str], List[str]]:
    # Use NLTK or a similar library to tokenize text into words and sentences
    return ([],[])

def map_words(original_words: List[Word], new_words: List[str], diffs: List[str]): # -> List[dict]:
    # Map new words to original words, preserving timestamps and confidence scores where possible
    pass

@app.patch("/transcripts/{transcript_id}")
async def update_transcript(transcript_id: str, update: TranscriptUpdate):
    transcript = transcripts.get(transcript_id)
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    
    updated_transcript = None
    # updated_transcript = reconstruct_transcript(transcript, update.full_text)
    
    transcripts[transcript_id] = updated_transcript
    return {"message": "Transcript updated successfully", "transcript": updated_transcript}