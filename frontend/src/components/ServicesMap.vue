<template>
  <div class="card shadow-sm border-0 p-3" style="height: 400px;">
    <h6 class="fw-bold mb-3">🗺 Cobertura de Servicios</h6>
    <div id="servicesMap" style="height: 100%; border-radius: 12px;"></div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

onMounted(() => {
  const map = L.map('servicesMap').setView([4.65, -74.05], 6)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
  }).addTo(map)

  // Ejemplo de marcador
  L.marker([4.65, -74.05]).addTo(map).bindPopup('Centro de salud').openPopup()
})
</script>
