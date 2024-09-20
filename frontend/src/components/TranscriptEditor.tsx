import React, { useState, useRef, useEffect } from 'react';
import { FaPlay, FaPause, FaRedo } from 'react-icons/fa';

interface Word {
  text: string;
  start: number;
  end: number;
}

interface Transcript {
  words: Word[];
  text: string;
}

const TranscriptEditor: React.FC = () => {
  const [transcript, setTranscript] = useState<Transcript>({ words: [], text: '' });
  const [text, setText] = useState('');
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isEnded, setIsEnded] = useState(false);
  const [audioUrl, setAudioUrl] = useState('');
  const [transcriptId, setTranscriptId] = useState('');
  const audioRef = useRef<HTMLAudioElement>(null);
  const editorRef = useRef<HTMLDivElement>(null);

  

  useEffect(() => {
    // Fetch transcript data
    fetch("http://127.0.0.1:8000/a5d413dc-9b20-41db-9ae0-53efbd610de4")
      .then(response => response.json())
      .then(data => {
        setTranscript(data.transcript);
        setText(data.transcript.text);
        setTranscriptId(data.transcript.id);
        setAudioUrl("https://storage.googleapis.com/linkthing/uploaded_files/Michael%2C%20Jim%2C%20Dwight%20epic%20scene%20%5BqHrN5Mf5sgo%5D.mp4");
      })
      .catch(error => console.error('Error fetching transcript:', error));
  }, []);

  const handleTextChange = (e: React.FormEvent<HTMLDivElement>) => {
    setText(e.currentTarget.textContent || '');
  };

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
    }
  };

  const handleAudioEnded = () => {
    setIsPlaying(false);
    setIsEnded(true);
  };

  const togglePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
        setIsEnded(false);
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleReplay = () => {
    if (audioRef.current) {
      audioRef.current.currentTime = 0;
      audioRef.current.play();
      setIsPlaying(true);
      setIsEnded(false);
    }
  };

  const renderHighlightedText = () => {
    return transcript.words.map((word, index) => {
      const isActive = currentTime * 1000 >= word.start && currentTime * 1000 <= word.end;
      return (
        <span
          key={index}
          className={isActive ? 'active' : ''}
        >
          {word.text}{' '}
        </span>
      );
    });
  };

  const handleConfirmChanges = async () => {
    const updateData = {
      old_text: transcript.text,
      new_text: text
    };

    try {
      const response = await fetch(`http://127.0.0.1:8000/transcripts/${transcriptId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log('Update successful:', result);
      
      // Update the local transcript state with the new data
      setTranscript(result.transcript);
      setText(result.transcript.text);

    } catch (error) {
      console.error('Error updating transcript:', error);
    }
  };

  useEffect(() => {
    if (editorRef.current) {
      const activeWord = editorRef.current.querySelector('span.active');
      if (activeWord) {
        activeWord.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  }, [currentTime]);

  return (
    <div className="transcript-editor">
      <div className="audio-player">
        <button
          onClick={isEnded ? handleReplay : togglePlayPause}
          className="control-button"
          aria-label={isEnded ? "Replay" : isPlaying ? "Pause" : "Play"}
        >
          {isEnded ? <FaRedo /> : isPlaying ? <FaPause /> : <FaPlay />}
        </button>
        <div className="progress-bar">
          <div
            className="progress"
            style={{ width: `${(currentTime / duration) * 100}%` }}
          ></div>
        </div>
        <div className="time-display">
          {formatTime(currentTime)} / {formatTime(duration)}
        </div>
      </div>
      <div
        ref={editorRef}
        className="editable-text"
        contentEditable
        onInput={handleTextChange}
        suppressContentEditableWarning={true}
        role="textbox"
        aria-label="Editable transcript"
      >
        {renderHighlightedText()}
      </div>
      <button className="confirm-changes-button" onClick={handleConfirmChanges}>Confirm Changes</button>
      <audio
        ref={audioRef}
        src={audioUrl}
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        onEnded={handleAudioEnded}
      />
    </div>
  );
};

function formatTime(seconds: number): string {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

export default TranscriptEditor;