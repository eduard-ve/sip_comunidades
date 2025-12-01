import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import DataTable from './DataTable.vue'

describe('DataTable.vue', () => {
  const headers = ['Nombre', 'Edad', 'Ciudad']
  const items = [
    { Nombre: 'Juan', Edad: 25, Ciudad: 'Bogotá' },
    { Nombre: 'María', Edad: 30, Ciudad: 'Medellín' },
    { Nombre: 'Pedro', Edad: 35, Ciudad: 'Cali' }
  ]

  it('renders table headers correctly', () => {
    const wrapper = mount(DataTable, {
      props: {
        headers,
        items
      }
    })

    const headerCells = wrapper.findAll('thead th')
    expect(headerCells.length).toBe(3)
    expect(headerCells[0].text()).toBe('Nombre')
    expect(headerCells[1].text()).toBe('Edad')
    expect(headerCells[2].text()).toBe('Ciudad')
  })

  it('renders table rows correctly', () => {
    const wrapper = mount(DataTable, {
      props: {
        headers,
        items
      }
    })

    const rows = wrapper.findAll('tbody tr')
    expect(rows.length).toBe(3)

    // Check first row
    const firstRowCells = rows[0].findAll('td')
    expect(firstRowCells.length).toBe(3)
    expect(firstRowCells[0].text()).toBe('Juan')
    expect(firstRowCells[1].text()).toBe('25')
    expect(firstRowCells[2].text()).toBe('Bogotá')
  })

  it('displays empty message when no items', () => {
    const wrapper = mount(DataTable, {
      props: {
        headers,
        items: []
      }
    })

    const rows = wrapper.findAll('tbody tr')
    expect(rows.length).toBe(1)

    const emptyCell = wrapper.find('tbody tr td')
    expect(emptyCell.text()).toBe('No hay datos para mostrar')
    expect(emptyCell.attributes('colspan')).toBe('3')
  })

  it('applies correct CSS classes', () => {
    const wrapper = mount(DataTable, {
      props: {
        headers,
        items
      }
    })

    const table = wrapper.find('table')
    expect(table.classes()).toContain('table')
    expect(table.classes()).toContain('table-striped')
    expect(table.classes()).toContain('table-hover')
    expect(table.classes()).toContain('align-middle')

    const thead = wrapper.find('thead')
    expect(thead.classes()).toContain('table-primary')
  })

  it('has responsive wrapper', () => {
    const wrapper = mount(DataTable, {
      props: {
        headers,
        items
      }
    })

    const container = wrapper.find('.table-responsive')
    expect(container.exists()).toBe(true)
  })

  it('handles different data types', () => {
    const mixedItems = [
      { Nombre: 'Test', Activo: true, Puntaje: 95.5, Fecha: '2024-01-01' }
    ]
    const mixedHeaders = ['Nombre', 'Activo', 'Puntaje', 'Fecha']

    const wrapper = mount(DataTable, {
      props: {
        headers: mixedHeaders,
        items: mixedItems
      }
    })

    const cells = wrapper.findAll('tbody td')
    expect(cells[0].text()).toBe('Test')
    expect(cells[1].text()).toBe('true')
    expect(cells[2].text()).toBe('95.5')
    expect(cells[3].text()).toBe('2024-01-01')
  })

  it('renders single row correctly', () => {
    const singleItem = [{ Nombre: 'Solo', Edad: 40 }]
    const wrapper = mount(DataTable, {
      props: {
        headers: ['Nombre', 'Edad'],
        items: singleItem
      }
    })

    const rows = wrapper.findAll('tbody tr')
    expect(rows.length).toBe(1)

    const cells = wrapper.findAll('tbody td')
    expect(cells.length).toBe(2)
    expect(cells[0].text()).toBe('Solo')
    expect(cells[1].text()).toBe('40')
  })
})