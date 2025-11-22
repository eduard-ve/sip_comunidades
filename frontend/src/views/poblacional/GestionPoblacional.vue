<template>
  <div class="gestion-poblacional-container">
    <!-- KPIs Section -->
    <div class="kpis-section">
      <div class="kpis-grid">
        <KpiCard
          v-for="kpi in kpis"
          :key="kpi.title"
          :title="kpi.title"
          :value="kpi.value"
          :change="kpi.change"
          :icon="kpi.icon"
          :color="kpi.color"
        />
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Filter Sidebar -->
      <div class="filter-section">
        <FilterSidebar
          :ocupaciones="ocupaciones"
          :niveles-educativos="nivelesEducativos"
          :estados-civiles="estadosCiviles"
          :lenguas="lenguas"
          @filtro-cambio="aplicarFiltros"
          @filtros-limpios="limpiarFiltros"
        />
      </div>

      <!-- Content Area -->
      <div class="content-section">
        <!-- Vista Selector -->
        <VistaSelector
          :personas="people"
          :personas-filtradas="personasFiltradas"
          :relaciones-familiares="relacionesFamiliares"
          :grupos-etnicos="gruposFamiliares"
          :distribucion-genero="distribucionGenero"
          :top-ocupaciones="topOcupaciones"
          :distribucion-educativa="distribucionEducativa"
          :lenguas-maternas="lenguasMaternas"
          :distribucion-edad="distribucionEdad"
          :cargando="cargando"
          @vista-cambiada="cambiarVista"
          @ver-detalle="verDetallePersona"
          @ver-arbol-familiar="verArbolFamiliar"
          @editar-persona="editarPersona"
          @eliminar-persona="eliminarPersona"
          @filtrar-ocupacion="filtrarPorOcupacion"
        />

        <!-- Botones de acción -->
        <div class="action-buttons">
          <button @click="showForm = true" class="btn btn-primary">
            <i class="bi bi-plus-circle me-2"></i>Nuevo Individuo
          </button>
          <button @click="exportarDatos" class="btn btn-success">
            <i class="bi bi-download me-2"></i>Exportar Datos
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- BaseModule original (comentado para referencia) -->
  <!--
  <BaseModule
    title="Gestión de Individuos"
    icon="bi bi-people"
    :kpis="kpis"
    :charts="charts"
    :showCreate="true"
    :showExport="false"
    :table="{ columns: tableColumns, rows: people }"
    :showSearch="true"
    :showEmptyMessage="true"
    :forceTable="true"
    @create="showForm = true"
  >
  </div>

  <!-- BaseModule original (comentado para referencia) -->
  <!--
    <template #table-cell="{ column, row }">
      <div>
        <div v-if="column.key === 'acciones'" class="d-flex gap-1">
          <button class="btn btn-sm btn-outline-primary" @click="editPersonByRow(row)">
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-sm btn-outline-danger" @click="deletePersonByRow(row)">
            <i class="bi bi-trash"></i>
          </button>
        </div>
        <span v-else-if="column.key === 'nombre_completo'">{{ row.nombre_completo }}</span>
        <span v-else-if="column.key === 'tipo_identificacion'">{{ row.tipo_identificacion_nombre }}</span>
        <span v-else-if="column.key === 'nivel_educativo'">{{ row.nivel_educativo_nombre }}</span>
        <span v-else-if="column.key === 'ocupacion'">{{ row.ocupacion_nombre }}</span>
        <span v-else-if="column.key === 'estado_civil'">{{ row.estado_civil_nombre }}</span>
        <span v-else>{{ row[column.key] }}</span>
      </div>
    </template>

    <template #extra>
      <div class="row g-3">
        <div class="col-md-6">
          <ServicesMap />
        </div>
        <div class="col-md-6">
          <div class="card shadow-sm border-0 p-3">
            <h6 class="fw-bold">🏠 Composición Familiar</h6>
            <ul class="list-unstyled">
              <li v-for="(member, index) in familyTree" :key="index">
                <i class="bi bi-person me-2"></i>{{ member.name }} - <small>{{ member.relation }}</small>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </template>
  </BaseModule>
  -->

  <!-- Modal formulario -->
  <div v-if="showForm" class="modal-backdrop">
    <div class="modal-card">
      <h5 class="mb-3">{{ editIndex !== null ? 'Editar Individuo' : 'Nuevo Individuo' }}</h5>
      <form @submit.prevent="savePerson">
        <div class="row g-3">
          <!-- Primera fila: Tipo ID y Número ID -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">Tipo de Identificación</label>
            <select v-model="form.tipo_identificacion" class="form-select form-select-sm" required>
              <option value="">Seleccionar tipo</option>
              <option v-for="tipo in tiposIdentificacion" :key="tipo.id" :value="tipo.id">{{ tipo.nombre }}</option>
            </select>
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">Número de Identificación</label>
            <input v-model="form.numero_identificacion" class="form-control form-control-sm" placeholder="Ej: 1234567890" required />
          </div>

          <!-- Segunda fila: Primer nombre y Segundo nombre -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">Primer Nombre</label>
            <input v-model="form.primer_nombre" class="form-control form-control-sm" placeholder="Nombre principal" required />
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">Segundo Nombre</label>
            <input v-model="form.segundo_nombre" class="form-control form-control-sm" placeholder="Segundo nombre (opcional)" />
          </div>

          <!-- Tercera fila: Primer apellido y Segundo apellido -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">Primer Apellido</label>
            <input v-model="form.primer_apellido" class="form-control form-control-sm" placeholder="Apellido paterno" required />
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">Segundo Apellido</label>
            <input v-model="form.segundo_apellido" class="form-control form-control-sm" placeholder="Apellido materno (opcional)" />
          </div>

          <!-- Cuarta fila: Fecha nacimiento y Género -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">Fecha de Nacimiento</label>
            <input v-model="form.fecha_nacimiento" type="date" class="form-control form-control-sm" required />
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">Género</label>
            <select v-model="form.genero" class="form-select form-select-sm" required>
              <option value="">Seleccionar género</option>
              <option value="M"> Masculino</option>
              <option value="F"> Femenino</option>
              <option value="O">🏳️ Otro</option>
            </select>
          </div>

          <!-- Quinta fila: Dirección completa -->
          <div class="col-12">
            <label class="form-label fw-semibold">Dirección</label>
            <input v-model="form.direccion" class="form-control form-control-sm" placeholder="Dirección completa de residencia" />
          </div>

          <!-- Sexta fila: Nivel educativo y Ocupación -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">Nivel Educativo</label>
            <select v-model="form.nivel_educativo" class="form-select form-select-sm" required>
              <option value="">Seleccionar nivel</option>
              <option v-for="nivel in nivelesEducativos" :key="nivel.id" :value="nivel.id">{{ nivel.nombre }}</option>
            </select>
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">Ocupación</label>
            <select v-model="form.ocupacion" class="form-select form-select-sm" required>
              <option value="">Seleccionar ocupación</option>
              <option v-for="ocup in ocupaciones" :key="ocup.id" :value="ocup.id">{{ ocup.nombre }}</option>
            </select>
          </div>

          <!-- Séptima fila: Grupo familiar y Estado civil -->
          <div class="col-md-6">
            <label class="form-label fw-semibold">Grupo Familiar</label>
            <select v-model="form.grupo_familiar" class="form-select form-select-sm">
              <option value="">Seleccionar grupo</option>
              <option v-for="grupo in gruposFamiliares" :key="grupo.id" :value="grupo.id">{{ grupo.nombre }}</option>
            </select>
          </div>

          <div class="col-md-6">
            <label class="form-label fw-semibold">Estado Civil</label>
            <select v-model="form.estado_civil" class="form-select form-select-sm">
              <option value="">Seleccionar estado</option>
              <option v-for="estado in estadosCiviles" :key="estado.id" :value="estado.id">{{ estado.nombre }}</option>
            </select>
          </div>

          <!-- Octava fila: Lengua materna -->
          <div class="col-12">
            <label class="form-label fw-semibold">Lengua Materna</label>
            <select v-model="form.lengua_materna" class="form-select form-select-sm">
              <option value="">Seleccionar lengua</option>
              <option v-for="lengua in lenguas" :key="lengua.id" :value="lengua.id">{{ lengua.nombre }}</option>
            </select>
          </div>
        </div>

        <div class="d-flex justify-content-end mt-4 pt-3 border-top">
          <button type="button" class="btn btn-outline-secondary btn-sm me-2" @click="closeForm">
            <i class="bi bi-x-circle me-1"></i>Cancelar
          </button>
          <button type="submit" class="btn btn-primary btn-sm">
            <i class="bi bi-check-circle me-1"></i>{{ editIndex !== null ? 'Actualizar Individuo' : 'Crear Individuo' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import KpiCard from '../../components/tarjetas/KpiCard.vue'
import FilterSidebar from '../../components/modulos/FilterSidebar.vue'
import VistaSelector from '../../components/modulos/VistaSelector.vue'
import { poblacionService } from '../../services/api.js'
import * as XLSX from 'xlsx'
import '../../assets/css/GestionPoblacional.css'

// KPIs dinámicos principales (5 KPIs)
const kpis = ref([
  { title: 'Población Total', value: '0', change: '0%', icon: 'bi bi-people-fill', color: 'primary' },
  { title: 'Edad Promedio', value: '0 años', change: '0.0', icon: 'bi bi-calendar-event', color: 'info' },
  { title: 'Tasa Alfabetismo', value: '0%', change: '0%', icon: 'bi bi-book', color: 'success' },
  { title: 'Ocupación Principal', value: 'N/A', change: '0%', icon: 'bi bi-briefcase', color: 'warning' },
  { title: 'Crecimiento Poblacional', value: '0%', change: '0%', icon: 'bi bi-graph-up', color: 'secondary' }
])

// Gráficas
const charts = {
  left: {
    id: 'populationTrend',
    type: 'line',
    title: '📈 Tendencia de Población',
    data: {
      labels: ['2019', '2020', '2021', '2022', '2023'],
      datasets: [{ label:'Población', data:[11000,11250,11500,12000,12450], borderColor:'#0d6efd', backgroundColor:'rgba(13,110,253,0.3)', fill:true }]
    }
  },
  right: {
    id: 'pyramid',
    type: 'bar',
    title: 'Pirámide Poblacional',
    data: {
      labels:['0-4','5-9','10-14','15-19','20-24','25-29','30-34','35-39','40-44'],
      datasets:[
        { label:'Hombres', data:[-500,-600,-800,-700,-650,-500,-400,-300,-200], backgroundColor:'rgba(13,110,253,0.7)' },
        { label:'Mujeres', data:[480,620,780,720,660,540,420,310,210], backgroundColor:'rgba(220,53,69,0.7)' }
      ]
    },
    options:{ indexAxis:'y', scales:{ x:{ stacked:true, ticks:{ callback:v=>Math.abs(v)} }, y:{ stacked:true } } }
  }
}

// Columnas de la tabla con Acciones
const tableColumns = [
   { key:'nombre_completo', label:'Nombre Completo' },
   { key:'tipo_identificacion', label:'Tipo Identificacion' },
   { key:'numero_identificacion', label:'Número Identificacion' },
   { key:'fecha_nacimiento', label:'Fecha Nacimiento' },
   { key:'genero', label:'Género' },
   { key:'nivel_educativo', label:'Nivel Educativo' },
   { key:'ocupacion', label:'Ocupación' },
   { key:'estado_civil', label:'Estado Civil' },
   { key:'direccion', label:'Dirección' },
   { key:'acciones', label:'Acciones' }
]

const people = ref([])
const personasFiltradas = ref([])
const relacionesFamiliares = ref([])

// Estadísticas para gráficas
const distribucionGenero = ref([])
const topOcupaciones = ref([])
const distribucionEducativa = ref([])
const lenguasMaternas = ref([])
const distribucionEdad = ref([])

// Estados
const cargando = ref(false)
const filtrosActuales = ref({})

// Datos select
const tiposIdentificacion = ref([])
const nivelesEducativos = ref([])
const ocupaciones = ref([])
const gruposFamiliares = ref([])
const estadosCiviles = ref([])
const lenguas = ref([])

// Modal
const showForm = ref(false)
const form = ref({ tipo_identificacion:'', numero_identificacion:'', primer_nombre:'', segundo_nombre:'', primer_apellido:'', segundo_apellido:'', fecha_nacimiento:'', genero:'', direccion:'', nivel_educativo:'', ocupacion:'', grupo_familiar:'', estado_civil:'', lengua_materna:'' })
const editIndex = ref(null)

function closeForm(){
  showForm.value=false
  editIndex.value=null
  form.value={ tipo_identificacion:'', numero_identificacion:'', primer_nombre:'', segundo_nombre:'', primer_apellido:'', segundo_apellido:'', fecha_nacimiento:'', genero:'', direccion:'', nivel_educativo:'', ocupacion:'', grupo_familiar:'', estado_civil:'', lengua_materna:'' }
}

async function savePerson(){
    try {
       if(editIndex.value!==null) {
          const response = await poblacionService.updatePersona(form.value.id, form.value)
          // Actualizar la persona en el array
          const index = people.value.findIndex(p => p.id === form.value.id)
          if (index !== -1) {
              people.value[index] = response.data
          }
          // Actualizar también en personasFiltradas si existe
          const filteredIndex = personasFiltradas.value.findIndex(p => p.id === form.value.id)
          if (filteredIndex !== -1) {
              personasFiltradas.value[filteredIndex] = response.data
          }
       } else {
          const response = await poblacionService.createPersona(form.value)
          people.value.push(response.data)
          // Agregar también a personasFiltradas si no hay filtros activos
          if (Object.keys(filtrosActuales.value).length === 0) {
              personasFiltradas.value.push(response.data)
          }
       }
       // Recargar estadísticas después de guardar
       await cargarEstadisticas()
       closeForm()
    } catch (error) {
       console.error('Error saving person:', error)
       alert('Error al guardar la persona')
    }
}

function editPersonByRow(row){
  editIndex.value=people.value.indexOf(row)
  form.value={...row}
  showForm.value=true
}

async function deletePersonByRow(row){
    if(confirm('¿Seguro que deseas eliminar este registro?')) {
       try {
          await poblacionService.deletePersona(row.id)
          // Eliminar de people
          const idx = people.value.indexOf(row)
          if(idx !== -1) people.value.splice(idx, 1)

          // Eliminar también de personasFiltradas
          const filteredIdx = personasFiltradas.value.indexOf(row)
          if(filteredIdx !== -1) personasFiltradas.value.splice(filteredIdx, 1)

          // Recargar estadísticas después de eliminar
          await cargarEstadisticas()
       } catch (error) {
          console.error('Error deleting person:', error)
          alert('Error al eliminar la persona')
       }
    }
}

// Composición familiar
const familyTree = ref([{ name:'Juan Pérez', relation:'Padre' },{ name:'Ana Gómez', relation:'Madre' },{ name:'Pedro Pérez', relation:'Hijo' }])

// Función para cargar estadísticas dinámicas
async function cargarEstadisticas() {
    try {
        const statsResponse = await poblacionService.getEstadisticas()
        const stats = statsResponse.data

        // Calcular estadísticas adicionales
        const distribucionEdadResponse = await poblacionService.getDistribucionEdad()
        const distribucionEdadData = distribucionEdadResponse.data
        distribucionEdad.value = distribucionEdadData
        const menores5 = distribucionEdadData.find(item => item.rango_edad === '0-5')?.cantidad || 0
        const mayores65 = distribucionEdadData.find(item => item.rango_edad === '66+')?.cantidad || 0

        const distribucionEducativaResponse = await poblacionService.getDistribucionEducativa()
        const distribucionEducativaData = distribucionEducativaResponse.data
        distribucionEducativa.value = distribucionEducativaData
        const analfabetos = distribucionEducativaData.find(item => item.nivel.toLowerCase().includes('analfabeto'))?.cantidad || 0

        // Cargar otras estadísticas para gráficas
        const distribucionGeneroResponse = await poblacionService.getDistribucionGenero()
        distribucionGenero.value = distribucionGeneroResponse.data

        const topOcupacionesResponse = await poblacionService.getTopOcupaciones()
        topOcupaciones.value = topOcupacionesResponse.data

        const lenguasMaternasResponse = await poblacionService.getLenguasMaternas()
        lenguasMaternas.value = lenguasMaternasResponse.data

        // Actualizar KPIs dinámicos principales (5 KPIs)
        kpis.value = [
            {
                title: 'Población Total',
                value: stats.poblacion_total?.toLocaleString() || '0',
                change: '+2.5%',
                icon: 'bi bi-people-fill',
                color: 'primary'
            },
            {
                title: 'Edad Promedio',
                value: `${stats.edad_promedio || 0} años`,
                change: '+0.2',
                icon: 'bi bi-calendar-event',
                color: 'info'
            },
            {
                title: 'Tasa Alfabetismo',
                value: `${stats.tasa_alfabetismo || 0}%`,
                change: '+1.2%',
                icon: 'bi bi-book',
                color: stats.tasa_alfabetismo >= 80 ? 'success' : 'warning'
            },
            {
                title: 'Ocupación Principal',
                value: stats.ocupacion_principal || 'N/A',
                change: '0.0%',
                icon: 'bi bi-briefcase',
                color: 'warning'
            },
            {
                title: 'Crecimiento Poblacional',
                value: `${stats.crecimiento_poblacional || 0}%`,
                change: '+0.1%',
                icon: 'bi bi-graph-up',
                color: 'secondary'
            }
        ]
    } catch (error) {
        console.error('Error cargando estadísticas:', error)
        // En caso de error, mantener valores por defecto
    }
}

// Función para aplicar filtros
function aplicarFiltros(filtros) {
    filtrosActuales.value = filtros
    filtrarPersonas()
}

// Función para limpiar filtros
function limpiarFiltros() {
    filtrosActuales.value = {}
    personasFiltradas.value = [...people.value]
}

// Función para filtrar personas
function filtrarPersonas() {
    let filtradas = [...people.value]

    // Filtro por edad
    if (filtrosActuales.value.edad_min || filtrosActuales.value.edad_max) {
        const minEdad = filtrosActuales.value.edad_min || 0
        const maxEdad = filtrosActuales.value.edad_max || 120
        filtradas = filtradas.filter(persona => {
            const edad = calcularEdad(persona.fecha_nacimiento)
            return edad >= minEdad && edad <= maxEdad
        })
    }

    // Filtro por género
    if (filtrosActuales.value.genero && filtrosActuales.value.genero.length > 0) {
        filtradas = filtradas.filter(persona => filtrosActuales.value.genero.includes(persona.genero))
    }

    // Filtro por ocupación
    if (filtrosActuales.value.ocupacion_id) {
        filtradas = filtradas.filter(persona => persona.ocupacion == filtrosActuales.value.ocupacion_id)
    }

    // Filtro por nivel educativo
    if (filtrosActuales.value.nivel_educativo_id) {
        filtradas = filtradas.filter(persona => persona.nivel_educativo == filtrosActuales.value.nivel_educativo_id)
    }

    // Filtro por estado civil
    if (filtrosActuales.value.estado_civil_ids && filtrosActuales.value.estado_civil_ids.length > 0) {
        filtradas = filtradas.filter(persona => filtrosActuales.value.estado_civil_ids.includes(persona.estado_civil))
    }

    // Filtro por lengua materna
    if (filtrosActuales.value.lengua_id) {
        filtradas = filtradas.filter(persona => persona.lengua_materna == filtrosActuales.value.lengua_id)
    }

    personasFiltradas.value = filtradas
}

// Función auxiliar para calcular edad
function calcularEdad(fechaNacimiento) {
    if (!fechaNacimiento) return 0
    const hoy = new Date()
    const nacimiento = new Date(fechaNacimiento)
    let edad = hoy.getFullYear() - nacimiento.getFullYear()
    const mes = hoy.getMonth() - nacimiento.getMonth()
    if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
        edad--
    }
    return edad
}

// Funciones para eventos de componentes
function cambiarVista(vista) {
    // Lógica para cambiar vista si es necesario
    console.log('Vista cambiada a:', vista)
}

function verDetallePersona(persona) {
    // Mostrar modal de detalles
    console.log('Ver detalle de:', persona)
}

function verArbolFamiliar(persona) {
    // Cambiar a vista de árbol familiar
    console.log('Ver árbol familiar de:', persona)
}

function editarPersona(persona) {
    editIndex.value = people.value.findIndex(p => p.id === persona.id)
    form.value = { ...persona }
    showForm.value = true
}

async function eliminarPersona(persona) {
    if(confirm(`¿Seguro que deseas eliminar a ${persona.nombre_completo}?`)) {
       try {
          await poblacionService.deletePersona(persona.id)

          // Eliminar de people
          const idx = people.value.findIndex(p => p.id === persona.id)
          if(idx !== -1) people.value.splice(idx, 1)

          // Eliminar también de personasFiltradas
          const filteredIdx = personasFiltradas.value.findIndex(p => p.id === persona.id)
          if(filteredIdx !== -1) personasFiltradas.value.splice(filteredIdx, 1)

          // Recargar estadísticas después de eliminar
          await cargarEstadisticas()

          alert('Persona eliminada exitosamente')
       } catch (error) {
          console.error('Error deleting person:', error)
          alert('Error al eliminar la persona')
       }
    }
}

function filtrarPorOcupacion(ocupacion) {
    filtrosActuales.value.ocupacion_id = ocupacion
    filtrarPersonas()
}

async function exportarDatos() {
    try {
        // Obtener datos filtrados
        const datosFiltrados = personasFiltradas.value.length > 0 ? personasFiltradas.value : people.value

        if (datosFiltrados.length === 0) {
            alert('No hay datos para exportar')
            return
        }

        // Crear datos para Excel
        const datosExcel = datosFiltrados.map(persona => ({
            'ID': persona.numero_identificacion,
            'Nombre Completo': persona.nombre_completo,
            'Fecha Nacimiento': persona.fecha_nacimiento,
            'Edad': calcularEdad(persona.fecha_nacimiento),
            'Género': persona.genero === 'M' ? 'Masculino' : persona.genero === 'F' ? 'Femenino' : 'Otro',
            'Dirección': persona.direccion || '',
            'Nivel Educativo': persona.nivel_educativo_nombre || '',
            'Ocupación': persona.ocupacion_nombre || '',
            'Estado Civil': persona.estado_civil_nombre || '',
            'Lengua Materna': persona.lengua_materna_nombre || '',
            'Grupo Familiar': persona.grupo_familiar_nombre || ''
        }))

        // Crear archivo Excel
        const ws = XLSX.utils.json_to_sheet(datosExcel)
        const wb = XLSX.utils.book_new()
        XLSX.utils.book_append_sheet(wb, ws, 'Personas')

        // Descargar archivo
        const fecha = new Date().toISOString().split('T')[0]
        XLSX.writeFile(wb, `poblacion_${fecha}.xlsx`)

    } catch (error) {
        console.error('Error exportando datos:', error)
        alert('Error al exportar los datos')
    }
}

// Cargar datos al montar el componente
onMounted(async () => {
    try {
        // Cargar estadísticas dinámicas
        await cargarEstadisticas()

        // Cargar personas
        const personasResponse = await poblacionService.getPersonas()
        people.value = personasResponse.data
        personasFiltradas.value = [...people.value] // Inicializar filtradas

        // Cargar catálogos
        const [tiposId, nivelesEdu, ocup, gruposFam, estadosCiv, leng] = await Promise.all([
            poblacionService.getTiposIdentificacion(),
            poblacionService.getNivelesEducativos(),
            poblacionService.getOcupaciones(),
            poblacionService.getGruposFamiliares(),
            poblacionService.getEstadosCiviles(),
            poblacionService.getLenguas()
        ])

        tiposIdentificacion.value = tiposId.data
        nivelesEducativos.value = nivelesEdu.data
        ocupaciones.value = ocup.data
        gruposFamiliares.value = gruposFam.data
        estadosCiviles.value = estadosCiv.data
        lenguas.value = leng.data
    } catch (error) {
        console.error('Error loading data:', error)
    }
})
</script>

<style scoped>
.gestion-poblacional-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.kpis-section {
  padding: 1.5rem;
  background: white;
  border-bottom: 1px solid #e9ecef;
}

.kpis-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
  align-items: stretch;
  max-width: 1400px;
  margin: 0 auto;
}

.main-content {
  display: flex;
  min-height: calc(100vh - 200px);
}

.filter-section {
  width: 300px;
  background: white;
  border-right: 1px solid #e9ecef;
  flex-shrink: 0;
}

.content-section {
  flex: 1;
  padding: 1.5rem;
  position: relative;
}

.action-buttons {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  display: flex;
  gap: 0.5rem;
  z-index: 100;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
  transform: translateY(-1px);
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover {
  background: #1e7e34;
  transform: translateY(-1px);
}

/* Modal styles */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.modal-card {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }

  .filter-section {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #e9ecef;
  }

  .kpis-grid {
    flex-direction: column;
    align-items: center;
  }

  .action-buttons {
    position: static;
    margin-top: 1rem;
    justify-content: center;
  }

  .btn {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 1024px) {
  .kpis-grid {
    justify-content: space-around;
  }
}
</style>
