import { verifyResetPasswordToken } from "./auth.js"

const url = new URL(window.location.href)
const searchParams = new URLSearchParams(url.search)
const token = searchParams.get("token")

if(!token){
    window.location.href = "/"
}
const resetForm = document.getElementById("resetPasswordForm")
if(resetForm){
    resetForm.addEventListener("submit", async (e) => {
        e.preventDefault()
        const formData = new FormData(resetForm)
        try{
            const response = await verifyResetPasswordToken(token, formData)
            if(response && response.status == 200){
                localStorage.setItem("toastrMessage", "Password have been updated");
                window.location.href = "/login"
            } else {
                toastr.warning("You're token has expired")
            }
        } catch (error) {
            console.log(error);
        }
    })
}

