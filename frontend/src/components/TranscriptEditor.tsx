import React, { useState, useRef, useEffect } from 'react';
import audioFile from '../1QQBB3cwNM0.wav';
import { FaPlay, FaPause, FaRedo } from 'react-icons/fa';

interface Word {
  text: string;
  start: number;
  end: number;
}

const words: Word[] = [
  { text: "Here's", start: 320, end: 488 },
  { text: "what's", start: 488, end: 616 },
  { text: "going", start: 616, end: 728 },
  { text: "to", start: 734, end: 886 },
  { text: "happen.", start: 918, end: 1182 },
  { text: "I", start: 1246, end: 1374 },
  { text: "am", start: 1382, end: 1526 },
  { text: "going", start: 1558, end: 1678 },
  { text: "to", start: 1694, end: 1822 },
  { text: "have", start: 1846, end: 2006 },
  { text: "to", start: 2038, end: 2470 },
  { text: "fix", start: 2590, end: 2958 },
  { text: "you,", start: 3014, end: 3374 },
  { text: "manage", start: 3462, end: 3854 },
  { text: "you", start: 3942, end: 4310 },
  { text: "to", start: 4390, end: 4894 },
  { text: "on", start: 5022, end: 5238 },
  { text: "a", start: 5254, end: 5406 },
  { text: "more", start: 5438, end: 5702 },
  { text: "personal", start: 5766, end: 6370 },
  { text: "scale,", start: 6750, end: 7570 },
  { text: "a", start: 8270, end: 8606 },
  { text: "more", start: 8638, end: 8854 },
  { text: "micro", start: 8902, end: 9422 },
  { text: "form", start: 9526, end: 9766 },
  { text: "of", start: 9798, end: 9990 },
  { text: "management.", start: 10030, end: 10422 },
  { text: "Jim,", start: 10526, end: 10806 },
  { text: "what", start: 10838, end: 10934 },
  { text: "is", start: 10942, end: 11038 },
  { text: "that", start: 11054, end: 11182 },
  { text: "called?", start: 11206, end: 11534 },
  { text: "Microjument", start: 11622, end: 12406 },
  { text: "boom.", start: 12478, end: 12886 },
  { text: "Yes.", start: 12958, end: 13110 }
];

const TranscriptEditor: React.FC = () => {
  const [text, setText] = useState(words.map(w => w.text).join(' '));
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isEnded, setIsEnded] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);
  const editorRef = useRef<HTMLDivElement>(null);

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
    return words.map((word, index) => {
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
      <button className="confirm-changes-button">Confirm Changes</button>
      <audio
        ref={audioRef}
        src={audioFile}
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
