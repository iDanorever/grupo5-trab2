# 🚀 Configuración del Backend - Reflexo Perú

## 📋 Requisitos Previos

- **Python 3.8+**
- **MariaDB 10.5+** o **MySQL 8.0+**

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd Backend-Optimizacion
```

### 2. Crear entorno virtual
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

#### Crear base de datos en phpMyAdmin:
1. Abrir phpMyAdmin (http://localhost/phpmyadmin)
2. Crear nueva base de datos: `reflexo_v3_django`
3. Importar el archivo SQL con la estructura de tablas (si existe)

#### O crear base de datos vacía:
```sql
CREATE DATABASE reflexo_v3_django CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configurar variables de entorno
Editar `settings/settings.py` si es necesario:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'reflexo_v3_django',
        'USER': 'root',
        'PASSWORD': '',  # Cambiar si tienes contraseña
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 6. Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear superusuario
```bash
python manage.py createsuperuser
```

### 8. Iniciar servidor
```bash
python manage.py runserver
```

## 🌐 Acceso al sistema

- **Admin Django**: http://localhost:8000/admin/
- **API REST**: http://localhost:8000/api/

## 📚 Funcionalidades Implementadas

### ✅ Módulos Completos
- **Usuarios y Perfiles** (`users_profiles`)
- **Pacientes y Diagnósticos** (`patients_diagnoses`)
- **Terapeutas** (`therapists`)
- **Citas y Estados** (`appointments_status`)
- **Historias Clínicas** (`histories_configurations`)
- **Reportes de Empresa** (`company_reports`)
- **Geolocalización** (`ubi_geo`)
- **Arquitectura y Permisos** (`architect`)

### 🔧 Características Técnicas
- **Creación automática de tickets** al crear citas
- **Soft delete** en todos los modelos
- **APIs REST** completas con DRF
- **Autenticación JWT**
- **Filtros y búsqueda** avanzados
- **Validaciones** robustas
- **Documentación** automática de APIs

## 🎯 Endpoints Principales

### Citas
- `GET/POST /api/appointments/` - Listar/Crear citas
- `GET/PUT/DELETE /api/appointments/{id}/` - Gestionar cita específica

### Pacientes
- `GET/POST /api/patients/` - Listar/Crear pacientes
- `GET/PUT/DELETE /api/patients/{id}/` - Gestionar paciente específico

### Terapeutas
- `GET/POST /api/therapists/` - Listar/Crear terapeutas
- `GET/PUT/DELETE /api/therapists/{id}/` - Gestionar terapeuta específico

### Tickets
- `GET/POST /api/tickets/` - Listar/Crear tickets
- `GET/PUT/DELETE /api/tickets/{id}/` - Gestionar ticket específico

## 🔐 Autenticación

El sistema usa JWT (JSON Web Tokens) para autenticación:

```bash
# Obtener token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "tu_password"}'

# Usar token en requests
curl -H "Authorization: Bearer <tu_token>" \
  http://localhost:8000/api/appointments/
```

## 🐛 Solución de Problemas

### Error de conexión a base de datos
- Verificar que MariaDB/MySQL esté ejecutándose
- Confirmar credenciales en `settings.py`
- Verificar que la base de datos existe

### Error de migraciones
```bash
python manage.py makemigrations --empty <app_name>
python manage.py migrate --fake-initial
```

### Error de dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📞 Soporte

Para problemas técnicos, revisar:
1. Logs del servidor Django
2. Logs de la base de datos
3. Documentación de Django REST Framework

---

**¡Listo para usar! 🎉**
