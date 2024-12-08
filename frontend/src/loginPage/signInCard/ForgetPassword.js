function ForgotPassword(){
    return (
        <>
          <p className="mt-3 text-center icon">
            <a href="#" className="link-maroon">
              <i className="fas fa-key me-2"></i>Forgot Password?
            </a>
          </p>
          <div className="text-center mt-4">
            <button className="btn btn-outline-maroon w-100 icon">
              <i className="fas fa-user-plus me-2"></i>Create an Account
            </button>
          </div>
        </>
      );
}
export default ForgotPassword;