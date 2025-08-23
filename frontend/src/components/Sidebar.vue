<template>
  <div class="sidebar bg-white border-end vh-100 shadow-sm p-3">
    <ul class="nav flex-column">
      <li v-for="link in links" :key="link.name" class="nav-item mb-2">
        <router-link
          class="nav-link d-flex align-items-center rounded py-2 px-3"
          :to="link.path"
          active-class="active-link"
        >
          <i :class="link.icon + ' me-2'"></i>
          <span>{{ link.name }}</span>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
const links = [
  { name: 'Dashboard', path: '/dashboard', icon: 'bi bi-speedometer2' },
  { name: 'Gestión Poblacional', path: '/poblacion', icon: 'bi bi-people-fill' },
  { name: 'Gestión Salud', path: '/salud', icon: 'bi bi-heart-pulse-fill' },
  { name: 'Gestión Social', path: '/social', icon: 'bi bi-hand-thumbs-up-fill' },
  { name: 'Encuestas', path: '/encuestas', icon: 'bi bi-ui-checks-grid' },
  { name: 'Reportes', path: '/reportes', icon: 'bi bi-bar-chart-fill' },
  { name: 'Usuarios y Roles', path: '/usuarios', icon: 'bi bi-person-gear' },
  { name: 'Auditoría', path: '/auditoria', icon: 'bi bi-shield-lock-fill' }
];
</script>

<style scoped>
.sidebar {
  width: 250px;
  min-width: 250px;
}

.nav-link {
  color: #555;
  transition: all 0.2s ease-in-out;
}

.nav-link:hover {
  background-color: #f8f9fa;
  color: #0d6efd;
}

.active-link {
  background-color: #0d6efd;
  color: white !important;
}

.active-link i {
  color: white !important;
}
</style>
