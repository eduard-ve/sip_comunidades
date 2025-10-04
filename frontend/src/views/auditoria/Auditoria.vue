<template> 
  <div class="container-fluid py-4 audit-container"> 
    <!-- Título y exportación --> 
    <div class="d-flex justify-content-between align-items-center mb-4"> 
      <h2 class="fw-bold audit-title">Auditoría</h2> 
    </div> 

    <!-- KPIs Section -->
    <div class="row mb-4">
      <!-- Total de Eventos -->
      <div class="col-xl-3 col-md-6 mb-3">
        <div class="card h-100 shadow-sm border-0 audit-kpi">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div class="audit-kpi-icon bg-primary bg-opacity-10 rounded-3 p-3">
                  <i class="fas fa-list-alt text-primary fs-4"></i>
                </div>
              </div>
              <div class="flex-grow-1 ms-3 audit-kpi-content">
                <h6 class="text-muted mb-1 fw-normal">Total Eventos</h6>
                <h3 class="mb-0 fw-bold">{{ totalEvents }}</h3>
                <small class="text-success">
                  <i class="fas fa-arrow-up"></i> +{{ todayEvents }} hoy
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Eventos por Usuario Activo -->
      <div class="col-xl-3 col-md-6 mb-3">
        <div class="card h-100 shadow-sm border-0 audit-kpi">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div class="audit-kpi-icon bg-success bg-opacity-10 rounded-3 p-3">
                  <i class="fas fa-users text-success fs-4"></i>
                </div>
              </div>
              <div class="flex-grow-1 ms-3 audit-kpi-content">
                <h6 class="text-muted mb-1 fw-normal">Usuarios Activos</h6>
                <h3 class="mb-0 fw-bold">{{ activeUsers }}</h3>
                <small class="text-info">
                  <i class="fas fa-clock"></i> Última hora
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Módulos Monitoreados -->
      <div class="col-xl-3 col-md-6 mb-3">
        <div class="card h-100 shadow-sm border-0 audit-kpi">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div class="audit-kpi-icon bg-warning bg-opacity-10 rounded-3 p-3">
                  <i class="fas fa-cubes text-warning fs-4"></i>
                </div>
              </div>
              <div class="flex-grow-1 ms-3 audit-kpi-content">
                <h6 class="text-muted mb-1 fw-normal">Módulos Activos</h6>
                <h3 class="mb-0 fw-bold">{{ activeModules }}</h3>
                <small class="text-muted">
                  <i class="fas fa-shield-alt"></i> Monitoreados
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Eventos Críticos -->
      <div class="col-xl-3 col-md-6 mb-3">
        <div class="card h-100 shadow-sm border-0 audit-kpi">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div class="audit-kpi-icon bg-danger bg-opacity-10 rounded-3 p-3">
                  <i class="fas fa-exclamation-triangle text-danger fs-4"></i>
                </div>
              </div>
              <div class="flex-grow-1 ms-3 audit-kpi-content">
                <h6 class="text-muted mb-1 fw-normal">Eventos Críticos</h6>
                <h3 class="mb-0 fw-bold">{{ criticalEvents }}</h3>
                <small class="text-danger">
                  <i class="fas fa-bell"></i> Requieren atención
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Gráficos de Análisis -->
    <div class="row mb-4">
      <!-- Actividad por Módulo -->
      <div class="col-lg-6 mb-3">
        <div class="card h-100 shadow-sm border-0 audit-card">
          <div class="card-header bg-white border-0 pb-0">
            <h6 class="fw-bold mb-0">Actividad por Módulo</h6>
            <small class="text-muted">Últimos 7 días</small>
          </div>
          <div class="card-body">
            <div class="module-activity">
              <div v-for="module in moduleActivity" :key="module.name" class="module-activity-item">
                <div class="module-activity-header">
                  <span class="module-activity-name">{{ module.name }}</span>
                  <span class="module-activity-count">{{ module.count }}</span>
                </div>
                <div class="progress audit-progress" style="height: 8px;">
                  <div 
                    class="progress-bar audit-progress-bar" 
                    :class="module.color"
                    :style="{ width: module.percentage + '%' }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Distribución por Acción -->
      <div class="col-lg-6 mb-3">
        <div class="card h-100 shadow-sm border-0 audit-card">
          <div class="card-header bg-white border-0 pb-0">
            <h6 class="fw-bold mb-0">Distribución por Acción</h6>
            <small class="text-muted">Este mes</small>
          </div>
          <div class="card-body">
            <div class="action-distribution">
              <div class="row text-center">
                <div v-for="action in actionDistribution" :key="action.type" class="col-4 mb-3">
                  <div class="action-distribution-item">
                    <div class="action-icon mb-2" :class="action.bgClass">
                      <i :class="action.icon"></i>
                    </div>
                    <h5 class="fw-bold mb-1">{{ action.count }}</h5>
                    <small class="text-muted">{{ action.type }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Actividad Reciente -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card shadow-sm border-0 audit-card">
          <div class="recent-activity-header">
            <div>
              <h6 class="recent-activity-title">Actividad Reciente</h6>
              <small class="recent-activity-subtitle">Últimos eventos registrados</small>
            </div>
            <div class="audit-filter-dropdown">
              <button 
                class="audit-filter-button" 
                type="button" 
                @click="toggleDropdown"
                :class="{ show: dropdownOpen }"
              >
                {{ currentFilterLabel }}
              </button>
              <ul class="audit-dropdown-menu" :class="{ show: dropdownOpen }">
                <li><a class="audit-dropdown-item" href="#" @click.prevent="filterEvents('all')">
                  <i class="fas fa-list me-2 text-secondary"></i>Todos los eventos
                </a></li>
                <li><hr class="audit-dropdown-divider"></li>
                <li><a class="audit-dropdown-item" href="#" @click.prevent="filterEvents('completed')">
                  <i class="fas fa-check-circle me-2 text-success"></i>Completado
                </a></li>
                <li><a class="audit-dropdown-item" href="#" @click.prevent="filterEvents('warning')">
                  <i class="fas fa-exclamation-triangle me-2 text-warning"></i>Advertencia
                </a></li>
                <li><a class="audit-dropdown-item" href="#" @click.prevent="filterEvents('critical')">
                  <i class="fas fa-times-circle me-2 text-danger"></i>Crítico
                </a></li>
                <li><hr class="audit-dropdown-divider"></li>
                <li><a class="audit-dropdown-item" href="#" @click.prevent="filterEvents('today')">
                  <i class="fas fa-calendar-day me-2 text-info"></i>Hoy
                </a></li>
              </ul>
            </div>
          </div>
          <div class="card-body p-0">
            <div class="recent-activity">
              <div v-for="event in filteredRecentActivity" :key="event.id" class="activity-item p-3 border-bottom">
                <div class="d-flex align-items-center">
                  <div class="activity-avatar me-3" :class="event.avatarClass">
                    <i :class="event.icon"></i>
                  </div>
                  <div class="flex-grow-1">
                    <div class="d-flex justify-content-between align-items-start">
                      <div>
                        <h6 class="mb-1 fw-medium">{{ event.title }}</h6>
                        <p class="mb-1 text-muted small">
                          <strong>{{ event.user }}</strong> en módulo 
                          <span class="audit-badge bg-light text-dark">{{ event.module }}</span>
                        </p>
                        <small class="text-muted">
                          <i class="fas fa-clock me-1"></i>{{ event.time }}
                        </small>
                      </div>
                      <span class="audit-badge" :class="event.statusClass">{{ event.status }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Componente de tabla --> 
    <AuditTable :events="events" @view-details="showDetails" /> 
 
    <!-- Modal detalle --> 
    <div v-if="selectedEvent" class="audit-modal"> 
      <div class="audit-modal-dialog"> 
        <div class="audit-modal-content"> 
          <div class="audit-modal-header"> 
            <h5 class="audit-modal-title">Detalle del evento</h5> 
            <button type="button" class="btn-close" @click="selectedEvent = null"></button> 
          </div> 
          <div class="audit-modal-body"> 
            <p><strong>Módulo:</strong> {{ selectedEvent.module }}</p> 
            <p><strong>Usuario:</strong> {{ selectedEvent.user }}</p> 
            <p><strong>Acción:</strong> {{ selectedEvent.action }}</p> 
            <p><strong>Fecha:</strong> {{ selectedEvent.date }}</p> 

            <h6 class="fw-bold mt-3">Cambios</h6> 
            <ul class="audit-changes-list"> 
              <li v-for="(value, field) in selectedEvent.changes" :key="field"> 
                <strong>{{ field }}:</strong> {{ value.old }} → {{ value.new }} 
              </li> 
            </ul> 
          </div> 
          <div class="audit-modal-footer"> 
            <button class="btn btn-secondary" @click="selectedEvent = null">Cerrar</button> 
          </div> 
        </div> 
      </div> 
    </div> 
    <div v-if="selectedEvent" class="audit-modal-backdrop"></div>
  </div> 
</template> 
 
<script setup> 
import { ref, computed } from "vue" 
import AuditTable from "../../components/comun/AuditTable.vue"
import '../../assets/css/Auditoria.css' 
 
const events = ref([ 
  { 
    id: 1, 
    module: "usuarios", 
    user: "admin", 
    action: "Creación de usuario", 
    date: "2025-08-15", 
    changes: { nombre: { old: "-", new: "Juan" }, rol: { old: "-", new: "Editor" } } 
  }, 
  { 
    id: 2, 
    module: "reportes", 
    user: "soporte", 
    action: "Eliminación de reporte", 
    date: "2025-08-14", 
    changes: { reporte: { old: "Reporte A", new: "-" } } 
  }, 
  { 
    id: 3, 
    module: "encuestas", 
    user: "usuario1", 
    action: "Modificación de encuesta", 
    date: "2025-08-13", 
    changes: { titulo: { old: "Encuesta 2024", new: "Encuesta 2025" } } 
  } 
]) 
 
const selectedEvent = ref(null) 

// Filtro states
const dropdownOpen = ref(false)
const currentFilter = ref('all')
const currentFilterLabel = ref('Filtrar')

// KPIs Data
const totalEvents = ref(1247)
const todayEvents = ref(23)
const activeUsers = ref(18)
const activeModules = ref(8)
const criticalEvents = ref(5)

// Module Activity Data
const moduleActivity = ref([
  { name: 'Usuarios', count: 342, percentage: 85, color: 'bg-primary' },
  { name: 'Reportes', count: 267, percentage: 67, color: 'bg-success' },
  { name: 'Encuestas', count: 189, percentage: 47, color: 'bg-warning' },
  { name: 'Configuración', count: 98, percentage: 25, color: 'bg-info' },
  { name: 'Sistema', count: 67, percentage: 17, color: 'bg-secondary' }
])

// Action Distribution Data
const actionDistribution = ref([
  { 
    type: 'Creación', 
    count: 456, 
    icon: 'fas fa-plus-circle', 
    bgClass: 'bg-success bg-opacity-10 text-success' 
  },
  { 
    type: 'Modificación', 
    count: 324, 
    icon: 'fas fa-edit', 
    bgClass: 'bg-warning bg-opacity-10 text-warning' 
  },
  { 
    type: 'Eliminación', 
    count: 89, 
    icon: 'fas fa-trash', 
    bgClass: 'bg-danger bg-opacity-10 text-danger' 
  }
])

// Recent Activity Data
const recentActivity = ref([
  {
    id: 1,
    title: 'Usuario creado exitosamente',
    user: 'admin',
    module: 'usuarios',
    time: 'hace 5 minutos',
    status: 'Completado',
    statusClass: 'bg-success',
    icon: 'fas fa-user-plus',
    avatarClass: 'bg-success bg-opacity-10 text-success'
  },
  {
    id: 2,
    title: 'Reporte eliminado',
    user: 'soporte',
    module: 'reportes',
    time: 'hace 1 hora',
    status: 'Advertencia',
    statusClass: 'bg-warning',
    icon: 'fas fa-file-times',
    avatarClass: 'bg-warning bg-opacity-10 text-warning'
  },
  {
    id: 3,
    title: 'Configuración actualizada',
    user: 'admin',
    module: 'sistema',
    time: 'hace 2 horas',
    status: 'Completado',
    statusClass: 'bg-success',
    icon: 'fas fa-cog',
    avatarClass: 'bg-primary bg-opacity-10 text-primary'
  },
  {
    id: 4,
    title: 'Acceso denegado detectado',
    user: 'usuario_desconocido',
    module: 'seguridad',
    time: 'hace 3 horas',
    status: 'Crítico',
    statusClass: 'bg-danger',
    icon: 'fas fa-exclamation-triangle',
    avatarClass: 'bg-danger bg-opacity-10 text-danger'
  }
])

// Computed property para filtrar actividad reciente
const filteredRecentActivity = computed(() => {
  const today = new Date()
  const todayStr = today.toISOString().split('T')[0]
  
  switch (currentFilter.value) {
    case 'completed':
      return recentActivity.value.filter(event => event.status === 'Completado')
    case 'warning':
      return recentActivity.value.filter(event => event.status === 'Advertencia')
    case 'critical':
      return recentActivity.value.filter(event => event.status === 'Crítico')
    case 'today':
      // Simular filtro por "hoy" basado en tiempo relativo
      return recentActivity.value.filter(event => 
        event.time.includes('minutos') || event.time.includes('hora')
      )
    default:
      return recentActivity.value
  }
})

// Methods
function exportExcel() { 
  alert("Exportando a Excel...") 
} 
 
function exportPdf() { 
  alert("Exportando a PDF...") 
} 
 
function showDetails(event) { 
  selectedEvent.value = event 
}

function filterEvents(filter) {
  currentFilter.value = filter
  dropdownOpen.value = false
  
  // Actualizar label del botón
  switch (filter) {
    case 'all':
      currentFilterLabel.value = 'Todos los eventos'
      break
    case 'completed':
      currentFilterLabel.value = 'Completado'
      break
    case 'warning':
      currentFilterLabel.value = 'Advertencia'
      break
    case 'critical':
      currentFilterLabel.value = 'Crítico'
      break
    case 'today':
      currentFilterLabel.value = 'Hoy'
      break
    default:
      currentFilterLabel.value = 'Filtrar'
  }
}

function toggleDropdown() {
  dropdownOpen.value = !dropdownOpen.value
}

// Cerrar dropdown al hacer click fuera
document.addEventListener('click', (e) => {
  if (!e.target.closest('.dropdown')) {
    dropdownOpen.value = false
  }
})
</script>