<template>
  <BaseModule 
    title="Salud Comunitaria" 
    :kpis="kpis" 
    :charts="charts"
    :table="tableData"
    :show-search="true"
  >
    <!-- Contenido adicional arriba de los charts -->
    <template #extra>
      <div class="row g-3">
        <!-- Campañas -->
        <div class="col-md-6">
          <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
              <h5 class="fw-bold mb-3">
                <i class="bi bi-bullhorn me-2"></i> Campañas de Salud
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
          <div class="card shadow-sm border-0 h-100">
            <div class="card-body">
              <h5 class="fw-bold mb-3">
                <i class="bi bi-hospital me-2"></i> Recursos disponibles
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
          <div class="card shadow-sm border-0">
            <div class="card-body">
              <h5 class="fw-bold mb-3">
                <i class="bi bi-exclamation-triangle me-2"></i> Alertas de Salud
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
          <div class="card shadow-sm border-0">
            <div class="card-body">
              <h5 class="fw-bold mb-3">
                <i class="bi bi-leaf me-2"></i> Medicina Tradicional
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
import BaseModule from '../components/BaseModule.vue'

/* Indicadores principales */
const kpis = [
  { title: 'Niños vacunados', value: '85%', icon: 'bi bi-capsule' },
  { title: 'Controles prenatales', value: 35, icon: 'bi bi-gender-female' },
  { title: 'Casos de malaria (último mes)', value: 12, icon: 'bi bi-bug' },
  { title: 'Acceso a agua potable', value: '70%', icon: 'bi bi-droplet' }
]

/* Gráficos representativos */
const charts = {
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
}

/* Campañas de salud activas */
const campaigns = [
  'Campaña de vacunación - Agosto 2025',
  'Prevención de malaria en temporada de lluvias',
  'Charlas sobre alimentación saludable',
  'Taller de medicina tradicional'
]
</script>
