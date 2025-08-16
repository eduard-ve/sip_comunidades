<template>
  <div class="card shadow-sm border-0 p-3 dashboard-chart">
    <h6 class="fw-bold mb-3"><slot name="title"></slot></h6>
     <div class="chart-wrapper">
        <canvas :id="chartId"></canvas>
      </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Chart from 'chart.js/auto'

const props = defineProps({
  chartId: { type: String, required: true },
  type: { type: String, default: 'bar' },
  data: { type: Object, required: true },
  options: { type: Object, default: () => ({}) }
})

onMounted(() => {
  new Chart(document.getElementById(props.chartId), {
    type: props.type,
    data: props.data,
    options: Object.assign({
      responsive: true,
      plugins: { legend: { position: 'bottom' } }
    }, props.options)
  })
})
</script>

<style scoped>
.dashboard-chart {
  border-radius: 12px;
}

.chart-wrapper {
  position: relative;
  width: 100%;
  max-width: 420px; /* 👈 ancho máximo */
  height: 280px;    /* 👈 altura fija más pequeña */
  margin: auto;     /* centrar dentro de la tarjeta */
}
</style>
