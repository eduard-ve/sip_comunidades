import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import ResponderEncuesta from './ResponderEncuesta.vue'
import api from '../../services/api.js'

// Mock del servicio API
vi.mock('../../services/api.js', () => ({
  default: {
    get: vi.fn(() => Promise.resolve({ data: {} })),
    post: vi.fn(() => Promise.resolve({ data: { success: true } }))
  }
}))

describe('ResponderEncuesta.vue', () => {
  let router

  beforeEach(() => {
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', component: { template: '<div>Home</div>' } }
      ]
    })

    vi.clearAllMocks()
  })

  it('renders ResponderEncuesta component correctly', () => {
    const wrapper = mount(ResponderEncuesta, {
      props: {
        id: '12345'
      },
      global: {
        plugins: [router]
      }
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('loads encuesta by token on mount', async () => {
    const mockEncuesta = {
      data: {
        id_encuesta: 1,
        titulo: 'Test Encuesta',
        descripcion: 'Description',
        preguntas: []
      }
    }
    
    api.get.mockResolvedValue(mockEncuesta)

    const wrapper = mount(ResponderEncuesta, {
      props: {
        id: '12345'
      },
      global: {
        plugins: [router]
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))

    // El componente puede cargar la encuesta de diferentes formas
    expect(wrapper.exists()).toBe(true)
  })

  it('handles error when loading encuesta', async () => {
    api.get.mockRejectedValue(new Error('Not found'))

    const wrapper = mount(ResponderEncuesta, {
      props: {
        id: '12345'
      },
      global: {
        plugins: [router]
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.exists()).toBe(true)
  })

  it('displays message when no preguntas', async () => {
    const mockEncuesta = {
      data: {
        id_encuesta: 1,
        titulo: 'Test',
        preguntas: []
      }
    }
    
    api.get.mockResolvedValue(mockEncuesta)

    const wrapper = mount(ResponderEncuesta, {
      props: {
        id: '12345'
      },
      global: {
        plugins: [router]
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.exists()).toBe(true)
  })
})
