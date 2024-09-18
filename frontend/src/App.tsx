import React, { useState } from 'react';
import TranscriptRegistration from './components/TranscriptRegistration';
import TranscriptEditor from './components/TranscriptEditor';
import './App.css';
import logo from './aai-logo.png';

const App: React.FC = () => {
  const [transcriptId, setTranscriptId] = useState<string | null>(null);

  return (
    <div className="App">
      <img src={logo} alt="Logo" className="logo" />
      <h1>PATCH Endpoint Frontend</h1>
      {!transcriptId ? (
        <TranscriptRegistration onRegister={setTranscriptId} />
      ) : (
        <TranscriptEditor transcriptId={transcriptId} />
      )}
    </div>
  );
};

export default App;
