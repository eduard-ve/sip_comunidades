<template>
  <BaseModule
    title="Gestión Social"
    :kpis="kpis"
    :charts="charts"
    :table="{ columns: tableColumns, rows: programas }"
    search-placeholder="Buscar programas o beneficiarios…"
    :show-create="true"
    @create="showForm = true"
    @export="onExport"
    @rowClick="onRowClick"
  >
    <!-- Personalización de celdas de la tabla -->
    <template #table-cell="{ column, row }">
      <!-- Si es columna acciones -->
      <div v-if="column.key === 'acciones'" class="d-flex gap-2 justify-content-center">
        <button class="btn btn-sm btn-outline-primary" @click="editPrograma(row)">
          <i class="bi bi-pencil"></i>
        </button>
        <button class="btn btn-sm btn-outline-danger" @click="deletePrograma(row)">
          <i class="bi bi-trash"></i>
        </button>
      </div>
      <!-- Para el resto de columnas -->
      <span v-else>{{ row[column.key] }}</span>
    </template>

    <!-- Extra contenido encima de charts -->
    <template #extra>
      <div class="mb-3">
        <ul>
          <li v-for="(act, idx) in actividades" :key="idx">{{ act }}</li>
        </ul>
      </div>
      <div class="mb-3">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5>Autoridades Comunitarias Activas</h5>
          <button class="btn btn-success btn-sm" @click="showAutoridadForm = true">
            <i class="bi bi-plus-circle me-1"></i>
            Nueva Autoridad
          </button>
        </div>
        <div class="row">
          <div v-for="autoridad in autoridadesActivas" :key="autoridad.id" class="col-md-6 mb-2">
            <div class="card">
              <div class="card-body p-2">
                <h6 class="card-title mb-1">{{ autoridad.persona.nombre_completo }}</h6>
                <p class="card-text small mb-1">
                  <strong>Rol:</strong> {{ autoridad.rol.nombre }}<br>
                  <strong>Tipo:</strong> {{ autoridad.tipo_autoridad.nombre }}<br>
                  <strong>Contacto:</strong> {{ autoridad.telefono_contacto || 'N/A' }}
                </p>
                <div class="d-flex gap-1">
                  <button class="btn btn-outline-primary btn-sm" @click="editAutoridad(autoridad)">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button class="btn btn-outline-danger btn-sm" @click="deleteAutoridad(autoridad)">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="mb-3">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5>Actividades Comunitarias</h5>
          <button class="btn btn-primary btn-sm" @click="showActividadForm = true">
            <i class="bi bi-plus-circle me-1"></i>
            Nueva Actividad
          </button>
        </div>
        <div class="row">
          <div v-for="actividad in actividadesComunitarias" :key="actividad.id" class="col-md-6 mb-2">
            <div class="card">
              <div class="card-body p-2">
                <h6 class="card-title mb-1">{{ actividad.titulo }}</h6>
                <p class="card-text small mb-1">
                  <strong>Tipo:</strong> {{ actividad.tipo_actividad.nombre }}<br>
                  <strong>Fecha:</strong> {{ new Date(actividad.fecha_inicio).toLocaleDateString() }}<br>
                  <strong>Asistentes:</strong> {{ actividad.asistentes_confirmados }}/{{ actividad.capacidad_maxima || '∞' }}
                </p>
                <div class="d-flex gap-1">
                  <button class="btn btn-outline-primary btn-sm" @click="editActividad(actividad)">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button class="btn btn-outline-danger btn-sm" @click="deleteActividad(actividad)">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Mapas de cobertura de programas -->
    <template #left>
      <MapPanel :programas="mapProgramas" />
    </template>

    <!-- ChartPanel de estadísticas de impacto social -->
    <template #right>
      <ChartPanel
        chart-id="impactoSocialChart"
        type="bar"
        :data="impactoData"
        :options="{ responsive: true }"
      >
        <template #title>Estadísticas de impacto social</template>
      </ChartPanel>
    </template>

    <!-- Tabla de beneficiarios por programa -->
    <template #table-footer>
      <div class="mt-3">
        <h6>Beneficiarios por programa</h6>
      </div>
    </template>
  </BaseModule>

  <!-- Modal para crear/editar programa -->
  <div v-if="showForm" class="modal-backdrop">
    <div class="modal-card">
      <h5 class="mb-3">{{ editIndex !== null ? 'Editar Programa' : 'Nuevo Programa' }}</h5>
      <form @submit.prevent="savePrograma">
        <input
          v-model="form.nombre"
          class="form-control mb-2"
          placeholder="Nombre del Programa"
          required
        />
        <textarea
          v-model="form.descripcion"
          class="form-control mb-2"
          placeholder="Descripción del Programa"
          rows="3"
        ></textarea>
        <!-- Select de estado alineado -->
        <select v-model="form.estado_id" class="form-control mb-2" required>
          <option disabled value="">Seleccione un estado</option>
          <option v-for="estado in estados" :key="estado.id" :value="estado.id">
            {{ estado.nombre }}
          </option>
        </select>
        <input
          v-model="form.fecha_inicio"
          type="date"
          class="form-control mb-2"
          placeholder="Fecha de Inicio"
        />
        <input
          v-model="form.fecha_fin"
          type="date"
          class="form-control mb-2"
          placeholder="Fecha de Fin"
        />
        <input
          v-model.number="form.beneficiarios_count"
          type="number"
          class="form-control mb-3"
          placeholder="Cantidad de Beneficiarios"
          min="0"
          required
        />
        <div class="text-end">
          <button type="button" class="btn btn-secondary btn-sm me-2" @click="closeForm">Cancelar</button>
          <button type="submit" class="btn btn-primary btn-sm">Guardar</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Modal para crear/editar autoridad -->
  <div v-if="showAutoridadForm" class="modal-backdrop">
    <div class="modal-card">
      <h5 class="mb-3">{{ editAutoridadIndex !== null ? 'Editar Autoridad' : 'Nueva Autoridad' }}</h5>
      <form @submit.prevent="saveAutoridad">
        <!-- Búsqueda por cédula -->
        <div class="row mb-3">
          <div class="col-md-8">
            <label class="form-label fw-semibold">Buscar por Número de Identificación</label>
            <input
              v-model="autoridadForm.numero_identificacion"
              type="text"
              class="form-control"
              placeholder="Ingrese número de cédula..."
              :disabled="buscandoPersona"
            />
          </div>
          <div class="col-md-4 d-flex align-items-end">
            <button
              type="button"
              class="btn btn-outline-primary w-100"
              @click="buscarPersonaPorCedula"
              :disabled="!autoridadForm.numero_identificacion.trim() || buscandoPersona"
            >
              <span v-if="buscandoPersona" class="spinner-border spinner-border-sm me-2"></span>
              Buscar
            </button>
          </div>
        </div>

        <!-- Información de la persona encontrada -->
        <div v-if="personaSeleccionada" class="alert alert-success mb-3">
          <h6 class="alert-heading mb-2">✅ Persona Encontrada</h6>
          <p class="mb-1"><strong>Nombre:</strong> {{ personaSeleccionada.nombre_completo }}</p>
          <p class="mb-1"><strong>ID:</strong> {{ personaSeleccionada.numero_identificacion }}</p>
          <p class="mb-0"><strong>Tipo ID:</strong> {{ personaSeleccionada.tipo_identificacion }}</p>
        </div>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label fw-semibold">Tipo de Autoridad</label>
            <select v-model="autoridadForm.tipo_autoridad_id" class="form-control" required>
              <option disabled value="">Seleccione tipo</option>
              <option v-for="tipo in tiposAutoridad" :key="tipo.id" :value="tipo.id">
                {{ tipo.nombre }}
              </option>
            </select>
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label fw-semibold">Rol</label>
            <select v-model="autoridadForm.rol_id" class="form-control" required>
              <option disabled value="">Seleccione rol</option>
              <option v-for="rol in rolesAutoridad" :key="rol.id" :value="rol.id">
                {{ rol.nombre }}
              </option>
            </select>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label fw-semibold">Fecha Inicio Mandato</label>
            <input
              v-model="autoridadForm.fecha_inicio_mandato"
              type="date"
              class="form-control"
              required
            />
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label fw-semibold">Fecha Fin Mandato (Opcional)</label>
            <input
              v-model="autoridadForm.fecha_fin_mandato"
              type="date"
              class="form-control"
            />
          </div>
        </div>
        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label fw-semibold">Teléfono de Contacto</label>
            <input
              v-model="autoridadForm.telefono_contacto"
              type="tel"
              class="form-control"
              placeholder="3001234567"
            />
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label fw-semibold">Email de Contacto</label>
            <input
              v-model="autoridadForm.email_contacto"
              type="email"
              class="form-control"
              placeholder="autoridad@example.com"
            />
          </div>
        </div>
        <div class="mb-3">
          <label class="form-label fw-semibold">Observaciones</label>
          <textarea
            v-model="autoridadForm.observaciones"
            class="form-control"
            rows="3"
            placeholder="Observaciones adicionales..."
          ></textarea>
        </div>
        <div class="mb-3 form-check">
          <input
            v-model="autoridadForm.activo"
            class="form-check-input"
            type="checkbox"
            id="activoCheck"
          />
          <label class="form-check-label fw-semibold" for="activoCheck">
            Autoridad Activa
          </label>
        </div>
        <div class="text-end">
          <button type="button" class="btn btn-secondary btn-sm me-2" @click="closeAutoridadForm">Cancelar</button>
          <button type="submit" class="btn btn-primary btn-sm">Guardar</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Modal para crear/editar actividad -->
  <div v-if="showActividadForm" class="modal-backdrop">
    <div class="modal-card">
      <h5 class="mb-3">{{ editActividadIndex !== null ? 'Editar Actividad' : 'Nueva Actividad' }}</h5>
      <form @submit.prevent="saveActividad">
        <div class="row">
          <div class="col-md-8 mb-3">
            <label class="form-label fw-semibold">Título de la Actividad</label>
            <input
              v-model="actividadForm.titulo"
              type="text"
              class="form-control"
              placeholder="Ingrese el título..."
              required
            />
          </div>
          <div class="col-md-4 mb-3">
            <label class="form-label fw-semibold">Tipo de Actividad</label>
            <select v-model="actividadForm.tipo_actividad_id" class="form-control" required>
              <option disabled value="">Seleccione tipo</option>
              <option v-for="tipo in tiposActividad" :key="tipo.id" :value="tipo.id">
                {{ tipo.nombre }}
              </option>
            </select>
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label fw-semibold">Descripción</label>
          <textarea
            v-model="actividadForm.descripcion"
            class="form-control"
            rows="3"
            placeholder="Descripción de la actividad..."
          ></textarea>
        </div>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label fw-semibold">Estado</label>
            <select v-model="actividadForm.estado_id" class="form-control" required>
              <option disabled value="">Seleccione estado</option>
              <option v-for="estado in estadosActividad" :key="estado.id" :value="estado.id">
                {{ estado.nombre }}
              </option>
            </select>
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label fw-semibold">Ubicación</label>
            <input
              v-model="actividadForm.ubicacion"
              type="text"
              class="form-control"
              placeholder="Lugar donde se realiza..."
            />
          </div>
        </div>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label fw-semibold">Fecha y Hora de Inicio</label>
            <input
              v-model="actividadForm.fecha_inicio"
              type="datetime-local"
              class="form-control"
              required
            />
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label fw-semibold">Fecha y Hora de Fin (Opcional)</label>
            <input
              v-model="actividadForm.fecha_fin"
              type="datetime-local"
              class="form-control"
            />
          </div>
        </div>

        <div class="row">
          <div class="col-md-6 mb-3">
            <label class="form-label fw-semibold">Capacidad Máxima</label>
            <input
              v-model.number="actividadForm.capacidad_maxima"
              type="number"
              class="form-control"
              placeholder="0"
              min="0"
            />
          </div>
          <div class="col-md-6 mb-3">
            <label class="form-label fw-semibold">Organizador</label>
            <input
              v-model="actividadForm.organizador"
              type="text"
              class="form-control"
              placeholder="Nombre del organizador..."
            />
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label fw-semibold">Observaciones</label>
          <textarea
            v-model="actividadForm.observaciones"
            class="form-control"
            rows="3"
            placeholder="Observaciones adicionales..."
          ></textarea>
        </div>

        <div class="text-end">
          <button type="button" class="btn btn-secondary btn-sm me-2" @click="closeActividadForm">Cancelar</button>
          <button type="submit" class="btn btn-primary btn-sm">Guardar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BaseModule from '../../components/comun/BaseModule.vue'
