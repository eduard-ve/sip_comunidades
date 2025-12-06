import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import ChartPanel from './ChartPanel.vue'

// Mock de Chart.js
vi.mock('chart.js/auto', () => {
  return {
    default: vi.fn().mockImplementation(() => ({
      data: {},
      update: vi.fn(),
      destroy: vi.fn()
    }))
  }
})

describe('ChartPanel.vue', () => {
  beforeEach(() => {
    // Crear canvas element en el DOM
    const canvas = document.createElement('canvas')
    canvas.id = 'testChart'
    document.body.appendChild(canvas)
  })

  it('renders ChartPanel component correctly', () => {
    const wrapper = mount(ChartPanel, {
      props: {
        chartId: 'testChart',
        type: 'bar',
        data: {
          labels: ['A', 'B'],
          datasets: [{ data: [1, 2] }]
        }
      }
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('creates chart on mount', async () => {
    const Chart = (await import('chart.js/auto')).default
    
    mount(ChartPanel, {
      props: {
        chartId: 'testChart',
        type: 'bar',
        data: {
          labels: ['A', 'B'],
          datasets: [{ data: [1, 2] }]
        }
      }
    })

    await new Promise(resolve => setTimeout(resolve, 50))
    
    expect(Chart).toHaveBeenCalled()
  })

  it('renders with card when noCard is false', () => {
    const wrapper = mount(ChartPanel, {
      props: {
        chartId: 'testChart',
        type: 'bar',
        data: { labels: [], datasets: [] },
        noCard: false
      }
    })

    expect(wrapper.find('.card').exists()).toBe(true)
  })

  it('renders without card when noCard is true', () => {
    const wrapper = mount(ChartPanel, {
      props: {
        chartId: 'testChart',
        type: 'bar',
        data: { labels: [], datasets: [] },
        noCard: true
      }
    })

    expect(wrapper.find('.card').exists()).toBe(false)
  })

  it('displays title slot when provided', () => {
    const wrapper = mount(ChartPanel, {
      props: {
        chartId: 'testChart',
        type: 'bar',
        data: { labels: [], datasets: [] }
      },
      slots: {
        title: 'Test Chart Title'
      }
    })

    expect(wrapper.text()).toContain('Test Chart Title')
  })

  it('updates chart when data changes', async () => {
    const Chart = (await import('chart.js/auto')).default
    const mockUpdate = vi.fn()
    const mockChart = {
      data: {},
      update: mockUpdate,
      destroy: vi.fn()
    }
    Chart.mockReturnValue(mockChart)

    const wrapper = mount(ChartPanel, {
      props: {
        chartId: 'testChart',
        type: 'bar',
        data: {
          labels: ['A'],
          datasets: [{ data: [1] }]
        }
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))

    await wrapper.setProps({
      data: {
        labels: ['A', 'B'],
        datasets: [{ data: [1, 2] }]
      }
    })

    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))

    expect(mockUpdate).toHaveBeenCalled()
  })

  it('applies custom height', () => {
    const wrapper = mount(ChartPanel, {
      props: {
        chartId: 'testChart',
        type: 'bar',
        data: { labels: [], datasets: [] },
        height: '400px'
      }
    })

    const chartWrapper = wrapper.find('.chart-wrapper')
    expect(chartWrapper.attributes('style')).toContain('height: 400px')
  })

  it('handles different chart types', () => {
    const types = ['bar', 'line', 'pie', 'doughnut']
    
    types.forEach(type => {
      const wrapper = mount(ChartPanel, {
        props: {
          chartId: `testChart${type}`,
          type: type,
          data: { labels: [], datasets: [] }
        }
      })

      expect(wrapper.exists()).toBe(true)
    })
  })
})

