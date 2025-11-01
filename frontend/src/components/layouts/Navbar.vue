<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
    <div class="container-fluid">
      <!-- Logo y nombre -->
      <a class="navbar-brand fw-bold d-flex align-items-center" href="#">
        <i class="bi bi-people-fill me-2"></i> SI-Población
      </a>

      <!-- Botón colapsable -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Menú principal -->
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <button class="btn btn-sm btn-outline-light dropdown-toggle" data-bs-toggle="dropdown" id="userDropdown">
              {{ user?.username || 'Usuario' }}
            </button>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
              <li><a class="dropdown-item" href="#" @click="goToProfile">
                <i class="bi bi-person me-2"></i>Perfil
              </a></li>
              <li v-if="isAdmin"><a class="dropdown-item" href="#" @click="goToUsers">
                <i class="bi bi-people me-2"></i>Gestión de Usuarios
              </a></li>
              <li><hr class="dropdown-divider"></li>
              <li>
                <button class="dropdown-item text-danger" @click="logout" style="border: none; background: none; width: 100%; text-align: left; padding: 0.375rem 0.75rem;">
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
.navbar-brand i {
  font-size: 1.2rem;
}
</style>
