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
    const resultContainer = document.createElement('div'); // Crear contenedor de resultados

    // Agregar el contenedor de resultados dentro del header o justo después de search-bar
    resultContainer.id = 'result-container';
    resultContainer.style.display = 'none';
    resultContainer.classList.add('dropdown-content');
    document.getElementById('search-bar').appendChild(resultContainer); // Coloca el contenedor en el header

    // Función para manejar la búsqueda
    const handleSearch = () => {
        const query = searchBar.value.trim();

        if (query) {
            // Enviar una petición al backend para obtener los resultados
            fetch(`search/?q=${query}&i=${selectedSearchType}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error en la respuesta del servidor');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Resultados de la búsqueda:', data);
                    displayResults(data); // Mostrar resultados
                })
                .catch(error => {
                    console.error('Error al realizar la búsqueda:', error);
                    alert('Ocurrió un error al realizar la búsqueda.');
                });
        } else {
            alert('Por favor, ingrese un término de búsqueda');
        }
    };

    searchButton.addEventListener('click', handleSearch);

    function displayResults(results) {
        resultContainer.innerHTML = ''; // Limpiar resultados anteriores
    
        if (results.length === 0) {
            const noResults = document.createElement('div');
            noResults.textContent = 'No se encontraron coincidencias';
            noResults.style.border = '1px solid red';
            noResults.style.padding = '10px';
            resultContainer.appendChild(noResults);
        } else {
            results.slice(0, 5).forEach(result => {
                const resultCard = document.createElement('div');
                resultCard.className = 'result-card';
                resultCard.innerHTML = `<h3>${result.name}</h3><p>${result.description}</p>`;
                resultContainer.appendChild(resultCard);
            });
        }
    
        resultContainer.style.display = 'block'; // Mostrar el contenedor de resultados
    }
    
    
});
