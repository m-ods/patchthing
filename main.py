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

def reconstruct_sentences(words: List[Word], sentence_breaks: List[int]): # -> List[dict]:
    # Reconstruct sentence objects from words

    # technically there's no need for sentence breaks because punctuation is attached to the word.
    pass

def reconstruct_paragraphs(sentences: List[Sentence]): # -> List[dict]:
    # Reconstruct paragraph objects from sentences
    pass

# def reconstruct_transcript(original_transcript: dict, new_text: str) -> dict:

#     # basically compare the transcripts then make the changes to old transcript and save it in the db

#     # Tokenize the new text
#     new_words, new_sentences = tokenize_text(new_text)
    
#     # Perform diff between original and new text
#     diffs = list(difflib.ndiff(original_transcript['text'].split(), new_text.split()))
    
#     # Map new words to original words, preserving metadata where possible
#     updated_words = map_words(original_transcript['words'], new_words, diffs)
    
#     # Reconstruct sentences and paragraphs
#     updated_sentences = reconstruct_sentences(updated_words, new_sentences)
#     updated_paragraphs = reconstruct_paragraphs(updated_sentences)
    
#     # Update the transcript object
#     updated_transcript = original_transcript.copy()
#     updated_transcript['text'] = new_text
#     updated_transcript['words'] = updated_words
#     updated_transcript['sentences'] = updated_sentences
#     updated_transcript['paragraphs'] = updated_paragraphs
    
#     return updated_transcript

@app.patch("/transcripts/{transcript_id}")
async def update_transcript(transcript_id: str, update: TranscriptUpdate):
    transcript = transcripts.get(transcript_id)
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    
    updated_transcript = reconstruct_transcript(transcript, update.full_text)
    
    transcripts[transcript_id] = updated_transcript
    return {"message": "Transcript updated successfully", "transcript": updated_transcript}