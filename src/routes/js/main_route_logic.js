import {ZOOM_IN_URL, ZOOM_OUT_URL} from './envs.js';

var openstreetAttr = '&copy; <a href="https://github.com/juanvilla23/Medallo-Oculto">Medallo Oculto</a>'; 
var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var markersGroup = new L.FeatureGroup();
var bounds = [
    [6.053, -75.800], // Suroeste del Valle de Aburrá (Caldas)
    [6.490, -74.800]  // Noreste del Valle de Aburrá (Barbosa)
];

var markers = [];

window.onload = function() {
    
    var map = L.map('map', {
        center: [6.2442, -75.5812], // Centro del mapa
        zoom: 13, // Zoom inicial
        minZoom: 10, // Zoom out mínimo
        maxZoom: 18, // Zoom in máximo
        maxBounds: bounds, // Limita el área navegable al Valle de Aburrá
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
        minZoom: 8, // Asegura que la capa de mosaicos respete el zoom mínimo
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
                // Eliminar todos los marcadores  && routeControl === null
                if (markers.length === 0) {
                    console.log("No markers or routes to remove.");
                    return;
                }
                markers.forEach(marker => {
                    map.removeLayer(marker);
                });
                markers = [];

                console.log("Markers and routes cleared.");
            }
        }],
        id: 'remove-markers-own-button',
        position: 'bottomright'
    });
    remove_markers.addTo(map);


    // Demostración de rutas y marcadores estaticos

    // Coordenadas de los marcadores
    const startCoords = [6.269625, -75.566078]; // Coordenadas del punto de inicio
    const endCoords = [6.244998, -75.573565];   // Coordenadas del punto de destino

    // Crear marcadores
    L.marker(startCoords).addTo(map)
        .bindPopup('Punto de Inicio')
        .openPopup();

    L.marker(endCoords).addTo(map)
        .bindPopup('Punto de Destino')
        .openPopup();

    //Demostración de una ruta peatonal
    const osrmUrl23 = 'http://localhost:5000/route/v1/foot/-75.566078,6.269625;-75.573565,6.244998?overview=full&geometries=geojson';

      fetch(osrmUrl23)
        .then(response => response.json())
        .then(data => {
          const route = data.routes[0].geometry;
          L.geoJSON(route, {
            style: {
              color: 'green',
              weight: 4
            }
          }).addTo(map);
        })
        .catch(err => console.error(err));

    //Demostración de una ruta en carro
    const osrmUrl232 = 'http://localhost:5001/route/v1/driving/-75.566078,6.269625;-75.573565,6.244998?overview=full&geometries=geojson';

    fetch(osrmUrl232)
        .then(response => response.json())
        .then(data => {
        const route = data.routes[0].geometry;
        L.geoJSON(route, {
            style: {
            color: 'blue',
            weight: 4
            }
        }).addTo(map);
        })
        .catch(err => console.error(err));
};