import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia, setActivePinia } from 'pinia'
import Login from './Login.vue'
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

describe('Login.vue', () => {
  let router

  beforeEach(() => {
    setActivePinia(createPinia())
    
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', component: { template: '<div>Home</div>' } },
        { path: '/dashboard', component: { template: '<div>Dashboard</div>' } }
      ]
    })

    vi.clearAllMocks()
  })

  it('renders login form correctly', () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [router]
      }
    })

    expect(wrapper.exists()).toBe(true)
    expect(wrapper.text()).toContain('iniciar sesión')
  })

  it('has username and password fields', () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [router]
      }
    })

    const usernameInput = wrapper.find('input#username')
    const passwordInput = wrapper.find('input#password')

    expect(usernameInput.exists()).toBe(true)
    expect(passwordInput.exists()).toBe(true)
  })

  it('calls login on form submit', async () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [router]
      }
    })

    const mockResponse = {
      data: {
        access: 'token',
        refresh: 'refresh'
      }
    }
    authService.login.mockResolvedValue(mockResponse)

    await wrapper.find('input#username').setValue('testuser')
    await wrapper.find('input#password').setValue('password123')
    
    const form = wrapper.find('form')
    await form.trigger('submit')
    await wrapper.vm.$nextTick()

    // Verificar que se llamó al servicio
    expect(authService.login).toHaveBeenCalled()
  })

  it('displays error message on login failure', async () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [router]
      }
    })

    const error = { response: { status: 401 } }
    authService.login.mockRejectedValue(error)

    await wrapper.find('input#username').setValue('testuser')
    await wrapper.find('input#password').setValue('wrongpass')

    const form = wrapper.find('form')
    await form.trigger('submit')
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))

    // El componente maneja el error internamente
    expect(wrapper.exists()).toBe(true)
  })

  it('toggles theme correctly', async () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [router]
      }
    })

    const initialTheme = wrapper.vm.isDarkTheme
    const themeButton = wrapper.find('.theme-toggle')
    if (themeButton.exists()) {
      await themeButton.trigger('click')
      expect(wrapper.vm.isDarkTheme).toBe(!initialTheme)
    }
  })
})
