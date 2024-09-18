import os

import assemblyai as aai
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import reconstructor
from utils import update_assemblyai_words

# Load environment variables from .env file
load_dotenv()

# Get environment variables
api_key = os.getenv("ASSEMBLYAI_API_KEY")
aai.settings.api_key = api_key

app = FastAPI()

# key - transcript ID, value - transcript JSON obj
transcripts = {}


class TranscriptUpdate(BaseModel):
    old_text: str
    new_text: str


@app.post("/{transcript_id}")
def register_transcript(transcript_id):
    try:
        t = aai.Transcript.get_by_id(transcript_id)
    except Exception as e:
        print(f"Exception in POST /<transcript_id> - {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Transcript {transcript_id} is not registered. Please use the AAI API to re-transcribe.",
        ) from None

    # TODO: Once we fetch from AAI api, save to Mongo if it doesnt exist?

    transcript = t.json_response
    if transcript:
        transcript["sentences"] = t.get_sentences()
        transcript["paragraphs"] = t.get_paragraphs()
    transcripts[transcript_id] = transcript
    return transcript


@app.get("/{transcript_id}")
def get_transcript(transcript_id):
    if transcript_id not in transcripts:
        raise HTTPException(
            status_code=400,
            detail=f"Please call POST /{transcript_id} to register the transcript first.",
        )

    # TODO: Fetch from mongo
    transcript = transcripts[transcript_id]
    return transcript


@app.patch("/transcripts/{transcript_id}")
async def update_transcript(transcript_id: str, update: TranscriptUpdate):
    transcript = transcripts.get(transcript_id)
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")

    words = update_assemblyai_words(transcript.words, update.old_text, update.new_text)

    # TODO: Test removals / additions / Add DB support?
    updated_transcript = reconstructor.reconstruct_transcript(transcript, words)

    # TODO: update mongo @ transcript id
    transcripts[transcript_id] = updated_transcript
    return {
        "message": "Transcript updated successfully",
        "transcript": updated_transcript,
    }


if __name__ == "__main__":
    print("Starting server on port 8000")
    uvicorn.run(
        app,
        # trunk-ignore(bandit/B104)
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug",
        debug=True,
    )
