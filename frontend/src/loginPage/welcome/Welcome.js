import React from 'react';
import './Welcome.css';
import logo from './logo.png';  // Import SVG as a React component

function Welcome() {
  return (
    <div className="col-12 col-md-6 col-lg-4 text-center">
      <img className="App-logo" alt="logo" src={logo} />
      <h2 className="text-center mb-4 text-maroon icon">
        Welcome to  
      </h2>
      <h2 className="text-center mb-4 text-maroon icon app-name">
        <i className="fas fa-heartbeat me-2"></i>My Health Tracker
      </h2>
      <div className="text-center mb-4">
        <p className="text-maroon">Track your health, manage your fitness goals, and stay on top of your well-being.</p>
      </div>
    </div>
  );
}

export default Welcome;
