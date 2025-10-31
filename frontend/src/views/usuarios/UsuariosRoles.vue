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
      <div class="roles-filter">
        <select class="form-select form-select-sm" v-model="filterRole">
          <option value="">Todos los roles</option>
          <option v-for="r in roles" :key="r" :value="r">{{ r }}</option>
        </select>
      </div>
      <div v-if="error" class="alert alert-danger mt-2">
        {{ error }}
      </div>
      <div v-if="loading" class="text-center mt-2">
        <div class="spinner-border spinner-border-sm" role="status"></div>
        Cargando usuarios...
      </div>
    </template>

    <!-- Personalización de las celdas de la tabla -->
    <template #table-cell="{ column, row }">
      <template v-if="column.key === 'acciones'">
        <div class="table-actions">
          <button class="btn btn-sm btn-outline-primary" @click.stop="openForm(row)">
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-sm btn-outline-danger" @click.stop="deleteUser(row.id)">
            <i class="bi bi-trash"></i>
          </button>
        </div>
      </template>
      <template v-else-if="column.key === 'is_active'">
        <span :class="`estado-badge estado-${row.is_active ? 'activo' : 'inactivo'}`">
          {{ row.is_active ? 'Activo' : 'Inactivo' }}
        </span>
      </template>
      <template v-else-if="column.key === 'rol'">
        <span :class="`rol-badge rol-${row.rol.toLowerCase()}`">
          {{ row.rol }}
        </span>
      </template>
      <template v-else>
        {{ row[column.key] }}
      </template>
    </template>

    <!-- Footer de la tabla -->
    <template #table-footer>
      <div class="table-footer">
        <button class="btn btn-sm btn-secondary" @click="onExport">Exportar lista</button>
      </div>
    </template>

    <!-- Modal -->
    <div v-if="showForm" class="modal d-block" style="z-index: 1055;">
      <div class="modal-dialog modal-lg">
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
    <div v-if="showForm" class="modal-backdrop fade show" style="z-index: 1050;"></div>
  </BaseModule>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import BaseModule from '../../components/comun/BaseModule.vue'
import UserForm from '../../components/formularios/UserForm.vue'
import { userService } from '../../services/api.js'
import '../../assets/css/UsuariosRoles.css'

const roles = ['admin', 'editor', 'invitado']

// Estado reactivo
const users = ref([])
const loading = ref(false)
const error = ref('')
const filterRole = ref('')
const showForm = ref(false)
const selectedUser = ref(null)

// KPIs calculados
const kpis = computed(() => [
  {
    title: 'Total Usuarios',
    value: users.value.length,
    icon: 'bi bi-people-fill',
    change: '+10',
    color: '#0d6efd'
  },
  {
    title: 'Roles Activos',
    value: users.value.filter(u => u.is_active).length,
    icon: 'bi-shield-lock',
    change: '+5'
  },
  {
    title: 'Roles Inactivos',
    value: users.value.filter(u => !u.is_active).length,
    icon: 'bi-shield-lock',
    change: '-2',
    color: '#6c757d'
  }
])

// Charts
const charts = computed(() => ({
  left: {
    id: 'rolesChart',
    type: 'bar',
    title: 'Usuarios por rol',
    data: {
      labels: ['admin', 'editor', 'invitado'],
      datasets: [{
        label: 'Usuarios',
        data: [
          users.value.filter(u => u.rol === 'admin').length,
          users.value.filter(u => u.rol === 'editor').length,
          users.value.filter(u => u.rol === 'invitado').length
        ],
        backgroundColor: '#0d6efd'
      }]
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
}))

// Tabla
const table = computed(() => ({
  columns: [
    { key: 'first_name', label: 'Nombre' },
    { key: 'username', label: 'Usuario' },
    { key: 'email', label: 'Email' },
    { key: 'rol', label: 'Rol' },
    { key: 'is_active', label: 'Estado' },
    { key: 'acciones', label: 'Acciones' }
  ],
  rows: filteredUsers.value
}))

const filteredUsers = computed(() => {
  if (!filterRole.value) return users.value
  return users.value.filter(u => u.rol === filterRole.value)
})

// Funciones
async function fetchUsers() {
  loading.value = true
  error.value = ''
  try {
    const response = await userService.getUsers()
    users.value = response.data
  } catch (err) {
    console.error('Error fetching users:', err)
    error.value = 'Error al cargar los usuarios'
  } finally {
    loading.value = false
  }
}

function openForm(user = null) {
  selectedUser.value = user ? { ...user } : {
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    telefono: '',
    rol: 'invitado',
    password: '',
    password2: ''
  }
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  selectedUser.value = null
}

async function handleSubmit(userData) {
  try {
    if (userData.id) {
      // Actualizar usuario existente
      await userService.updateUser(userData.id, userData)
    } else {
      // Crear nuevo usuario
      await userService.createUser(userData)
    }
    await fetchUsers() // Recargar lista
    closeForm()
  } catch (err) {
    console.error('Error saving user:', err)
    // Mostrar mensaje de error más específico
    if (err.response?.data) {
      const errors = Object.values(err.response.data).flat().join('\n')
      alert(`Error al guardar el usuario:\n${errors}`)
    } else {
      alert('Error al guardar el usuario')
    }
  }
}

async function deleteUser(id) {
  if (confirm('¿Seguro que deseas eliminar este usuario?')) {
    try {
      await userService.deleteUser(id)
      await fetchUsers() // Recargar lista
    } catch (err) {
      console.error('Error deleting user:', err)
      alert('Error al eliminar el usuario')
    }
  }
}

function onExport() {
  alert('Exportar lista de usuarios - funcionalidad no implementada')
}

// Cargar datos al montar el componente
onMounted(() => {
  fetchUsers()
})
</script>
