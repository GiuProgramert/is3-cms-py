FROM python:3.11-slim

# Configuración de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo
WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalación de dependencias de Python
COPY cms_backend/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar el código del backend
COPY cms_backend/ /app/cms_backend

# Copiar el archivo manage.py al directorio raíz
COPY cms_backend/manage.py /app/manage.py

# Colectar archivos estáticos
RUN python manage.py collectstatic --noinput

# Puerto expuesto
EXPOSE 8000

# Ejecutar Gunicorn
CMD ["gunicorn", "--chdir", "/app/cms_backend", "cms_backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]