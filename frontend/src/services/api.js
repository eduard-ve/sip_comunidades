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
  getGruposEtnicos: () => api.get('/poblacion/grupos_etnicos/'),
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
  getEstadisticas: () => api.get('/poblacion/estadisticas/estadisticas/'),
  getDistribucionEdad: () => api.get('/poblacion/estadisticas/distribucion_edad/'),
  getDistribucionEducativa: () => api.get('/poblacion/estadisticas/distribucion_educativa/'),
  getDistribucionGenero: () => api.get('/poblacion/estadisticas/distribucion_genero/'),
  getTopOcupaciones: () => api.get('/poblacion/estadisticas/top_ocupaciones/'),
  getLenguasMaternas: () => api.get('/poblacion/estadisticas/lenguas_maternas/'),
  getLenguasPorGrupoEtnico: (grupoId) => api.get(`/poblacion/estadisticas/${grupoId}/lenguas_por_grupo_etnico/`),
  getDashboardData: () => api.get('/poblacion/estadisticas/dashboard/'),
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

    // Actividades comunitarias
    getTiposActividad: () => api.get('/social/tipos-actividad/'),
    createTipoActividad: (tipoData) => api.post('/social/tipos-actividad/', tipoData),
    updateTipoActividad: (id, tipoData) => api.put(`/social/tipos-actividad/${id}/`, tipoData),
    deleteTipoActividad: (id) => api.delete(`/social/tipos-actividad/${id}/`),

    getEstadosActividad: () => api.get('/social/estados-actividad/'),
    createEstadoActividad: (estadoData) => api.post('/social/estados-actividad/', estadoData),
    updateEstadoActividad: (id, estadoData) => api.put(`/social/estados-actividad/${id}/`, estadoData),
    deleteEstadoActividad: (id) => api.delete(`/social/estados-actividad/${id}/`),

    getActividadesComunitarias: () => api.get('/social/actividades-comunitarias/'),
    createActividadComunitaria: (actividadData) => api.post('/social/actividades-comunitarias/', actividadData),
    updateActividadComunitaria: (id, actividadData) => api.put(`/social/actividades-comunitarias/${id}/`, actividadData),
    deleteActividadComunitaria: (id) => api.delete(`/social/actividades-comunitarias/${id}/`),

    // Funciones especiales para actividades
    registrarAsistencia: (actividadId, asistenciaData) => api.post(`/social/actividades-comunitarias/${actividadId}/registrar-asistencia/`, asistenciaData),
    getEstadisticasActividad: (actividadId) => api.get(`/social/actividades-comunitarias/${actividadId}/estadisticas/`),
    getCalendarioActividades: (params) => api.get('/social/actividades-comunitarias/calendario/', { params }),

    // Asistencias
    getAsistencias: () => api.get('/social/asistencias-actividad/'),
    getAsistenciasPorActividad: (actividadId) => api.get('/social/asistencias-actividad/por-actividad/', { params: { actividad_id: actividadId } }),
    createAsistencia: (asistenciaData) => api.post('/social/asistencias-actividad/', asistenciaData),
    updateAsistencia: (id, asistenciaData) => api.put(`/social/asistencias-actividad/${id}/`, asistenciaData),
    deleteAsistencia: (id) => api.delete(`/social/asistencias-actividad/${id}/`),
    }
  
  // Servicios de auditoría
  export const auditService = {
    getAuditLogs: () => api.get('/auditoria/'),
    getAuditStats: () => api.get('/auditoria/stats/'),
  }
  
  export default api