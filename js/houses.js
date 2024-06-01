import { blockHouse, deleteHouse, deleteImage, editHouse, getCookie } from "./auth.js";



export const fetchHouses = async (user) => {
    try{
        //This is so that i can reuse the same method, both BE and FE, to fetch all the houses, or only the ones that is associated with a user. 
        const url = user ? `/house?user_pk=${user.user_pk}` : "/house";

        const response = await fetch(url)
        const data = await response.json()
        return data
    } catch (error) {
        console.log(error);
    }
}

export const addHouses = async (houses, user, containerId="houseContainer", isProfilePage=false) => {
    const houseContainer = document.getElementById(containerId)
    houses.forEach(house => {
        
        const houseCard = document.createElement("article")
        houseCard.classList.add("houseCard");

        const imageDetailsWrapper = document.createElement("div")
        imageDetailsWrapper.classList.add("imageDetailsWrapper")
        houseCard.appendChild(imageDetailsWrapper)

        const image = document.createElement("img")
        image.src = house.images[0]
        imageDetailsWrapper.appendChild(image);

        const details = document.createElement("div")
        details.classList.add("houseDetails");

        const name = document.createElement("h1");
        name.textContent = house.house_name;
        details.appendChild(name);

        const price = document.createElement("p");
        price.textContent = "Price per night: " + house.house_price_per_night;
        details.appendChild(price);
    
        const stars = document.createElement("p");
        stars.textContent = "Stars: " + house.house_stars;
        details.appendChild(stars);

        //Hides the house for everyone that is not an admin
        if (house.house_is_blocked == 1 && (!user || user.user_role !== "admin")) {
            houseCard.classList.add("hidden");
        } else {
            houseCard.classList.remove("hidden");
        }

        if(!isProfilePage && user){
            if(user.user_role != "admin"){
                const bookBtn = document.createElement("button");
                bookBtn.classList.add("bookBtn")
                bookBtn.textContent = "Book!"
                bookBtn.addEventListener("click", () => {
                    bookBtn.textContent = bookBtn.textContent === "Unbook" ? "Book!" : "Unbook";
                })
                houseCard.appendChild(bookBtn);
            }
            if(user.user_role == "admin"){
                const blockBtn = document.createElement("button")
                blockBtn.classList.add("blockBtn")
                blockBtn.textContent = house.house_is_blocked ? "Unblock!" : "Block"
                
                blockBtn.addEventListener("click", async () => {
                    try{
                        const response = await blockHouse(house)
                        if(response.status == 200){
                            toastr.success("House has been blocked")
                            blockBtn.textContent = blockBtn.textContent === "Unblock" ? "Block!" : "Unblock";
                            
                        }
                    } catch (error) {
                        console.log(error);
                    } 
                })
                houseCard.appendChild(blockBtn);
            }
        }
    
        imageDetailsWrapper.appendChild(details);
        if(houseContainer){
            houseContainer.appendChild(houseCard);
        }

        imageDetailsWrapper.addEventListener("click", () => openModal(house, isProfilePage));
    })
}

export const openModal = async (house, isProfilePage=false) => {
    const modal = document.getElementById("houseModal");
    // Stops the modal from closing when an image is deleted
    modal.addEventListener("click", (e) => {
        e.stopPropagation();
    });
    const modalHouseName = document.getElementById("modal-house-name");
    const modalHouseDescription = document.getElementById("modal-house-description");
    const modalHousePrice = document.getElementById("modal-house-price");
    const modalHouseStars = document.getElementById("modal-house-stars");
    const modalHouseImages = document.getElementById("modal-house-images");

    modalHouseImages.innerHTML = '';
    house.images.forEach(imageUrl => {
        const imageContainer = document.createElement("div");

        const img = document.createElement("img");
        img.src = imageUrl;

        if(isProfilePage){
            const deleteButton = document.createElement("button");
            deleteButton.textContent = "Delete";   
            deleteButton.setAttribute("type", "button");
            imageContainer.appendChild(deleteButton)
            deleteButton.addEventListener("click", async (e) => {
                e.preventDefault()
                e.stopPropagation()
                try{
                    const response = await deleteImage(house, imageUrl)
                    if(response.status==200){
                        imageContainer.remove();
                    } else {
                        toastr.warning("Something went wrong, please try again")
                    }
                } catch (error) {
                    console.log(error);
                }
            })
        }
        imageContainer.appendChild(img)
        modalHouseImages.appendChild(imageContainer);
    });

    modalHouseName.textContent = house.house_name;
    modalHouseDescription.textContent = house.house_description;
    modalHousePrice.textContent = "Price per night: " + house.house_price_per_night;
    modalHouseStars.textContent = "Stars: " + house.house_stars;
  
    if (isProfilePage) {
        const editHouseForm = document.getElementById("editHouseForm")
        const deleteHouseBtn = document.getElementById("deleteHouseBtn")
        editHouseForm.elements[0].value = house.house_name
        editHouseForm.elements[1].value = house.house_description
        editHouseForm.elements[2].value = house.house_price_per_night
        editHouseForm.elements[3].value = house.house_stars
        editHouseForm.addEventListener("submit", async (e) => {
            e.preventDefault()
            const formData = new FormData(editHouseForm)
            try{
                const response = await editHouse(formData, house)
                if (response.status == 200){
                    toastr.success("House has been updated")
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
        deleteHouseBtn.addEventListener("click", async (e) => {
            e.preventDefault()
            try {
                const response = await deleteHouse(house)
                if(response.status == 200){
                    toastr.success("House has been deleted")
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

    modal.style.display = "block";
}

//CloseModal function only for main page
const closeModal = async () => {
    const modal = document.getElementById("houseModal");
    modal.style.display = "none";

}

document.addEventListener('DOMContentLoaded', async () => {
    document.getElementsByClassName("close")[0].addEventListener("click", closeModal);
    const houses = await fetchHouses()
    const user = await getCookie()
    addHouses(houses, user);
});

