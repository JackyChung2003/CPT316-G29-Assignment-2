import ReactSpeedometer from "react-d3-speedometer";

const Speedometer = ({ value }) => {
  return (
    <div style={{ width: "100%", maxWidth: "400px", margin: "0 auto" }}>
      <ReactSpeedometer
        value={value} // Value to display
        minValue={0} // Minimum value of the gauge
        maxValue={100} // Maximum value of the gauge
        segments={5} // Number of segments in the gauge
        needleColor="#333" // Needle color
        startColor="green" // Starting segment color
        endColor="red" // Ending segment color
        textColor="#fff" // Text color
        height={200} // Height of the gauge
      />
    </div>
  );
};

export default Speedometer;
