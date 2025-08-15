<template>
  <div class="card shadow-sm border-0 p-3">
    <h6 class="fw-bold mb-3">📚 Educación y Empleo</h6>
    <canvas id="educationChart"></canvas>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Chart from 'chart.js/auto'

onMounted(() => {
  new Chart(document.getElementById('educationChart'), {
    type: 'line',
    data: {
      labels: ['2019', '2020', '2021', '2022', '2023'],
      datasets: [
        {
          label: 'Tasa de Escolaridad (%)',
          data: [85, 87, 83, 88, 90],
          borderColor: '#0d6efd',
          backgroundColor: 'rgba(13, 110, 253, 0.2)',
          tension: 0.3,
          fill: true
        },
        {
          label: 'Empleo Juvenil (%)',
          data: [60, 58, 62, 65, 68],
          borderColor: '#198754',
          backgroundColor: 'rgba(25, 135, 84, 0.2)',
          tension: 0.3,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'bottom' } },
      scales: {
        y: { beginAtZero: true, max: 100 }
      }
    }
  })
})
</script>
