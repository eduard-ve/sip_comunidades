<template>
  <BaseModule
    title="Gestión Social"
    :kpis="kpis"
    :charts="charts"
    :table="{ columns: tableColumns, rows: programas }"
    search-placeholder="Buscar programas o beneficiarios…"
    :show-create="true"
    @create="showForm = true"
    @export="onExport"
    @rowClick="onRowClick"
  >
    <!-- Personalización de celdas de la tabla -->
    <template #table-cell="{ column, row }">
      <!-- Si es columna acciones -->
      <div v-if="column.key === 'acciones'" class="d-flex gap-2 justify-content-center">
        <button class="btn btn-sm btn-outline-primary" @click="editPrograma(row)">
          <i class="bi bi-pencil"></i>
        </button>
        <button class="btn btn-sm btn-outline-danger" @click="deletePrograma(row)">
          <i class="bi bi-trash"></i>
        </button>
      </div>
      <!-- Para el resto de columnas -->
      <span v-else>{{ row[column.key] }}</span>
    </template>

    <!-- Extra contenido encima de charts -->
    <template #extra>
      <div class="mb-3">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5>Autoridades Comunitarias Activas</h5>
          <button
            class="btn btn-sm nueva-autoridad-btn"
            @click="showAutoridadForm = true"
          >
            <i class="bi bi-plus-circle me-1"></i>
            Nueva Autoridad
          </button>
        </div>
        <div class="row">
          <div v-for="autoridad in autoridadesActivas" :key="autoridad.id" class="col-lg-4 col-md-6 mb-3">
            <div class="card border-primary shadow-sm h-100">
              <div class="card-header bg-primary text-white d-flex align-items-center">
                <i class="bi bi-person-badge-fill me-2"></i>
                <span class="fw-bold">{{ autoridad.rol.nombre }}</span>
              </div>
              <div class="card-body">
                <h6 class="card-title text-primary mb-2">
                  <i class="bi bi-person-circle me-1"></i>
                  {{ autoridad.persona.nombre_completo }}
                </h6>
                <div class="row g-2">
                  <div class="col-12">
                    <span class="badge bg-info mb-2">
                      <i class="bi bi-tag-fill me-1"></i>
                      {{ autoridad.tipo_autoridad.nombre }}
                    </span>
                  </div>
                  <div class="col-12">
                    <small class="text-muted d-block">
                      <i class="bi bi-calendar-event me-1"></i>
                      Desde: {{ new Date(autoridad.fecha_inicio_mandato).toLocaleDateString() }}
                    </small>
                  </div>
                  <div class="col-12">
                    <small class="text-muted d-block">
                      <i class="bi bi-telephone me-1"></i>
                      {{ autoridad.telefono_contacto || 'Sin teléfono' }}
                    </small>
                  </div>
                  <div class="col-12">
                    <small class="text-muted d-block">
                      <i class="bi bi-envelope me-1"></i>
                      {{ autoridad.email_contacto || 'Sin email' }}
                    </small>
                  </div>
                </div>
              </div>
              <div class="card-footer bg-light">
                <div class="d-flex gap-1 justify-content-end">
                  <button class="btn btn-outline-primary btn-sm" @click="editAutoridad(autoridad)" title="Editar">
                    <i class="bi bi-pencil-square"></i>
                  </button>
                  <button class="btn btn-outline-danger btn-sm" @click="deleteAutoridad(autoridad)" title="Eliminar">
                    <i class="bi bi-trash3"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="mb-3">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5>Actividades Comunitarias</h5>
          <button
            class="btn btn-sm nueva-actividad-btn"
            @click="showActividadForm = true"
          >
            <i class="bi bi-plus-circle me-1"></i>
            Nueva Actividad
          </button>
        </div>
        <div class="row">
          <div v-for="actividad in actividadesComunitarias" :key="actividad.id" class="col-lg-4 col-md-6 mb-3">
            <div class="card border-success shadow-sm h-100">
              <div class="card-header bg-success text-white d-flex align-items-center">
                <i class="bi bi-calendar-event-fill me-2"></i>
                <span class="fw-bold">{{ actividad.tipo_actividad.nombre }}</span>
                <span class="badge bg-light text-success ms-auto">{{ actividad.estado.nombre }}</span>
              </div>
              <div class="card-body">
                <h6 class="card-title text-success mb-2">
                  <i class="bi bi-flag-fill me-1"></i>
                  {{ actividad.titulo }}
                </h6>
                <div class="row g-2">
                  <div class="col-12">
                    <small class="text-muted d-block">
                      <i class="bi bi-calendar-date me-1"></i>
                      {{ new Date(actividad.fecha_inicio).toLocaleDateString() }}
                      <span v-if="actividad.fecha_fin" class="ms-2">
                        - {{ new Date(actividad.fecha_fin).toLocaleDateString() }}
                      </span>
                    </small>
                  </div>
                  <div class="col-12">
                    <small class="text-muted d-block">
                      <i class="bi bi-geo-alt me-1"></i>
                      {{ actividad.ubicacion || 'Ubicación no especificada' }}
                    </small>
                  </div>
                  <div class="col-6">
                    <div class="text-center p-2 bg-light rounded">
                      <div class="fw-bold text-success">{{ actividad.asistentes_confirmados }}</div>
                      <small class="text-muted">Confirmados</small>
                    </div>
                  </div>
                  <div class="col-6">
                    <div class="text-center p-2 bg-light rounded">
                      <div class="fw-bold text-info">{{ actividad.capacidad_maxima || '∞' }}</div>
                      <small class="text-muted">Capacidad</small>
                    </div>
                  </div>
                  <div class="col-12">
                    <small class="text-muted d-block">
                      <i class="bi bi-person me-1"></i>
                      <strong>Organizador:</strong> {{ actividad.organizador || 'No especificado' }}
                    </small>
                  </div>
                </div>
              </div>
              <div class="card-footer bg-light">
                <div class="d-flex gap-1 justify-content-end">
                  <button class="btn btn-outline-success btn-sm" @click="editActividad(actividad)" title="Editar">
                    <i class="bi bi-pencil-square"></i>
                  </button>
                  <button class="btn btn-outline-danger btn-sm" @click="deleteActividad(actividad)" title="Eliminar">
                    <i class="bi bi-trash3"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Gráfico de distribución por tipo de actividad -->
    <template #left>
      <ChartPanel
        chart-id="actividadesTipoChart"
        type="doughnut"
        :data="actividadesTipoData"
        :options="{
          responsive: true,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                padding: 20,
                usePointStyle: true
              }
            }
          }
        }"
      >
        <template #title>Distribución por Tipo de Actividad</template>
      </ChartPanel>
    </template>

    <!-- ChartPanel de estadísticas de impacto social -->
    <template #right>
      <ChartPanel
        chart-id="impactoSocialChart"
        type="bar"
        :data="impactoData"
        :options="{
          responsive: true,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              backgroundColor: 'rgba(0,0,0,0.8)',
              titleColor: '#fff',
              bodyColor: '#fff',
              callbacks: {
                label: function(context) {
                  return context.parsed.y + ' beneficiarios'
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0,0,0,0.1)'
              },
              ticks: {
                color: '#666'
              }
            },
            x: {
              grid: {
                display: false
              },
              ticks: {
                color: '#666',
                maxRotation: 45,
                minRotation: 45
              }
            }
          },
          elements: {
            bar: {
              borderRadius: 4,
              borderSkipped: false
            }
          }
        }"
      >
        <template #title>Estadísticas de impacto social</template>
      </ChartPanel>
    </template>
  </BaseModule>

  <!-- Modal para crear/editar programa -->
  <div v-if="showForm" class="modal-backdrop">
    <div class="modal-card" style="max-width: 600px;">
      <h5 class="mb-3">{{ editIndex !== null ? 'Editar Programa' : 'Nuevo Programa' }}</h5>
      <form @submit.prevent="savePrograma">
        <div class="mb-2">
          <label for="nombre_programa" class="form-label small fw-semibold">Nombre</label>
          <input
            id="nombre_programa"
            v-model="form.nombre"
            class="form-control form-control-sm"
            placeholder="Nombre del programa..."
            required
          />
        </div>

        <div class="mb-2">
          <label for="descripcion_programa" class="form-label small fw-semibold">Descripción</label>
          <textarea
            id="descripcion_programa"
            v-model="form.descripcion"
            class="form-control form-control-sm"
            placeholder="Descripción del programa..."
            rows="2"
          ></textarea>
        </div>

        <div class="mb-2">
          <label for="estado_programa" class="form-label small fw-semibold">Estado</label>
          <select id="estado_programa" v-model="form.estado_id" class="form-control form-control-sm" required>
            <option disabled value="">Seleccione estado</option>
            <option v-for="estado in estados" :key="estado.id" :value="estado.id">
              {{ estado.nombre }}
            </option>
          </select>
        </div>

        <div class="row mb-2">
          <div class="col-6">
            <label for="fecha_inicio_programa" class="form-label small fw-semibold">Fecha Inicio</label>
            <input
              id="fecha_inicio_programa"
              v-model="form.fecha_inicio"
              type="date"
              class="form-control form-control-sm"
            />
          </div>
          <div class="col-6">
            <label for="fecha_fin_programa" class="form-label small fw-semibold">Fecha Fin</label>
            <input
              id="fecha_fin_programa"
              v-model="form.fecha_fin"
              type="date"
              class="form-control form-control-sm"
            />
          </div>
        </div>

        <div class="mb-2">
          <label for="beneficiarios_count" class="form-label small fw-semibold">Beneficiarios</label>
          <input
            id="beneficiarios_count"
            v-model.number="form.beneficiarios_count"
            type="number"
            class="form-control form-control-sm"
            placeholder="0"
            min="0"
            required
            style="max-width: 120px;"
          />
        </div>

        <div class="d-flex justify-content-end gap-2 pt-2 border-top mt-3">
          <button type="button" class="btn btn-outline-secondary btn-sm px-3" @click="closeForm">
            Cancelar
          </button>
          <button type="submit" class="btn btn-primary btn-sm px-3">
            Guardar
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- Modal para crear/editar autoridad -->
  <div v-if="showAutoridadForm" class="modal-backdrop">
    <div class="modal-card" style="max-width: 600px;">
      <h5 class="mb-3">{{ editAutoridadIndex !== null ? 'Editar Autoridad' : 'Nueva Autoridad' }}</h5>
      <form @submit.prevent="saveAutoridad">
        <!-- Búsqueda por cédula -->
        <div class="row mb-2">
          <div class="col-8">
            <label for="numero_identificacion" class="form-label small fw-semibold">Buscar por ID</label>
            <input
              id="numero_identificacion"
              v-model="autoridadForm.numero_identificacion"
              type="text"
              class="form-control form-control-sm"
              placeholder="Número de cédula..."
              :disabled="buscandoPersona"
            />
          </div>
          <div class="col-4 d-flex align-items-end">
            <button
              type="button"
              class="btn btn-outline-primary btn-sm w-100"
              @click="buscarPersonaPorCedula"
              :disabled="!autoridadForm.numero_identificacion.trim() || buscandoPersona"
            >
              <span v-if="buscandoPersona" class="spinner-border spinner-border-sm me-1"></span>
              Buscar
            </button>
          </div>
        </div>

        <!-- Información de la persona encontrada -->
        <div v-if="personaSeleccionada" class="alert alert-success mb-2 py-2">
          <div class="row">
            <div class="col-8">
              <small class="fw-semibold">{{ personaSeleccionada.nombre_completo }}</small>
            </div>
            <div class="col-4 text-end">
              <small>ID: {{ personaSeleccionada.numero_identificacion }}</small>
            </div>
          </div>
        </div>

        <!-- Tipo y Rol en fila -->
        <div class="row mb-2">
          <div class="col-6">
            <label for="tipo_autoridad_id" class="form-label small fw-semibold">Tipo</label>
            <select id="tipo_autoridad_id" v-model="autoridadForm.tipo_autoridad_id" class="form-control form-control-sm" required>
              <option disabled value="">Tipo</option>
              <option v-for="tipo in tiposAutoridad" :key="tipo.id" :value="tipo.id">
                {{ tipo.nombre }}
              </option>
            </select>
          </div>
          <div class="col-6">
            <label for="rol_id" class="form-label small fw-semibold">Rol</label>
            <select id="rol_id" v-model="autoridadForm.rol_id" class="form-control form-control-sm" required>
              <option disabled value="">Rol</option>
              <option v-for="rol in rolesAutoridad" :key="rol.id" :value="rol.id">
                {{ rol.nombre }}
              </option>
            </select>
          </div>
        </div>
        <!-- Fechas en fila -->
        <div class="row mb-2">
          <div class="col-6">
            <label for="fecha_inicio_mandato" class="form-label small fw-semibold">Fecha Inicio</label>
            <input
              id="fecha_inicio_mandato"
              v-model="autoridadForm.fecha_inicio_mandato"
              type="date"
              class="form-control form-control-sm"
              required
            />
          </div>
          <div class="col-6">
            <label for="fecha_fin_mandato" class="form-label small fw-semibold">Fecha Fin</label>
            <input
              id="fecha_fin_mandato"
              v-model="autoridadForm.fecha_fin_mandato"
              type="date"
              class="form-control form-control-sm"
            />
          </div>
        </div>
        <!-- Contacto en fila -->
        <div class="row mb-2">
          <div class="col-6">
            <label for="telefono_contacto" class="form-label small fw-semibold">Teléfono</label>
            <input
              id="telefono_contacto"
              v-model="autoridadForm.telefono_contacto"
              type="tel"
              class="form-control form-control-sm"
              placeholder="3001234567"
            />
          </div>
          <div class="col-6">
            <label for="email_contacto" class="form-label small fw-semibold">Email</label>
            <input
              id="email_contacto"
              v-model="autoridadForm.email_contacto"
              type="email"
              class="form-control form-control-sm"
              placeholder="autoridad@example.com"
            />
          </div>
        </div>
        <!-- Observaciones -->
        <div class="mb-2">
          <label for="observaciones_autoridad" class="form-label small fw-semibold">Observaciones</label>
          <textarea
            id="observaciones_autoridad"
            v-model="autoridadForm.observaciones"
            class="form-control form-control-sm"
            rows="2"
            placeholder="Observaciones..."
          ></textarea>
        </div>
        <!-- Checkbox activo -->
        <div class="mb-2 form-check">
          <input
            v-model="autoridadForm.activo"
            class="form-check-input"
            type="checkbox"
            id="activoCheck"
          />
          <label class="form-check-label small fw-semibold" for="activoCheck">
            Autoridad Activa
          </label>
        </div>
        <!-- Botones -->
        <div class="d-flex justify-content-end gap-2 pt-2 border-top mt-3">
          <button type="button" class="btn btn-outline-secondary btn-sm px-3" @click="closeAutoridadForm">
            Cancelar
          </button>
          <button type="submit" class="btn btn-primary btn-sm px-3">
            Guardar
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- Modal para crear/editar actividad -->
  <div v-if="showActividadForm" class="modal-backdrop">
    <div class="modal-card" style="max-width: 600px;">
      <h5 class="mb-3">{{ editActividadIndex !== null ? 'Editar Actividad' : 'Nueva Actividad' }}</h5>
      <form @submit.prevent="saveActividad">
        <div class="row mb-2">
          <div class="col-8">
            <label for="titulo_actividad" class="form-label small fw-semibold">Título</label>
            <input
              id="titulo_actividad"
              v-model="actividadForm.titulo"
              type="text"
              class="form-control form-control-sm"
              placeholder="Título de la actividad..."
              required
            />
          </div>
          <div class="col-4">
            <label for="tipo_actividad_id" class="form-label small fw-semibold">Tipo</label>
            <select id="tipo_actividad_id" v-model="actividadForm.tipo_actividad_id" class="form-control form-control-sm" required>
              <option disabled value="">Tipo</option>
              <option v-for="tipo in tiposActividad" :key="tipo.id" :value="tipo.id">
                {{ tipo.nombre }}
              </option>
            </select>
          </div>
        </div>

        <div class="mb-2">
          <label for="descripcion_actividad" class="form-label small fw-semibold">Descripción</label>
          <textarea
            id="descripcion_actividad"
            v-model="actividadForm.descripcion"
            class="form-control form-control-sm"
            rows="2"
            placeholder="Descripción..."
          ></textarea>
        </div>

        <div class="row mb-2">
          <div class="col-6">
            <label for="estado_actividad_id" class="form-label small fw-semibold">Estado</label>
            <select id="estado_actividad_id" v-model="actividadForm.estado_id" class="form-control form-control-sm" required>
              <option disabled value="">Estado</option>
              <option v-for="estado in estadosActividad" :key="estado.id" :value="estado.id">
                {{ estado.nombre }}
              </option>
            </select>
          </div>
          <div class="col-6">
            <label for="ubicacion_actividad" class="form-label small fw-semibold">Ubicación</label>
            <input
              id="ubicacion_actividad"
              v-model="actividadForm.ubicacion"
              type="text"
              class="form-control form-control-sm"
              placeholder="Lugar..."
            />
          </div>
        </div>

        <div class="row mb-2">
          <div class="col-6">
            <label for="fecha_inicio_actividad" class="form-label small fw-semibold">Fecha Inicio</label>
            <input
              id="fecha_inicio_actividad"
              v-model="actividadForm.fecha_inicio"
              type="datetime-local"
              class="form-control form-control-sm"
              required
            />
          </div>
          <div class="col-6">
            <label for="fecha_fin_actividad" class="form-label small fw-semibold">Fecha Fin</label>
            <input
              id="fecha_fin_actividad"
              v-model="actividadForm.fecha_fin"
              type="datetime-local"
              class="form-control form-control-sm"
            />
          </div>
        </div>

        <div class="row mb-2">
          <div class="col-6">
            <label for="capacidad_maxima" class="form-label small fw-semibold">Capacidad</label>
            <input
              id="capacidad_maxima"
              v-model.number="actividadForm.capacidad_maxima"
              type="number"
              class="form-control form-control-sm"
              placeholder="0"
              min="0"
              style="max-width: 100px;"
            />
          </div>
          <div class="col-6">
            <label for="organizador_actividad" class="form-label small fw-semibold">Organizador</label>
            <input
              id="organizador_actividad"
              v-model="actividadForm.organizador"
              type="text"
              class="form-control form-control-sm"
              placeholder="Nombre..."
            />
          </div>
        </div>

        <div class="mb-2">
          <label for="observaciones_actividad" class="form-label small fw-semibold">Observaciones</label>
          <textarea
            id="observaciones_actividad"
            v-model="actividadForm.observaciones"
            class="form-control form-control-sm"
            rows="2"
            placeholder="Observaciones..."
          ></textarea>
        </div>

        <div class="d-flex justify-content-end gap-2 pt-2 border-top mt-3">
          <button type="button" class="btn btn-outline-secondary btn-sm px-3" @click="closeActividadForm">
            Cancelar
          </button>
          <button type="submit" class="btn btn-primary btn-sm px-3">
            Guardar
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BaseModule from '../../components/comun/BaseModule.vue'
import ChartPanel from '../../components/graficas/ChartPanel.vue'
import { socialService } from '../../services/api.js'
import '../../assets/css/GestionSocial.css'

