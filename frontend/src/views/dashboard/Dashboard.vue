<template>
  <div class="min-vh-100" style="background: linear-gradient(135deg, #f5f7fa 0%, #e8f0fe 100%);">

    <!-- HEADER -->
    <div class="position-sticky top-0 bg-white border-bottom shadow-sm" style="z-index: 1000;">
      <div class="container-fluid px-4 py-3" style="max-width: 1600px;">
        <div class="row align-items-center">
          <div class="col-12">
            <div class="d-flex align-items-center gap-3">
              <div
                class="rounded-3 d-flex align-items-center justify-center p-2"
                style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); box-shadow: 0 4px 10px rgba(102, 126, 234, 0.5);"
              >
                <i class="bi bi-bar-chart-line-fill text-white fs-4"></i>
              </div>

              <div>
                <h1 class="fs-3 fw-bolder text-dark mb-0">Dashboard Ejecutivo</h1>
                <p class="small text-muted mb-0 fw-medium text-uppercase">
                  {{ nombreComunidad }} • {{ currentYear }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- CONTENIDO -->
    <div class="container-fluid px-4 py-4" style="max-width: 1600px;">

      <!-- MÉTRICAS HERO -->
      <div class="row g-3 mb-4">
        <div
          v-for="metric in Object.values(heroMetrics)"
          :key="metric.label"
          class="col-6 col-md-3"
        >
          <div class="card border-0 shadow-sm h-100 hover-lift">
            <div class="card-body p-3">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <div class="flex-grow-1">
                  <p class="text-muted small mb-1 text-uppercase fw-semibold">{{ metric.label }}</p>
                  <h2 class="display-6 fw-bold mb-0" :style="{ color: metric.color }">
                    {{ metric.value }}
                  </h2>
                  <p class="text-muted small mb-0">{{ metric.sublabel }}</p>
                </div>
                <div class="text-end">
                  <span
                    class="badge rounded-pill"
                    :class="metric.trend >= 0 ? 'bg-success' : 'bg-danger'"
                  >
                    <i :class="metric.trend >= 0 ? 'bi bi-arrow-up' : 'bi bi-arrow-down'"></i>
                    {{ Math.abs(metric.trend) }}%
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- FILA PRINCIPAL -->
      <div class="row g-4 mb-3">

        <!-- COLUMNA IZQUIERDA -->
        <div class="col-lg-5">
          <div class="row g-4">

            <!-- EVOLUCIÓN REGISTROS -->
            <div class="col-12">
              <div class="card border-0 shadow-sm">
                <div class="card-header bg-white border-0 pt-3 pb-2">
                  <h5 class="fw-bold mb-0">
                    <span class="badge bg-primary me-2">📈</span>
                    Evolución de Registros (Tendencia)
                  </h5>
                </div>
                <div class="card-body p-0" style="height: 280px; overflow: hidden;">
                  <ChartPanel
                    noCard="true"
                    height="280px"
                    chart-id="areaChart"
                    type="line"
                    :data="evolucionData"
                    :options="{ maintainAspectRatio: false }"
                  />
                </div>
              </div>
            </div>

            <!-- OCUPACIÓN Y DESOCUPACIÓN -->
            <div class="col-12">
              <div class="card border-0 shadow-sm">
                <div class="card-header bg-white border-0 pt-3 pb-2">
                  <h5 class="fw-bold mb-0">
                    <span class="badge bg-success me-2">💼</span>
                    Indicadores de Empleo
                  </h5>
                </div>

                <div class="card-body p-3" style="overflow: hidden;">
                  <div class="row g-4">

                    <!-- OCUPACIÓN -->
                    <div class="col-6 text-center">
                      <h6 class="fw-bold small text-success mb-2">Tasa Ocupación (TO)</h6>
                      <div class="mb-2">
                        <div style="width: 100%; height: 60px; position: relative;">
                          <ChartPanel
                            height="60px"
                            chart-id="ocupacionDonut"
                            type="bar"
                            :data="ocupacionData"
                            :options="{
                              maintainAspectRatio: false,
                              indexAxis: 'y',
                              plugins: { legend: { display: false } }
                            }"
                          />
                        </div>
                      </div>

                      <div class="d-flex justify-content-center align-items-center gap-2">
                        <span
                          class="badge rounded-circle"
                          style="background-color: #3b82f6; width: 10px; height: 10px;"
                        ></span>
                        <span class="text-muted small">Hombres</span>

                        <span
                          class="badge rounded-circle"
                          style="background-color: #ec4899; width: 10px; height: 10px;"
                        ></span>
                        <span class="text-muted small">Mujeres</span>
                      </div>
                    </div>

                    <!-- DESOCUPACIÓN -->
                    <div class="col-6 text-center">
                      <h6 class="fw-bold small text-danger mb-2">Tasa Desocupación (TD)</h6>
                      <div class="mb-2">
                        <div style="width: 100%; height: 60px; position: relative;">
                          <ChartPanel
                            height="60px"
                            chart-id="desocupacionDonut"
                            type="bar"
                            :data="desocupacionData"
                            :options="{
                              maintainAspectRatio: false,
                              indexAxis: 'y',
                              plugins: { legend: { display: false } }
                            }"
                          />
                        </div>
                      </div>

                      <div class="d-flex justify-content-center align-items-center gap-2">
                        <span
                          class="badge rounded-circle"
                          style="background-color: #3b82f6; width: 10px; height: 10px;"
                        ></span>
                        <span class="text-muted small">Hombres</span>

                        <span
                          class="badge rounded-circle"
                          style="background-color: #ec4899; width: 10px; height: 10px;"
                        ></span>
                        <span class="text-muted small">Mujeres</span>
                      </div>
                    </div>
                  </div>
                </div>

              </div>
            </div>

          </div>
        </div>

        <!-- COLUMNA DERECHA -->
        <div class="col-lg-7">
          <div class="row g-2">

            <!-- PROGRAMAS Y BENEFICIARIOS -->
            <div class="col-lg-6">
              <div class="card border-0 shadow-sm h-100">
                <div class="card-header bg-white border-0 pt-3 pb-2">
                  <h5 class="fw-bold mb-0">
                    <span class="badge bg-info me-2">✅</span>
                    Programas y Beneficiarios
                  </h5>
                </div>

                <div class="card-body p-0 d-flex flex-column" style="overflow: hidden;">

                  <div class="row g-2 mb-3">
                    <div
                      v-for="prog in gestionSocial"
                      :key="prog.label"
                      class="col-6"
                    >
                      <div
                        class="p-2 rounded-3"
                        :style="{ borderLeft: `4px solid ${prog.color}`, backgroundColor: 'rgba(240,248,255,0.5)' }"
                      >
                        <p class="small text-muted mb-1 text-uppercase">{{ prog.label }}</p>
                        <h5 class="fw-bold" :style="{ color: prog.color }">{{ prog.value }}</h5>
                      </div>
                    </div>
                  </div>

                  <div style="flex-grow: 1; min-height: 220px;">
                    <h6 class="fw-bold small text-muted mb-2">Cobertura por Tipo</h6>
                    <div style="height: 280px; position: relative;">
                      <ChartPanel
                        noCard="true"
                        height="280px"
                        chart-id="programasTipoRadar"
                        type="radar"
                        :data="programasTipoRadarData"
                        :options="{
                          maintainAspectRatio: false,
                          scales: {
                            r: {
                              ticks: {
                                font: { size: 12 },
                                color: '#333'
                              },
                              pointLabels: {
                                font: { size: 14 },
                                color: '#333'
                              }
                            }
                          },
                          plugins: {
                            legend: {
                              labels: {
                                font: { size: 12 },
                                color: '#333'
                              }
                            }
                          }
                        }"
                      />
                    </div>
                  </div>

                </div>
              </div>
            </div>

            <!-- ACTIVIDAD COMUNITARIA -->
            <div class="col-lg-6">
              <div class="row g-4">

                <div class="col-12">
                  <div class="card border-0 shadow-sm">
                    <div class="card-header bg-white border-0 pt-3 pb-2">
                      <h5 class="fw-bold mb-0">
                        <span class="badge bg-warning me-2">📅</span>
                        Actividad Comunitaria
                      </h5>
                    </div>

                    <div class="card-body p-3" style="overflow: hidden;">
                      <h6 class="fw-bold text-primary small mb-2">Próximos Eventos (Top 2)</h6>

                      <ul class="list-group list-group-flush mb-3">
                        <li
                          v-for="(act, index) in proximasActividades"
                          :key="index"
                          class="list-group-item p-2 d-flex justify-content-between"
                        >
                          <div>
                            <span class="badge bg-secondary-subtle text-secondary me-2">{{ act.tipo }}</span>
                            <span class="fw-semibold small">{{ act.nombre }}</span>
                          </div>
                          <span class="small text-muted">{{ act.fecha }}</span>
                        </li>
                      </ul>

                      <h6 class="fw-bold text-success small mb-2">Autoridades Activas</h6>

                      <ul class="list-group list-group-flush">
                        <li
                          v-for="(auth, index) in autoridadesActivas"
                          :key="index"
                          class="list-group-item p-2 d-flex justify-content-between"
                        >
                          <div class="d-flex align-items-center">
                            <i class="bi bi-person-circle text-success me-2"></i>
                            <span class="fw-semibold small">{{ auth.rol }}</span>
                          </div>
                          <span class="badge bg-success-subtle text-success small">
                            {{ auth.nombre.split(' ')[0] }}
                          </span>
                        </li>
                      </ul>

                    </div>
                  </div>
                </div>

                <!-- INDICADORES DEMOGRÁFICOS -->
                <div class="col-12">
                  <div class="card border-0 shadow-sm">
                    <div class="card-header bg-white border-0 pt-3 pb-2">
                      <h5 class="fw-bold mb-0">
                        <span class="badge bg-secondary me-2">📋</span>
                        Indicadores Demográficos
                      </h5>
                    </div>

                    <div class="card-body p-3" style="overflow: hidden;">
                      <div class="row g-2">
                        <div
                          v-for="(indicator, key) in indicadoresCompactos"
                          :key="key"
                          class="col-6"
                        >
                          <div class="p-2 rounded-2 border bg-light">
                            <div class="d-flex flex-column align-items-start">
                              <div class="fw-bold small" :style="{ color: indicator.color }">
                                {{ indicator.value }}
                              </div>
                              <div class="text-muted small">{{ indicator.label }}</div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                  </div>
                </div>

              </div>
            </div>

          </div>
        </div>

      </div>

      <!-- FILA INFERIOR -->
      <div class="row g-4 mt-3">

        <!-- COMPOSICIÓN ETARIA -->
        <div class="col-lg-4">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-header bg-white border-0 pt-3 pb-2">
              <h5 class="fw-bold mb-0">
                <span class="badge bg-info me-2">👶</span>
                Composición Etaria
              </h5>
            </div>
            <div class="card-body p-0" style="height: 320px; overflow: hidden;">
              <ChartPanel
                noCard="true"
                height="320px"
                chart-id="edadChart"
                type="bar"
                :data="edadData"
                :options="{ maintainAspectRatio: false, scales: { x: { stacked: true }, y: { stacked: true } } }"
              />
            </div>
          </div>
        </div>

        <!-- DISTRIBUCIÓN GÉNERO -->
        <div class="col-lg-4">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-header bg-white border-0 pt-3 pb-2">
              <h5 class="fw-bold mb-0">
                <span class="badge bg-primary me-2">👥</span>
                Distribución por Género
              </h5>
            </div>

            <div class="card-body p-4 d-flex flex-column justify-content-center" style="height: 320px; overflow: hidden;">
              <div class="d-flex flex-column gap-3">

                <!-- MASCULINO -->
                <div class="d-flex align-items-center gap-3">
                  <div class="gender-icon text-primary"><i class="bi bi-gender-male"></i></div>
                  <div class="flex-grow-1">
                    <div class="d-flex justify-content-between">
                      <span class="fw-semibold small">Masculino</span>
                      <span class="fw-bold small text-primary">{{ generoPorcentajes.masculino }}%</span>
                    </div>
                    <div class="progress" style="height: 10px;">
                      <div
                        class="progress-bar bg-primary"
                        role="progressbar"
                        :style="{width: generoPorcentajes.masculino + '%'}"
                      ></div>
                    </div>
                  </div>
                </div>

                <!-- FEMENINO -->
                <div class="d-flex align-items-center gap-3">
                  <div class="gender-icon text-danger"><i class="bi bi-gender-female"></i></div>
                  <div class="flex-grow-1">
                    <div class="d-flex justify-content-between">
                      <span class="fw-semibold small">Femenino</span>
                      <span class="fw-bold small text-danger">{{ generoPorcentajes.femenino }}%</span>
                    </div>
                    <div class="progress" style="height: 10px;">
                      <div
                        class="progress-bar bg-danger"
                        role="progressbar"
                        :style="{width: generoPorcentajes.femenino + '%'}"
                      ></div>
                    </div>
                  </div>
                </div>

                <!-- OTRO -->
                <div class="d-flex align-items-center gap-3">
                  <div class="gender-icon text-secondary"><i class="bi bi-gender-ambiguous"></i></div>
                  <div class="flex-grow-1">
                    <div class="d-flex justify-content-between">
                      <span class="fw-semibold small">Otro</span>
                      <span class="fw-bold small text-secondary">{{ generoPorcentajes.otro }}%</span>
                    </div>
                    <div class="progress" style="height: 10px;">
                      <div
                        class="progress-bar bg-secondary"
                        role="progressbar"
                        :style="{width: generoPorcentajes.otro + '%'}"
                      ></div>
                    </div>
                  </div>
                </div>

              </div>
            </div>

          </div>
        </div>

        <!-- INDICADORES CLAVE -->
        <div class="col-lg-4">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-header bg-white border-0 pt-3 pb-2">
              <h5 class="fw-bold mb-0">
                <span class="badge bg-success me-2">🎯</span>
                Indicadores Clave
              </h5>
            </div>

            <div class="card-body p-0" style="height: 320px; overflow: hidden;">
              <div style="height: 250px; position: relative;">
                <ChartPanel
                  noCard="true"
                  height="250px"
                  chart-id="radarChart"
                  type="doughnut"
                  :data="indicadoresData"
                  :options="{
                    maintainAspectRatio: false,
                    cutout: '65%',
                    plugins: {
                      legend: { display: true, position: 'bottom' },
                      tooltip: { enabled: true }
                    }
                  }"
                />
              </div>
            </div>

          </div>
        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ChartPanel from '../../components/graficas/ChartPanel.vue'

