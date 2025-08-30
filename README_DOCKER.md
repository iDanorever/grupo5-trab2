# Docker Setup para Backend-Optimizacion

Este proyecto está configurado para ejecutarse completamente en Docker con todos los servicios necesarios.

## Requisitos Previos

- Docker Desktop instalado y ejecutándose
- Docker Compose (incluido en Docker Desktop)
- Al menos 4GB de RAM disponible para Docker

## Estructura de Servicios

El proyecto incluye los siguientes servicios:

- **web**: Aplicación Django (puerto 8000)
- **db**: Base de datos MySQL 8.0 (puerto 3306)
- **redis**: Cache y broker de mensajes (puerto 6379)
- **celery**: Worker de Celery para tareas asíncronas
- **celery-beat**: Scheduler de Celery para tareas programadas
- **nginx**: Servidor web y proxy reverso (puerto 80)

## Configuración Inicial

### 1. Configurar Variables de Entorno

Copia el archivo de ejemplo de variables de entorno:

```bash
cp env.example .env
```

Edita el archivo `.env` según tus necesidades.

### 2. Construir y Ejecutar

```bash
# Construir todas las imágenes
docker-compose build

# Ejecutar todos los servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f
```

### 3. Verificar que Todo Funcione

```bash
# Verificar que todos los contenedores estén ejecutándose
docker-compose ps

# Verificar logs de la aplicación web
docker-compose logs web

# Verificar logs de la base de datos
docker-compose logs db
```

## Acceso a la Aplicación

- **Aplicación principal**: http://localhost
- **Admin de Django**: http://localhost/admin
- **API REST**: http://localhost/api/

### Credenciales por Defecto

- **Superusuario**: admin / admin123
- **Base de datos**: root / 123456

## Comandos Útiles

### Gestión de Contenedores

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ver logs de un servicio específico
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f celery
```

### Gestión de Django

```bash
# Ejecutar comandos de Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Acceder al shell de Django
docker-compose exec web python manage.py shell

# Ejecutar tests
docker-compose exec web python manage.py test
```

### Gestión de Base de Datos

```bash
# Acceder a MySQL
docker-compose exec db mysql -u root -p

# Hacer backup de la base de datos
docker-compose exec db mysqldump -u root -p reflexo > backup.sql

# Restaurar backup
docker-compose exec -T db mysql -u root -p reflexo < backup.sql
```

### Gestión de Celery

```bash
# Ver logs de Celery worker
docker-compose logs -f celery

# Ver logs de Celery beat
docker-compose logs -f celery-beat

# Ejecutar tareas de Celery manualmente
docker-compose exec web celery -A settings call tasks.debug_task
```

## Desarrollo

### Modo Desarrollo

Para desarrollo, puedes usar el siguiente comando que monta el código como volumen:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### Hot Reload

Los cambios en el código se reflejarán automáticamente sin necesidad de reconstruir la imagen.

### Debugging

Para debugging, puedes acceder a los contenedores:

```bash
# Acceder al contenedor web
docker-compose exec web bash

# Acceder al contenedor de la base de datos
docker-compose exec db bash
```

## Producción

### Configuración de Producción

Para producción, asegúrate de:

1. Cambiar `DEBUG=False` en el archivo `.env`
2. Configurar una `SECRET_KEY` segura
3. Configurar `ALLOWED_HOSTS` apropiadamente
4. Configurar credenciales de base de datos seguras
5. Configurar SSL/TLS en Nginx

### Variables de Entorno de Producción

```bash
DEBUG=False
SECRET_KEY=tu-clave-secreta-muy-segura
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DATABASE_PASSWORD=password-muy-seguro
```

## Troubleshooting

### Problemas Comunes

1. **Puerto 3306 ya en uso**: Detén tu MySQL local o cambia el puerto en docker-compose.yml
2. **Puerto 80 ya en uso**: Detén tu servidor web local o cambia el puerto
3. **Error de permisos**: Asegúrate de que Docker tenga permisos para acceder a los archivos

### Logs y Debugging

```bash
# Ver todos los logs
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs web

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de los últimos 100 eventos
docker-compose logs --tail=100
```

### Limpieza

```bash
# Detener y eliminar contenedores
docker-compose down

# Eliminar también volúmenes (¡CUIDADO! Esto elimina la base de datos)
docker-compose down -v

# Eliminar imágenes
docker-compose down --rmi all

# Limpieza completa
docker system prune -a
```

## Estructura de Archivos

```
.
├── Dockerfile                 # Configuración de la imagen Docker
├── docker-compose.yml         # Configuración de servicios
├── entrypoint.sh             # Script de inicialización
├── .dockerignore             # Archivos a ignorar en Docker
├── env.example               # Variables de entorno de ejemplo
├── nginx/                    # Configuración de Nginx
│   ├── nginx.conf
│   └── default.conf
├── db/                       # Scripts de base de datos
│   └── init.sql
└── settings/                 # Configuración de Django
    ├── settings.py
    ├── celery.py
    └── __init__.py
```

## Monitoreo

### Health Checks

La aplicación incluye health checks automáticos:

- **Web**: http://localhost/health/
- **Database**: Verificado automáticamente en el entrypoint
- **Redis**: Verificado automáticamente en el entrypoint

### Métricas

Puedes monitorear los recursos usando:

```bash
# Ver uso de recursos
docker stats

# Ver información detallada de contenedores
docker-compose ps
```

## Soporte

Si encuentras problemas:

1. Revisa los logs: `docker-compose logs`
2. Verifica que todos los servicios estén ejecutándose: `docker-compose ps`
3. Revisa la configuración de red: `docker network ls`
4. Verifica los volúmenes: `docker volume ls`