// Reactive data
const kpis = ref([
  { title: 'Programas activos', value: 0, change: '+0', icon: 'bi-people' },
  { title: 'Beneficiarios totales', value: 0, change: '+0', icon: 'bi-person-check' },
  { title: 'Actividades culturales', value: 0, change: '+0', icon: 'bi-music-note-beamed' },
  { title: 'Autoridades activas', value: 0, change: '+0', icon: 'bi-person-badge' }
])

const actividades = ref([])
const impactoData = ref({
  labels: [],
  datasets: [{
    label: 'Beneficiarios',
    data: [],
    backgroundColor: [
      '#007bff', // Azul
      '#28a745', // Verde
      '#ffc107', // Amarillo
      '#dc3545', // Rojo
      '#6f42c1', // Morado
      '#fd7e14', // Naranja
      '#20c997', // Verde agua
      '#e83e8c', // Rosa
      '#17a2b8', // Cyan
      '#6c757d'  // Gris
    ],
    borderColor: [
      '#0056b3', // Azul oscuro
      '#1e7e34', // Verde oscuro
      '#d39e00', // Amarillo oscuro
      '#bd2130', // Rojo oscuro
      '#5a2d82', // Morado oscuro
      '#e8680f', // Naranja oscuro
      '#17a2b8', // Verde agua oscuro
      '#c2185b', // Rosa oscuro
      '#117a8b', // Cyan oscuro
      '#545b62'  // Gris oscuro
    ],
    borderWidth: 2,
    hoverBackgroundColor: [
      '#3395ff', // Azul claro
      '#5cb85c', // Verde claro
      '#ffdb4d', // Amarillo claro
      '#ff6b75', // Rojo claro
      '#9c6ade', // Morado claro
      '#ff8c42', // Naranja claro
      '#6dd5c3', // Verde agua claro
      '#ff6b9d', // Rosa claro
      '#5bc0de', // Cyan claro
      '#9ca3a7'  // Gris claro
    ]
  }]
})
const actividadesTipoData = ref({
  labels: [],
  datasets: [{
    label: 'Actividades',
    data: [],
    backgroundColor: [
      '#28a745', // Verde para Cultural
      '#007bff', // Azul para Deportiva
      '#ffc107', // Amarillo para Educativa
      '#dc3545', // Rojo para Comunitaria
      '#6f42c1', // Morado para otros tipos
      '#fd7e14', // Naranja para otros tipos
      '#20c997', // Verde agua para otros tipos
      '#e83e8c'  // Rosa para otros tipos
    ],
    borderWidth: 2
  }]
})