/* ---------------------------------------------
   DATOS GLOBALES
--------------------------------------------- */

const currentYear = ref(2025)
const nombreComunidad = ref('Comunidad Indígena El Refugio')

const heroMetrics = ref({
  poblacion: { value: '1,847', label: 'Población Total', sublabel: '512 familias', trend: 2.8, color: '#3b82f6' },
  familiar: { value: '3.6', label: 'Promedio Familiar', sublabel: 'Personas/hogar', trend: 0.5, color: '#10b981' },
  educacion: { value: '78%', label: 'Cobertura Educativa', sublabel: 'Escolaridad', trend: 3.2, color: '#f59e0b' },
  empleo: { value: '62%', label: 'Tasa de Empleo', sublabel: 'Población activa', trend: -1.2, color: '#ef4444' }
})

const indicadoresCompactos = ref({
  dependencia: { value: '61.4%', label: 'Tasa de Dependencia', color: '#ff7043' },
  servicios: { value: '88%', label: 'Hogares con Servicios', color: '#42a5f5' },
  alfabetizacion: { value: '92.2%', label: 'Alfabetización', color: '#10b981' },
  familiar: { value: '512', label: 'Total Familias', color: '#f59e0b' }
})

/* ---------------------------------------------
   GESTIÓN SOCIAL
--------------------------------------------- */

