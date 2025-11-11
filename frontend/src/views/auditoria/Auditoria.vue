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
        <div class="card h-100 shadow-sm border-0 audit-kpi audit-kpi-total-events">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div class="audit-kpi-icon bg-white bg-opacity-20 rounded-3 p-3">
                  <span class="text-white fs-4">📊</span>
                </div>
              </div>
              <div class="flex-grow-1 ms-3 audit-kpi-content">
                <h6 class="mb-1 fw-normal">Total Eventos</h6>
                <h3 class="mb-0 fw-bold">{{ totalEvents }}</h3>
                <small>
                  <i class="fas fa-arrow-up"></i> +{{ todayEvents }} hoy
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Eventos por Usuario Activo -->
      <div class="col-xl-3 col-md-6 mb-3">
        <div class="card h-100 shadow-sm border-0 audit-kpi audit-kpi-active-users">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div class="audit-kpi-icon bg-white bg-opacity-20 rounded-3 p-3">
                  <span class="text-white fs-4">👤</span>
                </div>
              </div>
              <div class="flex-grow-1 ms-3 audit-kpi-content">
                <h6 class="mb-1 fw-normal">Usuarios Activos</h6>
                <h3 class="mb-0 fw-bold">{{ activeUsers }}</h3>
                <small>
                  <i class="fas fa-clock"></i> Última hora
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Módulos Monitoreados -->
      <div class="col-xl-3 col-md-6 mb-3">
        <div class="card h-100 shadow-sm border-0 audit-kpi audit-kpi-active-modules">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div class="audit-kpi-icon bg-white bg-opacity-20 rounded-3 p-3">
                  <span class="text-white fs-4">📚</span>
                </div>
              </div>
              <div class="flex-grow-1 ms-3 audit-kpi-content">
                <h6 class="mb-1 fw-normal">Módulos Activos</h6>
                <h3 class="mb-0 fw-bold">{{ activeModules }}</h3>
                <small>
                  <i class="fas fa-shield-alt"></i> Monitoreados
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Eventos Críticos -->
      <div class="col-xl-3 col-md-6 mb-3">
        <div class="card h-100 shadow-sm border-0 audit-kpi audit-kpi-critical-events">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div class="audit-kpi-icon bg-white bg-opacity-20 rounded-3 p-3">
                  <span class="text-white fs-4">⚠️</span>
                </div>
              </div>
              <div class="flex-grow-1 ms-3 audit-kpi-content">
                <h6 class="mb-1 fw-normal">Eventos Críticos</h6>
                <h3 class="mb-0 fw-bold">{{ criticalEvents }}</h3>
                <small>
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

    <!-- Loading state -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
      <p class="mt-2">Cargando datos de auditoría...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="alert alert-danger" role="alert">
      <i class="fas fa-exclamation-triangle me-2"></i>
      {{ error }}
      <button class="btn btn-sm btn-outline-danger ms-3" @click="fetchAuditData">
        <i class="fas fa-redo me-1"></i>Reintentar
      </button>
    </div>

    <!-- Componente de tabla -->
    <AuditTable v-else :events="events" @view-details="showDetails" />
 
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
import { ref, computed, onMounted } from "vue"
import AuditTable from "../../components/comun/AuditTable.vue"
import { auditService } from "../../services/api.js"
import '../../assets/css/Auditoria.css'

const events = ref([])
const selectedEvent = ref(null)
const loading = ref(true)
const error = ref(null)

// Filtro states
const dropdownOpen = ref(false)
const currentFilter = ref('all')
const currentFilterLabel = ref('Filtrar')

// KPIs Data
const totalEvents = ref(0)
const todayEvents = ref(0)
const activeUsers = ref(0)
const activeModules = ref(0)
const criticalEvents = ref(0)

// Module Activity Data (computed from backend data)
const moduleActivity = computed(() => {
  if (!events.value.length) return []

  const moduleCounts = {}
  events.value.forEach(event => {
    moduleCounts[event.module] = (moduleCounts[event.module] || 0) + 1
  })

  const total = Object.values(moduleCounts).reduce((sum, count) => sum + count, 0)

  return Object.entries(moduleCounts)
    .map(([name, count]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      count,
      percentage: Math.round((count / total) * 100),
      color: getModuleColor(name)
    }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5) // Top 5 modules
})

// Action Distribution Data (computed from backend data)
const actionDistribution = computed(() => {
  if (!events.value.length) return []

  const actionCounts = {}
  events.value.forEach(event => {
    const actionType = getActionTypeLabel(event.action)
    actionCounts[actionType] = (actionCounts[actionType] || 0) + 1
  })

  return Object.entries(actionCounts).map(([type, count]) => ({
    type,
    count,
    icon: getActionIcon(type),
    bgClass: getActionBgClass(type)
  }))
})

function getModuleColor(module) {
  const colors = {
    'usuarios': 'bg-primary',
    'reportes': 'bg-success',
    'encuestas': 'bg-warning',
    'configuracion': 'bg-info',
    'sistema': 'bg-secondary',
    'poblacion': 'bg-info',
    'social': 'bg-success',
    'salud': 'bg-danger'
  }
  return colors[module.toLowerCase()] || 'bg-secondary'
}

function getActionTypeLabel(action) {
  const labels = {
    'CREATE': 'Creación',
    'UPDATE': 'Modificación',
    'DELETE': 'Eliminación',
    'LOGIN': 'Inicio de sesión',
    'LOGOUT': 'Cierre de sesión',
    'VIEW': 'Visualización'
  }
  return labels[action] || action
}

