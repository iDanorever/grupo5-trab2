# Script de inicio para PRODUCCIÓN - Backend-Optimizacion
Write-Host "🚀 Iniciando Backend-Optimizacion en PRODUCCIÓN..." -ForegroundColor Green

# Verificar si Docker está ejecutándose
try {
    docker info | Out-Null
    Write-Host "✅ Docker está ejecutándose" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Docker no está ejecutándose. Por favor, inicia Docker Desktop." -ForegroundColor Red
    exit 1
}

# Verificar si existe el archivo .env
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creando archivo .env desde env.prod.example..." -ForegroundColor Yellow
    Copy-Item "env.prod.example" ".env"
    Write-Host "✅ Archivo .env creado. ¡IMPORTANTE: Edita las variables de entorno para producción!" -ForegroundColor Green
}

# Función para mostrar el progreso
function Show-Progress {
    param([string]$Message)
    Write-Host "⏳ $Message..." -ForegroundColor Yellow
}

# Función para mostrar éxito
function Show-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

# Función para mostrar error
function Show-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# Construir las imágenes
Show-Progress "Construyendo imágenes Docker para PRODUCCIÓN"
try {
    docker-compose -f docker-compose.prod.yml build
    Show-Success "Imágenes construidas correctamente"
} catch {
    Show-Error "Error al construir las imágenes"
    exit 1
}

# Iniciar los servicios de producción
Show-Progress "Iniciando servicios de PRODUCCIÓN"
try {
    docker-compose -f docker-compose.prod.yml up -d
    Show-Success "Servicios de producción iniciados correctamente"
} catch {
    Show-Error "Error al iniciar los servicios"
    exit 1
}

# Esperar un momento para que los servicios se inicialicen
Show-Progress "Esperando que los servicios se inicialicen"
Start-Sleep -Seconds 15

# Verificar el estado de los contenedores
Show-Progress "Verificando estado de los contenedores"
try {
    $containers = docker-compose -f docker-compose.prod.yml ps
    if ($containers -match "Up") {
        Show-Success "Todos los contenedores están ejecutándose"
    } else {
        Show-Error "Algunos contenedores no están ejecutándose"
        Write-Host "📋 Estado de los contenedores:" -ForegroundColor Yellow
        docker-compose -f docker-compose.prod.yml ps
        exit 1
    }
} catch {
    Show-Error "Error al verificar el estado de los contenedores"
    exit 1
}

# Mostrar información de acceso
Write-Host ""
Write-Host "🎉 ¡Backend-Optimizacion está ejecutándose en PRODUCCIÓN!" -ForegroundColor Green
Write-Host ""
Write-Host "📱 URLs de acceso:" -ForegroundColor Cyan
Write-Host "   • Aplicación principal: http://localhost" -ForegroundColor White
Write-Host "   • Admin de Django: http://localhost/admin" -ForegroundColor White
Write-Host "   • API REST: http://localhost/api/" -ForegroundColor White
Write-Host ""
Write-Host "🔑 IMPORTANTE: Configura las credenciales en el archivo .env" -ForegroundColor Red
Write-Host ""
Write-Host "📋 Comandos útiles:" -ForegroundColor Cyan
Write-Host "   • Ver logs: docker-compose -f docker-compose.prod.yml logs -f" -ForegroundColor White
Write-Host "   • Detener servicios: docker-compose -f docker-compose.prod.yml down" -ForegroundColor White
Write-Host "   • Reiniciar servicios: docker-compose -f docker-compose.prod.yml restart" -ForegroundColor White
Write-Host "   • Acceder al shell: docker-compose -f docker-compose.prod.yml exec web bash" -ForegroundColor White
Write-Host ""
Write-Host "🔍 Para ver los logs en tiempo real, ejecuta:" -ForegroundColor Yellow
Write-Host "   docker-compose -f docker-compose.prod.yml logs -f" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  RECUERDA: Este es un entorno de PRODUCCIÓN" -ForegroundColor Red
Write-Host "   • Configura variables de entorno seguras" -ForegroundColor Red
Write-Host "   • Usa contraseñas fuertes" -ForegroundColor Red
Write-Host "   • Configura SSL/TLS" -ForegroundColor Red
Write-Host ""
