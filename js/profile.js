import { editProfile, deleteProfile, createHouse } from "./auth.js"
import { addHouses, fetchHouses } from "./houses.js"

export const setUpProfilePage = async (user) => {
    const welcome = document.getElementById("profileWelcome")
    const username = document.getElementById("profileUsername")
    const email = document.getElementById("profileEmail")

    if(welcome){
        welcome.textContent = `Hello ${user.user_username}!`
        username.textContent = "Username: " + user.user_username
        email.textContent = "Email: " + user.user_email
    }

    if(user.user_role === "partner"){
        const houses = await fetchHouses(user)
        await addHouses(houses, user, "profileHouseContainer", true);

        const closeBtns = document.getElementsByClassName("close")
        Array.from(closeBtns).forEach(closeBtn => {
            closeBtn.addEventListener("click", () => {
                closeModal()
            })
        })
        await createHouseForm(user)
    }



    const editProfileModal = document.getElementById("editProfileModal");
    const deleteProfileModal = document.getElementById("deleteProfileModal");  

    const editBtn = document.getElementById("editProfileBtn")
    const deleteBtn = document.getElementById("deleteProfileBtn")

    const closeEditModalBtn = editProfileModal.querySelector(".close");
    const closeDeleteModalBtn = deleteProfileModal.querySelector(".close");

    editBtn.addEventListener("click", () => {
        editProfileModal.style.display = "block";
    });

    closeEditModalBtn.addEventListener("click", () => {
        editProfileModal.style.display = "none";
    });

    deleteBtn.addEventListener("click", () => {
        deleteProfileModal.style.display = "block";
    });

    closeDeleteModalBtn.addEventListener("click", () => {
        deleteProfileModal.style.display = "none";
    });

    const editProfileForm = document.getElementById("editProfileForm")
    const deleteProfileForm = document.getElementById("deleteProfileForm")

    const placeholderUsername = document.getElementById("placeholderUsername")
    const placeholderEmail = document.getElementById("placeholderEmail")
    placeholderUsername.value = user.user_username
    placeholderEmail.value = user.user_email

    if(editProfileForm){
        editProfileForm.addEventListener("submit", async (e) => {
            e.preventDefault()
            const formData = new FormData(editProfileForm)
            try{
                const response = await editProfile(formData)
                if(response.status == 200){
                    toastr.success("You're account has been updated!")
                    setTimeout( () => {
                        location.reload()
                    }, 2000)
                } else {
                    toastr.warning("Something went wrong, please try again")
                }
            } catch (error) {
                console.log(error);
            }
        })
    }

    if(deleteProfileForm){
        deleteProfileForm.addEventListener("submit", async (e) => {
            e.preventDefault()
            try{
                const formData = new FormData(deleteProfileForm)
                const response = await deleteProfile(formData)
                if(response.status == 200){
                    toastr.success("You're account has been deleted, goodbye!")
                    setTimeout( () => {
                        window.location.href = "/"
                    }, 2000)
                } else {
                    toastr.warning("Something went wrong, please try again")
                }
            } catch (error) {
                console.log(error);
            }
        })
    }

}

//CloseModal function only for profile page
const closeModal = async () => {
    // location.reload()
    const modal = document.getElementById("houseModal");
    modal.style.display = "none";
}

const createHouseForm = async (user) => {
    const form = document.createElement('form');
    form.id = 'createHouseForm';

    const header = document.createElement('h2')
    header.innerText = "Upload a new house!"
    form.appendChild(header)

    const nameInput = document.createElement('input');
    nameInput.type = 'text';
    nameInput.placeholder = 'name';
    nameInput.name = 'house_name';
    form.appendChild(nameInput);

    const descriptionTextArea = document.createElement('textarea');
    descriptionTextArea.classList.add('houseDescriptionTextArea');
    descriptionTextArea.placeholder = 'description';
    descriptionTextArea.name = 'house_description';
    form.appendChild(descriptionTextArea);

    const priceInput = document.createElement('input');
    priceInput.type = 'text';
    priceInput.placeholder = 'price per night';
    priceInput.name = 'house_price_per_night';
    form.appendChild(priceInput);

    const starsInput = document.createElement('input');
    starsInput.type = 'text';
    starsInput.placeholder = 'stars';
    starsInput.name = 'house_stars';
    form.appendChild(starsInput);

    const latitudeInput = document.createElement('input')
    latitudeInput.type = 'text'
    latitudeInput.placeholder = 'latitude'
    latitudeInput.name = 'house_latitude'
    form.appendChild(latitudeInput)

    const longitudeInput = document.createElement('input')
    longitudeInput.type = 'text'
    longitudeInput.placeholder = 'longitude'
    longitudeInput.name = 'house_longitude'
    form.appendChild(longitudeInput)

    const imageInput = document.createElement('input');
    imageInput.type = 'file';
    imageInput.name = 'image';
    imageInput.accept = 'image/*';
    imageInput.multiple = true;
    form.appendChild(imageInput);

    const submitButton = document.createElement('button');
    submitButton.type = 'submit';
    submitButton.textContent = 'Upload house';
    form.appendChild(submitButton);

    const container = document.getElementById('profileCreateHouseContainer');
    if(container){
        container.appendChild(form);
    }

    form.addEventListener("submit", (e) => handleCreateHouseFormSubmit(form, user, e))
}

const handleCreateHouseFormSubmit = async (form, user ,e) => {
    e.preventDefault();
    try {
        const formData = new FormData(form);
        const response = await createHouse(formData, user);
        if (response.status == 200) {
            toastr.success("Your house has been created");
            setTimeout(() => {
                window.location.href = "/";
            }, 2000);
        } else {
            toastr.warning("Something went wrong, please try again");
        }
    } catch (error) {
        console.log(error);
    }
};