const tableColumns = [
  { key: 'nombre', label: 'Programa' },
  { key: 'beneficiarios_count', label: 'Beneficiarios' },
  { key: 'estado', label: 'Estado' },
  { key: 'acciones', label: 'Acciones', class: 'text-center'}
]

const programas = ref([])
const mapProgramas = ref([])
const estados = ref([])
const autoridadesActivas = ref([])
const actividadesComunitarias = ref([])

// Estados de carga
const loading = ref(false)
const error = ref(null)

// Modal formulario programas
const showForm = ref(false)
const form = ref({ nombre: '', descripcion: '', estado_id: '', fecha_inicio: '', fecha_fin: '', beneficiarios_count: 0 })
const editIndex = ref(null)

// Modal formulario autoridades
const showAutoridadForm = ref(false)
const autoridadForm = ref({
  persona_id: '',
  numero_identificacion: '',
  tipo_autoridad_id: '',
  rol_id: '',
  fecha_inicio_mandato: '',
  fecha_fin_mandato: '',
  telefono_contacto: '',
  email_contacto: '',
  observaciones: '',
  activo: true
})
const editAutoridadIndex = ref(null)

// Modal formulario actividades
const showActividadForm = ref(false)
const actividadForm = ref({
  titulo: '',
  descripcion: '',
  tipo_actividad_id: '',
  estado_id: '',
  fecha_inicio: '',
  fecha_fin: '',
  ubicacion: '',
  capacidad_maxima: '',
  organizador: '',
  observaciones: ''
})
const editActividadIndex = ref(null)

