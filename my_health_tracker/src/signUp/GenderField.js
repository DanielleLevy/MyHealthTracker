import React, { useState } from "react";
import "./GenderField.css";

function GenderField({ option1, option2, option3, setGender }) {
    const [selectedGender, setSelectedGender] = useState(null); // שמירת הערך שנבחר

    const handleGenderChange = (e) => {
        const selectedValue = parseInt(e.target.value, 10); // המרה למספר
        setSelectedGender(selectedValue); // עדכון state מקומי
        setGender(selectedValue); // עדכון ה-state בטופס ההרשמה
    };

    return (
        <div className="check-box-gender">
            <label>Gender</label>
            <div className="col-md-12 d-flex justify-content-center">
                {/* Male (1) */}
                <div className="form-check btn-group align-items-center col-4" role="group">
                    <input
                        className="form-check-input"
                        type="radio"
                        name="gender"
                        id="gender1"
                        value="1"
                        checked={selectedGender === 1}
                        onChange={handleGenderChange}
                    />
                    <label className="form-check-label btn btn-outline-secondary gender-btn" htmlFor="gender1">
                        {option1}
                    </label>
                </div>
                {/* Female (2) */}
                <div className="form-check btn-group align-items-center col-4" role="group">
                    <input
                        className="form-check-input"
                        type="radio"
                        name="gender"
                        id="gender2"
                        value="2"
                        checked={selectedGender === 2}
                        onChange={handleGenderChange}
                    />
                    <label className="form-check-label btn btn-outline-secondary gender-btn" htmlFor="gender2">
                        {option2}
                    </label>
                </div>
                {/* Other (0) */}
                <div className="form-check btn-group align-items-center col-4" role="group">
                    <input
                        className="form-check-input"
                        type="radio"
                        name="gender"
                        id="gender3"
                        value="0"
                        checked={selectedGender === 0}
                        onChange={handleGenderChange}
                    />
                    <label className="form-check-label btn btn-outline-secondary gender-btn" htmlFor="gender3">
                        {option3}
                    </label>
                </div>
            </div>
        </div>
    );
}

export default GenderField;
