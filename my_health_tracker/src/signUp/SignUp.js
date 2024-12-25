import React, { useState } from 'react';
import './SignUp.css';
import NameField from './NameField';
import UsernameField from './UsernameField';
import PasswordFields from './PasswordFields';
import BirthDateField from './BirthDateField';
import HeightWeightField from './HeightWeightField';
import GenderField from './GenderField';
import TitleSignUp from './TitleSignUp';
import Welcome from '../loginPage/welcome/Welcome';

/* import UsersPasswordField from './usersPasswordField/UsersPasswordField';
import UsersEmailField from './usersEmailField/UsersEmailField';
import ErrorMessage from './errorMessage/ErrorMessage';
import LogInButton from './logInButton/LogInButton';
import NewAccountButton from './newAccountButton/NewAccountButton';
import ForgotPasswordLink from './forgotPasswordLink/ForgotPasswordLink';
import {useNavigate } from 'react-router-dom';
import LoginLogo from './loginLogo/LoginLogo'; */


function SignUp({ onClose }) {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [passwordVerify, setPasswordVerify] = useState('');
    const [height, setHeight] = useState('');
    const [weight, setWeight] = useState('');
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('');

    async function handleSignUp(e) {
        e.preventDefault();
        if (password.length < 8 || password.length > 20) {
            return;
        }
        if (password !== passwordVerify) {
            return;
        }
        const newUser = {
            firstName,
            lastName,
            username,
            password,
            height,
            weight,
            gender,
            age,
        };
        console.log(newUser);
    }

    return (
        <div className="container-fluid login-page d-flex justify-content-center align-items-center">
          <Welcome />
          <div className="form-box-signUp">
                <button type="button" id="btn-close" className="btn-close" aria-label="Close" onClick={onClose}></button>
                <TitleSignUp />
                <form className="needs-validation" onSubmit={handleSignUp}>
                    <NameField required setFirstName={setFirstName} setLastName={setLastName} />
                    <UsernameField required username={setUsername} />
                    <PasswordFields required setUserPassword={setPassword} setUserPasswordVerify={setPasswordVerify} />
                    <BirthDateField required setAge={setAge} />
                    <HeightWeightField required setWeight={setWeight} setHeight={setHeight} />
                    <GenderField option1="Female" option2="Male" option3="Other" required setGender={setGender} />
                    <button className="btn btn-success btn-sign" type="submit">Sign up</button>
                </form>
            </div>
        </div>
      );
}

export default SignUp;
