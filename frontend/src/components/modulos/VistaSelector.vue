<template>
  <div class="vista-selector">
    <div class="selector-buttons">
      <button
        v-for="vista in vistas"
        :key="vista.id"
        @click="cambiarVista(vista.id)"
        :class="['vista-btn', { active: vistaActiva === vista.id }]"
      >
        <span class="vista-icon">{{ vista.icon }}</span>
        <span class="vista-text">{{ vista.nombre }}</span>
      </button>
    </div>

    <!-- Contenido dinámico según la vista seleccionada -->
    <div class="vista-content">
      <!-- Vista Tabla -->
      <div v-if="vistaActiva === 'tabla'" class="vista-tabla">
        <div class="table-responsive">
          <table class="table table-striped table-hover">
            <thead class="table-dark">
              <tr>
                <th v-for="col in tableColumns" :key="col.key">{{ col.label }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="persona in personasFiltradas" :key="persona.id">
                <td>{{ persona.nombre_completo }}</td>
                <td>{{ persona.numero_identificacion }}</td>
                <td>{{ persona.fecha_nacimiento }}</td>
                <td>{{ persona.genero }}</td>
                <td>{{ persona.nivel_educativo_nombre || 'N/A' }}</td>
                <td>{{ persona.ocupacion_nombre || 'N/A' }}</td>
                <td>{{ persona.estado_civil_nombre || 'N/A' }}</td>
                <td>{{ persona.direccion || 'N/A' }}</td>
                <td>{{ persona.lengua_materna_nombre || 'N/A' }}</td>
                <td>
                  <button @click="editarPersona(persona)" class="btn btn-sm btn-outline-warning">
                    ✏️ Editar
                  </button>
                  <button @click="eliminarPersona(persona)" class="btn btn-sm btn-outline-danger ms-1">
                    🗑️ Eliminar
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Vista Tarjetas -->
      <div v-else-if="vistaActiva === 'tarjetas'" class="vista-tarjetas">
        <PersonasCards
          :personas="personasFiltradas"
          :cargando="cargando"
          @ver-arbol-familiar="verArbolFamiliar"
          @editar-persona="editarPersona"
        />
      </div>

      <!-- Vista Árbol Familiar -->
      <div v-else-if="vistaActiva === 'arbol'" class="vista-arbol">
        <ArbolFamiliar
          :personas="personas"
          :relaciones-familiares="relacionesFamiliares"
        />
      </div>

      <!-- Vista Gráficas -->
      <div v-else-if="vistaActiva === 'graficas'" class="vista-graficas">
        <div class="charts-grid">
          <div class="chart-item">
            <DistribucionGenero :data="distribucionGenero" />
          </div>
          <div class="chart-item">
            <TopOcupaciones :data="topOcupaciones" />
          </div>
          <div class="chart-item">
            <DistribucionEducativa :data="distribucionEducativa" />
          </div>
          <div class="chart-item">
            <LenguasMaternas :data="lenguasMaternas" />
          </div>
          <div class="chart-item">
            <DistribucionEdad :data="distribucionEdad" />
          </div>
          <div class="chart-item">
            <PopulationPyramid :data="distribucionEdad" />
          </div>
        </div>
      </div>

      <!-- Vista Análisis -->
      <div v-else-if="vistaActiva === 'analisis'" class="vista-analisis">
        <TablasAnalisis
          :distribucion-edad="distribucionEdad"
          :top-ocupaciones="topOcupaciones"
          @filtrar-ocupacion="filtrarPorOcupacion"
        />
      </div>
    </div>
  </div>
</template>

<script>
import PersonasCards from './PersonasCards.vue'
import ArbolFamiliar from './ArbolFamiliar.vue'
import DistribucionGenero from '../graficas/DistribucionGenero.vue'
import TopOcupaciones from '../graficas/TopOcupaciones.vue'
import DistribucionEducativa from '../graficas/DistribucionEducativa.vue'
import LenguasMaternas from '../graficas/LenguasMaternas.vue'
import DistribucionEdad from '../graficas/DistribucionEdad.vue'
import PopulationPyramid from '../graficas/PopulationPyramid.vue'
import TablasAnalisis from './TablasAnalisis.vue'

export default {
  name: 'VistaSelector',
  components: {
    PersonasCards,
    ArbolFamiliar,
    DistribucionGenero,
    TopOcupaciones,
    DistribucionEducativa,
    LenguasMaternas,
    DistribucionEdad,
    PopulationPyramid,
    TablasAnalisis
  },
  props: {
    personas: {
      type: Array,
      default: () => []
    },
    personasFiltradas: {
      type: Array,
      default: () => []
    },
    relacionesFamiliares: {
      type: Array,
      default: () => []
    },
    distribucionGenero: {
      type: Array,
      default: () => []
    },
    topOcupaciones: {
      type: Array,
      default: () => []
    },
    distribucionEducativa: {
      type: Array,
      default: () => []
    },
    lenguasMaternas: {
      type: Array,
      default: () => []
    },
    distribucionEdad: {
      type: Array,
      default: () => []
    },
    cargando: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      vistaActiva: 'tarjetas', // Vista por defecto
      vistas: [
        { id: 'tabla', nombre: 'Tabla', icon: '📊' },
        { id: 'tarjetas', nombre: 'Tarjetas', icon: '📇' },
        { id: 'arbol', nombre: 'Árbol Familiar', icon: '🌳' },
        { id: 'graficas', nombre: 'Gráficas', icon: '📈' },
        { id: 'analisis', nombre: 'Análisis', icon: '📋' }
      ],
      tableColumns: [
        { key: 'nombre_completo', label: 'Nombre Completo' },
        { key: 'numero_identificacion', label: 'ID' },
        { key: 'fecha_nacimiento', label: 'Fecha Nacimiento' },
        { key: 'genero', label: 'Género' },
        { key: 'nivel_educativo', label: 'Educación' },
        { key: 'ocupacion', label: 'Ocupación' },
        { key: 'estado_civil', label: 'Estado Civil' },
        { key: 'direccion', label: 'Dirección' },
        { key: 'lengua_materna', label: 'Lengua Materna' },
        { key: 'acciones', label: 'Acciones' }
      ]
    }
  },
  methods: {
    cambiarVista(vistaId) {
      this.vistaActiva = vistaId
      this.$emit('vista-cambiada', vistaId)
    },

    verDetalle(persona) {
      this.$emit('ver-detalle', persona)
    },

    verArbolFamiliar(persona) {
      this.cambiarVista('arbol')
      // Aquí podríamos emitir un evento para seleccionar la persona en el árbol
      this.$emit('ver-arbol-familiar', persona)
    },

    editarPersona(persona) {
      this.$emit('editar-persona', persona)
    },

    filtrarPorOcupacion(ocupacion) {
      this.$emit('filtrar-ocupacion', ocupacion)
    },

    eliminarPersona(persona) {
      if (confirm(`¿Seguro que deseas eliminar a ${persona.nombre_completo}?`)) {
        this.$emit('eliminar-persona', persona)
      }
    },

    personaEliminada(persona) {
      // Este método será llamado desde el componente padre para actualizar la vista
      // La lógica de eliminación se maneja en GestionPoblacional.vue
    }
  }
}
</script>

