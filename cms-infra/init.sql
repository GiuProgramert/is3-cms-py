-- Crear los permisos en la tabla cms_backend_permiso
INSERT INTO cms_backend_permiso (nombre) VALUES
('LISTAR_USUARIO'),
('LISTAR_CATEGORIA'),
('LISTAR_CONTENIDO'),
('LISTAR_ROL'),
('LISTAR_PERMISO'),
('CREAR_USUARIO'),
('EDITAR_USUARIO'),
('EDITAR_ROL'),
('CREAR_ROL'),
('EDITAR_CATEGORIA'),
('CREAR_CATEGORIA'),
('EDITAR_CONTENIDO'),
('CREAR_CONTENIDO'),
('PUBLICAR_CONTENIDO'),
('RECHAZAR_CONTENIDO'),
('ELIMINAR_USUARIO'),
('ELIMINAR_ROL'),
('ELIMINAR_CATEGORIA'),
('INACTIVAR_CONTENIDO'),
('LISTAR_MONITOREO'),
('VER_PAGINA_PRINCIPAL');

-- Crear el rol de administrador en la tabla cms_backend_rol
INSERT INTO cms_backend_rol (nombre) VALUES ('ADMIN');

-- Asignar todos los permisos al rol de administrador
INSERT INTO cms_backend_rol_permisos (rol_id, permiso_id)
SELECT (SELECT id FROM cms_backend_rol WHERE nombre = 'ADMIN'), id FROM cms_backend_permiso;

-- Crear el usuario administrador en la tabla cms_backend_usuario
INSERT INTO cms_backend_usuario (username, email) VALUES ('admin1', 'cmsa154@gmail.com');

-- Asignar el rol de administrador al usuario
INSERT INTO cms_backend_usuario_roles (usuario_id, rol_id)
SELECT (SELECT id FROM cms_backend_usuario WHERE username = 'admin1'), (SELECT id FROM cms_backend_rol WHERE nombre = 'ADMIN');

-- Crear el rol de 'AUTOR' en la tabla cms_backend_rol
INSERT INTO cms_backend_rol (nombre) VALUES ('AUTOR');

-- Asignar permisos específicos al rol de 'AUTOR'
-- En este caso, solo otorgamos 'LISTAR_CONTENIDO' y 'CREAR_CONTENIDO'
INSERT INTO cms_backend_rol_permisos (rol_id, permiso_id)
SELECT (SELECT id FROM cms_backend_rol WHERE nombre = 'AUTOR'), id FROM cms_backend_permiso
WHERE nombre IN ('LISTAR_CONTENIDO', 'CREAR_CONTENIDO');

-- Crear el usuario 'cmsautor' en la tabla cms_backend_usuario
INSERT INTO cms_backend_usuario (username, email) VALUES ('cmsautor', 'cmsautor@gmail.com');

-- Asignar el rol de 'AUTOR' al usuario 'cmsautor'
INSERT INTO cms_backend_usuario_roles (usuario_id, rol_id)
SELECT (SELECT id FROM cms_backend_usuario WHERE username = 'cmsautor'),
       (SELECT id FROM cms_backend_rol WHERE nombre = 'AUTOR');

-- Crear el rol de 'EDITOR' en la tabla cms_backend_rol
INSERT INTO cms_backend_rol (nombre) VALUES ('EDITOR');

-- Asignar permisos específicos al rol de 'EDITOR'
-- En este caso, otorgamos 'LISTAR_CONTENIDO' y 'EDITAR_CONTENIDO'
INSERT INTO cms_backend_rol_permisos (rol_id, permiso_id)
SELECT (SELECT id FROM cms_backend_rol WHERE nombre = 'EDITOR'), id FROM cms_backend_permiso
WHERE nombre IN ('LISTAR_CONTENIDO', 'EDITAR_CONTENIDO');

-- Crear el usuario 'cmseditor' en la tabla cms_backend_usuario
INSERT INTO cms_backend_usuario (username, email) VALUES ('cmseditor', 'cmseditor214@gmail.com');

-- Asignar el rol de 'EDITOR' al usuario 'cmseditor'
INSERT INTO cms_backend_usuario_roles (usuario_id, rol_id)
SELECT (SELECT id FROM cms_backend_usuario WHERE username = 'cmseditor'),
       (SELECT id FROM cms_backend_rol WHERE nombre = 'EDITOR');

-- Crear el rol de 'PUBLICADOR' en la tabla cms_backend_rol
INSERT INTO cms_backend_rol (nombre) VALUES ('PUBLICADOR');

-- Asignar permisos específicos al rol de 'PUBLICADOR'
-- En este caso, otorgamos 'PUBLICAR_CONTENIDO', 'RECHAZAR_CONTENIDO', 'INACTIVAR_CONTENIDO', y 'LISTAR_CONTENIDO'
INSERT INTO cms_backend_rol_permisos (rol_id, permiso_id)
SELECT (SELECT id FROM cms_backend_rol WHERE nombre = 'PUBLICADOR'), id FROM cms_backend_permiso
WHERE nombre IN ('PUBLICAR_CONTENIDO', 'RECHAZAR_CONTENIDO', 'INACTIVAR_CONTENIDO', 'LISTAR_CONTENIDO');

-- Crear el usuario 'publicador' en la tabla cms_backend_usuario
INSERT INTO cms_backend_usuario (username, email) VALUES ('publicador', 'mariaotiliazaratedevillalba@gmail.com');

-- Asignar el rol de 'PUBLICADOR' al usuario 'publicador'
INSERT INTO cms_backend_usuario_roles (usuario_id, rol_id)
SELECT (SELECT id FROM cms_backend_usuario WHERE username = 'publicador'),
       (SELECT id FROM cms_backend_rol WHERE nombre = 'PUBLICADOR');