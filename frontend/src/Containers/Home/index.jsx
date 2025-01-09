import React, { useState } from "react";
import { FaLocationArrow } from "react-icons/fa";
import { IoCloseSharp } from "react-icons/io5";
import axios from "axios"; // Import Axios for HTTP requests
import "./index.css";

import Speedometer from "../../Component/SpeedMeter";
const Home = () => {
  const [comment, setComment] = useState(""); // User input
  const [toxicity, setToxicity] = useState(null); // Toxicity percentage
  const [isToxic, setIsToxic] = useState(null); // Toxic/Non-Toxic result
  const [toxicityLabel, setToxicityLabel] = useState("Unknown"); // Label for toxicity level


  // Fetch response for toxicity analysis from the backend
  const analyzeComment = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/classify", { text: comment });

      // Extract the response data
      const { toxicity_score, toxic } = response.data;

      // Update state with backend response
      setToxicity((toxicity_score * 100).toFixed(0)); // Convert to percentage
      setIsToxic(toxic);

      // Determine toxicity label
      let label = "Unknown";
      if (toxicity_score >= 0.8) {
        label = "Toxic";
      } else if (toxicity_score >= 0.5) {
        label = "Moderate Toxicity";
      } else {
        label = "Low Toxicity/Non-Toxic";
      }
      setToxicityLabel(label);

    } catch (error) {
      console.error("Error analyzing comment:", error);
      setToxicity(null);
      setIsToxic(null);
      setToxicityLabel("Error");
      alert("Failed to analyze comment. Please try again later.");
    }
  };

  // Clear the input and analysis results
  const clearInput = () => {
    setComment("");
    setToxicity(null);
    setIsToxic(null);
    setToxicityLabel("Unknown");
  };

  return (
    <div className="home-container">
      {/* Analysis Section */}
      <div className="analysis-section">
        <div className="donut-chart">
          <Speedometer value={toxicity || 0} />
        </div>
        <div className="result-status">
          <h2>Analysis Result</h2>
          <p className="toxicity-result">
            The comment is{" "}
             <span
              className={`toxic-status ${
                toxicityLabel === "Toxic"
                  ? "high"
                  : toxicityLabel === "Moderate Toxicity"
                  ? "moderate"
                  : "low"
              }`}
            >
              {toxicityLabel}
            </span>
          </p>
        </div>
      </div>

      {/* Chat Section */}
      <div className="chat-section">
        <div className="chat-input-wrapper">
          <textarea
            className="chat-input"
            placeholder="Type your comment here..."
            value={comment}
            onChange={(e) => setComment(e.target.value)}
          />
          {comment && (
            <button className="clear-button" onClick={clearInput}>
              <IoCloseSharp size={20} />
            </button>
          )}
          <div className="chat-actions">
            <button
              className={`btn send-btn ${comment ? "active" : "inactive"}`}
              onClick={analyzeComment}
              disabled={!comment}
            >
              <FaLocationArrow size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;