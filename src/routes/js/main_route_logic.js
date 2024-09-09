import {ZOOM_IN_URL, ZOOM_OUT_URL} from './envs.js';

var openstreetAttr = '&copy; <a href="https://github.com/juanvilla23/Medallo-Oculto">Medallo Oculto</a>'; 
var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var markersGroup = new L.FeatureGroup();
var bounds = [
    [6.1442, -75.6812], // Suroeste
    [6.3442, -75.4812]  // Noreste
];

var selectedRouteType = 'foot'; // Valor por defecto para el tipo de ruta
var markers = [];
var selectedMarkers = []; // Para almacenar los marcadores seleccionados para la ruta
var routeControl = null; // Inicializar routeControl como null
var map;

window.onload = function() {
    
    map = L.map('map', {
        center: [6.2442, -75.5812], // Centro del mapa
        zoom: 13, // Zoom inicial
        minZoom: 10, // Zoom out mínimo
        maxZoom: 18, // Zoom in máximo
        maxBounds: bounds, // Limita el área navegable al Valle de Aburrá
        maxBoundsViscosity: 1.0,
        zoomControl: false,
        attributionControl: false, // Desactiva el control de atribución predeterminado

        contextmenu: true, // Activa el menú contextual que se activa con click derecho
        contextmenuWidth: 140,
        contextmenuItems: [{
            text: 'Mostrar coordenadas',
            callback: showCoordinates
        }, {
            text: 'Centrar mapa aquí',
            callback: centerMap
        }, '-', {
            text: 'Zoom in',
            icon: ZOOM_IN_URL,
            callback: zoomIn
        }, {
            text: 'Zoom out',
            icon: ZOOM_OUT_URL,
            callback: zoomOut
        }, '-', {
            text: 'Crear marcador aquí',
            callback: createMarker // Añadir el nuevo item para crear un marcador
        }, '-', {
            text: 'Crear ruta',
            callback: drawRoute // Añadir el nuevo item para crear un marcador
        }]
    });

    // Añadir el grupo de marcadores al mapa
    markersGroup.addTo(map);

    function showCoordinates (e) {
        alert(e.latlng);
    }
    
    function centerMap (e) {
        map.panTo(e.latlng);
    }
    
    function zoomIn (e) {
        map.zoomIn();
    }
    
    function zoomOut (e) {
        map.zoomOut();
    }
    
    function createMarker(e) {
        var marker = L.marker(e.latlng).addTo(markersGroup);
        marker.bindPopup("Marcador en: " + e.latlng.toString()).openPopup();
        markers.push(marker);
    }

    var openstreetmap = L.tileLayer(osmUrl, { 
        attribution: openstreetAttr,
        minZoom: 10, // Asegura que la capa de mosaicos respete el zoom mínimo
        maxZoom: 18  // Asegura que la capa de mosaicos respete el zoom máximo
    }).addTo(map);

    L.control.attribution({ prefix: false }) // Elimina la atribución de Leaflet
        .addAttribution(openstreetAttr) // Agrega tu propia atribución
        .addTo(map);

    L.control.zoom({ position : 'bottomright' }).addTo(map);

    var home_button = L.easyButton({
        states:[{
            stateName: 'set-view-to-newest',
            icon: 'fa fa-home',
            title: 'Center Map',
            onClick: function (btn, map) {
                map.setView([6.2442, -75.5812], 13, {animate: false});
            }
        }],
        id: 'set-view-to-newest',
        position: 'bottomright'
    });
    home_button.addTo(map);

    var remove_markers = L.easyButton({
        states:[{
            stateName: 'set-view-to-newest',
            icon: 'fa fa-trash',
            title: 'Remove Markers',
            onClick: function (btn, map) {
                console.log("Clear function called");
                // Eliminar todos los marcadores
                if (markers.length === 0) {
                    console.log("No markers or routes to remove.");
                    clearRoute();
                    return;
                }
                markers.forEach(marker => {
                    map.removeLayer(marker);
                });
                markers = [];
                selectedMarkers = []; // Limpiar los marcadores seleccionados
                console.log("Markers cleared.");
                clearRoute();
            }
        }],
        id: 'remove-markers-own-button',
        position: 'bottomright'
    });
    remove_markers.addTo(map);

    // Función para añadir marcadores a la ruta
    function addToRoute(lat, lng, button) {
        // Desactivar el botón mientras se procesa la solicitud
        button.disabled = true;
        
        // Añadir el marcador seleccionado al array
        selectedMarkers.push([lat, lng]);
        
        console.log("Marcador añadido a la ruta: ", lat, lng);
    
        // Simular un pequeño retraso para asegurar que el marcador se ha añadido correctamente
        setTimeout(() => {
            button.disabled = false; // Reactivar el botón
    
            // Cerrar el popup correctamente usando el método proporcionado por Leaflet
            const popup = map._popup; // Obtener el popup activo en el mapa
            if (popup) {
                map.closePopup(popup); // Cerrar el popup
            }
        }, 500);
    }

    // Función para dibujar la ruta
    function drawRoute() {
        if (selectedMarkers.length < 2) {
            alert("Selecciona al menos dos puntos para trazar la ruta.");
            return;
        }

        const colors = ['red', 'green', 'blue', 'orange', 'purple', 'darkred', 'lightgreen', 'darkblue', 'pink', 'yellow', 'black'];
        const randomColor = colors[Math.floor(Math.random() * colors.length)];
        const port = selectedRouteType === 'foot' ? '5000' : '5001';
        const coordinates = selectedMarkers.map(marker => `${marker[1]},${marker[0]}`).join(';');
        const osrmUrl = `http://localhost:${port}/route/v1/driving/${coordinates}?overview=full&geometries=geojson`;

        fetch(osrmUrl)
            .then(response => response.json())
            .then(data => {
                if (routeControl) {
                    map.removeLayer(routeControl); // Elimina la ruta previa si ya existe
                }
                const route = data.routes[0].geometry;
                routeControl = L.geoJSON(route, {
                    style: {
                        color: randomColor,
                        weight: 4
                    }
                }).addTo(map);
                //map.fitBounds(routeControl.getBounds());
            })
            .catch(error => {
                console.error('Error al obtener la ruta:', error);
            });
    }

    // Función para limpiar la ruta
    function clearRoute() {
        if (routeControl) {
            map.removeLayer(routeControl); // Eliminar la ruta del mapa
            routeControl = null;
        }
        selectedMarkers = []; // Limpiar los marcadores seleccionados
        console.log("Ruta y marcadores limpiados.");
    }

    function loadMarkers() {
        fetch('get-markers/')  // URL de la vista en Django
        .then(response => response.json())
        .then(data => {
            const markers = data.markers;
    
            markers.forEach(markerData => {
                var marker = L.marker([markerData.latitude, markerData.longitude]).addTo(map);
    
                // Crear el popup con un diseño más compacto
                const popupContent = `
                    <div style="background-color:#0081a7; color: white; padding: 8px; border-radius: 8px; max-width: 200px; text-align: center; font-family: Arial, sans-serif;">
                        <img src="${markerData.images[0]}" alt="${markerData.name}" style="width:100%; height:auto; border-radius: 4px;">
                        <h3 style="margin-top: 8px; font-size: 14px; color: #423E3B;">${markerData.name}</h3>
                        <p style="font-size: 10px; color: #ffffffb3;">${markerData.description}</p>
                        <button onclick="verMas(${markerData.id})" style="background-color: #423E3B; color:#ffffffb3; border: none; padding: 6px 10px; border-radius: 4px; cursor: pointer;">
                            Ver más
                        </button>
                        <button class="add-to-route" data-lat="${markerData.latitude}" data-lng="${markerData.longitude}" style="background-color: #f3e900; color:#423E3B; border: none; padding: 6px 10px; border-radius: 4px; cursor: pointer; margin-top: 8px;">
                            Añadir a Ruta
                        </button>
                    </div>
                `;
    
                marker.bindPopup(popupContent);
    
                // Usamos un listener para asegurar que los botones se comporten correctamente
                marker.on("popupopen", function() {
                    var button = document.querySelector(".add-to-route");
                    if (button) {
                        button.addEventListener("click", function() {
                            var lat = this.getAttribute("data-lat");
                            var lng = this.getAttribute("data-lng");
                            addToRoute(lat, lng, this); // Pasamos el botón a la función
                        });
                    }
                });
            });
        })
        .catch(error => {
            console.error('Error al obtener los marcadores:', error);
        });
    }

    loadMarkers();

};

