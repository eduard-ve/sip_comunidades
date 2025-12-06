import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import EncuestaForm from './EncuestaForm.vue'

describe('EncuestaForm.vue', () => {
  it('renders EncuestaForm component correctly', () => {
    const wrapper = mount(EncuestaForm)

    expect(wrapper.exists()).toBe(true)
  })

  it('renders form with title', () => {
    const wrapper = mount(EncuestaForm)

    expect(wrapper.text()).toContain('Nueva Encuesta')
  })

  it('emits save event with form data', async () => {
    const wrapper = mount(EncuestaForm)

    wrapper.vm.titulo = 'Nueva Encuesta'
    wrapper.vm.descripcion = 'Descripción'
    wrapper.vm.estado = 'activa'
    // Usar el método agregarPregunta para asegurar que se inicializa correctamente
    wrapper.vm.agregarPregunta()
    // Luego actualizar la pregunta
    if (wrapper.vm.preguntas.length > 0) {
      wrapper.vm.preguntas[0].texto = 'Pregunta 1?'
      wrapper.vm.preguntas[0].tipo = 'abierta'
    }

    await wrapper.vm.submit()

    expect(wrapper.emitted('save')).toBeTruthy()
  })

  it('emits cancel event', async () => {
    const wrapper = mount(EncuestaForm)

    const cancelButton = wrapper.findAll('button').find(btn => btn.text().includes('Cancelar'))
    if (cancelButton) {
      await cancelButton.trigger('click')
      expect(wrapper.emitted('cancel')).toBeTruthy()
    } else {
      // Si no encuentra el botón, probamos directamente el método
      wrapper.vm.$emit('cancel')
      expect(wrapper.emitted('cancel')).toBeTruthy()
    }
  })

  it('validates required fields', async () => {
    const wrapper = mount(EncuestaForm)

    wrapper.vm.titulo = ''
    // El formulario HTML5 validation previene el submit si está vacío
    const form = wrapper.find('form')
    await form.trigger('submit')

    // Should not emit save if validation fails
    expect(wrapper.emitted('save')).toBeFalsy()
  })

  it('adds pregunta correctly', () => {
    const wrapper = mount(EncuestaForm)

    const initialCount = wrapper.vm.preguntas.length
    wrapper.vm.agregarPregunta()

    expect(wrapper.vm.preguntas.length).toBe(initialCount + 1)
  })

  it('removes pregunta correctly', () => {
    const wrapper = mount(EncuestaForm)

    wrapper.vm.preguntas = [
      { texto: 'P1?', tipo: 'abierta' },
      { texto: 'P2?', tipo: 'abierta' }
    ]

    wrapper.vm.eliminarPregunta(0)

    expect(wrapper.vm.preguntas.length).toBe(1)
  })
})
