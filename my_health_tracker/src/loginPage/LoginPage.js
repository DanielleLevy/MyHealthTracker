import React, { useState } from 'react';
import './LoginPage.css';
import Welcome from './welcome/Welcome';
import SignInCard from './signInCard/SignInCard';

/* import UsersPasswordField from './usersPasswordField/UsersPasswordField';
import UsersEmailField from './usersEmailField/UsersEmailField';
import ErrorMessage from './errorMessage/ErrorMessage';
import LogInButton from './logInButton/LogInButton';
import NewAccountButton from './newAccountButton/NewAccountButton';
import ForgotPasswordLink from './forgotPasswordLink/ForgotPasswordLink';
import {useNavigate } from 'react-router-dom';
import LoginLogo from './loginLogo/LoginLogo'; */


function LoginPage({toggleForm, userData, setUserData, onCreateAccount}) {
    // const [email, setEmail] = useState(userData.Email || ''); //if user hasn't entered email, initilize as empty
    // const [password, setPassword] = useState('');
    // const [error, setError] = useState('');
    // const navigate = useNavigate();


// checks for the login. only signed up users can login
    // const handleLogin = (e) => {
    //     e.preventDefault();

    //     // Check if email and password match the user data
    //     if (email==userData.Email && password==userData.Password) {
    //         setUserData({
    //             "FirstName" : userData.FirstName,
    //             "LastName" : userData.LastName,
    //             "Email" : userData.Email,
    //             "Password" : userData.Password,
    //             "ProfilePhoto" : userData.ProfilePhoto,
    //             "IsLogIn" : true}
    //         )
    //         setError('');
    //         navigate('/feed');
    //     } else {
    //         // email or password incorrect
    //         setError('Email or password is incorrect');
    //     }
    // };

    return (
        <div className="container-fluid login-page d-flex justify-content-center align-items-center">
          <Welcome />
          <SignInCard onCreateAccount={onCreateAccount}/>
        </div>
      );
}

export default LoginPage;
