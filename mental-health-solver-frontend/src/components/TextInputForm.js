import { analyzeText } from '../services/api';
import { useNavigate } from 'react-router-dom';

const handleSubmit = async (e) => {
  e.preventDefault();

  try {
    const result = await analyzeText(inputText);
    console.log('Prediction result:', result);

    // Pass result to ResultsPage (temporarily using state)
    navigate('/results', { state: { result } });
  } catch (error) {
    alert('Failed to analyze text. Please try again later.');
  }
};
