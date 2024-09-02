import {ZOOM_IN_URL, ZOOM_OUT_URL} from './envs.js';

var openstreetAttr = '&copy; <a href="https://github.com/juanvilla23/Medallo-Oculto">Medallo Oculto</a>'; 
var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var markersGroup = new L.FeatureGroup();
var bounds = [
    [6.053, -75.800], // Suroeste del Valle de Aburrá (Caldas)
    [6.490, -74.800]  // Noreste del Valle de Aburrá (Barbosa)
];

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
        }]
    });

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
            title: 'Set View to Newest',
            onClick: function (btn, map) {
                map.setView([6.2442, -75.5812], 13, {animate: false});
            }
        }],
        id: 'set-view-to-newest',
        position: 'bottomright'
    });
    home_button.addTo(map);

};
