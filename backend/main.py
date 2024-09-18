import json
import os

import assemblyai as aai
import database as db
import reconstructor
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import dictify, update_assemblyai_words

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
        transcript["sentences"] = dictify(t.get_sentences())
        transcript["paragraphs"] = dictify(t.get_paragraphs())

    transcript_document = db.create_transcript(transcript)
    transcript_dict = transcript_document.dict()
    transcript_dict["id"] = str(transcript_dict["id"])
    return transcript_dict


@app.get("/{transcript_id}")
def get_transcript(transcript_id):
    transcript_document = db.fetch_transcript(transcript_id)
    if not transcript_document:
        raise HTTPException(
            status_code=400,
            detail=f"Please call POST /{transcript_id} to register the transcript first.",
        )
    transcript_dict = transcript_document.dict()
    transcript_dict["id"] = str(transcript_dict["id"])
    return transcript_dict


@app.patch("/transcripts/{transcript_id}")
async def update_transcript(transcript_id: str, update: TranscriptUpdate):

    transcript_document = db.fetch_transcript(transcript_id)
    if not transcript_document:
        raise HTTPException(status_code=404, detail="Transcript not found")

    transcript = transcript_document.transcript
    if transcript["text"].strip().lower() != update.old_text.strip().lower():
        raise HTTPException(
            status_code=400,
            detail="Old text parameter doesnt match text in the DB for that transcript. Please reload.",
        )

    if update.old_text.strip().lower() == update.new_text.strip().lower():
        return {"message": "No update needed, both texts are the same"}

    words = update_assemblyai_words(
        transcript["words"], update.old_text, update.new_text
    )

    # TODO: Test removals / additions
    updated_transcript = reconstructor.reconstruct_transcript(transcript, words)

    db.update_transcript(transcript_document.transcript_id, updated_transcript)
    return {
        "message": "Transcript updated successfully",
        "transcript": updated_transcript,
    }


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
