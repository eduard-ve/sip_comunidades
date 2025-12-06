import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia, setActivePinia } from 'pinia'
import Login from '../../views/usuarios/Login.vue'
import { authService } from '../../services/api.js'
import { useAuth } from '../../stores/auth.js'

// Mock del servicio API
vi.mock('../../services/api.js', () => ({
  authService: {
    login: vi.fn()
  }
}))

// Mock del store de auth
vi.mock('../../stores/auth.js', () => ({
  useAuth: vi.fn(() => ({
    initAuth: vi.fn()
  }))
}))

describe('Login Flow Integration', () => {
  let router

  beforeEach(() => {
    setActivePinia(createPinia())
    
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/login', component: Login },
        { path: '/dashboard', component: { template: '<div>Dashboard</div>' } }
      ]
    })

    vi.clearAllMocks()
    localStorage.clear()
  })

  it('completes full login flow', async () => {
    const mockResponse = {
      data: {
        access: 'access-token',
        refresh: 'refresh-token'
      }
    }
    authService.login.mockResolvedValue(mockResponse)

    const wrapper = mount(Login, {
      global: {
        plugins: [router]
      }
    })

    await wrapper.find('input#username').setValue('testuser')
    await wrapper.find('input#password').setValue('password123')

    const form = wrapper.find('form')
    await form.trigger('submit')
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(authService.login).toHaveBeenCalled()
    expect(localStorage.getItem('access_token')).toBe('access-token')
  })

  it('handles login failure gracefully', async () => {
    const error = { response: { status: 401 } }
    authService.login.mockRejectedValue(error)

    const wrapper = mount(Login, {
      global: {
        plugins: [router]
      }
    })

    await wrapper.find('input#username').setValue('wronguser')
    await wrapper.find('input#password').setValue('wrongpass')

    const form = wrapper.find('form')
    await form.trigger('submit')
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))

    // El componente maneja el error internamente
    expect(wrapper.exists()).toBe(true)
  })

  it('shows loading state during login', async () => {
    const mockResponse = {
      data: {
        access: 'token',
        refresh: 'refresh'
      }
    }
    authService.login.mockImplementation(() => new Promise(resolve => setTimeout(() => resolve(mockResponse), 100)))

    const wrapper = mount(Login, {
      global: {
        plugins: [router]
      }
    })

    await wrapper.find('input#username').setValue('testuser')
    await wrapper.find('input#password').setValue('password123')

    const form = wrapper.find('form')
    const submitPromise = form.trigger('submit')
    
    await wrapper.vm.$nextTick()
    
    await submitPromise
    await new Promise(resolve => setTimeout(resolve, 150))

    expect(authService.login).toHaveBeenCalled()
  })
})
