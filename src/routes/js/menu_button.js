var selectedRouteType = 'foot'; // Valor por defecto para el tipo de ruta
var selectedSearchType = 'place'; // Valor por defecto para el tipo de búsqueda

document.addEventListener('DOMContentLoaded', function() {

    // Mostrar u ocultar el menú de rutas al hacer clic en el primer botón de menú
    document.getElementById('menu-button').addEventListener('click', function() {
        var routeOptions = document.getElementById('route-options');
        if (routeOptions.style.display === 'none' || routeOptions.style.display === '') {
            routeOptions.style.display = 'block';
        } else {
            routeOptions.style.display = 'none';
        }
    });

    // Función para actualizar el círculo seleccionado para rutas
    function updateSelectedCircle(selectedId) {
        document.getElementById('foot-circle').classList.remove('selected');
        document.getElementById('car-circle').classList.remove('selected');
        document.getElementById(selectedId).classList.add('selected');
    }

    // Event listeners para rutas
    document.getElementById('foot-route').addEventListener('click', function(event) {
        event.preventDefault();
        selectedRouteType = 'foot';
        loadRoute(selectedRouteType);
        updateSelectedCircle('foot-circle');
        document.getElementById('route-options').style.display = 'none';
    });

    document.getElementById('car-route').addEventListener('click', function(event) {
        event.preventDefault();
        selectedRouteType = 'driving';
        loadRoute(selectedRouteType);
        updateSelectedCircle('car-circle');
        document.getElementById('route-options').style.display = 'none';
    });

    // Mostrar u ocultar el menú de búsqueda al hacer clic en el segundo botón de menú
    document.getElementById('menu-button2').addEventListener('click', function() {
        var searchOptions = document.getElementById('search-options');
        if (searchOptions.style.display === 'none' || searchOptions.style.display === '') {
            searchOptions.style.display = 'block';
        } else {
            searchOptions.style.display = 'none';
        }
    });

    // Función para actualizar el círculo seleccionado para tipos de búsqueda
    function updateSelectedSearchCircle(selectedId) {
        document.getElementById('event-circle').classList.remove('selected');
        document.getElementById('route-circle').classList.remove('selected');
        document.getElementById('place-circle').classList.remove('selected');
        document.getElementById(selectedId).classList.add('selected');
    }

    // Event listeners para el tipo de búsqueda
    document.getElementById('event-button').addEventListener('click', function(event) {
        event.preventDefault();
        selectedSearchType = 'event';
        updateSelectedSearchCircle('event-circle');
        document.getElementById('search-options').style.display = 'none';
        console.log("Tipo de búsqueda seleccionado: Evento");
    });

    document.getElementById('route-button').addEventListener('click', function(event) {
        event.preventDefault();
        selectedSearchType = 'route';
        updateSelectedSearchCircle('route-circle');
        document.getElementById('search-options').style.display = 'none';
        console.log("Tipo de búsqueda seleccionado: Ruta");
    });

    document.getElementById('place-button').addEventListener('click', function(event) {
        event.preventDefault();
        selectedSearchType = 'place';
        updateSelectedSearchCircle('place-circle');
        document.getElementById('search-options').style.display = 'none';
        console.log("Tipo de búsqueda seleccionado: Lugar de interés");
    });

    // Función para cargar la ruta según el tipo seleccionado
    function loadRoute(type) {
        console.log("Cargando ruta tipo:", type);
        // Aquí puedes implementar la lógica para cargar la ruta
    }



    const searchBar = document.getElementById('input_search_bar');
    const searchButton = document.getElementById('search-button');

    // Función para manejar la búsqueda
    const handleSearch = () => {
        const query = searchBar.value.trim(); // Tomar el valor de la barra de búsqueda

        if (query) {
            // Enviar una petición al backend para obtener los resultados
            fetch(`search/?q=${query}&i=${selectedSearchType}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error en la respuesta del servidor');
                    }
                    return response.json(); // Convertir a JSON
                })
                .then(data => {
                    // Aquí puedes manejar los resultados obtenidos y mostrarlos en el mapa o la interfaz
                    console.log("Datos recibidos:", data); // Muestra los resultados en la consola
                    displayResults(data); // Función para mostrar resultados
                })
                .catch(error => {
                    console.error('Error al realizar la búsqueda:', error);
                    alert('Ocurrió un error al realizar la búsqueda.');
                });
        } else {
            alert('Por favor, ingrese un término de búsqueda');
        }
    };

    // Asignar el evento al botón de búsqueda
    searchButton.addEventListener('click', handleSearch);

    // Función para mostrar resultados (personalízala según tus necesidades)
    function displayResults(results) {
        // Limpia los resultados anteriores
        const resultContainer = document.createElement('div'); // Crear un contenedor para los resultados

        // Crear un HTML dinámico o mostrar marcadores en el mapa según los resultados
        results.forEach(result => {
            const resultElement = document.createElement('p');
            resultElement.textContent = `Nombre: ${result.name}, ID: ${result.id}`; // Ajustar según los campos que recibes
            resultContainer.appendChild(resultElement);
        });

        // Añadir el contenedor de resultados al DOM (ajusta según tu estructura HTML)
        document.body.appendChild(resultContainer);
    }

});
