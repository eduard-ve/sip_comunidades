import { ref, computed } from 'vue'
import { authService } from '../services/api.js'

const user = ref(null)
const isAuthenticated = ref(false)
const loading = ref(false)

export const useAuth = () => {
  // Inicializar estado desde localStorage
  const initAuth = () => {
    const token = localStorage.getItem('access_token')
    if (token) {
      isAuthenticated.value = true
      // Aquí podrías hacer una llamada para obtener el perfil del usuario
    }
  }

  const login = async (credentials) => {
    loading.value = true
    try {
      const response = await authService.login(credentials)
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
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

  return {
    user: computed(() => user.value),
    isAuthenticated: computed(() => isAuthenticated.value),
    loading: computed(() => loading.value),
    login,
    logout,
    getProfile,
    initAuth
  }
}