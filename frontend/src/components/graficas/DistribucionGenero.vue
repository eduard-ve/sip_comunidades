<template>
  <ChartPanel :chartId="'generoChart'" :type="'doughnut'" :data="chartData" :options="chartOptions">
    <template #title>👥 Distribución por Género</template>
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

const chartData = ref({
  labels: ['Masculino', 'Femenino', 'Otro'],
  datasets: [{
    data: [0, 0, 0],
    backgroundColor: [
      'rgba(13, 110, 253, 0.8)',  // Azul para masculino
      'rgba(255, 193, 7, 0.8)',   // Amarillo para femenino
      'rgba(108, 117, 125, 0.8)'  // Gris para otro
    ],
    borderWidth: 2,
    borderColor: '#ffffff'
  }]
})

const chartOptions = ref({
  responsive: true,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        padding: 20,
        usePointStyle: true
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
  },
  cutout: '60%'
})

const updateChartData = () => {
  if (props.data && props.data.length > 0) {
    const masculino = props.data.find(item => item.genero === 'Masculino')?.cantidad || 0
    const femenino = props.data.find(item => item.genero === 'Femenino')?.cantidad || 0
    const otro = props.data.find(item => item.genero === 'Otro')?.cantidad || 0

    chartData.value.datasets[0].data = [masculino, femenino, otro]
  } else {
    chartData.value.datasets[0].data = [0, 0, 0]
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