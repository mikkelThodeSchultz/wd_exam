const fetchHouses = async () => {
    try{
        const response = await fetch("/house")
        const data = await response.json()
        return data
    } catch (error) {
        console.log(error);
    }
}

const createMap = async (houses) => {
    try {
        const response = await fetch("/mapbox_token")
        const mapbox_token = await response.text()
        mapboxgl.accessToken = mapbox_token
        var map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [12.5683, 55.6761],
            zoom: 12
        });
        houses.forEach(house => {
            var marker = new mapboxgl.Marker()
                .setLngLat([house.house_longitude, house.house_latitude])
                .addTo(map);

            marker.getElement().addEventListener('click', () => {
                openModal(house);
            });
        
        });
    } catch (error){
        console.log(error);
    }
}

const addHouses = async (houses) => {
    const houseContainer = document.getElementById("houseContainer")
    houses.forEach(house => {
        const houseCard = document.createElement("article")
        houseCard.classList.add("houseCard");

        const image = document.createElement("img")
        image.src = house.images[0]
        houseCard.appendChild(image);

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
    
        houseCard.appendChild(details);
        houseContainer.appendChild(houseCard);

        houseCard.addEventListener("click", () => openModal(house));
    })
}

const openModal = async (house) => {
    const modal = document.getElementById("houseModal");
    const modalHouseName = document.getElementById("modal-house-name");
    const modalHouseDescription = document.getElementById("modal-house-description");
    const modalHousePrice = document.getElementById("modal-house-price");
    const modalHouseStars = document.getElementById("modal-house-stars");
    const modalHouseImages = document.getElementById("modal-house-images");

    modalHouseImages.innerHTML = '';
    house.images.forEach(imageUrl => {
        const img = document.createElement("img");
        img.src = imageUrl;
        modalHouseImages.appendChild(img);
    });

    modalHouseName.textContent = house.house_name;
    modalHouseDescription.textContent = house.house_description;
    modalHousePrice.textContent = "Price per night: " + house.house_price_per_night;
    modalHouseStars.textContent = "Stars: " + house.house_stars;
  
    modal.style.display = "block";
}

const closeModal = async () => {
    const modal = document.getElementById("houseModal");
    modal.style.display = "none";
}

document.addEventListener('DOMContentLoaded', async () => {
    document.getElementsByClassName("close")[0].addEventListener("click", closeModal);
    const houses = await fetchHouses()
    createMap(houses);
    addHouses(houses);
});