import MapPanel from '../../components/mapas/MapPanel.vue'
import ChartPanel from '../../components/graficas/ChartPanel.vue'
import { socialService } from '../../services/api.js'
import '../../assets/css/GestionSocial.css'

// Reactive data
const kpis = ref([
  { title: 'Programas activos', value: 0, change: '+0', icon: 'bi-people' },
  { title: 'Beneficiarios totales', value: 0, change: '+0', icon: 'bi-person-check' },
  { title: 'Actividades culturales', value: 0, change: '+0', icon: 'bi-music-note-beamed' },
  { title: 'Autoridades activas', value: 0, change: '+0', icon: 'bi-person-badge' }
])

const actividades = ref([])
const impactoData = ref({
  labels: [],
  datasets: [{ label: 'Beneficiarios', data: [], backgroundColor: '#0d6efd' }]
})

const tableColumns = [
  { key: 'nombre', label: 'Programa' },
  { key: 'beneficiarios_count', label: 'Beneficiarios' },
  { key: 'estado', label: 'Estado' },
  { key: 'acciones', label: 'Acciones', class: 'text-center'}
]

const programas = ref([])
const mapProgramas = ref([])
const estados = ref([])
const autoridadesActivas = ref([])
const actividadesComunitarias = ref([])

// Estados de carga
const loading = ref(false)
const error = ref(null)