// Datos para autoridades
const tiposAutoridad = ref([])
const rolesAutoridad = ref([])
const personaSeleccionada = ref(null)
const buscandoPersona = ref(false)

// Datos para actividades comunitarias
const tiposActividad = ref([])
const estadosActividad = ref([])

// Agregar console.log para debugging
console.log('Componente GestionSocial montado')
console.log('tiposActividad inicial:', tiposActividad.value)
console.log('estadosActividad inicial:', estadosActividad.value)

// Funciones para cargar datos del backend
async function loadProgramasSociales() {
  try {
    loading.value = true
    const response = await socialService.getProgramasSociales()
    programas.value = response.data.map(programa => ({
      ...programa,
      estado: programa.estado ? programa.estado.nombre : 'Sin estado'
    }))

    // Actualizar KPIs
    const programasActivos = programas.value.filter(p => p.estado === 'Activo').length
    const totalBeneficiarios = programas.value.reduce((sum, p) => sum + p.beneficiarios_count, 0)
    kpis.value[0].value = programasActivos
    kpis.value[1].value = totalBeneficiarios

    // Actualizar chart de impacto
    impactoData.value.labels = programas.value.map(p => p.nombre)
    impactoData.value.datasets[0].data = programas.value.map(p => p.beneficiarios_count)

    // Actualizar KPI de autoridades comunitarias
    await loadAutoridadesComunitarias()
  } catch (err) {
    error.value = 'Error al cargar programas sociales'
    console.error('Error loading programas:', err)
  } finally {
    loading.value = false
  }
}

