import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import LenguasMaternas from './LenguasMaternas.vue'

describe('LenguasMaternas.vue', () => {
  it('renders LenguasMaternas component correctly', () => {
    const wrapper = mount(LenguasMaternas, {
      props: {
        data: []
      },
      global: {
        stubs: {
          ChartPanel: true
        }
      }
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('updates chart data when props change', async () => {
    const wrapper = mount(LenguasMaternas, {
      props: {
        data: [
          { lengua: 'Cubeo', cantidad: 50 },
          { lengua: 'Español', cantidad: 30 }
        ]
      },
      global: {
        stubs: {
          ChartPanel: true
        }
      }
    })

    await wrapper.vm.$nextTick()

    expect(wrapper.vm.chartData.labels).toContain('Cubeo')
    expect(wrapper.vm.chartData.labels).toContain('Español')
  })

  it('handles empty data gracefully', () => {
    const wrapper = mount(LenguasMaternas, {
      props: {
        data: []
      },
      global: {
        stubs: {
          ChartPanel: true
        }
      }
    })

    expect(wrapper.vm.chartData.labels).toEqual([])
    expect(wrapper.vm.chartData.datasets[0].data).toEqual([])
  })
})

