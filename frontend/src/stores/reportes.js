import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

export const useReportesStore = defineStore('reportes', {
  state: () => ({
    reportesSalud: [],
    reportesSociales: [],
    reportesEncuestas: [],
    loading: false,
    error: null
  }),

  getters: {
    reportesSaludCount: (state) => state.reportesSalud.length,
    reportesSocialesCount: (state) => state.reportesSociales.length,
    reportesEncuestasCount: (state) => state.reportesEncuestas.length,
    totalReportes: (state) => state.reportesSalud.length + state.reportesSociales.length + state.reportesEncuestas.length
  },

  actions: {
    async fetchReportesSalud() {
      this.loading = true
      try {
        const response = await axios.get(`${API_BASE_URL}/reportes/salud/`)
        this.reportesSalud = response.data
        this.error = null
      } catch (error) {
        this.error = 'Error al cargar reportes de salud'
        console.error(error)
      } finally {
        this.loading = false
      }
    },

    async fetchReportesSociales() {
      this.loading = true
      try {
        const response = await axios.get(`${API_BASE_URL}/reportes/social/`)
        this.reportesSociales = response.data
        this.error = null
      } catch (error) {
        this.error = 'Error al cargar reportes sociales'
        console.error(error)
      } finally {
        this.loading = false
      }
    },

    async fetchReportesEncuestas() {
      this.loading = true
      try {
        const response = await axios.get(`${API_BASE_URL}/reportes/encuestas/`)
        this.reportesEncuestas = response.data
        this.error = null
      } catch (error) {
        this.error = 'Error al cargar reportes de encuestas'
        console.error(error)
      } finally {
        this.loading = false
      }
    },

    async createReporteSalud(reporteData) {
      try {
        const response = await axios.post(`${API_BASE_URL}/reportes/salud/`, reporteData)
        this.reportesSalud.push(response.data)
        return response.data
      } catch (error) {
        this.error = 'Error al crear reporte de salud'
        throw error
      }
    },

    async createReporteSocial(reporteData) {
      try {
        const response = await axios.post(`${API_BASE_URL}/reportes/social/`, reporteData)
        this.reportesSociales.push(response.data)
        return response.data
      } catch (error) {
        this.error = 'Error al crear reporte social'
        throw error
      }
    },

    async createReporteEncuestas(reporteData) {
      try {
        const response = await axios.post(`${API_BASE_URL}/reportes/encuestas/`, reporteData)
        this.reportesEncuestas.push(response.data)
        return response.data
      } catch (error) {
        this.error = 'Error al crear reporte de encuestas'
        throw error
      }
    },

    async updateReporteSalud(id, reporteData) {
      try {
        const response = await axios.put(`${API_BASE_URL}/reportes/salud/${id}/`, reporteData)
        const index = this.reportesSalud.findIndex(r => r.id === id)
        if (index !== -1) {
          this.reportesSalud[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = 'Error al actualizar reporte de salud'
        throw error
      }
    },

    async deleteReporteSalud(id) {
      try {
        await axios.delete(`${API_BASE_URL}/reportes/salud/${id}/`)
        this.reportesSalud = this.reportesSalud.filter(r => r.id !== id)
      } catch (error) {
        this.error = 'Error al eliminar reporte de salud'
        throw error
      }
    },

    async deleteReporteSocial(id) {
      try {
        await axios.delete(`${API_BASE_URL}/reportes/social/${id}/`)
        this.reportesSociales = this.reportesSociales.filter(r => r.id !== id)
      } catch (error) {
        this.error = 'Error al eliminar reporte social'
        throw error
      }
    },

    async deleteReporteEncuestas(id) {
      try {
        await axios.delete(`${API_BASE_URL}/reportes/encuestas/${id}/`)
        this.reportesEncuestas = this.reportesEncuestas.filter(r => r.id !== id)
      } catch (error) {
        this.error = 'Error al eliminar reporte de encuestas'
        throw error
      }
    }
  }
})