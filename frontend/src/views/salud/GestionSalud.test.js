import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import GestionSalud from './GestionSalud.vue'
import { useSaludStore } from '../../stores/salud.js'

// Mock the salud store
vi.mock('../../stores/salud.js', () => ({
  useSaludStore: vi.fn(() => ({
    alertas: [],
    alertasActivas: 0,
    enfermedadesComunes: [],
    fetchAlertas: vi.fn().mockResolvedValue(),
    fetchEnfermedadesComunes: vi.fn().mockResolvedValue()
  }))
}))

describe('GestionSalud.vue', () => {
  let pinia

  beforeEach(() => {
    pinia = createPinia()
    vi.clearAllMocks()
  })

  it('renders gestion salud component', () => {
    const wrapper = mount(GestionSalud, {
      global: {
        plugins: [pinia],
        stubs: global.testStubs
      }
    })

    expect(wrapper.exists()).toBe(true)
  })
})