// Modal formulario programas
const showForm = ref(false)
const form = ref({ nombre: '', descripcion: '', estado_id: '', fecha_inicio: '', fecha_fin: '', beneficiarios_count: 0 })
const editIndex = ref(null)

// Modal formulario autoridades
const showAutoridadForm = ref(false)
const autoridadForm = ref({
  persona_id: '',
  numero_identificacion: '',
  tipo_autoridad_id: '',
  rol_id: '',
  fecha_inicio_mandato: '',
  fecha_fin_mandato: '',
  telefono_contacto: '',
  email_contacto: '',
  observaciones: '',
  activo: true
})
const editAutoridadIndex = ref(null)

// Modal formulario actividades
const showActividadForm = ref(false)
const actividadForm = ref({
  titulo: '',
  descripcion: '',
  tipo_actividad_id: '',
  estado_id: '',
  fecha_inicio: '',
  fecha_fin: '',
  ubicacion: '',
  capacidad_maxima: '',
  organizador: '',
  observaciones: ''
})
const editActividadIndex = ref(null)

// Datos para autoridades
const tiposAutoridad = ref([])
const rolesAutoridad = ref([])
const personaSeleccionada = ref(null)
const buscandoPersona = ref(false)

// Datos para actividades comunitarias
const tiposActividad = ref([])
const estadosActividad = ref([])