<style scoped>
.vista-selector {
  width: 100%;
}

.selector-buttons {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  justify-content: center;
}

.vista-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: 2px solid #e9ecef;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  font-weight: 500;
  color: #495057;
}

.vista-btn:hover {
  border-color: #007bff;
  background: #f8f9ff;
  transform: translateY(-1px);
}

.vista-btn.active {
  border-color: #007bff;
  background: #007bff;
  color: white;
  box-shadow: 0 2px 4px rgba(0,123,255,0.3);
}

.vista-icon {
  font-size: 1.1rem;
}

.vista-content {
  width: 100%;
}

/* Vista Tabla */
.vista-tabla {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.table-responsive {
  max-height: 600px;
  overflow-y: auto;
}

.table {
  margin-bottom: 0;
}

.table th {
  position: sticky;
  top: 0;
  background: #343a40;
  color: white;
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 1rem 0.75rem;
}

.table td {
  padding: 0.75rem;
  vertical-align: middle;
  font-size: 0.85rem;
}

/* Vista Tarjetas */
.vista-tarjetas {
  /* Los estilos están en PersonasCards.vue */
}

/* Vista Árbol */
.vista-arbol {
  /* Los estilos están en ArbolFamiliar.vue */
}

/* Vista Gráficas */
.vista-graficas {
  padding: 1rem 0;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.chart-item {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 1rem;
}

/* Vista Análisis */
.vista-analisis {
  /* Los estilos están en TablasAnalisis.vue */
}

/* Responsive */
@media (max-width: 768px) {
  .selector-buttons {
    flex-direction: column;
    align-items: stretch;
  }

  .vista-btn {
    justify-content: center;
    padding: 0.5rem 1rem;
  }

  .charts-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .chart-item {
    padding: 0.5rem;
  }

  .table-responsive {
    max-height: 400px;
  }

  .table th,
  .table td {
    padding: 0.5rem 0.25rem;
    font-size: 0.75rem;
  }
}
</style>