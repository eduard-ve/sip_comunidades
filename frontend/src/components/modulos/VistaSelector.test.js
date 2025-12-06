import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import VistaSelector from './VistaSelector.vue'

describe('VistaSelector.vue', () => {
  it('renders VistaSelector component correctly', () => {
    const wrapper = mount(VistaSelector, {
      props: {
        personas: [],
        personasFiltradas: [],
        cargando: false
      },
      global: {
        stubs: {
          PersonasCards: true,
          DistribucionGenero: true,
          TopOcupaciones: true,
          DistribucionEducativa: true,
          LenguasMaternas: true,
          DistribucionEdad: true,
          PopulationPyramid: true,
          TablasAnalisis: true,
          ArbolFamiliar: true
        }
      }
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('displays vista buttons', () => {
    const wrapper = mount(VistaSelector, {
      props: {
        personas: [],
        personasFiltradas: [],
        cargando: false
      },
      global: {
        stubs: {
          PersonasCards: true,
          DistribucionGenero: true,
          TopOcupaciones: true,
          DistribucionEducativa: true,
          LenguasMaternas: true,
          DistribucionEdad: true,
          PopulationPyramid: true,
          TablasAnalisis: true,
          ArbolFamiliar: true
        }
      }
    })

    const buttons = wrapper.findAll('.vista-btn')
    expect(buttons.length).toBeGreaterThan(0)
  })

  it('changes vista when button is clicked', async () => {
    const wrapper = mount(VistaSelector, {
      props: {
        personas: [],
        personasFiltradas: [],
        cargando: false
      },
      global: {
        stubs: {
          PersonasCards: true,
          DistribucionGenero: true,
          TopOcupaciones: true,
          DistribucionEducativa: true,
          LenguasMaternas: true,
          DistribucionEdad: true,
          PopulationPyramid: true,
          TablasAnalisis: true,
          ArbolFamiliar: true
        }
      }
    })

    const initialVista = wrapper.vm.vistaActiva
    const buttons = wrapper.findAll('.vista-btn')
    
    if (buttons.length > 1) {
      await buttons[1].trigger('click')
      expect(wrapper.emitted('vista-cambiada')).toBeTruthy()
    }
  })

  it('displays tarjetas vista by default', () => {
    const wrapper = mount(VistaSelector, {
      props: {
        personas: [],
        personasFiltradas: [],
        cargando: false
      },
      global: {
        stubs: {
          PersonasCards: true,
          DistribucionGenero: true,
          TopOcupaciones: true,
          DistribucionEducativa: true,
          LenguasMaternas: true,
          DistribucionEdad: true,
          PopulationPyramid: true,
          TablasAnalisis: true,
          ArbolFamiliar: true
        }
      }
    })

    expect(wrapper.vm.vistaActiva).toBe('tarjetas')
  })

  it('emits ver-detalle event', async () => {
    const wrapper = mount(VistaSelector, {
      props: {
        personas: [],
        personasFiltradas: [],
        cargando: false
      },
      global: {
        stubs: {
          PersonasCards: true,
          DistribucionGenero: true,
          TopOcupaciones: true,
          DistribucionEducativa: true,
          LenguasMaternas: true,
          DistribucionEdad: true,
          PopulationPyramid: true,
          TablasAnalisis: true,
          ArbolFamiliar: true
        }
      }
    })

    const persona = { id: 1, nombre_completo: 'Juan Pérez' }
    wrapper.vm.verDetalle(persona)

    expect(wrapper.emitted('ver-detalle')).toBeTruthy()
    expect(wrapper.emitted('ver-detalle')[0][0]).toEqual(persona)
  })

  it('emits editar-persona event', () => {
    const wrapper = mount(VistaSelector, {
      props: {
        personas: [],
        personasFiltradas: [],
        cargando: false
      },
      global: {
        stubs: {
          PersonasCards: true,
          DistribucionGenero: true,
          TopOcupaciones: true,
          DistribucionEducativa: true,
          LenguasMaternas: true,
          DistribucionEdad: true,
          PopulationPyramid: true,
          TablasAnalisis: true,
          ArbolFamiliar: true
        }
      }
    })

    const persona = { id: 1, nombre_completo: 'Juan Pérez' }
    wrapper.vm.editarPersona(persona)

    expect(wrapper.emitted('editar-persona')).toBeTruthy()
  })

  it('emits eliminar-persona event', () => {
    const wrapper = mount(VistaSelector, {
      props: {
        personas: [],
        personasFiltradas: [],
        cargando: false
      },
      global: {
        stubs: {
          PersonasCards: true,
          DistribucionGenero: true,
          TopOcupaciones: true,
          DistribucionEducativa: true,
          LenguasMaternas: true,
          DistribucionEdad: true,
          PopulationPyramid: true,
          TablasAnalisis: true,
          ArbolFamiliar: true
        }
      }
    })

    const persona = { id: 1, nombre_completo: 'Juan Pérez' }
    // Mock confirm para que retorne true
    global.confirm = vi.fn(() => true)
    wrapper.vm.eliminarPersona(persona)

    expect(wrapper.emitted('eliminar-persona')).toBeTruthy()
  })
})

