<template>
  <div class="responder-encuesta">
    <div class="container-fluid">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow">
            <div class="card-header bg-primary text-white">
              <h4 class="mb-0">{{ encuesta.titulo }}</h4>
            </div>
            <div class="card-body">
              <p class="text-muted mb-4">{{ encuesta.descripcion }}</p>

              <!-- Mostrar mensaje de error si existe -->
              <div v-if="error" class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle"></i> {{ error }}
              </div>

              <!-- Mostrar mensaje si no hay preguntas -->
              <div v-if="!encuesta.preguntas || encuesta.preguntas.length === 0" class="alert alert-info" role="alert">
                <i class="bi bi-info-circle"></i> Esta encuesta no tiene preguntas configuradas.
              </div>

              <form v-else @submit.prevent="submitRespuesta">
                <div v-for="(pregunta, index) in encuesta.preguntas" :key="pregunta.id_pregunta" class="mb-4">
                  <h5 class="question-title">{{ index + 1 }}. {{ pregunta.texto_pregunta }}</h5>

                  <!-- Pregunta de texto abierto -->
                  <div v-if="pregunta.tipo === 'abierta'" class="mb-3">
                    <textarea
                      v-model="respuestas[pregunta.id_pregunta]"
                      class="form-control"
                      rows="3"
                      placeholder="Escribe tu respuesta aquí..."
                      required
                    ></textarea>
                  </div>

                  <!-- Pregunta de opción múltiple -->
                  <div v-else-if="pregunta.tipo === 'opcion_multiple'" class="mb-3">
                    <div v-for="opcion in pregunta.opciones" :key="opcion.id_opcion" class="form-check">
                      <input
                        v-model="respuestas[pregunta.id_pregunta]"
                        :value="opcion.id_opcion"
                        class="form-check-input"
                        type="radio"
                        :name="'pregunta_' + pregunta.id_pregunta"
                        required
                      />
                      <label class="form-check-label">
                        {{ opcion.texto_opcion }}
                      </label>
                    </div>
                    <div v-if="!pregunta.opciones || pregunta.opciones.length === 0" class="text-muted">
                      No hay opciones disponibles para esta pregunta.
                    </div>
                  </div>

                  <!-- Pregunta Sí/No -->
                  <div v-else-if="pregunta.tipo === 'si_no'" class="mb-3">
                    <div v-for="opcion in pregunta.opciones" :key="opcion.id_opcion" class="form-check">
                      <input
                        v-model="respuestas[pregunta.id_pregunta]"
                        :value="opcion.id_opcion"
                        class="form-check-input"
                        type="radio"
                        :name="'pregunta_' + pregunta.id_pregunta"
                        required
                      />
                      <label class="form-check-label">
                        {{ opcion.texto_opcion }}
                      </label>
                    </div>
                    <div v-if="!pregunta.opciones || pregunta.opciones.length === 0" class="text-muted">
                      No hay opciones disponibles para esta pregunta.
                    </div>
                  </div>

                  <!-- Pregunta de escala -->
                  <div v-else-if="pregunta.tipo === 'escala'" class="mb-3">
                    <div class="scale-options">
                      <div v-for="opcion in pregunta.opciones" :key="opcion.id_opcion" class="form-check">
                        <input
                          v-model="respuestas[pregunta.id_pregunta]"
                          :value="opcion.id_opcion"
                          class="form-check-input"
                          type="radio"
                          :name="'pregunta_' + pregunta.id_pregunta"
                          required
                        />
                        <label class="form-check-label">
                          {{ opcion.texto_opcion }} ({{ opcion.valor }})
                        </label>
                      </div>
                    </div>
                    <div v-if="!pregunta.opciones || pregunta.opciones.length === 0" class="text-muted">
                      No hay opciones disponibles para esta pregunta.
                    </div>
                  </div>

                </div>

                <div class="d-flex justify-content-between">
                  <button type="button" class="btn btn-secondary" @click="cancelar">Cancelar</button>
                  <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                    {{ isSubmitting ? 'Enviando...' : 'Enviar Respuesta' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../services/api.js'

const route = useRoute()
const router = useRouter()

const encuesta = ref({})
const respuestas = ref({})
const isSubmitting = ref(false)
const error = ref('')

onMounted(async () => {
  const id = route.params.id
  if (!id) {
    error.value = 'ID de encuesta no válido'
    return
  }

  try {
    console.log('Cargando encuesta con ID:', id)
    const response = await api.get(`/encuestas/by_token/?token=${id}`)
    console.log('Respuesta del servidor:', response)

    if (response.data) {
      encuesta.value = response.data
      console.log('Encuesta cargada:', encuesta.value)

      // Inicializar respuestas vacías para cada pregunta
      if (encuesta.value.preguntas && encuesta.value.preguntas.length > 0) {
        encuesta.value.preguntas.forEach(pregunta => {
          respuestas.value[pregunta.id_pregunta] = null
        })
        console.log('Respuestas inicializadas para', encuesta.value.preguntas.length, 'preguntas')
      } else {
        console.warn('La encuesta no tiene preguntas configuradas')
      }
    } else {
      error.value = 'Encuesta no encontrada'
    }
  } catch (err) {
    console.error('Error cargando encuesta:', err)
    console.error('Detalles del error:', err.response?.data)

    if (err.response && err.response.data && err.response.data.message) {
      error.value = err.response.data.message
    } else if (err.response && err.response.status === 404) {
      error.value = 'Encuesta no encontrada o no disponible'
    } else {
      error.value = 'Error al cargar la encuesta. Por favor intenta de nuevo.'
    }
  }
})

const submitRespuesta = async () => {
  // Validar que todas las preguntas hayan sido respondidas
  const preguntasSinResponder = encuesta.value.preguntas.filter((pregunta, index) => {
    const respuesta = respuestas.value[pregunta.id_pregunta]
    return !respuesta || (typeof respuesta === 'string' && !respuesta.trim())
  })

  if (preguntasSinResponder.length > 0) {
    alert('Por favor responde todas las preguntas antes de enviar.')
    return
  }

  isSubmitting.value = true
  try {
    // Preparar las respuestas para enviar al backend
    const respuestasData = Object.entries(respuestas.value).map(([preguntaId, respuesta]) => ({
      pregunta: parseInt(preguntaId),
      encuesta: encuesta.value.id_encuesta,
      respuesta_texto: typeof respuesta === 'string' ? respuesta.trim() : null,
      opcion: typeof respuesta === 'number' ? respuesta : null
    }))

    console.log('Enviando respuestas:', respuestasData)

    // Enviar respuestas al backend usando POST al endpoint bulk
    const response = await api.post('/encuestas/respuestas/bulk/', respuestasData)

    console.log('Respuesta del servidor:', response)

    if (response.status === 201) {
      alert('¡Gracias por tu respuesta! La encuesta ha sido enviada correctamente.')
      router.push('/')
    } else {
      throw new Error('Respuesta inesperada del servidor')
    }
  } catch (err) {
    console.error('Error enviando respuesta:', err)
    console.error('Detalles del error:', err.response?.data)

    let errorMessage = 'Error al enviar la respuesta. Por favor intenta de nuevo.'

    if (err.response?.data?.error) {
      errorMessage = err.response.data.error
    } else if (err.response?.data?.message) {
      errorMessage = err.response.data.message
    } else if (err.response?.data?.detail) {
      errorMessage = err.response.data.detail
    } else if (err.message) {
      errorMessage = err.message
    }

    alert(errorMessage)
  } finally {
    isSubmitting.value = false
  }
}

const cancelar = () => {
  if (confirm('¿Estás seguro de que quieres cancelar? Tu progreso se perderá.')) {
    router.push('/')
  }
}
</script>

<style scoped>
.responder-encuesta {
  min-height: 100vh;
  background-color: #f8f9fa;
  padding: 2rem 0;
}

.question-title {
  color: #495057;
  margin-bottom: 1rem;
  font-weight: 600;
}

.scale-options {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.form-check-inline {
  margin-right: 1rem;
}

.card {
  border: none;
  border-radius: 0.5rem;
}

.card-header {
  border-radius: 0.5rem 0.5rem 0 0 !important;
}
</style>
