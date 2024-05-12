import { setupLoginForm, setupSignupForm, setupResetPassword } from "./js/index.js";
import { displayToastMessage } from "./js/toastHandler.js";

setupLoginForm()
setupSignupForm()
setupResetPassword()
displayToastMessage()

toastr.options = {
    closeButton: true
};

