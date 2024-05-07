const loginForm = document.getElementById("loginForm");
loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
        const formData = new FormData(loginForm)
        const response = await fetch("/login", {
            method: 'POST',
            body: formData
        });

        //TODO Handle response and make front end validation
        console.log(response);
        
    } catch (error) {
        console.log(error);
    }
})