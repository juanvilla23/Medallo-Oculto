const medelllin = [6.244203, -75.581211];
var map = L.map('map').setView([medelllin[0], medelllin[1]], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


// var menu = L.leafletMenu(map, Options)
// menu.show()
// menu.hide()
// menu.removeMenu()