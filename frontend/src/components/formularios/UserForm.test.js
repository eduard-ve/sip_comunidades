import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import UserForm from './UserForm.vue'

describe('UserForm.vue', () => {
  const defaultProps = {
    modelValue: {
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      telefono: '',
      rol: 'invitado',
      is_active: true,
      password: '',
      password2: ''
    },
    roles: ['admin', 'editor', 'invitado']
  }

  it('renders form fields correctly', () => {
    const wrapper = mount(UserForm, {
      props: defaultProps
    })

    // Check required fields
    expect(wrapper.find('#username').exists()).toBe(true)
    expect(wrapper.find('#first_name').exists()).toBe(true)
    expect(wrapper.find('#email').exists()).toBe(true)
    expect(wrapper.find('#rol').exists()).toBe(true)
    expect(wrapper.find('#is_active').exists()).toBe(true)

    // Check optional fields
    expect(wrapper.find('#last_name').exists()).toBe(true)
    expect(wrapper.find('#telefono').exists()).toBe(true)
  })

  it('shows password fields only for new users', () => {
    // New user (no id)
    const wrapper = mount(UserForm, {
      props: defaultProps
    })

    expect(wrapper.find('#password').exists()).toBe(true)
    expect(wrapper.find('#password2').exists()).toBe(true)

    // Existing user (with id)
    const existingUserProps = {
      ...defaultProps,
      modelValue: { ...defaultProps.modelValue, id: 1 }
    }
    const wrapperExisting = mount(UserForm, {
      props: existingUserProps
    })

    expect(wrapperExisting.find('#password').exists()).toBe(false)
    expect(wrapperExisting.find('#password2').exists()).toBe(false)
  })

  it('displays role options correctly', () => {
    const wrapper = mount(UserForm, {
      props: defaultProps
    })

    const roleSelect = wrapper.find('#rol')
    const options = roleSelect.findAll('option')

    // Should have 4 options: disabled + 3 roles
    expect(options.length).toBe(4)
    expect(options[0].text()).toBe('Seleccionar rol')
    expect(options[1].text()).toBe('👑 Administrador')
    expect(options[2].text()).toBe('✏️ Editor')
    expect(options[3].text()).toBe('👤 Invitado')
  })

  it('validates required fields', async () => {
    const wrapper = mount(UserForm, {
      props: defaultProps
    })

    // Submit empty form
    await wrapper.find('form').trigger('submit.prevent')

    // Check that validation errors are shown
    expect(wrapper.text()).toContain('El nombre de usuario es obligatorio')
    expect(wrapper.text()).toContain('El nombre es obligatorio')
  })

  it('validates email format', async () => {
    const wrapper = mount(UserForm, {
      props: {
        ...defaultProps,
        modelValue: {
          ...defaultProps.modelValue,
          username: 'testuser',
          first_name: 'Test',
          email: 'invalid-email'
        }
      }
    })

    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.text()).toContain('Email inválido')
  })

  it('validates password requirements for new users', async () => {
    const wrapper = mount(UserForm, {
      props: {
        ...defaultProps,
        modelValue: {
          ...defaultProps.modelValue,
          username: 'testuser',
          first_name: 'Test',
          email: 'test@example.com',
          password: '123', // Too short
          password2: '123'
        }
      }
    })

    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.text()).toContain('La contraseña debe tener al menos 8 caracteres')
  })

  it('validates password confirmation match', async () => {
    const wrapper = mount(UserForm, {
      props: {
        ...defaultProps,
        modelValue: {
          ...defaultProps.modelValue,
          username: 'testuser',
          first_name: 'Test',
          email: 'test@example.com',
          password: 'password123',
          password2: 'different123'
        }
      }
    })

    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.text()).toContain('Las contraseñas no coinciden')
  })

  it('emits submit event with valid data for new user', async () => {
    const wrapper = mount(UserForm, {
      props: {
        ...defaultProps,
        modelValue: {
          ...defaultProps.modelValue,
          username: 'testuser',
          first_name: 'Test',
          last_name: 'User',
          email: 'test@example.com',
          telefono: '123456789',
          rol: 'editor',
          is_active: true,
          password: 'password123',
          password2: 'password123'
        }
      }
    })

    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.emitted('submit')).toBeTruthy()
    const emittedData = wrapper.emitted('submit')[0][0]

    expect(emittedData.username).toBe('testuser')
    expect(emittedData.first_name).toBe('Test')
    expect(emittedData.email).toBe('test@example.com')
    expect(emittedData.password).toBe('password123')
    expect(emittedData.password2).toBe('password123')
  })

  it('emits submit event with valid data for existing user', async () => {
    const wrapper = mount(UserForm, {
      props: {
        ...defaultProps,
        modelValue: {
          id: 1,
          username: 'existinguser',
          first_name: 'Existing',
          last_name: 'User',
          email: 'existing@example.com',
          telefono: '987654321',
          rol: 'admin',
          is_active: false
        }
      }
    })

    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.emitted('submit')).toBeTruthy()
    const emittedData = wrapper.emitted('submit')[0][0]

    // Password fields should not be included for existing users
    expect(emittedData.password).toBeUndefined()
    expect(emittedData.password2).toBeUndefined()
    expect(emittedData.username).toBe('existinguser')
    expect(emittedData.is_active).toBe(false)
  })

  it('emits cancel event when cancel button is clicked', async () => {
    const wrapper = mount(UserForm, {
      props: defaultProps
    })

    const cancelButton = wrapper.find('button[type="button"]')
    await cancelButton.trigger('click')

    expect(wrapper.emitted('cancel')).toBeTruthy()
  })

  it('updates form when modelValue changes', async () => {
    const wrapper = mount(UserForm, {
      props: defaultProps
    })

    // Initial values
    expect(wrapper.vm.form.username).toBe('')

    // Update props
    await wrapper.setProps({
      modelValue: {
        ...defaultProps.modelValue,
        username: 'updateduser',
        first_name: 'Updated'
      }
    })

    expect(wrapper.vm.form.username).toBe('updateduser')
    expect(wrapper.vm.form.first_name).toBe('Updated')
  })

  it('shows validation errors with correct styling', async () => {
    const wrapper = mount(UserForm, {
      props: defaultProps
    })

    // Submit empty form to trigger validation
    await wrapper.find('form').trigger('submit.prevent')

    // Check that invalid classes are applied
    const usernameInput = wrapper.find('#username')
    expect(usernameInput.classes()).toContain('is-invalid')

    const emailInput = wrapper.find('#email')
    expect(emailInput.classes()).toContain('is-invalid')
  })

  it('displays correct button text for new vs existing user', () => {
    // New user
    const wrapper = mount(UserForm, {
      props: defaultProps
    })

    const submitButton = wrapper.find('button[type="submit"]')
    expect(submitButton.text()).toContain('Crear Usuario')

    // Existing user
    const existingUserProps = {
      ...defaultProps,
      modelValue: { ...defaultProps.modelValue, id: 1 }
    }
    const wrapperExisting = mount(UserForm, {
      props: existingUserProps
    })

    const submitButtonExisting = wrapperExisting.find('button[type="submit"]')
    expect(submitButtonExisting.text()).toContain('Actualizar Usuario')
  })

  it('handles form submission without errors for valid data', async () => {
    const wrapper = mount(UserForm, {
      props: {
        ...defaultProps,
        modelValue: {
          ...defaultProps.modelValue,
          username: 'validuser',
          first_name: 'Valid',
          email: 'valid@example.com',
          rol: 'editor',
          password: 'password123',
          password2: 'password123'
        }
      }
    })

    await wrapper.find('form').trigger('submit.prevent')

    // Should emit submit event without validation errors
    expect(wrapper.emitted('submit')).toBeTruthy()
  })
})