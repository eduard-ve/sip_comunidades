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
          {{ row.primer_nombre }} {{ row.segundo_nombre }}
        </span>
        <span v-else-if="column.key === 'apellido_completo'">
          {{ row.primer_apellido }} {{ row.segundo_apellido }}
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
        <div class="mb-2">
          <label class="form-label">Tipo de Identificación</label>
          <select v-model="form.tipo_identificacion_id" class="form-select" required>
            <option value="">Seleccione...</option>
            <option v-for="tipo in tiposIdentificacion" :key="tipo.id" :value="tipo.id">{{ tipo.nombre }}</option>
          </select>
        </div>

        <input v-model="form.numero_identificacion" class="form-control mb-2" placeholder="Número de Identificación" required />
        <input v-model="form.primer_nombre" class="form-control mb-2" placeholder="Primer Nombre" required />
        <input v-model="form.segundo_nombre" class="form-control mb-2" placeholder="Segundo Nombre" />
        <input v-model="form.primer_apellido" class="form-control mb-2" placeholder="Primer Apellido" required />
        <input v-model="form.segundo_apellido" class="form-control mb-2" placeholder="Segundo Apellido" />
        <input v-model="form.fecha_nacimiento" type="date" class="form-control mb-2" placeholder="Fecha de Nacimiento" required />

        <select v-model="form.genero" class="form-select mb-2" required>
          <option value="">Seleccione Género...</option>
          <option value="M">Masculino</option>
          <option value="F">Femenino</option>
          <option value="O">Otro</option>
        </select>

        <input v-model="form.direccion" class="form-control mb-2" placeholder="Dirección" />

        <div class="d-flex gap-2 mb-3">
          <select v-model="form.nivel_educativo_id" class="form-select" required>
            <option value="">Nivel Educativo</option>
            <option v-for="nivel in nivelesEducativos" :key="nivel.id" :value="nivel.id">{{ nivel.nombre }}</option>
          </select>

          <select v-model="form.ocupacion_id" class="form-select" required>
            <option value="">Ocupación</option>
            <option v-for="ocup in ocupaciones" :key="ocup.id" :value="ocup.id">{{ ocup.nombre }}</option>
          </select>
        </div>

        <div class="d-flex gap-2 mb-3">
          <select v-model="form.grupo_familiar_id" class="form-select">
            <option value="">Grupo Familiar</option>
            <option v-for="grupo in gruposFamiliares" :key="grupo.id" :value="grupo.id">{{ grupo.nombre }}</option>
          </select>

          <select v-model="form.estado_civil_id" class="form-select">
            <option value="">Estado Civil</option>
            <option v-for="estado in estadosCiviles" :key="estado.id" :value="estado.id">{{ estado.nombre }}</option>
          </select>
        </div>

        <select v-model="form.lengua_materna_id" class="form-select mb-3">
          <option value="">Lengua Materna</option>
          <option v-for="lengua in lenguas" :key="lengua.id" :value="lengua.id">{{ lengua.nombre }}</option>
        </select>

        <div class="text-end">
          <button type="button" class="btn btn-secondary btn-sm me-2" @click="closeForm">Cancelar</button>
          <button type="submit" class="btn btn-primary btn-sm">Guardar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BaseModule from '../components/BaseModule.vue'
import ServicesMap from '../components/ServicesMap.vue'

// KPIs
const kpis = [
  { title: 'Población Total', value: '12,450', change: '2.5', icon: 'bi bi-people-fill' },
  { title: 'Nacimientos', value: '340', change: '1.2', icon: 'bi bi-person-plus-fill' },
  { title: 'Defunciones', value: '120', change: '-0.5', icon: 'bi bi-person-dash-fill' },
  { title: 'Crecimiento', value: '2.1%', change: '0.3', icon: 'bi bi-graph-up' }
]

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
  { key:'nombre_completo', label:'Nombres' },
  { key:'apellido_completo', label:'Apellidos' },
  { key:'tipo_identificacion_id', label:'Tipo ID' },
  { key:'numero_identificacion', label:'Número ID' },
  { key:'fecha_nacimiento', label:'Fecha Nacimiento' },
  { key:'genero', label:'Género' },
  { key:'direccion', label:'Dirección' },
  { key:'acciones', label:'Acciones' }
]

const people = ref([])

// Datos select
const tiposIdentificacion = ref([{ id:1,nombre:'Cédula' },{ id:2,nombre:'Targeta de Identidad' }])
const nivelesEducativos = ref([{ id:1,nombre:'Primaria' },{ id:2,nombre:'Secundaria' }, { id:3,nombre:'Universitario' }])
const ocupaciones = ref([{ id:1,nombre:'Desempleado' },{ id:2,nombre:'Profesor' }, { id:3,nombre:'Pescador' }, { id:4,nombre:'Agricultor' }])
const gruposFamiliares = ref([{ id:1,nombre:'Familia A' },{ id:2,nombre:'Familia B' }])
const estadosCiviles = ref([{ id:1,nombre:'Soltero' },{ id:2,nombre:'Casado' }])
const lenguas = ref([{ id:1,nombre:'Siriano' },{ id:2,nombre:'Desano' }])

// Modal
const showForm = ref(false)
const form = ref({ tipo_identificacion_id:'', numero_identificacion:'', primer_nombre:'', segundo_nombre:'', primer_apellido:'', segundo_apellido:'', fecha_nacimiento:'', genero:'', direccion:'', nivel_educativo_id:'', ocupacion_id:'', grupo_familiar_id:'', estado_civil_id:'', lengua_materna_id:'' })
const editIndex = ref(null)

function closeForm(){
  showForm.value=false
  editIndex.value=null
  form.value={ tipo_identificacion_id:'', numero_identificacion:'', primer_nombre:'', segundo_nombre:'', primer_apellido:'', segundo_apellido:'', fecha_nacimiento:'', genero:'', direccion:'', nivel_educativo_id:'', ocupacion_id:'', grupo_familiar_id:'', estado_civil_id:'', lengua_materna_id:'' }
}

function savePerson(){
  if(editIndex.value!==null) people.value[editIndex.value]={...form.value}
  else people.value.push({...form.value})
  closeForm()
}

function editPersonByRow(row){
  editIndex.value=people.value.indexOf(row)
  form.value={...row}
  showForm.value=true
}

function deletePersonByRow(row){
  const idx=people.value.indexOf(row)
  if(idx!==-1 && confirm('¿Seguro que deseas eliminar este registro?')) people.value.splice(idx,1)
}

// Composición familiar
const familyTree = ref([{ name:'Juan Pérez', relation:'Padre' },{ name:'Ana Gómez', relation:'Madre' },{ name:'Pedro Pérez', relation:'Hijo' }])
</script>

<style scoped>
.modal-backdrop {
  position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.5); display:flex; justify-content:center; align-items:center; z-index:1050;
}
.modal-card { background:white; padding:20px; border-radius:10px; width:100%; max-width:500px; }
</style>
