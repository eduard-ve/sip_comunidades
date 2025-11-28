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
              <div v-if="saludStore.alertas.length > 0" class="table-responsive">
                <table class="table table-striped table-hover">
                  <thead class="table-dark">
                    <tr>
                      <th>Persona</th>
                      <th>Título</th>
                      <th>Descripción</th>
                      <th>Prioridad</th>
                      <th>Estado</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="alerta in saludStore.alertas" :key="alerta.id">
                      <td>{{ alerta.persona_nombre }} {{ alerta.persona_apellido }}</td>
                      <td>{{ alerta.titulo }}</td>
                      <td>{{ alerta.descripcion }}</td>
                      <td>
                        <span class="badge" :class="alerta.prioridad === 'alta' ? 'bg-danger' : alerta.prioridad === 'media' ? 'bg-warning' : alerta.prioridad === 'critica' ? 'bg-dark' : 'bg-info'">
                          {{ alerta.prioridad }}
                        </span>
                      </td>
                      <td>
                        <span v-if="!alerta.resuelta" class="text-danger">Activa</span>
                        <span v-else class="text-success">Resuelta</span>
                      </td>
                      <td>
                        <button class="btn btn-sm btn-outline-primary me-1" @click="editarAlerta(alerta)">
                          <i class="bi bi-pencil"></i> Editar
                        </button>
                        <button class="btn btn-sm btn-outline-danger" @click="eliminarAlerta(alerta.id)">
                          <i class="bi bi-trash"></i> Eliminar
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p v-else class="text-muted">No hay alertas registradas en este momento.</p>

              <!-- Formulario para crear nueva alerta -->
              <div class="mt-3 border-top pt-3">
                <h6 class="text-primary mb-3"><i class="bi bi-plus-circle me-2"></i>Crear Nueva Alerta</h6>
                <form @submit.prevent="crearAlerta" class="row g-3">
                  <div class="col-md-6">
                    <label class="form-label fw-bold">Título</label>
                    <input v-model="nuevaAlerta.titulo" type="text" class="form-control" placeholder="Ej: Alerta de infección" required>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label fw-bold">Prioridad</label>
                    <select v-model="nuevaAlerta.prioridad" class="form-select" required>
                      <option value="baja">Baja</option>
                      <option value="media">Media</option>
                      <option value="alta">Alta</option>
                      <option value="critica">Crítica</option>
                    </select>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label fw-bold">Persona</label>
                    <select v-model="nuevaAlerta.persona" class="form-select" required>
                      <option value="">Seleccionar persona</option>
                      <option v-for="persona in personas" :key="persona.id" :value="persona.id">
                        {{ persona.primer_nombre }} {{ persona.primer_apellido }} - {{ persona.numero_identificacion }}
                      </option>
                    </select>
                  </div>
                  <div class="col-12">
                    <label class="form-label fw-bold">Descripción</label>
                    <textarea v-model="nuevaAlerta.descripcion" class="form-control" rows="3" placeholder="Describe la alerta en detalle" required></textarea>
                  </div>
                  <div class="col-12">
                    <button type="submit" class="btn btn-success me-2" :disabled="!nuevaAlerta.titulo || !nuevaAlerta.descripcion || !nuevaAlerta.persona">
                      <i class="bi bi-check-circle me-2"></i>{{ isEditing ? 'Actualizar Alerta' : 'Crear Alerta' }}
                    </button>
                    <button v-if="isEditing" type="button" class="btn btn-secondary" @click="resetForm">
                      <i class="bi bi-x-circle me-2"></i>Cancelar
                    </button>
                  </div>
                </form>
              </div>
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
import axios from 'axios'
import { useSaludStore } from '../../stores/salud.js'
import BaseModule from '../../components/comun/BaseModule.vue'
import '../../assets/css/GestionSalud.css'

const saludStore = useSaludStore()

/* Estado reactivo para datos dinámicos */
const kpis = ref([
  { title: 'Alertas activas', value: 0, icon: 'bi bi-exclamation-triangle' },
  { title: 'Total de alertas', value: 0, icon: 'bi bi-bell' }
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

/* Nueva alerta */
const nuevaAlerta = ref({
  titulo: '',
  descripcion: '',
  prioridad: 'media',
  persona: null
})

/* Personas disponibles */
const personas = ref([])

/* Edición */
const isEditing = ref(false)
const editingId = ref(null)

/* Crear o actualizar alerta */
const crearAlerta = async () => {
  try {
    if (isEditing.value) {
      await saludStore.updateAlerta(editingId.value, nuevaAlerta.value)
    } else {
      await saludStore.createAlerta(nuevaAlerta.value)
    }
    // Limpiar formulario
    resetForm()
    // Recargar alertas
    await saludStore.fetchAlertas()
  } catch (error) {
    console.error('Error guardando alerta:', error)
  }
}

/* Editar alerta */
const editarAlerta = (alerta) => {
  nuevaAlerta.value = {
    titulo: alerta.titulo,
    descripcion: alerta.descripcion,
    prioridad: alerta.prioridad,
    persona: alerta.persona
  }
  isEditing.value = true
  editingId.value = alerta.id
}

/* Eliminar alerta */
const eliminarAlerta = async (id) => {
  if (confirm('¿Estás seguro de eliminar esta alerta?')) {
    try {
      await saludStore.deleteAlerta(id)
      await saludStore.fetchAlertas()
    } catch (error) {
      console.error('Error eliminando alerta:', error)
    }
  }
}

/* Fetch personas */
const fetchPersonas = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await axios.get('http://127.0.0.1:8000/api/poblacion/personas/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    personas.value = response.data
  } catch (error) {
    console.error('Error fetching personas:', error)
  }
}

/* Reset form */
const resetForm = () => {
  nuevaAlerta.value = {
    titulo: '',
    descripcion: '',
    prioridad: 'media',
    persona: null
  }
  isEditing.value = false
  editingId.value = null
}

/* Cargar datos del backend */
onMounted(async () => {
  try {
    await Promise.all([
      saludStore.fetchAlertas(),
      saludStore.fetchEnfermedadesComunes(),
      fetchPersonas()
    ])

    // Actualizar KPIs con datos reales
    kpis.value[0].value = saludStore.alertasActivas
    kpis.value[1].value = saludStore.alertas.length

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
