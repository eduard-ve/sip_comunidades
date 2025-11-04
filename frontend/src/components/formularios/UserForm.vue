<template>
  <form @submit.prevent="onSubmit">
    <div class="row g-3">
      <!-- Primera fila: Username y Nombre -->
      <div class="col-md-6">
        <label for="username" class="form-label fw-semibold">Nombre de Usuario</label>
        <input
          type="text"
          id="username"
          v-model="form.username"
          class="form-control form-control-sm"
          :class="{ 'is-invalid': errors.username }"
          placeholder="Usuario"
          required
        />
        <div class="invalid-feedback">{{ errors.username }}</div>
      </div>

      <div class="col-md-6">
        <label for="first_name" class="form-label fw-semibold">Nombre</label>
        <input
          type="text"
          id="first_name"
          v-model="form.first_name"
          class="form-control form-control-sm"
          :class="{ 'is-invalid': errors.first_name }"
          placeholder="Nombre completo"
          required
        />
        <div class="invalid-feedback">{{ errors.first_name }}</div>
      </div>

      <!-- Segunda fila: Apellido y Email -->
      <div class="col-md-6">
        <label for="last_name" class="form-label fw-semibold">Apellido</label>
        <input
          type="text"
          id="last_name"
          v-model="form.last_name"
          class="form-control form-control-sm"
          placeholder="Apellido completo"
        />
      </div>

      <div class="col-md-6">
        <label for="email" class="form-label fw-semibold">Email</label>
        <input
          type="email"
          id="email"
          v-model="form.email"
          class="form-control form-control-sm"
          :class="{ 'is-invalid': errors.email }"
          placeholder="correo@ejemplo.com"
          required
        />
        <div class="invalid-feedback">{{ errors.email }}</div>
      </div>

      <!-- Tercera fila: Teléfono y Rol -->
      <div class="col-md-6">
        <label for="telefono" class="form-label fw-semibold">Teléfono</label>
        <input
          type="tel"
          id="telefono"
          v-model="form.telefono"
          class="form-control form-control-sm"
          placeholder="+57 300 123 4567"
        />
      </div>

      <div class="col-md-6">
        <label for="rol" class="form-label fw-semibold">Rol</label>
        <select
          id="rol"
          v-model="form.rol"
          class="form-select form-select-sm"
          required
        >
          <option value="" disabled>Seleccionar rol</option>
          <option v-for="r in roles" :key="r" :value="r">{{ getRoleDisplay(r) }}</option>
        </select>
      </div>

      <!-- Cuarta fila: Estado -->
      <div class="col-md-6">
        <label for="is_active" class="form-label fw-semibold">Estado</label>
        <select
          id="is_active"
          v-model="form.is_active"
          class="form-select form-select-sm"
          required
        >
          <option :value="true">Activo</option>
          <option :value="false">Inactivo</option>
        </select>
      </div>

      <!-- Campos de contraseña solo para nuevos usuarios -->
      <template v-if="!form.id">
        <!-- Quinta fila: Contraseñas -->
        <div class="col-md-6">
          <label for="password" class="form-label fw-semibold">Contraseña</label>
          <input
            type="password"
            id="password"
            v-model="form.password"
            class="form-control form-control-sm"
            :class="{ 'is-invalid': errors.password }"
            placeholder="Mínimo 8 caracteres"
            required
          />
          <div class="invalid-feedback">{{ errors.password }}</div>
        </div>

        <div class="col-md-6">
          <label for="password2" class="form-label fw-semibold">Confirmar Contraseña</label>
          <input
            type="password"
            id="password2"
            v-model="form.password2"
            class="form-control form-control-sm"
            :class="{ 'is-invalid': errors.password2 }"
            placeholder="Repetir contraseña"
            required
          />
          <div class="invalid-feedback">{{ errors.password2 }}</div>
        </div>
      </template>
    </div>

    <div class="d-flex justify-content-end mt-4 pt-3 border-top">
      <button type="button" class="btn btn-outline-secondary btn-sm me-2" @click="$emit('cancel')">
        <i class="bi bi-x-circle me-1"></i>Cancelar
      </button>
      <button type="submit" class="btn btn-primary btn-sm">
        <i class="bi bi-check-circle me-1"></i>{{ form.id ? 'Actualizar Usuario' : 'Crear Usuario' }}
      </button>
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
      is_active: true,
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

function getRoleDisplay(rol) {
  const roles = {
    'admin': '👑 Administrador',
    'editor': '✏️ Editor',
    'invitado': '👤 Invitado'
  }
  return roles[rol] || rol
}
</script>

<style scoped>
/* Estilo opcional para el modal */
</style>
