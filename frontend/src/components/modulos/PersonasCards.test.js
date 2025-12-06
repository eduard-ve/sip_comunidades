import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import PersonasCards from './PersonasCards.vue'

describe('PersonasCards.vue', () => {
  it('renders PersonasCards component correctly', () => {
    const wrapper = mount(PersonasCards, {
      props: {
        personas: [],
        cargando: false
      }
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('displays loading state when cargando is true', () => {
    const wrapper = mount(PersonasCards, {
      props: {
        personas: [],
        cargando: true
      }
    })

    expect(wrapper.text()).toContain('Cargando personas')
  })

  it('displays no data message when personas is empty', () => {
    const wrapper = mount(PersonasCards, {
      props: {
        personas: [],
        cargando: false
      }
    })

    expect(wrapper.text()).toContain('No se encontraron personas')
  })

  it('displays persona cards when data is available', () => {
    const personas = [
      {
        id: 1,
        nombre_completo: 'Juan Pérez',
        fecha_nacimiento: '1990-01-01',
        ocupacion_nombre: 'Agricultor',
        estado_civil_nombre: 'Soltero',
        genero: 'M',
        numero_identificacion: '123456789'
      }
    ]

    const wrapper = mount(PersonasCards, {
      props: {
        personas,
        cargando: false
      }
    })

    expect(wrapper.text()).toContain('Juan Pérez')
  })

  it('calculates age correctly', () => {
    const wrapper = mount(PersonasCards, {
      props: {
        personas: [],
        cargando: false
      }
    })

    const edad = wrapper.vm.calcularEdad('1990-01-01')
    expect(edad).toBeGreaterThan(30)
  })

  it('gets initials correctly', () => {
    const wrapper = mount(PersonasCards, {
      props: {
        personas: [],
        cargando: false
      }
    })

    expect(wrapper.vm.getIniciales('Juan Pérez')).toBe('JP')
    expect(wrapper.vm.getIniciales('María José García López')).toBe('MJ')
  })

  it('opens modal when card is clicked', async () => {
    const persona = {
      id: 1,
      nombre_completo: 'Juan Pérez',
      fecha_nacimiento: '1990-01-01'
    }

    const wrapper = mount(PersonasCards, {
      props: {
        personas: [persona],
        cargando: false
      }
    })

    await wrapper.find('.persona-card').trigger('click')
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.modalVisible).toBe(true)
    expect(wrapper.vm.personaSeleccionada).toEqual(persona)
  })

  it('closes modal correctly', async () => {
    const wrapper = mount(PersonasCards, {
      props: {
        personas: [],
        cargando: false
      }
    })

    wrapper.vm.modalVisible = true
    wrapper.vm.cerrarModal()

    expect(wrapper.vm.modalVisible).toBe(false)
    expect(wrapper.vm.personaSeleccionada).toBeNull()
  })
})

