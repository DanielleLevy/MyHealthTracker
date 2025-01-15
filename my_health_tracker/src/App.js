import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./loginPage/LoginPage";
import MainPage from "./MainPage";
import SignUp from "./signUp/SignUp"; 

function App() {
  const [showSignUp, setShowSignUp] = useState(false); 

  const handleCreateAccountClick = () => {
    setShowSignUp(true); 
  };

  const handleCloseSignUp = () => {
    setShowSignUp(false); 
  };

  return (
    <div className="App" >
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            !showSignUp ? (
              <LoginPage onCreateAccount={handleCreateAccountClick} />
            ) : (
              <SignUp onClose={handleCloseSignUp} />
            )
          }
        />
        <Route path="/mainpage" element={<MainPage />} />
      </Routes>
    </Router>
    </div>
  );
}

export default App;