const gestionSocial = ref([
  { label: 'Programas Activos', value: 5, color: '#17a2b8' },
  { label: 'Beneficiarios Totales', value: 53, color: '#fd7e14' },
  { label: 'Autoridades Activas', value: 2, color: '#28a745' },
  { label: 'Actividades Realizadas', value: 3, color: '#6f42c1' }
])

const programasTipoRadarData = ref({
  labels: ['Salud', 'Educación', 'Cultural', 'Infraestructura', 'Asistencia'],
  datasets: [
    {
      label: 'Programas',
      data: [4, 5, 3, 2, 5],
      backgroundColor: 'rgba(59, 130, 246, 0.3)',
      borderColor: '#3b82f6',
      pointBackgroundColor: ['#10b981', '#f59e0b', '#8b5cf6', '#ef4444', '#06b6d4']
    }
  ]
})

const proximasActividades = ref([
  { nombre: 'Actividad Deportiva', tipo: 'Planificada', fecha: '13/11/2025' },
  { nombre: 'Taller', tipo: 'Planificada', fecha: '12/11/2025' }
])

const autoridadesActivas = ref([
  { rol: 'Coordinador', nombre: 'Sebastián bolivar velez' },
  { rol: 'Secretario', nombre: 'john eduard velez vasca' }
])

