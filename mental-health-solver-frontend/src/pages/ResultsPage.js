import React from 'react';
import { useLocation } from 'react-router-dom';

function ResultsPage() {
  const location = useLocation();
  const result = location.state?.result;

  return (
    <div>
      <h2>Prediction Result</h2>
      {result ? (
        <div className="alert alert-info">
          <strong>Category:</strong> {result.category}
        </div>
      ) : (
        <p>No result found.</p>
      )}
    </div>
  );
}

export default ResultsPage;
