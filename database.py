import os
from typing import Dict, Optional

import assemblyai as aai
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables from .env file
load_dotenv()

# Get environment variables
uri = os.getenv("mongodb_uri")
api_key = os.getenv("ASSEMBLYAI_API_KEY")
aai.settings.api_key = api_key

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["transcript_db"]
collection = db["transcripts"]


class TranscriptDocument(BaseModel):
    id: str = Field(default=None, alias="_id")
    transcript: Dict

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


def create_transcript(transcript: Dict):
    doc = TranscriptDocument(id=transcript["id"], transcript=transcript)
    try:
        collection.insert_one(doc.dict(by_alias=True))
        return doc
    except Exception as e:
        print(f"Exception in database/create_transcript: {e}")
        raise e


def fetch_transcript(transcript_id: str) -> Optional[TranscriptDocument]:
    # Fetch the document from MongoDB by _id
    try:
        result = collection.find_one({"_id": transcript_id})
        if result:
            # Create a TranscriptDocument from the result
            return TranscriptDocument(
                **result
            )  # Unpack the result into the Pydantic model
        else:
            print("No transcript found with the given ID.")
            return None
    except Exception as e:
        print(f"An error occurred during fetching: {e}")
        raise e


def update_transcript(
    transcript_id: str, transcript: Dict
) -> Optional[TranscriptDocument]:
    # Update the existing transcript in MongoDB
    try:
        collection.update_one({"_id": transcript_id}, {"$set": transcript})
        return fetch_transcript(transcript_id)
    except Exception as e:
        print(f"An error occurred during updating: {e}")
        raise e
