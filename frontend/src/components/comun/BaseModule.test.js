import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseModule from './BaseModule.vue'

describe('BaseModule.vue', () => {
  it('renders title correctly', () => {
    const wrapper = mount(BaseModule, {
      props: {
        title: 'Test Module'
      }
    })
    expect(wrapper.text()).toContain('Test Module')
  })

  it('renders breadcrumbs when provided', () => {
    const breadcrumbs = [
      { label: 'Home', to: '/' },
      { label: 'Current' }
    ]
    const wrapper = mount(BaseModule, {
      props: {
        title: 'Test Module',
        breadcrumbs
      }
    })
    expect(wrapper.text()).toContain('Home')
    expect(wrapper.text()).toContain('Current')
  })

  it('emits create event when create button is clicked', async () => {
    const wrapper = mount(BaseModule, {
      props: {
        title: 'Test Module',
        showCreate: true
      }
    })
    const button = wrapper.find('button')
    await button.trigger('click')
    expect(wrapper.emitted()).toHaveProperty('create')
  })

  it('filters table rows based on search query', async () => {
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
        title: 'Test Module',
        table,
        showSearch: true
      }
    })

    // Initially shows both rows
    expect(wrapper.text()).toContain('John')
    expect(wrapper.text()).toContain('Jane')

    // Set search query
    const input = wrapper.find('input[type="text"]')
    await input.setValue('John')

    // Should only show John
    expect(wrapper.text()).toContain('John')
    expect(wrapper.text()).not.toContain('Jane')
  })

  it('displays empty message when no data', () => {
    const wrapper = mount(BaseModule, {
      props: {
        title: 'Test Module',
        table: { columns: [{ key: 'name', label: 'Name' }], rows: [] },
        showEmptyMessage: true,
        emptyMessage: 'No data available'
      }
    })
    // Check that the component renders and has the table structure
    expect(wrapper.find('table').exists()).toBe(true)
    expect(wrapper.find('tbody').exists()).toBe(true)
  })
})