var selectedRouteType = 'foot'; // Valor por defecto
document.addEventListener('DOMContentLoaded', function() {

    // Mostrar u ocultar el menú al hacer clic en el botón de menú
    document.getElementById('menu-button').addEventListener('click', function() {
        var routeOptions = document.getElementById('route-options');
        if (routeOptions.style.display === 'none' || routeOptions.style.display === '') {
            routeOptions.style.display = 'block';
        } else {
            routeOptions.style.display = 'none';
        }
    });

    // Función para actualizar el círculo seleccionado
    function updateSelectedCircle(selectedId) {
        // Restablece todos los círculos a blanco
        document.getElementById('foot-circle').classList.remove('selected');
        document.getElementById('car-circle').classList.remove('selected');

        // Cambia el círculo seleccionado a negro
        document.getElementById(selectedId).classList.add('selected');
    }

    // Inicialmente, selecciona Peatonal
    updateSelectedCircle('foot-circle');

    // Event listeners para cambiar la selección y ocultar el menú
    document.getElementById('foot-route').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir la acción por defecto del enlace
        selectedRouteType = 'foot';
        loadRoute(selectedRouteType);
        updateSelectedCircle('foot-circle');
        document.getElementById('route-options').style.display = 'none';
    });

    document.getElementById('car-route').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir la acción por defecto del enlace
        selectedRouteType = 'driving';
        loadRoute(selectedRouteType);
        updateSelectedCircle('car-circle');
        document.getElementById('route-options').style.display = 'none';
    });

    function loadRoute(type) {
        console.log("Cargando ruta tipo:", type);
        // Aquí puedes implementar la lógica para cargar la ruta según el tipo seleccionado
    }
});
