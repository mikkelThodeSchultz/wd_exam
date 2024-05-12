import { verifyResetPasswordToken } from "./auth.js"

const url = new URL(window.location.href)
const searchParams = new URLSearchParams(url.search)
const token = searchParams.get("token")

const response = await verifyResetPasswordToken(token)
if(response && response.status == 200){

} else {
    
}