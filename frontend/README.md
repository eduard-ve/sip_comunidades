# SIP Comunidades - Frontend

Sistema de Información Poblacional para la gestión comunitaria del Guaviare. Una aplicación web para el seguimiento y gestión de datos poblacionales, salud comunitaria, programas sociales y más.

## 📋 Descripción del Proyecto

Este proyecto es un sistema integral de gestión comunitaria desarrollado para el departamento del Guaviare, Colombia. Permite a las autoridades locales y equipos de salud llevar un registro organizado de la población, actividades de salud preventiva, programas sociales y estadísticas comunitarias.

### 🎯 Objetivos Principales

- Facilitar el seguimiento de la información médica de las personas
- Apoyar las actividades preventivas y controles de salud
- Proporcionar una visión general del estado de salud de la población
- Gestionar programas sociales y beneficiarios
- Generar reportes y estadísticas en tiempo real

## 🛠️ Tecnologías Utilizadas

### Frontend
- **Vue 3** - Framework JavaScript progresivo
- **Vite** - Herramienta de construcción rápida
- **Pinia** - Gestión de estado
- **Vue Router** - Enrutamiento
- **Bootstrap 5** - Framework CSS
- **Chart.js** - Gráficos y visualizaciones
- **Axios** - Cliente HTTP

### Backend
- **Django 4.2** - Framework web Python
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de datos
- **Simple JWT** - Autenticación JWT

## 🚀 Instalación y Configuración

### Prerrequisitos

- Node.js (versión 16 o superior)
- npm o yarn
- Python 3.8+
- PostgreSQL (opcional, por defecto usa SQLite)

### Instalación del Frontend

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd sip_comunidades/frontend
   ```

2. **Instalar dependencias**
   ```bash
   npm install
   ```

3. **Configurar variables de entorno** (opcional)
   Crear archivo `.env` en la raíz del proyecto frontend:
   ```env
   VITE_API_BASE_URL=http://127.0.0.1:8000/api
   ```

4. **Ejecutar en modo desarrollo**
   ```bash
   npm run dev
   ```

5. **Construir para producción**
   ```bash
   npm run build
   ```

## 📁 Estructura del Proyecto

```
frontend/
├── public/                 # Archivos estáticos
├── src/
│   ├── assets/            # Recursos (CSS, imágenes, etc.)
│   ├── components/        # Componentes reutilizables
│   │   ├── comun/         # Componentes comunes
│   │   └── modulos/       # Componentes específicos de módulos
│   ├── router/            # Configuración de rutas
│   ├── stores/            # Gestión de estado (Pinia)
│   ├── views/             # Vistas/páginas
│   │   ├── dashboard/     # Dashboard principal
│   │   ├── poblacional/   # Gestión poblacional
│   │   ├── salud/         # Gestión de salud
│   │   ├── social/        # Gestión social
│   │   └── usuarios/      # Gestión de usuarios
│   └── services/          # Servicios API
├── index.html
├── package.json
└── vite.config.js
```

## 🎨 Características Principales

### 👥 Gestión Poblacional
- Registro completo de personas
- Árboles genealógicos
- Estadísticas demográficas
- Filtros avanzados

### 🏥 Gestión de Salud
- Registros médicos
- Alertas de salud
- Controles programados
- Vacunas y medicamentos
- Estadísticas de enfermedades

### 🤝 Gestión Social
- Programas sociales
- Beneficiarios
- Autoridades comunitarias
- Actividades comunitarias

### 📊 Dashboard y Reportes
- KPIs en tiempo real
- Gráficos interactivos
- Reportes personalizados
- Estadísticas poblacionales

## 🔐 Sistema de Roles

El sistema cuenta con tres niveles de acceso:

- **Administrador (admin)**: Acceso completo a todas las funcionalidades
- **Editor (editor)**: Permisos de edición y gestión
- **Invitado (invitado)**: Acceso de solo lectura

### Credenciales de Prueba
- **Admin**: `admin` / `admin123`
- **Editor**: `editor` / `editor123`
- **Invitado**: `invitado` / `invitado123`

## 🔧 Scripts Disponibles

```bash
# Desarrollo
npm run dev          # Inicia servidor de desarrollo
npm run build        # Construye para producción
npm run preview      # Vista previa de producción
npm run lint         # Ejecuta linter
```

## 🌐 API Backend

El frontend se conecta a una API REST desarrollada con Django. Los endpoints principales incluyen:

- `/api/usuarios/` - Gestión de usuarios
- `/api/poblacion/` - Datos poblacionales
- `/api/salud/` - Información de salud
- `/api/social/` - Programas sociales
- `/api/reportes/` - Generación de reportes

## 📱 Responsive Design

La aplicación está diseñada para ser completamente responsive, funcionando en:
- Escritorio
- Tablets
- Dispositivos móviles

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- Email: soporte@sipcomunidades.com
- Documentación: [Wiki del proyecto](https://github.com/sip-comunidades/wiki)

---

**Desarrollado con ❤️ para la comunidad del Guaviare**
