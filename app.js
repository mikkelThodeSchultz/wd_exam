import { setupAdminPage } from "./js/admin.js";
import { getCookie } from "./js/auth.js";
import { setupLoginForm, setupSignupForm, setupResetPassword } from "./js/index.js";
import { setUpProfilePage } from "./js/profile.js";
import { displayToastMessage } from "./js/toastHandler.js";

setupLoginForm()
setupSignupForm()
setupResetPassword()
setupAdminPage()
displayToastMessage()
const user = await getCookie()

toastr.options = {
    closeButton: true

};

const updateNavbar = async (user) => {
    const loggedOutLinks = document.getElementById("loggedOutLinks")
    const loggedInLinks = document.getElementById("loggedInLinks")
    const adminLink = document.getElementById("adminLink")
    const userRole = user ? user.user_role : null;

    if(userRole == "admin" || userRole == "customer" || userRole == "partner"){
        if(userRole == "admin"){
            adminLink.classList.add("shown")
            adminLink.classList.remove("hidden")
        }

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

await updateNavbar(user);
if(user){
    await setUpProfilePage(user)
} 

