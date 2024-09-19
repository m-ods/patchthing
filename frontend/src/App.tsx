import React from 'react';
import './App.css';
import TranscriptEditor from './components/TranscriptEditor';
import logo from './aai-logo.png';

const App: React.FC = () => {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} alt="Logo" className="logo" />
        <h1>Transcript Editor</h1>
      </header>
      <main className="App-main">
        <TranscriptEditor />
      </main>
    </div>
  );
};

export default App;
