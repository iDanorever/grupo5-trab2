#!/bin/bash

# Script de inicio para PRODUCCIÓN - Backend-Optimizacion
echo "🚀 Iniciando Backend-Optimizacion en PRODUCCIÓN..."

# Verificar si Docker está ejecutándose
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está ejecutándose. Por favor, inicia Docker."
    exit 1
fi

# Verificar si existe el archivo .env
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env desde env.prod.example..."
    cp env.prod.example .env
    echo "✅ Archivo .env creado. ¡IMPORTANTE: Edita las variables de entorno para producción!"
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
show_progress "Construyendo imágenes Docker para PRODUCCIÓN"
if docker-compose -f docker-compose.prod.yml build; then
    show_success "Imágenes construidas correctamente"
else
    show_error "Error al construir las imágenes"
    exit 1
fi

# Iniciar los servicios de producción
show_progress "Iniciando servicios de PRODUCCIÓN"
if docker-compose -f docker-compose.prod.yml up -d; then
    show_success "Servicios de producción iniciados correctamente"
else
    show_error "Error al iniciar los servicios"
    exit 1
fi

# Esperar un momento para que los servicios se inicialicen
show_progress "Esperando que los servicios se inicialicen"
sleep 15

# Verificar el estado de los contenedores
show_progress "Verificando estado de los contenedores"
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    show_success "Todos los contenedores están ejecutándose"
else
    show_error "Algunos contenedores no están ejecutándose"
    echo "📋 Estado de los contenedores:"
    docker-compose -f docker-compose.prod.yml ps
    exit 1
fi

# Mostrar información de acceso
echo ""
echo "🎉 ¡Backend-Optimizacion está ejecutándose en PRODUCCIÓN!"
echo ""
echo "📱 URLs de acceso:"
echo "   • Aplicación principal: http://localhost"
echo "   • Admin de Django: http://localhost/admin"
echo "   • API REST: http://localhost/api/"
echo ""
echo "🔑 IMPORTANTE: Configura las credenciales en el archivo .env"
echo ""
echo "📋 Comandos útiles:"
echo "   • Ver logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "   • Detener servicios: docker-compose -f docker-compose.prod.yml down"
echo "   • Reiniciar servicios: docker-compose -f docker-compose.prod.yml restart"
echo "   • Acceder al shell: docker-compose -f docker-compose.prod.yml exec web bash"
echo ""
echo "🔍 Para ver los logs en tiempo real, ejecuta:"
echo "   docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "⚠️  RECUERDA: Este es un entorno de PRODUCCIÓN"
echo "   • Configura variables de entorno seguras"
echo "   • Usa contraseñas fuertes"
echo "   • Configura SSL/TLS"
echo ""