export async function setViewOnPlace(lat, lng) {
    map.setView([lat, lng], 18);
}

export async function getselectedRouteType() {
    return selectedRouteType;
}

export function setselectedRouteType(routeType) {
    selectedRouteType = routeType;
}

export async function addsearchedRoute(markers){
    selectedMarkers = markers;
    if (selectedMarkers.length < 2) {
        alert("Selecciona al menos dos puntos para trazar la ruta.");
        return;
    }

    const colors = ['red', 'green', 'blue', 'orange', 'purple', 'darkred', 'lightgreen', 'darkblue', 'pink', 'yellow', 'black'];
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    const port = selectedRouteType === 'foot' ? '5000' : '5001';
    const coordinates = selectedMarkers.map(marker => `${marker[1]},${marker[0]}`).join(';');
    const osrmUrl = `http://localhost:${port}/route/v1/driving/${coordinates}?overview=full&geometries=geojson`;

    fetch(osrmUrl)
        .then(response => response.json())
        .then(data => {
            if (routeControl) {
                map.removeLayer(routeControl); // Elimina la ruta previa si ya existe
            }
            const route = data.routes[0].geometry;
            routeControl = L.geoJSON(route, {
                style: {
                    color: randomColor,
                    weight: 4
                }
            }).addTo(map);
            //map.fitBounds(routeControl.getBounds());
        })
        .catch(error => {
            console.error('Error al obtener la ruta:', error);
        });
}
