# 🚀 Instrucciones para Ejecutar Backend-Optimizacion en Docker

## 📋 Requisitos Previos

1. **Docker Desktop** instalado y ejecutándose
2. **Al menos 4GB de RAM** disponible para Docker
3. **Puertos disponibles**: 80, 3306, 6379, 8000

## 🎯 Inicio Rápido (Recomendado)

### Opción 1: Script Automático (Windows)
```powershell
# Ejecutar el script de PowerShell
.\start.ps1
```

### Opción 2: Script Automático (Linux/Mac)
```bash
# Hacer ejecutable el script
chmod +x start.sh

# Ejecutar el script
./start.sh
```

### Opción 3: Comandos Manuales
```bash
# 1. Copiar variables de entorno
cp env.example .env

# 2. Construir imágenes
docker-compose build

# 3. Iniciar servicios
docker-compose up -d

# 4. Ver logs
docker-compose logs -f
```

## 🔧 Configuración Detallada

### 1. Variables de Entorno
Edita el archivo `.env` según tus necesidades:
```bash
# Configuración básica
DEBUG=True
SECRET_KEY=tu-clave-secreta
DATABASE_PASSWORD=123456

# Configuración de red
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 2. Modos de Ejecución

#### Modo Desarrollo
```bash
# Con hot reload y debugging
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

#### Modo Producción
```bash
# Configurar variables de producción
cp env.prod.example .env.prod
# Editar .env.prod con valores seguros

# Ejecutar en modo producción
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

## 🌐 Acceso a la Aplicación

Una vez que todos los servicios estén ejecutándose:

- **Aplicación principal**: http://localhost
- **Admin de Django**: http://localhost/admin
- **API REST**: http://localhost/api/
- **Health Check**: http://localhost/health/

### Credenciales por Defecto
- **Superusuario**: `admin` / `admin123`
- **Base de datos**: `root` / `123456`

## 📊 Monitoreo y Logs

### Ver Estado de Servicios
```bash
# Estado general
docker-compose ps

# Logs en tiempo real
docker-compose logs -f

# Logs de un servicio específico
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f celery
```

### Métricas de Recursos
```bash
# Uso de recursos
docker stats

# Información detallada
docker system df
```

## 🛠️ Comandos Útiles

### Gestión de Django
```bash
# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Recolectar archivos estáticos
docker-compose exec web python manage.py collectstatic

# Shell de Django
docker-compose exec web python manage.py shell

# Ejecutar tests
docker-compose exec web python manage.py test
```

### Gestión de Base de Datos
```bash
# Acceder a MySQL
docker-compose exec db mysql -u root -p

# Backup de la base de datos
docker-compose exec db mysqldump -u root -p reflexo > backup.sql

# Restaurar backup
docker-compose exec -T db mysql -u root -p reflexo < backup.sql
```

### Gestión de Celery
```bash
# Ver logs de Celery
docker-compose logs -f celery

# Ejecutar tarea manualmente
docker-compose exec web celery -A settings call tasks.debug_task

# Monitorear Celery
docker-compose exec web celery -A settings flower
```

## 🔍 Troubleshooting

### Problemas Comunes

#### 1. Puerto 3306 ya en uso
```bash
# Detener MySQL local
sudo service mysql stop
# O cambiar puerto en docker-compose.yml
```

#### 2. Puerto 80 ya en uso
```bash
# Detener servidor web local
sudo service apache2 stop
sudo service nginx stop
# O cambiar puerto en docker-compose.yml
```

#### 3. Error de permisos
```bash
# En Windows, ejecutar PowerShell como administrador
# En Linux/Mac, verificar permisos de archivos
chmod +x start.sh
```

#### 4. Contenedores no inician
```bash
# Verificar logs
docker-compose logs

# Reconstruir imágenes
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Limpieza y Reset
```bash
# Detener y eliminar contenedores
docker-compose down

# Eliminar volúmenes (¡CUIDADO! Elimina datos)
docker-compose down -v

# Limpieza completa
docker system prune -a
docker volume prune
```

## 📁 Estructura de Archivos Docker

```
.
├── Dockerfile                 # Imagen de la aplicación
├── docker-compose.yml         # Configuración principal
├── docker-compose.dev.yml     # Configuración desarrollo
├── docker-compose.prod.yml    # Configuración producción
├── entrypoint.sh             # Script de inicialización
├── start.sh                  # Script de inicio (Linux/Mac)
├── start.ps1                 # Script de inicio (Windows)
├── .dockerignore             # Archivos a ignorar
├── env.example               # Variables de entorno ejemplo
├── env.prod.example          # Variables de entorno producción
├── nginx/                    # Configuración Nginx
│   ├── nginx.conf
│   ├── nginx.prod.conf
│   ├── default.conf
│   ├── default.prod.conf
│   └── nginx.dev.conf
├── db/                       # Scripts de base de datos
│   └── init.sql
└── settings/                 # Configuración Django
    ├── settings.py
    ├── celery.py
    └── __init__.py
```

## 🔒 Seguridad

### Para Desarrollo
- Usar `DEBUG=True` solo en desarrollo
- Cambiar credenciales por defecto
- No exponer puertos innecesarios

### Para Producción
- Usar `DEBUG=False`
- Configurar `SECRET_KEY` segura
- Configurar SSL/TLS
- Usar credenciales fuertes
- Configurar firewalls
- Monitorear logs regularmente

## 📞 Soporte

Si encuentras problemas:

1. **Revisar logs**: `docker-compose logs`
2. **Verificar estado**: `docker-compose ps`
3. **Verificar red**: `docker network ls`
4. **Verificar volúmenes**: `docker volume ls`
5. **Revisar recursos**: `docker stats`

## 🎉 ¡Listo!

Tu aplicación Backend-Optimizacion está ahora ejecutándose completamente en Docker con:

- ✅ Django con Gunicorn
- ✅ MySQL 8.0
- ✅ Redis para cache y Celery
- ✅ Celery para tareas asíncronas
- ✅ Nginx como proxy reverso
- ✅ Configuración de seguridad
- ✅ Logging y monitoreo
- ✅ Health checks automáticos

¡Disfruta de tu aplicación! 🚀
