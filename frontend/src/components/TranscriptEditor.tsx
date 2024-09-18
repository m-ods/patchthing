import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface TranscriptEditorProps {
  transcriptId: string;
}

const TranscriptEditor: React.FC<TranscriptEditorProps> = ({ transcriptId }) => {
  const [transcript, setTranscript] = useState('');
  const [editedTranscript, setEditedTranscript] = useState('');

  useEffect(() => {
    const fetchTranscript = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/${transcriptId}`);
        setTranscript(response.data.text);
        setEditedTranscript(response.data.text);
      } catch (error) {
        console.error('Error fetching transcript:', error);
      }
    };

    fetchTranscript();
  }, [transcriptId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.patch(`http://localhost:8000/transcripts/${transcriptId}`, {
        old_text: transcript,
        new_text: editedTranscript,
      });
      setTranscript(editedTranscript);
    } catch (error) {
      console.error('Error updating transcript:', error);
    }
  };

  return (
    <div className="input-container">
      <h2>Edit Transcript</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={editedTranscript}
          onChange={(e) => setEditedTranscript(e.target.value)}
          rows={10}
          required
        />
        <button type="submit">Update Transcript</button>
      </form>
    </div>
  );
};

export default TranscriptEditor;

export {};
