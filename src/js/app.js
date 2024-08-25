let map;
let userMarker = null;
let sales = [];
let broadcastInterval;

// Function to initialize the map
function initMap() {
    map = L.map('map').setView([51.505, -0.09], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Show the initial prompt to choose between buying or selling
    showBuyOrSellPrompt();
}

function showBuyOrSellPrompt() {
    const buyOrSellContent = `
        <div>
            <h2>What are you doing today?</h2>
            <button onclick="chooseBuy()">Buying</button>
            <button onclick="chooseSell()">Selling</button>
        </div>
    `;

    const popup = L.popup()
        .setLatLng(map.getCenter())
        .setContent(buyOrSellContent)
        .openOn(map);
}

function chooseBuy() {
    map.closePopup();
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const userLatLng = [position.coords.latitude, position.coords.longitude];
            map.setView(userLatLng, 13);
        }, () => {
            console.log('Geolocation not available');
        });
    }
}

function chooseSell() {
    map.closePopup();
    const sellContent = `
        <div>
            <h2>Enter Sale Details</h2>
            <input type="text" id="saleAddress" placeholder="Enter Address"><br>
            <textarea id="saleDescription" placeholder="Enter Description (Optional)"></textarea><br>
            <button onclick="startBeacon()">Start Sale Beacon</button>
        </div>
    `;
    const popup = L.popup()
        .setLatLng(map.getCenter())
        .setContent(sellContent)
        .openOn(map);
}

function startBeacon() {
    const address = document.getElementById('saleAddress').value;
    const description = document.getElementById('saleDescription').value;

    if (!address) {
        alert("Please enter an address to start the sale beacon.");
        return;
    }

    // Use the OpenCage Geocoding API to convert the address to latitude and longitude
    const apiKey = '7fb07eecb2cf4d01888939bab36021af';  // OpenCage API key
    const geocodingUrl = `https://api.opencagedata.com/geocode/v1/json?q=${encodeURIComponent(address)}&key=${apiKey}`;

    fetch(geocodingUrl)
        .then(response => response.json())
        .then(data => {
            if (data.results && data.results.length > 0) {
                const latLng = data.results[0].geometry;

                const saleDetails = {
                    address: address,
                    description: description,
                    latlng: { lat: latLng.lat, lng: latLng.lng }
                };

                // Save the sale details locally
                sales.push(saleDetails);

                // Place the marker on the map
                userMarker = L.marker([latLng.lat, latLng.lng]).addTo(map).bindPopup(`<strong>${address}</strong><br>${description}`).openPopup();

                // Broadcast the beacon every few seconds
                broadcastInterval = setInterval(() => {
                    broadcastSale(saleDetails);
                }, 5000);

                // Close the popup
                map.closePopup();
            } else {
                alert("Could not find the location. Please check the address and try again.");
            }
        })
        .catch(error => {
            console.error("Error fetching geocoding data: ", error);
            alert("There was an error processing the address. Please try again later.");
        });
}

// Function to broadcast the sale to other users (simulated with console log)
function broadcastSale(saleDetails) {
    console.log("Broadcasting sale: ", saleDetails);
    // TODO: Implement WebSocket or P2P broadcasting here
}

// Function to stop the beacon
function stopBeacon() {
    if (broadcastInterval) {
        clearInterval(broadcastInterval);
        broadcastInterval = null;
        alert("Your garage sale beacon has been stopped.");
    }
}

// Initialize the map
document.addEventListener('DOMContentLoaded', initMap);
