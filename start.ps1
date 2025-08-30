# Script de inicio rápido para Backend-Optimizacion (PowerShell)
Write-Host "🚀 Iniciando Backend-Optimizacion con Docker..." -ForegroundColor Green

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
    Write-Host "📝 Creando archivo .env desde env.example..." -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
    Write-Host "✅ Archivo .env creado. Puedes editarlo si es necesario." -ForegroundColor Green
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
Show-Progress "Construyendo imágenes Docker"
try {
    docker-compose build
    Show-Success "Imágenes construidas correctamente"
} catch {
    Show-Error "Error al construir las imágenes"
    exit 1
}

# Iniciar los servicios
Show-Progress "Iniciando servicios"
try {
    docker-compose up -d
    Show-Success "Servicios iniciados correctamente"
} catch {
    Show-Error "Error al iniciar los servicios"
    exit 1
}

# Esperar un momento para que los servicios se inicialicen
Show-Progress "Esperando que los servicios se inicialicen"
Start-Sleep -Seconds 10

# Verificar el estado de los contenedores
Show-Progress "Verificando estado de los contenedores"
try {
    $containers = docker-compose ps
    if ($containers -match "Up") {
        Show-Success "Todos los contenedores están ejecutándose"
    } else {
        Show-Error "Algunos contenedores no están ejecutándose"
        Write-Host "📋 Estado de los contenedores:" -ForegroundColor Yellow
        docker-compose ps
        exit 1
    }
} catch {
    Show-Error "Error al verificar el estado de los contenedores"
    exit 1
}

# Mostrar información de acceso
Write-Host ""
Write-Host "🎉 ¡Backend-Optimizacion está listo!" -ForegroundColor Green
Write-Host ""
Write-Host "📱 URLs de acceso:" -ForegroundColor Cyan
Write-Host "   • Aplicación principal: http://localhost" -ForegroundColor White
Write-Host "   • Admin de Django: http://localhost/admin" -ForegroundColor White
Write-Host "   • API REST: http://localhost/api/" -ForegroundColor White
Write-Host ""
Write-Host "🔑 Credenciales por defecto:" -ForegroundColor Cyan
Write-Host "   • Superusuario: admin / admin123" -ForegroundColor White
Write-Host "   • Base de datos: root / 123456" -ForegroundColor White
Write-Host ""
Write-Host "📋 Comandos útiles:" -ForegroundColor Cyan
Write-Host "   • Ver logs: docker-compose logs -f" -ForegroundColor White
Write-Host "   • Detener servicios: docker-compose down" -ForegroundColor White
Write-Host "   • Reiniciar servicios: docker-compose restart" -ForegroundColor White
Write-Host "   • Acceder al shell: docker-compose exec web bash" -ForegroundColor White
Write-Host ""
Write-Host "🔍 Para ver los logs en tiempo real, ejecuta:" -ForegroundColor Yellow
Write-Host "   docker-compose logs -f" -ForegroundColor White
Write-Host ""