async function loadActividadesSociales() {
  try {
    const response = await socialService.getActividadesSociales()
    actividades.value = response.data.map(act => act.titulo)
    kpis.value[2].value = actividades.value.length
  } catch (err) {
    console.error('Error loading actividades sociales:', err)
    actividades.value = []
    kpis.value[2].value = 0
  }

  // Siempre mostrar actividades comunitarias como respaldo principal
  if (actividadesComunitarias.value.length > 0) {
    actividades.value = actividadesComunitarias.value.map(act => act.titulo)
    kpis.value[2].value = actividades.value.length
  } else {
    // Si no hay actividades comunitarias, intentar usar las sociales
    actividades.value = actividades.value || []
    kpis.value[2].value = actividades.value.length
  }
}

async function loadCoberturasProgramas() {
  try {
    const response = await socialService.getCoberturasProgramas()
    mapProgramas.value = response.data.map(cobertura => ({
      nombre: cobertura.programa.nombre,
      coordenadas: [Number.parseFloat(cobertura.latitud), Number.parseFloat(cobertura.longitud)]
    }))
    // Cambiar KPI de cobertura territorial por autoridades comunitarias
    // kpis.value[3].value = `${response.data.length} regiones`
  } catch (err) {
    console.error('Error loading coberturas:', err)
  }
}

