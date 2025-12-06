import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useSaludStore } from './salud.js'
import axios from 'axios'

// Mock de axios
vi.mock('axios', () => ({
  default: {
    get: vi.fn(() => Promise.resolve({ data: [] })),
    post: vi.fn(() => Promise.resolve({ data: {} })),
    put: vi.fn(() => Promise.resolve({ data: {} })),
    delete: vi.fn(() => Promise.resolve({}))
  }
}))

describe('useSaludStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    localStorage.setItem('access_token', 'test-token')
  })

  it('initializes with empty data', () => {
    const store = useSaludStore()
    expect(store.registros).toEqual([])
    expect(store.alertas).toEqual([])
    expect(store.controles).toEqual([])
    expect(store.loading).toBe(false)
  })

  it('loads registros successfully', async () => {
    const mockRegistros = [
      { id: 1, tipo_registro: 'Consulta', descripcion: 'Consulta médica' }
    ]
    
    axios.get.mockResolvedValue({ data: mockRegistros })

    const store = useSaludStore()
    await store.fetchRegistros()

    expect(axios.get).toHaveBeenCalled()
    expect(store.registros.length).toBeGreaterThan(0)
  })

  it('loads alertas successfully', async () => {
    const mockAlertas = [
      { id: 1, titulo: 'Alerta', prioridad: 'alta', resuelta: false }
    ]
    
    axios.get.mockResolvedValue({ data: mockAlertas })

    const store = useSaludStore()
    await store.fetchAlertas()

    expect(axios.get).toHaveBeenCalled()
    expect(store.alertas.length).toBeGreaterThan(0)
  })

  it('loads controles successfully', async () => {
    const mockControles = [
      { id: 1, tipo_control: 'Vacunación', realizado: false }
    ]
    
    axios.get.mockResolvedValue({ data: mockControles })

    const store = useSaludStore()
    await store.fetchControles()

    expect(axios.get).toHaveBeenCalled()
    expect(store.controles.length).toBeGreaterThan(0)
  })

  it('handles error when loading data', async () => {
    axios.get.mockRejectedValue(new Error('Network error'))

    const store = useSaludStore()
    await store.fetchRegistros()

    expect(store.error).toBeTruthy()
  })
})
