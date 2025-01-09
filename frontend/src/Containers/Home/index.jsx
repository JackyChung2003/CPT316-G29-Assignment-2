import React from "react";
import ToxicForm from "./ToxicForm";
import ToxicResult from "./ToxicResult";
import "./index.css";

const Home = () => {
  return (
    <div className="home">
      <h1>Welcome to ToxiCheck</h1>
      <ToxicForm />
      <ToxicResult />
    </div>
  );
};

export default Home;
