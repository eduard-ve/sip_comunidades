import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import AuditTable from './AuditTable.vue'

describe('AuditTable.vue', () => {
  const mockEvents = [
    {
      id: 1,
      module: 'usuarios',
      user: 'admin',
      action: 'Creación de usuario',
      date: '2024-01-15'
    },
    {
      id: 2,
      module: 'reportes',
      user: 'user1',
      action: 'Modificación de reporte',
      date: '2024-01-16'
    },
    {
      id: 3,
      module: 'encuestas',
      user: 'user2',
      action: 'Eliminación de encuesta',
      date: '2024-01-17'
    }
  ]

  it('renders filters correctly', () => {
    const wrapper = mount(AuditTable, {
      props: { events: mockEvents }
    })

    // Check module filter
    const moduleSelect = wrapper.find('select')
    expect(moduleSelect.exists()).toBe(true)
    const options = moduleSelect.findAll('option')
    expect(options.length).toBe(4) // Todos + 3 modules

    // Check user input
    const userInput = wrapper.find('input[type="text"]')
    expect(userInput.exists()).toBe(true)
    expect(userInput.attributes('placeholder')).toBe('Buscar usuario...')

    // Check date input
    const dateInput = wrapper.find('input[type="date"]')
    expect(dateInput.exists()).toBe(true)

    // Check reset button
    const resetButton = wrapper.find('button')
    expect(resetButton.text()).toContain('Limpiar')
  })

  it('renders table headers correctly', () => {
    const wrapper = mount(AuditTable, {
      props: { events: mockEvents }
    })

    const headers = wrapper.findAll('thead th')
    expect(headers.length).toBe(6)
    expect(headers[0].text()).toBe('ID')
    expect(headers[1].text()).toBe('Módulo')
    expect(headers[2].text()).toBe('Usuario')
    expect(headers[3].text()).toBe('Acción')
    expect(headers[4].text()).toBe('Fecha')
    expect(headers[5].text()).toBe('Acciones')
  })

  it('renders events correctly', () => {
    const wrapper = mount(AuditTable, {
      props: { events: mockEvents }
    })

    const rows = wrapper.findAll('tbody tr')
    expect(rows.length).toBe(3)

    // Check first row
    const firstRowCells = rows[0].findAll('td')
    expect(firstRowCells[0].text()).toBe('1')
    expect(firstRowCells[1].text()).toBe('usuarios')
    expect(firstRowCells[2].text()).toBe('admin')
    expect(firstRowCells[3].text()).toContain('Creación de usuario')
    expect(firstRowCells[4].text()).toBe('2024-01-15')
  })

  it('displays action icons correctly', () => {
    const wrapper = mount(AuditTable, {
      props: { events: mockEvents }
    })

    const actionCells = wrapper.findAll('tbody tr td:nth-child(4)')

    // Check creation icon
    const creationIcon = actionCells[0].find('i')
    expect(creationIcon.classes()).toContain('fas')
    expect(creationIcon.classes()).toContain('fa-plus-circle')
    expect(creationIcon.classes()).toContain('text-success')

    // Check modification icon
    const modificationIcon = actionCells[1].find('i')
    expect(modificationIcon.classes()).toContain('fas')
    expect(modificationIcon.classes()).toContain('fa-edit')
    expect(modificationIcon.classes()).toContain('text-warning')

    // Check deletion icon
    const deletionIcon = actionCells[2].find('i')
    expect(deletionIcon.classes()).toContain('fas')
    expect(deletionIcon.classes()).toContain('fa-trash')
    expect(deletionIcon.classes()).toContain('text-danger')
  })

  it('filters by module correctly', async () => {
    const wrapper = mount(AuditTable, {
      props: { events: mockEvents }
    })

    // Initially all events shown
    expect(wrapper.findAll('tbody tr').length).toBe(3)

    // Filter by usuarios module
    const moduleSelect = wrapper.find('select')
    await moduleSelect.setValue('usuarios')

    // Should show only 1 event
    expect(wrapper.findAll('tbody tr').length).toBe(1)
    expect(wrapper.find('tbody tr td').text()).toBe('1')
  })

  it('filters by user correctly', async () => {
    const wrapper = mount(AuditTable, {
      props: { events: mockEvents }
    })

    // Filter by user
    const userInput = wrapper.find('input[type="text"]')
    await userInput.setValue('admin')

    // Should show only 1 event
    expect(wrapper.findAll('tbody tr').length).toBe(1)
    expect(wrapper.find('tbody tr td:nth-child(3)').text()).toBe('admin')
  })

  it('filters by date correctly', async () => {
    const wrapper = mount(AuditTable, {
      props: { events: mockEvents }
    })

    // Filter by date
    const dateInput = wrapper.find('input[type="date"]')
    await dateInput.setValue('2024-01-15')

    // Should show only 1 event
    expect(wrapper.findAll('tbody tr').length).toBe(1)
    expect(wrapper.find('tbody tr td:nth-child(5)').text()).toBe('2024-01-15')
  })

  it('resets filters correctly', async () => {
    const wrapper = mount(AuditTable, {
      props: { events: mockEvents }
    })

    // Apply filters
    const moduleSelect = wrapper.find('select')
    const userInput = wrapper.find('input[type="text"]')
    const dateInput = wrapper.find('input[type="date"]')

    await moduleSelect.setValue('usuarios')
    await userInput.setValue('admin')
    await dateInput.setValue('2024-01-15')

    // Should show 1 event
    expect(wrapper.findAll('tbody tr').length).toBe(1)

    // Reset filters
    const resetButton = wrapper.find('button')
    await resetButton.trigger('click')

    // Should show all events again
    expect(wrapper.findAll('tbody tr').length).toBe(3)
  })

  it('emits view-details event when view button is clicked', async () => {
    const wrapper = mount(AuditTable, {
      props: { events: mockEvents }
    })

    const viewButton = wrapper.find('button.btn-outline-info')
    await viewButton.trigger('click')

    expect(wrapper.emitted('view-details')).toBeTruthy()
    expect(wrapper.emitted('view-details')[0]).toEqual([mockEvents[0]])
  })

  it('displays empty message when no events match filters', async () => {
    const wrapper = mount(AuditTable, {
      props: { events: mockEvents }
    })

    // Filter by non-existent user
    const userInput = wrapper.find('input[type="text"]')
    await userInput.setValue('nonexistent')

    const emptyRow = wrapper.find('tbody tr')
    expect(emptyRow.find('td').text()).toBe('Sin registros')
    expect(emptyRow.find('td').attributes('colspan')).toBe('6')
  })

  it('displays empty message when no events provided', () => {
    const wrapper = mount(AuditTable, {
      props: { events: [] }
    })

    const emptyRow = wrapper.find('tbody tr')
    expect(emptyRow.find('td').text()).toBe('Sin registros')
  })

  it('applies correct CSS classes', () => {
    const wrapper = mount(AuditTable, {
      props: { events: mockEvents }
    })

    // Check card classes
    const cards = wrapper.findAll('.card')
    expect(cards.length).toBe(2)

    // Check table classes
    const table = wrapper.find('table')
    expect(table.classes()).toContain('table')
    expect(table.classes()).toContain('table-hover')
    expect(table.classes()).toContain('table-striped')
    expect(table.classes()).toContain('align-middle')

    // Check table header classes
    const thead = wrapper.find('thead')
    expect(thead.classes()).toContain('table-dark')
  })
})