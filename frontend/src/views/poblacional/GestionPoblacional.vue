<template>
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
    <!-- Personalización de celdas de la tabla -->
    <template #table-cell="{ column, row }">
      <div>
        <!-- Columna de Acciones -->
        <div v-if="column.key === 'acciones'" class="d-flex gap-1">
          <button class="btn btn-sm btn-outline-primary" @click="editPersonByRow(row)">
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-sm btn-outline-danger" @click="deletePersonByRow(row)">
            <i class="bi bi-trash"></i>
          </button>
        </div>

        <!-- Otras columnas -->
        <span v-else-if="column.key === 'nombre_completo'">
           {{ row.nombre_completo }}
        </span>
        <span v-else-if="column.key === 'tipo_identificacion'">
           {{ row.tipo_identificacion_nombre }}
        </span>
        <span v-else-if="column.key === 'nivel_educativo'">
           {{ row.nivel_educativo_nombre }}
        </span>
        <span v-else-if="column.key === 'ocupacion'">
           {{ row.ocupacion_nombre }}
        </span>
        <span v-else-if="column.key === 'estado_civil'">
           {{ row.estado_civil_nombre }}
        </span>
        <span v-else>
           {{ row[column.key] }}
        </span>
      </div>
    </template>

    <!-- Extra: Mapa y Composición familiar -->
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
              <option value="M">👨 Masculino</option>
              <option value="F">👩 Femenino</option>
              <option value="O">🏳️‍🌈 Otro</option>
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
import { ref, onMounted } from 'vue'
import BaseModule from '../../components/comun/BaseModule.vue'
import ServicesMap from '../../components/mapas/ServicesMap.vue'
import { poblacionService } from '../../services/api.js'
import '../../assets/css/GestionPoblacional.css'

// KPIs
const kpis = ref([
  { title: 'Población Total', value: '0', change: '0', icon: 'bi bi-people-fill' },
  { title: 'Nacimientos', value: '0', change: '0', icon: 'bi bi-person-plus-fill' },
  { title: 'Defunciones', value: '0', change: '0', icon: 'bi bi-person-dash-fill' },
  { title: 'Crecimiento', value: '0%', change: '0', icon: 'bi bi-graph-up' }
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
         people.value[editIndex.value] = response.data
      } else {
         const response = await poblacionService.createPersona(form.value)
         people.value.push(response.data)
      }
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
         const idx = people.value.indexOf(row)
         if(idx !== -1) people.value.splice(idx, 1)
      } catch (error) {
         console.error('Error deleting person:', error)
         alert('Error al eliminar la persona')
      }
   }
}

// Composición familiar
const familyTree = ref([{ name:'Juan Pérez', relation:'Padre' },{ name:'Ana Gómez', relation:'Madre' },{ name:'Pedro Pérez', relation:'Hijo' }])

// Cargar datos al montar el componente
onMounted(async () => {
    try {
       // Cargar estadísticas para KPIs
       const statsResponse = await poblacionService.getPopulationStats()
       const stats = statsResponse.data

       // Actualizar KPIs con datos del backend
       kpis.value = [
          {
             title: 'Población Total',
             value: stats.total_population.toLocaleString(),
             change: '2.5',
             icon: 'bi bi-people-fill'
          },
          {
             title: 'Nacimientos',
             value: stats.births.toLocaleString(),
             change: '1.2',
             icon: 'bi bi-person-plus-fill'
          },
          {
             title: 'Defunciones',
             value: stats.deaths.toLocaleString(),
             change: '-0.5',
             icon: 'bi bi-person-dash-fill'
          },
          {
             title: 'Crecimiento',
             value: `${stats.growth_rate}%`,
             change: '0.3',
             icon: 'bi bi-graph-up'
          }
       ]

       // Cargar personas
       const personasResponse = await poblacionService.getPersonas()
       people.value = personasResponse.data

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
