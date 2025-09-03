# 🚀 Backend-Optimizacion - Guía de Producción

## 📋 Descripción
Este proyecto ha sido optimizado para producción, eliminando archivos innecesarios y configurando solo lo esencial para el despliegue en un entorno productivo.

## 🗂️ Estructura del Proyecto (Producción)

```
Backend-Optimizacion/
├── manage.py                          # Comando principal de Django
├── requirements.txt                   # Dependencias de producción
├── requirements.dev.txt               # Dependencias de desarrollo (backup)
├── Dockerfile                         # Construcción de imagen Docker
├── docker-compose.prod.yml           # Orquestación de producción
├── docker-compose.prod.override.yml  # Personalizaciones de producción
├── entrypoint.sh                      # Script de inicialización
├── .dockerignore                      # Exclusión de archivos en Docker
├── .env                              # Variables de entorno (crear desde env.prod.example)
├── env.prod.example                  # Plantilla de variables de entorno
├── start-prod.ps1                    # Script de inicio para Windows
├── start-prod.sh                     # Script de inicio para Linux/Mac
├── settings/                          # Configuración de Django
├── nginx/                            # Configuración de Nginx
│   ├── default.prod.conf             # Configuración de sitio para producción
│   └── nginx.prod.conf               # Configuración principal de Nginx
├── db/                               # Scripts de base de datos
│   └── init.sql                      # Inicialización de BD
├── logs/                             # Directorio de logs
├── staticfiles/                       # Archivos estáticos
├── media/                            # Archivos de medios
└── [aplicaciones_django]/            # Módulos de la aplicación
```

## 🚀 Inicio Rápido

### Windows (PowerShell)
```powershell
.\start-prod.ps1
```

### Linux/Mac (Bash)
```bash
chmod +x start-prod.sh
./start-prod.sh
```

### Manual
```bash
# 1. Configurar variables de entorno
cp env.prod.example .env
# Editar .env con valores de producción

# 2. Construir y ejecutar
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

## ⚙️ Configuración de Producción

### 1. Variables de Entorno (.env)
```bash
# Copiar plantilla
cp env.prod.example .env

# Editar con valores reales
nano .env
```

**Variables críticas a configurar:**
- `SECRET_KEY`: Clave secreta única y segura
- `DATABASE_PASSWORD`: Contraseña fuerte para MySQL
- `ALLOWED_HOSTS`: Dominios permitidos (separados por comas)
- `DEBUG`: Debe ser `False` en producción

### 2. Base de Datos
- MySQL 8.0 configurado automáticamente
- Puerto: 3306 (solo acceso local)
- Volumen persistente: `mysql_data_prod`

### 3. Redis
- Redis 7 para Celery
- Puerto: 6379 (solo acceso local)
- Volumen persistente: `redis_data_prod`

### 4. Nginx
- Configurado para producción
- Soporte para SSL/TLS
- Servir archivos estáticos y medios
- Puerto 80 (HTTP) y 443 (HTTPS)

## 🔧 Comandos Útiles

### Gestión de Servicios
```bash
# Ver estado
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f

# Reiniciar servicios
docker-compose -f docker-compose.prod.yml restart

# Detener servicios
docker-compose -f docker-compose.prod.yml down

# Reconstruir y reiniciar
docker-compose -f docker-compose.prod.yml up -d --build
```

### Acceso a Contenedores
```bash
# Shell del contenedor web
docker-compose -f docker-compose.prod.yml exec web bash

# Shell de la base de datos
docker-compose -f docker-compose.prod.yml exec db mysql -u root -p

# Logs de Nginx
docker-compose -f docker-compose.prod.yml exec nginx tail -f /var/log/nginx/access.log
```

### Django Management
```bash
# Ejecutar comandos de Django
docker-compose -f docker-compose.prod.yml exec web python manage.py [comando]

# Crear superusuario
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Recolectar archivos estáticos
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic

# Ejecutar migraciones
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

## 🔒 Seguridad en Producción

### 1. Variables de Entorno
- ✅ Usar contraseñas fuertes
- ✅ Cambiar SECRET_KEY por defecto
- ✅ Configurar ALLOWED_HOSTS específicos
- ✅ Deshabilitar DEBUG

### 2. Base de Datos
- ✅ Contraseñas fuertes para MySQL
- ✅ Acceso solo desde contenedores
- ✅ Volúmenes persistentes

### 3. Nginx
- ✅ Configuración de seguridad
- ✅ Headers de seguridad
- ✅ Rate limiting (configurar según necesidades)

### 4. SSL/TLS
- ✅ Configurar certificados SSL
- ✅ Redirigir HTTP a HTTPS
- ✅ Headers de seguridad

## 📊 Monitoreo y Logs

### Logs Disponibles
- **Django**: `/app/logs/` en contenedor web
- **Nginx**: `/var/log/nginx/` en contenedor nginx
- **MySQL**: Logs del contenedor MySQL
- **Redis**: Logs del contenedor Redis

### Health Checks
- **Web**: `http://localhost/health/`
- **Base de datos**: Ping automático
- **Redis**: Ping automático

## 🚨 Solución de Problemas

### Servicio no inicia
```bash
# Ver logs específicos
docker-compose -f docker-compose.prod.yml logs [servicio]

# Verificar estado
docker-compose -f docker-compose.prod.yml ps

# Reconstruir imagen
docker-compose -f docker-compose.prod.yml build --no-cache [servicio]
```

### Base de datos no conecta
```bash
# Verificar estado del contenedor
docker-compose -f docker-compose.prod.yml exec db mysqladmin ping

# Ver logs de MySQL
docker-compose -f docker-compose.prod.yml logs db
```

### Nginx no sirve archivos
```bash
# Verificar configuración
docker-compose -f docker-compose.prod.yml exec nginx nginx -t

# Ver logs de Nginx
docker-compose -f docker-compose.prod.yml logs nginx
```

## 📞 Soporte

Para problemas específicos:
1. Revisar logs del servicio afectado
2. Verificar configuración en `.env`
3. Confirmar que Docker esté ejecutándose
4. Verificar puertos disponibles

## 🔄 Actualizaciones

### Actualizar Código
```bash
# 1. Hacer pull del código actualizado
git pull origin main

# 2. Reconstruir y reiniciar
docker-compose -f docker-compose.prod.yml up -d --build

# 3. Ejecutar migraciones si es necesario
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### Actualizar Dependencias
```bash
# 1. Actualizar requirements.txt
# 2. Reconstruir imagen
docker-compose -f docker-compose.prod.yml build --no-cache web

# 3. Reiniciar servicios
docker-compose -f docker-compose.prod.yml up -d
```

---

**⚠️ IMPORTANTE**: Este es un entorno de PRODUCCIÓN. Siempre haz backup de la base de datos antes de realizar cambios importantes.
