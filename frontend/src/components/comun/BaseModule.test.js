import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseModule from './BaseModule.vue'

describe('BaseModule.vue', () => {
  it('renders without crashing', () => {
    const wrapper = mount(BaseModule, {
      global: {
        stubs: {
          KpiCard: true,
          ChartPanel: true,
          RouterLink: true
        }
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('can handle basic props', () => {
    const wrapper = mount(BaseModule, {
      props: {
        title: 'Test Module'
      },
      global: {
        stubs: {
          KpiCard: true,
          ChartPanel: true,
          RouterLink: true
        }
      }
    })

    expect(wrapper.text()).toContain('Test Module')
  })

  it('can handle table data', () => {
    const table = {
      columns: [
        { key: 'name', label: 'Name' },
        { key: 'age', label: 'Age' }
      ],
      rows: [
        { name: 'John', age: 25 },
        { name: 'Jane', age: 30 }
      ]
    }

    const wrapper = mount(BaseModule, {
      props: {
        title: 'Test',
        table
      },
      global: {
        stubs: {
          KpiCard: true,
          ChartPanel: true,
          'router-link': {
            template: '<a><slot></slot></a>',
            props: ['to']
          }
        }
      }
    })

    expect(wrapper.text()).toContain('Name')
    expect(wrapper.text()).toContain('Age')
  })

  it('can handle search functionality', async () => {
    const table = {
      columns: [
        { key: 'name', label: 'Name' }
      ],
      rows: [
        { name: 'John' },
        { name: 'Jane' }
      ]
    }

    const wrapper = mount(BaseModule, {
      props: {
        title: 'Test',
        table,
        showSearch: true
      },
      global: {
        stubs: {
          KpiCard: true,
          ChartPanel: true,
          RouterLink: true
        }
      }
    })

    const input = wrapper.find('input[type="text"]')
    expect(input.exists()).toBe(true)
  })

  it('can handle breadcrumb navigation', () => {
    const breadcrumbs = [
      { label: 'Home', to: '/' },
      { label: 'Current Page' }
    ]

    const wrapper = mount(BaseModule, {
      props: {
        title: 'Test',
        breadcrumbs
      },
      global: {
        stubs: {
          KpiCard: true,
          ChartPanel: true,
          RouterLink: {
            template: '<a><slot></slot></a>',
            props: ['to']
          }
        }
      }
    })

    expect(wrapper.text()).toContain('Home')
    expect(wrapper.text()).toContain('Current Page')
  })
})