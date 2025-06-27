// src/services/api.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // 🔁 Change this if your backend is deployed elsewhere

export const analyzeText = async (inputText) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/analyze`, { text: inputText });
    return response.data;
  } catch (error) {
    console.error('API error:', error);
    throw error;
  }
};
