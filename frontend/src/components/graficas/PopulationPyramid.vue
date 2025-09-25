<template>
  <ChartPanel :chartId="'pyramidChart'" :type="'bar'" :data="chartData" :options="chartOptions">
    <template #title>🏛 Pirámide de Población</template>
  </ChartPanel>
</template>

<script setup>
import ChartPanel from './ChartPanel.vue'

const chartData = {
  labels: ['0-4', '5-9', '10-14', '15-19', '20-24'],
  datasets: [
    {
      label: 'Hombres',
      data: [-500, -400, -300, -200, -100],
      backgroundColor: 'rgba(13, 110, 253, 0.7)'
    },
    {
      label: 'Mujeres',
      data: [480, 420, 350, 280, 150],
      backgroundColor: 'rgba(255, 193, 7, 0.7)'
    }
  ]
}

const chartOptions = {
  indexAxis: 'y',
  scales: {
    x: {
      stacked: true,
      ticks: {
        callback: value => Math.abs(value)
      }
    },
    y: { stacked: true }
  }
}
</script>
