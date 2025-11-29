import { defineStore } from 'pinia'
import api from '../services/api.js'

const API_BASE_URL = 'http://127.0.0.1:8000/api'

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
    // Función para determinar la URL según el tipo de reporte
    getApiUrl(tipoReporte) {
      if (tipoReporte === 'reporte_salud') {
        return '/api/reportes/salud/';
      } else if (tipoReporte === 'reporte_social') {
        return '/api/reportes/social/';
      } else if (tipoReporte === 'reporte_encuestas') {
        return '/api/reportes/encuestas/';
      }
      return '/api/reportes/salud/'; // fallback
    },

    async fetchReportesSalud() {
      this.loading = true
      try {
        const response = await api.get('/reportes/salud/')
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
        const response = await api.get('/reportes/social/')
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
        const response = await api.get('/reportes/encuestas/')
        this.reportesEncuestas = response.data
        this.error = null
      } catch (error) {
        this.error = 'Error al cargar reportes de encuestas'
        console.error(error)
      } finally {
        this.loading = false
      }
    },

    async createReporte(reporteData) {
      try {
        const apiUrl = this.getApiUrl(reporteData.tipo_reporte);
        const response = await api.post(apiUrl, reporteData)

        // Agregar a la lista correspondiente según el tipo
        if (reporteData.tipo_reporte === 'reporte_salud') {
          this.reportesSalud.push(response.data)
        } else if (reporteData.tipo_reporte === 'reporte_social') {
          this.reportesSociales.push(response.data)
        } else if (reporteData.tipo_reporte === 'reporte_encuestas') {
          this.reportesEncuestas.push(response.data)
        }

        return response.data
      } catch (error) {
        this.error = 'Error al crear reporte'
        throw error
      }
    },

    async createReporteSalud(reporteData) {
      try {
        const response = await api.post('/reportes/salud/', reporteData)
        this.reportesSalud.push(response.data)
        return response.data
      } catch (error) {
        this.error = 'Error al crear reporte de salud'
        throw error
      }
    },

    async createReporteSocial(reporteData) {
      try {
        const response = await api.post('/reportes/social/', reporteData)
        this.reportesSociales.push(response.data)
        return response.data
      } catch (error) {
        this.error = 'Error al crear reporte social'
        throw error
      }
    },

    async createReporteEncuestas(reporteData) {
      try {
        const response = await api.post('/reportes/encuestas/', reporteData)
        this.reportesEncuestas.push(response.data)
        return response.data
      } catch (error) {
        this.error = 'Error al crear reporte de encuestas'
        throw error
      }
    },

    async updateReporteSalud(id, reporteData) {
      try {
        const response = await api.put(`/reportes/salud/${id}/`, reporteData)
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
        await api.delete(`/reportes/salud/${id}/`)
        this.reportesSalud = this.reportesSalud.filter(r => r.id !== id)
      } catch (error) {
        this.error = 'Error al eliminar reporte de salud'
        throw error
      }
    },

    async deleteReporteSocial(id) {
      try {
        await api.delete(`/reportes/social/${id}/`)
        this.reportesSociales = this.reportesSociales.filter(r => r.id !== id)
      } catch (error) {
        this.error = 'Error al eliminar reporte social'
        throw error
      }
    },

    async deleteReporteEncuestas(id) {
      try {
        await api.delete(`/reportes/encuestas/${id}/`)
        this.reportesEncuestas = this.reportesEncuestas.filter(r => r.id !== id)
      } catch (error) {
        this.error = 'Error al eliminar reporte de encuestas'
        throw error
      }
    },

    async updateReporteSocial(id, reporteData) {
      try {
        const response = await api.put(`/reportes/social/${id}/`, reporteData)
        const index = this.reportesSociales.findIndex(r => r.id === id)
        if (index !== -1) {
          this.reportesSociales[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = 'Error al actualizar reporte social'
        throw error
      }
    },

    async updateReporteEncuestas(id, reporteData) {
      try {
        const response = await api.put(`/reportes/encuestas/${id}/`, reporteData)
        const index = this.reportesEncuestas.findIndex(r => r.id === id)
        if (index !== -1) {
          this.reportesEncuestas[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = 'Error al actualizar reporte de encuestas'
        throw error
      }
    },

    async exportReportePDF(id, categoria) {
      try {
        let url = ''
        if (categoria === 'Salud') {
          url = `/reportes/salud/${id}/export_pdf/`
        } else if (categoria === 'Social') {
          url = `/reportes/social/${id}/export_pdf/`
        } else if (categoria === 'Encuestas') {
          url = `/reportes/encuestas/${id}/export_pdf/`
        }

        const response = await api.get(url, { responseType: 'blob' })

        // Crear un enlace para descargar el archivo
        const blob = new Blob([response.data], { type: 'application/pdf' })
        const link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = `reporte_${categoria.toLowerCase()}_${id}.pdf`
        link.click()

        return true
      } catch (error) {
        this.error = 'Error al exportar PDF'
        throw error
      }
    }
  }
})