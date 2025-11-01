<template>
  <div class="login-container">
    <div class="login-overlay">
      <div class="login-card">
        <div class="text-center mb-4">
          <div class="login-logo">
            <i class="bi bi-shield-lock-fill text-primary" style="font-size: 3rem;"></i>
          </div>
          <h2 class="login-title">Sistema de Información Poblacional</h2>
          <p class="text-muted">Inicie sesión para acceder al sistema</p>
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
                placeholder="Ingrese su usuario"
                :disabled="loading"
                required
              >
            </div>
          </div>

          <div class="mb-4">
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
                placeholder="Ingrese su contraseña"
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
            {{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
          </button>
        </form>

        <div class="text-center">
          <small class="text-muted">
            <i class="bi bi-info-circle me-1"></i>
            Sistema seguro - Todos los datos están protegidos
          </small>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref, computed } from 'vue';
import { authService } from '../../services/api.js';

const router = useRouter();
const username = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);

const isFormValid = computed(() => {
  return username.value.trim() && password.value.trim();
});

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

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.login-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 450px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.login-logo {
  margin-bottom: 20px;
}

.login-title {
  color: #2c3e50;
  font-weight: 700;
  margin-bottom: 8px;
  font-size: 1.8rem;
}

.form-label {
  color: #34495e;
  margin-bottom: 8px;
}

.input-group-text {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  color: #6c757d;
}

.form-control {
  border-left: none;
  padding: 12px 16px;
}

.form-control:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  border-left: none;
}

.input-group:focus-within .input-group-text {
  border-color: #007bff;
  background: #e3f2fd;
}

.btn-primary {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  border: none;
  padding: 12px 24px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #0056b3 0%, #004085 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 123, 255, 0.3);
}

.btn-primary:disabled {
  background: #6c757d;
  opacity: 0.7;
}

.alert {
  border-radius: 10px;
  border: none;
  font-weight: 500;
}

.alert-danger {
  background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
  color: white;
}

.btn-close {
  filter: invert(1);
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

/* Animaciones */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-card {
  animation: fadeInUp 0.6s ease-out;
}

/* Responsive */
@media (max-width: 576px) {
  .login-card {
    padding: 30px 20px;
    margin: 20px;
  }

  .login-title {
    font-size: 1.5rem;
  }
}

/* Efectos de fondo */
.login-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
