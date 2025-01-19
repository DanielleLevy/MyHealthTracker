import React from "react";

function UsernameField({ setUsername }) {
    const handleUsernameChange = (e) => {
        setUsername(e.target.value); // עדכון השם משתמש ב-state של ההרשמה
    };

    return (
        <div className="row">
            <div className="col-12 username-field">
                <label htmlFor="username" className="form-label"></label>
                <input
                    type="text"
                    className="form-control"
                    id="username"
                    name="username"
                    placeholder="Username"
                    required
                    onChange={handleUsernameChange} // קריאה לפונקציה בעת שינוי הקלט
                />
                <div className="invalid-feedback">Please enter a username.</div>
            </div>
        </div>
    );
}

export default UsernameField;
