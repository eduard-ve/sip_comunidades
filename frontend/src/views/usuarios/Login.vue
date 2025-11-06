<template>
  <div class="login-container" :class="{ 'dark-theme': isDarkTheme }">
    <!-- Botón para alternar el tema -->
    <button class="theme-toggle" @click="toggleTheme">
      <i :class="isDarkTheme ? 'bi bi-sun' : 'bi bi-moon'"></i>
    </button>

    <div class="login-wrapper">
      <!-- Lado izquierdo - Imagen de fondo con texto de bienvenida -->
      <div class="left-panel">
        <div class="welcome-overlay">
          <div class="welcome-content">
            <h1 class="welcome-title">SAFIR</h1>
            <p class="welcome-subtitle">Sistema de Administración y Fortalecimiento Integral Refugio</p>
            <p class="welcome-description">Plataforma integral para la gestión y análisis de datos poblacionales</p>
          </div>
        </div>
      </div>

      <!-- Lado derecho - Formulario de inicio de sesión -->
      <div class="right-panel">
        <div class="login-card">
          <div class="text-center mb-4">
            <div class="login-logo">
              <i class="bi bi-shield-lock-fill text-primary"></i>
            </div>
            <h2 class="login-title">iniciar sesión </h2>
            <p class="text-muted">Introduce tus credenciales para acceder al sistema</p>
          </div>

          <!-- Mensaje de error -->
          <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            {{ error }}
            <button type="button" class="btn-close" @click="error = ''"></button>
          </div>

          <form @submit.prevent="login">
            <div class="mb-3">
              <label for="username" class="form-label fw-semibold">Usuario</label>
              <div class="input-group">
                <span class="input-group-text">
                  <i class="bi bi-person-fill"></i>
                </span>
                <input
                  id="username"
                  v-model="username"
                  type="text"
                  class="form-control form-control-lg"
                  placeholder="Intoduce tu usuario"
                  :disabled="loading"
                  required
                >
              </div>
            </div>

            <div class="mb-3">
              <label for="password" class="form-label fw-semibold">Contraseña</label>
              <div class="input-group">
                <span class="input-group-text">
                  <i class="bi bi-lock-fill"></i>
                </span>
                <input
                  id="password"
                  v-model="password"
                  type="password"
                  class="form-control form-control-lg"
                  placeholder="Introduce tu contraseña"
                  :disabled="loading"
                  required
                >
              </div>
            </div>

            <button
              type="submit"
              class="btn btn-primary btn-lg w-100 mb-3"
              :disabled="loading || !username || !password"
            >
              <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
              <i v-else class="bi bi-box-arrow-in-right me-2"></i>
              {{ loading ? 'Signing in...' : 'Iniciar sesión' }}
            </button>
          </form>

          <div class="text-center mb-3">
            <small class="text-muted">
              <i class="bi bi-info-circle me-1"></i>
              Sistema seguro: todos los datos están protegidos
            </small>
          </div>

          <!-- Opciones de inicio de sesión social
           implemetar funciolidad futura -->
          <div class="social-login">
            <p class="text-muted mb-3">Conecta con nosotros</p>
            <div class="social-icons">
              <button class="btn btn-outline-secondary me-2">
                <i class="bi bi-google"></i>
              </button>
              <button class="btn btn-outline-secondary me-2">
                <i class="bi bi-facebook"></i>
              </button>
              <button class="btn btn-outline-secondary">
                <i class="bi bi-twitter"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref, computed, onMounted } from 'vue';
import { authService } from '../../services/api.js';
import { useAuth } from '../../stores/auth.js';

const router = useRouter();
const username = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);
const isDarkTheme = ref(true);
const showLoginForm = ref(false);

const isFormValid = computed(() => {
  return username.value.trim() && password.value.trim();
});

// Cambiar tema según preferencia guardada en localStorage
onMounted(() => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    isDarkTheme.value = savedTheme === 'dark';
  } else {
    // Tema por defecto oscuro
    isDarkTheme.value = true;
    localStorage.setItem('theme', 'dark');
  }
});

// Alternar tema claro/oscuro
function toggleTheme() {
  isDarkTheme.value = !isDarkTheme.value;
  localStorage.setItem('theme', isDarkTheme.value ? 'dark' : 'light');
}

// Mostrar formulario de login
function showLogin() {
  showLoginForm.value = true;
}

async function login() {
  if (!isFormValid.value) {
    error.value = 'Por favor complete todos los campos';
    return;
  }

  loading.value = true;
  error.value = '';

  try {
    const response = await authService.login({
      username: username.value.trim(),
      password: password.value
    });

    // Guardar tokens
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);

    // Inicializar estado de autenticación con el rol del usuario
    const { initAuth } = useAuth();
    initAuth();

    // Redirigir al dashboard
    router.push('/dashboard');
  } catch (err) {
    console.error('Error de login:', err);
    if (err.response?.status === 401) {
      error.value = 'Usuario o contraseña incorrectos';
    } else if (err.response?.status === 400) {
      error.value = 'Datos de entrada inválidos';
    } else if (!navigator.onLine) {
      error.value = 'Sin conexión a internet. Verifique su conexión.';
    } else {
      error.value = 'Error al iniciar sesión. Intente nuevamente.';
    }
  } finally {
    loading.value = false;
  }
}

// Limpiar error cuando el usuario empiece a escribir
function clearError() {
  if (error.value) {
    error.value = '';
  }
}
</script>

<style>
@import '../../assets/css/login.css';
</style>