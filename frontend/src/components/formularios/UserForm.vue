<template>
  <form @submit.prevent="onSubmit">
    <div class="mb-3">
      <label for="username" class="form-label">Nombre de Usuario</label>
      <input
        type="text"
        id="username"
        v-model="form.username"
        class="form-control"
        :class="{ 'is-invalid': errors.username }"
        placeholder="Ingrese el nombre de usuario"
        required
      />
      <div class="invalid-feedback">{{ errors.username }}</div>
    </div>

    <div class="mb-3">
      <label for="first_name" class="form-label">Nombre</label>
      <input
        type="text"
        id="first_name"
        v-model="form.first_name"
        class="form-control"
        :class="{ 'is-invalid': errors.first_name }"
        placeholder="Ingrese el nombre"
        required
      />
      <div class="invalid-feedback">{{ errors.first_name }}</div>
    </div>

    <div class="mb-3">
      <label for="last_name" class="form-label">Apellido</label>
      <input
        type="text"
        id="last_name"
        v-model="form.last_name"
        class="form-control"
        placeholder="Ingrese el apellido"
      />
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
      <label for="telefono" class="form-label">Teléfono</label>
      <input
        type="tel"
        id="telefono"
        v-model="form.telefono"
        class="form-control"
        placeholder="Ingrese el teléfono"
      />
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

    <!-- Campos de contraseña solo para nuevos usuarios -->
    <template v-if="!form.id">
      <div class="mb-3">
        <label for="password" class="form-label">Contraseña</label>
        <input
          type="password"
          id="password"
          v-model="form.password"
          class="form-control"
          :class="{ 'is-invalid': errors.password }"
          placeholder="Ingrese la contraseña"
          required
        />
        <div class="invalid-feedback">{{ errors.password }}</div>
      </div>

      <div class="mb-3">
        <label for="password2" class="form-label">Confirmar Contraseña</label>
        <input
          type="password"
          id="password2"
          v-model="form.password2"
          class="form-control"
          :class="{ 'is-invalid': errors.password2 }"
          placeholder="Confirme la contraseña"
          required
        />
        <div class="invalid-feedback">{{ errors.password2 }}</div>
      </div>
    </template>

    <div class="d-flex justify-content-end">
      <button type="button" class="btn btn-secondary me-2" @click="$emit('cancel')">Cancelar</button>
      <button type="submit" class="btn btn-primary">{{ form.id ? 'Actualizar' : 'Crear' }}</button>
    </div>
  </form>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      telefono: '',
      rol: 'invitado',
      password: '',
      password2: ''
    })
  },
  roles: {
    type: Array,
    default: () => ['admin', 'editor', 'invitado']
  }
})

const emit = defineEmits(['update:modelValue', 'submit', 'cancel'])

const form = reactive({ ...props.modelValue })
const errors = reactive({
  username: '',
  email: '',
  first_name: '',
  password: '',
  password2: ''
})

// Sincronizar cambios si se edita un usuario
watch(() => props.modelValue, (newVal) => {
  Object.assign(form, newVal)
})

function validate() {
  let valid = true
  // Reset errors
  Object.keys(errors).forEach(key => errors[key] = '')

  if (!form.username?.trim()) {
    errors.username = 'El nombre de usuario es obligatorio'
    valid = false
  }

  if (!form.first_name?.trim()) {
    errors.first_name = 'El nombre es obligatorio'
    valid = false
  }

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailPattern.test(form.email || '')) {
    errors.email = 'Email inválido'
    valid = false
  }

  // Validación de contraseña solo para nuevos usuarios
  if (!form.id) {
    if (!form.password) {
      errors.password = 'La contraseña es obligatoria'
      valid = false
    } else if (form.password.length < 8) {
      errors.password = 'La contraseña debe tener al menos 8 caracteres'
      valid = false
    }

    if (form.password !== form.password2) {
      errors.password2 = 'Las contraseñas no coinciden'
      valid = false
    }
  }

  return valid
}

function onSubmit() {
  if (!validate()) return

  const userData = { ...form }

  // Remover campos que no se deben enviar en la actualización
  if (form.id) {
    delete userData.password
    delete userData.password2
  }

  emit('submit', userData)
}
</script>

<style scoped>
/* Estilo opcional para el modal */
</style>
