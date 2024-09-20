# 🧩 Patch-thing

Patch-thing is a FastAPI-based backend service for managing and updating transcripts. It integrates with AssemblyAI for transcription services and uses MongoDB for data storage.

## Features

- Register and fetch transcripts
- Update existing transcripts
- Reconstruct transcript components (words, sentences, paragraphs, utterances)
- Integration with AssemblyAI API
- MongoDB database storage

## Prerequisites

- Python 3.7+
- MongoDB
- AssemblyAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/patchthing.git
   cd patchthing
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r backend/requirements.txt
   ```

4. Create a `.env` file in the `backend` directory with the following content:
   ```
   ASSEMBLYAI_API_KEY=your_assemblyai_api_key
   ```

## Running the Backend

To start the backend server:

```
cd backend
uvicorn main:app 
```

The server will start on `http://0.0.0.0:8000`.

## API Endpoints

- `POST /{transcript_id}`: Register a transcript
- `GET /{transcript_id}`: Fetch a transcript
- `PATCH /transcripts/{transcript_id}`: Update a transcript

For more details on the API endpoints, refer to the `main.py` file:

## Project Structure

- `backend/`: Contains the main application code
  - `main.py`: FastAPI application and route definitions
  - `database.py`: MongoDB connection and operations
  - `reconstructor.py`: Functions for reconstructing transcript components
  - `utils.py`: Utility functions for text processing
- `requirements.txt`: Python dependencies


