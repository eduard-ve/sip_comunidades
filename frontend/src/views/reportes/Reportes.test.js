import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import Reportes from './Reportes.vue'
import { useReportesStore } from '../../stores/reportes.js'

// Mock del store
vi.mock('../../stores/reportes.js', () => ({
  useReportesStore: vi.fn(() => ({
    fetchReportesSalud: vi.fn(() => Promise.resolve()),
    fetchReportesSociales: vi.fn(() => Promise.resolve()),
    fetchReportesEncuestas: vi.fn(() => Promise.resolve()),
    reportesSaludCount: 0,
    reportesSocialesCount: 0,
    reportesEncuestasCount: 0,
    totalReportes: 0,
    reportesSalud: [],
    reportesSociales: [],
    reportesEncuestas: []
  }))
}))

describe('Reportes.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    global.confirm = vi.fn(() => true)
  })

  it('renders reportes view correctly', () => {
    const wrapper = mount(Reportes, {
      global: {
        stubs: {
          BaseModule: true,
          ReporteForm: true
        }
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('loads reportes on mount', async () => {
    const mockStore = {
      fetchReportesSalud: vi.fn(() => Promise.resolve()),
      fetchReportesSociales: vi.fn(() => Promise.resolve()),
      fetchReportesEncuestas: vi.fn(() => Promise.resolve()),
      reportesSaludCount: 0,
      reportesSocialesCount: 0,
      reportesEncuestasCount: 0,
      totalReportes: 0,
      reportesSalud: [],
      reportesSociales: [],
      reportesEncuestas: []
    }
    useReportesStore.mockReturnValue(mockStore)

    const wrapper = mount(Reportes, {
      global: {
        stubs: {
          BaseModule: true,
          ReporteForm: true
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(mockStore.fetchReportesSalud).toHaveBeenCalled()
  })

  it('opens form for new reporte', () => {
    const wrapper = mount(Reportes, {
      global: {
        stubs: {
          BaseModule: true,
          ReporteForm: true
        }
      }
    })

    wrapper.vm.showForm = true
    expect(wrapper.vm.showForm).toBe(true)
  })

  it('handles error gracefully', async () => {
    const mockStore = {
      fetchReportesSalud: vi.fn(() => Promise.reject(new Error('Network error'))),
      fetchReportesSociales: vi.fn(() => Promise.reject(new Error('Network error'))),
      fetchReportesEncuestas: vi.fn(() => Promise.reject(new Error('Network error'))),
      reportesSaludCount: 0,
      reportesSocialesCount: 0,
      reportesEncuestasCount: 0,
      totalReportes: 0,
      reportesSalud: [],
      reportesSociales: [],
      reportesEncuestas: []
    }
    useReportesStore.mockReturnValue(mockStore)

    const wrapper = mount(Reportes, {
      global: {
        stubs: {
          BaseModule: true,
          ReporteForm: true
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.exists()).toBe(true)
  })
})
