import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();

  // Updated to match the structure passed from HomePage.jsx
  const prediction = location.state?.result?.prediction;

  if (!prediction) {
    return (
      <div className="container mt-5">
        <h4>No prediction found. Please submit some text first.</h4>
        <button className="btn btn-secondary mt-3" onClick={() => navigate("/")}>
          Go Back
        </button>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <h3>Prediction Result</h3>
      <p>Your mental health category might be:</p>
      <div className="alert alert-info">
        <strong>{prediction}</strong>
      </div>
      <button className="btn btn-secondary" onClick={() => navigate("/")}>
        Analyze Another
      </button>
    </div>
  );
}

export default ResultsPage;
