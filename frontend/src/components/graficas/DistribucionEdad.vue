<template>
  <ChartPanel :chartId="'edadChart'" :type="'bar'" :data="chartData" :options="chartOptions">
    <template #title>📊 Distribución por Edad</template>
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
    backgroundColor: [],
    borderColor: [],
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
          const total = context.dataset.data.reduce((a, b) => a + b, 0)
          const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0
          return `Personas: ${value} (${percentage}%)`
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

const getColorForAgeGroup = (rango) => {
  // Resaltar menores de 5 años y mayores de 65 en rojo
  if (rango.includes('0-5') || rango.includes('66+')) {
    return 'rgba(220, 53, 69, 0.8)' // Rojo
  }
  return 'rgba(13, 110, 253, 0.8)' // Azul normal
}

const updateChartData = () => {
  if (props.data && props.data.length > 0) {
    chartData.value.labels = props.data.map(item => item.rango_edad || 'Sin especificar')
    chartData.value.datasets[0].data = props.data.map(item => item.cantidad || 0)
    chartData.value.datasets[0].backgroundColor = props.data.map(item => getColorForAgeGroup(item.rango_edad))
    chartData.value.datasets[0].borderColor = props.data.map(item => getColorForAgeGroup(item.rango_edad).replace('0.8', '1'))
  } else {
    chartData.value.labels = []
    chartData.value.datasets[0].data = []
    chartData.value.datasets[0].backgroundColor = []
    chartData.value.datasets[0].borderColor = []
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