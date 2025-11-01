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
        <h5>Actividades culturales/comunitarias recientes</h5>
        <ul>
          <li v-for="(act, idx) in actividades" :key="idx">{{ act }}</li>
        </ul>
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
          class="form-control mb-3"
          placeholder="Fecha de Fin"
        />
        <div class="text-end">
          <button type="button" class="btn btn-secondary btn-sm me-2" @click="closeForm">Cancelar</button>
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
  { title: 'Cobertura territorial', value: '0 regiones', change: '+0', icon: 'bi-geo-alt' }
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

// Estados de carga
const loading = ref(false)
const error = ref(null)

// Modal formulario
const showForm = ref(false)
const form = ref({ nombre: '', descripcion: '', estado_id: '', fecha_inicio: '', fecha_fin: '' })
const editIndex = ref(null)

// Funciones para cargar datos del backend
async function loadProgramasSociales() {
  try {
    loading.value = true
    const response = await socialService.getProgramasSociales()
    programas.value = response.data.map(programa => ({
      ...programa,
      beneficiarios_count: programa.beneficiarios ? programa.beneficiarios.length : 0,
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
    console.error('Error loading actividades:', err)
  }
}

async function loadCoberturasProgramas() {
  try {
    const response = await socialService.getCoberturasProgramas()
    mapProgramas.value = response.data.map(cobertura => ({
      nombre: cobertura.programa.nombre,
      coordenadas: [parseFloat(cobertura.latitud), parseFloat(cobertura.longitud)]
    }))
    kpis.value[3].value = `${response.data.length} regiones`
  } catch (err) {
    console.error('Error loading coberturas:', err)
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

// Cargar todos los datos al montar el componente
onMounted(async () => {
  await Promise.all([
    loadProgramasSociales(),
    loadActividadesSociales(),
    loadCoberturasProgramas(),
    loadEstadosProgramas()
  ])
})

// Funciones del modal
function closeForm() {
  showForm.value = false
  form.value = { nombre: '', descripcion: '', estado_id: '', fecha_inicio: '', fecha_fin: '' }
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
    fecha_fin: row.fecha_fin || ''
  }
  showForm.value = true
}

async function deletePrograma(row) {
  if (confirm('¿Seguro que deseas eliminar este programa?')) {
    try {
      await socialService.deleteProgramaSocial(row.id)
      await loadProgramasSociales() // Recargar datos
    } catch (err) {
      error.value = 'Error al eliminar el programa'
      console.error('Error deleting programa:', err)
    }
  }
}

// Eventos
function onExport() { console.log('Exportar datos') }
function onRowClick(row) { console.log('Fila clickeada', row) }
</script>
