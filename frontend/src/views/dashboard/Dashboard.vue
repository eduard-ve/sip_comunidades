<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);">

    <!-- Header Superior Fijo -->
    <div class="position-sticky top-0 bg-white border-bottom border-secondary shadow-sm" style="z-index: 50;">
      <div class="container-fluid px-4 py-3" style="max-width: 1800px;">
        <div class="d-flex align-items-center justify-content-center">
          <div class="d-flex align-items-center gap-3">
            <div class="bg-primary rounded-4 d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;">
              <i class="bi bi-people-fill text-white fs-5"></i>
            </div>
            <div class="text-center">
              <h1 class="fs-3 fw-bold text-dark mb-0">Dashboard Poblacional</h1>
              <p class="fs-6 text-muted mb-0">{{ nombreComunidad }} • {{ currentYear }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container-fluid px-4 py-3" style="max-width: 1800px;">

       <!-- Hero Metrics - 4 Columnas -->
       <div class="row g-3 mb-3">
        <div class="col-12 col-sm-6 col-lg-3">
           <div class="bg-white rounded-4 shadow-sm border border-light p-3 text-center">
             <div class="circular-progress position-relative d-inline-block mb-3" style="width: 120px; height: 120px;">
               <svg width="120" height="120" viewBox="0 0 120 120">
                 <circle cx="60" cy="60" r="50" stroke="#e6e6e6" stroke-width="8" fill="none" />
                 <circle cx="60" cy="60" r="50" :stroke="heroMetrics.poblacion.trend >= 0 ? '#10b981' : '#ef4444'" stroke-width="8" fill="none" stroke-dasharray="314.16" :stroke-dashoffset="314.16 - (Math.abs(heroMetrics.poblacion.trend)/100)*314.16" transform="rotate(-90 60 60)" stroke-linecap="round" />
               </svg>
               <div class="position-absolute top-50 start-50 translate-middle">
                 <div class="fs-4 fw-bold" :class="heroMetrics.poblacion.trend >= 0 ? 'text-success' : 'text-danger'">{{ Math.abs(heroMetrics.poblacion.trend) }}%</div>
               </div>
             </div>
             <div class="display-6 fw-bold mb-2 text-primary">{{ heroMetrics.poblacion.value }}</div>
             <div class="fs-6 fw-bold text-secondary text-uppercase mb-1">{{ heroMetrics.poblacion.label }}</div>
             <div class="fs-6 text-muted">{{ heroMetrics.poblacion.sublabel }}</div>
           </div>
         </div>
        <div class="col-12 col-sm-6 col-lg-3">
          <div class="bg-white rounded-4 shadow-sm border border-light p-3 text-center">
            <div class="circular-progress position-relative d-inline-block mb-3" style="width: 120px; height: 120px;">
              <svg width="120" height="120" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="50" stroke="#e6e6e6" stroke-width="8" fill="none" />
                <circle cx="60" cy="60" r="50" :stroke="heroMetrics.familiar.trend >= 0 ? '#10b981' : '#ef4444'" stroke-width="8" fill="none" stroke-dasharray="314.16" :stroke-dashoffset="314.16 - (Math.abs(heroMetrics.familiar.trend)/100)*314.16" transform="rotate(-90 60 60)" stroke-linecap="round" />
              </svg>
              <div class="position-absolute top-50 start-50 translate-middle">
                <div class="fs-4 fw-bold" :class="heroMetrics.familiar.trend >= 0 ? 'text-success' : 'text-danger'">{{ Math.abs(heroMetrics.familiar.trend) }}%</div>
              </div>
            </div>
            <div class="display-6 fw-bold mb-2 text-success">{{ heroMetrics.familiar.value }}</div>
            <div class="fs-6 fw-bold text-secondary text-uppercase mb-1">{{ heroMetrics.familiar.label }}</div>
            <div class="fs-6 text-muted">{{ heroMetrics.familiar.sublabel }}</div>
          </div>
        </div>
        <div class="col-12 col-sm-6 col-lg-3">
          <div class="bg-white rounded-4 shadow-sm border border-light p-3 text-center">
            <div class="circular-progress position-relative d-inline-block mb-3" style="width: 120px; height: 120px;">
              <svg width="120" height="120" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="50" stroke="#e6e6e6" stroke-width="8" fill="none" />
                <circle cx="60" cy="60" r="50" :stroke="heroMetrics.educacion.trend >= 0 ? '#10b981' : '#ef4444'" stroke-width="8" fill="none" stroke-dasharray="314.16" :stroke-dashoffset="314.16 - (Math.abs(heroMetrics.educacion.trend)/100)*314.16" transform="rotate(-90 60 60)" stroke-linecap="round" />
              </svg>
              <div class="position-absolute top-50 start-50 translate-middle">
                <div class="fs-4 fw-bold" :class="heroMetrics.educacion.trend >= 0 ? 'text-success' : 'text-danger'">{{ Math.abs(heroMetrics.educacion.trend) }}%</div>
              </div>
            </div>
            <div class="display-6 fw-bold mb-2 text-warning">{{ heroMetrics.educacion.value }}</div>
            <div class="fs-6 fw-bold text-secondary text-uppercase mb-1">{{ heroMetrics.educacion.label }}</div>
            <div class="fs-6 text-muted">{{ heroMetrics.educacion.sublabel }}</div>
          </div>
        </div>
        <div class="col-12 col-sm-6 col-lg-3">
          <div class="bg-white rounded-4 shadow-sm border border-light p-3 text-center">
            <div class="circular-progress position-relative d-inline-block mb-3" style="width: 120px; height: 120px;">
              <svg width="120" height="120" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="50" stroke="#e6e6e6" stroke-width="8" fill="none" />
                <circle cx="60" cy="60" r="50" :stroke="heroMetrics.empleo.trend >= 0 ? '#10b981' : '#ef4444'" stroke-width="8" fill="none" stroke-dasharray="314.16" :stroke-dashoffset="314.16 - (Math.abs(heroMetrics.empleo.trend)/100)*314.16" transform="rotate(-90 60 60)" stroke-linecap="round" />
              </svg>
              <div class="position-absolute top-50 start-50 translate-middle">
                <div class="fs-4 fw-bold" :class="heroMetrics.empleo.trend >= 0 ? 'text-success' : 'text-danger'">{{ Math.abs(heroMetrics.empleo.trend) }}%</div>
              </div>
            </div>
            <div class="display-6 fw-bold mb-2 text-danger">{{ heroMetrics.empleo.value }}</div>
            <div class="fs-6 fw-bold text-secondary text-uppercase mb-1">{{ heroMetrics.empleo.label }}</div>
            <div class="fs-6 text-muted">{{ heroMetrics.empleo.sublabel }}</div>
          </div>
        </div>
      </div>

      <!-- Grid Principal - 2 Filas -->

      <!-- Fila 1: Evolución + Composición + Indicadores -->

      <!-- Grid Principal - 2 Filas -->

      <!-- Fila 1: Evolución + Composición + Indicadores -->
      <div class="row g-3 mb-3">

        <!-- Área CHART - Evolución Temporal -->
        <div class="col-12 col-lg-4">
          <div class="bg-white rounded-4 shadow-sm border border-light p-3" style="height: 320px;">
            <div class="d-flex align-items-center justify-content-between mb-3">
              <h3 class="fs-5 fw-bold text-dark d-flex align-items-center mb-0">
                <div class="bg-primary rounded-pill me-3" style="width: 4px; height: 24px;"></div>
                Evolución de Registros
              </h3>
              <button class="btn btn-link text-primary p-0 fs-6 fw-semibold d-flex align-items-center">
                Ver detalle <i class="bi bi-chevron-right ms-1"></i>
              </button>
            </div>
            <ChartPanel chart-id="areaChart" type="line" :data="evolucionData">
              <template #title></template>
            </ChartPanel>
          </div>
        </div>

        <!-- TREEMAP - Composición Demográfica -->
        <div class="col-12 col-lg-4">
          <div class="bg-white rounded-4 shadow-sm border border-light p-3" style="height: 320px;">
            <div class="d-flex align-items-center justify-content-between mb-3">
              <h3 class="fs-5 fw-bold text-dark d-flex align-items-center mb-0">
                <div class="bg-primary rounded-pill me-3" style="width: 4px; height: 24px;"></div>
                Composición por Edad
              </h3>
              <button class="btn btn-link text-primary p-0 fs-6 fw-semibold d-flex align-items-center">
                Ver grupos <i class="bi bi-chevron-right ms-1"></i>
              </button>
            </div>
            <ChartPanel chart-id="treemapChart" type="bar" :data="composicionData">
              <template #title></template>
            </ChartPanel>
          </div>
        </div>

        <!-- RADAR CHART - Indicadores Sociodemográficos -->
        <div class="col-12 col-lg-4">
          <div class="bg-white rounded-4 shadow-sm border border-light p-3" style="height: 320px;">
            <div class="d-flex align-items-center justify-content-between mb-3">
              <h3 class="fs-5 fw-bold text-dark d-flex align-items-center mb-0">
                <div class="bg-primary rounded-pill me-3" style="width: 4px; height: 24px;"></div>
                Indicadores Clave
              </h3>
              <button class="btn btn-link text-primary p-0 fs-6 fw-semibold d-flex align-items-center">
                Ver todos <i class="bi bi-chevron-right ms-1"></i>
              </button>
            </div>
            <ChartPanel chart-id="radarChart" type="radar" :data="indicadoresData">
              <template #title></template>
            </ChartPanel>
          </div>
        </div>
      </div>

      <!-- Grid Secundario -->
      <div class="row g-3 mb-3">

        <!-- HORIZONTAL BAR - Nivel Educativo -->
        <div class="col-12 col-lg-4">
          <div class="bg-white rounded-4 shadow-sm border border-light p-3" style="height: 320px;">
            <div class="d-flex align-items-center justify-content-between mb-3">
              <h3 class="fs-5 fw-bold text-dark d-flex align-items-center mb-0">
                <div class="bg-primary rounded-pill me-3" style="width: 4px; height: 24px;"></div>
                Nivel Educativo
              </h3>
              <button class="btn btn-link text-primary p-0 fs-6 fw-semibold d-flex align-items-center">
                Ver estadísticas <i class="bi bi-chevron-right ms-1"></i>
              </button>
            </div>
            <ChartPanel chart-id="educacionChart" type="bar" :data="educacionData">
              <template #title></template>
            </ChartPanel>
          </div>
        </div>

        <!-- DONUT CHART - Distribución de Género -->
        <div class="col-12 col-lg-4">
          <div class="bg-white rounded-4 shadow-sm border border-light p-3" style="height: 320px;">
            <div class="d-flex align-items-center justify-content-between mb-3">
              <h3 class="fs-5 fw-bold text-dark d-flex align-items-center mb-0">
                <div class="bg-primary rounded-pill me-3" style="width: 4px; height: 24px;"></div>
                Distribución de Género
              </h3>
            </div>
            <ChartPanel chart-id="generoChart" type="doughnut" :data="generoData">
              <template #title></template>
            </ChartPanel>
            <div class="row g-2 mt-3">
              <div v-for="(value, index) in generoData.datasets[0].data" :key="index" class="col-4 text-center">
                <div class="fs-4 fw-bold text-dark">{{ value }}</div>
                <div class="fs-6 text-muted fw-medium">{{ generoData.labels[index] }}</div>
                <div class="w-100 rounded-pill mt-1" style="height: 4px;" :style="{ backgroundColor: generoData.datasets[0].backgroundColor[index] }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- STACKED BAR - Grupos de Edad por Género -->
        <div class="col-12 col-lg-4">
          <div class="bg-white rounded-4 shadow-sm border border-light p-3" style="height: 320px;">
            <div class="d-flex align-items-center justify-content-between mb-3">
              <h3 class="fs-5 fw-bold text-dark d-flex align-items-center mb-0">
                <div class="bg-primary rounded-pill me-3" style="width: 4px; height: 24px;"></div>
                Pirámide Poblacional Simplificada
              </h3>
              <button class="btn btn-link text-primary p-0 fs-6 fw-semibold d-flex align-items-center">
                Ver detalle <i class="bi bi-chevron-right ms-1"></i>
              </button>
            </div>
            <ChartPanel chart-id="gruposEdadChart" type="bar" :data="gruposEdadData" :options="gruposEdadOptions">
              <template #title></template>
            </ChartPanel>
          </div>
        </div>
      </div>

      <!-- Fila Inferior - Estructura Familiar + Mapa -->
      <div class="row g-3">

        <!-- Estructura Familiar - Cards Grid -->
        <div class="col-12 col-lg-4">
          <div class="bg-white rounded-4 shadow-sm border border-light p-3" style="height: 320px;">
            <div class="d-flex align-items-center justify-content-between mb-3">
              <h3 class="fs-5 fw-bold text-dark d-flex align-items-center mb-0">
                <div class="bg-primary rounded-pill me-3" style="width: 4px; height: 24px;"></div>
                Estructura Familiar
              </h3>
              <button class="btn btn-link text-primary p-0 fs-6 fw-semibold d-flex align-items-center">
                Ver composición <i class="bi bi-chevron-right ms-1"></i>
              </button>
            </div>
            <div class="row g-3">
              <div v-for="item in estructuraFamiliar" :key="item.tipo" class="col-6 col-md-3">
                <div class="rounded-4 p-3 text-white position-relative overflow-hidden" :style="{ backgroundColor: item.color }">
                  <div class="position-absolute top-0 end-0 opacity-25" style="width: 80px; height: 80px; transform: translate(24px, -24px);">
                    <i class="bi bi-people" style="font-size: 5rem;"></i>
                  </div>
                  <div class="position-relative">
                    <div class="fs-2 fw-bold mb-1">{{ item.cantidad }}</div>
                    <div class="fs-6 fw-semibold opacity-75">{{ item.tipo }}</div>
                    <div class="fs-4 fw-bold mt-2">{{ item.porcentaje }}%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Métricas Compactas -->
        <div class="col-12 col-lg-4">
          <div class="bg-white rounded-4 shadow-sm border border-light p-3" style="height: 320px;">
            <div class="d-flex align-items-center justify-content-between mb-3">
              <h3 class="fs-5 fw-bold text-dark d-flex align-items-center mb-0">
                <div class="bg-primary rounded-pill me-3" style="width: 4px; height: 24px;"></div>
                Indicadores Demográficos
              </h3>
            </div>
            <div class="row g-3">
              <div class="col-6">
                <div class="d-flex align-items-center gap-3 p-3 bg-white rounded-3 border border-light shadow-sm">
                  <div class="p-2 rounded-3" style="background-color: rgba(59, 130, 246, 0.15);">
                    <i class="bi bi-people fs-4 text-primary"></i>
                  </div>
                  <div class="flex-fill">
                    <div class="fs-5 fw-bold text-dark">{{ indicadoresCompactos.menores.value }}</div>
                    <div class="fs-6 text-muted">{{ indicadoresCompactos.menores.label }}</div>
                  </div>
                </div>
              </div>
              <div class="col-6">
                <div class="d-flex align-items-center gap-3 p-3 bg-white rounded-3 border border-light shadow-sm">
                  <div class="p-2 rounded-3" style="background-color: rgba(139, 92, 246, 0.15);">
                    <i class="bi bi-people fs-4 text-info"></i>
                  </div>
                  <div class="flex-fill">
                    <div class="fs-5 fw-bold text-dark">{{ indicadoresCompactos.adultosMayores.value }}</div>
                    <div class="fs-6 text-muted">{{ indicadoresCompactos.adultosMayores.label }}</div>
                  </div>
                </div>
              </div>
              <div class="col-6">
                <div class="d-flex align-items-center gap-3 p-3 bg-white rounded-3 border border-light shadow-sm">
                  <div class="p-2 rounded-3" style="background-color: rgba(16, 185, 129, 0.15);">
                    <i class="bi bi-graph-up fs-4 text-success"></i>
                  </div>
                  <div class="flex-fill">
                    <div class="fs-5 fw-bold text-dark">{{ indicadoresCompactos.alfabetizacion.value }}</div>
                    <div class="fs-6 text-muted">{{ indicadoresCompactos.alfabetizacion.label }}</div>
                  </div>
                </div>
              </div>
              <div class="col-6">
                <div class="d-flex align-items-center gap-3 p-3 bg-white rounded-3 border border-light shadow-sm">
                  <div class="p-2 rounded-3" style="background-color: rgba(245, 158, 11, 0.15);">
                    <i class="bi bi-house fs-4 text-warning"></i>
                  </div>
                  <div class="flex-fill">
                    <div class="fs-5 fw-bold text-dark">{{ indicadoresCompactos.familiar.value }}</div>
                    <div class="fs-6 text-muted">{{ indicadoresCompactos.familiar.label }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Mapa 3D con Población -->
        <div class="col-12 col-lg-4">
          <div class="bg-white rounded-4 shadow-sm border border-light p-3" style="height: 320px;">
            <div class="d-flex align-items-center justify-content-between mb-3">
              <h3 class="fs-5 fw-bold text-dark d-flex align-items-center mb-0">
                <div class="bg-primary rounded-pill me-3" style="width: 4px; height: 24px;"></div>
                Mapa Poblacional 3D
              </h3>
              <button class="btn btn-link text-primary p-0 fs-6 fw-semibold d-flex align-items-center">
                Ver en detalle <i class="bi bi-chevron-right ms-1"></i>
              </button>
            </div>
            <div class="position-relative">
              <canvas
                ref="mapaCanvas"
                width="320"
                height="160"
                class="w-100 rounded-4"
                style="background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);"
              />
              <div class="position-absolute bottom-0 start-0 end-0 text-center">
                <div class="d-inline-block bg-white bg-opacity-90 backdrop-blur px-3 py-1 rounded-pill border border-primary border-opacity-25 shadow-sm">
                  <span class="fs-6 fw-semibold text-secondary">
                    <span class="d-inline-block bg-primary rounded-circle me-1" style="width: 8px; height: 8px; animation: pulse 2s infinite;"></span>
                    {{ totalPersonas.toLocaleString() }} personas registradas
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import ChartPanel from '../../components/graficas/ChartPanel.vue'

// Estados reactivos
const periodo = ref('mes')
const currentYear = ref(2025)
const nombreComunidad = ref('Comunidad Indígena El Refugio')
const totalPersonas = ref(1847)
const mapaCanvas = ref(null)

// Usuario (simulado)
const usuario = ref({
  rol: 'admin',
  nombre: 'Admin Juan',
  permisos: []
})

// Hero Metrics
const heroMetrics = ref({
  poblacion: {
    value: '1,847',
    label: 'Población Total',
    sublabel: '512 familias registradas',
    trend: 2.8,
    color: '#3b82f6'
  },
  familiar: {
    value: '3.6',
    label: 'Promedio Familiar',
    sublabel: 'Personas por hogar',
    trend: 0.5,
    color: '#10b981'
  },
  educacion: {
    value: '78%',
    label: 'Cobertura Educativa',
    sublabel: 'Nivel escolarizado',
    trend: 3.2,
    color: '#f59e0b'
  },
  empleo: {
    value: '62%',
    label: 'Tasa de Empleo',
    sublabel: 'Población activa',
    trend: -1.2,
    color: '#ef4444'
  }
})

// Indicadores Compactos
const indicadoresCompactos = ref({
  menores: { value: '423', label: 'Menores de Edad' },
  adultosMayores: { value: '135', label: 'Adultos Mayores' },
  alfabetizacion: { value: '92.2%', label: 'Alfabetización' },
  familiar: { value: '3.6', label: 'Promedio Familiar' }
})

// Estructura Familiar
const estructuraFamiliar = ref([
  { tipo: 'Nuclear', cantidad: 256, porcentaje: 50, color: '#3b82f6' },
  { tipo: 'Extendida', cantidad: 154, porcentaje: 30, color: '#10b981' },
  { tipo: 'Monoparental', cantidad: 77, porcentaje: 15, color: '#f59e0b' },
  { tipo: 'Unipersonal', cantidad: 25, porcentaje: 5, color: '#ef4444' }
])

// ======= SISTEMA DE PERMISOS =======
const permisosPorRol = {
  admin: ['poblacional', 'social', 'salud', 'encuestas', 'reportes', 'auditoria', 'usuarios'],
  coordinador_salud: ['poblacional_basico', 'salud', 'reportes_limitado'],
  coordinador_social: ['poblacional_basico', 'social', 'reportes_limitado'],
  encuestador: ['encuestas', 'reportes_limitado'],
  invitado: ['poblacional_publico']
}

// Computed para verificar si es admin
const esAdmin = computed(() => usuario.value.rol === 'admin')

// Función para verificar permisos
const puedeVerModulo = (modulo) => {
  const permisos = permisosPorRol[usuario.value.rol] || []
  
  // Admin ve todo
  if (usuario.value.rol === 'admin') return true
  
  // Verificar permisos específicos
  return permisos.includes(modulo) || permisos.includes(`${modulo}_basico`) || permisos.includes(`${modulo}_publico`)
}

// Función para verificar si mostrar sección completa
const mostrarSeccion = (seccion) => {
  const mapeoSecciones = {
    'resumen_modulos': ['admin', 'coordinador_salud', 'coordinador_social'],
    'graficos_poblacionales': ['admin', 'coordinador_salud', 'coordinador_social'],
    'graficos_adicionales': ['admin', 'coordinador_salud', 'coordinador_social'],
    'indicadores_sectoriales': ['admin', 'coordinador_salud', 'coordinador_social'],
    'actividad_auditoria': ['admin'],
    'encuestas_reportes': ['admin', 'coordinador_salud', 'coordinador_social', 'encuestador']
  }
  
  return mapeoSecciones[seccion]?.includes(usuario.value.rol) || false
}

// Módulos disponibles en el selector según rol
const modulosDisponibles = computed(() => {
  const todosModulos = [
    { value: 'todo', label: 'Vista Completa', roles: ['admin'] },
    { value: 'poblacional', label: 'Solo Poblacional', roles: ['admin', 'coordinador_salud', 'coordinador_social'] },
    { value: 'social', label: 'Solo Social', roles: ['admin', 'coordinador_social'] },
    { value: 'salud', label: 'Solo Salud', roles: ['admin', 'coordinador_salud'] },
    { value: 'encuestas', label: 'Solo Encuestas', roles: ['admin', 'encuestador'] },
    { value: 'auditoria', label: 'Solo Auditoría', roles: ['admin'] }
  ]
  
  return todosModulos.filter(modulo => modulo.roles.includes(usuario.value.rol))
})

// ======= KPIs FILTRADOS POR ROL =======
const todosLosKpis = [
  { 
    title: 'Población', 
    value: 1847, 
    change: 2.8, 
    icon: 'bi bi-people-fill', 
    color: '#0d6efd',
    subtitle: '512 familias',
    roles: ['admin', 'coordinador_salud', 'coordinador_social', 'invitado']
  },
  { 
    title: 'Salud', 
    value: '85%', 
    change: 1.5, 
    icon: 'bi bi-heart-pulse', 
    color: '#dc3545',
    subtitle: '3 campañas activas',
    roles: ['admin', 'coordinador_salud']
  },
  { 
    title: 'Educación', 
    value: '78%', 
    change: 3, 
    icon: 'bi bi-book', 
    color: '#ffc107',
    subtitle: 'Cobertura escolar',
    roles: ['admin', 'coordinador_social']
  },
  { 
    title: 'Empleo', 
    value: '62%', 
    change: -1, 
    icon: 'bi bi-briefcase', 
    color: '#198754',
    subtitle: 'Tasa de ocupación',
    roles: ['admin', 'coordinador_social']
  },
  { 
    title: 'Programas', 
    value: 8, 
    change: 12.5, 
    icon: 'bi bi-diagram-3', 
    color: '#6f42c1',
    subtitle: '634 beneficiarios',
    roles: ['admin', 'coordinador_social']
  },
  { 
    title: 'Usuarios', 
    value: 235, 
    change: 5.2, 
    icon: 'bi bi-person-check', 
    color: '#0dcaf0',
    subtitle: '12 nuevos este mes',
    roles: ['admin']
  }
]

const kpisVisibles = computed(() => {
  return todosLosKpis.filter(kpi => kpi.roles.includes(usuario.value.rol))
})

// ======= RESUMEN DE MÓDULOS FILTRADO =======
const todosModulosResumen = [
  {
    nombre: 'Poblacional',
    valor: '1,847',
    descripcion: 'Personas registradas',
    icon: 'bi bi-people',
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    badge: '512 familias',
    badgeClass: 'bg-primary',
    detalles: [
      { label: 'Masculino', value: '892' },
      { label: 'Femenino', value: '941' },
      { label: 'Menores', value: '423' },
      { label: 'Mayores', value: '135' }
    ],
    roles: ['admin', 'coordinador_salud', 'coordinador_social']
  },
  {
    nombre: 'Social',
    valor: '8',
    descripcion: 'Programas activos',
    icon: 'bi bi-hearts',
    color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    badge: '634 beneficiarios',
    badgeClass: 'bg-danger',
    detalles: [
      { label: 'Beneficiarios', value: '634' },
      { label: 'Actividades', value: '5' },
      { label: 'Cobertura', value: '12 zonas' },
      { label: 'Tasa', value: '34.3%' }
    ],
    roles: ['admin', 'coordinador_social']
  },
  {
    nombre: 'Salud',
    valor: '456',
    descripcion: 'Vacunaciones realizadas',
    icon: 'bi bi-heart-pulse-fill',
    color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    badge: '89 casos',
    badgeClass: 'bg-info',
    detalles: [
      { label: 'Campañas', value: '3' },
      { label: 'Controles', value: '23' },
      { label: 'Alertas', value: '2' },
      { label: 'Recursos', value: '12' }
    ],
    roles: ['admin', 'coordinador_salud']
  },
  {
    nombre: 'Encuestas',
    valor: '4',
    descripcion: 'Encuestas activas',
    icon: 'bi bi-clipboard-data',
    color: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    badge: '48.3% participación',
    badgeClass: 'bg-warning',
    detalles: [
      { label: 'Activas', value: '4' },
      { label: 'Cerradas', value: '15' },
      { label: 'Respuestas', value: '892' },
      { label: 'Usuarios', value: '348' }
    ],
    roles: ['admin', 'encuestador']
  }
]

const modulosResumenVisibles = computed(() => {
  return todosModulosResumen.filter(modulo => modulo.roles.includes(usuario.value.rol))
})

// ======= ALERTAS FILTRADAS =======
const todasLasAlertas = [
  { 
    id: 1, 
    tipo: 'danger',
    icon: 'exclamation-triangle-fill',
    titulo: 'Alerta Crítica',
    mensaje: 'Brote de dengue detectado en zona norte.',
    roles: ['admin', 'coordinador_salud']
  },
  { 
    id: 2, 
    tipo: 'warning',
    icon: 'exclamation-circle',
    titulo: 'Advertencia',
    mensaje: 'Interrupción temporal de agua potable mañana.',
    roles: ['admin', 'coordinador_salud', 'coordinador_social', 'invitado']
  },
  { 
    id: 3, 
    tipo: 'info',
    icon: 'info-circle',
    titulo: 'Información',
    mensaje: 'Nueva encuesta disponible para la comunidad.',
    roles: ['admin', 'coordinador_social', 'encuestador', 'invitado']
  }
]

const alertasVisibles = computed(() => {
  return todasLasAlertas.filter(alerta => alerta.roles.includes(usuario.value.rol))
})

// ======= DATOS DE GRÁFICAS =======

// Evolución Temporal (Area Chart)
const evolucionData = ref({
  labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago'],
  datasets: [
    {
      label: 'Registros',
      data: [142, 158, 133, 165, 152, 173, 168, 181],
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59, 130, 246, 0.3)',
      fill: true,
      tension: 0.4
    },
    {
      label: 'Meta',
      data: [150, 160, 155, 170, 165, 175, 170, 180],
      borderColor: '#10b981',
      backgroundColor: 'rgba(16, 185, 129, 0.2)',
      fill: true,
      tension: 0.4,
      borderDash: [5, 5]
    }
  ]
})

// Composición Demográfica (Treemap - usando bar chart por ahora)
const composicionData = ref({
  labels: ['Adultos 31-50 años', 'Jóvenes 18-30 años', 'Adolescentes 13-17 años', 'Niños 6-12 años', 'Primera infancia 0-5 años', 'Adultos mayores 51-65 años', 'Tercera edad 65+ años'],
  datasets: [
    {
      label: 'Población',
      data: [512, 324, 243, 160, 181, 279, 134],
      backgroundColor: ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#6366f1', '#ef4444']
    }
  ]
})

// Indicadores Sociodemográficos (Radar Chart)
const indicadoresData = ref({
  labels: ['Alfabetización', 'Empleo', 'Educación', 'Salud', 'Vivienda', 'Servicios'],
  datasets: [
    {
      label: 'Cobertura',
      data: [92, 62, 78, 85, 71, 88],
      borderColor: '#8b5cf6',
      backgroundColor: 'rgba(139, 92, 246, 0.6)',
      pointBackgroundColor: '#8b5cf6'
    }
  ]
})

// Nivel Educativo (Horizontal Bar)
const educacionData = ref({
  labels: ['Secundaria', 'Primaria', 'Técnico', 'Sin educación', 'Universidad', 'Posgrado'],
  datasets: [
    {
      label: 'Cantidad',
      data: [723, 486, 312, 145, 156, 25],
      backgroundColor: '#f59e0b'
    }
  ]
})

// Distribución de Género (Donut Chart)
const generoData = ref({
  labels: ['Femenino', 'Masculino', 'Otro'],
  datasets: [
    {
      data: [941, 892, 14],
      backgroundColor: ['#ec4899', '#3b82f6', '#8b5cf6'],
      borderWidth: 2,
      borderColor: '#fff'
    }
  ]
})

// Grupos de Edad por Género (Stacked Bar)
const gruposEdadData = ref({
  labels: ['0-12', '13-17', '18-30', '31-50', '51+'],
  datasets: [
    {
      label: 'Masculino',
      data: [214, 78, 156, 245, 199],
      backgroundColor: '#3b82f6'
    },
    {
      label: 'Femenino',
      data: [210, 82, 168, 267, 214],
      backgroundColor: '#ec4899'
    }
  ]
})

const gruposEdadOptions = ref({
  scales: {
    x: {
      stacked: true
    },
    y: {
      stacked: true
    }
  }
})

const pieChartData = {
  labels: ['Masculino', 'Femenino', 'Otro'],
  datasets: [
    {
      data: [892, 941, 14],
      backgroundColor: [
        'rgba(13, 110, 253, 0.9)', 
        'rgba(255, 193, 7, 0.9)',
        'rgba(108, 117, 125, 0.9)'
      ],
      borderWidth: 2,
      borderColor: '#fff'
    }
  ]
}

const programasSocialesData = {
  labels: ['Alimentación', 'Educación', 'Vivienda', 'Salud', 'Empleo'],
  datasets: [
    {
      data: [156, 189, 98, 123, 68],
      backgroundColor: [
        'rgba(220, 53, 69, 0.8)',
        'rgba(255, 193, 7, 0.8)',
        'rgba(13, 202, 240, 0.8)',
        'rgba(25, 135, 84, 0.8)',
        'rgba(111, 66, 193, 0.8)'
      ],
      borderWidth: 2,
      borderColor: '#fff'
    }
  ]
}

const saludChartData = {
  labels: ['Vacunaciones', 'Controles', 'Casos', 'Alertas'],
  datasets: [
    {
      label: 'Cantidad',
      data: [456, 23, 89, 2],
      backgroundColor: [
        'rgba(25, 135, 84, 0.8)',
        'rgba(13, 110, 253, 0.8)',
        'rgba(255, 193, 7, 0.8)',
        'rgba(220, 53, 69, 0.8)'
      ],
      borderRadius: 6
    }
  ]
}

const auditoria = {
  completados: 146,
  advertencias: 8,
  criticos: 2
}

const auditoriaChartData = {
  labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
  datasets: [
    {
      label: 'Eventos Completados',
      data: [120, 135, 128, 142, 156, 98, 146],
      borderColor: 'rgba(25, 135, 84, 1)',
      backgroundColor: 'rgba(25, 135, 84, 0.1)',
      tension: 0.4,
      fill: true
    },
    {
      label: 'Advertencias',
      data: [5, 7, 6, 8, 9, 4, 8],
      borderColor: 'rgba(255, 193, 7, 1)',
      backgroundColor: 'rgba(255, 193, 7, 0.1)',
      tension: 0.4,
      fill: true
    },
    {
      label: 'Críticos',
      data: [1, 0, 2, 1, 3, 0, 2],
      borderColor: 'rgba(220, 53, 69, 1)',
      backgroundColor: 'rgba(220, 53, 69, 0.1)',
      tension: 0.4,
      fill: true
    }
  ]
}

const encuestas = {
  activas: 4,
  cerradas:15,
   respuestas: 892,
  tasaParticipacion: 48.3
}

const reportes = {
  generados: 67,
  pendientes: 3,
  descargasTotal: 234
}

const reportesChartData = {
  labels: ['PDF', 'Excel', 'CSV'],
  datasets: [
    {
      data: [34, 21, 12],
      backgroundColor: [
        'rgba(220, 53, 69, 0.8)',
        'rgba(25, 135, 84, 0.8)',
        'rgba(13, 110, 253, 0.8)'
      ],
      borderWidth: 2,
      borderColor: '#fff'
    }
  ]
}

const actividadReciente = [
  { 
    id: 1, 
    accion: 'Nueva persona registrada', 
    usuario: 'Admin Juan', 
    modulo: 'Poblacional',
    moduloColor: 'primary',
    tiempo: 'Hace 5 minutos',
    color: '#0d6efd'
  },
  { 
    id: 2, 
    accion: 'Reporte PDF generado', 
    usuario: 'Editor María', 
    modulo: 'Reportes',
    moduloColor: 'success',
    tiempo: 'Hace 12 minutos',
    color: '#198754'
  },
  { 
    id: 3, 
    accion: 'Encuesta cerrada', 
    usuario: 'Admin Juan', 
    modulo: 'Encuestas',
    moduloColor: 'warning',
    tiempo: 'Hace 23 minutos',
    color: '#ffc107'
  },
  { 
    id: 4, 
    accion: 'Beneficiario inscrito', 
    usuario: 'Editor Carlos', 
    modulo: 'Social',
    moduloColor: 'danger',
    tiempo: 'Hace 1 hora',
    color: '#dc3545'
  },
  { 
    id: 5, 
    accion: 'Vacunación registrada', 
    usuario: 'Editor María', 
    modulo: 'Salud',
    moduloColor: 'info',
    tiempo: 'Hace 2 horas',
    color: '#0dcaf0'
  }
]

const noticias = [
  { 
    id: 1, 
    titulo: 'Nueva jornada de vacunación', 
    fecha: '2025-08-12', 
    descripcion: 'Se realizará en el centro de salud comunitario.',
    categoria: 'Salud'
  },
  { 
    id: 2, 
    titulo: 'Taller de capacitación agrícola', 
    fecha: '2025-08-20', 
    descripcion: 'Dirigido a productores locales.',
    categoria: 'Social'
  },
  { 
    id: 3, 
    titulo: 'Nuevo programa de vivienda', 
    fecha: '2025-08-25', 
    descripcion: 'Inicio de inscripciones para beneficiarios.',
    categoria: 'Social'
  }
]

// ======= 3D MAP LOGIC =======
const puntos3D = ref([])
const rotacion3D = ref(0)

const generarPuntos3D = () => {
  const nuevosPuntos = []
  const radio = 80
  const capas = 8
  const puntosPorCapa = Math.ceil(totalPersonas.value / capas)

  for (let capa = 0; capa < capas; capa++) {
    const y = (capa / (capas - 1)) * 2 - 1
    const radioEnCapa = Math.sqrt(1 - y * y) * radio
    const puntosEnEstaCapa = Math.floor(puntosPorCapa * (1 - Math.abs(y) * 0.3))

    for (let i = 0; i < puntosEnEstaCapa; i++) {
      const angulo = (i / puntosEnEstaCapa) * Math.PI * 2
      nuevosPuntos.push({
        x: Math.cos(angulo) * radioEnCapa,
        y: y * radio * 0.8,
        z: Math.sin(angulo) * radioEnCapa,
        color: `hsl(${200 + capa * 20}, 70%, ${50 + capa * 5}%)`,
        size: 2 + Math.random() * 2
      })
    }
  }
  puntos3D.value = nuevosPuntos.slice(0, Math.min(totalPersonas.value, 500))
}

const dibujarMapa3D = () => {
  const canvas = mapaCanvas.value
  if (!canvas) return

  const ctx = canvas.getContext('2d')
  const width = canvas.width
  const height = canvas.height

  ctx.clearRect(0, 0, width, height)

  const gradiente = ctx.createRadialGradient(width/2, height/2, 0, width/2, height/2, width/2)
  gradiente.addColorStop(0, 'rgba(59, 130, 246, 0.1)')
  gradiente.addColorStop(1, 'rgba(139, 92, 246, 0.05)')
  ctx.fillStyle = gradiente
  ctx.fillRect(0, 0, width, height)

  const puntosOrdenados = [...puntos3D.value].sort((a, b) => {
    const rad = (rotacion3D.value * Math.PI) / 180
    const zA = a.z * Math.cos(rad) - a.x * Math.sin(rad)
    const zB = b.z * Math.cos(rad) - b.x * Math.sin(rad)
    return zA - zB
  })

  puntosOrdenados.forEach(punto => {
    const rad = (rotacion3D.value * Math.PI) / 180

    const x3d = punto.x * Math.cos(rad) + punto.z * Math.sin(rad)
    const z3d = punto.z * Math.cos(rad) - punto.x * Math.sin(rad)

    const escala = 300 / (300 + z3d)
    const x2d = width / 2 + x3d * escala
    const y2d = height / 2 + punto.y * escala

    const opacidad = 0.3 + (z3d + 100) / 200 * 0.7

    ctx.shadowBlur = 8
    ctx.shadowColor = punto.color
    ctx.fillStyle = punto.color
    ctx.globalAlpha = opacidad

    ctx.beginPath()
    ctx.arc(x2d, y2d, punto.size * escala, 0, Math.PI * 2)
    ctx.fill()

    ctx.shadowBlur = 0
    ctx.globalAlpha = 1
  })

  ctx.strokeStyle = 'rgba(59, 130, 246, 0.3)'
  ctx.lineWidth = 2
  ctx.setLineDash([5, 5])
  ctx.beginPath()
  ctx.arc(width/2, height/2, 80, 0, Math.PI * 2)
  ctx.stroke()
  ctx.setLineDash([])
}

// ======= CARGAR DATOS AL MONTAR =======
onMounted(() => {
  generarPuntos3D()

  const intervalo = setInterval(() => {
    rotacion3D.value = (rotacion3D.value + 0.5) % 360
    dibujarMapa3D()
  }, 50)

  // Cleanup on unmount
  return () => clearInterval(intervalo)
})
</script>

<style scoped>
.container-fluid {
  max-width: 1600px;
}

.activity-timeline {
  max-height: 400px;
  overflow-y: auto;
}

.activity-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 15px;
  margin-top: 5px;
  flex-shrink: 0;
}

.activity-item:last-child {
  border-bottom: none !important;
}

.card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

.badge {
  font-weight: 600;
}

.progress {
  border-radius: 10px;
  overflow: hidden;
}

.progress-bar {
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Animación de pulso para el indicador del mapa 3D */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Estilos adicionales para el mapa 3D */
canvas {
  display: block;
  max-width: 100%;
  height: auto;
}
</style>