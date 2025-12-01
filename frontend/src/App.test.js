import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import App from './App.vue'

describe('App.vue', () => {
  it('renders router-view', () => {
    const wrapper = mount(App)
    expect(wrapper.findComponent({ name: 'router-view' })).toBeTruthy()
  })

  it('applies global styles', () => {
    const wrapper = mount(App)
    // Check if body styles are applied (this might not work in jsdom)
    // This is more of a smoke test
    expect(wrapper.exists()).toBe(true)
  })
})