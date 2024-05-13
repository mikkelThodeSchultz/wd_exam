import { getUser } from "./js/auth.js";
import { setupLoginForm, setupSignupForm, setupResetPassword } from "./js/index.js";
import { displayToastMessage } from "./js/toastHandler.js";

setupLoginForm()
setupSignupForm()
setupResetPassword()
displayToastMessage()

toastr.options = {
    closeButton: true
};

const updateNavbar = async () => {
    const loggedOutLinks = document.getElementById("loggedOutLinks")
    const loggedInLinks = document.getElementById("loggedInLinks")
    const user = await getUser()
    const userRole = user.user_role
    if(userRole == "admin" || userRole == "customer" || userRole == "partner"){
        loggedInLinks.classList.add("shown")
        loggedInLinks.classList.remove("hidden")

        loggedOutLinks.classList.add("hidden")
        loggedOutLinks.classList.remove("shown")
    } else {
        loggedInLinks.classList.remove("shown")
        loggedInLinks.classList.add("hidden")

        loggedOutLinks.classList.remove("hidden")
        loggedOutLinks.classList.add("shown") 
    }
}

await updateNavbar();