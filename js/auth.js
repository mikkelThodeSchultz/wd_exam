import { verifyFormdata, verifyHouseFormData } from "./validate.js";


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

export const getCookie = async () => {
    try{
        const response = await fetch("/cookie", {
            method: "GET"
        })
        if(response.status==200){
            const cookieValue = await response.json()
            return cookieValue
        }
        if(response.status==404){
            return null
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



