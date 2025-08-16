<script setup>
import { ref } from "vue"
import BaseModule from "../components/BaseModule.vue"
import ReporteForm from "../components/ReporteForm.vue"

const breadcrumbs = [
  { label: "Inicio", to: "/dashboard" },
  { label: "Reportes" }
]

const kpis = [
  { title: "Reportes generados", value: 28, change: 12, icon: "bi bi-file-earmark-text" },
  { title: "Pendientes", value: 5, change: -8, icon: "bi bi-hourglass-split" },
  { title: "Errores", value: 1, change: -50, icon: "bi bi-exclamation-triangle" },
  { title: "Descargas", value: 120, change: 7, icon: "bi bi-download" }
]

const charts = {
  left: {
    id: "repMensuales",
    title: "Reportes por mes",
    type: "bar",
    data: {
      labels: ["Ene","Feb","Mar","Abr","May","Jun"],
      datasets: [{ label: "Reportes", data: [3,5,4,6,4,6] }]
    }
  },
  right: {
    id: "porTipo",
    title: "Distribución por tipo",
    type: "pie",
    data: {
      labels: ["PDF", "Excel", "CSV"],
      datasets: [{ data: [50, 35, 15] }]
    }
  }
}

// Estado de tabla
const table = ref({
  columns: [
    { key: "id", label: "IDENTIFICACIÓN" },
    { key: "tipo", label: "Tipo" },
    { key: "fecha", label: "Fecha" },
    { key: "estado", label: "Estado" }
  ],
  rows: [
    { id: 101, tipo: "PDF", fecha: "10/08/2025", estado: "Generado" },
    { id: 102, tipo: "Excel", fecha: "11/08/2025", estado: "Pendiente" },
    { id: 103, tipo: "CSV", fecha: "11/08/2025", estado: "Generado" }
  ]
})

// Estado modal
const showForm = ref(false)

// Guardar reporte
function saveReporte(newReporte) {
  const id = table.value.rows.length + 101
  table.value.rows.push({ id, ...newReporte, estado: "Generado" })
  alert("✅ Reporte generado con éxito")
  showForm.value = false
}

// Exportar simulación
function exportar(tipo) {
  alert(`📂 Exportando en formato ${tipo}...`)
}
</script>

<template>
  <BaseModule
    title="Reportes"
    :breadcrumbs="breadcrumbs"
    :kpis="kpis"
    :charts="charts"
    :table="table"
    @create="showForm = true"
    @export="() => exportar('Excel')"
    @rowClick="(row) => alert(`📌 Detalles del reporte ID: ${row.id}`)"
  >
  <template #table-filters>
    <div class="d-flex justify-content-end gap-2">
      <button class="btn btn-sm btn-outline-primary">
        <i class="bi bi-funnel me-1"></i> Filtros avanzados
      </button>
      <button class="btn btn-sm btn-success" @click="exportar('Excel')">
        <i class="bi bi-file-earmark-excel me-1"></i> Exportar Excel
      </button>
      <button class="btn btn-sm btn-danger" @click="exportar('PDF')">
        <i class="bi bi-file-earmark-pdf me-1"></i> Exportar PDF
      </button>
    </div>
  </template>

  </BaseModule>

  <!-- Modal de reporte -->
  <ReporteForm
    v-if="showForm"
    @close="showForm = false"
    @save="saveReporte"
  />
</template>