// Agregar console.log para debugging
console.log('Componente GestionSocial montado')
console.log('tiposActividad inicial:', tiposActividad.value)
console.log('estadosActividad inicial:', estadosActividad.value)

// Funciones para cargar datos del backend
async function loadProgramasSociales() {
  try {
    loading.value = true
    const response = await socialService.getProgramasSociales()
    programas.value = response.data.map(programa => ({
      ...programa,
      estado: programa.estado ? programa.estado.nombre : 'Sin estado'
    }))

    // Actualizar KPIs
    const programasActivos = programas.value.filter(p => p.estado === 'Activo').length
    const totalBeneficiarios = programas.value.reduce((sum, p) => sum + p.beneficiarios_count, 0)
    kpis.value[0].value = programasActivos
    kpis.value[1].value = totalBeneficiarios

    // Actualizar chart de impacto
    impactoData.value.labels = programas.value.map(p => p.nombre)
    impactoData.value.datasets[0].data = programas.value.map(p => p.beneficiarios_count)

    // Actualizar KPI de autoridades comunitarias
    await loadAutoridadesComunitarias()
  } catch (err) {
    error.value = 'Error al cargar programas sociales'
    console.error('Error loading programas:', err)
  } finally {
    loading.value = false
  }
}

async function loadActividadesSociales() {
  try {
    const response = await socialService.getActividadesSociales()
    actividades.value = response.data.map(act => act.titulo)
    kpis.value[2].value = actividades.value.length
  } catch (err) {
    console.error('Error loading actividades sociales:', err)
    actividades.value = []
    kpis.value[2].value = 0
  }

  // Siempre mostrar actividades comunitarias como respaldo
  if (actividadesComunitarias.value.length > 0) {
    actividades.value = actividadesComunitarias.value.map(act => act.titulo)
    kpis.value[2].value = actividades.value.length
  }
}

