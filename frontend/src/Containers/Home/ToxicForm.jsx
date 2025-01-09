import React, { useState } from "react";

const ToxicForm = () => {
  const [text, setText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Call the API
    console.log("Text Submitted:", text);
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        placeholder="Enter your text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        required
      ></textarea>
      <button type="submit">Analyze</button>
    </form>
  );
};

export default ToxicForm;
