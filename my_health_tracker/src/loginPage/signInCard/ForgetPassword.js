import React from 'react';
import '../LoginPage.css';

function ForgotPassword({onCreateAccount}){
    return (
        <>
          <p className="mt-3 text-center icon text-maroon">
              Don't have an account yet?
          </p>
          <div className="text-center">
            <button className="btn btn-outline-maroon w-100 icon" onClick={onCreateAccount}>
              <i className="fas fa-user-plus me-2"></i>Create New Account
            </button>
          </div>
        </>
      );
}
export default ForgotPassword;