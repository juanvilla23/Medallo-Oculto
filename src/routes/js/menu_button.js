import { setViewOnPlace, getselectedRouteType, setselectedRouteType, addsearchedRoute } from './main_route_logic.js';
var selectedRouteType = await getselectedRouteType(); // Valor por defecto para el tipo de ruta
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
        selectedRouteType = setselectedRouteType('foot');
        loadRoute(selectedRouteType);
        updateSelectedCircle('foot-circle');
        document.getElementById('route-options').style.display = 'none';
    });

    document.getElementById('car-route').addEventListener('click', function(event) {
        event.preventDefault();
        selectedRouteType = setselectedRouteType('driving');
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
                    displayResults(data, selectedSearchType); // Mostrar resultados
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

    function displayResults(results, selectedSearchType) {
        console.log('Mostrando resultados:', results);
        resultContainer.innerHTML = ''; // Limpiar resultados anteriores
    
        if (results.length === 0) {
            const noResults = document.createElement('div');
            noResults.textContent = 'No se encontraron coincidencias';
            noResults.style.border = '1px solid red';
            noResults.style.padding = '10px';
            noResults.style.borderRadius = '10px'; // Caja redondeada
            resultContainer.appendChild(noResults);
        } else {
            results.slice(0, 5).forEach(result => {
                const resultCard = document.createElement('div');
                resultCard.className = 'result-card';
                resultCard.innerHTML = `
                    <h3 style="margin-right: 8px;">${result.name}</h3>
                    <p>${result.description}</p>
                    <div class="button-container"></div>
                `; // Añadir un contenedor para los botones
                
                const buttonContainer = resultCard.querySelector('.button-container');
    
                // Añadir botones según el tipo de búsqueda seleccionado
                if (selectedSearchType === 'route') {
                    const viewRouteButton = document.createElement('button');
                    viewRouteButton.textContent = 'Ver ruta';
                    viewRouteButton.classList.add('action-button', 'styled-button'); // Añadir las clases de estilo de otros botones
                    viewRouteButton.onclick = () => viewRoute(result.id); // Función para ver ruta
    
                    const showRouteButton = document.createElement('button');
                    showRouteButton.textContent = 'Mostrar';
                    showRouteButton.classList.add('action-button', 'styled-button'); // Añadir las clases de estilo de otros botones
                    showRouteButton.onclick = () => showRoute(result.id); // Función para mostrar ruta
    
                    buttonContainer.appendChild(viewRouteButton);
                    buttonContainer.appendChild(showRouteButton);
                } 
                else if (selectedSearchType === 'place') {
                    const viewPlaceButton = document.createElement('button');
                    viewPlaceButton.textContent = 'Ver lugar';
                    viewPlaceButton.classList.add('action-button', 'styled-button'); // Añadir las clases de estilo de otros botones
                    viewPlaceButton.onclick = () => viewPlace(result.id); // Función para ver lugar
    
                    const showPlaceButton = document.createElement('button');
                    showPlaceButton.textContent = 'Mostrar';
                    showPlaceButton.classList.add('action-button', 'styled-button'); // Añadir las clases de estilo de otros botones
                    showPlaceButton.onclick = () => showPlace(result.id); // Función para mostrar lugar
    
                    buttonContainer.appendChild(viewPlaceButton);
                    buttonContainer.appendChild(showPlaceButton);
                }
                else if (selectedSearchType === 'event') {
                    const viewEventButton = document.createElement('button');
                    viewEventButton.textContent = 'Ver evento';
                    viewEventButton.classList.add('action-button', 'styled-button'); // Añadir las clases de estilo de otros botones
                    viewEventButton.onclick = () => viewEvent(result.id); // Función para ver evento
    
                    buttonContainer.appendChild(viewEventButton);
                }
    
                resultContainer.appendChild(resultCard);
            });
        }
    
        resultContainer.style.display = 'block'; // Mostrar el contenedor de resultados
    }
    
    // Ejemplo de las funciones que se ejecutarán cuando se haga clic en los botones
    async function viewRoute(routeId) {
        console.log('Ver ruta con ID:', routeId);

        try {
            const response = await fetch(`get_route_coords_by_id/?id=${routeId}`);
    
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }

            const data = await response.json();
            const coordinates = data.map(location => {
                return [parseFloat(location.latitude), parseFloat(location.longitude)];
            });
            console.log('Respuesta del servidor formateada:', coordinates)
            await addsearchedRoute(coordinates);

        } catch (error) {
            console.error('Error al obtener las coordenadas de la ruta:', error);
            alert('Ocurrió un error al obtener las coordenadas de la ruta');
        }
        // Aquí puedes implementar la lógica para ver la ruta
    }
    
    function showRoute(routeId) {
        console.log('Mostrar ruta con ID:', routeId);
        // Aquí puedes implementar la lógica para mostrar la ruta en el mapa
    }
    
    async function viewPlace(placeId) {
        console.log('Ver lugar con ID:', placeId);
        
        try {
            const response = await fetch(`get_coords_by_id/?id=${placeId}`);
    
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }
    
            const data = await response.json(); // Espera a que se resuelva el JSON
            console.log('Respuesta del servidor:', data);
            
            const latitude = parseFloat(data.latitude);
            const longitude = parseFloat(data.longitude);
    
            await setViewOnPlace(latitude, longitude);
    
        } catch (error) {
            console.error('Error al obtener las coordenadas:', error);
            alert('Ocurrió un error al obtener las coordenadas del lugar');
        }
    }
    
    function showPlace(placeId) {
        console.log('Mostrar lugar con ID:', placeId);
        // Aquí puedes implementar la lógica para mostrar el lugar en el mapa
    }
    
    function viewEvent(eventId) {
        console.log('Ver evento con ID:', eventId);
        // Aquí puedes implementar la lógica para ver el evento
    }
    
    document.addEventListener('click', function(event) {
        var resultContainer = document.getElementById('result-container');
        var searchBar = document.getElementById('input_search_bar');
        var searchButton = document.getElementById('search-button');
    
        if (!resultContainer.contains(event.target) && !searchBar.contains(event.target) && !searchButton.contains(event.target)) {
            resultContainer.style.display = 'none'; // Hide the results if clicked outside
        }
    });
    
    
});
