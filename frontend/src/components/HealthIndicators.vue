<template>
  <div class="card shadow-sm border-0 p-3">
    <h6 class="fw-bold mb-3">🩺 Indicadores de Salud</h6>
    <canvas id="healthChart"></canvas>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Chart from 'chart.js/auto'

onMounted(() => {
  new Chart(document.getElementById('healthChart'), {
    type: 'bar',
    data: {
      labels: ['Vacunación', 'Cobertura Médica', 'Atención Primaria'],
      datasets: [
        {
          label: 'Porcentaje',
          data: [85, 70, 60],
          backgroundColor: ['#0d6efd', '#198754', '#ffc107'],
          borderRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, max: 100 }
      }
    }
  })
})
</script>
