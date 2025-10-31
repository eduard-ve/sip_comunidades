import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

export const useSaludStore = defineStore('salud', {
  state: () => ({
    registros: [],
    alertas: [],
    controles: [],
    loading: false,
    error: null
  }),

  getters: {
    registrosCount: (state) => state.registros.length,
    alertasActivas: (state) => state.alertas.filter(a => !a.resuelta).length,
    controlesPendientes: (state) => state.controles.filter(c => !c.realizado).length
  },

  actions: {
    async fetchRegistros() {
      this.loading = true
      try {
        const response = await axios.get(`${API_BASE_URL}/salud/registros/`)
        this.registros = response.data
        this.error = null
      } catch (error) {
        this.error = 'Error al cargar registros de salud'
        console.error(error)
      } finally {
        this.loading = false
      }
    },

    async fetchAlertas() {
      this.loading = true
      try {
        const response = await axios.get(`${API_BASE_URL}/salud/alertas/`)
        this.alertas = response.data
        this.error = null
      } catch (error) {
        this.error = 'Error al cargar alertas de salud'
        console.error(error)
      } finally {
        this.loading = false
      }
    },

    async fetchControles() {
      this.loading = true
      try {
        const response = await axios.get(`${API_BASE_URL}/salud/controles/`)
        this.controles = response.data
        this.error = null
      } catch (error) {
        this.error = 'Error al cargar controles de salud'
        console.error(error)
      } finally {
        this.loading = false
      }
    },

    async createRegistro(registroData) {
      try {
        const response = await axios.post(`${API_BASE_URL}/salud/registros/`, registroData)
        this.registros.push(response.data)
        return response.data
      } catch (error) {
        this.error = 'Error al crear registro de salud'
        throw error
      }
    },

    async createAlerta(alertaData) {
      try {
        const response = await axios.post(`${API_BASE_URL}/salud/alertas/`, alertaData)
        this.alertas.push(response.data)
        return response.data
      } catch (error) {
        this.error = 'Error al crear alerta de salud'
        throw error
      }
    },

    async createControl(controlData) {
      try {
        const response = await axios.post(`${API_BASE_URL}/salud/controles/`, controlData)
        this.controles.push(response.data)
        return response.data
      } catch (error) {
        this.error = 'Error al crear control de salud'
        throw error
      }
    },

    async updateRegistro(id, registroData) {
      try {
        const response = await axios.put(`${API_BASE_URL}/salud/registros/${id}/`, registroData)
        const index = this.registros.findIndex(r => r.id === id)
        if (index !== -1) {
          this.registros[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = 'Error al actualizar registro de salud'
        throw error
      }
    },

    async deleteRegistro(id) {
      try {
        await axios.delete(`${API_BASE_URL}/salud/registros/${id}/`)
        this.registros = this.registros.filter(r => r.id !== id)
      } catch (error) {
        this.error = 'Error al eliminar registro de salud'
        throw error
      }
    }
  }
})