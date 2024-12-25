import './App.css';
import LoginPage from './loginPage/LoginPage';
import SignUp from './signUp/SignUp';
import MainPage from './MainPage';
import { useState } from 'react';

function App() {
  const [showSignUp, setShowSignUp] = useState(false); // Manage which form is displayed

  const handleCreateAccountClick = () => {
      setShowSignUp(true); // Show the SignUp form
  };

  const handleCloseSignUp = () => {
      setShowSignUp(false); // Return to the ForgotPassword form
  };
  return (
    <div className="App">
                  {/* {!showSignUp ? (
                // Render the ForgotPassword component
                <LoginPage onCreateAccount={handleCreateAccountClick} />
            ) : (
                // Render the SignUp component
                <SignUp onClose={handleCloseSignUp} />
            )} */}
            <MainPage/>
    </div>
  );
}

export default App;
