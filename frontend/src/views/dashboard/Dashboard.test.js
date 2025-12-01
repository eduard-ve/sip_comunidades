import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import Dashboard from './Dashboard.vue'
import { poblacionService } from '../../services/api.js'

// Mock the API service
vi.mock('../../services/api.js', () => ({
  poblacionService: {
    getDashboardData: vi.fn()
  }
}))

// Mock ChartPanel component
const ChartPanelStub = {
  name: 'ChartPanel',
  template: '<div class="chart-panel-stub"><slot /></div>',
  props: ['data', 'options', 'type', 'height', 'chartId', 'noCard']
}

describe('Dashboard.vue', () => {
  beforeEach(() => {
    // Reset mocks
    vi.clearAllMocks()
  })

  it('renders dashboard component with basic structure', () => {
    // Mock empty data
    poblacionService.getDashboardData.mockResolvedValue({
      data: {
        hero_metrics: {},
        indicadores_compactos: {},
        gestion_social: [],
        programas_tipo_radar: {},
        proximas_actividades: [],
        autoridades_activas: [],
        evolucion_data: {},
        ocupacion_data: {},
        desocupacion_data: {},
        genero_porcentajes: { masculino: 0, femenino: 0, otro: 0 },
        indicadores_data: {},
        edad_data: {}
      }
    })

    const wrapper = mount(Dashboard, {
      global: {
        stubs: {
          ChartPanel: ChartPanelStub
        }
      }
    })

    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('h1').text()).toContain('Dashboard Ejecutivo')
    expect(wrapper.text()).toContain('Comunidad Indígena El Refugio')
    expect(wrapper.text()).toContain('2025')
  })

  it('handles API errors gracefully', async () => {
    // Mock API error
    const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
    poblacionService.getDashboardData.mockRejectedValue(new Error('API Error'))

    const wrapper = mount(Dashboard, {
      global: {
        stubs: {
          ChartPanel: ChartPanelStub
        }
      }
    })

    // Wait for error handling
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 10))

    // Should have fallback data
    expect(wrapper.vm.heroMetrics.poblacion).toBeDefined()
    expect(wrapper.vm.heroMetrics.poblacion.value).toBe('0')

    consoleErrorSpy.mockRestore()
  })

  it('displays social management data', async () => {
    const mockData = {
      hero_metrics: {},
      indicadores_compactos: {},
      gestion_social: [
        { label: 'Programas Activos', value: 5, color: '#17a2b8' },
        { label: 'Beneficiarios Totales', value: 150, color: '#fd7e14' }
      ],
      programas_tipo_radar: {
        labels: ['Salud', 'Educación', 'Cultural'],
        datasets: [{
          label: 'Programas',
          data: [3, 2, 1],
          backgroundColor: 'rgba(59, 130, 246, 0.3)',
          borderColor: '#3b82f6'
        }]
      },
      proximas_actividades: [
        { nombre: 'Reunión Comunitaria', tipo: 'Reunión', fecha: '15/12/2025' }
      ],
      autoridades_activas: [
        { rol: 'Presidente', nombre: 'Juan Pérez' }
      ],
      evolucion_data: {},
      ocupacion_data: {},
      desocupacion_data: {},
      genero_porcentajes: { masculino: 50, femenino: 45, otro: 5 },
      indicadores_data: {},
      edad_data: {}
    }

    poblacionService.getDashboardData.mockResolvedValue({ data: mockData })

    const wrapper = mount(Dashboard, {
      global: {
        stubs: {
          ChartPanel: ChartPanelStub
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))

    // Check social management data
    expect(wrapper.text()).toContain('Programas Activos')
    expect(wrapper.text()).toContain('5')
    expect(wrapper.text()).toContain('Beneficiarios Totales')
    expect(wrapper.text()).toContain('150')

    // Check upcoming activities
    expect(wrapper.text()).toContain('Reunión Comunitaria')
    expect(wrapper.text()).toContain('Reunión')

    // Check active authorities
    expect(wrapper.text()).toContain('Presidente')
  })

  it('displays gender distribution correctly', async () => {
    const mockData = {
      hero_metrics: {},
      indicadores_compactos: {},
      gestion_social: [],
      programas_tipo_radar: {},
      proximas_actividades: [],
      autoridades_activas: [],
      evolucion_data: {},
      ocupacion_data: {},
      desocupacion_data: {},
      genero_porcentajes: {
        masculino: 52,
        femenino: 45,
        otro: 3
      },
      indicadores_data: {},
      edad_data: {}
    }

    poblacionService.getDashboardData.mockResolvedValue({ data: mockData })

    const wrapper = mount(Dashboard, {
      global: {
        stubs: {
          ChartPanel: ChartPanelStub
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))

    // Check gender percentages are displayed
    expect(wrapper.text()).toContain('Masculino')
    expect(wrapper.text()).toContain('52%')
    expect(wrapper.text()).toContain('Femenino')
    expect(wrapper.text()).toContain('45%')
    expect(wrapper.text()).toContain('Otro')
    expect(wrapper.text()).toContain('3%')
  })

  it('displays compact indicators', async () => {
    const mockData = {
      hero_metrics: {},
      indicadores_compactos: {
        dependencia: { value: '35.2%', label: 'Tasa de Dependencia', color: '#ff7043' },
        promedio_edad: { value: '28.5 años', label: 'Edad Promedio', color: '#42a5f5' },
        alfabetizacion: { value: '87.3%', label: 'Alfabetización', color: '#10b981' },
        cobertura_programas: { value: '65.8%', label: 'Cobertura Programas', color: '#f59e0b' }
      },
      gestion_social: [],
      programas_tipo_radar: {},
      proximas_actividades: [],
      autoridades_activas: [],
      evolucion_data: {},
      ocupacion_data: {},
      desocupacion_data: {},
      genero_porcentajes: { masculino: 50, femenino: 45, otro: 5 },
      indicadores_data: {},
      edad_data: {}
    }

    poblacionService.getDashboardData.mockResolvedValue({ data: mockData })

    const wrapper = mount(Dashboard, {
      global: {
        stubs: {
          ChartPanel: ChartPanelStub
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))

    // Check compact indicators
    expect(wrapper.text()).toContain('Tasa de Dependencia')
    expect(wrapper.text()).toContain('35.2%')
    expect(wrapper.text()).toContain('Edad Promedio')
    expect(wrapper.text()).toContain('28.5 años')
    expect(wrapper.text()).toContain('Alfabetización')
    expect(wrapper.text()).toContain('87.3%')
  })

  it('renders chart components with correct props', async () => {
    const mockData = {
      hero_metrics: {},
      indicadores_compactos: {},
      gestion_social: [],
      programas_tipo_radar: {},
      proximas_actividades: [],
      autoridades_activas: [],
      evolucion_data: {
        labels: ['Ene', 'Feb', 'Mar'],
        datasets: [{
          label: 'Registros',
          data: [100, 120, 110],
          borderColor: '#3b82f6'
        }]
      },
      ocupacion_data: {
        labels: ['Hombres', 'Mujeres'],
        datasets: [{
          data: [60, 55],
          backgroundColor: ['#3b82f6', '#ec4899']
        }]
      },
      desocupacion_data: {
        labels: ['Hombres', 'Mujeres'],
        datasets: [{
          data: [10, 8],
          backgroundColor: ['#3b82f6', '#ec4899']
        }]
      },
      genero_porcentajes: { masculino: 50, femenino: 45, otro: 5 },
      indicadores_data: {
        labels: ['Cubeo', 'Siriano', 'Desano'],
        datasets: [{
          data: [30, 25, 20],
          backgroundColor: ['#8b5cf6', '#3b5cf6', '#10b981']
        }]
      },
      edad_data: {
        labels: ['0-5', '6-12', '13-17'],
        datasets: [
          { label: 'Hombres', data: [50, 45, 40], backgroundColor: '#3b82f6' },
          { label: 'Mujeres', data: [48, 42, 38], backgroundColor: '#ec4899' }
        ]
      }
    }

    poblacionService.getDashboardData.mockResolvedValue({ data: mockData })

    const wrapper = mount(Dashboard, {
      global: {
        stubs: {
          ChartPanel: ChartPanelStub
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))

    // Check that ChartPanel components are rendered
    const chartPanels = wrapper.findAllComponents(ChartPanelStub)
    expect(chartPanels.length).toBeGreaterThan(0)

    // Check specific chart data is passed
    expect(wrapper.vm.evolucionData.labels).toEqual(['Ene', 'Feb', 'Mar'])
    expect(wrapper.vm.ocupacionData.labels).toEqual(['Hombres', 'Mujeres'])
    expect(wrapper.vm.edadData.datasets).toHaveLength(2)
  })

  it('handles empty data gracefully', async () => {
    poblacionService.getDashboardData.mockResolvedValue({
      data: {
        hero_metrics: {},
        indicadores_compactos: {},
        gestion_social: [],
        programas_tipo_radar: {},
        proximas_actividades: [],
        autoridades_activas: [],
        evolucion_data: {},
        ocupacion_data: {},
        desocupacion_data: {},
        genero_porcentajes: {},
        indicadores_data: {},
        edad_data: {}
      }
    })

    const wrapper = mount(Dashboard, {
      global: {
        stubs: {
          ChartPanel: ChartPanelStub
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))

    // Should not crash with empty data
    expect(wrapper.exists()).toBe(true)
  })
})