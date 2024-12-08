function NameField({setFirstName, setLastName}){
    return(
        <div className="row">
            <div className="col-md-6 d-flex form-field">
                <label for="validationCustom01" className="form-label"></label>
                <input type="text" className="form-control" placeholder="First Name" required onChange={(e) => setFirstName(e.target.value)}></input>
            </div>

            <div className="col-md-6 d-flex form-field">
                <label for="validationCustom01" className="form-label"></label>
                <input type="text" className="form-control" placeholder="Last Name" required onChange={(e) => setLastName(e.target.value)}></input>
            </div>
        </div>

    );
}

export default NameField;