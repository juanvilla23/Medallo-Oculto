-- Datos de prueba para la base de datos

-- Extensión para manejar texto sin acentos
CREATE EXTENSION IF NOT EXISTS unaccent;

-- Crear usuario "Usuario Test" en auth_user
INSERT INTO auth_user (password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES
('pbkdf2_sha256$720000$6APqoOARSSte4HyC7gkV5O$LznZ71RF8eBx4V6uTLsWyjr3pfQ4ffmROtPX41y2CbM=', -- Contraseña: test)
 false, 'UsuarioTest', 'Usuario', 'Test', 'usuariotest@example.com', false, true, NOW());

-- Insertar en users_turista para enlazarlo como turista
INSERT INTO users_turista (user_id, tipo)
SELECT id, 'Turista' FROM auth_user WHERE username = 'UsuarioTest';

-- Insertar lugares de interés con el usuario "Usuario Test" como creador
INSERT INTO interest_place (name, description, categories, status, latitude, longitude, images, creator_id, address)
VALUES
('Parque Explora', 'Un parque interactivo y educativo', ARRAY['Educación', 'Entretenimiento'], TRUE, 6.270121, -75.565755, ARRAY['https://www.medellin.travel/wp-content/uploads/2020/10/Explora.jpg'], (SELECT id FROM auth_user WHERE username = 'UsuarioTest'), 'Cra. 52 #73-75, Medellín, Antioquia'),
('Museo de Antioquia', 'Museo de arte y cultura en Medellín', ARRAY['Cultura', 'Historia'], TRUE, 6.251840, -75.563591, ARRAY['https://th.bing.com/th/id/OIP.UFXNwnGzi7IuNQYeBdtJcwAAAA?rs=1&pid=ImgDetMain'], (SELECT id FROM auth_user WHERE username = 'UsuarioTest') , 'Cra. 52 #52-43, Medellín, Antioquia'),
('Pueblito Paisa', 'Un pequeño pueblo tradicional en la cima del Cerro Nutibara', ARRAY['Turismo', 'Cultura'], TRUE, 6.242287, -75.576492, ARRAY['https://th.bing.com/th/id/OIP.BgaVq6WK3DBOB59fbZwq0gHaEK?w=300&h=180&c=7&r=0&o=5&pid=1.7'], (SELECT id FROM auth_user WHERE username = 'UsuarioTest') , 'Cra. 30 #55-219, Medellín, Antioquia'),
('Parque Arví', 'Un gran parque natural en Medellín', ARRAY['Naturaleza', 'Turismo'], TRUE, 6.284250, -75.518639, ARRAY['https://www.sitiosturisticoscolombia.com/wp-content/uploads/cascada-reserva-ecoturistica-la-avispa-500x383@2x.jpg'], (SELECT id FROM auth_user WHERE username = 'UsuarioTest') , 'Corregimiento Santa Elena, Medellín, Antioquia'),
('Teatro Pablo Tobón Uribe', 'Un teatro histórico y cultural en Medellín', ARRAY['Cultura', 'Entretenimiento'], TRUE, 6.247637, -75.565340, ARRAY['https://th.bing.com/th/id/OIP.KWJjdSFVze214pw6UrzWxgHaE5?w=263&h=180&c=7&r=0&o=5&pid=1.7'], (SELECT id FROM auth_user WHERE username = 'UsuarioTest') , 'Cra. 41 #57-30, Medellín, Antioquia'),
('Casa Museo Otraparte', 'Casa museo dedicada al escritor Fernando González', ARRAY['Cultura', 'Historia'], TRUE, 6.161055, -75.608574, ARRAY['https://th.bing.com/th/id/OIP.vpU3S36XxATEZurwQKC56QHaFj?w=220&h=180&c=7&r=0&o=5&pid=1.7'], (SELECT id FROM auth_user WHERE username = 'UsuarioTest') , 'Cra. 66 #34-24, Envigado, Antioquia'),
('Jardín Botánico', 'Un jardín botánico que alberga una amplia variedad de plantas', ARRAY['Naturaleza', 'Educación'], TRUE, 6.270640, -75.565815, ARRAY['https://th.bing.com/th/id/OIP.LvsCrJnWMnVnCDtpkZ7eyQHaEJ?w=306&h=180&c=7&r=0&o=5&pid=1.7'], (SELECT id FROM auth_user WHERE username = 'UsuarioTest') , 'Cra. 52 #73-75, Medellín, Antioquia'),
('Cerro El Volador', 'Una de las principales reservas naturales en Medellín', ARRAY['Naturaleza', 'Turismo'], TRUE, 6.268430, -75.579209, ARRAY['https://th.bing.com/th/id/OIP.rhdy9NmLzAu7vzyF5ZHGZwHaEK?w=286&h=180&c=7&r=0&o=5&pid=1.7'], (SELECT id FROM auth_user WHERE username = 'UsuarioTest') , 'Cra. 65 #73-223, Medellín, Antioquia'),
('Plaza Botero', 'Una plaza pública con esculturas del artista Fernando Botero', ARRAY['Arte', 'Urbano'], TRUE, 6.251569, -75.563786, ARRAY['https://th.bing.com/th/id/OIP.jMpKBDr0cpK88tqdSWuWEgHaHa?w=194&h=194&c=7&r=0&o=5&pid=1.7'], (SELECT id FROM auth_user WHERE username = 'UsuarioTest') , 'Cra. 52 #52-43, Medellín, Antioquia'),
('Parque de los Deseos', 'Un parque urbano que ofrece diversas actividades culturales', ARRAY['Cultura', 'Urbano'], TRUE, 6.268187, -75.565684, ARRAY['https://th.bing.com/th/id/OIP.lF6dc_rC4AN4RdFKAHBELQHaE7?w=282&h=188&c=7&r=0&o=5&pid=1.7'], (SELECT id FROM auth_user WHERE username = 'UsuarioTest') , 'Cra. 53 #74-82, Medellín, Antioquia');

-- Insertar rutas con el usuario "Usuario Test" como creador
INSERT INTO route (name, creator_id, description)
VALUES
('Ruta Cultural', (SELECT id FROM auth_user WHERE username = 'UsuarioTest'), 'Recorrido por lugares culturales de Medellín'),
('Ruta Natural', (SELECT id FROM auth_user WHERE username = 'UsuarioTest'), 'Exploración de espacios naturales en Medellín'),
('Ruta Urbana', (SELECT id FROM auth_user WHERE username = 'UsuarioTest'), 'Tour por sitios urbanos y representativos de Medellín');

-- Insertar lugares de interés en las rutas
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