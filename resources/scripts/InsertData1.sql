-- InterestPlace
INSERT INTO interest_place (name, description, categories, status, latitude, longitude, images)
VALUES 
('Parque Explora', 'Un parque interactivo y educativo', ARRAY['Educación', 'Entretenimiento'], TRUE, 6.270121, -75.565755, ARRAY['explora1.jpg', 'explora2.jpg']),
('Museo de Antioquia', 'Museo de arte y cultura en Medellín', ARRAY['Cultura', 'Historia'], TRUE, 6.251840, -75.563591, ARRAY['museo1.jpg', 'museo2.jpg']),
('Pueblito Paisa', 'Un pequeño pueblo tradicional en la cima del Cerro Nutibara', ARRAY['Turismo', 'Cultura'], TRUE, 6.242287, -75.576492, ARRAY['paisa1.jpg', 'paisa2.jpg']),
('Parque Arví', 'Un gran parque natural en Medellín', ARRAY['Naturaleza', 'Turismo'], TRUE, 6.284250, -75.518639, ARRAY['arvi1.jpg', 'arvi2.jpg']),
('Teatro Pablo Tobón Uribe', 'Un teatro histórico y cultural en Medellín', ARRAY['Cultura', 'Entretenimiento'], TRUE, 6.247637, -75.565340, ARRAY['teatro1.jpg', 'teatro2.jpg']),
('Casa Museo Otraparte', 'Casa museo dedicada al escritor Fernando González', ARRAY['Cultura', 'Historia'], TRUE, 6.161055, -75.608574, ARRAY['otraparte1.jpg', 'otraparte2.jpg']),
('Jardín Botánico', 'Un jardín botánico que alberga una amplia variedad de plantas', ARRAY['Naturaleza', 'Educación'], TRUE, 6.270640, -75.565815, ARRAY['jardin1.jpg', 'jardin2.jpg']),
('Cerro El Volador', 'Una de las principales reservas naturales en Medellín', ARRAY['Naturaleza', 'Turismo'], TRUE, 6.268430, -75.579209, ARRAY['volador1.jpg', 'volador2.jpg']),
('Plaza Botero', 'Una plaza pública con esculturas del artista Fernando Botero', ARRAY['Arte', 'Urbano'], TRUE, 6.251569, -75.563786, ARRAY['plazabotero1.jpg', 'plazabotero2.jpg']),
('Parque de los Deseos', 'Un parque urbano que ofrece diversas actividades culturales', ARRAY['Cultura', 'Urbano'], TRUE, 6.268187, -75.565684, ARRAY['deseos1.jpg', 'deseos2.jpg']);

-- Insertar datos en la tabla Route
INSERT INTO route (name)
VALUES 
('Ruta Cultural'),
('Ruta Natural'),
('Ruta Urbana');

-- RouteInterestPlace
INSERT INTO route_interest_place (route_id, interest_place_id, created_at, updated_at)
VALUES 
((SELECT id FROM route WHERE name = 'Ruta Cultural'), (SELECT id FROM interest_place WHERE name = 'Museo de Antioquia'), NOW(), NOW()),
((SELECT id FROM route WHERE name = 'Ruta Cultural'), (SELECT id FROM interest_place WHERE name = 'Pueblito Paisa'), NOW(), NOW()),
((SELECT id FROM route WHERE name = 'Ruta Cultural'), (SELECT id FROM interest_place WHERE name = 'Teatro Pablo Tobón Uribe'), NOW(), NOW()),
((SELECT id FROM route WHERE name = 'Ruta Cultural'), (SELECT id FROM interest_place WHERE name = 'Casa Museo Otraparte'), NOW(), NOW()),
((SELECT id FROM route WHERE name = 'Ruta Natural'), (SELECT id FROM interest_place WHERE name = 'Parque Arví'), NOW(), NOW()),
((SELECT id FROM route WHERE name = 'Ruta Natural'), (SELECT id FROM interest_place WHERE name = 'Jardín Botánico'), NOW(), NOW()),
((SELECT id FROM route WHERE name = 'Ruta Natural'), (SELECT id FROM interest_place WHERE name = 'Cerro El Volador'), NOW(), NOW()),
((SELECT id FROM route WHERE name = 'Ruta Urbana'), (SELECT id FROM interest_place WHERE name = 'Parque Explora'), NOW(), NOW()),
((SELECT id FROM route WHERE name = 'Ruta Urbana'), (SELECT id FROM interest_place WHERE name = 'Plaza Botero'), NOW(), NOW()),
((SELECT id FROM route WHERE name = 'Ruta Urbana'), (SELECT id FROM interest_place WHERE name = 'Parque de los Deseos'), NOW(), NOW());
