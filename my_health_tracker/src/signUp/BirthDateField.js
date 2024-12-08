import { useState } from "react";
import './BirthDateField.css';

function BirthDateField(){
    const [birthdate, setBirthdate] = useState(new Date());

    const validateAge = (event) => {
        const selectedDate = new Date(event.target.value);
        setBirthdate(selectedDate);
        
        const today = new Date();
        let age = today.getFullYear() - selectedDate.getFullYear();
        const monthDiff = today.getMonth() - selectedDate.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < selectedDate.getDate())) {
            age--;
        }

        event.target.setCustomValidity('');
    }
    return(
        <div className="row birthday">
            <div className="col-md-12">
                <label htmlFor="exampleDate" className="form-label birthday">Birthday</label>
                <span className='question-icon col-1'>
                    <i className="bi bi-question-circle"></i>
                    <span id="passwordHelpInline" className="signUp-helper-text">
                    We use your age to tailor your test results to a population similar to you.
                    </span>
                </span>
                <input type="date" className="form-control" id="exampleDate" onChange={validateAge} required></input>
            </div>
        </div>
    );
}

export default BirthDateField;