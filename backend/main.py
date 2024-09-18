import os

import assemblyai as aai
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import database as db
import reconstructor
from utils import update_assemblyai_words

# Load environment variables from .env file
load_dotenv()

# Get environment variables
api_key = os.getenv("ASSEMBLYAI_API_KEY")
aai.settings.api_key = api_key

app = FastAPI()

# key - transcript ID, value - transcript JSON obj
class TranscriptUpdate(BaseModel):
    old_text: str
    new_text: str


@app.post("/{transcript_id}")
def register_transcript(transcript_id):
    # First try to fetch it from mongo
    transcript_document = db.fetch_transcript(transcript_id)
    if transcript_document:
        return transcript_document.transcript

    try:
        t = aai.Transcript.get_by_id(transcript_id)
    except Exception as e:
        print(f"Exception in POST /<transcript_id> - {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Transcript {transcript_id} is not registered. Please use the AAI API to re-transcribe.",
        ) from None

    transcript = t.json_response
    if transcript:
        transcript["sentences"] = t.get_sentences()
        transcript["paragraphs"] = t.get_paragraphs()

    db.create_transcript(transcript)
    return transcript


@app.get("/{transcript_id}")
def get_transcript(transcript_id):
    transcript_document = db.fetch_transcript(transcript_id)
    if not transcript_document:
        raise HTTPException(
            status_code=400,
            detail=f"Please call POST /{transcript_id} to register the transcript first.",
        )

    return transcript_document.transcript


@app.patch("/transcripts/{transcript_id}")
async def update_transcript(transcript_id: str, update: TranscriptUpdate):

    if update.old_text.strip().lower() == update.new_text.strip().lower():
        return {"message": "No update needed, both texts are the same"}

    transcript_document = db.fetch_transcript(transcript_id)
    if not transcript_document:
        raise HTTPException(status_code=404, detail="Transcript not found")
    transcript = transcript_document.transcript
    words = update_assemblyai_words(
        transcript["words"], update.old_text, update.new_text
    )

    # TODO: Test removals / additions
    updated_transcript = reconstructor.reconstruct_transcript(transcript, words)

    db.update_transcript(transcript_document.id, updated_transcript)
    return {
        "message": "Transcript updated successfully",
        "transcript": updated_transcript,
    }


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    print("Starting server on port 8000")
    uvicorn.run(
        app,
        # trunk-ignore(bandit/B104)
        host="0.0.0.0",
        port=8000,
    )
