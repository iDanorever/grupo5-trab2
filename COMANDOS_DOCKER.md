# 🐳 Comandos Docker - Backend-Optimizacion

Documentación completa de comandos para gestionar el proyecto Dockerizado.

## 📋 Índice
- [Iniciar Servicios](#-iniciar-servicios)
- [Detener Servicios](#-detener-servicios)
- [Monitorear Servicios](#-monitorear-servicios)
- [Logs y Debugging](#-logs-y-debugging)
- [Gestión de Imágenes](#-gestión-de-imágenes)
- [Gestión de Volúmenes](#-gestión-de-volúmenes)
- [Comandos de Desarrollo](#-comandos-de-desarrollo)
- [Comandos de Producción](#-comandos-de-producción)
- [Troubleshooting](#-troubleshooting)

---

## 🚀 Iniciar Servicios

### **Iniciar todos los servicios en segundo plano (recomendado)**
```bash
docker-compose up -d
```

### **Iniciar y ver logs en tiempo real**
```bash
docker-compose up
```

### **Iniciar servicios específicos**
```bash
# Solo Django y Nginx
docker-compose up -d web nginx

# Solo servicios de backend
docker-compose up -d web redis

# Solo Celery
docker-compose up -d celery celery-beat
```

### **Iniciar con rebuild forzado**
```bash
docker-compose up -d --build
```

---

## 🛑 Detener Servicios

### **Detener todos los servicios**
```bash
docker-compose down
```

### **Detener y eliminar volúmenes**
```bash
docker-compose down -v
```

### **Detener y eliminar imágenes**
```bash
docker-compose down --rmi all
```

### **Detener servicios específicos**
```bash
docker-compose stop web
docker-compose stop nginx
docker-compose stop redis
```

---

## 📊 Monitorear Servicios

### **Ver estado de todos los contenedores**
```bash
docker-compose ps
```

### **Ver información detallada de servicios**
```bash
docker-compose ps -a
```

### **Ver recursos de contenedores**
```bash
docker stats
```

### **Ver información de un servicio específico**
```bash
docker-compose ps web
docker-compose ps nginx
docker-compose ps redis
```

---

## 📝 Logs y Debugging

### **Ver logs de todos los servicios**
```bash
docker-compose logs
```

### **Ver logs de un servicio específico**
```bash
docker-compose logs web
docker-compose logs nginx
docker-compose logs redis
docker-compose logs celery
docker-compose logs celery-beat
```

### **Ver logs en tiempo real (follow)**
```bash
docker-compose logs -f
docker-compose logs -f web
docker-compose logs -f nginx
```

### **Ver últimas N líneas de logs**
```bash
docker-compose logs --tail=50 web
docker-compose logs --tail=100 nginx
```

### **Ver logs con timestamps**
```bash
docker-compose logs -t web
```

---

## 🏗️ Gestión de Imágenes

### **Construir todas las imágenes**
```bash
docker-compose build
```

### **Construir imagen específica**
```bash
docker-compose build web
docker-compose build celery
```

### **Construir sin cache**
```bash
docker-compose build --no-cache
docker-compose build --no-cache web
```

### **Ver imágenes del proyecto**
```bash
docker-compose images
```

### **Eliminar imágenes no utilizadas**
```bash
docker image prune
docker image prune -a
```

---

## 💾 Gestión de Volúmenes

### **Ver volúmenes del proyecto**
```bash
docker-compose volume ls
```

### **Ver información de volúmenes**
```bash
docker volume ls
docker volume inspect backend-optimizacion_static_volume
```

### **Eliminar volúmenes**
```bash
docker-compose down -v
docker volume rm backend-optimizacion_static_volume
```

### **Backup de volúmenes**
```bash
docker run --rm -v backend-optimizacion_redis_data:/data -v $(pwd):/backup alpine tar czf /backup/redis_backup.tar.gz -C /data .
```

---

## 🔧 Comandos de Desarrollo

### **Ejecutar comandos dentro de contenedores**
```bash
# Ejecutar shell en Django
docker-compose exec web bash

# Ejecutar Python en Django
docker-compose exec web python manage.py shell

# Ejecutar comandos Django
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py createsuperuser
```

### **Ver archivos dentro de contenedores**
```bash
docker-compose exec web ls -la
docker-compose exec web cat /app/settings/settings.py
```

### **Copiar archivos desde/hacia contenedores**
```bash
docker cp reflexo_django:/app/logs/ ./local_logs/
docker cp ./local_file.txt reflexo_django:/app/
```

### **Reiniciar servicios específicos**
```bash
docker-compose restart web
docker-compose restart nginx
docker-compose restart redis
```

---

## 🚀 Comandos de Producción

### **Iniciar en modo producción**
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### **Verificar health checks**
```bash
docker-compose ps
curl http://localhost/health/
```

### **Escalar servicios**
```bash
docker-compose up -d --scale web=3
docker-compose up -d --scale celery=2
```

### **Backup completo**
```bash
# Backup de la base de datos
mysqldump -u root -p123456 reflexo > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup de volúmenes
docker run --rm -v backend-optimizacion_static_volume:/data -v $(pwd):/backup alpine tar czf /backup/static_backup.tar.gz -C /data .
```

---

## 🔍 Troubleshooting

### **Verificar conectividad de red**
```bash
docker-compose exec web ping redis
docker-compose exec web ping host.docker.internal
```

### **Verificar variables de entorno**
```bash
docker-compose exec web env | grep DATABASE
docker-compose exec web env | grep REDIS
```

### **Verificar logs de errores**
```bash
docker-compose logs --tail=100 web | grep ERROR
docker-compose logs --tail=100 nginx | grep error
```

### **Reiniciar todo desde cero**
```bash
docker-compose down -v --rmi all
docker system prune -a
docker-compose up -d --build
```

### **Verificar espacio en disco**
```bash
docker system df
docker volume ls
```

### **Limpiar recursos no utilizados**
```bash
docker system prune
docker system prune -a
docker volume prune
```

---

## 🌐 Acceso a la Aplicación

Una vez iniciados los servicios:

- **🌐 Aplicación principal:** http://localhost
- **🔧 Admin de Django:** http://localhost/admin/
- **📡 API de Django:** http://localhost:8000/
- **📊 Redis (opcional):** http://localhost:6379

### **Credenciales del Superusuario:**
- **📧 Email:** `admin@reflexo.com`
- **🔑 Contraseña:** `admin123456`
- **👤 Usuario:** `admin`
- **📄 Documento:** `12345678`

---

## 📋 Comandos Rápidos de Referencia

```bash
# Iniciar proyecto
docker-compose up -d

# Ver estado
docker-compose ps

# Ver logs
docker-compose logs -f web

# Detener proyecto
docker-compose down

# Reiniciar
docker-compose restart

# Reconstruir
docker-compose build --no-cache
```

---

## ⚠️ Notas Importantes

1. **Base de datos:** El proyecto está configurado para usar tu MySQL local en el puerto 3306
2. **Puertos utilizados:**
   - 80: Nginx
   - 8000: Django
   - 6379: Redis
   - 443: Nginx (HTTPS)
3. **Volúmenes:** Los archivos estáticos y media se almacenan en volúmenes Docker
4. **Red:** Los servicios se comunican a través de la red `reflexo_network`

---

## 🆘 Comandos de Emergencia

### **Parada de emergencia**
```bash
docker-compose kill
docker-compose down --remove-orphans
```

### **Recuperación completa**
```bash
docker-compose down -v --rmi all
docker system prune -a --volumes
docker-compose up -d --build
```

---

*Documentación generada para Backend-Optimizacion - Proyecto Django Dockerizado*
