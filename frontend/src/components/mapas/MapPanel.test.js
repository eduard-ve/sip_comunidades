import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import MapPanel from './MapPanel.vue'

describe('MapPanel.vue', () => {
  beforeEach(() => {
    // Mock de Leaflet
    global.L = {
      map: vi.fn(() => ({
        setView: vi.fn(),
        addLayer: vi.fn(),
        eachLayer: vi.fn(),
        removeLayer: vi.fn(),
        fitBounds: vi.fn()
      })),
      tileLayer: vi.fn(() => ({
        addTo: vi.fn()
      })),
      marker: vi.fn(() => ({
        addTo: vi.fn(),
        bindPopup: vi.fn()
      })),
      latLngBounds: vi.fn(() => ({}))
    }
  })

  it('renders MapPanel component correctly', () => {
    const wrapper = mount(MapPanel, {
      props: {
        programas: []
      }
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('renders map container', () => {
    const wrapper = mount(MapPanel, {
      props: {
        programas: []
      }
    })

    const mapContainer = wrapper.find('.map-container')
    expect(mapContainer.exists()).toBe(true)
  })

  it('handles programas prop', () => {
    const programas = [
      { nombre: 'Location 1', coordenadas: [4.0, -72.0] },
      { nombre: 'Location 2', coordenadas: [4.1, -72.1] }
    ]

    const wrapper = mount(MapPanel, {
      props: {
        programas
      }
    })

    expect(wrapper.props('programas')).toEqual(programas)
  })

  it('handles empty programas', () => {
    const wrapper = mount(MapPanel, {
      props: {
        programas: []
      }
    })

    expect(wrapper.props('programas')).toEqual([])
  })
})
