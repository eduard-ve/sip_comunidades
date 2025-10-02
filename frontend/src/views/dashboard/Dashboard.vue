<template>
  <div class="container-fluid py-4">
    <!-- ======= Encabezado Mejorado ======= -->
    <div class="d-flex flex-wrap justify-content-between align-items-center mb-4">
      <div>
        <h2 class="fw-bold mb-1">📊 Dashboard - Sistema de Gestión Comunitaria</h2>
        <div class="text-muted small">
          Comunidad: <span class="fw-semibold">{{ nombreComunidad }}</span> |
          Año: <span class="fw-semibold">{{ currentYear }}</span> |
          Última actualización: <span class="fw-semibold">{{ lastUpdate }}</span>
        </div>
      </div>
      <div class="d-flex gap-2">
        <!-- Selector de vista por módulo (según permisos) -->
        <select v-if="modulosDisponibles.length > 1" v-model="vistaActual" class="form-select w-auto">
          <option v-for="modulo in modulosDisponibles" :key="modulo.value" :value="modulo.value">
            {{ modulo.label }}
          </option>
        </select>
        
        <select v-model="currentYear" class="form-select w-auto">
          <option v-for="y in years" :key="y">{{ y }}</option>
        </select>
        
        <select v-model="periodo" class="form-select w-auto">
          <option value="dia">Día</option>
          <option value="semana">Semana</option>
          <option value="mes">Mes</option>
          <option value="año">Año</option>
        </select>
      </div>
    </div>

    <!-- ======= KPIs Principales (Filtrados por permisos) ======= -->
    <div class="row g-3 mb-4">
      <div class="col-12 col-sm-6 col-lg-2" v-for="card in kpisVisibles" :key="card.title">
        <KpiCard
          :title="card.title"
          :value="card.value"
          :change="card.change"
          :icon="card.icon"
          :color-icon="card.color"
          :subtitle="card.subtitle"
        />
      </div>
    </div>

    <!-- ======= Resumen por Módulos (Filtrado por permisos) ======= -->
    <div class="row g-3 mb-4" v-if="mostrarSeccion('resumen_modulos')">
      <div class="col-md-3" v-for="modulo in modulosResumenVisibles" :key="modulo.nombre">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <div :style="`background: ${modulo.color}; padding: 12px; border-radius: 8px;`">
                <i :class="modulo.icon" class="text-white" style="font-size: 1.5rem;"></i>
              </div>
              <span v-if="modulo.badge" class="badge" :class="modulo.badgeClass">{{ modulo.badge }}</span>
            </div>
            <h5 class="fw-bold mb-2">{{ modulo.nombre }}</h5>
            <h3 class="fw-bold text-primary mb-1">{{ modulo.valor }}</h3>
            <p class="text-muted small mb-3">{{ modulo.descripcion }}</p>
            <div class="border-top pt-2">
              <div v-for="det in modulo.detalles" :key="det.label" class="d-flex justify-content-between mb-1">
                <small class="text-muted">{{ det.label }}:</small>
                <small class="fw-semibold">{{ det.value }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ======= Gráficos Principales ======= -->
    <div class="row g-3 mb-4" v-if="mostrarSeccion('graficos_poblacionales')">
      <div class="col-md-6" v-if="puedeVerModulo('poblacional')">
        <ChartPanel chart-id="barLineChart" type="bar" :data="barLineChartData">
          <template #title>📈 Evolución de Registros Poblacionales</template>
        </ChartPanel>
      </div>
      <div class="col-md-6" v-if="puedeVerModulo('poblacional')">
        <ChartPanel chart-id="pieChart" type="pie" :data="pieChartData">
          <template #title>👥 Distribución por Género</template>
        </ChartPanel>
      </div>
    </div>

    <!-- ======= Gráficos Adicionales ======= -->
    <div class="row g-3 mb-4" v-if="mostrarSeccion('graficos_adicionales')">
      <div class="col-md-6" v-if="puedeVerModulo('social')">
        <ChartPanel chart-id="programasSociales" type="doughnut" :data="programasSocialesData">
          <template #title>🤝 Programas Sociales - Beneficiarios</template>
        </ChartPanel>
      </div>
      <div class="col-md-6" v-if="puedeVerModulo('salud')">
        <ChartPanel chart-id="saludChart" type="bar" :data="saludChartData">
          <template #title>🏥 Indicadores de Salud</template>
        </ChartPanel>
      </div>
    </div>

    <!-- ======= Mapas y Pirámide ======= -->
    <div class="row g-3 mb-4" v-if="puedeVerModulo('poblacional')">
      <div class="col-md-6">
        <PopulationPyramid />
      </div>
      <div class="col-md-6">
        <ServicesMap />
      </div>
    </div>

    <!-- ======= Indicadores Sectoriales ======= -->
    <div class="row g-3 mb-4" v-if="mostrarSeccion('indicadores_sectoriales')">
      <div class="col-md-6" v-if="puedeVerModulo('salud')">
        <HealthIndicators />
      </div>
      <div class="col-md-6" v-if="puedeVerModulo('poblacional')">
        <EducationStats />
      </div>
    </div>

    <!-- ======= Actividad Reciente y Auditoría ======= -->
    <div class="row g-3 mb-4" v-if="mostrarSeccion('actividad_auditoria')">
      <div class="col-md-6" v-if="puedeVerModulo('auditoria')">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h6 class="fw-bold mb-0">📅 Actividad Reciente del Sistema</h6>
              <span class="badge bg-primary">{{ actividadReciente.length }} eventos</span>
            </div>
            <div class="activity-timeline">
              <div v-for="act in actividadReciente" :key="act.id" class="activity-item mb-3 pb-3 border-bottom">
                <div class="d-flex">
                  <div class="activity-dot" :style="`background: ${act.color};`"></div>
                  <div class="flex-grow-1">
                    <div class="d-flex justify-content-between align-items-start">
                      <div>
                        <strong class="d-block">{{ act.accion }}</strong>
                        <!-- Solo admin ve el usuario -->
                        <small class="text-muted" v-if="esAdmin">{{ act.usuario }}</small>
                        <small class="text-muted" v-else>Usuario del sistema</small>
                      </div>
                      <span class="badge" :class="`bg-${act.moduloColor}`">{{ act.modulo }}</span>
                    </div>
                    <small class="text-muted">{{ act.tiempo }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6" v-if="puedeVerModulo('auditoria')">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h6 class="fw-bold mb-3">🛡️ Resumen de Auditoría</h6>
            <div class="row g-3 mb-3">
              <div class="col-4">
                <div class="border-start border-success border-4 ps-3">
                  <h3 class="fw-bold text-success mb-0">{{ auditoria.completados }}</h3>
                  <small class="text-muted">Completados</small>
                </div>
              </div>
              <div class="col-4">
                <div class="border-start border-warning border-4 ps-3">
                  <h3 class="fw-bold text-warning mb-0">{{ auditoria.advertencias }}</h3>
                  <small class="text-muted">Advertencias</small>
                </div>
              </div>
              <div class="col-4">
                <div class="border-start border-danger border-4 ps-3">
                  <h3 class="fw-bold text-danger mb-0">{{ auditoria.criticos }}</h3>
                  <small class="text-muted">Críticos</small>
                </div>
              </div>
            </div>
            <ChartPanel chart-id="auditoriaChart" type="line" :data="auditoriaChartData">
              <template #title>Eventos de Auditoría (7 días)</template>
            </ChartPanel>
          </div>
        </div>
      </div>
    </div>

    <!-- ======= Encuestas y Reportes ======= -->
    <div class="row g-3 mb-4" v-if="mostrarSeccion('encuestas_reportes')">
      <div class="col-md-6" v-if="puedeVerModulo('encuestas')">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h6 class="fw-bold mb-3">📋 Estado de Encuestas</h6>
            <div class="mb-3">
              <div class="d-flex justify-content-between mb-2">
                <span>Encuestas Activas</span>
                <strong class="text-success">{{ encuestas.activas }}</strong>
              </div>
              <div class="d-flex justify-content-between mb-2">
                <span>Encuestas Cerradas</span>
                <strong class="text-secondary">{{ encuestas.cerradas }}</strong>
              </div>
              <div class="d-flex justify-content-between mb-2">
                <span>Total Respuestas</span>
                <strong class="text-primary">{{ encuestas.respuestas }}</strong>
              </div>
              <div class="d-flex justify-content-between">
                <span>Tasa de Participación</span>
                <strong class="text-info">{{ encuestas.tasaParticipacion }}%</strong>
              </div>
            </div>
            <div class="progress" style="height: 25px;">
              <div class="progress-bar bg-success" role="progressbar" 
                   :style="`width: ${encuestas.tasaParticipacion}%`">
                {{ encuestas.tasaParticipacion }}%
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6" v-if="puedeVerModulo('reportes')">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h6 class="fw-bold mb-3">📊 Reportes Generados</h6>
            <ChartPanel chart-id="reportesChart" type="doughnut" :data="reportesChartData">
              <template #title>Distribución por Tipo</template>
            </ChartPanel>
            <div class="mt-3 text-center">
              <small class="text-muted">Total descargas: <strong>{{ reportes.descargasTotal }}</strong></small>
              <div class="mt-2">
                <router-link to="/reportes" class="btn btn-sm btn-outline-primary">
                  Ir a Módulo de Reportes
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ======= Alertas y Noticias ======= -->
    <div class="row g-3 mb-4">
      <div class="col-md-8">
        <div class="card shadow-sm p-3 h-100">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h6 class="fw-bold mb-0">📰 Noticias y Comunicados</h6>
            <button class="btn btn-sm btn-outline-primary">Ver todas</button>
          </div>
          <ul class="list-group list-group-flush">
            <li class="list-group-item" v-for="n in noticias" :key="n.id">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <strong class="d-block">{{ n.titulo }}</strong>
                  <p class="mb-1">{{ n.descripcion }}</p>
                  <small class="text-muted">
                    <i class="bi bi-calendar3"></i> {{ n.fecha }}
                  </small>
                </div>
                <span class="badge bg-info">{{ n.categoria }}</span>
              </div>
            </li>
          </ul>
        </div>
      </div>
      
      <div class="col-md-4">
        <div class="card shadow-sm p-3 h-100 bg-light">
          <h6 class="fw-bold mb-3">⚠️ Alertas Activas</h6>
          <ul class="list-unstyled">
            <li v-for="a in alertasVisibles" :key="a.id" class="mb-3">
              <div class="alert" :class="`alert-${a.tipo}`" role="alert">
                <i class="bi" :class="`bi-${a.icon}`"></i>
                <strong>{{ a.titulo }}</strong>
                <p class="mb-0 small">{{ a.mensaje }}</p>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import KpiCard from '../../components/tarjetas/KpiCard.vue'
import ChartPanel from '../../components/graficas/ChartPanel.vue'
import PopulationPyramid from '../../components/graficas/PopulationPyramid.vue'
import ServicesMap from '../../components/mapas/ServicesMap.vue'
import HealthIndicators from '../../components/tarjetas/HealthIndicators.vue'
import EducationStats from '../../components/graficas/EducationStats.vue'

// ======= CONFIGURACIÓN DE USUARIO Y PERMISOS =======
// TODO: Reemplazar con datos reales del backend/Django
const usuario = ref({
  rol: 'admin', // Opciones: 'admin', 'coordinador_salud', 'coordinador_social', 'encuestador', 'invitado'
  nombre: 'Admin Juan',
  permisos: [] // Se llenará según el rol
})

// Nombre de la comunidad (viene de configuración)
const nombreComunidad = ref('Comunidad Indígena  El Refugio')

// Estados reactivos
const vistaActual = ref('todo')
const currentYear = ref(2025)
const periodo = ref('mes')
const lastUpdate = ref('Hoy, 14:32')
const years = [2023, 2024, 2025]

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

// ======= DATOS DE GRÁFICAS (Sin cambios) =======
const barLineChartData = {
  labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago'],
  datasets: [
    {
      type: 'bar',
      label: 'Registros Poblacionales',
      data: [42, 58, 33, 65, 52, 73, 68, 81],
      backgroundColor: 'rgba(13, 110, 253, 0.8)',
      borderRadius: 6
    },
    {
      type: 'line',
      label: 'Tendencia',
      data: [40, 55, 35, 60, 55, 70, 70, 80],
      borderColor: '#ffc107',
      borderWidth: 3,
      tension: 0.4,
      fill: false,
      pointRadius: 5,
      pointBackgroundColor: '#ffc107'
    }
  ]
}

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

// ======= CARGAR DATOS DEL USUARIO AL MONTAR =======
onMounted(async () => {
  // TODO: Reemplazar con llamada real a tu API Django
  // const response = await fetch('/api/auth/user')
  // const userData = await response.json()
  // usuario.value = userData
  
  // Por ahora usa datos simulados
  console.log('Usuario cargado:', usuario.value)
  console.log('Permisos:', permisosPorRol[usuario.value.rol])
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
</style>