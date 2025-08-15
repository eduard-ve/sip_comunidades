<template>
  <BaseModule
    title="Gestión Social"
    :breadcrumbs="[
      { label: 'Inicio', to: '/' },
      { label: 'Gestión Social' }
    ]"
    :kpis="kpis"
    :charts="charts"
    :table="table"
    search-placeholder="Buscar programas o beneficiarios…"
    @create="onCreate"
    @export="onExport"
    @rowClick="onRowClick"
  >
    <!-- Extra contenido encima de charts -->
    <template #extra>
      <div class="mb-3">
        <h5>Actividades culturales/comunitarias recientes</h5>
        <ul>
          <li v-for="(act, idx) in actividades" :key="idx">{{ act }}</li>
        </ul>
      </div>
    </template>

    <!-- Mapas de cobertura de programas -->
    <template #left>
      <MapPanel :programas="mapProgramas" />
    </template>

    <!-- ChartPanel de estadísticas de impacto social -->
    <template #right>
      <ChartPanel
        chart-id="impactoSocialChart"
        type="bar"
        :data="impactoData"
        :options="{ responsive: true }"
      >
        <template #title>Estadísticas de impacto social</template>
      </ChartPanel>
    </template>

    <!-- Tabla de beneficiarios por programa -->
    <template #table-footer>
      <div class="mt-3">
        <h6>Beneficiarios por programa</h6>
      </div>
    </template>
  </BaseModule>
</template>

<script setup>
import { ref } from 'vue'
import BaseModule from '../components/BaseModule.vue'
import MapPanel from '../components/MapPanel.vue'
import ChartPanel from '../components/ChartPanel.vue'

// KPIs
const kpis = ref([
  { title: 'Programas activos', value: 12, change: '+2', icon: 'bi-people' },
  { title: 'Beneficiarios totales', value: 340, change: '+15', icon: 'bi-person-check' },
  { title: 'Actividades culturales', value: 8, change: '+1', icon: 'bi-music-note-beamed' },
  { title: 'Cobertura territorial', value: '5 regiones', change: '+1', icon: 'bi-geo-alt' }
])

// Lista de actividades
const actividades = ref([
  'Festival comunitario en Barrio Norte',
  'Taller de arte para niños',
  'Campaña de salud preventiva',
  'Charla sobre medio ambiente'
])

// Datos para ChartPanel
const impactoData = ref({
  labels: ['Programa A', 'Programa B', 'Programa C'],
  datasets: [
    { label: 'Beneficiarios', data: [120, 95, 125], backgroundColor: '#0d6efd' }
  ]
})

// Tabla de beneficiarios por programa
const table = ref({
  columns: [
    { key: 'programa', label: 'Programa' },
    { key: 'beneficiarios', label: 'Beneficiarios' },
    { key: 'region', label: 'Región' }
  ],
  rows: [
    { programa: 'Programa A', beneficiarios: 120, region: 'Norte' },
    { programa: 'Programa B', beneficiarios: 95, region: 'Sur' },
    { programa: 'Programa C', beneficiarios: 125, region: 'Centro' }
  ]
})

// Mapas de cobertura
const mapProgramas = ref([
  { nombre: 'Programa A', coordenadas: [-12.0464, -77.0428] },
  { nombre: 'Programa B', coordenadas: [-16.4090, -71.5375] },
  { nombre: 'Programa C', coordenadas: [-12.0464, -77.0428] }
])

// Eventos
function onCreate() {
  console.log('Crear nuevo programa')
}

function onExport() {
  console.log('Exportar datos')
}

function onRowClick(row) {
  console.log('Fila clickeada', row)
}
</script>