function getActionIcon(type) {
  const icons = {
    'Creación': 'fas fa-plus-circle',
    'Modificación': 'fas fa-edit',
    'Eliminación': 'fas fa-trash',
    'Inicio de sesión': 'fas fa-sign-in-alt',
    'Cierre de sesión': 'fas fa-sign-out-alt',
    'Visualización': 'fas fa-eye'
  }
  return icons[type] || 'fas fa-cog'
}

function getActionBgClass(type) {
  const classes = {
    'Creación': 'bg-success bg-opacity-10 text-success',
    'Modificación': 'bg-warning bg-opacity-10 text-warning',
    'Eliminación': 'bg-danger bg-opacity-10 text-danger',
    'Inicio de sesión': 'bg-info bg-opacity-10 text-info',
    'Cierre de sesión': 'bg-secondary bg-opacity-10 text-secondary',
    'Visualización': 'bg-primary bg-opacity-10 text-primary'
  }
  return classes[type] || 'bg-secondary bg-opacity-10 text-secondary'
}

// Recent Activity Data (computed from backend data)
const recentActivity = computed(() => {
  return events.value
    .slice(0, 10) // Get most recent 10 events
    .map(event => ({
      id: event.id,
      title: getActivityTitle(event),
      user: event.user,
      module: event.module,
      time: getRelativeTime(event.date),
      status: event.status,
      statusClass: getStatusClass(event.status),
      icon: getActivityIcon(event.action),
      avatarClass: getAvatarClass(event.status)
    }))
})

function getActivityTitle(event) {
  const actionLabels = {
    'CREATE': 'creado',
    'UPDATE': 'actualizado',
    'DELETE': 'eliminado',
    'LOGIN': 'inició sesión',
    'LOGOUT': 'cerró sesión',
    'VIEW': 'visualizó'
  }

  const action = actionLabels[event.action] || 'realizó acción'
  return `${event.module.charAt(0).toUpperCase() + event.module.slice(1)} ${action}`
}

function getRelativeTime(dateStr) {
  const now = new Date()
  const eventDate = new Date(dateStr.split('/').reverse().join('-')) // Convert dd/mm/yyyy to yyyy-mm-dd

  const diffMs = now - eventDate
  const diffMins = Math.floor(diffMs / (1000 * 60))
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

  if (diffMins < 60) {
    return `hace ${diffMins} minuto${diffMins !== 1 ? 's' : ''}`
  } else if (diffHours < 24) {
    return `hace ${diffHours} hora${diffHours !== 1 ? 's' : ''}`
  } else {
    return `hace ${diffDays} día${diffDays !== 1 ? 's' : ''}`
  }
}

function getStatusClass(status) {
  const classes = {
    'Completado': 'bg-success',
    'Advertencia': 'bg-warning',
    'Crítico': 'bg-danger'
  }
  return classes[status] || 'bg-secondary'
}

function getActivityIcon(action) {
  const icons = {
    'CREATE': 'fas fa-plus-circle',
    'UPDATE': 'fas fa-edit',
    'DELETE': 'fas fa-trash-alt',
    'LOGIN': 'fas fa-sign-in-alt',
    'LOGOUT': 'fas fa-sign-out-alt',
    'VIEW': 'fas fa-eye'
  }
  return icons[action] || 'fas fa-cog'
}

function getAvatarClass(status) {
  const classes = {
    'Completado': 'bg-success bg-opacity-10 text-success',
    'Advertencia': 'bg-warning bg-opacity-10 text-warning',
    'Crítico': 'bg-danger bg-opacity-10 text-danger'
  }
  return classes[status] || 'bg-secondary bg-opacity-10 text-secondary'
}

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
async function fetchAuditData() {
  try {
    loading.value = true
    error.value = null

    // Fetch audit logs and stats in parallel
    const [logsResponse, statsResponse] = await Promise.all([
      auditService.getAuditLogs(),
      auditService.getAuditStats()
    ])

    // Transform audit logs to match frontend structure
    events.value = logsResponse.data.map(log => ({
      id: log.id_audit,
      module: log.modelo,
      user: log.usuario_username || 'Sistema',
      action: log.accion,
      date: new Date(log.fecha).toLocaleDateString('es-ES'),
      changes: transformChanges(log.datos_anteriores, log.datos_nuevos),
      description: log.descripcion,
      status: getStatusFromAction(log.accion)
    }))

    // Update KPIs from stats
    totalEvents.value = statsResponse.data.total_logs || 0
    activeUsers.value = statsResponse.data.usuarios_activos || 0
    activeModules.value = statsResponse.data.modelos?.length || 0

    // Calculate today events (simplified - in real app might need backend support)
    const today = new Date().toISOString().split('T')[0]
    todayEvents.value = events.value.filter(event =>
      event.date === new Date().toLocaleDateString('es-ES')
    ).length

    // Calculate critical events (DELETE actions)
    criticalEvents.value = events.value.filter(event =>
      event.status === 'Crítico'
    ).length

  } catch (err) {
    error.value = 'Error al cargar los datos de auditoría'
    console.error('Error fetching audit data:', err)
  } finally {
    loading.value = false
  }
}

function transformChanges(oldData, newData) {
  const changes = {}
  if (oldData && newData) {
    Object.keys(newData).forEach(key => {
      if (oldData[key] !== newData[key]) {
        changes[key] = {
          old: oldData[key] || '-',
          new: newData[key] || '-'
        }
      }
    })
  }
  return changes
}

function getStatusFromAction(action) {
  switch (action) {
    case 'CREATE':
      return 'Completado'
    case 'UPDATE':
      return 'Completado'
    case 'DELETE':
      return 'Crítico'
    case 'LOGIN':
      return 'Completado'
    case 'LOGOUT':
      return 'Completado'
    case 'VIEW':
      return 'Completado'
    default:
      return 'Advertencia'
  }
}

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

// Lifecycle
onMounted(() => {
  fetchAuditData()
})
</script>