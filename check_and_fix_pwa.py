import os

# Set up the directory name for your PWA
project_name = "GarageSalePWA"
parent_directory = "/media/johndaniel/RedNAS1/PWA"  # Update this if your directory changes
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
    <title>Garage Sale Finder</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <link rel="stylesheet" href="src/css/styles.css">
</head>
<body>
    <div id="app">
        <h1>Garage Sale Finder</h1>
        <input type="text" id="searchInput" placeholder="Search for an address">
        <button onclick="searchAddress()">Search</button>
        <div id="map" style="height: 500px; width: 100%;"></div>

        <!-- Action buttons for the user's marker -->
        <div id="actions" style="margin-top: 20px;">
            <button onclick="editSale()">Edit Sale</button>
            <button onclick="deleteSale()">Delete Sale</button>
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
let sales = JSON.parse(localStorage.getItem('garageSales')) || [];

function initMap() {
    map = L.map('map').setView([51.505, -0.09], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Attempt to get user's location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const userLatLng = [position.coords.latitude, position.coords.longitude];
            map.setView(userLatLng, 13);
            L.marker(userLatLng).addTo(map).bindPopup('You are here').openPopup();
        }, () => {
            console.log('Geolocation not available');
        });
    }

    // Load existing garage sales
    sales.forEach(sale => {
        placeMarker(sale.latlng, sale.details);
    });

    // Add a click event listener to the map to allow users to add garage sale markers
    map.on('click', (e) => {
        if (!userMarker) {
            openAddSalePopup(e.latlng);
        } else {
            alert("You can only add one garage sale marker.");
        }
    });
}

function openAddSalePopup(latlng) {
    const formContent = `
        <div>
            <strong>Add Garage Sale</strong><br>
            <input type="text" id="saleAddress" placeholder="Enter Address"><br>
            <input type="text" id="saleTime" placeholder="Enter Time"><br>
            <textarea id="saleDescription" placeholder="Description"></textarea><br>
            <button onclick="saveSale('${latlng.lat}', '${latlng.lng}')">Save Sale</button>
        </div>
    `;
    L.popup()
        .setLatLng(latlng)
        .setContent(formContent)
        .openOn(map);
}

function saveSale(lat, lng) {
    const address = document.getElementById('saleAddress').value;
    const time = document.getElementById('saleTime').value;
    const description = document.getElementById('saleDescription').value;

    const saleDetails = {
        address: address,
        time: time,
        description: description
    };

    const sale = {
        latlng: { lat: lat, lng: lng },
        details: saleDetails
    };

    sales.push(sale);
    localStorage.setItem('garageSales', JSON.stringify(sales));

    // Place the marker on the map
    placeMarker(sale.latlng, sale.details);

    // Close the popup
    map.closePopup();

    // Set userMarker to prevent additional markers
    userMarker = L.marker(sale.latlng).addTo(map).bindPopup(`<strong>${saleDetails.address}</strong><br>${saleDetails.time}<br>${saleDetails.description}`);
}

function placeMarker(latlng, details) {
    const marker = L.marker(latlng).addTo(map);
    marker.bindPopup(`<strong>${details.address}</strong><br>${details.time}<br>${details.description}`);
}

function editSale() {
    if (userMarker) {
        const newAddress = prompt("Enter new address:", userMarker.getPopup().getContent().split('<br>')[0].replace('<strong>', '').replace('</strong>', ''));
        const newTime = prompt("Enter new time:", userMarker.getPopup().getContent().split('<br>')[1]);
        const newDescription = prompt("Enter new description:", userMarker.getPopup().getContent().split('<br>')[2]);
        
        if (newAddress && newTime && newDescription) {
            userMarker.setPopupContent(`<strong>${newAddress}</strong><br>${newTime}<br>${newDescription}`);
            updateSale(newAddress, newTime, newDescription);
        }
    } else {
        alert("You have no garage sale to edit.");
    }
}

function deleteSale() {
    if (userMarker) {
        map.removeLayer(userMarker);
        userMarker = null;
        localStorage.removeItem('garageSales');
        alert("Your garage sale has been deleted.");
    } else {
        alert("You have no garage sale to delete.");
    }
}

function updateSale(newAddress, newTime, newDescription) {
    sales = sales.map(sale => {
        if (sale.latlng.lat === userMarker.getLatLng().lat && sale.latlng.lng === userMarker.getLatLng().lng) {
            sale.details.address = newAddress;
            sale.details.time = newTime;
            sale.details.description = newDescription;
        }
        return sale;
    });
    localStorage.setItem('garageSales', JSON.stringify(sales));
}

// Initialize the map
document.addEventListener('DOMContentLoaded', initMap);
""",
    "manifest.json": """{
    "name": "Garage Sale Finder",
    "short_name": "GarageSales",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#317EFB",
    "icons": [
        {
            "src": "src/images/icon.png",
            "sizes": "192x192",
            "type": "image/png"
        }
    ]
}""",
    "service-worker.js": """self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('garage-sale-v1').then(cache => {
      return cache.addAll([
        '/',
        '/index.html',
        '/src/css/styles.css',
        '/src/js/app.js',
        '/manifest.json'
      ]);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});"""
}

# Create project directory if it doesn't exist
os.makedirs(project_path, exist_ok=True)

# Create subdirectories if they don't exist
for directory in directories:
    os.makedirs(os.path.join(project_path, directory), exist_ok=True)

# Create files if they don't exist
for filename, content in files.items():
    filepath = os.path.join(project_path, filename)
    if not os.path.exists(filepath):
        with open(filepath, 'w') as file:
            file.write(content)
        print(f"Created missing file: {filename}")

print(f"Project '{project_name}' has been checked and fixed successfully in '{project_path}'!")

