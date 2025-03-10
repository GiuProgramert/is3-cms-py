#!/bin/bash

# Configuración inicial
set -e

# Ruta al backend y frontend
BACKEND_DIR="./backend/cms_backend"
FRONTEND_DIR="./frontend/cms-frontend"

# Función para instalar dependencias y configurar el entorno virtual
setup_backend() {
    echo "Configurando el backend..."

    # Crear entorno virtual si no existe
    if [ ! -d "$BACKEND_DIR/venv" ]; then
        echo "Creando entorno virtual..."
        python3 -m venv "$BACKEND_DIR/venv"
    fi

    # Activar entorno virtual
    if [ -f "$BACKEND_DIR/venv/bin/activate" ]; then
    source "$BACKEND_DIR/venv/bin/activate"
elif [ -f "$BACKEND_DIR/venv/Scripts/activate" ]; then
    source "$BACKEND_DIR/venv/Scripts/activate"
else
    echo "Error: No se pudo encontrar el script de activación del entorno virtual."
    exit 1
fi


    # Configurar el PYTHONPATH
    export PYTHONPATH="$PYTHONPATH:$BACKEND_DIR"

    # Instalar dependencias
    "$BACKEND_DIR/venv/Scripts/python.exe" -m pip install --upgrade pip
    pip install -r "$BACKEND_DIR/requirements.txt"

    # Configurar la base de datos
    echo "Configurando la base de datos..."

    # Verificar si la base de datos "cms" existe en el host postgres.cms
    DB_EXIST=$(psql -h postgres.cms -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='cms';")

    if [ "$DB_EXIST" != "1" ]; then
        echo "La base de datos 'cms' no existe. Creando..."
        psql -h postgres.cms -U postgres -c "CREATE DATABASE cms;"
        psql -h postgres.cms -U postgres -c "CREATE USER postgres WITH PASSWORD 'postgres';"
        psql -h postgres.cms -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE cms TO postgres;"
    else
        echo "La base de datos 'cms' ya existe. No se realizará ningún cambio."
    fi

    # Aplicar migraciones
    echo "Aplicando migraciones..."
    python "$BACKEND_DIR/manage.py" migrate

    # Crear superusuario opcionalmente
    read -p "¿Deseas crear un superusuario? (s/n): " create_superuser
    if [ "$create_superuser" == "s" ]; then
        python "$BACKEND_DIR/manage.py" createsuperuser
    fi

    # Generar la documentación con pydoc
    echo "Generando la documentación con pydoc..."
    pydoc -w "$BACKEND_DIR"

    # Levantar servidor de desarrollo del backend
    echo "Levantando el servidor de desarrollo del backend..."
    python "$BACKEND_DIR/manage.py" runserver &
}

# Función para configurar el frontend
setup_frontend() {
    echo "Configurando el frontend..."

    # Instalar dependencias del frontend
    cd "$FRONTEND_DIR"
    npm install

    # Levantar el servidor de desarrollo del frontend
    echo "Levantando el servidor de desarrollo del frontend..."
    npm start &
}

# Ejecutar las funciones
setup_backend
setup_frontend

echo "¡Entorno de desarrollo configurado y levantado correctamente!"
