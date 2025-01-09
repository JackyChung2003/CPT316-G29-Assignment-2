import React, { useState } from "react";
import { FaMicrophone, FaMicrophoneSlash, FaLocationArrow } from "react-icons/fa";
import { IoCloseSharp } from "react-icons/io5";
import "./index.css";

const Home = () => {
  const [comment, setComment] = useState(""); // User input
  const [toxicity, setToxicity] = useState(null); // Toxicity percentage
  const [isToxic, setIsToxic] = useState(null); // Toxic/Non-Toxic result
  const [isRecording, setIsRecording] = useState(false); // Microphone toggle state

  // Toggle microphone recording state
  const toggleMicrophone = () => {
    setIsRecording((prevState) => !prevState);
  };

  // Mock fetch response for toxicity analysis
  const analyzeComment = () => {
    const mockResponse = {
      toxicity_score: Math.random().toFixed(2), // Random percentage for simulation
      toxic: Math.random() > 0.5, // Random boolean for toxic or non-toxic
    };

    setToxicity((mockResponse.toxicity_score * 100).toFixed(0)); // Convert to percentage
    setIsToxic(mockResponse.toxic);
  };

  // Clear the input and analysis results
  const clearInput = () => {
    setComment("");
    setToxicity(null);
    setIsToxic(null);
  };

  return (
    <div className="home-container">
      {/* Analysis Section */}
      <div className="analysis-section">
        <div className="donut-chart">
          <div
            className="donut-circle"
            style={{
              background: `conic-gradient(
                ${isToxic ? "#f44336" : "#00c853"} ${toxicity || 0}%,
                #ddd ${toxicity || 0}%
              )`,
            }}
          >
            <span className="donut-percentage">{toxicity || 0}%</span>
          </div>
        </div>
        <div className="result-status">
          <h2>Analysis Result</h2>
          <p className="toxicity-result">
            The comment is{" "}
            <span
              className="toxic-status"
              style={{
                color: isToxic === null ? "#bbb" : isToxic ? "#f44336" : "#00c853",
              }}
            >
              {isToxic === null ? "Unknown" : isToxic ? "Toxic" : "Non-Toxic"}
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
            {comment ? (
              <button className="btn send-btn" onClick={analyzeComment}>
                <FaLocationArrow size={16} />
              </button>
            ) : (
              <button className="btn sound-btn" onClick={toggleMicrophone}>
                {isRecording ? <FaMicrophoneSlash size={16} /> : <FaMicrophone size={16} />}
              </button>
            )}
          </div>
        </div>
        {/* <div className="chat-actions">
          {comment ? (
            <button className="btn send-btn" onClick={analyzeComment}>
              <FaLocationArrow size={16} />
            </button>
          ) : (
            <button className="btn sound-btn" onClick={toggleMicrophone}>
              {isRecording ? <FaMicrophoneSlash size={16} /> : <FaMicrophone size={16} />}
            </button>
          )}
        </div> */}
      </div>
    </div>
  );
};

export default Home;
