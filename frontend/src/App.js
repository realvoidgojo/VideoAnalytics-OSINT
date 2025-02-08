import React from "react";
import VideoDisplay from "./components/VideoDisplay";
import "./App.css";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>CCTV Analytics</h1>
        <VideoDisplay />
      </header>
    </div>
  );
}

export default App;
