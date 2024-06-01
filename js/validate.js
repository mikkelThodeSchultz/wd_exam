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

export const verifyFormdata = (formData) => {
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

export const verifyHouseFormData = (formData) => {
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

