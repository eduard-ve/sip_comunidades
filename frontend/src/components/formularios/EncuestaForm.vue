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
        <div v-for="(pregunta, idx) in preguntas" :key="idx" class="d-flex align-items-center mb-1">
          <input v-model="pregunta.texto" type="text" class="form-control me-2" placeholder="Pregunta" required />
          <select v-model="pregunta.tipo" class="form-select me-2" style="max-width:120px;">
            <option value="texto">Texto</option>
            <option value="opcion">Opción múltiple</option>
          </select>
          <button type="button" class="btn btn-danger btn-sm" @click="eliminarPregunta(idx)">✕</button>
        </div>
        <button type="button" class="btn btn-success btn-sm mt-1" @click="agregarPregunta">Agregar pregunta</button>
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
  preguntas.value.push({ texto: '', tipo: 'texto' })
}
function eliminarPregunta(idx) {
  preguntas.value.splice(idx, 1)
}

function submit() {
  emit('save', {
    titulo: titulo.value,
    estado: estado.value,
    descripcion: descripcion.value,
    preguntas: preguntas.value.map(p => ({ ...p })),
    fecha: new Date().toISOString().slice(0, 10),
    respuestas: 0
  })
  titulo.value = ''
  estado.value = 'activa'
  descripcion.value = ''
  preguntas.value = []
}
</script>