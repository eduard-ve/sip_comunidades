#!/bin/bash

echo "🚀 Ejecutando todas las pruebas del proyecto SIP"
echo "=================================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Verificar si estamos en el directorio correcto
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Este script debe ejecutarse desde la raíz del proyecto SIP"
    exit 1
fi

# 1. Pruebas del Backend
print_status "Ejecutando pruebas del backend (Django/Python)..."
cd backend

if python -m pytest --cov=. --cov-report=xml --cov-config=.coveragerc apps/auditoria/tests.py apps/encuestas/tests.py apps/poblacion/tests.py apps/social/tests.py apps/salud/tests.py apps/usuarios/tests.py apps/reportes/tests.py -v; then
    print_success "✅ Pruebas del backend completadas exitosamente"
else
    print_error "❌ Fallaron las pruebas del backend"
    cd ..
    exit 1
fi

cd ..

# 2. Pruebas del Frontend
print_status "Ejecutando pruebas del frontend (Vue.js)..."
cd frontend

if npm run test:coverage; then
    print_success "✅ Pruebas del frontend completadas exitosamente"
else
    print_error "❌ Fallaron las pruebas del frontend"
    cd ..
    exit 1
fi

cd ..

# 3. Verificación final
print_status "Verificando archivos de cobertura generados..."

if [ -f "backend/coverage.xml" ]; then
    print_success "✅ Archivo de cobertura del backend generado: backend/coverage.xml"
else
    print_warning "⚠️  No se encontró el archivo de cobertura del backend"
fi

if [ -f "frontend/coverage/lcov.info" ]; then
    print_success "✅ Archivo de cobertura del frontend generado: frontend/coverage/lcov.info"
else
    print_warning "⚠️  No se encontró el archivo de cobertura del frontend"
fi

# 4. Resumen
print_success "🎉 Todas las pruebas se ejecutaron exitosamente!"
echo ""
print_status "Para enviar a SonarQube, ejecuta:"
print_status "  sonar-scanner"
echo ""
print_status "Archivos generados:"
print_status "  - backend/coverage.xml (cobertura backend)"
print_status "  - frontend/coverage/lcov.info (cobertura frontend)"
print_status "  - sonar-project.properties (configuración SonarQube)"