import React, { useState } from "react";

function LoginForm({}){
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
};

    return (
        <form>
          <div className="mb-3 input-group">
            <span className="input-group-text bg-light-brown icon text-maroon">
              <i className="fas fa-user"></i>
            </span>
            <input
              type="text"
              className="form-control"
              id="username"
              placeholder="Enter your username"
              required
            />
          </div>
          <div className="mb-3 input-group">
            <span className="input-group-text bg-light-brown icon text-maroon">
              <i className="fas fa-lock"></i>
            </span>
            <input
              type={showPassword ? "text" : "password"}
              className="form-control"
              id="password"
              placeholder="Enter your password"
              required
              onChange={(e) => setPassword(e.target.value)}
            />
            {password.length>0 &&(
                <button className="btn show-password-btn col-1" type="button" onClick={togglePasswordVisibility}>
                    <i class={showPassword ? "bi bi-eye-slash" : "bi bi-eye"} ></i>
                </button>
            )}
          </div>
          <div className="text-center">
            <button type="submit" className="btn btn-maroon icon w-100 mb-2">
              <i className="fas fa-sign-in-alt me-2"></i>Login
            </button>
          </div>
        </form>
      );
}
export default LoginForm;