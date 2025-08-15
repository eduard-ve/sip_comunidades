<template>
  <BaseModule
    title="Gestión de Salud"
    :breadcrumbs="breadcrumbs"
    :kpis="kpis"
    :charts="charts"
    :table="table"
  />
</template>

<script setup>
import BaseModule from '../components/BaseModule.vue'

const breadcrumbs = [
  { label: 'Inicio', to: '/dashboard' },
  { label: 'Gestión de Salud' }
]

const kpis = [
  { title: 'Pacientes activos', value: 240, change: 8, icon: 'bi bi-heart' },
  { title: 'Consultas', value: 1200, change: 15, icon: 'bi bi-clipboard-pulse' }
]

const charts = {
  left: {
    title: 'Consultas por mes',
    type: 'bar',
    data: { labels: ['Ene', 'Feb'], datasets: [{ label: 'Consultas', data: [120, 140] }] }
  },
  right: {
    title: 'Tipos de consultas',
    type: 'pie',
    data: { labels: ['General', 'Especialidad'], datasets: [{ data: [70, 30] }] }
  }
}

const table = {
  columns: [
    { key: 'paciente', label: 'Paciente' },
    { key: 'fecha', label: 'Fecha' },
    { key: 'tipo', label: 'Tipo de consulta' }
  ],
  rows: [
    { paciente: 'Juan Pérez', fecha: '2025-08-01', tipo: 'General' },
    { paciente: 'María López', fecha: '2025-08-02', tipo: 'Especialidad' }
  ]
}
</script>



