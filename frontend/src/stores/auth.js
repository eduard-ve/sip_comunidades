import { ref, computed } from 'vue'
import { authService } from '../services/api.js'
import { jwtDecode } from 'jwt-decode'
import axios from 'axios'

const user = ref(null)
const isAuthenticated = ref(false)
const loading = ref(false)

export const useAuth = () => {
  // Decodificar token JWT para obtener información del usuario
  const decodeToken = (token) => {
    try {
      return jwtDecode(token)
    } catch (error) {
      console.error('Error decodificando token:', error)
      return null
    }
  }

  // Inicializar estado desde localStorage
  const initAuth = () => {
    // Limpiar estado inicial
    user.value = null
    isAuthenticated.value = false

    const token = localStorage.getItem('access_token')
    if (token) {
      const decoded = decodeToken(token)
      if (decoded && decoded.exp * 1000 > Date.now()) {
        user.value = {
          username: decoded.username,
          rol: decoded.rol
        }
        isAuthenticated.value = true
      } else {
        // Token expirado o inválido, limpiar
        logout()
      }
    }
  }

  const login = async (credentials) => {
    loading.value = true
    try {
      const response = await authService.login(credentials)
      const token = response.data.access
      localStorage.setItem('access_token', token)
      localStorage.setItem('refresh_token', response.data.refresh)

      // Set axios default header
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

      // Decodificar token para obtener información del usuario
      const decoded = decodeToken(token)
      if (decoded) {
        user.value = {
          username: decoded.username,
          rol: decoded.rol
        }
      }

      isAuthenticated.value = true
      return response.data
    } catch (error) {
      throw error
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    user.value = null
    isAuthenticated.value = false
  }

  const getProfile = async () => {
    try {
      const response = await authService.getProfile()
      user.value = response.data
      return response.data
    } catch (error) {
      // Si falla, hacer logout
      logout()
      throw error
    }
  }

  // Verificar si el usuario tiene un rol específico
  const hasRole = (requiredRoles) => {
    if (!user.value || !user.value.rol) return false
    if (Array.isArray(requiredRoles)) {
      return requiredRoles.includes(user.value.rol)
    }
    return user.value.rol === requiredRoles
  }

  // Verificar si es admin
  const isAdmin = () => hasRole('admin')

  // Verificar si es editor o superior
  const isEditor = () => hasRole(['admin', 'editor'])

  // Verificar si es invitado o superior
  const isInvitado = () => hasRole(['admin', 'editor', 'invitado'])

  return {
    user: computed(() => user.value),
    isAuthenticated: computed(() => isAuthenticated.value),
    loading: computed(() => loading.value),
    login,
    logout,
    getProfile,
    initAuth,
    hasRole,
    isAdmin,
    isEditor,
    isInvitado
  }
}