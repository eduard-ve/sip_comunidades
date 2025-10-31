<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card p-4" style="width: 300px;">
      <h4 class="mb-3 text-center">Iniciar Sesión</h4>

      <!-- Mensaje de error -->
      <div v-if="error" class="alert alert-danger" role="alert">
        {{ error }}
      </div>

      <input v-model="username" type="text" class="form-control mb-2" placeholder="Usuario" :disabled="loading">
      <input v-model="password" type="password" class="form-control mb-3" placeholder="Contraseña" :disabled="loading">

      <button class="btn btn-primary w-100" @click="login" :disabled="loading">
        <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
        {{ loading ? 'Iniciando...' : 'Entrar' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import { authService } from '../../services/api.js';

const router = useRouter();
const username = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);

async function login() {
  if (!username.value || !password.value) {
    error.value = 'Por favor ingrese usuario y contraseña';
    return;
  }

  loading.value = true;
  error.value = '';

  try {
    const response = await authService.login({
      username: username.value,
      password: password.value
    });

    // Guardar tokens
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);

    // Redirigir al dashboard
    router.push('/dashboard');
  } catch (err) {
    console.error('Error de login:', err);
    if (err.response?.status === 401) {
      error.value = 'Usuario o contraseña incorrectos';
    } else {
      error.value = 'Error al iniciar sesión. Intente nuevamente.';
    }
  } finally {
    loading.value = false;
  }
}
</script>
