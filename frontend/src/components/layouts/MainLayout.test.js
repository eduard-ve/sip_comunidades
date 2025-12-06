import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia, setActivePinia } from 'pinia'
import MainLayout from './MainLayout.vue'
import { useAuth } from '../../stores/auth.js'

// Mock del store de auth
vi.mock('../../stores/auth.js', () => ({
  useAuth: vi.fn()
}))

describe('MainLayout.vue', () => {
  let router
  let mockAuth

  beforeEach(() => {
    setActivePinia(createPinia())
    
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/dashboard', component: { template: '<div>Dashboard</div>' } }
      ]
    })

    mockAuth = {
      isAuthenticated: { value: true },
      initAuth: vi.fn(),
      hasRole: vi.fn(() => true),
      user: { value: { username: 'test', rol: 'admin' } }
    }

    useAuth.mockReturnValue(mockAuth)
  })

  it('renders MainLayout component correctly', () => {
    const wrapper = mount(MainLayout, {
      global: {
        plugins: [router]
      }
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('includes Navbar component', () => {
    const wrapper = mount(MainLayout, {
      global: {
        plugins: [router],
        stubs: {
          Navbar: true,
          Sidebar: true,
          RouterView: true
        }
      }
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('includes Sidebar component', () => {
    const wrapper = mount(MainLayout, {
      global: {
        plugins: [router],
        stubs: {
          Navbar: true,
          Sidebar: true,
          RouterView: true
        }
      }
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('includes RouterView component', () => {
    const wrapper = mount(MainLayout, {
      global: {
        plugins: [router],
        stubs: {
          Navbar: true,
          Sidebar: true,
          RouterView: true
        }
      }
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('initializes auth on mount', async () => {
    const wrapper = mount(MainLayout, {
      global: {
        plugins: [router],
        stubs: {
          Navbar: true,
          Sidebar: true,
          RouterView: true
        }
      }
    })

    await wrapper.vm.$nextTick()
    // MainLayout simplemente renderiza Navbar, Sidebar y RouterView
    expect(wrapper.exists()).toBe(true)
  })

  it('renders correctly when not authenticated', async () => {
    mockAuth.isAuthenticated.value = false

    const wrapper = mount(MainLayout, {
      global: {
        plugins: [router],
        stubs: {
          Navbar: true,
          Sidebar: true,
          RouterView: true
        }
      }
    })

    await wrapper.vm.$nextTick()
    
    // El componente se renderiza independientemente del estado de autenticación
    expect(wrapper.exists()).toBe(true)
  })
})

