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
          <button class="btn btn-sm btn-primary" @click.stop="editarReporte(row)">
            <i class="bi bi-pencil me-1"></i> Editar
          </button>
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
    :reporte="editingReporte"
    @close="closeForm"
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
const charts = ref({
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
})

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
const editingReporte = ref(null)

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
    charts.value.right.data.datasets[0].data = [
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
    console.log('Datos del reporte a guardar:', newReporte)
<<<<<<< Updated upstream
    // Determinar si es creación o edición
    const isEditing = editingReporte.value !== null
=======
>>>>>>> Stashed changes

    // Determinar el tipo de reporte basado en el valor seleccionado
    let storeMethod
    if (newReporte.tipo_reporte === 'resumen_salud' || newReporte.tipo_reporte === 'indicadores_salud') {
<<<<<<< Updated upstream
      storeMethod = isEditing ? reportesStore.updateReporteSalud : reportesStore.createReporteSalud
    } else if (newReporte.tipo_reporte === 'reporte_social' || newReporte.tipo_reporte === 'condiciones_sociales') {
      storeMethod = isEditing ? reportesStore.updateReporteSocial : reportesStore.createReporteSocial
    } else if (newReporte.tipo_reporte === 'resultados_encuesta' || newReporte.tipo_reporte === 'analisis_encuesta') {
      storeMethod = isEditing ? reportesStore.updateReporteEncuestas : reportesStore.createReporteEncuestas
    } else {
      // Fallback: si no coincide exactamente, usar lógica anterior
      if (newReporte.tipo_reporte.includes('salud')) {
        storeMethod = isEditing ? reportesStore.updateReporteSalud : reportesStore.createReporteSalud
      } else if (newReporte.tipo_reporte.includes('social')) {
        storeMethod = isEditing ? reportesStore.updateReporteSocial : reportesStore.createReporteSocial
      } else {
        storeMethod = isEditing ? reportesStore.updateReporteEncuestas : reportesStore.createReporteEncuestas
=======
      storeMethod = reportesStore.createReporteSalud
    } else if (newReporte.tipo_reporte === 'reporte_social' || newReporte.tipo_reporte === 'condiciones_sociales') {
      storeMethod = reportesStore.createReporteSocial
    } else if (newReporte.tipo_reporte === 'resultados_encuesta' || newReporte.tipo_reporte === 'analisis_encuesta') {
      storeMethod = reportesStore.createReporteEncuestas
    } else {
      // Fallback: si no coincide exactamente, usar lógica anterior
      if (newReporte.tipo_reporte.includes('salud')) {
        storeMethod = reportesStore.createReporteSalud
      } else if (newReporte.tipo_reporte.includes('social')) {
        storeMethod = reportesStore.createReporteSocial
      } else {
        storeMethod = reportesStore.createReporteEncuestas
>>>>>>> Stashed changes
      }
    }

    console.log('Método del store a usar:', storeMethod.name)
<<<<<<< Updated upstream

    if (isEditing) {
      await storeMethod(editingReporte.value.id, newReporte)
    } else {
      await storeMethod(newReporte)

    }

    console.log('Método del store a usar:', storeMethod.name)
=======
>>>>>>> Stashed changes
    await storeMethod(newReporte)

    // Recargar datos
    await Promise.all([
      reportesStore.fetchReportesSalud(),
      reportesStore.fetchReportesSociales(),
      reportesStore.fetchReportesEncuestas()
    ])

    // Actualizar tabla
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

<<<<<<< Updated upstream

    alert(isEditing ? "Reporte actualizado con éxito" : "Reporte generado con éxito")
    closeForm()
  } catch (error) {
    console.error('Error al guardar reporte:', error)
    alert(`Error al ${editingReporte.value ? 'actualizar' : 'generar'} el reporte: ${error.response?.data?.error || error.response?.data?.detail || error.message}`)

=======
    alert("Reporte generado con éxito")
    showForm.value = false
  } catch (error) {
    console.error('Error al guardar reporte:', error)
    alert(`Error al generar el reporte: ${error.response?.data?.detail || error.message}`)
>>>>>>> Stashed changes
  }
}

// Simulación de exportación para una fila específica
function exportar(row) {
  alert(`Exportando el reporte con ID: ${row.id} en formato PDF...`)
}

// Función para editar un reporte
function editarReporte(row) {
  editingReporte.value = row
  showForm.value = true
}

// Función para cerrar el formulario
function closeForm() {
  showForm.value = false
  editingReporte.value = null
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