async function loadCoberturasProgramas() {
  try {
    const response = await socialService.getCoberturasProgramas()
    mapProgramas.value = response.data.map(cobertura => ({
      nombre: cobertura.programa.nombre,
      coordenadas: [Number.parseFloat(cobertura.latitud), Number.parseFloat(cobertura.longitud)]
    }))
    // Cambiar KPI de cobertura territorial por autoridades comunitarias
    // kpis.value[3].value = `${response.data.length} regiones`
  } catch (err) {
    console.error('Error loading coberturas:', err)
  }
}

async function loadAutoridadesComunitarias() {
  try {
    const response = await socialService.getAutoridadesComunitarias()
    autoridadesActivas.value = response.data.filter(aut => aut.activo)
    kpis.value[3].value = autoridadesActivas.value.length
  } catch (err) {
    console.error('Error loading autoridades:', err)
  }
}

async function loadEstadosProgramas() {
  try {
    const response = await socialService.getEstadosProgramas()
    estados.value = response.data
  } catch (err) {
    console.error('Error loading estados:', err)
  }
}

// Funciones para cargar datos de autoridades
async function loadTiposAutoridad() {
  try {
    const response = await socialService.getTiposAutoridad()
    tiposAutoridad.value = response.data
  } catch (err) {
    console.error('Error loading tipos autoridad:', err)
  }
}

async function loadRolesAutoridad() {
  try {
    const response = await socialService.getRolesAutoridad()
    rolesAutoridad.value = response.data
  } catch (err) {
    console.error('Error loading roles autoridad:', err)
  }
}

// Funciones para cargar datos de actividades comunitarias
async function loadTiposActividad() {
  try {
    console.log('Cargando tipos de actividad...')
    const response = await socialService.getTiposActividad()
    tiposActividad.value = response.data
    console.log('Tipos de actividad cargados:', tiposActividad.value.length, 'elementos')
    console.log('Primeros tipos:', tiposActividad.value.slice(0, 3))
  } catch (err) {
    console.error('Error loading tipos actividad:', err)
    tiposActividad.value = []
  }
}

async function loadEstadosActividad() {
  try {
    console.log('Cargando estados de actividad...')
    const response = await socialService.getEstadosActividad()
    estadosActividad.value = response.data
    console.log('Estados de actividad cargados:', estadosActividad.value.length, 'elementos')
    console.log('Primeros estados:', estadosActividad.value.slice(0, 3))
  } catch (err) {
    console.error('Error loading estados actividad:', err)
    estadosActividad.value = []
  }
}

async function loadActividadesComunitarias() {
  try {
    console.log('Cargando actividades comunitarias...')
    const response = await socialService.getActividadesComunitarias()
    actividadesComunitarias.value = response.data
    console.log('Actividades comunitarias cargadas:', actividadesComunitarias.value.length, 'elementos')
    console.log('Primeras actividades:', actividadesComunitarias.value.slice(0, 2))
  } catch (err) {
    console.error('Error loading actividades comunitarias:', err)
    actividadesComunitarias.value = []
  }
}

async function buscarPersonaPorCedula() {
  if (!autoridadForm.value.numero_identificacion.trim()) {
    alert('Por favor ingrese un número de identificación')
    return
  }

  buscandoPersona.value = true
  try {
    const response = await socialService.buscarPersonaPorCedula(autoridadForm.value.numero_identificacion)
    personaSeleccionada.value = response.data.persona

    if (response.data.es_autoridad_activa) {
      alert('Esta persona ya es una autoridad activa')
      return
    }

    // Auto-llenar campos
    autoridadForm.value.persona_id = response.data.persona.id
    autoridadForm.value.telefono_contacto = response.data.persona.direccion || ''
    autoridadForm.value.email_contacto = ''

  } catch (err) {
    console.error('Error buscando persona:', err)
    alert('Persona no encontrada o error en la búsqueda')
    personaSeleccionada.value = null
  } finally {
    buscandoPersona.value = false
  }
}

