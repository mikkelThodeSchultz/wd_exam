
const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
const PASSWORD_REGEX = /.{4,}/;
const USERNAME_REGEX = /.{4,}/;

function validateEmail(email){
    return EMAIL_REGEX.test(email);
}
function validatePassword(password){
    return PASSWORD_REGEX.test(password);
}
function validateUsername(username){
    return USERNAME_REGEX.test(username)
}

function verifyFormdata(formData){
    if(formData.get('user_email')){
        const email = formData.get('user_email');
        if(!validateEmail(email)){
            toastr.warning("Invalid email format")
            return false;
        }
    }
    if(formData.get('user_password')){
        const password = formData.get('user_password');
        if(!validatePassword(password)){
            toastr.warning("Password must be at least 4 characters long")
            return false;
        }
    }
    if(formData.get('user_username')){
        const username = formData.get('user_username')
        if(!validateUsername(username)){
            toastr.warning("Username must be at least 4 characters long")
            return false
        }
    }
    return true
}

export const loginUser = async (formData) => {
    if(!verifyFormdata(formData)){
        return
    }
    try {
        const response = await fetch("/login", {
            method: 'POST',
            body: formData
        });
        return response
    } catch (error) {
        throw new Error("Login failed: " + error)
    }
}

export const signupUser = async (formData) => {
    if(!verifyFormdata(formData)){
        return
    }
    try{
        const response = await fetch("/signup", {
            method: 'POST',
            body: formData
        });
        return response
    } catch (error) {
        throw new Error("Signup failed: " + error)
    }
}

export const verifyAccount = async (token) => {
    if(!token){
        return
    }
    try{
        const response = await fetch(`/verify-account?token=${encodeURIComponent(token)}`, {
            method: 'POST'
        })
        return response
    } catch (error) {
        throw new Error("Verify account failed: " + error)
    }
}

export const resetPassword = async (formData) => {
    if(!verifyFormdata(formData)){
        return
    }
    try{
        const response = await fetch("/reset-password", {
            method: 'POST',
            body: formData
        });
        return response
    } catch (error) {
        throw new Error("Reset password failed: " + error)
    }
}

export const verifyResetPasswordToken = async (token) => {
    if(!token){
        return
    }
    try{
        const response = await fetch(`/verify-reset-password?token=${encodeURIComponent(token)}`, {
            method: 'POST'
        })
        return response
    } catch (error) {
        throw new Error("Password reset failed : " + error)
    }
}