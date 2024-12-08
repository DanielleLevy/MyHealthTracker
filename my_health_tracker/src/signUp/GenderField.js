import React from 'react';
import './GenderField.css';

function GenderField({ option1, option2, option3 }) {
    return (
        <div className="check-box-gender">
            <label>Gender</label>
            <div className="col-md-12 d-flex justify-content-center">
                {/* Option 1 */}
                <div className="form-check btn-group align-items-center col-4" role="group">
                    <input
                        className="form-check-input"
                        type="radio"
                        name="gridRadios"
                        id="gridRadios1"
                        value="option1"
                    />
                    <label
                        className="form-check-label btn btn-outline-secondary gender-btn"
                        htmlFor="gridRadios1"
                    >
                        {option1}
                    </label>
                </div>
                {/* Option 2 */}
                <div className="form-check btn-group align-items-center col-4" role="group">
                    <input
                        className="form-check-input"
                        type="radio"
                        name="gridRadios"
                        id="gridRadios2"
                        value="option2"
                    />
                    <label
                        className="form-check-label btn btn-outline-secondary gender-btn"
                        htmlFor="gridRadios2"
                    >
                        {option2}
                    </label>
                </div>
                {/* Option 3 */}
                <div className="form-check btn-group align-items-center col-4" role="group">
                    <input
                        className="form-check-input"
                        type="radio"
                        name="gridRadios"
                        id="gridRadios3"
                        value="option3"
                    />
                    <label
                        className="form-check-label btn btn-outline-secondary gender-btn"
                        htmlFor="gridRadios3"
                    >
                        {option3}
                    </label>
                </div>
            </div>
        </div>
    );
}

export default GenderField;
