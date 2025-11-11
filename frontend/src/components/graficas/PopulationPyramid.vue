<template>
  <ChartPanel :chartId="'pyramidChart'" :type="'bar'" :data="chartData" :options="chartOptions">
    <template #title>🏛 Pirámide de Población</template>
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
  labels: ['0-5', '6-12', '13-17', '18-30', '31-50', '51-65', '66+'],
  datasets: [
    {
      label: 'Hombres',
      data: [],
      backgroundColor: 'rgba(13, 110, 253, 0.8)',
      borderColor: 'rgba(13, 110, 253, 1)',
      borderWidth: 1
    },
    {
      label: 'Mujeres',
      data: [],
      backgroundColor: 'rgba(255, 193, 7, 0.8)',
      borderColor: 'rgba(255, 193, 7, 1)',
      borderWidth: 1
    }
  ]
})

const chartOptions = ref({
  indexAxis: 'y',
  responsive: true,
  plugins: {
    legend: {
      position: 'bottom'
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          const value = Math.abs(context.parsed.x) || 0
          return `${context.dataset.label}: ${value}`
        }
      }
    }
  },
  scales: {
    x: {
      stacked: false,
      ticks: {
        callback: value => Math.abs(value)
      },
      grid: {
        color: function(context) {
          // Líneas marcando edades críticas
          const ageGroups = ['0-5', '6-12', '13-17', '18-30', '31-50', '51-65', '66+']
          const criticalAges = [5, 18, 65] // Edades críticas
          const currentLabel = ageGroups[context.index]

          if (currentLabel) {
            const maxAge = parseInt(currentLabel.split('-')[1] || currentLabel.replace('+', ''))
            if (criticalAges.includes(maxAge)) {
              return 'rgba(255, 0, 0, 0.3)' // Rojo para edades críticas
            }
          }
          return 'rgba(0, 0, 0, 0.1)' // Normal
        }
      }
    },
    y: {
      stacked: false
    }
  }
})

const updateChartData = () => {
  if (props.data && props.data.length > 0) {
    // Convertir datos de edad a formato pirámide
    const rangos = ['0-5', '6-12', '13-17', '18-30', '31-50', '51-65', '66+']
    const hombres = []
    const mujeres = []

    rangos.forEach(rango => {
      const rangoData = props.data.find(item => item.rango_edad === rango)
      if (rangoData) {
        // Aquí necesitaríamos datos separados por género
        // Por ahora, simulamos distribución 50/50
        const total = rangoData.cantidad || 0
        const mitad = Math.floor(total / 2)
        hombres.push(-mitad) // Negativo para lado izquierdo
        mujeres.push(mitad)  // Positivo para lado derecho
      } else {
        hombres.push(0)
        mujeres.push(0)
      }
    })

    chartData.value.datasets[0].data = hombres
    chartData.value.datasets[1].data = mujeres
  } else {
    chartData.value.datasets[0].data = []
    chartData.value.datasets[1].data = []
  }
}

onMounted(() => {
  updateChartData()
})

watch(() => props.data, () => {
  updateChartData()
}, { deep: true })
</script>
