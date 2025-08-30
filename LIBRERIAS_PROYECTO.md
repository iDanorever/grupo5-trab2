# 📚 Librerías del Proyecto - Backend-Optimizacion

Documentación completa de todas las librerías y dependencias utilizadas en el proyecto Django.

## 📋 Índice
- [Librerías Principales](#-librerías-principales)
- [Dependencias de Django](#-dependencias-de-django)
- [Dependencias de xhtml2pdf](#-dependencias-de-xhtml2pdf)
- [Dependencias de Docker y Producción](#-dependencias-de-docker-y-producción)
- [Dependencias de Desarrollo y Testing](#-dependencias-de-desarrollo-y-testing)
- [Dependencias Transitivas](#-dependencias-transitivas)
- [Resumen de Versiones](#-resumen-de-versiones)

---

## 🎯 Librerías Principales

### **Django y REST Framework**
```bash
Django==5.2.5                    # Framework web principal
djangorestframework==3.14.0      # API REST para Django
djangorestframework-simplejwt==5.3.0  # Autenticación JWT
```

### **Extensiones de Django**
```bash
django-filter==23.5              # Filtros avanzados para Django
django-guardian==2.4.0           # Permisos por objeto
django-cors-headers==4.3.1       # Headers CORS para APIs
django-xhtml2pdf==0.0.3          # Generación de PDFs
django-celery-beat==2.8.0        # Tareas programadas con Celery
django-celery-results==2.5.1     # Almacenamiento de resultados de Celery
```

### **Base de Datos**
```bash
mysqlclient==2.2.0               # Cliente MySQL para Python
psycopg2-binary==2.9.9           # Cliente PostgreSQL (para Docker)
```

### **Procesamiento de Archivos**
```bash
xlsxwriter==3.1.9                # Generación de archivos Excel
Pillow==10.1.0                   # Procesamiento de imágenes
```

### **Configuración y Utilidades**
```bash
python-decouple==3.8             # Gestión de variables de entorno
whitenoise==6.6.0                # Servir archivos estáticos
```

---

## 🔧 Dependencias de Django

### **Dependencias Core de Django**
```bash
asgiref==3.8.1                   # Interfaz ASGI para Django
pytz==2024.2                     # Zonas horarias
sqlparse==0.5.1                  # Parser SQL para Django
```

### **Dependencias Opcionales**
```bash
six==1.16.0                      # Compatibilidad Python 2/3
```

---

## 📄 Dependencias de xhtml2pdf

### **Generación de PDFs**
```bash
xhtml2pdf==0.2.11                # Conversión HTML a PDF
reportlab==3.6.13                # Generación de PDFs (backend)
PyPDF2==3.0.1                    # Manipulación de PDFs
```

### **Procesamiento de Texto**
```bash
html5lib==1.1                    # Parser HTML5
arabic-reshaper==3.0.0           # Soporte para texto árabe
python-bidi==0.4.2               # Soporte para texto bidireccional
```

---

## 🐳 Dependencias de Docker y Producción

### **Servidor Web**
```bash
gunicorn==21.2.0                 # Servidor WSGI para producción
```

### **Cache y Cola de Mensajes**
```bash
redis==5.0.1                     # Cliente Redis
celery==5.3.4                    # Tareas asíncronas
```

---

## 🧪 Dependencias de Desarrollo y Testing

### **Testing Framework**
```bash
pytest==7.4.3                    # Framework de testing
pytest-django==4.7.0             # Plugin Django para pytest
```

### **Generación de Datos**
```bash
factory-boy==3.3.0               # Generación de datos de prueba
```

### **Cobertura de Código**
```bash
coverage==7.3.2                  # Medición de cobertura de código
```

---

## 🔗 Dependencias Transitivas

### **Dependencias de Django REST Framework**
```bash
markdown==3.5.1                  # Renderizado de Markdown
PyJWT==2.8.0                     # Implementación JWT
cryptography==41.0.7             # Criptografía para JWT
```

### **Dependencias de Celery**
```bash
click==8.1.7                     # CLI para Celery
click-didyoumean==0.3.0          # Sugerencias de comandos
click-plugins==1.1.1             # Sistema de plugins
click-repl==0.3.0                # REPL interactivo
prompt-toolkit==3.0.39           # Toolkit para interfaces CLI
wcwidth==0.2.12                  # Ancho de caracteres
kombu==5.3.4                     # Biblioteca de mensajería
amqp==5.2.0                      # Protocolo AMQP
vine==5.1.0                      # Promesas y futuros
billiard==4.2.0                  # Multiprocesamiento
```

### **Dependencias de Redis**
```bash
packaging==23.2                  # Utilidades de empaquetado
```

### **Dependencias de Pillow**
```bash
typing-extensions==4.8.0         # Extensiones de typing
```

### **Dependencias de ReportLab**
```bash
setuptools==68.2.2               # Herramientas de instalación
```

### **Dependencias de xlsxwriter**
```bash
# No tiene dependencias externas
```

### **Dependencias de pytest**
```bash
iniconfig==2.0.0                 # Configuración INI
packaging==23.2                  # Utilidades de empaquetado
pluggy==1.3.0                    # Sistema de plugins
```

### **Dependencias de factory-boy**
```bash
Faker==20.1.0                    # Generación de datos falsos
text-unidecode==1.3              # Normalización de texto
```

---

## 📊 Resumen de Versiones

### **Versiones Principales**
| Librería | Versión | Propósito |
|----------|---------|-----------|
| Django | 5.2.5 | Framework web |
| DRF | 3.14.0 | API REST |
| Celery | 5.3.4 | Tareas asíncronas |
| Redis | 5.0.1 | Cache y broker |
| MySQL | 2.2.0 | Cliente MySQL |
| Pillow | 10.1.0 | Procesamiento de imágenes |

### **Versiones de Testing**
| Librería | Versión | Propósito |
|----------|---------|-----------|
| pytest | 7.4.3 | Framework testing |
| factory-boy | 3.3.0 | Datos de prueba |
| coverage | 7.3.2 | Cobertura de código |

### **Versiones de Producción**
| Librería | Versión | Propósito |
|----------|---------|-----------|
| gunicorn | 21.2.0 | Servidor WSGI |
| whitenoise | 6.6.0 | Archivos estáticos |
| python-decouple | 3.8 | Variables de entorno |

---

## 🔍 Análisis de Dependencias

### **Dependencias Críticas**
- **Django 5.2.5**: Versión LTS, soporte hasta 2026
- **DRF 3.14.0**: Compatible con Django 5.2
- **Celery 5.3.4**: Última versión estable
- **Redis 5.0.1**: Cliente compatible con Redis 6+

### **Dependencias de Seguridad**
- **cryptography 41.0.7**: Criptografía moderna
- **PyJWT 2.8.0**: Implementación JWT segura
- **mysqlclient 2.2.0**: Cliente MySQL actualizado

### **Compatibilidad**
- **Python**: 3.8+ (recomendado 3.11+)
- **Django**: 5.2.5 (LTS)
- **MySQL**: 8.0+
- **Redis**: 6.0+

---

## 📦 Instalación

### **Instalación Completa**
```bash
pip install -r requirements.txt
```

### **Instalación por Categorías**

#### **Solo Producción**
```bash
pip install Django==5.2.5 djangorestframework==3.14.0 mysqlclient==2.2.0 gunicorn==21.2.0 redis==5.0.1 celery==5.3.4
```

#### **Solo Desarrollo**
```bash
pip install pytest==7.4.3 pytest-django==4.7.0 factory-boy==3.3.0 coverage==7.3.2
```

#### **Solo PDFs**
```bash
pip install django-xhtml2pdf==0.0.3 xhtml2pdf==0.2.11 reportlab==3.6.13
```

---

## ⚠️ Notas Importantes

### **Conflictos de Versiones Resueltos**
- `django-celery-beat==2.8.0`: Compatible con Django 5.2.5
- `reportlab==3.6.13`: Compatible con xhtml2pdf
- `python-bidi==0.4.2`: Versión estable para texto bidireccional

### **Dependencias Opcionales**
- `psycopg2-binary`: Solo para entornos con PostgreSQL
- `pytest*`: Solo para desarrollo y testing
- `factory-boy`: Solo para generación de datos de prueba

### **Actualizaciones Recomendadas**
- Mantener Django en versión LTS
- Actualizar dependencias de seguridad regularmente
- Verificar compatibilidad antes de actualizar

---

## 🔧 Comandos Útiles

### **Verificar Dependencias**
```bash
pip list
pip show django
pip show djangorestframework
```

### **Verificar Conflictos**
```bash
pip check
```

### **Generar requirements.txt**
```bash
pip freeze > requirements.txt
```

### **Instalar en Entorno Virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## 📈 Estadísticas

- **Total de librerías principales**: 44
- **Dependencias transitivas**: ~150+
- **Tamaño total**: ~500MB (con dependencias)
- **Tiempo de instalación**: ~5-10 minutos

---

*Documentación generada para Backend-Optimizacion - Análisis completo de dependencias*