/* ---------------------------------------------
   GRÁFICAS
--------------------------------------------- */

const evolucionData = ref({
  labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago'],
  datasets: [
    {
      label: 'Registros',
      data: [142, 158, 133, 165, 152, 173, 168, 181],
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      fill: true,
      tension: 0.4,
      borderWidth: 2
    },
    {
      label: 'Meta',
      data: [150, 160, 155, 170, 165, 175, 170, 180],
      borderColor: '#10b981',
      backgroundColor: 'rgba(16, 185, 129, 0.05)',
      fill: true,
      tension: 0.4,
      borderDash: [5, 5],
      borderWidth: 2
    }
  ]
})

const ocupacionData = ref({
  labels: ['Hombres', 'Mujeres'],
  datasets: [
    {
      data: [55.2, 44.8],
      backgroundColor: ['#3b82f6', '#ec4899'],
      borderWidth: 0
    }
  ]
})

const desocupacionData = ref({
  labels: ['Hombres', 'Mujeres'],
  datasets: [
    {
      data: [38.5, 61.5],
      backgroundColor: ['#3b82f6', '#ec4899'],
      borderWidth: 0
    }
  ]
})

/* ---------------------------------------------
   DISTRIBUCIÓN POR GÉNERO
--------------------------------------------- */

