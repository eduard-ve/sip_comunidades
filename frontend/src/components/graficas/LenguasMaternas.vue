<template>
  <ChartPanel :chartId="'lenguasChart'" :type="'pie'" :data="chartData" :options="chartOptions">
    <template #title>🌍 Lenguas Maternas</template>
  </ChartPanel>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import ChartPanel from './ChartPanel.vue'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
})

const colores = [
  'rgba(255, 99, 132, 0.8)',
  'rgba(54, 162, 235, 0.8)',
  'rgba(255, 205, 86, 0.8)',
  'rgba(75, 192, 192, 0.8)',
  'rgba(153, 102, 255, 0.8)',
  'rgba(255, 159, 64, 0.8)',
  'rgba(201, 203, 207, 0.8)',
  'rgba(255, 99, 132, 0.8)',
  'rgba(54, 162, 235, 0.8)',
  'rgba(255, 205, 86, 0.8)'
]

const chartData = ref({
  labels: [],
  datasets: [{
    data: [],
    backgroundColor: colores,
    borderColor: colores.map(color => color.replace('0.8', '1')),
    borderWidth: 2
  }]
})

const chartOptions = ref({
  responsive: true,
  plugins: {
    legend: {
      position: 'right',
      labels: {
        padding: 20,
        usePointStyle: true,
        font: {
          size: 11
        }
      }
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          const label = context.label || ''
          const value = context.parsed || 0
          const total = context.dataset.data.reduce((a, b) => a + b, 0)
          const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0
          return `${label}: ${value} (${percentage}%)`
        }
      }
    }
  }
})

const updateChartData = () => {
  if (props.data && props.data.length > 0) {
    chartData.value.labels = props.data.map(item => item.lengua || 'Sin especificar')
    chartData.value.datasets[0].data = props.data.map(item => item.cantidad || 0)
  } else {
    chartData.value.labels = []
    chartData.value.datasets[0].data = []
  }
}

onMounted(() => {
  updateChartData()
})

watch(() => props.data, () => {
  updateChartData()
}, { deep: true })
</script>

<style scoped>
/* Estilos específicos para esta gráfica si son necesarios */
</style>