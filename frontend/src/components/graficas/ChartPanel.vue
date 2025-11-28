<template>
  <div v-if="!noCard" :class="['card shadow-sm border-0 p-3 dashboard-chart', variant === 'donut' ? 'donut-variant' : '']">
    <h6 v-if="variant !== 'donut'" class="fw-bold mb-3"><slot name="title"></slot></h6>
     <div class="chart-wrapper" :style="{ height: height }">
        <canvas :id="chartId"></canvas>
      </div>
  </div>
  <div v-else class="chart-wrapper" :style="{ height: height }">
    <canvas :id="chartId"></canvas>
  </div>
</template>

<script setup>
import { onMounted, watch, ref } from 'vue'
import Chart from 'chart.js/auto'

const props = defineProps({
  chartId: { type: String, required: true },
  type: { type: String, default: 'bar' },
  data: { type: Object, required: true },
  options: { type: Object, default: () => ({}) },
  variant: { type: String, default: 'default' },
  height: { type: String, default: '280px' },
  noCard: { type: Boolean, default: false }
})

let chartInstance = null

onMounted(() => {
  const ctx = document.getElementById(props.chartId)
  if (ctx) {
    chartInstance = new Chart(ctx, {
      type: props.type,
      data: props.data,
      options: Object.assign({
        responsive: true,
        plugins: { legend: { position: 'bottom' } }
      }, props.options)
    })
    console.log(`Chart ${props.chartId} created successfully`)
  } else {
    console.error(`Canvas element with id ${props.chartId} not found`)
  }
})

// Watch for data changes and update chart
watch(() => props.data, (newData) => {
  if (chartInstance && newData) {
    chartInstance.data = newData
    chartInstance.update()
    console.log(`Chart ${props.chartId} updated with new data`)
  }
}, { deep: true })

// Cleanup on unmount
import { onUnmounted } from 'vue'
onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
})
</script>

<style scoped>
.dashboard-chart {
  border-radius: 12px;
}

.donut-variant {
  padding: 0;
  box-shadow: none;
  border: none;
}

.donut-variant .chart-wrapper {
  height: 160px !important;
  max-width: 160px !important;
}

.chart-wrapper {
  position: relative;
  width: 100%;
  max-width: 420px; /* 👈 ancho máximo */
  margin: auto;     /* centrar dentro de la tarjeta */
  overflow: hidden;
}
</style>
