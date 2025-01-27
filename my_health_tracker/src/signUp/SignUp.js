import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; 
import "./SignUp.css";
import UsernameField from "./UsernameField";
import PasswordFields from "./PasswordFields";
import BirthDateField from "./BirthDateField";
import HeightWeightField from "./HeightWeightField";
import GenderField from "./GenderField";
import TitleSignUp from "./TitleSignUp";
import Welcome from "../loginPage/welcome/Welcome";

function SignUp({ onClose }) {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [passwordVerify, setPasswordVerify] = useState("");
    const [height, setHeight] = useState("");
    const [weight, setWeight] = useState("");
    const [age, setAge] = useState("");
    const [gender, setGender] = useState("");
    const [errorMessage, setErrorMessage] = useState(""); // הודעת שגיאה
    const navigate = useNavigate(); // ניווט לעמוד אחר

    const handleSignUp = async (e) => {
        e.preventDefault();

        if (password.length < 8 || password.length > 20) {
            setErrorMessage("Password must be between 8 and 20 characters.");
            return;
        }
        if (password !== passwordVerify) {
            setErrorMessage("Passwords do not match.");
            return;
        }

        try {
            const response = await axios.post("http://localhost:5001/api/signup", {
                username,
                password,
                height,
                weight,
                age,
                gender,
            });

            if (response.data.success) {
                console.log("User registered:", response.data.user);
                localStorage.setItem("username", username);
                navigate("/mainpage"); // מעבר לעמוד הראשי
            } else {
                setErrorMessage(response.data.message);
            }
        } catch (error) {
            console.error("Signup error:", error.response ? error.response.data : error.message);
            setErrorMessage(error.response ? error.response.data.message : "Server not reachable");
        }
    };

    return (
        <div className="container-fluid login-page d-flex justify-content-center align-items-center">
            <Welcome />
            <div className="form-box-signUp">
                <button type="button" id="btn-close" className="btn-close" aria-label="Close" onClick={onClose}></button>
                <TitleSignUp />
                <form className="needs-validation" onSubmit={handleSignUp}>
                    <UsernameField required setUsername={setUsername} />
                    <PasswordFields required setUserPassword={setPassword} setUserPasswordVerify={setPasswordVerify} />
                    <BirthDateField required setAge={setAge} />
                    <HeightWeightField required setWeight={setWeight} setHeight={setHeight} />
                    <GenderField option1="Male" option2="Female" option3="Other" required setGender={setGender} />
                    {errorMessage && <p className="text-danger">{errorMessage}</p>}
                    <button className="btn btn-success btn-sign" type="submit">Sign up</button>
                </form>
            </div>
        </div>
    );
}

export default SignUp;
