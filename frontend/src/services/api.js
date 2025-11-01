import axios from 'axios'

// Configuración base de la API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

// Crear instancia de axios con configuración base
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para agregar token de autenticación
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Servicios de autenticación
export const authService = {
  login: (credentials) => api.post('/usuarios/login/', credentials),
  register: (userData) => api.post('/usuarios/registro/', userData),
  refreshToken: (refreshToken) => api.post('/usuarios/token/refresh/', { refresh: refreshToken }),
  getProfile: () => api.get('/usuarios/perfil/'),
}

// Servicios de usuarios
export const userService = {
  getUsers: () => api.get('/usuarios/usuarios/'),
  createUser: (userData) => api.post('/usuarios/registro/', userData),
  updateUser: (id, userData) => api.put(`/usuarios/usuarios/${id}/`, userData),
  deleteUser: (id) => api.delete(`/usuarios/usuarios/${id}/`),
}

// Servicios de población
export const poblacionService = {
  // Personas
  getPersonas: () => api.get('/poblacion/personas/'),
  createPersona: (personaData) => api.post('/poblacion/personas/', personaData),
  updatePersona: (id, personaData) => api.put(`/poblacion/personas/${id}/`, personaData),
  deletePersona: (id) => api.delete(`/poblacion/personas/${id}/`),

  // Catálogos
  getTiposIdentificacion: () => api.get('/poblacion/tipos_identificacion/'),
  getNivelesEducativos: () => api.get('/poblacion/niveles_educativos/'),
  getOcupaciones: () => api.get('/poblacion/ocupaciones/'),
  getGruposFamiliares: () => api.get('/poblacion/grupos_familiares/'),
  getEstadosCiviles: () => api.get('/poblacion/estados_civiles/'),
  getLenguas: () => api.get('/poblacion/lenguas/'),
  getTiposRelaciones: () => api.get('/poblacion/tipos_relaciones/'),

  // Relaciones familiares
  getRelacionesFamiliares: () => api.get('/poblacion/relaciones_familiares/'),
  createRelacionFamiliar: (relacionData) => api.post('/poblacion/relaciones_familiares/', relacionData),
  updateRelacionFamiliar: (id, relacionData) => api.put(`/poblacion/relaciones_familiares/${id}/`, relacionData),
  deleteRelacionFamiliar: (id) => api.delete(`/poblacion/relaciones_familiares/${id}/`),

  // Estadísticas de población
  getPopulationStats: () => api.get('/poblacion/stats/'),
}
export default api