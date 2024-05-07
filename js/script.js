const loginForm = document.getElementById("loginForm");
loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
        const formData = new FormData(loginForm)
        console.log(formData.get("user_email"));
        const response = await fetch("/login", {
            method: 'POST',
            body: formData
        });
        
    } catch (error) {
        console.log(error);
    }
})