async function loadAutoridadesComunitarias() {
  try {
    const response = await socialService.getAutoridadesComunitarias()
    autoridadesActivas.value = response.data.filter(aut => aut.activo)
    kpis.value[3].value = autoridadesActivas.value.length
  } catch (err) {
    console.error('Error loading autoridades:', err)
  }
}

async function loadEstadosProgramas() {
  try {
    const response = await socialService.getEstadosProgramas()
    estados.value = response.data
  } catch (err) {
    console.error('Error loading estados:', err)
  }
}

// Funciones para cargar datos de autoridades
async function loadTiposAutoridad() {
  try {
    const response = await socialService.getTiposAutoridad()
    tiposAutoridad.value = response.data
  } catch (err) {
    console.error('Error loading tipos autoridad:', err)
  }
}

async function loadRolesAutoridad() {
  try {
    const response = await socialService.getRolesAutoridad()
    rolesAutoridad.value = response.data
  } catch (err) {
    console.error('Error loading roles autoridad:', err)
  }
}

// Funciones para cargar datos de actividades comunitarias
async function loadTiposActividad() {
  try {
    console.log('Cargando tipos de actividad...')
    const response = await socialService.getTiposActividad()
    tiposActividad.value = response.data
    console.log('Tipos de actividad cargados:', tiposActividad.value.length, 'elementos')
    console.log('Primeros tipos:', tiposActividad.value.slice(0, 3))
  } catch (err) {
    console.error('Error loading tipos actividad:', err)
    tiposActividad.value = []
  }
}

async function loadEstadosActividad() {
  try {
    console.log('Cargando estados de actividad...')
    const response = await socialService.getEstadosActividad()
    estadosActividad.value = response.data
    console.log('Estados de actividad cargados:', estadosActividad.value.length, 'elementos')
    console.log('Primeros estados:', estadosActividad.value.slice(0, 3))
  } catch (err) {
    console.error('Error loading estados actividad:', err)
    estadosActividad.value = []
  }
}

async function loadActividadesComunitarias() {
  try {
    console.log('Cargando actividades comunitarias...')
    const response = await socialService.getActividadesComunitarias()
    actividadesComunitarias.value = response.data
    console.log('Actividades comunitarias cargadas:', actividadesComunitarias.value.length, 'elementos')
    console.log('Primeras actividades:', actividadesComunitarias.value.slice(0, 2))

    // Actualizar gráfico de distribución por tipo
    updateActividadesTipoChart()
  } catch (err) {
    console.error('Error loading actividades comunitarias:', err)
    actividadesComunitarias.value = []
  }
}

function updateActividadesTipoChart() {
  // Contar actividades por tipo
  const tipoCount = {}
  const lista = actividadesComunitarias.value || []
  for ( const actividad of lista ) {
    const tipoNombre = actividad.tipo_actividad?.nombre || 'Sin tipo'
    tipoCount[tipoNombre] = (tipoCount[tipoNombre] || 0) + 1
  }

  // Actualizar datos del gráfico
  actividadesTipoData.value.labels = Object.keys(tipoCount)
  actividadesTipoData.value.datasets[0].data = Object.values(tipoCount)
}

