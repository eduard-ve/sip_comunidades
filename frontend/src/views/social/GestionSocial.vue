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
          v-model="form.programa" 
          class="form-control mb-2" 
          placeholder="Nombre del Programa" 
          required 
        />
        <input 
          v-model.number="form.beneficiarios" 
          type="number" 
          class="form-control mb-2" 
          placeholder="Número de Beneficiarios" 
          required 
        />
        <!-- Select de estado alineado -->
        <select v-model="form.estado" class="form-control mb-3" required>
          <option disabled value="">Seleccione un estado</option>
          <option value="Activo">Activo</option>
          <option value="Inactivo">Inactivo</option>
          <option value="Suspendido">Suspendido</option>
          <option value="Completado">Tramite</option>
        </select>
        <div class="text-end">
          <button type="button" class="btn btn-secondary btn-sm me-2" @click="closeForm">Cancelar</button>
          <button type="submit" class="btn btn-primary btn-sm">Guardar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BaseModule from '../../components/comun/BaseModule.vue'
import MapPanel from '../../components/mapas/MapPanel.vue'
import ChartPanel from '../../components/graficas/ChartPanel.vue'

// KPIs
const kpis = ref([
  { title: 'Programas activos', value: 12, change: '+2', icon: 'bi-people' },
  { title: 'Beneficiarios totales', value: 340, change: '+15', icon: 'bi-person-check' },
  { title: 'Actividades culturales', value: 8, change: '+1', icon: 'bi-music-note-beamed' },
  { title: 'Cobertura territorial', value: '5 regiones', change: '+1', icon: 'bi-geo-alt' }
])

// Actividades recientes
const actividades = ref([
  'Festival comunitario de música',
  'Taller de arte para niños',
  'Campaña de salud preventiva',
  'Charla sobre medio ambiente'
])

// Chart de impacto social
const impactoData = ref({
  labels: ['Programa A', 'Programa B', 'Programa C'],
  datasets: [{ label: 'Beneficiarios', data: [120, 95, 125], backgroundColor: '#0d6efd' }]
})

// Tabla de programas con columna de acciones
const tableColumns = [
  { key: 'programa', label: 'Programa' },
  { key: 'beneficiarios', label: 'Beneficiarios' },
  { key: 'estado', label: 'Estado' },
  { key: 'acciones', label: 'Acciones', class: 'text-center'}
]

const programas = ref([
  { programa: 'Programa A', beneficiarios: 120, estado: 'Activo' },
  { programa: 'Programa B', beneficiarios: 95, estado: 'Inactivo' },
  { programa: 'Programa C', beneficiarios: 125, estado: 'Suspendido' }
])

// Mapas de cobertura
const mapProgramas = ref([
  { nombre: 'Programa A', coordenadas: [-12.0464, -77.0428] },
  { nombre: 'Programa B', coordenadas: [-16.4090, -71.5375] },
  { nombre: 'Programa C', coordenadas: [-12.0464, -77.0428] }
])

// Modal formulario
const showForm = ref(false)
const form = ref({ programa: '', beneficiarios: '', estado: '' })
const editIndex = ref(null)

// Funciones del modal
function closeForm() {
  showForm.value = false
  form.value = { programa: '', beneficiarios: '', estado: '' }
  editIndex.value = null
}

function savePrograma() {
  if (editIndex.value !== null) {
    programas.value[editIndex.value] = { ...form.value }
  } else {
    programas.value.push({ ...form.value })
  }
  closeForm()
}

function editPrograma(row) {
  editIndex.value = programas.value.indexOf(row)
  form.value = { ...row }
  showForm.value = true
}

function deletePrograma(row) {
  const idx = programas.value.indexOf(row)
  if (idx !== -1 && confirm('¿Seguro que deseas eliminar este registro?')) {
    programas.value.splice(idx, 1)
  }
}

// Eventos
function onExport() { console.log('Exportar datos') }
function onRowClick(row) { console.log('Fila clickeada', row) }
</script>

<style scoped>
.modal-backdrop {
  position: fixed; top:0; left:0; width:100%; height:100%;
  background: rgba(0,0,0,0.5); display:flex; justify-content:center; align-items:center; z-index:1050;
}
.modal-card {
  background:white; padding:20px; border-radius:10px; width:100%; max-width:400px;
}
</style>
