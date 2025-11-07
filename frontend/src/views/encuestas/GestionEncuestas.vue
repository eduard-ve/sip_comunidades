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
  <div v-if="showForm" class="modal-backdrop">
    <div class="modal-card">
      <EncuestaForm @save="saveSurvey" @cancel="cancelSurvey" />
    </div>
  </div>

  <!-- NUEVO: Modal para elegir entre Enlace y PDF -->
  <div v-if="showOptions" class="modal-backdrop">
    <div class="modal-card modal-options">
      <h5>Encuesta guardada</h5>
      <div class="mb-3">¿Qué acción deseas realizar?</div>
      <div class="d-flex">
        <button class="btn btn-primary" @click="generateLink">Generar Enlace</button>
        <button class="btn btn-secondary" @click="generatePdf">Generar PDF</button>
      </div>
    </div>
  </div>

  <!-- Modal para mostrar el enlace único con botón copiar -->
  <div v-if="showLink" class="modal-backdrop">
    <div class="modal-card modal-link">
      <h5>Encuesta creada</h5>
      <div class="mb-2">Comparte este enlace con los usuarios:</div>
      <div class="mb-3">
        <div class="input-group">
          <input :value="enlaceEncuesta" class="form-control" readonly id="survey-link" />
          <button class="btn btn-outline-primary" @click="copyToClipboard" id="copy-btn">
            <i class="bi bi-clipboard"></i> Copiar
          </button>
        </div>
      </div>
      <div v-if="copySuccess" class="alert alert-success py-2 mb-3">
        <i class="bi bi-check-circle"></i> ¡Enlace copiado al portapapeles!
      </div>
      <button class="btn btn-primary btn-sm" @click="showLink = false">Cerrar</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import EncuestaBase from "./components/EncuestaBase.vue"
import EncuestaForm from "../../components/formularios/EncuestaForm.vue"
import '../../assets/css/GestionEncuestas.css'

// Variables de estado
const showForm = ref(false)
const showLink = ref(false)
const showOptions = ref(false) // NUEVO: Estado para el modal de opciones
const enlaceEncuesta = ref("")
const lastSavedSurveyId = ref(null) // NUEVO: Para guardar el ID de la última encuesta guardada
const copySuccess = ref(false) // Para mostrar notificación de copiado

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

    const response = await fetch('/api/encuestas/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      const encuestas = await response.json()
      console.log('Encuestas cargadas desde backend:', encuestas.length)
      table.value.rows = encuestas.map(encuesta => ({
        id: encuesta.id_encuesta,
        titulo: encuesta.titulo,
        estado: encuesta.estado,
        descripcion: encuesta.descripcion,
        token: encuesta.token,
        fecha: new Date(encuesta.fecha_creacion).toISOString().slice(0, 10),
        respuestas: 0 // TODO: Calcular desde respuestas
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

function saveSurvey(nuevaEncuesta) {
  // Generar un ID único simple
  const id = Date.now().toString()
  nuevaEncuesta.id = id
  table.value.rows.push(nuevaEncuesta)
  saveToLocalStorage()

  // Guardar el ID de la encuesta recién creada
  lastSavedSurveyId.value = id

  // Ocultar el formulario y mostrar el modal de opciones
  showForm.value = false
  showOptions.value = true
}

function cancelSurvey() {
  showForm.value = false
}

// Función para generar y mostrar el enlace
function generateLink() {
  showOptions.value = false // Oculta el modal de opciones
  // Usar el ID de la encuesta guardada
  enlaceEncuesta.value = `${window.location.origin}/encuesta/${lastSavedSurveyId.value}`
  copySuccess.value = false // Reset copy success state
  showLink.value = true // Muestra el modal del enlace
}

// Función para copiar enlace al portapapeles
async function copyToClipboard() {
  try {
    await navigator.clipboard.writeText(enlaceEncuesta.value)
    copySuccess.value = true
    // Ocultar notificación después de 3 segundos
    setTimeout(() => {
      copySuccess.value = false
    }, 3000)
  } catch (err) {
    console.error('Error copiando al portapapeles:', err)
    // Fallback para navegadores que no soportan clipboard API
    const textArea = document.createElement('textarea')
    textArea.value = enlaceEncuesta.value
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    copySuccess.value = true
    setTimeout(() => {
      copySuccess.value = false
    }, 3000)
  }
}

// Función para generar PDF
async function generatePdf() {
  showOptions.value = false // Oculta el modal de opciones

  try {
    // Obtener los datos completos de la encuesta desde el backend
    const response = await fetch(`/api/encuestas/${lastSavedSurveyId.value}/`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      }
    })

    if (!response.ok) {
      throw new Error('Error al obtener datos de la encuesta')
    }

    const surveyData = await response.json()

    // Aquí se podría integrar una librería como jsPDF o html2pdf
    // Por ahora, mostrar los datos en consola y alert
    console.log('Datos de la encuesta para PDF:', surveyData)
    alert(`PDF generado para la encuesta: ${surveyData.titulo}\n\nDatos preparados para exportación.`)

  } catch (error) {
    console.error('Error generando PDF:', error)
    alert('Error al generar el PDF. Por favor intenta de nuevo.')
  }
}

// Propiedad computada para el conteo de encuestas filtradas
const filteredCount = computed(() => {
  if (!selectedStatus.value) return table.value.rows.length
  return table.value.rows.filter(r => r.estado === selectedStatus.value).length
})

function openSurvey(row) {
  alert("Abrir encuesta: " + row.titulo)
}
</script>
