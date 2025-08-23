<template>
  <BaseModule
    title="Reportes"
    :kpis="kpis"
    :charts="charts"
    :table="table"
    :show-create="true"
    :show-export="false"
    @create="showForm = true"
    @rowClick="(row) => alert(` Detalles del reporte ID: ${row.id}`)"
  >
    <template #table-filters>
      <div class="d-flex justify-content-end gap-2">
        <button class="btn btn-sm btn-outline-primary">
          <i class="bi bi-funnel me-1"></i> Filtros avanzados
        </button>
      </div>
    </template>

    <!-- Slot para las celdas de la tabla -->
    <template #table-cell="{ column, row }">
      <template v-if="column.key === 'acciones'">
        <div class="d-flex gap-2">
          <button class="btn btn-sm btn-success" @click.stop="exportar(row)">
            <i class="bi bi-file-earmark-excel me-1"></i> PDF
          </button>
          <button class="btn btn-sm btn-danger" @click.stop="eliminarReporte(row)">
            <i class="bi bi-trash me-1"></i> Eliminar
          </button>
        </div>
      </template>
      <template v-else>
        {{ row[column.key] }}
      </template>
    </template>
  </BaseModule>

  <!-- Modal de reporte -->
  <ReporteForm
    v-if="showForm"
    @close="showForm = false"
    @save="saveReporte"
  />
</template>

<script setup>
import { ref } from "vue"
import BaseModule from "../components/BaseModule.vue"
import ReporteForm from "../components/ReporteForm.vue"

// Datos de ejemplo para los KPIs
const kpis = [
  { title: "Reportes generados", value: 28, change: 12, icon: "bi bi-file-earmark-text" },
  { title: "Pendientes", value: 5, change: -8, icon: "bi bi-hourglass-split" },
  { title: "Errores", value: 1, change: -50, icon: "bi bi-exclamation-triangle" },
  { title: "Descargas", value: 120, change: 7, icon: "bi bi-download" }
]

// Datos de ejemplo para los gráficos
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

// Estado de la tabla
const table = ref({
  columns: [
    { key: "id", label: "IDENTIFICACIÓN" },
    { key: "tipo", label: "Tipo" },
    { key: "fecha", label: "Fecha" },
    { key: "estado", label: "Estado" },
    { key: "acciones", label: "Acciones" } 
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
  alert("Reporte generado con éxito")
  showForm.value = false
}

// Simulación de exportación para una fila específica
function exportar(row) {
  alert(`Exportando el reporte con ID: ${row.id} en formato PDF...`)
}

// Función para eliminar un reporte
function eliminarReporte(row) {
  if (confirm(`¿Estás seguro de que quieres eliminar el reporte ${row.id}?`)) {
    table.value.rows = table.value.rows.filter(r => r.id !== row.id)
    alert(`Reporte ${row.id} eliminado.`)
  }
}
</script>
