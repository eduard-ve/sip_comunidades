<template>
  <BaseModule 
    title="Salud Comunitaria" 
    :kpis="kpis" 
    :charts="charts"
    :show-search="false"
  >
    <!-- Contenido adicional arriba de los charts -->
    <template #extra>
      <div class="row g-3">
        <!-- Campañas -->
        <div class="col-md-6">
          <div class="card shadow-sm border-0 h-100 salud-card salud-campaigns-card">
            <div class="card-body">
              <h5 class="fw-bold mb-3">
                <i class="bi bi-bullhorn me-2 salud-icon"></i> Campañas de Salud
              </h5>
              <ul class="list-group list-group-flush">
                <li v-for="(c, i) in campaigns" :key="i" class="list-group-item">
                  {{ c }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Recursos disponibles -->
        <div class="col-md-6">
          <div class="card shadow-sm border-0 h-100 salud-card salud-resources-card">
            <div class="card-body">
              <h5 class="fw-bold mb-3">
                <i class="bi bi-hospital me-2 salud-icon"></i> Recursos disponibles
              </h5>
              <ul class="list-group list-group-flush">
                <li class="list-group-item">
                  Hospital San José del Guaviare (baja y mediana complejidad)
                </li>
                <li class="list-group-item">Secretaría de Salud Departamental del Guaviare</li>
                <li class="list-group-item">IPS: Nueva EPS, Fisiomed, Medicenter</li>
                <li class="list-group-item">Ambulancia en cabecera municipal</li>
                <li class="list-group-item">Emergencias: 310-456-7890</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Contenido adicional abajo de charts -->
    <template #default>
      <div class="row g-3 mt-2">
        <!-- Alertas -->
        <div class="col-12">
          <div class="card shadow-sm border-0 salud-card salud-alerts">
            <div class="card-body">
              <h5 class="fw-bold mb-3">
                <i class="bi bi-exclamation-triangle me-2 salud-icon"></i> Alertas de Salud
              </h5>
              <ul>
                <li>⚠️ Prevención de dengue: eliminar criaderos de zancudos.</li>
                <li>💧 Recomendación: hervir el agua antes de consumir.</li>
                <li>🌧️ En temporada de lluvias: cuidado con enfermedades respiratorias.</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Medicina tradicional -->
        <div class="col-12">
          <div class="card shadow-sm border-0 salud-card salud-traditional-medicine">
            <div class="card-body">
              <h5 class="fw-bold mb-3">
                <i class="bi bi-leaf me-2 salud-icon"></i> Medicina Tradicional
              </h5>
              <p>
                En la comunidad se valora el conocimiento ancestral transmitido por los mayores.
                La medicina tradicional se basa en plantas medicinales, rituales y prácticas
                espirituales que fortalecen el bienestar colectivo.
              </p>
              <ul class="list-group list-group-flush">
                <li class="list-group-item">🌿 Infusiones de hierbas para problemas digestivos</li>
                <li class="list-group-item">🌱 Baños de plantas para tratamiento de fiebres</li>
                <li class="list-group-item">🔥 Sahumerios para limpiezas espirituales</li>
                <li class="list-group-item">🪶 Consejos de sabedores y médicos tradicionales</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </template>
  </BaseModule>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useSaludStore } from '../../stores/salud.js'
import BaseModule from '../../components/comun/BaseModule.vue'
import '../../assets/css/GestionSalud.css'

const saludStore = useSaludStore()

/* Estado reactivo para datos dinámicos */
const kpis = ref([
  { title: 'Registros de salud', value: 0, icon: 'bi bi-clipboard-data' },
  { title: 'Alertas activas', value: 0, icon: 'bi bi-exclamation-triangle' },
  { title: 'Controles pendientes', value: 0, icon: 'bi bi-calendar-check' },
  { title: 'Controles realizados', value: 0, icon: 'bi bi-check-circle' }
])

const charts = ref({
  left: {
    title: 'Enfermedades más comunes',
    type: 'bar',
    data: {
      labels: ['Infecciones respiratorias', 'Malaria', 'Desnutrición'],
      datasets: [{ label: 'Casos', data: [40, 12, 8] }]
    }
  },
  right: {
    title: 'Distribución por grupos de edad',
    type: 'pie',
    data: {
      labels: ['Niños', 'Adultos', 'Adultos mayores'],
      datasets: [{ data: [45, 40, 15] }]
    }
  }
})

/* Campañas de salud activas */
const campaigns = [
  'Campaña de vacunación - Agosto 2025',
  'Prevención de malaria en temporada de lluvias',
  'Charlas sobre alimentación saludable',
  'Taller de medicina tradicional'
]

/* Cargar datos del backend */
onMounted(async () => {
  try {
    await Promise.all([
      saludStore.fetchRegistros(),
      saludStore.fetchAlertas(),
      saludStore.fetchControles()
    ])

    // Actualizar KPIs con datos reales
    kpis.value[0].value = saludStore.registrosCount
    kpis.value[1].value = saludStore.alertasActivas
    kpis.value[2].value = saludStore.controlesPendientes
    kpis.value[3].value = saludStore.controles.filter(c => c.realizado).length

  } catch (error) {
    console.error('Error al cargar datos de salud:', error)
  }
})
</script>
