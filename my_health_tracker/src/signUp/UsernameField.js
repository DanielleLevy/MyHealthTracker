function UsernameField({}){
    return(
        <div className="row">
            <div className="col-12 username-field">
                <label htmlFor="username" className="form-label"></label>
                <input type="text" className="form-control" id="username" name="username" placeholder="Username" required/> 
                <div className="invalid-feedback">
                    Please enter a username.
                    </div>
            </div>
        </div>

    );
}

export default UsernameField;