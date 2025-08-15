<template>
  <div class="map-container" ref="mapContainer"></div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  programas: {
    type: Array,
    default: () => [] // [{ nombre: 'Programa A', coordenadas: [lat, lng] }]
  }
})

const mapContainer = ref(null)
let map

onMounted(() => {
  map = L.map(mapContainer.value).setView([0, 0], 2)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map)

  updateMarkers()
})

// Función para agregar marcadores
function updateMarkers() {
  if (!map) return

  props.programas.forEach(p => {
    if (p.coordenadas && p.coordenadas.length === 2) {
      L.marker(p.coordenadas)
        .addTo(map)
        .bindPopup(`<b>${p.nombre}</b>`)
    }
  })

  // Ajustar el zoom al bounds de los marcadores
  const bounds = L.latLngBounds(props.programas.map(p => p.coordenadas))
  if (props.programas.length) map.fitBounds(bounds, { padding: [50, 50] })
}

// Actualiza marcadores si cambian los programas
watch(() => props.programas, () => {
  if (map) map.eachLayer(layer => { if (layer instanceof L.Marker) map.removeLayer(layer) })
  updateMarkers()
})
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 400px;
  border-radius: 12px;
}
</style>
