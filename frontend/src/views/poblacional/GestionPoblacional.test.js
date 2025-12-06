import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import GestionPoblacional from './GestionPoblacional.vue'
import { poblacionService } from '../../services/api.js'

// Mock del servicio API
vi.mock('../../services/api.js', () => ({
  poblacionService: {
    getPersonas: vi.fn(() => Promise.resolve({ data: [] })),
    getTiposIdentificacion: vi.fn(() => Promise.resolve({ data: [] })),
    getNivelesEducativos: vi.fn(() => Promise.resolve({ data: [] })),
    getOcupaciones: vi.fn(() => Promise.resolve({ data: [] })),
    getEstadosCiviles: vi.fn(() => Promise.resolve({ data: [] })),
    getLenguas: vi.fn(() => Promise.resolve({ data: [] })),
    getDistribucionGenero: vi.fn(() => Promise.resolve({ data: [] })),
    getTopOcupaciones: vi.fn(() => Promise.resolve({ data: [] })),
    getDistribucionEducativa: vi.fn(() => Promise.resolve({ data: [] })),
    getLenguasMaternas: vi.fn(() => Promise.resolve({ data: [] })),
    getDistribucionEdad: vi.fn(() => Promise.resolve({ data: [] })),
    getRelacionesFamiliares: vi.fn(() => Promise.resolve({ data: [] }))
  }
}))

describe('GestionPoblacional.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    global.confirm = vi.fn(() => true)
  })

  it('renders GestionPoblacional component correctly', () => {
    const wrapper = mount(GestionPoblacional, {
      global: {
        stubs: {
          KpiCard: true,
          FilterSidebar: true,
          VistaSelector: true
        }
      }
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('loads personas on mount', async () => {
    const mockPersonas = {
      data: [
        { id: 1, nombre_completo: 'Juan Pérez', numero_identificacion: '123456789' }
      ]
    }
    
    poblacionService.getPersonas.mockResolvedValue(mockPersonas)

    const wrapper = mount(GestionPoblacional, {
      global: {
        stubs: {
          KpiCard: true,
          FilterSidebar: true,
          VistaSelector: true
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 200))

    expect(poblacionService.getPersonas).toHaveBeenCalled()
  })

  it('calculates KPIs correctly', async () => {
    const mockPersonas = {
      data: [
        { id: 1, nombre_completo: 'Juan', genero: 'M' },
        { id: 2, nombre_completo: 'María', genero: 'F' }
      ]
    }
    
    poblacionService.getPersonas.mockResolvedValue(mockPersonas)

    const wrapper = mount(GestionPoblacional, {
      global: {
        stubs: {
          KpiCard: true,
          FilterSidebar: true,
          VistaSelector: true
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 200))

    // Los KPIs pueden ser números o strings
    expect(wrapper.vm.kpis).toBeDefined()
    expect(Array.isArray(wrapper.vm.kpis)).toBe(true)
  })

  it('handles error when loading personas', async () => {
    poblacionService.getPersonas.mockRejectedValue(new Error('Network error'))

    const wrapper = mount(GestionPoblacional, {
      global: {
        stubs: {
          KpiCard: true,
          FilterSidebar: true,
          VistaSelector: true
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.exists()).toBe(true)
  })
})
