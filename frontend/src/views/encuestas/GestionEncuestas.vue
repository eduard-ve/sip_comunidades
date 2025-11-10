<template>
  <EncuestaBase
    title="Encuestas"
    :kpis="kpis"
    :charts="charts"
    :table="table"
    search-placeholder="Buscar encuesta…"
    @create="createSurvey"
    @rowClick="openSurvey"
  >
    <!-- El resto de tus templates actuales -->
    <template #table-filters>
      <div class="table-filters">
        <select v-model="selectedStatus" class="form-select form-select-sm">
          <option value="">Todos los estados</option>
          <option value="activa">Activa</option>
          <option value="cerrada">Cerrada</option>
          <option value="borrador">Borrador</option>
        </select>
      </div>
    </template>
    <template #table-footer>
      <div class="table-footer">
        <div class="text-muted small">
          Total: {{ filteredCount }} encuestas
        </div>
      </div>
    </template>
  </EncuestaBase>

  <!-- Modal para el formulario de la encuesta -->
  <div v-if="showForm" class="modal-backdrop" @click="cancelSurvey">
    <div class="modal-card" @click.stop>
      <EncuestaForm @save="saveSurvey" @cancel="cancelSurvey" />
    </div>
  </div>

</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter } from 'vue-router'
import EncuestaBase from "./components/EncuestaBase.vue"
import EncuestaForm from "../../components/formularios/EncuestaForm.vue"
import api from '../../services/api.js'
import '../../assets/css/GestionEncuestas.css'

const router = useRouter()

// Variables de estado
const showForm = ref(false)

// Datos de la interfaz
const kpis = ref([
  { title: "Encuestas activas", value: 5, change: "2", icon: "bi-clipboard-check", colorIcon: "#198754" },
  { title: "Respuestas totales", value: 1240, change: "120", icon: "bi-people", colorIcon: "#0d6efd" },
  { title: "Tasa de respuesta", value: "68%", change: "3", icon: "bi-bar-chart-line", colorIcon: "#ffc107" },
  { title: "Promedio satisfacción", value: "4.2/5", change: "0.3", icon: "bi-star", colorIcon: "#fd7e14" }
])

const charts = ref({
  left: {
    id: "chart1",
    type: "bar",
    title: "Respuestas por encuesta",
    data: {
      labels: ["Encuesta 1", "Encuesta 2", "Encuesta 3"],
      datasets: [{ label: "Respuestas", data: [120, 80, 200], backgroundColor: "#0d6efd" }]
    }
  },
  right: {
    id: "chart2",
    type: "pie",
    title: "Distribución por estado",
    data: {
      labels: ["Activa", "Cerrada", "Borrador"],
      datasets: [{ data: [3, 2, 1], backgroundColor: ["#198754", "#dc3545", "#6c757d"] }]
    }
  }
})

const table = ref({
  columns: [
    { key: "titulo", label: "Título" },
    { key: "estado", label: "Estado" },
    { key: "descripcion", label: "Descripción" },
    { key: "fecha", label: "Fecha" },
    { key: "respuestas", label: "Respuestas" }
  ],
  rows: []
})

const selectedStatus = ref("")

// Ciclo de vida: Cargar datos desde el backend al montar el componente
onMounted(async () => {
  await loadSurveys()
})