// Cargar todos los datos al montar el componente
onMounted(async () => {
  console.log('Iniciando carga de datos...')
  try {
    // Cargar primero los tipos y estados que necesita el formulario
    await Promise.all([
      loadTiposActividad(),
      loadEstadosActividad()
    ])
    console.log('Tipos y estados cargados:', tiposActividad.value.length, estadosActividad.value.length)

    // Luego cargar el resto de datos
    await Promise.all([
      loadProgramasSociales(),
      loadActividadesSociales(),
      loadCoberturasProgramas(),
      loadEstadosProgramas(),
      loadAutoridadesComunitarias(),
      loadTiposAutoridad(),
      loadRolesAutoridad(),
      loadPersonasDisponibles(),
      loadActividadesComunitarias()
    ])
  } catch (error) {
    console.error('Error en carga inicial:', error)
  }
  console.log('Carga de datos completada')
  console.log('Estado final - tiposActividad:', tiposActividad.value)
  console.log('Estado final - estadosActividad:', estadosActividad.value)
})

// Funciones del modal
function closeForm() {
  showForm.value = false
  form.value = { nombre: '', descripcion: '', estado_id: '', fecha_inicio: '', fecha_fin: '', beneficiarios_count: 0 }
  editIndex.value = null
}

async function savePrograma() {
  try {
    if (editIndex.value !== null) {
      // Actualizar programa existente
      const programa = programas.value[editIndex.value]
      await socialService.updateProgramaSocial(programa.id, form.value)
    } else {
      // Crear nuevo programa
      await socialService.createProgramaSocial(form.value)
    }
    closeForm()
    await loadProgramasSociales() // Recargar datos
  } catch (err) {
    error.value = 'Error al guardar el programa'
    console.error('Error saving programa:', err)
  }
}

function editPrograma(row) {
  editIndex.value = programas.value.indexOf(row)
  form.value = {
    nombre: row.nombre,
    descripcion: row.descripcion || '',
    estado_id: row.estado_id || '',
    fecha_inicio: row.fecha_inicio || '',
    fecha_fin: row.fecha_fin || '',
    beneficiarios_count: row.beneficiarios_count || 0
  }
  showForm.value = true
}

async function deletePrograma(row) {
  if (window.confirm('¿Seguro que deseas eliminar este programa?')) {
    try {
      await socialService.deleteProgramaSocial(row.id)
      await loadProgramasSociales() // Recargar datos
    } catch (err) {
      error.value = 'Error al eliminar el programa'
      console.error('Error deleting programa:', err)
    }
  }
}

// Funciones para autoridades
function closeAutoridadForm() {
  showAutoridadForm.value = false
  autoridadForm.value = {
    persona_id: '',
    numero_identificacion: '',
    tipo_autoridad_id: '',
    rol_id: '',
    fecha_inicio_mandato: '',
    fecha_fin_mandato: '',
    telefono_contacto: '',
    email_contacto: '',
    observaciones: '',
    activo: true
  }
  editAutoridadIndex.value = null
  personaSeleccionada.value = null
}

async function saveAutoridad() {
  try {
    // Preparar datos para enviar (excluir numero_identificacion que no va al backend)
    const dataToSend = { ...autoridadForm.value }
    delete dataToSend.numero_identificacion

    if (editAutoridadIndex.value !== null) {
      // Actualizar autoridad existente
      const autoridad = autoridadesActivas.value[editAutoridadIndex.value]
      await socialService.updateAutoridadComunitaria(autoridad.id, dataToSend)
    } else {
      // Crear nueva autoridad
      await socialService.createAutoridadComunitaria(dataToSend)
    }
    closeAutoridadForm()
    await loadAutoridadesComunitarias()
    await loadPersonasDisponibles() // Recargar personas disponibles
    // Mostrar mensaje de éxito
    alert(editAutoridadIndex.value !== null ? 'Autoridad actualizada exitosamente' : 'Autoridad creada exitosamente')
  } catch (err) {
    console.error('Error saving autoridad:', err)
    alert('Error al guardar la autoridad. Verifica los datos e intenta nuevamente.')
  }
}

