<template>
  <div>
    <h5>Nueva Encuesta</h5>
    <form @submit.prevent="submit">
      <div class="mb-2">
        <label class="form-label">Título</label>
        <input v-model="titulo" type="text" class="form-control" required />
      </div>
      <div class="mb-2">
        <label class="form-label">Estado</label>
        <select v-model="estado" class="form-select" required>
          <option value="activa">Activa</option>
          <option value="cerrada">Cerrada</option>
          <option value="borrador">Borrador</option>
        </select>
      </div>
      <div class="mb-2">
        <label class="form-label">Descripción</label>
        <textarea v-model="descripcion" class="form-control" rows="2" />
      </div>
      <div class="mb-2">
        <label class="form-label">Preguntas</label>
        <div v-for="(pregunta, idx) in preguntas" :key="idx" class="border rounded p-3 mb-3">
          <div class="d-flex align-items-center mb-2">
            <input
              v-model="pregunta.texto"
              type="text"
              class="form-control me-2"
              placeholder="Texto de la pregunta"
              required
              minlength="3"
              @input="validatePregunta(idx)"
            />
            <select
              v-model="pregunta.tipo"
              class="form-select me-2"
              style="max-width:150px;"
              @change="onTipoChange(idx)"
              required
            >
              <option value="abierta">Abierta</option>
              <option value="opcion_multiple">Opción múltiple</option>
              <option value="si_no">Sí/No</option>
            </select>
            <button type="button" class="btn btn-danger btn-sm" @click="eliminarPregunta(idx)">✕</button>
          </div>

          <!-- Mensaje de error para pregunta -->
          <div v-if="pregunta.error" class="text-danger small mb-2">
            {{ pregunta.error }}
          </div>

          <!-- Opciones para preguntas de opción múltiple -->
          <div v-if="pregunta.tipo === 'opcion_multiple'" class="ms-3">
            <label class="form-label small">Opciones de respuesta:</label>
            <div v-for="(opcion, optIdx) in pregunta.opciones" :key="optIdx" class="d-flex align-items-center mb-1">
              <input
                v-model="opcion.texto_opcion"
                type="text"
                class="form-control form-control-sm me-2"
                placeholder="Opción"
                required
                minlength="1"
                @input="validateOpcion(idx, optIdx)"
              />
              <input
                v-model.number="opcion.valor"
                type="number"
                class="form-control form-control-sm me-2"
                placeholder="Valor"
                style="max-width:80px;"
                required
                min="0"
                @input="validateOpcion(idx, optIdx)"
              />
              <button type="button" class="btn btn-outline-danger btn-sm" @click="eliminarOpcion(idx, optIdx)">−</button>
            </div>
            <div v-if="pregunta.opcionesError" class="text-danger small mb-2">
              {{ pregunta.opcionesError }}
            </div>
            <button type="button" class="btn btn-outline-success btn-sm mt-1" @click="agregarOpcion(idx)">+ Agregar opción</button>
          </div>

        </div>
        <button type="button" class="btn btn-success btn-sm" @click="agregarPregunta">+ Agregar pregunta</button>
      </div>
      <button type="submit" class="btn btn-primary btn-sm mt-2">Guardar</button>
      <button type="button" class="btn btn-secondary btn-sm ms-2 mt-2" @click="$emit('cancel')">Cancelar</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const emit = defineEmits(['save', 'cancel'])

const titulo = ref('')
const estado = ref('activa')
const descripcion = ref('')
const preguntas = ref([])

function agregarPregunta() {
  preguntas.value.push({
    texto: '',
    tipo: 'abierta',
    opciones: [],
    error: '',
    opcionesError: ''
  })
  console.log('Pregunta agregada, total preguntas:', preguntas.value.length)
}

function eliminarPregunta(idx) {
  preguntas.value.splice(idx, 1)
  validateForm()
}

function onTipoChange(idx) {
  const pregunta = preguntas.value[idx]
  pregunta.error = ''
  pregunta.opcionesError = ''

  if (pregunta.tipo === 'opcion_multiple') {
    pregunta.opciones = [
      { texto_opcion: '', valor: 1 },
      { texto_opcion: '', valor: 2 }
    ]
  } else if (pregunta.tipo === 'si_no') {
    pregunta.opciones = [
      { texto_opcion: 'Sí', valor: 1 },
      { texto_opcion: 'No', valor: 0 }
    ]
  } else {
    pregunta.opciones = []
  }

  validatePregunta(idx)
}

function agregarOpcion(idx) {
  const pregunta = preguntas.value[idx]
  pregunta.opciones.push({
    texto_opcion: '',
    valor: pregunta.opciones.length + 1
  })
  pregunta.opcionesError = ''
}


function eliminarOpcion(pregIdx, optIdx) {
  preguntas.value[pregIdx].opciones.splice(optIdx, 1)
  validatePregunta(pregIdx)
}

function validatePregunta(idx) {
  const pregunta = preguntas.value[idx]
  pregunta.error = ''
  pregunta.opcionesError = ''

  // Validar texto de pregunta
  if (!pregunta.texto || pregunta.texto.trim().length < 3) {
    pregunta.error = 'La pregunta debe tener al menos 3 caracteres'
  }

  // Validar opciones según tipo
  if (pregunta.tipo === 'opcion_multiple') {
    if (!pregunta.opciones || pregunta.opciones.length === 0) {
      pregunta.opcionesError = 'Este tipo de pregunta requiere al menos una opción'
    } else {
      // Validar que todas las opciones tengan texto
      const opcionesInvalidas = pregunta.opciones.filter(opt => !opt.texto_opcion || !opt.texto_opcion.trim())
      if (opcionesInvalidas.length > 0) {
        pregunta.opcionesError = 'Todas las opciones deben tener texto'
      }
    }
  }
}

function validateOpcion(pregIdx, optIdx) {
  validatePregunta(pregIdx)
}

function validateForm() {
  let isValid = true

  // Validar título
  if (!titulo.value || titulo.value.trim().length < 3) {
    isValid = false
  }

  // Validar preguntas
  preguntas.value.forEach((pregunta, idx) => {
    validatePregunta(idx)
    if (pregunta.error || pregunta.opcionesError) {
      isValid = false
    }
  })

  return isValid
}

function submit() {
  // Validar formulario antes de enviar
  if (!validateForm()) {
    alert('Por favor corrige los errores en el formulario antes de guardar')
    return
  }

  console.log('Enviando formulario con preguntas:', preguntas.value)
  emit('save', {
    titulo: titulo.value.trim(),
    estado: estado.value,
    descripcion: descripcion.value?.trim() || '',
    preguntas: preguntas.value.map(p => ({
      texto_pregunta: p.texto.trim(),
      tipo: p.tipo,
      orden: preguntas.value.indexOf(p) + 1,
      opciones: p.opciones.map(opt => ({
        texto_opcion: opt.texto_opcion?.trim() || '',
        valor: opt.valor
      }))
    }))
  })

  // Limpiar formulario después de envío exitoso
  titulo.value = ''
  estado.value = 'activa'
  descripcion.value = ''
  preguntas.value = []
}
</script>