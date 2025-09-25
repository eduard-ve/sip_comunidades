<template>
  <form @submit.prevent="onSubmit">
    <div class="mb-3">
      <label for="nombre" class="form-label">Nombre</label>
      <input
        type="text"
        id="nombre"
        v-model="form.nombre"
        class="form-control"
        :class="{ 'is-invalid': errors.nombre }"
        placeholder="Ingrese el nombre"
        required
      />
      <div class="invalid-feedback">{{ errors.nombre }}</div>
    </div>

    <div class="mb-3">
      <label for="email" class="form-label">Email</label>
      <input
        type="email"
        id="email"
        v-model="form.email"
        class="form-control"
        :class="{ 'is-invalid': errors.email }"
        placeholder="Ingrese el email"
        required
      />
      <div class="invalid-feedback">{{ errors.email }}</div>
    </div>

    <div class="mb-3">
      <label for="rol" class="form-label">Rol</label>
      <select
        id="rol"
        v-model="form.rol"
        class="form-select"
        required
      >
        <option value="" disabled>Seleccione un rol</option>
        <option v-for="r in roles" :key="r" :value="r">{{ r }}</option>
      </select>
    </div>

    <div class="mb-3 form-check">
      <input
        type="checkbox"
        id="estado"
        v-model="form.estado"
        class="form-check-input"
      />
      <label for="estado" class="form-check-label">Activo</label>
    </div>

    <div class="d-flex justify-content-end">
      <button type="button" class="btn btn-secondary me-2" @click="$emit('cancel')">Cancelar</button>
      <button type="submit" class="btn btn-primary">{{ form.id ? 'Actualizar' : 'Crear' }}</button>
    </div>
  </form>
</template>

<script setup>
import { reactive, watch, toRefs } from 'vue'
import { ref } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({ nombre: '', email: '', rol: '', estado: true })
  },
  roles: {
    type: Array,
    default: () => ['Admin', 'Editor', 'Invitado']
  }
})

const emit = defineEmits(['update:modelValue', 'submit', 'cancel'])

const form = reactive({ ...props.modelValue })
const errors = reactive({ nombre: '', email: '' })

// Sincronizar cambios si se edita un usuario
watch(() => props.modelValue, (newVal) => {
  Object.assign(form, newVal)
})

function validate() {
  let valid = true
  errors.nombre = ''
  errors.email = ''

  if (!form.nombre.trim()) {
    errors.nombre = 'El nombre es obligatorio'
    valid = false
  }

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailPattern.test(form.email)) {
    errors.email = 'Email inválido'
    valid = false
  }

  return valid
}

function onSubmit() {
  if (!validate()) return
  emit('submit', { ...form })
}
</script>

<style scoped>
/* Estilo opcional para el modal */
</style>