function editAutoridad(autoridad) {
  editAutoridadIndex.value = autoridadesActivas.value.indexOf(autoridad)
  autoridadForm.value = {
    persona_id: autoridad.persona.id,
    numero_identificacion: autoridad.persona.numero_identificacion,
    tipo_autoridad_id: autoridad.tipo_autoridad.id,
    rol_id: autoridad.rol.id,
    fecha_inicio_mandato: autoridad.fecha_inicio_mandato,
    fecha_fin_mandato: autoridad.fecha_fin_mandato || '',
    telefono_contacto: autoridad.telefono_contacto || '',
    email_contacto: autoridad.email_contacto || '',
    observaciones: autoridad.observaciones || '',
    activo: autoridad.activo
  }
  // Mostrar la persona como seleccionada
  personaSeleccionada.value = autoridad.persona
  showAutoridadForm.value = true
}

async function deleteAutoridad(autoridad) {
  if (globalThis.confirm('¿Seguro que deseas eliminar esta autoridad?')) {
    try {
      await socialService.deleteAutoridadComunitaria(autoridad.id)
      await loadActividadesComunitarias()
      await loadPersonasDisponibles() // Recargar personas disponibles
    } catch (err) {
      console.error('Error deleting autoridad:', err)
    }
  }
}

// Funciones para actividades comunitarias
function closeActividadForm() {
  showActividadForm.value = false
  actividadForm.value = {
    titulo: '',
    descripcion: '',
    tipo_actividad_id: '',
    estado_id: '',
    fecha_inicio: '',
    fecha_fin: '',
    ubicacion: '',
    capacidad_maxima: '',
    organizador: '',
    observaciones: ''
  }
  editActividadIndex.value = null
}

async function saveActividad() {
  try {
    // Preparar datos para enviar
    const dataToSend = {
      titulo: actividadForm.value.titulo,
      descripcion: actividadForm.value.descripcion,
      tipo_actividad_id: actividadForm.value.tipo_actividad_id,
      estado_id: actividadForm.value.estado_id,
      fecha_inicio: actividadForm.value.fecha_inicio,
      fecha_fin: actividadForm.value.fecha_fin || null,
      ubicacion: actividadForm.value.ubicacion,
      capacidad_maxima: actividadForm.value.capacidad_maxima || null,
      organizador: actividadForm.value.organizador || null,
      observaciones: actividadForm.value.observaciones
    }

    console.log('Enviando datos de actividad:', dataToSend)

    if (editActividadIndex.value !== null) {
      // Actualizar actividad existente
      const actividad = actividadesComunitarias.value[editActividadIndex.value]
      await socialService.updateActividadComunitaria(actividad.id, dataToSend)
    } else {
      // Crear nueva actividad
      await socialService.createActividadComunitaria(dataToSend)
    }
    closeActividadForm()
    await loadActividadesComunitarias()
    // Mostrar mensaje de éxito
    alert(editActividadIndex.value !== null ? 'Actividad actualizada exitosamente' : 'Actividad creada exitosamente')
  } catch (err) {
    console.error('Error saving actividad:', err)
    alert('Error al guardar la actividad. Verifica los datos e intenta nuevamente.')
  }
}

function editActividad(actividad) {
  editActividadIndex.value = actividadesComunitarias.value.indexOf(actividad)
  actividadForm.value = {
    titulo: actividad.titulo,
    descripcion: actividad.descripcion || '',
    tipo_actividad_id: actividad.tipo_actividad ? actividad.tipo_actividad.id : '',
    estado_id: actividad.estado ? actividad.estado.id : '',
    fecha_inicio: actividad.fecha_inicio,
    fecha_fin: actividad.fecha_fin || '',
    ubicacion: actividad.ubicacion || '',
    capacidad_maxima: actividad.capacidad_maxima || '',
    organizador: actividad.organizador || '',
    observaciones: actividad.observaciones || ''
  }
  showActividadForm.value = true
}

async function deleteActividad(actividad) {
  if (globalThis.confirm('¿Seguro que deseas eliminar esta actividad?')) {
    try {
      await socialService.deleteActividadComunitaria(actividad.id)
      await loadActividadesComunitarias()
    } catch (err) {
      console.error('Error deleting actividad:', err)
    }
  }
}

// Eventos
function onExport() { console.log('Exportar datos') }
function onRowClick(row) { console.log('Fila clickeada', row) }
</script>
