import os

# Set up the directory name for your PWA
project_name = "GarageSalePWA"
parent_directory = "/media/johndaniel/RedNAS1/PWA"  # Update this path if necessary
project_path = os.path.join(parent_directory, project_name)

# Directory structure
directories = [
    "src",
    "src/assets",
    "src/css",
    "src/js",
    "src/images",
]

# Basic files and their contents
files = {
    "index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JD's Garage Sale Finder</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <link rel="stylesheet" href="src/css/styles.css">
</head>
<body>
    <div id="app">
        <h1>JD's Garage Sale Finder</h1>
        <input type="text" id="searchInput" placeholder="Search for an address">
        <button onclick="searchAddress()">Search</button>
        <div id="map" style="height: 500px; width: 100%;"></div>

        <!-- Action buttons for the user's marker -->
        <div id="actions" style="margin-top: 20px;">
            <button onclick="stopBeacon()">Stop Sale Beacon</button>
        </div>
    </div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script src="src/js/app.js"></script>
</body>
</html>
""",
    "src/css/styles.css": """body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}

#app {
    max-width: 1200px;
    margin: auto;
    padding: 20px;
}

button {
    padding: 10px;
    margin-top: 10px;
}""",
    "src/js/app.js": """let map;
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

    const latLng = map.getCenter();

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
"""
}

# Create project directory if it doesn't exist
os.makedirs(project_path, exist_ok=True)

# Create subdirectories if they don't exist
for directory in directories:
    os.makedirs(os.path.join(project_path, directory), exist_ok=True)

# Create files if they don't exist
for filename, content in files.items():
    filepath = os.path.join(project_path, filename)
    with open(filepath, 'w') as file:
        file.write(content)
    print(f"Updated file: {filename}")

print(f"Project '{project_name}' has been updated successfully in '{project_path}'!")

