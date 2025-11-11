<template>
  <ChartPanel :chartId="'ocupacionesChart'" :type="'bar'" :data="chartData" :options="chartOptions">
    <template #title>💼 Top Ocupaciones</template>
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
    backgroundColor: 'rgba(40, 167, 69, 0.8)',
    borderColor: 'rgba(40, 167, 69, 1)',
    borderWidth: 1,
    borderRadius: 4,
    borderSkipped: false
  }]
})

const chartOptions = ref({
  responsive: true,
  indexAxis: 'y', // Barras horizontales
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          const value = context.parsed.x || 0
          return `Personas: ${value}`
        }
      }
    }
  },
  scales: {
    x: {
      beginAtZero: true,
      ticks: {
        precision: 0
      }
    },
    y: {
      ticks: {
        font: {
          size: 11
        }
      }
    }
  },
  onClick: (event, elements) => {
    if (elements.length > 0) {
      const index = elements[0].index
      const ocupacion = props.data[index]?.ocupacion
      if (ocupacion) {
        // Emitir evento para filtrar por esta ocupación
        const event = new CustomEvent('filtrar-ocupacion', {
          detail: { ocupacion_id: ocupacion }
        })
        window.dispatchEvent(event)
      }
    }
  }
})

const updateChartData = () => {
  if (props.data && props.data.length > 0) {
    chartData.value.labels = props.data.map(item => item.ocupacion || 'Sin especificar')
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