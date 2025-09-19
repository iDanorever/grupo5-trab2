# 🖥️ Backend - ReflexoPeru 🚀

Este directorio contiene toda la lógica del servidor y la implementación de la API para sincronizar citas entre ReflexoPeru v3 y Go High Level (GHL), desarrollado en Visual Studio.

---

## 📦 Contenido principal

- Proyecto Django desarrollado en Visual Studio 🐍  
- Modelos para la base de datos local (modelo Cita) 📊  
- Importación y transformación de datos desde ReflexoPeru versión 3 🔄  
- Envío de citas al endpoint GHL con calendarId correcto 📅  
- Manejo de autenticación y seguridad en llamadas API 🔒  
- Pruebas unitarias e integración para asegurar la calidad ✅

---

## ⚙️ Instrucciones para instalar y ejecutar

1. Abre Visual Studio y carga el proyecto en la carpeta backend.  
2. Instala las dependencias necesarias usando la terminal integrada:  

pip install -r requirements.txt

3. Configura las variables de entorno para las credenciales y URLs GHL en Visual Studio 🔧  
4. Ejecuta migraciones para la base de datos local:  

python manage.py migrate

5. Levanta el servidor Django para desarrollo y pruebas:  

python manage.py runserver

6. Usa Postman o Thunder Client para validar los endpoints y la sincronización de citas 📡

---

## 🎯 Objetivo

Desarrollar una API robusta y segura en Django, usando Visual Studio, que sincronice citas médicas entre ReflexoPeru y GHL manteniendo datos consistentes en ambas plataformas.

