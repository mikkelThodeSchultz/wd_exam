import { loginUser, signupUser, resetPassword } from "./auth.js";

export const setupLoginForm = async () => {
    const loginForm = document.getElementById("loginForm");
    if(loginForm){
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault()
            const formData = new FormData(loginForm);
            try{
                const response = await loginUser(formData);
                if(response.status == 200){
                    localStorage.setItem("toastrMessage", "Welcome back!");
                    window.location.href = "/"
                } else {
                    toastr.warning("Wrong email or password")
                }
            } catch (error)  {
                console.log(error);
            }
        }) 
    }
} 

export const setupSignupForm = async () => {
    const signupForm = document.getElementById("signupForm");
    if(signupForm){
        signupForm.addEventListener("submit", async (e) => {
            e.preventDefault()
            const formData = new FormData(signupForm);
            try{
                const response = await signupUser(formData)
                if(response.status == 201){
                    localStorage.setItem("toastrMessage", "We have sent you an email, please verify your account and then log in");
                    window.location.href = "/login"
                } 
                if(response.status == 409){
                    toastr.warning("Email is already in use")
                }
            } catch (error) {
                console.log(error);
            }
        })
    }
}

export const setupResetPassword = async () => {
    const resetPasswordForm = document.getElementById("resetPasswordForm")
    if(resetPasswordForm){
        resetPasswordForm.addEventListener("submit", async (e) => {
            e.preventDefault()
            const formData = new FormData(resetPasswordForm)
            try{
                const response = await resetPassword(formData)
                if(response.status == 200){
                    localStorage.setItem("toastrMessage", "We have sent you an email with information as to how you can reset you're password");
                    window.location.href = "/login"
                }
                if(response.status == 404){
                    toastr.warning("The email is not in our system")
                }
            } catch (error) {
                console.log(error);
            }
        })
    }
}