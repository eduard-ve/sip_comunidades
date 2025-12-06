import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import DistribucionEdad from './DistribucionEdad.vue'

describe('DistribucionEdad.vue', () => {
  it('renders DistribucionEdad component correctly', () => {
    const wrapper = mount(DistribucionEdad, {
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
    const wrapper = mount(DistribucionEdad, {
      props: {
        data: [
          { rango_edad: '0-5', cantidad: 20 },
          { rango_edad: '6-12', cantidad: 30 }
        ]
      },
      global: {
        stubs: {
          ChartPanel: true
        }
      }
    })

    await wrapper.vm.$nextTick()

    expect(wrapper.vm.chartData.labels).toContain('0-5')
    expect(wrapper.vm.chartData.labels).toContain('6-12')
  })

  it('handles empty data gracefully', () => {
    const wrapper = mount(DistribucionEdad, {
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