async function buscarPersonaPorCedula() {
  if (!autoridadForm.value.numero_identificacion.trim()) {
    alert('Por favor ingrese un número de identificación')
    return
  }

  buscandoPersona.value = true
  try {
    const response = await socialService.buscarPersonaPorCedula(autoridadForm.value.numero_identificacion)
    personaSeleccionada.value = response.data.persona

    if (response.data.es_autoridad_activa) {
      alert('Esta persona ya es una autoridad activa')
      return
    }

    // Auto-llenar campos
    autoridadForm.value.persona_id = response.data.persona.id
    autoridadForm.value.telefono_contacto = response.data.persona.direccion || ''
    autoridadForm.value.email_contacto = ''

  } catch (err) {
    console.error('Error buscando persona:', err)
    alert('Persona no encontrada o error en la búsqueda')
    personaSeleccionada.value = null
  } finally {
    buscandoPersona.value = false
  }
}

// Cargar todos los datos al montar el componente
onMounted(async () => {
  console.log('Iniciando carga de datos...')
  try {
    // Cargar primero los tipos y estados que necesita el formulario
    await Promise.all([
      loadTiposActividad(),
      loadEstadosActividad()
    ])
    console.log('Tipos y estados cargados:', tiposActividad.value.length, estadosActividad.value.length)

    // Cargar actividades comunitarias primero para asegurar que estén disponibles
    await loadActividadesComunitarias()
    updateActividadesTipoChart()

    // Luego cargar el resto de datos
    await Promise.all([
      loadProgramasSociales(),
      loadActividadesSociales(),
      loadCoberturasProgramas(),
      loadEstadosProgramas(),
      loadAutoridadesComunitarias(),
      loadTiposAutoridad(),
      loadRolesAutoridad(),
      loadPersonasDisponibles()
    ])
  } catch (error) {
    console.error('Error en carga inicial:', error)
  }
  console.log('Carga de datos completada')
  console.log('Estado final - tiposActividad:', tiposActividad.value)
  console.log('Estado final - estadosActividad:', estadosActividad.value)
  console.log('Actividades comunitarias cargadas:', actividadesComunitarias.value.length)
})

// Funciones del modal
function closeForm() {
  showForm.value = false
  form.value = { nombre: '', descripcion: '', estado_id: '', fecha_inicio: '', fecha_fin: '', beneficiarios_count: 0 }
  editIndex.value = null
}

async function savePrograma() {
  try {
    const isEditing = editIndex.value !== null
    if (isEditing) {
      // Actualizar programa existente
      const programa = programas.value[editIndex.value]
      await socialService.updateProgramaSocial(programa.id, form.value)
    } else {
      // Crear nuevo programa
      await socialService.createProgramaSocial(form.value)
    }
    closeForm()
    await loadProgramasSociales() // Recargar datos
  } catch (err) {
    error.value = 'Error al guardar el programa'
    console.error('Error saving programa:', err)
  }
}

function editPrograma(row) {
  editIndex.value = programas.value.indexOf(row)
  form.value = {
    nombre: row.nombre,
    descripcion: row.descripcion || '',
    estado_id: row.estado_id || '',
    fecha_inicio: row.fecha_inicio || '',
    fecha_fin: row.fecha_fin || '',
    beneficiarios_count: row.beneficiarios_count || 0
  }
  showForm.value = true
}

async function deletePrograma(row) {
  if (globalThis.confirm('¿Seguro que deseas eliminar este programa?')) {
    try {
      await socialService.deleteProgramaSocial(row.id)
      await loadProgramasSociales() // Recargar datos
    } catch (err) {
      error.value = 'Error al eliminar el programa'
      console.error('Error deleting programa:', err)
    }
  }
}

// Funciones para autoridades
function closeAutoridadForm() {
  showAutoridadForm.value = false
  autoridadForm.value = {
    persona_id: '',
    numero_identificacion: '',
    tipo_autoridad_id: '',
    rol_id: '',
    fecha_inicio_mandato: '',
    fecha_fin_mandato: '',
    telefono_contacto: '',
    email_contacto: '',
    observaciones: '',
    activo: true
  }
  editAutoridadIndex.value = null
  personaSeleccionada.value = null
}

async function saveAutoridad() {
  try {
    // Preparar datos para enviar (excluir numero_identificacion que no va al backend)
    const dataToSend = { ...autoridadForm.value }
    delete dataToSend.numero_identificacion

    const isEditing = editAutoridadIndex.value !== null
    if (isEditing) {
      // Actualizar autoridad existente
      const autoridad = autoridadesActivas.value[editAutoridadIndex.value]
      await socialService.updateAutoridadComunitaria(autoridad.id, dataToSend)
    } else {
      // Crear nueva autoridad
      await socialService.createAutoridadComunitaria(dataToSend)
    }
    closeAutoridadForm()
    await loadAutoridadesComunitarias() // Recargar autoridades para actualizar la vista
    await loadPersonasDisponibles() // Recargar personas disponibles
    // Mostrar mensaje de éxito
    const mensaje = isEditing ? 'Autoridad actualizada exitosamente' : 'Autoridad creada exitosamente'
    alert(mensaje)
  } catch (err) {
    console.error('Error saving autoridad:', err)
    // Solo mostrar error si realmente hay un problema de validación o conexión
    // No mostrar error si la operación fue exitosa pero hay un problema menor
    if (err.response && err.response.status !== 201 && err.response.status !== 200) {
      alert('Error al guardar la autoridad. Verifica los datos e intenta nuevamente.')
    }
  }
}

