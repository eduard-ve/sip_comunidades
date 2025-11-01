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

  <!-- Modal para mostrar el enlace único (sin cambios) -->
  <div v-if="showLink" class="modal-backdrop">
    <div class="modal-card modal-link">
      <h5>Encuesta creada</h5>
      <div class="mb-2">Comparte este enlace con los usuarios:</div>
      <div class="mb-3">
        <input :value="enlaceEncuesta" class="form-control" readonly />
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
  try {
    const response = await fetch('/api/encuestas/', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })

    if (response.ok) {
      const encuestas = await response.json()
      table.value.rows = encuestas.map(encuesta => ({
        id: encuesta.id_encuesta,
        titulo: encuesta.titulo,
        estado: encuesta.estado,
        descripcion: encuesta.descripcion,
        token: encuesta.token,
        fecha: new Date(encuesta.fecha_creacion).toISOString().slice(0, 10),
        respuestas: 0 // TODO: Calcular desde respuestas
      }))
      saveToLocalStorage()
    } else {
      // Fallback a localStorage si falla la API
      const saved = localStorage.getItem('encuestas')
      if (saved) {
        table.value.rows = JSON.parse(saved)
      }
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
})

// Funciones de lógica
function saveToLocalStorage() {
  localStorage.setItem('encuestas', JSON.stringify(table.value.rows))
}

function createSurvey() {
  showForm.value = true
}

async function saveSurvey(nuevaEncuesta) {
  try {
    // Validar datos básicos
    if (!nuevaEncuesta.titulo?.trim()) {
      alert('El título de la encuesta es obligatorio')
      return
    }

    if (!nuevaEncuesta.preguntas?.length) {
      alert('La encuesta debe tener al menos una pregunta')
      return
    }

    // Preparar datos para enviar al backend
    const surveyData = {
      titulo: nuevaEncuesta.titulo.trim(),
      descripcion: nuevaEncuesta.descripcion?.trim() || '',
      estado: nuevaEncuesta.estado,
      preguntas: nuevaEncuesta.preguntas.map((pregunta, index) => ({
        texto_pregunta: pregunta.texto?.trim(),
        tipo: pregunta.tipo === 'texto' ? 'abierta' : pregunta.tipo === 'opcion' ? 'opcion_multiple' : pregunta.tipo,
        orden: index + 1,
        opciones: pregunta.tipo === 'opcion' ? [] : [] // Por ahora vacío, se puede expandir
      }))
    }

    // Enviar al backend
    const response = await fetch('/api/encuestas/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}` // Asumiendo que hay token
      },
      body: JSON.stringify(surveyData)
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Error al guardar la encuesta')
    }

    const savedSurvey = await response.json()

    // Agregar a la tabla local con el token
    nuevaEncuesta.id = savedSurvey.id_encuesta
    nuevaEncuesta.token = savedSurvey.token
    table.value.rows.push(nuevaEncuesta)
    saveToLocalStorage()

    // Guardar el ID de la encuesta recién creada
    lastSavedSurveyId.value = savedSurvey.id_encuesta

    // Ocultar el formulario y mostrar el modal de opciones
    showForm.value = false
    showOptions.value = true
  } catch (error) {
    console.error('Error guardando encuesta:', error)
    alert(`Error al guardar la encuesta: ${error.message}`)
  }
}

function cancelSurvey() {
  showForm.value = false
}

// Función para generar y mostrar el enlace
function generateLink() {
  showOptions.value = false // Oculta el modal de opciones
  // Usar el token de la encuesta guardada en lugar del ID
  const survey = table.value.rows.find(s => s.id === lastSavedSurveyId.value)
  if (survey && survey.token) {
    enlaceEncuesta.value = `${window.location.origin}/encuesta/${survey.token}`
  } else {
    enlaceEncuesta.value = `${window.location.origin}/encuesta/${lastSavedSurveyId.value}`
  }
  showLink.value = true // Muestra el modal del enlace
}

// Función para generar PDF
async function generatePdf() {
  showOptions.value = false // Oculta el modal de opciones

  try {
    // Obtener los datos completos de la encuesta desde el backend
    const response = await fetch(`/api/encuestas/${lastSavedSurveyId.value}/`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
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
