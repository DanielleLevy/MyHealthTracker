import React from "react";
import LoginForm from "./LoginForm";
import "./SignInCard.css";
import ForgetPassword from "./ForgetPassword";

function SignInCard({onCreateAccount}){
    return (
        <div className="card login-card shadow">
            <h2 className="text-center mb-4 text-maroon icon">Log In</h2>
            <LoginForm />
            <ForgetPassword onCreateAccount={onCreateAccount}/>
        </div>
      );
}
export default SignInCard;