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
      <select v-model="selectedStatus" class="form-select form-select-sm" style="max-width: 180px;">
        <option value="">Todos los estados</option>
        <option value="activa">Activa</option>
        <option value="cerrada">Cerrada</option>
        <option value="borrador">Borrador</option>
      </select>
    </template>
    <template #table-footer>
      <div class="d-flex justify-content-end text-muted small mt-2">
        Total: {{ filteredCount }} encuestas
      </div>
    </template>
  </EncuestaBase>

  <!-- Modal para el formulario de la encuesta -->
  <div v-if="showForm" class="modal-backdrop" style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:1050;background:rgba(0,0,0,0.3);display:flex;align-items:center;justify-content:center;">
    <div class="bg-white p-4 rounded shadow" style="min-width:320px;">
      <EncuestaForm @save="saveSurvey" @cancel="cancelSurvey" />
    </div>
  </div>

  <!-- NUEVO: Modal para elegir entre Enlace y PDF -->
  <div v-if="showOptions" class="modal-backdrop" style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:1050;background:rgba(0,0,0,0.3);display:flex;align-items:center;justify-content:center;">
    <div class="bg-white p-4 rounded shadow" style="min-width:320px;">
      <h5>Encuesta guardada</h5>
      <div class="mb-3">¿Qué acción deseas realizar?</div>
      <div class="d-flex justify-content-between">
        <button class="btn btn-primary" @click="generateLink">Generar Enlace</button>
        <button class="btn btn-secondary" @click="generatePdf">Generar PDF</button>
      </div>
    </div>
  </div>

  <!-- Modal para mostrar el enlace único (sin cambios) -->
  <div v-if="showLink" class="modal-backdrop" style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:1050;background:rgba(0,0,0,0.3);display:flex;align-items:center;justify-content:center;">
    <div class="bg-white p-4 rounded shadow" style="min-width:320px;">
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
import EncuestaBase from "../components/EncuestaBase.vue"
import EncuestaForm from "../components/EncuestaForm.vue"

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

// Ciclo de vida: Cargar datos desde localStorage al montar el componente
onMounted(() => {
  const saved = localStorage.getItem('encuestas')
  if (saved) {
    table.value.rows = JSON.parse(saved)
  } else {
    // Datos de muestra si no hay nada en localStorage
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
  enlaceEncuesta.value = `${window.location.origin}/encuesta/${lastSavedSurveyId.value}`
  showLink.value = true // Muestra el modal del enlace
}

// Función para simular la generación de PDF
function generatePdf() {
  showOptions.value = false // Oculta el modal de opciones
  alert("Procesando la generación del PDF. Esta función requiere una librería externa.")
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
