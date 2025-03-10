#!/bin/bash
set -e

# Verificar que la variable DATABASE_URL esté definida
if [ -z "$DATABASE_URL" ]; then
  echo "La variable de entorno DATABASE_URL no está definida."
  exit 1
fi

# Esperar a que la base de datos esté lista
until psql "$DATABASE_URL" -c '\q'; do
  >&2 echo "Postgres aún no está disponible - esperando..."
  sleep 1
done

>&2 echo "Postgres está arriba - continuando con la configuración."

# Moverse al directorio de la aplicación
cd /app

# Aplicar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Levantar el servidor (Gunicorn o cualquier otro servidor)
exec "$@"
