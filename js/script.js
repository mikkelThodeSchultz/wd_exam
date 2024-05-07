const loginForm = document.getElementById("loginForm");
loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
        const formData = new FormData(loginForm)
        const response = await fetch("/https://mikkelthodeschultz.pythonanywhere.com/login", {
            method: 'POST',
            body: formData
        });
        
    } catch (error) {
        console.log(error);
    }
})