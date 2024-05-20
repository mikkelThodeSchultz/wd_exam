import { blockUser, getUsers } from "./auth.js";

export const setupAdminPage = async () => {
    const users = await getUsers()
    
    const listOfUsers = document.getElementById("listOfUsers");
    listOfUsers.innerHTML = "";

    users.forEach(user => {
        const userContainer = document.createElement("div");
        userContainer.classList.add("user");

        const userName = document.createElement("p");
        userName.textContent = `Name: ${user.user_username}`;
        const userEmail = document.createElement("p");
        userEmail.textContent = `Email: ${user.user_email}`;
        const userRole = document.createElement("p");
        userRole.textContent = `Role: ${user.user_role}`;
        const userCreatedAt = document.createElement("p");
        userCreatedAt.textContent = `Created At: ${new Date(user.user_created_at * 1000).toLocaleString()}`;
        const userUpdatedAt = document.createElement("p");
        userUpdatedAt.textContent = `Updated At: ${user.user_updated_at ? new Date(user.user_updated_at * 1000).toLocaleString() : "Not updated"}`;
        const userIsVerified = document.createElement("p");
        userIsVerified.textContent = `Verified: ${user.user_is_verified ? 'Yes' : 'No'}`;

        const blockButton = document.createElement("button");
        blockButton.textContent = `${user.user_is_blocked ? 'Unblock' : 'Block'}`
        blockButton.addEventListener("click", async () => {
            try{
                const response = await blockUser(user.user_pk);
                if(response.status == 200) {
                    toastr.success(`User has been ${blockButton.textContent.toLowerCase()}ed`);
                    blockButton.textContent = blockButton.textContent === "Block" ? "Unblock" : "Block";
                }
            } catch (error){
                console.log(error);
            }
            
        });

        userContainer.appendChild(userName);
        userContainer.appendChild(userEmail);
        userContainer.appendChild(userRole);
        userContainer.appendChild(userCreatedAt);
        userContainer.appendChild(userUpdatedAt);
        userContainer.appendChild(userIsVerified);
        userContainer.appendChild(blockButton);

        listOfUsers.appendChild(userContainer);
    })
}

