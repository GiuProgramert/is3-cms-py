# 📦 CMS - Guía de Instalación y Ejecución

Este proyecto CMS está configurado con Docker y utiliza imágenes almacenadas en **GitLab Container Registry** para el frontend, backend, base de datos y servidor Nginx.

---

## ✅ **1. Requisitos Previos**
- Docker y Docker Compose instalados en el sistema.
- Acceso al GitLab Container Registry.
- Permisos para acceder a los repositorios de imágenes.

---

## 🌐 **2. Configuración Inicial**

### 🔒 **2.1. Iniciar Sesión en GitLab Container Registry**
Ejecuta el siguiente comando para iniciar sesión en el registro de contenedores:

```bash
docker login registry.gitlab.com
```
Ingresa tu nombre de usuario y token de acceso personal (PAT) cuando se te solicite.

---

### 📁 **2.2. Estructura de Directorios**
Asegúrate de tener la siguiente estructura:

```
cms
├── backend
├── frontend
├── cms-volumes
│   ├── static
│   └── postgres_data
└── infra
    ├── docker-compose.yml
    └── init.sql
```

---

## 🚀 **3. Levantar la Aplicación**

### 💾 **3.1. Descargar las Imágenes Desde GitLab**
Desde la carpeta **infra**, ejecuta:

```bash
docker pull registry.gitlab.com/is2-bbfl/cms-backend:latest
docker pull registry.gitlab.com/is2-bbfl/cms-frontend:latest
docker pull nginx:stable-alpine
docker pull postgres:15
```

---

### 🐳 **3.2. Iniciar los Contenedores**
Para levantar los contenedores en segundo plano, ejecuta:

```bash
docker compose up -d
```

Para ver los logs de un contenedor en particular, usa:

```bash
docker compose logs backend
```

---

## 🌍 **4. Acceder a la Aplicación**
- **Frontend:** [http://localhost:3000](http://localhost:3000)
- **Backend:** [http://localhost:8000](http://localhost:8000)
- **Nginx:** [http://localhost](http://localhost)

---

## 🗑️ **5. Detener y Eliminar los Contenedores**
Para detener todos los contenedores:

```bash
docker compose down
```

Para eliminar los contenedores y los volúmenes persistentes:

```bash
docker compose down --volumes
```

---

## 💡 **6. Problemas Comunes**

1. **Error de permisos al acceder al registro:**
   - Asegúrate de haber iniciado sesión correctamente con `docker login registry.gitlab.com`.

2. **Los cambios en el código no se reflejan:**
   - Ejecuta `docker compose build --no-cache` para reconstruir las imágenes.

3. **Error de conexión a la base de datos:**
   - Verifica que los volúmenes estén correctamente configurados y elimina el volumen de PostgreSQL si es necesario.
3. **Base de datos vacia:**
   - Ingresa mediante bash al contenedor backend y ejecuta las migraciones Django.
   ```bash
   rm -rf cms_backend/migrations/*.py
   touch cms_backend/migrations/__init__.py
   python manage.py makemigrations
   python manage.py migrate
   ```
   - Ejecuta el script `init.sql` para poblar la base de datos.

---

## 📄 **7. Notas Adicionales**
- Este proyecto utiliza una red Docker personalizada llamada `app-network`.
- El volumen `cms-volumes` se comparte entre los servicios para almacenar archivos estáticos y datos de la base de datos.
- Asegúrate de tener acceso a los repositorios de GitLab para descargar las imágenes.

---

Si encuentras algún problema, contacta al administrador del proyecto. 🚀

