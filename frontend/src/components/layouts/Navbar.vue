<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-lg" style="position: relative; z-index: 1000;">
    <div class="container-fluid px-4">
      <!-- Logo y nombre -->
      <a class="navbar-brand fw-bold d-flex align-items-center text-white" href="#" style="font-size: 1.1rem;">
        <i class="bi bi-shield-check me-2" style="font-size: 1.4rem;"></i>
        <span class="d-none d-md-inline">SAFIR - Sistema de Administración y Fortalecimiento Integral Refugio</span>
        <span class="d-md-none">SAFIR</span>
      </a>

      <!-- Botón colapsable -->
      <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Menú principal -->
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav align-items-center">
          <li class="nav-item dropdown">
            <button class="btn btn-outline-light btn-sm dropdown-toggle d-flex align-items-center" data-bs-toggle="dropdown" id="userDropdown" aria-expanded="false" style="min-width: 100px;">
              <i class="bi bi-person-circle me-2"></i>
              <span class="d-none d-md-inline">{{ user?.username || 'Usuario' }}</span>
            </button>
            <ul class="dropdown-menu dropdown-menu-end shadow" aria-labelledby="userDropdown" style="min-width: 200px; z-index: 10000; position: absolute;">
              <li class="px-3 py-2 border-bottom">
                <div class="d-flex align-items-center">
                  <i class="bi bi-person-circle text-primary me-2" style="font-size: 1.5rem;"></i>
                  <div>
                    <div class="fw-bold">{{ user?.username || 'Usuario' }}</div>
                    <small class="text-muted">{{ getRoleDisplay(user?.rol) }}</small>
                  </div>
                </div>
              </li>
              <li><a class="dropdown-item py-2" href="#" @click.prevent="goToProfile">
                <i class="bi bi-person me-2"></i>Perfil
              </a></li>
              <li v-if="isAdmin"><a class="dropdown-item py-2" href="#" @click.prevent="goToUsers">
                <i class="bi bi-people me-2"></i>Gestión de Usuarios
              </a></li>
              <li><hr class="dropdown-divider my-1"></li>
              <li>
                <button class="dropdown-item text-danger py-2" @click="logout" style="border: none; background: none; width: 100%; text-align: left;">
                  <i class="bi bi-box-arrow-right me-2"></i>Cerrar Sesión
                </button>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuth } from '../../stores/auth.js'
import { onMounted } from 'vue'

const router = useRouter()
const { user, logout: authLogout, isAdmin } = useAuth()

onMounted(() => {
  // Asegurar que Bootstrap esté disponible y el dropdown funcione
  const dropdownElement = document.getElementById('userDropdown')
  if (dropdownElement) {
    // Forzar inicialización del dropdown
    if (typeof bootstrap !== 'undefined') {
      new bootstrap.Dropdown(dropdownElement)
    }
  }
})

function getRoleDisplay(rol) {
  const roles = {
    'admin': 'Administrador',
    'editor': 'Editor',
    'invitado': 'Invitado'
  }
  return roles[rol] || rol
}

function goToProfile() {
  // TODO: Implementar vista de perfil
  console.log('Ir a perfil')
}

function goToUsers() {
  router.push('/usuarios')
}

function logout() {
  // Limpiar estado de autenticación
  authLogout()
  // Forzar recarga completa de la página para asegurar limpieza del estado
  window.location.href = '/login'
}
</script>

<style scoped>
.navbar {
  backdrop-filter: blur(10px);
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.navbar-brand {
  transition: transform 0.2s ease;
}

.navbar-brand:hover {
  transform: scale(1.02);
}

.navbar-brand i {
  color: #ffffff;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

.btn-outline-light {
  border-color: rgba(255, 255, 255, 0.5);
  color: #ffffff;
  transition: all 0.3s ease;
}

.btn-outline-light:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: #ffffff;
  color: #ffffff;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.dropdown-menu {
  border: none;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-radius: 8px;
  overflow: hidden;
}

.dropdown-item {
  transition: background-color 0.2s ease;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}

.dropdown-item.text-danger:hover {
  background-color: #f8d7da;
}

.navbar-toggler {
  border: none;
  background: rgba(255, 255, 255, 0.1);
}

.navbar-toggler:focus {
  box-shadow: 0 0 0 0.2rem rgba(255, 255, 255, 0.25);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .navbar-brand {
    font-size: 1rem !important;
  }

  .dropdown-menu {
    min-width: 180px;
  }

  .btn-outline-light {
    padding: 0.25rem 0.5rem;
    font-size: 0.875rem;
  }
}
</style>
