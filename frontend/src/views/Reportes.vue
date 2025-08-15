<script setup>
import BaseModule from '../components/BaseModule.vue'

const breadcrumbs = [
  { label: 'Inicio', to: '/dashboard' },
  { label: 'Reportes' }
]

const kpis = [
  { title: 'Reportes generados', value: 28, change: 12, icon: 'bi bi-file-earmark-text' },
  { title: 'Pendientes', value: 5, change: -8, icon: 'bi bi-hourglass-split' },
  { title: 'Errores', value: 1, change: -50, icon: 'bi bi-exclamation-triangle' },
  { title: 'Descargas', value: 120, change: 7, icon: 'bi bi-download' }
]

const charts = {
  left: {
    id: 'repMensuales',
    title: 'Reportes por mes',
    type: 'bar',
    data: {
      labels: ['Ene','Feb','Mar','Abr','May','Jun'],
      datasets: [{ label: 'Reportes', data: [3,5,4,6,4,6] }]
    }
  },
  right: {
    id: 'porTipo',
    title: 'Distribución por tipo',
    type: 'pie',
    data: {
      labels: ['PDF', 'Excel', 'CSV'],
      datasets: [{ data: [50, 35, 15] }]
    }
  }
}

const table = {
  columns: [
    { key: 'id', label: 'ID' },
    { key: 'tipo', label: 'Tipo' },
    { key: 'fecha', label: 'Fecha' },
    { key: 'estado', label: 'Estado' }
  ],
  rows: [
    { id: 101, tipo: 'PDF', fecha: '2025-08-10', estado: 'Generado' },
    { id: 102, tipo: 'Excel', fecha: '2025-08-11', estado: 'Pendiente' },
    { id: 103, tipo: 'CSV', fecha: '2025-08-11', estado: 'Generado' }
  ]
}
</script>

<template>
  <BaseModule
    title="Reportes"
    :breadcrumbs="breadcrumbs"
    :kpis="kpis"
    :charts="charts"
    :table="table"
    @create="() => alert('Crear reporte')"
    @export="() => alert('Exportar lista')"
    @rowClick="(row) => alert(`Fila: ${row.id}`)"
  >
    <!-- Contenido adicional opcional -->
    <template #table-filters>
      <button class="btn btn-sm btn-outline-primary">
        <i class="bi bi-funnel me-1"></i> Filtros avanzados
      </button>
    </template>
  </BaseModule>
</template>
