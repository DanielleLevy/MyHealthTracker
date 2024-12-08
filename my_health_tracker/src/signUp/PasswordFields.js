import React, { useState } from 'react';
import './PasswordFields.css';

function PasswordFields({setUserPassword, setUserPasswordVerify}){
    const [password, setPassword] = useState('');
    const [verifyPassword, setVerifyPassword] = useState('');
    const [passwordMatch, setPasswordMatch] = useState(true);

    // checks if the password fields match in every change in password field and set the new password
    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
        setUserPassword(e.target.value);
        checkPasswordMatch(e.target.value, verifyPassword);
    };

    // set the changed password in every change in the varify password field
    const handleVerifyPasswordChange = (e) => {
        const newPassword = e.target.value;
        setVerifyPassword(newPassword);
        setUserPasswordVerify(newPassword);

        // checks match after the changing
        if (password !== newPassword) {
            setPasswordMatch(false);
        } else {
            setPasswordMatch(true);
        }
    };

    // checks if the password fields match
    const checkPasswordMatch = (password, verifyPassword) => {
        if (password !== '' || verifyPassword !== '') {
            setPasswordMatch(password === verifyPassword);
        } else {
            setPasswordMatch(true);
        }
    };

    return(
        <div className="row mt-1">
            <div className="input-group-text col-md-12 d-flex">
                <input name="Password" type="password" className={`form-control ${(password.length >= 8 && password.length <= 20) ? 'is-valid' : (password.length > 0 || password.length > 20 ? 'is-invalid' : '')}`} placeholder="New password" aria-describedby="passwordHelpInline"
                    onChange={handlePasswordChange} required></input>
                    {/* question mark icon that help the user know the password requierments */}
                <span className='question-icon col-1'>
                    <i className="bi bi-question-circle"></i>
                    <span id="passwordHelpInline" className="signUp-helper-text">
                        Must be 8-20 characters long.
                    </span>
                </span>
            </div>
            {/* the label of the field changes according to user's input
            helps the user to know if his password is valid */}
            <label htmlFor="validationCustom03" className="signUp-helper-text">
                {password !== '' ? (password.length >= 8 && password.length <= 20 ? (<span className="text-success"></span>) : (password.length < 8 ?
                    (<span className="text-danger">Password too short</span>) :
                    (<span className="text-danger">Password too long</span>))) : ("")}
            </label>

                <div className="col-md-12 mt-1">
                    <input type="password" className={`form-control ${(passwordMatch && verifyPassword !== '') ? 'is-valid' : (verifyPassword !== '' ? 'is-invalid' : '')}`}
                        id="validationCustom03" placeholder='Password verify' value={verifyPassword}
                        onChange={handleVerifyPasswordChange} required ></input>
                        {/* the label of the field changes according to user's input
                        helps the user to know if his password verify match the entered password */}
                    <label htmlFor="validationCustom03" className="row form-label">
                        {verifyPassword !== '' ? (passwordMatch ? (
                            <span className="text-success">Passwords match!</span>) : (
                            <span className="text-danger">Passwords do not match</span>)) : ("")}
                    </label>
                </div>
        </div>
    );

}

export default PasswordFields;