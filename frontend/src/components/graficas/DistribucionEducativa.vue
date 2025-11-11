<template>
  <ChartPanel :chartId="'educativaChart'" :type="'bar'" :data="chartData" :options="chartOptions">
    <template #title>🎓 Distribución Educativa</template>
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
  labels: [],
  datasets: [{
    label: 'Número de personas',
    data: [],
    backgroundColor: [
      'rgba(220, 53, 69, 0.8)',   // Rojo para Analfabeto
      'rgba(255, 193, 7, 0.8)',   // Amarillo para Primaria
      'rgba(40, 167, 69, 0.8)',   // Verde para Secundaria
      'rgba(13, 110, 253, 0.8)'   // Azul para Superior
    ],
    borderColor: [
      'rgba(220, 53, 69, 1)',
      'rgba(255, 193, 7, 1)',
      'rgba(40, 167, 69, 1)',
      'rgba(13, 110, 253, 1)'
    ],
    borderWidth: 1,
    borderRadius: 4,
    borderSkipped: false
  }]
})

const chartOptions = ref({
  responsive: true,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          const value = context.parsed.y || 0
          return `Personas: ${value}`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        precision: 0
      }
    },
    x: {
      ticks: {
        font: {
          size: 11
        }
      }
    }
  }
})

const updateChartData = () => {
  if (props.data && props.data.length > 0) {
    chartData.value.labels = props.data.map(item => item.nivel || 'Sin especificar')
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