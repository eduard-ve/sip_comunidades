import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuth } from './auth.js'
import { authService } from '../services/api.js'

// Mock del servicio API
vi.mock('../services/api.js', () => ({
  authService: {
    login: vi.fn(),
    register: vi.fn(),
    refreshToken: vi.fn(),
    getProfile: vi.fn()
  }
}))

// Mock de jwt-decode
vi.mock('jwt-decode', () => ({
  jwtDecode: vi.fn()
}))

// Mock de axios
vi.mock('axios', () => ({
  default: {
    defaults: {
      headers: {
        common: {}
      }
    }
  }
}))

describe('useAuth', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    vi.clearAllMocks()
  })

  it('initializes with no user when no token exists', () => {
    const { user, isAuthenticated } = useAuth()
    expect(user.value).toBeNull()
    expect(isAuthenticated.value).toBe(false)
  })

  it('initializes with user when valid token exists', async () => {
    const mockDecoded = { username: 'testuser', rol: 'admin', exp: Date.now() / 1000 + 3600 }
    const { jwtDecode } = await import('jwt-decode')
    jwtDecode.mockReturnValue(mockDecoded)
    
    localStorage.setItem('access_token', 'valid-token')
    
    const { user, isAuthenticated, initAuth } = useAuth()
    initAuth()
    
    expect(user.value).toBeTruthy()
    expect(user.value.username).toBe('testuser')
    expect(isAuthenticated.value).toBe(true)
  })

  it('clears user when token is expired', async () => {
    const mockDecoded = { username: 'testuser', rol: 'admin', exp: Date.now() / 1000 - 3600 }
    const { jwtDecode } = await import('jwt-decode')
    jwtDecode.mockReturnValue(mockDecoded)
    
    localStorage.setItem('access_token', 'expired-token')
    
    const { user, isAuthenticated, initAuth } = useAuth()
    initAuth()
    
    expect(user.value).toBeNull()
    expect(isAuthenticated.value).toBe(false)
    expect(localStorage.getItem('access_token')).toBeNull()
  })

  it('logs in successfully', async () => {
    const mockResponse = {
      data: {
        access: 'new-access-token',
        refresh: 'new-refresh-token'
      }
    }
    const mockDecoded = { username: 'testuser', rol: 'admin', exp: Date.now() / 1000 + 3600 }
    
    authService.login.mockResolvedValue(mockResponse)
    const { jwtDecode } = await import('jwt-decode')
    jwtDecode.mockReturnValue(mockDecoded)
    
    const { login, user, isAuthenticated } = useAuth()
    const result = await login({ username: 'testuser', password: 'password' })
    
    expect(authService.login).toHaveBeenCalledWith({ username: 'testuser', password: 'password' })
    expect(localStorage.getItem('access_token')).toBe('new-access-token')
    expect(localStorage.getItem('refresh_token')).toBe('new-refresh-token')
    expect(user.value.username).toBe('testuser')
    expect(isAuthenticated.value).toBe(true)
    expect(result).toEqual(mockResponse.data)
  })

  it('handles login error', async () => {
    const mockError = new Error('Invalid credentials')
    authService.login.mockRejectedValue(mockError)
    
    const { login } = useAuth()
    
    await expect(login({ username: 'testuser', password: 'wrong' })).rejects.toThrow()
    expect(localStorage.getItem('access_token')).toBeNull()
  })

  it('logs out successfully', () => {
    localStorage.setItem('access_token', 'token')
    localStorage.setItem('refresh_token', 'refresh')
    
    const { logout, user, isAuthenticated } = useAuth()
    logout()
    
    expect(localStorage.getItem('access_token')).toBeNull()
    expect(localStorage.getItem('refresh_token')).toBeNull()
    expect(user.value).toBeNull()
    expect(isAuthenticated.value).toBe(false)
  })

  it('gets profile successfully', async () => {
    const mockProfile = { id: 1, username: 'testuser', email: 'test@test.com' }
    authService.getProfile.mockResolvedValue({ data: mockProfile })
    
    const { getProfile, user } = useAuth()
    const result = await getProfile()
    
    expect(authService.getProfile).toHaveBeenCalled()
    expect(user.value).toEqual(mockProfile)
    expect(result).toEqual(mockProfile)
  })

  it('logs out on profile error', async () => {
    const mockError = new Error('Unauthorized')
    authService.getProfile.mockRejectedValue(mockError)
    
    const { getProfile } = useAuth()
    
    await expect(getProfile()).rejects.toThrow()
    expect(localStorage.getItem('access_token')).toBeNull()
  })

  it('checks hasRole correctly', async () => {
    const mockResponse = {
      data: {
        access: 'token',
        refresh: 'refresh'
      }
    }
    const mockDecoded = { username: 'testuser', rol: 'admin', exp: Date.now() / 1000 + 3600 }
    
    authService.login.mockResolvedValue(mockResponse)
    const { jwtDecode } = await import('jwt-decode')
    jwtDecode.mockReturnValue(mockDecoded)
    
    const { login, hasRole } = useAuth()
    await login({ username: 'testuser', password: 'password' })
    
    expect(hasRole(['admin', 'editor'])).toBe(true)
    expect(hasRole('admin')).toBe(true)
    expect(hasRole('editor')).toBe(false)
  })

  it('returns false for hasRole when no user', () => {
    // Asegurarse de que no hay token en localStorage
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    
    // Crear una nueva instancia de useAuth
    const { hasRole, logout, initAuth } = useAuth()
    
    // Limpiar estado usando logout primero
    logout()
    
    // Luego usar initAuth que resetea user.value
    initAuth()
    
    // Verificar que hasRole retorna false cuando no hay usuario
    // hasRole verifica: if (!user.value || !user.value.rol) return false
    expect(hasRole('admin')).toBe(false)
    expect(hasRole(['admin'])).toBe(false)
  })

  it('checks isAdmin correctly', async () => {
    const mockResponse = {
      data: {
        access: 'token',
        refresh: 'refresh'
      }
    }
    const mockDecoded = { username: 'admin', rol: 'admin', exp: Date.now() / 1000 + 3600 }
    
    authService.login.mockResolvedValue(mockResponse)
    const { jwtDecode } = await import('jwt-decode')
    jwtDecode.mockReturnValue(mockDecoded)
    
    const { login, isAdmin } = useAuth()
    await login({ username: 'admin', password: 'password' })
    
    expect(isAdmin()).toBe(true)
    
    // Test con editor
    const mockDecodedEditor = { username: 'user', rol: 'editor', exp: Date.now() / 1000 + 3600 }
    jwtDecode.mockReturnValue(mockDecodedEditor)
    authService.login.mockResolvedValue(mockResponse)
    await login({ username: 'user', password: 'password' })
    
    expect(isAdmin()).toBe(false)
  })

  it('checks isEditor correctly', async () => {
    const mockResponse = {
      data: {
        access: 'token',
        refresh: 'refresh'
      }
    }
    const mockDecoded = { username: 'editor', rol: 'editor', exp: Date.now() / 1000 + 3600 }
    
    authService.login.mockResolvedValue(mockResponse)
    const { jwtDecode } = await import('jwt-decode')
    jwtDecode.mockReturnValue(mockDecoded)
    
    const { login, isEditor } = useAuth()
    await login({ username: 'editor', password: 'password' })
    
    expect(isEditor()).toBe(true)
    
    // Test con invitado
    const mockDecodedInvitado = { username: 'user', rol: 'invitado', exp: Date.now() / 1000 + 3600 }
    jwtDecode.mockReturnValue(mockDecodedInvitado)
    authService.login.mockResolvedValue(mockResponse)
    await login({ username: 'user', password: 'password' })
    
    expect(isEditor()).toBe(false)
  })

  it('handles loading state during login', async () => {
    const mockResponse = {
      data: {
        access: 'token',
        refresh: 'refresh'
      }
    }
    const mockDecoded = { username: 'testuser', rol: 'admin', exp: Date.now() / 1000 + 3600 }
    
    authService.login.mockImplementation(() => new Promise(resolve => setTimeout(() => resolve(mockResponse), 100)))
    const { jwtDecode } = await import('jwt-decode')
    jwtDecode.mockReturnValue(mockDecoded)
    
    const { login, loading } = useAuth()
    const loginPromise = login({ username: 'test', password: 'pass' })
    
    expect(loading.value).toBe(true)
    
    await loginPromise
    
    expect(loading.value).toBe(false)
  })
})
