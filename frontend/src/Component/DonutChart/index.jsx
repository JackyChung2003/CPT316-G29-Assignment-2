import React, { useState, useEffect } from "react";
import "./index.css";

const HalfDonutChart = ({ percentage }) => {
  const [displayPercentage, setDisplayPercentage] = useState(0);

  // Animation logic to increment the percentage
  useEffect(() => {
    let start = 0;
    const interval = setInterval(() => {
      start += 1;
      if (start > percentage) {
        clearInterval(interval);
      } else {
        setDisplayPercentage(start);
      }
    }, 10); // Adjust speed of animation here
    return () => clearInterval(interval);
  }, [percentage]);

  return (
    <div className="half-donut-chart">
      <div
        className="half-donut"
        style={{
          background: `conic-gradient(
            ${
              percentage > 50 ? "#f44336" : percentage > 25 ? "#ff9800" : "#00c853"
            } ${displayPercentage * 1.8}deg, 
            #ddd ${displayPercentage * 1.8}deg
          )`,
        }}
      >
        <span className="percentage-text">{displayPercentage}%</span>
      </div>
    </div>
  );
};

export default HalfDonutChart;
