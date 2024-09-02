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
        center: [6.2442, -75.5812],
        zoom: 13,
        maxBounds: bounds,
        zoomControl: false,
        attributionControl: false, // Desactivar el control de atribución predeterminado

        contextmenu: true, // Activar el menú contextual que se activa con click derecho
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

    var openstreetmap = L.tileLayer(osmUrl, { attribution: openstreetAttr }).addTo(map);
    
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