async function loadSurveys() {
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      console.warn('No hay token de autenticación - usando datos de muestra')
      // Fallback a datos de muestra cuando no hay token
      table.value.rows = [
        { titulo: "Satisfacción clientes", estado: "activa", descripcion: "Encuesta sobre satisfacción", preguntas: [], fecha: "2025-08-10", respuestas: 120 },
        { titulo: "Evaluación interna", estado: "cerrada", descripcion: "Evaluación de procesos internos", preguntas: [], fecha: "2025-07-22", respuestas: 80 },
        { titulo: "Clima laboral", estado: "activa", descripcion: "Encuesta sobre clima laboral", preguntas: [], fecha: "2025-08-05", respuestas: 200 },
        { titulo: "Mejoras 2026", estado: "borrador", descripcion: "Sugerencias para mejoras", preguntas: [], fecha: "-", respuestas: 0 }
      ]
      return
    }

    const response = await api.get('/encuestas/')

    if (response.status === 200) {
      const encuestas = response.data
      console.log('Encuestas cargadas desde backend:', encuestas.length)
      table.value.rows = encuestas.map(encuesta => ({
        id: encuesta.id_encuesta,
        titulo: encuesta.titulo,
        estado: encuesta.estado,
        descripcion: encuesta.descripcion,
        fecha: new Date(encuesta.fecha_creacion).toISOString().slice(0, 10),
        respuestas: encuesta.respuestas_count || 0
      }))
      console.log('Tabla actualizada con', table.value.rows.length, 'encuestas')
      saveToLocalStorage()
    } else if (response.status === 401) {
      console.warn('Token expirado o inválido - usando datos de muestra')
      // Fallback a datos de muestra
      table.value.rows = [
        { titulo: "Satisfacción clientes", estado: "activa", descripcion: "Encuesta sobre satisfacción", preguntas: [], fecha: "2025-08-10", respuestas: 120 },
        { titulo: "Evaluación interna", estado: "cerrada", descripcion: "Evaluación de procesos internos", preguntas: [], fecha: "2025-07-22", respuestas: 80 },
        { titulo: "Clima laboral", estado: "activa", descripcion: "Encuesta sobre clima laboral", preguntas: [], fecha: "2025-08-05", respuestas: 200 },
        { titulo: "Mejoras 2026", estado: "borrador", descripcion: "Sugerencias para mejoras", preguntas: [], fecha: "-", respuestas: 0 }
      ]
    } else {
      console.error('Error del servidor:', response.status)
      // Fallback a datos de muestra
      table.value.rows = [
        { titulo: "Satisfacción clientes", estado: "activa", descripcion: "Encuesta sobre satisfacción", preguntas: [], fecha: "2025-08-10", respuestas: 120 },
        { titulo: "Evaluación interna", estado: "cerrada", descripcion: "Evaluación de procesos internos", preguntas: [], fecha: "2025-07-22", respuestas: 80 },
        { titulo: "Clima laboral", estado: "activa", descripcion: "Encuesta sobre clima laboral", preguntas: [], fecha: "2025-08-05", respuestas: 200 },
        { titulo: "Mejoras 2026", estado: "borrador", descripcion: "Sugerencias para mejoras", preguntas: [], fecha: "-", respuestas: 0 }
      ]
    }
  } catch (error) {
    console.error('Error cargando encuestas:', error)
    // Fallback a datos de muestra
    table.value.rows = [
      { titulo: "Satisfacción clientes", estado: "activa", descripcion: "Encuesta sobre satisfacción", preguntas: [], fecha: "2025-08-10", respuestas: 120 },
      { titulo: "Evaluación interna", estado: "cerrada", descripcion: "Evaluación de procesos internos", preguntas: [], fecha: "2025-07-22", respuestas: 80 },
      { titulo: "Clima laboral", estado: "activa", descripcion: "Encuesta sobre clima laboral", preguntas: [], fecha: "2025-08-05", respuestas: 200 },
      { titulo: "Mejoras 2026", estado: "borrador", descripcion: "Sugerencias para mejoras", preguntas: [], fecha: "-", respuestas: 0 }
    ]
  }
}

// Funciones de lógica
function saveToLocalStorage() {
  localStorage.setItem('encuestas', JSON.stringify(table.value.rows))
}

function createSurvey() {
  showForm.value = true
}

async function saveSurvey(nuevaEncuesta) {
  try {
    console.log('Enviando encuesta:', nuevaEncuesta)
    const response = await api.post('/encuestas/', nuevaEncuesta)
    console.log('Encuesta guardada:', response.data)
    await loadSurveys() // Recargar la lista de encuestas
    showForm.value = false
  } catch (error) {
    console.error('Error guardando encuesta:', error)
    console.error('Detalles del error:', error.response?.data)
    alert('Error al guardar la encuesta. Por favor intenta de nuevo.')
  }
}

function cancelSurvey() {
  showForm.value = false
}

// Propiedad computada para el conteo de encuestas filtradas
const filteredCount = computed(() => {
  if (!selectedStatus.value) return table.value.rows.length
  return table.value.rows.filter(r => r.estado === selectedStatus.value).length
})

function openSurvey(row) {
  // Redirigir a la página de respuesta de la encuesta usando el id_encuesta
  router.push(`/encuesta/${row.id}`)
}
</script>

