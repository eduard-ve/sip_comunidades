<template>
  <BaseModule title="Gestión Poblacional" icon="bi bi-people">
    
    <!-- KPIs -->
    <template #kpis>
      <KpiCard title="Población Total" value="12,450" change="2.5" icon="bi bi-people-fill" />
      <KpiCard title="Nacimientos" value="340" change="1.2" icon="bi bi-person-plus-fill" />
      <KpiCard title="Defunciones" value="120" change="-0.5" icon="bi bi-person-dash-fill" />
      <KpiCard title="Crecimiento" value="2.1%" change="0.3" icon="bi bi-graph-up" />
    </template>

    <!-- Estadísticas -->
    <template #charts>
      <div class="row g-3">
        <div class="col-md-6">
          <ChartPanel chart-id="populationTrend" type="line" :data="populationTrendData">
            <template #title>📈 Tendencia de Población</template>
          </ChartPanel>
        </div>
        <div class="col-md-6">
          <PopulationPyramid />
        </div>
      </div>
    </template>

    <!-- Lista de personas -->
    <template #table>
      <div class="card shadow-sm border-0 p-3">
        <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
          <h6 class="fw-bold">📋 Lista de Personas / Familias</h6>
          <div>
            <button class="btn btn-success btn-sm me-2" @click="exportExcel">
              <i class="bi bi-file-earmark-excel"></i> Excel
            </button>
            <button class="btn btn-danger btn-sm me-2" @click="exportPDF">
              <i class="bi bi-file-earmark-pdf"></i> PDF
            </button>
            <button class="btn btn-primary btn-sm" @click="showForm = true">
              <i class="bi bi-plus-lg"></i> Nuevo Registro
            </button>
          </div>
        </div>

        <DataTable :headers="tableHeaders" :items="people" />
      </div>
    </template>

    <!-- Mapa y Composición familiar -->
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
      <h5 class="mb-3">Nuevo Registro</h5>
      <form @submit.prevent="addPerson">
        <input v-model="form.name" class="form-control mb-2" placeholder="Nombre completo" required />
        <input v-model.number="form.age" type="number" class="form-control mb-2" placeholder="Edad" required />
        <input v-model="form.community" class="form-control mb-3" placeholder="Comunidad" required />
        <div class="text-end">
          <button type="button" class="btn btn-secondary btn-sm me-2" @click="showForm = false">Cancelar</button>
          <button type="submit" class="btn btn-primary btn-sm">Guardar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue' // ✅ NECESARIO
import BaseModule from '../components/BaseModule.vue'
import KpiCard from '../components/KpiCard.vue'
import ChartPanel from '../components/ChartPanel.vue'
import PopulationPyramid from '../components/PopulationPyramid.vue'
import ServicesMap from '../components/ServicesMap.vue'
import DataTable from '../components/DataTable.vue'

// 📋 Cabeceras de la tabla
const tableHeaders = ['Nombre', 'Edad', 'Comunidad']

// 📌 Datos iniciales
const people = ref([
  { Nombre: 'Juan Pérez', Edad: 35, Comunidad: 'Comunidad A' },
  { Nombre: 'Ana Gómez', Edad: 28, Comunidad: 'Comunidad B' }
])

// 🌳 Composición familiar
const familyTree = ref([
  { name: 'Juan Pérez', relation: 'Padre' },
  { name: 'Ana Gómez', relation: 'Madre' },
  { name: 'Pedro Pérez', relation: 'Hijo' }
])

// 📈 Datos de tendencia de población
const populationTrendData = {
  labels: ['2019', '2020', '2021', '2022', '2023'],
  datasets: [
    {
      label: 'Población',
      data: [11000, 11250, 11500, 12000, 12450],
      borderColor: '#0d6efd',
      backgroundColor: 'rgba(13, 110, 253, 0.3)',
      tension: 0.3,
      fill: true
    }
  ]
}

// 📑 Formulario y modal
const showForm = ref(false)
const form = ref({ name: '', age: '', community: '' })

function addPerson() {
  if (form.value.name && form.value.age && form.value.community) {
    people.value.push({
      Nombre: form.value.name,
      Edad: form.value.age,
      Comunidad: form.value.community
    })
    form.value = { name: '', age: '', community: '' }
    showForm.value = false
  }
}

function exportExcel() {
  console.log('Exportar Excel')
}

function exportPDF() {
  console.log('Exportar PDF')
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}
.modal-card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
}
</style>
