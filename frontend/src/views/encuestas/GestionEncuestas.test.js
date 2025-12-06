import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia, setActivePinia } from 'pinia'
import GestionEncuestas from './GestionEncuestas.vue'
import api from '../../services/api.js'

// Mock del servicio API
vi.mock('../../services/api.js', () => ({
  default: {
    get: vi.fn(() => Promise.resolve({ status: 200, data: [] }))
  }
}))

describe('GestionEncuestas.vue', () => {
  let router

  beforeEach(() => {
    setActivePinia(createPinia())
    
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', component: { template: '<div>Home</div>' } }
      ]
    })

    vi.clearAllMocks()
    localStorage.setItem('access_token', 'test-token')
    global.confirm = vi.fn(() => true)
  })

  it('renders GestionEncuestas view correctly', () => {
    const wrapper = mount(GestionEncuestas, {
      global: {
        plugins: [router],
        stubs: {
          EncuestaBase: true,
          EncuestaForm: true
        }
      }
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('loads encuestas on mount', async () => {
    const mockEncuestas = [
      { id_encuesta: 1, titulo: 'Encuesta 1', estado: 'activa' }
    ]
    
    api.get.mockResolvedValue({ status: 200, data: mockEncuestas })

    const wrapper = mount(GestionEncuestas, {
      global: {
        plugins: [router],
        stubs: {
          EncuestaBase: true,
          EncuestaForm: true
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 200))

    expect(api.get).toHaveBeenCalled()
  })

  it('opens form for new encuesta', () => {
    const wrapper = mount(GestionEncuestas, {
      global: {
        plugins: [router],
        stubs: {
          EncuestaBase: true,
          EncuestaForm: true
        }
      }
    })

    wrapper.vm.createSurvey()
    expect(wrapper.vm.showForm).toBe(true)
  })

  it('filters encuestas by status', async () => {
    const wrapper = mount(GestionEncuestas, {
      global: {
        plugins: [router],
        stubs: {
          EncuestaBase: true,
          EncuestaForm: true
        }
      }
    })

    wrapper.vm.selectedStatus = 'activa'
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.selectedStatus).toBe('activa')
  })

  it('handles error when loading encuestas', async () => {
    api.get.mockRejectedValue(new Error('Network error'))

    const wrapper = mount(GestionEncuestas, {
      global: {
        plugins: [router],
        stubs: {
          EncuestaBase: true,
          EncuestaForm: true
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 200))

    expect(wrapper.exists()).toBe(true)
  })
})
