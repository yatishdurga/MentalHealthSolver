import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { analyzeText } from "../services/api";

function TextInputForm() {
  const [text, setText] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!text.trim()) {
      setError("Please enter some text to analyze.");
      return;
    }

    try {
      const result = await analyzeText(text);
      navigate("/results", { state: { prediction: result.prediction } });
    } catch (err) {
      console.error("Error:", err);
      setError("Something went wrong!");
    }
  };

  return (
    <div className="container mt-5">
      <h2>Mental Health Text Analysis</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          className="form-control mb-3"
          rows="5"
          placeholder="Describe how you feel..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button className="btn btn-primary" type="submit">Analyze</button>
        {error && <div className="alert alert-danger mt-2">{error}</div>}
      </form>
    </div>
  );
}

export default TextInputForm;
