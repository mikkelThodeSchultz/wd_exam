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

const verifyFormdata = (formData) => {
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
    if(formData.get("user_password_2")){
        const password = formData.get("user_password")
        const password2 = formData.get("user_password_2")
        if(password != password2){
            toastr.warning("Passwords do not match. Please make sure your passwords match before proceeding")
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

export const editProfile = async (formData) => {
    if(!verifyFormdata(formData)){
        return
    }
    try {
        const response = await fetch("/user", {
            method: 'PUT',
            body: formData
        });
        return response
    } catch (error) {
        throw new Error("Edit profile failed: " + error)
    }
}

export const deleteProfile = async (formData) => {
    if(!verifyFormdata(formData)){
        return
    }
    try{
        const response = await fetch("/user", {
            method: 'DELETE',
            body: formData
        });
        return response
    } catch (error) {
        throw new Error("Delete profile failed: " + error)
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

export const verifyResetPasswordToken = async (token, formData) => {
    if(!token){
        return
    }
    if(!verifyFormdata(formData)){
        return
    }
    try{
        const response = await fetch(`/verify-reset-password?token=${encodeURIComponent(token)}`, {
            method: 'POST',
            body: formData
        })
        return response
    } catch (error) {
        throw new Error("Password reset failed : " + error)
    }
}

export const getUser = async () => {
    try{
        const response = await fetch("/cookie", {
            method: "GET"
        })
        if(response.status==200){
            const cookieValue = await response.json()
            return cookieValue
        }
    } catch (error) {
        throw new Error("Error getting cookie: " + error)
    }
}

export const getUsers = async () => {
    try {
        const response = await fetch("/user", {
            method: "GET"
        })
        if(response.status==200){
            const users = await response.json()
            return users
        }
    } catch (error) {
        throw new Error("Error getting users: " + error)
    }
}

export const blockUser = async (user_pk) => {
    try {
        const url = "/user?user_pk=" + user_pk
        const response = await fetch(url, {
            method: 'PUT'
        })
        return response
    } catch (error) {
        throw new Error("Error updating ")
    }
}

export const deleteImage = async (house, imageUrl) => {
    if(!house || !imageUrl){
        return
    }
    try {
        const response = await fetch(`/image?house_pk=${house.house_pk}&imageUrl=${imageUrl}`, {
        method: 'DELETE'
        })
        return response
    } catch (error) {
        console.log(error);
    }
}

export const editHouse = async (formData, house) => {
    if(!verifyHouseFormData(formData)){
        return
    }
    if(!house.house_pk){
        return
    }
    try{
        const response = await fetch(`/house?house_pk=${house.house_pk}`, {
            method: 'PUT',
            body: formData
        })
        return response
    } catch (error) {
        console.log(error);
    }
}

export const blockHouse = async (house) => {
    if(!house.house_pk){
        return
    }
    try{
        const response = await fetch(`/house?house_pk=${house.house_pk}&house_block=true`, {
            method: 'PUT'
        })
        return response
    } catch (error) {
        console.log(error);
    }

}

export const deleteHouse = async (house) => {
    if(!house.house_pk){
        return
    }
    try{
        const response = await fetch(`/house?house_pk=${house.house_pk}`, {
            method: 'DELETE'
        })
        return response
    } catch (error) {
        console.log(error);
    }
}

export const createHouse = async (formData, user) => {
    if(!verifyHouseFormData(formData)){
        return
    }
    if(!user){
        return
    }
    try{
        const response = await fetch(`/house?user_pk=${user.user_pk}`, {
            method: 'POST',
            body: formData
        })
        return response
    } catch (error) {
        console.log(error);
    }
}




const verifyHouseFormData = (formData) => {
    const images = formData.getAll("image")
    const maxSizeInBytes = 5 * 1024 * 1024
    const houseName = formData.get("house_name");
    const houseDescription = formData.get("house_description");
    const housePricePerNight = formData.get("house_price_per_night");
    const houseStars = formData.get("house_stars");
    const houseLatitude = formData.get("house_latitude");
    const houseLongitude = formData.get("house_longitude")

    if(houseName=="" || houseDescription=="" || housePricePerNight=="" || houseStars=="" || houseLatitude=="" || houseLongitude==""){
        toastr.warning("Please fill out all fields")
        return false
    }

    if(images.length < 0){
        for (const image of images) {
            if (!image.type.startsWith('image/')) {
                toastr.warning("Please only upload images");
                return false;
            }
            if (image.size > maxSizeInBytes) {
                toastr.warning("Image is too big (5MB)");
                return false;
            }
        }
    }

    if(isNaN(houseLatitude)){
        toastr.warning("Latitude must be a number")
        return false
    }

    if(isNaN(houseLongitude)){
        toastr.warning("Longitude must be a number")
        return false
    }

    if (!(houseLatitude >= -90 && houseLatitude <= 90)) {
        toastr.warning("Latitude must be between -90 and 90")
        return false;
    }

    if (!(houseLongitude >= -180 && houseLongitude <= 180)) {
        toastr.warning("Longitude must be between -180 and 180")
        return false
    }
        
    if (houseName.length > 20) {
        toastr.warning("House name must be 20 characters or less");
        return false;
    }

    if (houseDescription.length > 500) {
        toastr.warning("House description must be 500 characters or less");
        return false;
    }

    if (isNaN(housePricePerNight)) {
        toastr.warning("Price per night must be a number");
        return false;
    }

    if (houseStars < 0 || houseStars > 5) {
        toastr.warning("Stars must be between 0 and 5");
        return false;
    }

    return true;
}