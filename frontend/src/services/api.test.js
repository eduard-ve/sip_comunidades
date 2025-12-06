import { describe, it, expect, beforeEach, vi } from 'vitest'

// Mock de axios antes de importar los servicios
vi.mock('axios', () => {
  const mockAxiosInstance = {
    get: vi.fn(() => Promise.resolve({ data: {} })),
    post: vi.fn(() => Promise.resolve({ data: {} })),
    put: vi.fn(() => Promise.resolve({ data: {} })),
    patch: vi.fn(() => Promise.resolve({ data: {} })),
    delete: vi.fn(() => Promise.resolve({ data: {} })),
    interceptors: {
      request: { use: vi.fn() },
      response: { use: vi.fn() }
    }
  }

  return {
    default: {
      create: vi.fn(() => mockAxiosInstance),
      interceptors: {
        request: { use: vi.fn() },
        response: { use: vi.fn() }
      },
      get: vi.fn(() => Promise.resolve({ data: {} })),
      post: vi.fn(() => Promise.resolve({ data: {} })),
      put: vi.fn(() => Promise.resolve({ data: {} })),
      patch: vi.fn(() => Promise.resolve({ data: {} })),
      delete: vi.fn(() => Promise.resolve({ data: {} }))
    }
  }
})

// Importar servicios después del mock
import { authService, userService, poblacionService, socialService } from './api.js'
import axios from 'axios'

// Obtener la instancia mockeada
const getMockInstance = () => axios.create()

