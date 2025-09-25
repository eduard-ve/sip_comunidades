<template>
  <BaseModule
    title="Usuarios y Roles"
    :breadcrumbs="breadcrumbs"
    :kpis="kpis"
    :charts="charts"
    :table="{ columns: table.columns, rows: filteredUsers }"
    searchPlaceholder="Buscar usuario…"
    :showCreate="true"
    :showExport="false"
    @create="openForm()"
  >
    <!-- Filtro de roles -->
    <template #extra>
      <select class="form-select form-select-sm me-2" v-model="filterRole" style="max-width: 180px;">
        <option value="">Todos los roles</option>
        <option v-for="r in roles" :key="r" :value="r">{{ r }}</option>
      </select>
    </template>

    <!-- Personalización de las celdas de la tabla -->
    <template #table-cell="{ column, row }">
      <template v-if="column.key === 'acciones'">
        <button class="btn btn-sm btn-outline-primary me-1" @click.stop="openForm(row)">
          <i class="bi bi-pencil"></i>
        </button>
        <button class="btn btn-sm btn-outline-danger" @click.stop="deleteUser(row.id)">
          <i class="bi bi-trash"></i>
        </button>
      </template>
      <template v-else>
        {{ row[column.key] }}
      </template>
    </template>

    <!-- Footer de la tabla -->
    <template #table-footer>
      <div class="d-flex justify-content-end mt-2">
        <button class="btn btn-sm btn-secondary" @click="onExport">Exportar lista</button>
      </div>
    </template>

    <!-- Modal -->
    <div v-if="showForm" class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ selectedUser?.id ? 'Editar Usuario' : 'Nuevo Usuario' }}</h5>
            <button type="button" class="btn-close" @click="closeForm"></button>
          </div>
          <div class="modal-body">
            <UserForm
              :model-value="selectedUser"
              @update:modelValue="selectedUser = $event"
              @submit="handleSubmit"
              @cancel="closeForm"
              :roles="roles"
            />
          </div>
        </div>
      </div>
    </div>
    <div v-if="showForm" class="modal-backdrop fade show"></div>
  </BaseModule>
</template>

<script setup>
import { ref, computed } from 'vue'
import BaseModule from '../../components/comun/BaseModule.vue'
import UserForm from '../../components/formularios/UserForm.vue'

const roles = ['Admin', 'Editor', 'Invitado']


// KPIs
const kpis = [
  { title: 'Total Usuarios', value: 120, icon: 'bi bi-people-fill', change: '100', color: '#0d6efd' },
  { title: 'Roles Activos', value: 100, icon: 'bi-shield-lock', change: '80' },
  { title: 'Roles Inactivos', value: 20, icon: 'bi-shield-lock', change: '20', color: '#0d6efd' }
]

// Charts
const charts = {
  left: {
    id: 'rolesChart',
    type: 'bar',
    title: 'Usuarios por rol',
    data: {
      labels: ['Admin', 'Editor', 'Invitado'],
      datasets: [{ label: 'Usuarios', data: [5, 60, 55], backgroundColor: '#0d6efd' }]
    },
    options: { responsive: true, plugins: { legend: { display: false } } }
  },
  right: {
    id: 'loginChart',
    type: 'line',
    title: 'Historial de inicio de sesión',
    data: {
      labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie'],
      datasets: [{ label: 'Inicios de sesión', data: [12, 15, 9, 20, 18], borderColor: '#198754', fill: false }]
    },
    options: { responsive: true }
  }
}

// Tabla
const table = {
  columns: [
    { key: 'nombre', label: 'Nombre' },
    { key: 'email', label: 'Email' },
    { key: 'rol', label: 'Rol' },
    { key: 'estado', label: 'Estado' },
    { key: 'acciones', label: 'Acciones' } 
  ],
  rows: [
    { id: 1, nombre: 'Ana Pérez', email: 'ana@example.com', rol: 'Admin', estado: 'Sí' },
    { id: 2, nombre: 'Juan Gómez', email: 'juan@example.com', rol: 'Editor', estado: 'No' },
    { id :3, nombre: 'Eduard', email: 'eduardvelez1@gmail.com', rol: 'Admin', estado: 'Sí' }
  ]
}

const filterRole = ref('')
const showForm = ref(false)
const selectedUser = ref(null)

const filteredUsers = computed(() => {
  if (!filterRole.value) return table.rows
  return table.rows.filter(u => u.rol === filterRole.value)
})

// Funciones
function openForm(user = null) {
  selectedUser.value = user ? { ...user } : { nombre: '', email: '', rol: '', estado: true }
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  selectedUser.value = null
}

function handleSubmit(userData) {
  if (userData.id) {
    // Editar usuario
    const idx = table.rows.findIndex(u => u.id === userData.id)
    if (idx !== -1) table.rows[idx] = { ...userData }
  } else {
    // Nuevo usuario
    userData.id = table.rows.length + 1
    table.rows.push({ ...userData })
  }
  closeForm()
}

function deleteUser(id) {
  if (confirm('¿Seguro que deseas eliminar este usuario?')) {
    const idx = table.rows.findIndex(u => u.id === id)
    if (idx !== -1) table.rows.splice(idx, 1)
  }
}

function onExport() {
  alert('Exportar lista de usuarios')// funcionalidad de exportación no implementada
}
</script>
