import React, { useState } from 'react';
import { registerTranscript } from '../services/api';

interface TranscriptRegistrationProps {
  onRegister: (transcriptId: string) => void;
}

const TranscriptRegistration: React.FC<TranscriptRegistrationProps> = ({ onRegister }) => {
  const [transcriptId, setTranscriptId] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await registerTranscript(transcriptId);
      onRegister(transcriptId);
    } catch (error) {
      console.error('Error registering transcript:', error);
    }
  };

  return (
    <div className="input-container">
      <h2>Register Transcript</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={transcriptId}
          onChange={(e) => setTranscriptId(e.target.value)}
          placeholder="Enter Transcript ID"
          required
        />
        <div className="button-spacing">
          <button type="submit">Register</button>
        </div>
      </form>
    </div>
  );
};

export default TranscriptRegistration;

export {};
