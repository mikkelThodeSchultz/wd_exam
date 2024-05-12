import { verifyAccount } from "./auth.js"


const url = new URL(window.location.href)
const searchParams = new URLSearchParams(url.search)
const token = searchParams.get("token")

const response = await verifyAccount(token)
if(response && response.status == 200){
    localStorage.setItem("toastrMessage", "Account has been verified, please sign in");
    window.location.href = "/login"
} else {
    window.location.href = "/login"
}