describe('API Services', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.clearAllMocks()
  })

  describe('authService', () => {
    it('login calls correct endpoint with credentials', async () => {
      const credentials = { username: 'test', password: 'pass' }
      await authService.login(credentials)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/usuarios/login/', credentials)
    })

    it('register calls correct endpoint with user data', async () => {
      const userData = { username: 'newuser', email: 'test@test.com', password: 'pass' }
      await authService.register(userData)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/usuarios/registro/', userData)
    })

    it('refreshToken calls correct endpoint with refresh token', async () => {
      await authService.refreshToken('refresh-token')
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/usuarios/token/refresh/', { refresh: 'refresh-token' })
    })

    it('getProfile calls correct endpoint', async () => {
      await authService.getProfile()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/usuarios/perfil/')
    })
  })

  describe('userService', () => {
    it('getUsers calls correct endpoint', async () => {
      await userService.getUsers()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/usuarios/usuarios/')
    })

    it('createUser calls correct endpoint with user data', async () => {
      const userData = { username: 'newuser', email: 'test@test.com' }
      await userService.createUser(userData)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/usuarios/registro/', userData)
    })

    it('updateUser calls correct endpoint with id and user data', async () => {
      const userData = { username: 'updated' }
      await userService.updateUser(1, userData)
      const mockInstance = getMockInstance()
      expect(mockInstance.put).toHaveBeenCalledWith('/usuarios/usuarios/1/', userData)
    })

    it('deleteUser calls correct endpoint with id', async () => {
      await userService.deleteUser(1)
      const mockInstance = getMockInstance()
      expect(mockInstance.delete).toHaveBeenCalledWith('/usuarios/usuarios/1/')
    })
  })

  describe('poblacionService', () => {
    it('getPersonas calls correct endpoint', async () => {
      await poblacionService.getPersonas()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/personas/')
    })

    it('createPersona calls correct endpoint', async () => {
      const personaData = { nombre: 'Juan', apellido: 'Pérez' }
      await poblacionService.createPersona(personaData)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/poblacion/personas/', personaData)
    })

    it('updatePersona calls correct endpoint', async () => {
      const personaData = { nombre: 'Juan Updated' }
      await poblacionService.updatePersona(1, personaData)
      const mockInstance = getMockInstance()
      expect(mockInstance.put).toHaveBeenCalledWith('/poblacion/personas/1/', personaData)
    })

    it('deletePersona calls correct endpoint', async () => {
      await poblacionService.deletePersona(1)
      const mockInstance = getMockInstance()
      expect(mockInstance.delete).toHaveBeenCalledWith('/poblacion/personas/1/')
    })

    it('getTiposIdentificacion calls correct endpoint', async () => {
      await poblacionService.getTiposIdentificacion()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/tipos_identificacion/')
    })

    it('getNivelesEducativos calls correct endpoint', async () => {
      await poblacionService.getNivelesEducativos()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/niveles_educativos/')
    })

    it('getOcupaciones calls correct endpoint', async () => {
      await poblacionService.getOcupaciones()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/ocupaciones/')
    })

    it('getGruposEtnicos calls correct endpoint', async () => {
      await poblacionService.getGruposEtnicos()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/grupos_etnicos/')
    })

    it('getEstadosCiviles calls correct endpoint', async () => {
      await poblacionService.getEstadosCiviles()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/estados_civiles/')
    })

    it('getLenguas calls correct endpoint', async () => {
      await poblacionService.getLenguas()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/lenguas/')
    })

    it('getTiposRelaciones calls correct endpoint', async () => {
      await poblacionService.getTiposRelaciones()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/tipos_relaciones/')
    })

    it('getRelacionesFamiliares calls correct endpoint', async () => {
      await poblacionService.getRelacionesFamiliares()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/relaciones_familiares/')
    })

    it('createRelacionFamiliar calls correct endpoint', async () => {
      const relacionData = { persona: 1, familiar: 2, tipo_relacion: 1 }
      await poblacionService.createRelacionFamiliar(relacionData)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/poblacion/relaciones_familiares/', relacionData)
    })

    it('updateRelacionFamiliar calls correct endpoint', async () => {
      const relacionData = { tipo_relacion: 2 }
      await poblacionService.updateRelacionFamiliar(1, relacionData)
      const mockInstance = getMockInstance()
      expect(mockInstance.put).toHaveBeenCalledWith('/poblacion/relaciones_familiares/1/', relacionData)
    })

    it('deleteRelacionFamiliar calls correct endpoint', async () => {
      await poblacionService.deleteRelacionFamiliar(1)
      const mockInstance = getMockInstance()
      expect(mockInstance.delete).toHaveBeenCalledWith('/poblacion/relaciones_familiares/1/')
    })

    it('getStats calls correct endpoint', async () => {
      await poblacionService.getStats()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/stats/')
    })

    it('getEstadisticas calls correct endpoint', async () => {
      await poblacionService.getEstadisticas()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/estadisticas/estadisticas/')
    })

    it('getDistribucionEdad calls correct endpoint', async () => {
      await poblacionService.getDistribucionEdad()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/estadisticas/distribucion_edad/')
    })

    it('getDistribucionEducativa calls correct endpoint', async () => {
      await poblacionService.getDistribucionEducativa()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/estadisticas/distribucion_educativa/')
    })

    it('getDistribucionGenero calls correct endpoint', async () => {
      await poblacionService.getDistribucionGenero()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/estadisticas/distribucion_genero/')
    })

    it('getTopOcupaciones calls correct endpoint', async () => {
      await poblacionService.getTopOcupaciones()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/estadisticas/top_ocupaciones/')
    })

    it('getLenguasMaternas calls correct endpoint', async () => {
      await poblacionService.getLenguasMaternas()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/estadisticas/lenguas_maternas/')
    })

    it('getLenguasPorGrupoEtnico calls correct endpoint', async () => {
      await poblacionService.getLenguasPorGrupoEtnico(1)
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/estadisticas/1/lenguas_por_grupo_etnico/')
    })

    it('getDashboard calls correct endpoint', async () => {
      await poblacionService.getDashboard()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/poblacion/estadisticas/dashboard/')
    })
  })

  describe('socialService', () => {
    it('getEstadosPrograma calls correct endpoint', async () => {
      await socialService.getEstadosPrograma()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/social/estados/')
    })

    it('createEstadoPrograma calls correct endpoint', async () => {
      const estadoData = { nombre: 'Activo', descripcion: 'Estado activo', color: '#28a745' }
      await socialService.createEstadoPrograma(estadoData)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/social/estados/', estadoData)
    })

    it('updateEstadoPrograma calls correct endpoint', async () => {
      const estadoData = { nombre: 'Actualizado' }
      await socialService.updateEstadoPrograma(1, estadoData)
      const mockInstance = getMockInstance()
      expect(mockInstance.put).toHaveBeenCalledWith('/social/estados/1/', estadoData)
    })

    it('deleteEstadoPrograma calls correct endpoint', async () => {
      await socialService.deleteEstadoPrograma(1)
      const mockInstance = getMockInstance()
      expect(mockInstance.delete).toHaveBeenCalledWith('/social/estados/1/')
    })

    it('getProgramas calls correct endpoint', async () => {
      await socialService.getProgramas()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/social/programas/')
    })

    it('createPrograma calls correct endpoint', async () => {
      const programaData = { nombre: 'Programa Test', descripcion: 'Descripción', estado: 1 }
      await socialService.createPrograma(programaData)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/social/programas/', programaData)
    })

    it('updatePrograma calls correct endpoint', async () => {
      const programaData = { nombre: 'Programa Actualizado' }
      await socialService.updatePrograma(1, programaData)
      const mockInstance = getMockInstance()
      expect(mockInstance.put).toHaveBeenCalledWith('/social/programas/1/', programaData)
    })

    it('deletePrograma calls correct endpoint', async () => {
      await socialService.deletePrograma(1)
      const mockInstance = getMockInstance()
      expect(mockInstance.delete).toHaveBeenCalledWith('/social/programas/1/')
    })

    it('getBeneficiarios calls correct endpoint', async () => {
      await socialService.getBeneficiarios()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/social/beneficiarios/')
    })

    it('createBeneficiario calls correct endpoint', async () => {
      const beneficiarioData = { persona: 1, programa: 1 }
      await socialService.createBeneficiario(beneficiarioData)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/social/beneficiarios/', beneficiarioData)
    })

    it('updateBeneficiario calls correct endpoint', async () => {
      const beneficiarioData = { programa: 2 }
      await socialService.updateBeneficiario(1, beneficiarioData)
      const mockInstance = getMockInstance()
      expect(mockInstance.put).toHaveBeenCalledWith('/social/beneficiarios/1/', beneficiarioData)
    })

    it('deleteBeneficiario calls correct endpoint', async () => {
      await socialService.deleteBeneficiario(1)
      const mockInstance = getMockInstance()
      expect(mockInstance.delete).toHaveBeenCalledWith('/social/beneficiarios/1/')
    })

    it('getActividadesSociales calls correct endpoint', async () => {
      await socialService.getActividadesSociales()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/social/actividades/')
    })

    it('createActividadSocial calls correct endpoint', async () => {
      const actividadData = { titulo: 'Actividad Test', descripcion: 'Descripción' }
      await socialService.createActividadSocial(actividadData)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/social/actividades/', actividadData)
    })

    it('updateActividadSocial calls correct endpoint', async () => {
      const actividadData = { titulo: 'Actividad Actualizada' }
      await socialService.updateActividadSocial(1, actividadData)
      const mockInstance = getMockInstance()
      expect(mockInstance.put).toHaveBeenCalledWith('/social/actividades/1/', actividadData)
    })

    it('deleteActividadSocial calls correct endpoint', async () => {
      await socialService.deleteActividadSocial(1)
      const mockInstance = getMockInstance()
      expect(mockInstance.delete).toHaveBeenCalledWith('/social/actividades/1/')
    })

    it('getCoberturas calls correct endpoint', async () => {
      await socialService.getCoberturas()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/social/coberturas/')
    })

    it('createCobertura calls correct endpoint', async () => {
      const coberturaData = { programa: 1, cantidad: 100 }
      await socialService.createCobertura(coberturaData)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/social/coberturas/', coberturaData)
    })

    it('updateCobertura calls correct endpoint', async () => {
      const coberturaData = { cantidad: 150 }
      await socialService.updateCobertura(1, coberturaData)
      const mockInstance = getMockInstance()
      expect(mockInstance.put).toHaveBeenCalledWith('/social/coberturas/1/', coberturaData)
    })

    it('deleteCobertura calls correct endpoint', async () => {
      await socialService.deleteCobertura(1)
      const mockInstance = getMockInstance()
      expect(mockInstance.delete).toHaveBeenCalledWith('/social/coberturas/1/')
    })

    it('getTiposAutoridad calls correct endpoint', async () => {
      await socialService.getTiposAutoridad()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/social/tipos-autoridad/')
    })

    it('createTipoAutoridad calls correct endpoint', async () => {
      const tipoData = { nombre: 'Tipo Test', descripcion: 'Descripción' }
      await socialService.createTipoAutoridad(tipoData)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/social/tipos-autoridad/', tipoData)
    })

    it('updateTipoAutoridad calls correct endpoint', async () => {
      const tipoData = { nombre: 'Tipo Actualizado' }
      await socialService.updateTipoAutoridad(1, tipoData)
      const mockInstance = getMockInstance()
      expect(mockInstance.put).toHaveBeenCalledWith('/social/tipos-autoridad/1/', tipoData)
    })

    it('deleteTipoAutoridad calls correct endpoint', async () => {
      await socialService.deleteTipoAutoridad(1)
      const mockInstance = getMockInstance()
      expect(mockInstance.delete).toHaveBeenCalledWith('/social/tipos-autoridad/1/')
    })

    it('getRolesAutoridad calls correct endpoint', async () => {
      await socialService.getRolesAutoridad()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/social/roles-autoridad/')
    })

    it('createRolAutoridad calls correct endpoint', async () => {
      const rolData = { nombre: 'Rol Test', descripcion: 'Descripción' }
      await socialService.createRolAutoridad(rolData)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/social/roles-autoridad/', rolData)
    })

    it('updateRolAutoridad calls correct endpoint', async () => {
      const rolData = { nombre: 'Rol Actualizado' }
      await socialService.updateRolAutoridad(1, rolData)
      const mockInstance = getMockInstance()
      expect(mockInstance.put).toHaveBeenCalledWith('/social/roles-autoridad/1/', rolData)
    })

    it('deleteRolAutoridad calls correct endpoint', async () => {
      await socialService.deleteRolAutoridad(1)
      const mockInstance = getMockInstance()
      expect(mockInstance.delete).toHaveBeenCalledWith('/social/roles-autoridad/1/')
    })

    it('getAutoridades calls correct endpoint', async () => {
      await socialService.getAutoridades()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/social/autoridades/')
    })

    it('createAutoridad calls correct endpoint', async () => {
      const autoridadData = { persona: 1, tipo_autoridad: 1, rol: 1 }
      await socialService.createAutoridad(autoridadData)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/social/autoridades/', autoridadData)
    })

    it('updateAutoridad calls correct endpoint', async () => {
      const autoridadData = { rol: 2 }
      await socialService.updateAutoridad(1, autoridadData)
      const mockInstance = getMockInstance()
      expect(mockInstance.put).toHaveBeenCalledWith('/social/autoridades/1/', autoridadData)
    })

    it('deleteAutoridad calls correct endpoint', async () => {
      await socialService.deleteAutoridad(1)
      const mockInstance = getMockInstance()
      expect(mockInstance.delete).toHaveBeenCalledWith('/social/autoridades/1/')
    })

    it('buscarPersona calls correct endpoint', async () => {
      await socialService.buscarPersona('123456789')
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/social/autoridades/buscar-persona/', { params: { numero_identificacion: '123456789' } })
    })

    it('getTiposActividad calls correct endpoint', async () => {
      await socialService.getTiposActividad()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/social/tipos-actividad/')
    })

    it('createTipoActividad calls correct endpoint', async () => {
      const tipoData = { nombre: 'Cultural', descripcion: 'Actividades culturales' }
      await socialService.createTipoActividad(tipoData)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/social/tipos-actividad/', tipoData)
    })

    it('updateTipoActividad calls correct endpoint', async () => {
      const tipoData = { nombre: 'Deportiva' }
      await socialService.updateTipoActividad(1, tipoData)
      const mockInstance = getMockInstance()
      expect(mockInstance.put).toHaveBeenCalledWith('/social/tipos-actividad/1/', tipoData)
    })

    it('deleteTipoActividad calls correct endpoint', async () => {
      await socialService.deleteTipoActividad(1)
      const mockInstance = getMockInstance()
      expect(mockInstance.delete).toHaveBeenCalledWith('/social/tipos-actividad/1/')
    })

    it('getEstadosActividad calls correct endpoint', async () => {
      await socialService.getEstadosActividad()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/social/estados-actividad/')
    })

    it('createEstadoActividad calls correct endpoint', async () => {
      const estadoData = { nombre: 'Programada', descripcion: 'Actividad programada', color: '#007bff' }
      await socialService.createEstadoActividad(estadoData)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/social/estados-actividad/', estadoData)
    })

    it('updateEstadoActividad calls correct endpoint', async () => {
      const estadoData = { nombre: 'En Curso' }
      await socialService.updateEstadoActividad(1, estadoData)
      const mockInstance = getMockInstance()
      expect(mockInstance.put).toHaveBeenCalledWith('/social/estados-actividad/1/', estadoData)
    })

    it('deleteEstadoActividad calls correct endpoint', async () => {
      await socialService.deleteEstadoActividad(1)
      const mockInstance = getMockInstance()
      expect(mockInstance.delete).toHaveBeenCalledWith('/social/estados-actividad/1/')
    })

    it('getActividadesComunitarias calls correct endpoint', async () => {
      await socialService.getActividadesComunitarias()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/social/actividades-comunitarias/')
    })

    it('createActividadComunitaria calls correct endpoint', async () => {
      const actividadData = { titulo: 'Actividad Test', descripcion: 'Descripción', tipo_actividad: 1, estado: 1 }
      await socialService.createActividadComunitaria(actividadData)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/social/actividades-comunitarias/', actividadData)
    })

    it('updateActividadComunitaria calls correct endpoint', async () => {
      const actividadData = { titulo: 'Actividad Actualizada' }
      await socialService.updateActividadComunitaria(1, actividadData)
      const mockInstance = getMockInstance()
      expect(mockInstance.put).toHaveBeenCalledWith('/social/actividades-comunitarias/1/', actividadData)
    })

    it('deleteActividadComunitaria calls correct endpoint', async () => {
      await socialService.deleteActividadComunitaria(1)
      const mockInstance = getMockInstance()
      expect(mockInstance.delete).toHaveBeenCalledWith('/social/actividades-comunitarias/1/')
    })

    it('registrarAsistencia calls correct endpoint', async () => {
      const asistenciaData = { persona_id: 1, confirmado: true }
      await socialService.registrarAsistencia(1, asistenciaData)
      const mockInstance = getMockInstance()
      expect(mockInstance.post).toHaveBeenCalledWith('/social/actividades-comunitarias/1/registrar-asistencia/', asistenciaData)
    })

    it('getEstadisticasActividad calls correct endpoint', async () => {
      await socialService.getEstadisticasActividad(1)
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/social/actividades-comunitarias/1/estadisticas/')
    })

    it('getCalendarioActividades calls correct endpoint', async () => {
      await socialService.getCalendarioActividades({ mes: 12, año: 2024 })
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/social/actividades-comunitarias/calendario/', { params: { mes: 12, año: 2024 } })
    })

    it('getAsistencias calls correct endpoint', async () => {
      await socialService.getAsistencias()
      const mockInstance = getMockInstance()
      expect(mockInstance.get).toHaveBeenCalledWith('/social/asistencias-actividad/')
    })
  })
})
