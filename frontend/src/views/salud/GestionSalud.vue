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

      <!-- Información sobre la Gestión de Salud -->
      <div class="row g-3">
        <div class="col-12">
          <div class="card shadow-sm border-0 salud-card salud-info-card">
            <div class="card-body">
              <h5 class="fw-bold mb-3">
                <i class="bi bi-info-circle me-2 salud-icon"></i> Acerca de la Gestión de Salud
              </h5>
              <p class="mb-3">
                La Gestión de Salud Comunitaria es una herramienta creada para acompañar y mejorar el cuidado de la salud en la comunidad del Guaviare. Su propósito es facilitar el seguimiento de la información médica de las personas, apoyar las actividades preventivas y brindar una visión general del estado de salud de la población.
              </p>
              <p class="mb-3">
                Este sistema permite llevar un registro organizado de consultas, tratamientos y controles, lo que ayuda a que la atención sea más oportuna y eficaz. Además, ofrece la posibilidad de detectar alertas tempranas, recordar controles programados y visualizar estadísticas que permiten conocer cuáles son las enfermedades más frecuentes y cómo están cambiando con el tiempo.
              </p>
              <p class="mb-3">
                Gracias a esta información, las autoridades y equipos de salud pueden tomar decisiones más acertadas y planear acciones que beneficien a toda la comunidad, promoviendo hábitos saludables y una mejor calidad de vida.
              </p>
              <p class="text-muted small">
                <strong>Funcionalidades destacadas:</strong>
              </p>
              <ul class="text-muted small">
                <li>Registro completo de consultas y atenciones médicas para cada persona de la comunidad.</li>
                <li>Alertas inteligentes y recordatorios para actividades preventivas y controles de salud.</li>
                <li>Controles de salud programados con seguimiento de cumplimiento.</li>
                <li>Análisis de datos en tiempo real sobre la salud comunitaria, incluyendo estadísticas de enfermedades y distribución por edad.</li>
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
    title: 'Enfermedades más comunes',
    type: 'pie',
    data: {
      labels: ['Infecciones respiratorias', 'Malaria', 'Desnutrición'],
      datasets: [{ data: [40, 12, 8] }]
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
      saludStore.fetchControles(),
      saludStore.fetchEnfermedadesComunes()
    ])

    // Actualizar KPIs con datos reales
    kpis.value[0].value = saludStore.registrosCount
    kpis.value[1].value = saludStore.alertasActivas
    kpis.value[2].value = saludStore.controlesPendientes
    kpis.value[3].value = saludStore.controles.filter(c => c.realizado).length

    // Actualizar gráficos con datos reales
    if (saludStore.enfermedadesComunes.length > 0) {
      const labels = saludStore.enfermedadesComunes.map(e => e.enfermedad)
      const data = saludStore.enfermedadesComunes.map(e => e.casos)

      // Gráfica de barras (izquierda)
      charts.value.left.data.labels = labels
      charts.value.left.data.datasets[0].data = data

      // Gráfica circular (derecha) - mismos datos
      charts.value.right.data.labels = labels
      charts.value.right.data.datasets[0].data = data
    }

  } catch (error) {
    console.error('Error al cargar datos de salud:', error)
  }
})
</script>
