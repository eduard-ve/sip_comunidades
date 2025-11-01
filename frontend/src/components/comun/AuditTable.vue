<template>
  <div>
    <!-- Filtros -->
    <div class="card border-0 shadow-sm mb-4">
      <div class="card-body d-flex flex-wrap gap-3">
        <div class="flex-grow-1">
          <label class="form-label">Módulo</label>
          <select v-model="filters.module" class="form-select">
            <option value="">Todos</option>
            <option value="usuarios">Usuarios</option>
            <option value="reportes">Reportes</option>
            <option value="encuestas">Encuestas</option>
          </select>
        </div>
        <div class="flex-grow-1">
          <label class="form-label">Usuario</label>
          <input v-model="filters.user" type="text" class="form-control" placeholder="Buscar usuario..." />
        </div>
        <div>
          <label class="form-label">Fecha</label>
          <input v-model="filters.date" type="date" class="form-control" />
        </div>
        <div class="align-self-end">
          <button class="btn btn-outline-primary" @click="resetFilters">
            <i class="bi bi-arrow-counterclockwise"></i> Limpiar
          </button>
        </div>
      </div>
    </div>

    <!-- Tabla -->
    <div class="card border-0 shadow-sm">
      <div class="card-body table-responsive">
        <table class="table table-hover table-striped align-middle">
          <thead class="table-dark">
            <tr>
              <th>ID</th>
              <th>Módulo</th>
              <th>Usuario</th>
              <th>Acción</th>
              <th>Fecha</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="evento in filteredEvents" :key="evento.id">
              <td>{{ evento.id }}</td>
              <td>{{ evento.module }}</td>
              <td>{{ evento.user }}</td>
              <td>
                <div class="d-flex align-items-center">
                  <i :class="getActionIcon(evento.action)" class="me-2"></i>
                  {{ evento.action }}
                </div>
              </td>
              <td>{{ evento.date }}</td>
              <td>
                <button class="btn btn-sm btn-outline-info" @click="$emit('view-details', evento)">
                  <i class="bi bi-eye"></i> Ver
                </button>
              </td>
            </tr>
            <tr v-if="!filteredEvents.length">
              <td colspan="6" class="text-center text-muted py-4">Sin registros</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue"

const props = defineProps({
  events: { type: Array, required: true }
})

const filters = ref({
  module: "",
  user: "",
  date: ""
})

const filteredEvents = computed(() => {
  return props.events.filter(e => {
    const matchModule = !filters.value.module || e.module === filters.value.module
    const matchUser = !filters.value.user || e.user.toLowerCase().includes(filters.value.user.toLowerCase())
    const matchDate = !filters.value.date || e.date === filters.value.date
    return matchModule && matchUser && matchDate
  })
})

function resetFilters() {
  filters.value = { module: "", user: "", date: "" }
}

function getActionIcon(action) {
  if (action.toLowerCase().includes('creación') || action.toLowerCase().includes('creado')) {
    return 'fas fa-plus-circle text-success'
  } else if (action.toLowerCase().includes('eliminación') || action.toLowerCase().includes('eliminado')) {
    return 'fas fa-trash text-danger'
  } else if (action.toLowerCase().includes('modificación') || action.toLowerCase().includes('actualizado')) {
    return 'fas fa-edit text-warning'
  } else {
    return 'fas fa-info-circle text-info'
  }
}
</script>
