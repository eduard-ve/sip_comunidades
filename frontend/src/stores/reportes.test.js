import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useReportesStore } from './reportes.js'
import api from '../services/api.js'

// Mock del servicio API
vi.mock('../services/api.js', () => ({
  default: {
    get: vi.fn(() => Promise.resolve({ data: [] })),
    post: vi.fn(() => Promise.resolve({ data: {} })),
    put: vi.fn(() => Promise.resolve({ data: {} })),
    delete: vi.fn(() => Promise.resolve({}))
  }
}))

describe('useReportesStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('initializes with empty reportes', () => {
    const store = useReportesStore()
    expect(store.reportesSalud).toEqual([])
    expect(store.reportesSociales).toEqual([])
    expect(store.reportesEncuestas).toEqual([])
    expect(store.loading).toBe(false)
  })

  it('loads reportes successfully', async () => {
    const mockReportes = [
      { id: 1, tipo_reporte: 'reporte_salud', fecha_reporte: '2024-01-01' }
    ]
    
    api.get.mockResolvedValue({ data: mockReportes })

    const store = useReportesStore()
    await store.fetchReportesSalud()

    expect(api.get).toHaveBeenCalledWith('/reportes/salud/')
    expect(store.reportesSalud.length).toBeGreaterThan(0)
  })

  it('creates reporte successfully', async () => {
    const mockReporte = { id: 1, tipo_reporte: 'reporte_salud' }
    api.post.mockResolvedValue({ data: mockReporte })

    const store = useReportesStore()
    await store.createReporte(mockReporte)

    expect(api.post).toHaveBeenCalled()
  })

  it('updates reporte successfully', async () => {
    const mockReporte = { id: 1, tipo_reporte: 'reporte_salud_updated' }
    api.put.mockResolvedValue({ data: mockReporte })

    const store = useReportesStore()
    store.reportesSalud = [{ id: 1, tipo_reporte: 'reporte_salud' }]
    await store.updateReporteSalud(1, mockReporte)

    expect(api.put).toHaveBeenCalled()
  })

  it('deletes reporte successfully', async () => {
    api.delete.mockResolvedValue({})

    const store = useReportesStore()
    store.reportesSalud = [{ id: 1, tipo_reporte: 'reporte_salud' }]
    await store.deleteReporteSalud(1)

    expect(api.delete).toHaveBeenCalled()
    expect(store.reportesSalud.length).toBe(0)
  })

  it('handles error when loading reportes', async () => {
    api.get.mockRejectedValue(new Error('Network error'))

    const store = useReportesStore()
    await store.fetchReportesSalud()

    expect(store.error).toBeTruthy()
  })
})
