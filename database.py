from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from assemblyai.types import Word, Sentence, Paragraph, Utterance, UtteranceWord
from assemblyai.transcriber import Transcript as AAITranscript
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import assemblyai as aai

# Load environment variables from .env file
load_dotenv()

# Get environment variables
uri = os.getenv('mongodb_uri')
api_key = os.getenv('ASSEMBLYAI_API_KEY')
aai.settings.api_key = api_key

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["transcript_db"]
collection = db["transcripts"]

class TranscriptDocument(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    transcript: Optional[dict]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


def create_transcript(transcript: AAITranscript):
    doc = TranscriptDocument(transcript=transcript.json_response)
    result = collection.insert_one(doc.dict(by_alias=True, exclude={"id"}))
    doc.id = str(result.inserted_id)
    return doc

if __name__ == "__main__":
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    transcript = aai.Transcript.get_by_id("a5d413dc-9b20-41db-9ae0-53efbd610de4")
    create_transcript(transcript)
