export interface Transcript {
  id: string;
  text: string;
  // Add other properties as needed
}

export interface TranscriptUpdate {
  old_text: string;
  new_text: string;
}

export {};