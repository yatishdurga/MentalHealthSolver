// src/pages/HomePage.js
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function HomePage() {
  const [inputText, setInputText] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/analyze', { text: inputText });
      navigate('/results', { state: { result: response.data } });
    } catch (error) {
      alert('Something went wrong');
    }
  };

  return (
    <div className="card p-4">
      <h2 className="mb-3">Mental Health Text Analysis</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group mb-3">
          <textarea
            className="form-control"
            rows="4"
            placeholder="Type your thoughts here..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            required
          ></textarea>
        </div>
        <button className="btn btn-primary" type="submit">Analyze</button>
      </form>
    </div>
  );
}

export default HomePage;
