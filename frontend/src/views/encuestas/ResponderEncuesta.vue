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

              <form @submit.prevent="submitRespuesta">
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
                    <div class="form-check form-check-inline">
                      <input
                        v-model="respuestas[pregunta.id_pregunta]"
                        value="si"
                        class="form-check-input"
                        type="radio"
                        :name="'pregunta_' + pregunta.id_pregunta"
                        required
                      />
                      <label class="form-check-label">Sí</label>
                    </div>
                    <div class="form-check form-check-inline">
                      <input
                        v-model="respuestas[pregunta.id_pregunta]"
                        value="no"
                        class="form-check-input"
                        type="radio"
                        :name="'pregunta_' + pregunta.id_pregunta"
                        required
                      />
                      <label class="form-check-label">No</label>
                    </div>
                  </div>

                  <!-- Pregunta de escala -->
                  <div v-else-if="pregunta.tipo === 'escala'" class="mb-3">
                    <div class="scale-options">
                      <div v-for="opcion in pregunta.opciones" :key="opcion.id_opcion" class="form-check form-check-inline">
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
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const encuesta = ref({})
const respuestas = ref({})
const isSubmitting = ref(false)
const error = ref('')

onMounted(async () => {
  const token = route.params.token
  if (!token) {
    error.value = 'Token de encuesta no válido'
    return
  }

  try {
    const response = await axios.get(`/api/encuestas/by_token/?token=${token}`)
    if (response.data) {
      encuesta.value = response.data
    } else {
      error.value = 'Encuesta no encontrada'
    }
  } catch (err) {
    error.value = 'Encuesta no encontrada o no disponible'
    console.error('Error cargando encuesta:', err)
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

    // Enviar respuestas al backend
    const response = await axios.post('/api/respuestas/', respuestasData)

    if (response.status === 201) {
      alert('¡Gracias por tu respuesta! La encuesta ha sido enviada correctamente.')
      router.push('/')
    }
  } catch (err) {
    console.error('Error enviando respuesta:', err)
    alert('Error al enviar la respuesta. Por favor intenta de nuevo.')
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