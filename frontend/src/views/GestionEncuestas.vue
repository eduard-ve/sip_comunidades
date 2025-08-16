<template>
  <EncuestaBase
    title="Encuestas"
    :breadcrumbs="[
      { label: 'Inicio', to: '/' },
      { label: 'Encuestas' }
    ]"
    :kpis="kpis"
    :charts="charts"
    :table="table"
    search-placeholder="Buscar encuesta…"
    @create="createSurvey"
    @export="exportResults"
    @rowClick="openSurvey"
  >
    <!-- filtros adicionales -->
    <template #table-filters>
      <select v-model="selectedStatus" class="form-select form-select-sm" style="max-width: 180px;">
        <option value="">Todos los estados</option>
        <option value="activa">Activa</option>
        <option value="cerrada">Cerrada</option>
        <option value="borrador">Borrador</option>
      </select>
    </template>

    <!-- pie de tabla -->
    <template #table-footer>
      <div class="d-flex justify-content-end text-muted small mt-2">
        Total: {{ filteredCount }} encuestas
      </div>
    </template>
  </EncuestaBase>
</template>

<script setup>
import { ref, computed } from "vue"
import EncuestaBase from "../components/EncuestaBase.vue"

const kpis = ref([
  { title: "Encuestas activas", value: 5, change: "+2", icon: "bi-clipboard-check", colorIcon: "#198754" },
  { title: "Respuestas totales", value: 1240, change: "+120", icon: "bi-people", colorIcon: "#0d6efd" },
  { title: "Tasa de respuesta", value: "68%", change: "-3%", icon: "bi-bar-chart-line", colorIcon: "#ffc107" },
  { title: "Promedio satisfacción", value: "4.2/5", change: "+0.3", icon: "bi-star", colorIcon: "#fd7e14" }
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
    { key: "fecha", label: "Fecha" },
    { key: "respuestas", label: "Respuestas" }
  ],
  rows: [
    { titulo: "Satisfacción clientes", estado: "activa", fecha: "2025-08-10", respuestas: 120 },
    { titulo: "Evaluación interna", estado: "cerrada", fecha: "2025-07-22", respuestas: 80 },
    { titulo: "Clima laboral", estado: "activa", fecha: "2025-08-05", respuestas: 200 },
    { titulo: "Mejoras 2026", estado: "borrador", fecha: "-", respuestas: 0 }
  ]
})

const selectedStatus = ref("")

// filtrar según estado
const filteredCount = computed(() => {
  if (!selectedStatus.value) return table.value.rows.length
  return table.value.rows.filter(r => r.estado === selectedStatus.value).length
})

function createSurvey() {
  alert("Crear nueva encuesta")
}

function exportResults() {
  alert("Exportar resultados")
}

function openSurvey(row) {
  alert("Abrir encuesta: " + row.titulo)
}
</script>



