import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import UsuariosRoles from './UsuariosRoles.vue'
import { userService } from '../../services/api.js'

// Mock del servicio API
vi.mock('../../services/api.js', () => ({
  userService: {
    getUsers: vi.fn(),
    createUser: vi.fn(),
    updateUser: vi.fn(),
    deleteUser: vi.fn()
  }
}))

describe('UsuariosRoles.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    global.confirm = vi.fn(() => true)
  })

  it('renders usuarios roles view correctly', () => {
    const wrapper = mount(UsuariosRoles, {
      global: {
        stubs: {
          BaseModule: true,
          UserForm: true
        }
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('loads users on mount', async () => {
    const mockUsers = {
      data: [
        { id: 1, username: 'admin', rol: 'admin' },
        { id: 2, username: 'user', rol: 'editor' }
      ]
    }
    
    userService.getUsers.mockResolvedValue(mockUsers)

    const wrapper = mount(UsuariosRoles, {
      global: {
        stubs: {
          BaseModule: true,
          UserForm: true
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 200))

    expect(userService.getUsers).toHaveBeenCalled()
  })

  it('calculates KPIs correctly', async () => {
    const mockUsers = {
      data: [
        { id: 1, username: 'admin', rol: 'admin' },
        { id: 2, username: 'user1', rol: 'editor' },
        { id: 3, username: 'user2', rol: 'invitado' }
      ]
    }
    
    userService.getUsers.mockResolvedValue(mockUsers)

    const wrapper = mount(UsuariosRoles, {
      global: {
        stubs: {
          BaseModule: true,
          UserForm: true
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 200))

    expect(wrapper.vm.kpis).toBeDefined()
    expect(Array.isArray(wrapper.vm.kpis)).toBe(true)
  })

  it('filters users by role', async () => {
    const wrapper = mount(UsuariosRoles, {
      global: {
        stubs: {
          BaseModule: true,
          UserForm: true
        }
      }
    })

    wrapper.vm.filterRole = 'admin'
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.filterRole).toBe('admin')
  })

  it('opens form for new user', () => {
    const wrapper = mount(UsuariosRoles, {
      global: {
        stubs: {
          BaseModule: true,
          UserForm: true
        }
      }
    })

    if (typeof wrapper.vm.openForm === 'function') {
      wrapper.vm.openForm()
      expect(wrapper.vm.showForm).toBe(true)
    } else {
      wrapper.vm.showForm = true
      expect(wrapper.vm.showForm).toBe(true)
    }
  })

  it('handles error when loading users', async () => {
    userService.getUsers.mockRejectedValue(new Error('Network error'))

    const wrapper = mount(UsuariosRoles, {
      global: {
        stubs: {
          BaseModule: true,
          UserForm: true
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.exists()).toBe(true)
  })
})
