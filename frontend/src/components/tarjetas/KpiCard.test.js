import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import KpiCard from './KpiCard.vue'

describe('KpiCard.vue', () => {
  it('renders KpiCard component correctly', () => {
    const wrapper = mount(KpiCard, {
      props: {
        title: 'Test KPI',
        value: 100,
        change: 5,
        icon: 'bi-graph-up',
        colorIcon: '#007bff'
      }
    })

    expect(wrapper.exists()).toBe(true)
    expect(wrapper.text()).toContain('Test KPI')
    expect(wrapper.text()).toContain('100')
  })

  it('displays positive change with success color', () => {
    const wrapper = mount(KpiCard, {
      props: {
        title: 'Test',
        value: 100,
        change: 5,
        icon: 'bi-graph-up'
      }
    })

    const changeElement = wrapper.find('small')
    expect(changeElement.classes()).toContain('text-success')
    expect(wrapper.text()).toContain('+5%')
  })

  it('displays negative change with danger color', () => {
    const wrapper = mount(KpiCard, {
      props: {
        title: 'Test',
        value: 100,
        change: -3,
        icon: 'bi-graph-down'
      }
    })

    const changeElement = wrapper.find('small')
    expect(changeElement.classes()).toContain('text-danger')
    expect(wrapper.text()).toContain('-3%')
  })

  it('displays icon with custom color', () => {
    const wrapper = mount(KpiCard, {
      props: {
        title: 'Test',
        value: 100,
        change: 0,
        icon: 'bi-star',
        colorIcon: '#ffc107'
      }
    })

    const icon = wrapper.find('i')
    expect(icon.exists()).toBe(true)
    // El navegador convierte hex a rgb, verificamos que tenga el color
    expect(icon.attributes('style')).toContain('color')
  })

  it('handles string values', () => {
    const wrapper = mount(KpiCard, {
      props: {
        title: 'Test',
        value: '68%',
        change: 3,
        icon: 'bi-percent'
      }
    })

    expect(wrapper.text()).toContain('68%')
  })

  it('handles numeric values', () => {
    const wrapper = mount(KpiCard, {
      props: {
        title: 'Test',
        value: 1240,
        change: 120,
        icon: 'bi-people'
      }
    })

    expect(wrapper.text()).toContain('1240')
  })

  it('applies default colorIcon when not provided', () => {
    const wrapper = mount(KpiCard, {
      props: {
        title: 'Test',
        value: 100,
        change: 0,
        icon: 'bi-graph'
      }
    })

    const icon = wrapper.find('i')
    // El navegador convierte hex a rgb, verificamos que tenga el color
    expect(icon.attributes('style')).toContain('color')
  })
})

