#!/bin/bash

# Script de inicio rápido para Backend-Optimizacion
echo "🚀 Iniciando Backend-Optimizacion con Docker..."

# Verificar si Docker está ejecutándose
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está ejecutándose. Por favor, inicia Docker Desktop."
    exit 1
fi

# Verificar si existe el archivo .env
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env desde env.example..."
    cp env.example .env
    echo "✅ Archivo .env creado. Puedes editarlo si es necesario."
fi

# Función para mostrar el progreso
show_progress() {
    echo "⏳ $1..."
}

# Función para mostrar éxito
show_success() {
    echo "✅ $1"
}

# Función para mostrar error
show_error() {
    echo "❌ $1"
}

# Construir las imágenes
show_progress "Construyendo imágenes Docker"
if docker-compose build; then
    show_success "Imágenes construidas correctamente"
else
    show_error "Error al construir las imágenes"
    exit 1
fi

# Iniciar los servicios
show_progress "Iniciando servicios"
if docker-compose up -d; then
    show_success "Servicios iniciados correctamente"
else
    show_error "Error al iniciar los servicios"
    exit 1
fi

# Esperar un momento para que los servicios se inicialicen
show_progress "Esperando que los servicios se inicialicen"
sleep 10

# Verificar el estado de los contenedores
show_progress "Verificando estado de los contenedores"
if docker-compose ps | grep -q "Up"; then
    show_success "Todos los contenedores están ejecutándose"
else
    show_error "Algunos contenedores no están ejecutándose"
    echo "📋 Estado de los contenedores:"
    docker-compose ps
    exit 1
fi

# Mostrar información de acceso
echo ""
echo "🎉 ¡Backend-Optimizacion está listo!"
echo ""
echo "📱 URLs de acceso:"
echo "   • Aplicación principal: http://localhost"
echo "   • Admin de Django: http://localhost/admin"
echo "   • API REST: http://localhost/api/"
echo ""
echo "🔑 Credenciales por defecto:"
echo "   • Superusuario: admin / admin123"
echo "   • Base de datos: root / 123456"
echo ""
echo "📋 Comandos útiles:"
echo "   • Ver logs: docker-compose logs -f"
echo "   • Detener servicios: docker-compose down"
echo "   • Reiniciar servicios: docker-compose restart"
echo "   • Acceder al shell: docker-compose exec web bash"
echo ""
echo "🔍 Para ver los logs en tiempo real, ejecuta:"
echo "   docker-compose logs -f"
echo ""
