import React from "react";

const ToxicResult = ({ result }) => {
  if (!result) return null;

  return (
    <div className="toxic-result">
      <h2>Analysis Result</h2>
      <p>{result.isToxic ? "The text is toxic." : "The text is not toxic."}</p>
      <p>Toxicity Score: {result.score.toFixed(2)}</p>
    </div>
  );
};

export default ToxicResult;
