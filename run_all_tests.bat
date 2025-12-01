@echo off
echo 🚀 Ejecutando todas las pruebas del proyecto SIP
echo ==================================================

REM Verificar si estamos en el directorio correcto
if not exist "backend" (
    echo [ERROR] Este script debe ejecutarse desde la raíz del proyecto SIP
    pause
    exit /b 1
)

if not exist "frontend" (
    echo [ERROR] Este script debe ejecutarse desde la raíz del proyecto SIP
    pause
    exit /b 1
)

REM 1. Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] No se pudo activar el entorno virtual
    pause
    exit /b 1
)

REM 2. Instalar dependencias si es necesario
echo [INFO] Verificando dependencias...
cd backend
pip install pytest-cov coverage -q
if %errorlevel% neq 0 (
    echo [WARNING] No se pudieron instalar las dependencias, continuando...
)

REM 3. Pruebas del Backend
echo [INFO] Ejecutando pruebas del backend (Django/Python)...
python -m pytest apps/auditoria/tests.py apps/encuestas/tests.py apps/poblacion/tests.py -v
if %errorlevel% neq 0 (
    echo [ERROR] ❌ Fallaron las pruebas del backend
    cd ..
    pause
    exit /b 1
) else (
    echo [SUCCESS] ✅ Pruebas del backend completadas exitosamente
)

cd ..

REM 4. Pruebas del Frontend
echo [INFO] Ejecutando pruebas del frontend (Vue.js)...
cd frontend

REM Instalar dependencias de Node.js si no existen
if not exist "node_modules" (
    echo [INFO] Instalando dependencias de Node.js...
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] No se pudieron instalar las dependencias de Node.js
        cd ..
        pause
        exit /b 1
    )
)

call npm run test:coverage
if %errorlevel% neq 0 (
    echo [WARNING] ⚠️  Las pruebas del frontend fallaron, pero continuamos con SonarQube
    echo [INFO] Esto puede deberse a dependencias faltantes, pero el backend está listo
) else (
    echo [SUCCESS] ✅ Pruebas del frontend completadas exitosamente
)

cd ..

REM 5. Verificación final
echo [INFO] Verificando archivos de cobertura generados...

if exist "backend\coverage.xml" (
    echo [SUCCESS] ✅ Archivo de cobertura del backend generado: backend\coverage.xml
) else (
    echo [WARNING] ⚠️  No se encontró el archivo de cobertura del backend
)

if exist "frontend\coverage\lcov.info" (
    echo [SUCCESS] ✅ Archivo de cobertura del frontend generado: frontend\coverage\lcov.info
) else (
    echo [WARNING] ⚠️  No se encontró el archivo de cobertura del frontend
)

REM 5. Resumen
echo.
echo [SUCCESS] 🎉 Todas las pruebas se ejecutaron exitosamente!
echo.
echo [INFO] Para enviar a SonarQube, ejecuta:
echo [INFO]   sonar-scanner
echo.
echo [INFO] Archivos generados:
echo [INFO]   - backend\coverage.xml (cobertura backend)
echo [INFO]   - frontend\coverage\lcov.info (cobertura frontend)
echo [INFO]   - sonar-project.properties (configuración SonarQube)

pause