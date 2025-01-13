import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; // לשימוש בניווט

function LoginForm() {
  const [username, setUsername] = useState(""); // שם משתמש
  const [password, setPassword] = useState(""); // סיסמה
  const [errorMessage, setErrorMessage] = useState(""); // הודעת שגיאה
  const navigate = useNavigate(); // ניווט לנתיב אחר

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      // קריאה ל-API של ההתחברות
      const response = await axios.post("http://localhost:5001/api/login", {
        username,
        password,
      });

      // אם ההתחברות הצליחה
      if (response.data.success) {
        console.log("User logged in:", response.data.user); // הצגת פרטי המשתמש בקונסולה
        localStorage.setItem("username", username); // שמירת שם המשתמש
        navigate("/mainpage"); // מעבר לעמוד MainPage
      } else {
        setErrorMessage(response.data.message); // הצגת הודעת שגיאה מה-API
      }
    } catch (error) {
      console.error("Login error:", error.response ? error.response.data : error.message);
      setErrorMessage(error.response ? error.response.data.message : "Server not reachable");
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <div className="mb-3 input-group">
        <span className="input-group-text bg-light-brown icon text-maroon">
          <i className="fas fa-user"></i>
        </span>
        <input
          type="text"
          className="form-control"
          placeholder="Enter your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
      </div>
      <div className="mb-3 input-group">
        <span className="input-group-text bg-light-brown icon text-maroon">
          <i className="fas fa-lock"></i>
        </span>
        <input
          type="password"
          className="form-control"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      {errorMessage && <p className="text-danger">{errorMessage}</p>}
      <div className="text-center">
        <button type="submit" className="btn btn-maroon icon w-100 mb-2">
          <i className="fas fa-sign-in-alt me-2"></i>Login
        </button>
      </div>
    </form>
  );
}

export default LoginForm;
