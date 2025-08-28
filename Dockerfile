# Imagen base ligera con Python
FROM python:3.12-slim

# Ajustes de Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Paquetes del sistema necesarios
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-traditional \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . /app

# (opcional) si tu módulo settings es distinto, ajusta la ruta WSGI abajo
EXPOSE 8000

# Comando por defecto: migraciones, collectstatic (tolerado) y Gunicorn
CMD sh -c "python manage.py migrate && \
           python manage.py collectstatic --noinput || true && \
           gunicorn settings.wsgi:application --bind 0.0.0.0:8000 --workers 3"
