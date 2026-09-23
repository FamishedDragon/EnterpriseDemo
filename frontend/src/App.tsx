import React from 'react';
import logo from './logo.svg';
import './App.css';

const handleHealthCheck = async () => {
  try {
    const response = await fetch("http://localhost:8000/health/database");

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const data = await response.json();

    console.log("Backend Response:", data);
  } catch (error) {
    console.error("Backend health check failed:", error);
  }
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <button onClick={handleHealthCheck}> TEST</button>
      </header>
    </div>
  );
}

export default App;
