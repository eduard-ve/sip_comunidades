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
      <div class="table-filters">
        <button class="btn btn-sm btn-outline-primary">
          <i class="bi bi-funnel me-1"></i> Filtros avanzados
        </button>
      </div>
    </template>

    <!-- Slot para las celdas de la tabla -->
    <template #table-cell="{ column, row }">
      <template v-if="column.key === 'acciones'">
        <div class="table-actions">
          <button class="btn btn-sm btn-success" @click.stop="exportar(row)">
            <i class="bi bi-file-earmark-excel me-1"></i> PDF
          </button>
          <button class="btn btn-sm btn-danger" @click.stop="eliminarReporte(row)">
            <i class="bi bi-trash me-1"></i> Eliminar
          </button>
        </div>
      </template>
      <template v-else-if="column.key === 'estado'">
        <span :class="`estado-badge estado-${row.estado.toLowerCase()}`">
          {{ row.estado }}
        </span>
      </template>
      <template v-else-if="column.key === 'tipo'">
        <span :class="`tipo-badge tipo-${row.tipo.toLowerCase()}`">
          {{ row.tipo }}
        </span>
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
import { ref, onMounted } from "vue"
import { useReportesStore } from "../../stores/reportes.js"
import BaseModule from "../../components/comun/BaseModule.vue"
import ReporteForm from "../../components/formularios/ReporteForm.vue"
import '../../assets/css/Reportes.css'

const reportesStore = useReportesStore()

// Estado reactivo para los KPIs
const kpis = ref([
  { title: "Reportes de salud", value: 0, change: 0, icon: "bi bi-heart-pulse" },
  { title: "Reportes sociales", value: 0, change: 0, icon: "bi bi-people" },
  { title: "Reportes de encuestas", value: 0, change: 0, icon: "bi bi-clipboard-check" },
  { title: "Total reportes", value: 0, change: 0, icon: "bi bi-file-earmark-text" }
])

// Datos de ejemplo para los gráficos (pueden actualizarse con datos reales)
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
      labels: ["Salud", "Social", "Encuestas"],
      datasets: [{ data: [0, 0, 0] }]
    }
  }
}

// Estado de la tabla
const table = ref({
  columns: [
    { key: "id", label: "ID" },
    { key: "tipo_reporte", label: "Tipo" },
    { key: "fecha_reporte", label: "Fecha" },
    { key: "generado_por", label: "Generado por" },
    { key: "acciones", label: "Acciones" }
  ],
  rows: []
})

// Estado modal
const showForm = ref(false)

// Cargar datos del backend
onMounted(async () => {
  try {
    await Promise.all([
      reportesStore.fetchReportesSalud(),
      reportesStore.fetchReportesSociales(),
      reportesStore.fetchReportesEncuestas()
    ])

    // Actualizar KPIs con datos reales
    kpis.value[0].value = reportesStore.reportesSaludCount
    kpis.value[1].value = reportesStore.reportesSocialesCount
    kpis.value[2].value = reportesStore.reportesEncuestasCount
    kpis.value[3].value = reportesStore.totalReportes

    // Actualizar tabla con todos los reportes
    const allReportes = [
      ...reportesStore.reportesSalud.map(r => ({ ...r, categoria: 'Salud' })),
      ...reportesStore.reportesSociales.map(r => ({ ...r, categoria: 'Social' })),
      ...reportesStore.reportesEncuestas.map(r => ({ ...r, categoria: 'Encuestas' }))
    ]

    table.value.rows = allReportes.map(reporte => ({
      id: reporte.id,
      tipo_reporte: reporte.tipo_reporte,
      fecha_reporte: new Date(reporte.fecha_reporte).toLocaleDateString(),
      generado_por: reporte.generado_por,
      categoria: reporte.categoria
    }))

    // Actualizar gráfico de distribución
    charts.right.data.datasets[0].data = [
      reportesStore.reportesSaludCount,
      reportesStore.reportesSocialesCount,
      reportesStore.reportesEncuestasCount
    ]

  } catch (error) {
    console.error('Error al cargar reportes:', error)
  }
})

// Guardar reporte
async function saveReporte(newReporte) {
  try {
    // Determinar el tipo de reporte basado en los datos
    if (newReporte.tipo_reporte.includes('salud')) {
      await reportesStore.createReporteSalud(newReporte)
    } else if (newReporte.tipo_reporte.includes('social')) {
      await reportesStore.createReporteSocial(newReporte)
    } else {
      await reportesStore.createReporteEncuestas(newReporte)
    }

    // Recargar datos
    await Promise.all([
      reportesStore.fetchReportesSalud(),
      reportesStore.fetchReportesSociales(),
      reportesStore.fetchReportesEncuestas()
    ])

    alert("Reporte generado con éxito")
    showForm.value = false
  } catch (error) {
    console.error('Error al guardar reporte:', error)
    alert("Error al generar el reporte")
  }
}

// Simulación de exportación para una fila específica
function exportar(row) {
  alert(`Exportando el reporte con ID: ${row.id} en formato PDF...`)
}

// Función para eliminar un reporte
async function eliminarReporte(row) {
  if (confirm(`¿Estás seguro de que quieres eliminar el reporte ${row.id}?`)) {
    try {
      // Determinar el tipo de reporte para eliminar del store correcto
      if (row.categoria === 'Salud') {
        await reportesStore.deleteReporteSalud(row.id)
      } else if (row.categoria === 'Social') {
        await reportesStore.deleteReporteSocial(row.id)
      } else {
        await reportesStore.deleteReporteEncuestas(row.id)
      }

      // Actualizar tabla
      table.value.rows = table.value.rows.filter(r => r.id !== row.id)
      alert(`Reporte ${row.id} eliminado.`)
    } catch (error) {
      console.error('Error al eliminar reporte:', error)
      alert("Error al eliminar el reporte")
    }
  }
}
</script>
