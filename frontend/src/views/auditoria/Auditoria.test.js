import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import Auditoria from './Auditoria.vue'
import { auditService } from '../../services/api.js'

// Mock del servicio API
vi.mock('../../services/api.js', () => ({
  auditService: {
    getAuditLogs: vi.fn(),
    getAuditStats: vi.fn()
  }
}))

describe('Auditoria.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('renders auditoria view correctly', () => {
    const wrapper = mount(Auditoria, {
      global: {
        stubs: {
          AuditTable: true
        }
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('loads audit data on mount', async () => {
    const mockLogs = {
      data: [
        { id_audit: 1, accion: 'CREATE', modelo: 'User', descripcion: 'User created' }
      ]
    }
    const mockStats = {
      data: {
        total_logs: 1,
        acciones: { CREATE: 1 },
        modelos: { User: 1 }
      }
    }
    
    auditService.getAuditLogs.mockResolvedValue(mockLogs)
    auditService.getAuditStats.mockResolvedValue(mockStats)

    const wrapper = mount(Auditoria, {
      global: {
        stubs: {
          AuditTable: true
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 200))

    expect(auditService.getAuditLogs).toHaveBeenCalled()
  })

  it('handles API errors gracefully', async () => {
    auditService.getAuditLogs.mockRejectedValue(new Error('Network error'))
    auditService.getAuditStats.mockRejectedValue(new Error('Network error'))

    const wrapper = mount(Auditoria, {
      global: {
        stubs: {
          AuditTable: true
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))

    expect(wrapper.exists()).toBe(true)
  })

  it('displays loading state initially', () => {
    const wrapper = mount(Auditoria, {
      global: {
        stubs: {
          AuditTable: true
        }
      }
    })

    // El componente tiene un estado de loading
    expect(wrapper.vm.loading).toBeDefined()
  })
})
