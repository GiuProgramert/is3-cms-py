#!/bin/bash

# Variables de configuración
REPO_URL="https://gitlab.com/is2-bbfl/cms-24.git"
BRANCH="develop"
PROJECT_DIR="cms-24"
NETWORK_NAME="cms-24_app-network"
VOLUME_STATIC="cms-24_static_volume"
VOLUME_DB="cms-24_postgres_data"

# Configuración del volumen externo para archivos estáticos si no existe
if ! docker volume ls | grep -q $VOLUME_STATIC; then
    echo "Creando el volumen externo $VOLUME_STATIC..."
    docker volume create $VOLUME_STATIC
else
    echo "El volumen externo $VOLUME_STATIC ya existe."
fi

# Configuración del volumen externo para la base de datos si no existe
if ! docker volume ls | grep -q $VOLUME_DB; then
    echo "Creando el volumen externo $VOLUME_DB..."
    docker volume create $VOLUME_DB
else
    echo "El volumen externo $VOLUME_DB ya existe."
fi

# Configuración de la red si no existe
if ! docker network ls | grep -q $NETWORK_NAME; then
    echo "Creando la red $NETWORK_NAME..."
    docker network create $NETWORK_NAME
else
    echo "La red $NETWORK_NAME ya existe."
fi

# Clonar o actualizar el repositorio
if [ -d "$PROJECT_DIR" ]; then
    echo "Actualizando el repositorio en desarrollo..."
    cd $PROJECT_DIR
    git pull origin $BRANCH
else
    echo "Clonando el repositorio..."
    git clone -b $BRANCH $REPO_URL
    cd $PROJECT_DIR
fi

# Crear y levantar contenedores en modo desarrollo
echo "Levantando contenedores de desarrollo..."
docker-compose -f docker-compose.yml up --build -d

# Esperar a que el contenedor de la base de datos esté listo
echo "Esperando a que la base de datos esté disponible..."
docker-compose exec -T db bash -c "until pg_isready -h db -U postgres ; do sleep 1 ; done"

# Crear nuevas migraciones si hay cambios en los modelos
echo "Creando nuevas migraciones..."
docker-compose exec backend bash -c "python /app/cms_backend/manage.py makemigrations"

# Aplicar migraciones
echo "Aplicando migraciones..."
docker-compose exec backend bash -c "python /app/cms_backend/manage.py migrate"

# Copiar el archivo SQL al contenedor de la base de datos y poblar la base de datos
echo "Poblando la base de datos con datos iniciales desde datos2.sql..."
docker cp datos2.sql $(docker-compose ps -q db):/datos2.sql
docker-compose exec -T db psql -U postgres -d cms -f /datos2.sql

echo "Despliegue de desarrollo completado."
