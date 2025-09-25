<template>
  <div class="container-fluid py-4">
    <!-- ======= Encabezado ======= -->
    <div class="d-flex flex-wrap justify-content-between align-items-center mb-4">
      <div>
        <h2 class="fw-bold mb-0">📊 bienvenidos, aca podras visualizar y conocer todo sobre nuestro objetivo</h2>
        <div class="text-muted small">
          Comunidad: <span class="fw-semibold">{{ currentCommunity }}</span> |
          Año: <span class="fw-semibold">{{ currentYear }}</span>
        </div>
      </div>
      <div class="d-flex gap-2">
        <select v-model="currentCommunity" class="form-select w-auto">
          <option v-for="c in communities" :key="c">{{ c }}</option>
        </select>
        <select v-model="currentYear" class="form-select w-auto">
          <option v-for="y in years" :key="y">{{ y }}</option>
        </select>
      </div>
    </div>

    <!-- ======= KPIs ======= -->
    <div class="row g-3 mb-4">
      <div class="col-12 col-sm-6 col-lg-2" v-for="card in cards" :key="card.title">
        <KpiCard
          :title="card.title"
          :value="card.value"
          :change="card.change"
          :icon="card.icon"
          :color-icon="card.color"
        />
      </div>
    </div>

    <!-- ======= Gráficos principales ======= -->
    <div class="row g-3 mb-4">
      <div class="col-md-6">
        <ChartPanel chart-id="barLineChart" type="bar" :data="barLineChartData">
          <template #title>📈 Evolución de Registros</template>
        </ChartPanel>
      </div>
      <div class="col-md-6">
        <ChartPanel chart-id="pieChart" type="pie" :data="pieChartData">
          <template #title>👥 Distribución por Género</template>
        </ChartPanel>
      </div>
    </div>

    <!-- ======= Mapas y pirámide ======= -->
    <div class="row g-3 mb-4">
      <div class="col-md-6">
        <PopulationPyramid />
      </div>
      <div class="col-md-6">
        <ServicesMap />
      </div>
    </div>

    <!-- ======= Indicadores sectoriales ======= -->
    <div class="row g-3 mb-4">
      <div class="col-md-6">
        <HealthIndicators />
      </div>
      <div class="col-md-6">
        <EducationStats />
      </div>
    </div>

    <!-- ======= Alertas y noticias ======= -->
    <div class="row g-3 mb-4">
      <div class="col-md-8">
        <div class="card shadow-sm p-3 h-100">
          <h6 class="fw-bold mb-3">📰 Noticias y Comunicados</h6>
          <ul class="list-group list-group-flush">
            <li class="list-group-item" v-for="n in noticias" :key="n.id">
              <strong>{{ n.titulo }}</strong> - <small>{{ n.fecha }}</small>
              <p class="mb-0">{{ n.descripcion }}</p>
            </li>
          </ul>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card shadow-sm p-3 h-100 bg-light">
          <h6 class="fw-bold mb-3">⚠️ Alertas</h6>
          <ul>
            <li v-for="a in alertas" :key="a.id">{{ a.mensaje }}</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- ======= Descarga de reportes ======= -->
    <div class="text-center mt-4">
      <button class="btn btn-primary me-2">📄 Descargar PDF</button>
      <button class="btn btn-outline-secondary">📊 Exportar CSV</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import KpiCard from '../components/KpiCard.vue'
import ChartPanel from '../components/ChartPanel.vue'
import PopulationPyramid from '../components/PopulationPyramid.vue'
import ServicesMap from '../components/ServicesMap.vue'
import HealthIndicators from '../components/HealthIndicators.vue'
import EducationStats from '../components/EducationStats.vue'

const currentCommunity = ref('Comunidad A')
const currentYear = ref(2025)
const communities = ['Comunidad A', 'Comunidad B', 'Comunidad C']
const years = [2023, 2024, 2025]

const cards = [
  { title: 'Población', value: 560, change: 2, icon: 'bi bi-people-fill', color: '#0d6efd' },
  { title: 'Salud', value: '85%', change: 1.5, icon: 'bi bi-heart-pulse', color: '#dc3545' },
  { title: 'Educación', value: '78%', change: 3, icon: 'bi bi-book', color: '#ffc107' },
  { title: 'Empleo', value: '62%', change: -1, icon: 'bi bi-briefcase', color: '#198754' },
  { title: 'Proyectos', value: 12, change: 4, icon: 'bi bi-diagram-3', color: '#6f42c1' }
]

// Datos para gráfico de barras + línea
const barLineChartData = {
  labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
  datasets: [
    {
      type: 'bar',
      label: 'Registros',
      data: [12, 19, 3, 5, 2, 3],
      backgroundColor: 'rgba(13, 110, 253, 0.8)',
      borderRadius: 6
    },
    {
      type: 'line',
      label: 'Tendencia',
      data: [10, 15, 4, 6, 3, 4],
      borderColor: '#ffc107',
      borderWidth: 2,
      tension: 0.3,
      fill: false
    }
  ]
}

// Datos para gráfico de pastel
const pieChartData = {
  labels: ['Hombres', 'Mujeres'],
  datasets: [
    {
      data: [300, 500],
      backgroundColor: ['rgba(13, 110, 253, 0.9)', 'rgba(255, 193, 7, 0.9)'],
      borderWidth: 1
    }
  ]
}

// Noticias y alertas simuladas
const noticias = [
  { id: 1, titulo: 'Nueva jornada de vacunación', fecha: '2025-08-12', descripcion: 'Se realizará en el centro de salud comunitario.' },
  { id: 2, titulo: 'Taller de capacitación agrícola', fecha: '2025-08-20', descripcion: 'Dirigido a productores locales.' }
]

const alertas = [
  { id: 1, mensaje: 'Alerta sanitaria por brote de dengue.' },
  { id: 2, mensaje: 'Interrupción temporal de agua potable.' }
]
</script>

<style scoped>
.container-fluid {
  max-width: 1400px;
}
</style>
