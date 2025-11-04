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
            <h1 class="welcome-title">Welcome SAFIR</h1>
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
            <h2 class="login-title">LOGIN</h2>
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

            <div class="mb-3 d-flex justify-content-between align-items-center">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" id="rememberMe">
                <label class="form-check-label" for="rememberMe">
                  Remember Me
                </label>
              </div>
              <a href="#" class="text-decoration-none">Lost your password?</a>
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

          <div class="text-center mb-3">
            <a href="#" class="text-decoration-none me-3">Terms of Service</a>
            <a href="#" class="text-decoration-none">Privacy Policy</a>
          </div>

          <div class="social-login">
            <p class="text-muted mb-3">Or sign in with</p>
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

// Load theme preference from localStorage
onMounted(() => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    isDarkTheme.value = savedTheme === 'dark';
  } else {
    // Default to dark theme
    isDarkTheme.value = true;
    localStorage.setItem('theme', 'dark');
  }
});

// Toggle theme
function toggleTheme() {
  isDarkTheme.value = !isDarkTheme.value;
  localStorage.setItem('theme', isDarkTheme.value ? 'dark' : 'light');
}

// Show login form
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

<style scoped>
.login-container {
  min-height: 100vh;
  background: #0A1629;
  position: relative;
  overflow: hidden;
  transition: background-color 0.3s ease;
}

.login-container:not(.dark-theme) {
  background: #ffffff;
}

.theme-toggle {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
  backdrop-filter: blur(10px);
}

.login-container:not(.dark-theme) .theme-toggle {
  background: rgba(0, 0, 0, 0.1);
  border-color: rgba(0, 0, 0, 0.2);
  color: #333;
}

.theme-toggle:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

.login-container:not(.dark-theme) .theme-toggle:hover {
  background: rgba(0, 0, 0, 0.2);
}

.login-wrapper {
  display: flex;
  min-height: 100vh;
}

.left-panel {
  flex: 1;
  background: url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80') center/cover no-repeat;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 60px;
  position: relative;
  overflow: hidden;
}

.welcome-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.3) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.welcome-content {
  text-align: center;
  color: white;
  z-index: 2;
  max-width: 500px;
}

.welcome-title {
  font-size: 4rem;
  font-weight: 700;
  margin-bottom: 20px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
  letter-spacing: -1px;
}

.welcome-subtitle {
  font-size: 1.5rem;
  font-weight: 300;
  margin-bottom: 15px;
  opacity: 0.9;
}

.welcome-description {
  font-size: 1.1rem;
  opacity: 0.8;
  line-height: 1.6;
}

.login-container:not(.dark-theme) .left-panel {
  background: url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80') center/cover no-repeat;
}

/* Remove old rotating background effect */

/* Remove old brand and features sections */

.right-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: #0A1629;
}

.login-container:not(.dark-theme) .right-panel {
  background: #ffffff;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 450px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.login-container:not(.dark-theme) .login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.login-logo {
  margin-bottom: 20px;
}

.login-logo i {
  font-size: 3rem;
  color: #6f42c1;
}

.login-container:not(.dark-theme) .login-logo i {
  color: #667eea;
}

.login-title {
  color: #2c3e50;
  font-weight: 700;
  margin-bottom: 8px;
  font-size: 1.8rem;
}

/* Remove old light theme styles for removed sections */

/* Keep login title color consistent */

.form-label {
  color: #2c3e50;
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
  background: #fff;
  border-color: #dee2e6;
  color: #495057;
  border-radius: 8px;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
  border-left: none;
}

.input-group:focus-within .input-group-text {
  border-color: #667eea;
  background: #e3f2fd;
}

.btn-primary {
  background: linear-gradient(135deg, #6f42c1 0%, #5a32a3 100%);
  border: none;
  padding: 12px 24px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.login-container:not(.dark-theme) .btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #5a67d8 100%);
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #5a32a3 0%, #4c2889 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(111, 66, 193, 0.3);
}

.login-container:not(.dark-theme) .btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #5a67d8 0%, #4c51bf 100%);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
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

/* Dark theme text visibility adjustments */
.login-container.dark-theme .text-muted {
  color: #cccccc !important;
}

/* Social login styles */
.social-login {
  text-align: center;
}

.social-icons {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.social-icons .btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.social-icons .btn i {
  font-size: 1.2rem;
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
@media (max-width: 768px) {
  .login-wrapper {
    flex-direction: column;
  }

  .left-panel {
    flex: none;
    min-height: 50vh;
    padding: 40px 20px;
  }

  .welcome-title {
    font-size: 3rem;
  }

  .welcome-subtitle {
    font-size: 1.2rem;
  }

  .welcome-description {
    font-size: 0.9rem;
  }

  .right-panel {
    flex: none;
    min-height: 50vh;
    padding: 20px;
  }

  .login-card {
    padding: 30px 20px;
    margin: 20px;
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(30px);
  }

  .login-title {
    font-size: 1.5rem;
  }

  .theme-toggle {
    top: 10px;
    right: 10px;
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
}

@media (max-width: 576px) {
  .left-panel {
    padding: 30px 15px;
  }

  .welcome-title {
    font-size: 2.5rem;
  }

  .login-card {
    padding: 25px 15px;
    margin: 15px;
  }
}

/* Efectos de fondo */
@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