const rawGeneroData = ref({
  femenino: 941,
  masculino: 892,
  otro: 14
})

const generoPorcentajes = computed(() => {
  const total =
    rawGeneroData.value.femenino +
    rawGeneroData.value.masculino +
    rawGeneroData.value.otro

  return {
    femenino: Math.round((rawGeneroData.value.femenino / total) * 100),
    masculino: Math.round((rawGeneroData.value.masculino / total) * 100),
    otro: Math.round((rawGeneroData.value.otro / total) * 100)
  }
})

/* ---------------------------------------------
   INDICADORES RADAR
--------------------------------------------- */

const indicadoresData = ref({
  labels: ['Alfabetización', 'Empleo', 'Educación', 'Salud', 'Vivienda', 'Servicios'],
  datasets: [
    {
      data: [92, 62, 78, 85, 71, 88],
      backgroundColor: ['#8b5cf6', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#6b7280'],
      borderWidth: 0
    }
  ]
})

/* ---------------------------------------------
   EDAD (CORREGIDO COMPLETO)
--------------------------------------------- */

const edadData = ref({
  labels: ['0-5', '6-12', '13-17', '18-30', '31-50', '51-65', '65+'],
  datasets: [
    {
      label: 'Hombres',
      backgroundColor: '#3b82f6',
      data: [132, 241, 152, 321, 290, 184, 72]
    },
    {
      label: 'Mujeres',
      backgroundColor: '#ec4899',
      data: [141, 252, 160, 335, 301, 170, 82]
    }
  ]
})
</script>

<style scoped>
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}
.gender-icon {
  font-size: 1.4rem;
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