function editAutoridad(autoridad) {
  editAutoridadIndex.value = autoridadesActivas.value.indexOf(autoridad)
  autoridadForm.value = {
    persona_id: autoridad.persona.id,
    numero_identificacion: autoridad.persona.numero_identificacion,
    tipo_autoridad_id: autoridad.tipo_autoridad.id,
    rol_id: autoridad.rol.id,
    fecha_inicio_mandato: autoridad.fecha_inicio_mandato,
    fecha_fin_mandato: autoridad.fecha_fin_mandato || '',
    telefono_contacto: autoridad.telefono_contacto || '',
    email_contacto: autoridad.email_contacto || '',
    observaciones: autoridad.observaciones || '',
    activo: autoridad.activo
  }
  // Mostrar la persona como seleccionada
  personaSeleccionada.value = autoridad.persona
  showAutoridadForm.value = true
}

async function deleteAutoridad(autoridad) {
  if (globalThis.confirm('¿Seguro que deseas eliminar esta autoridad?')) {
    try {
      await socialService.deleteAutoridadComunitaria(autoridad.id)
      await loadAutoridadesComunitarias() // Recargar autoridades para actualizar la vista
      await loadPersonasDisponibles() // Recargar personas disponibles
      alert('Autoridad eliminada exitosamente')
    } catch (err) {
      console.error('Error deleting autoridad:', err)
      // Solo mostrar error si realmente hay un problema (no si ya fue eliminada)
      if (err.response && err.response.status !== 204 && err.response.status !== 404) {
        alert('Error al eliminar la autoridad')
      }
    }
  }
}

// Funciones para actividades comunitarias
function closeActividadForm() {
  showActividadForm.value = false
  actividadForm.value = {
    titulo: '',
    descripcion: '',
    tipo_actividad_id: '',
    estado_id: '',
    fecha_inicio: '',
    fecha_fin: '',
    ubicacion: '',
    capacidad_maxima: '',
    organizador: '',
    observaciones: ''
  }
  editActividadIndex.value = null
}

async function saveActividad() {
  try {
    // Preparar datos para enviar
    const dataToSend = {
      titulo: actividadForm.value.titulo,
      descripcion: actividadForm.value.descripcion,
      tipo_actividad_id: actividadForm.value.tipo_actividad_id,
      estado_id: actividadForm.value.estado_id,
      fecha_inicio: actividadForm.value.fecha_inicio,
      fecha_fin: actividadForm.value.fecha_fin || null,
      ubicacion: actividadForm.value.ubicacion,
      capacidad_maxima: actividadForm.value.capacidad_maxima || null,
      organizador: actividadForm.value.organizador || null,
      observaciones: actividadForm.value.observaciones
    }

    console.log('Enviando datos de actividad:', dataToSend)

    const isEditing = editActividadIndex.value !== null
    if (isEditing) {
      // Actualizar actividad existente
      const actividad = actividadesComunitarias.value[editActividadIndex.value]
      await socialService.updateActividadComunitaria(actividad.id, dataToSend)
    } else {
      // Crear nueva actividad
      await socialService.createActividadComunitaria(dataToSend)
    }
    closeActividadForm()
    await loadActividadesComunitarias()
    // Mostrar mensaje de éxito
    const mensaje = isEditing ? 'Actividad actualizada exitosamente' : 'Actividad creada exitosamente'
    alert(mensaje)
  } catch (err) {
    console.error('Error saving actividad:', err)
    alert('Error al guardar la actividad. Verifica los datos e intenta nuevamente.')
  }
}

function editActividad(actividad) {
  editActividadIndex.value = actividadesComunitarias.value.indexOf(actividad)
  actividadForm.value = {
    titulo: actividad.titulo,
    descripcion: actividad.descripcion || '',
    tipo_actividad_id: actividad.tipo_actividad ? actividad.tipo_actividad.id : '',
    estado_id: actividad.estado ? actividad.estado.id : '',
    fecha_inicio: actividad.fecha_inicio,
    fecha_fin: actividad.fecha_fin || '',
    ubicacion: actividad.ubicacion || '',
    capacidad_maxima: actividad.capacidad_maxima || '',
    organizador: actividad.organizador || '',
    observaciones: actividad.observaciones || ''
  }
  showActividadForm.value = true
}

async function deleteActividad(actividad) {
  if (globalThis.confirm('¿Seguro que deseas eliminar esta actividad?')) {
    try {
      await socialService.deleteActividadComunitaria(actividad.id)
      await loadActividadesComunitarias()
    } catch (err) {
      console.error('Error deleting actividad:', err)
    }
  }
}

// Eventos
function onExport() { console.log('Exportar datos') }
function onRowClick(row) { console.log('Fila clickeada', row) }
</script>
