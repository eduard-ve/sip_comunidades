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
  
  // Servicios sociales
  export const socialService = {
    // Estados de programas
    getEstadosProgramas: () => api.get('/social/estados/'),
    createEstadoPrograma: (estadoData) => api.post('/social/estados/', estadoData),
    updateEstadoPrograma: (id, estadoData) => api.put(`/social/estados/${id}/`, estadoData),
    deleteEstadoPrograma: (id) => api.delete(`/social/estados/${id}/`),
  
    // Programas sociales
    getProgramasSociales: () => api.get('/social/programas/'),
    createProgramaSocial: (programaData) => api.post('/social/programas/', programaData),
    updateProgramaSocial: (id, programaData) => api.put(`/social/programas/${id}/`, programaData),
    deleteProgramaSocial: (id) => api.delete(`/social/programas/${id}/`),
  
    // Beneficiarios
    getBeneficiarios: () => api.get('/social/beneficiarios/'),
    createBeneficiario: (beneficiarioData) => api.post('/social/beneficiarios/', beneficiarioData),
    updateBeneficiario: (id, beneficiarioData) => api.put(`/social/beneficiarios/${id}/`, beneficiarioData),
    deleteBeneficiario: (id) => api.delete(`/social/beneficiarios/${id}/`),
  
    // Actividades sociales
    getActividadesSociales: () => api.get('/social/actividades/'),
    createActividadSocial: (actividadData) => api.post('/social/actividades/', actividadData),
    updateActividadSocial: (id, actividadData) => api.put(`/social/actividades/${id}/`, actividadData),
    deleteActividadSocial: (id) => api.delete(`/social/actividades/${id}/`),
  
    // Coberturas de programas
    getCoberturasProgramas: () => api.get('/social/coberturas/'),
    createCoberturaPrograma: (coberturaData) => api.post('/social/coberturas/', coberturaData),
    updateCoberturaPrograma: (id, coberturaData) => api.put(`/social/coberturas/${id}/`, coberturaData),
    deleteCoberturaPrograma: (id) => api.delete(`/social/coberturas/${id}/`),

    // Autoridades comunitarias
    getTiposAutoridad: () => api.get('/social/tipos-autoridad/'),
    createTipoAutoridad: (tipoData) => api.post('/social/tipos-autoridad/', tipoData),
    updateTipoAutoridad: (id, tipoData) => api.put(`/social/tipos-autoridad/${id}/`, tipoData),
    deleteTipoAutoridad: (id) => api.delete(`/social/tipos-autoridad/${id}/`),

    getRolesAutoridad: () => api.get('/social/roles-autoridad/'),
    createRolAutoridad: (rolData) => api.post('/social/roles-autoridad/', rolData),
    updateRolAutoridad: (id, rolData) => api.put(`/social/roles-autoridad/${id}/`, rolData),
    deleteRolAutoridad: (id) => api.delete(`/social/roles-autoridad/${id}/`),

    getAutoridadesComunitarias: () => api.get('/social/autoridades/'),
    createAutoridadComunitaria: (autoridadData) => api.post('/social/autoridades/', autoridadData),
    updateAutoridadComunitaria: (id, autoridadData) => api.put(`/social/autoridades/${id}/`, autoridadData),
    deleteAutoridadComunitaria: (id) => api.delete(`/social/autoridades/${id}/`),
    buscarPersonaPorCedula: (numeroIdentificacion) => api.get(`/social/autoridades/buscar-persona/?numero_identificacion=${numeroIdentificacion}`),
  }
  export default api