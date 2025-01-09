import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./Containers/Home";
import NotFound from "./Containers/Notfound";
import HorizontalNavbar from "./Containers/Navigation/HorizontalNavBar";
import "./App.css";

const App = () => {
  return (
    <Router>
      <div className="app">
        <HorizontalNavbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
