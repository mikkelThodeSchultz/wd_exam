const loginForm = document.getElementById("loginForm");
loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
        const formData = new FormData(loginForm)
        const response = await fetch("/login", {
            method: 'POST',
            body: formData
        });

        console.log(response);
        if(!response.ok){
            console.log("no");
        }
        console.log("yes");
    } catch (error) {
        console.log(error);
    }
})