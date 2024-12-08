import React from 'react';
import './TitleSignUp.css';

function TitleSignUp(){
    return(
        <div>
            <div className="fw-bold titleSignup">Sign Up</div>
            <div className="fw-normal titleSignup" id="subtitle">It's quick and easy.</div>
            <div className="new-account row justify-content-center align-items-center">
                <div className="line" id="signUp-line"></div>
            </div>
        </div>
    );
}

export default TitleSignUp;