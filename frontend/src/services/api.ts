import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const registerTranscript = async (transcriptId: string) => {
  const response = await axios.post(`${API_BASE_URL}/${transcriptId}`);
  return response.data;
};

export const getTranscript = async (transcriptId: string) => {
  const response = await axios.get(`${API_BASE_URL}/${transcriptId}`);
  return response.data;
};

export const updateTranscript = async (transcriptId: string, update: { old_text: string; new_text: string }) => {
  const response = await axios.patch(`${API_BASE_URL}/transcripts/${transcriptId}`, update);
  return response.data;
};

export {};