<template>
  <div class="arbol-familiar">
    <div class="arbol-header">
      <h2>🌍 Lenguas por Grupo Étnico</h2>
      <select v-model="grupoSeleccionadoId" @change="cargarArbol" class="persona-selector">
        <option value="">Selecciona un grupo étnico</option>
        <option
          v-for="grupo in todosLosGrupos"
          :key="grupo.id"
          :value="grupo.id"
        >
          {{ grupo.nombre }}
        </option>
      </select>
    </div>

    <div v-if="cargando" class="loading">
      <div class="spinner"></div>
      <p>Cargando árbol familiar...</p>
    </div>

    <div v-else-if="!grupoSeleccionadoId" class="no-selection">
      <p>👆 Selecciona un grupo étnico para ver sus lenguas maternas</p>
    </div>

    <div v-else class="arbol-container">
      <!-- Nivel 1: Grupo Étnico Central -->
      <div class="nivel central">
        <div class="nodo-familiar central-nodo grupo-etnico">
          <div class="nodo-avatar central-avatar" style="background-color: #007bff;">
            🌍
          </div>
          <div class="nodo-info">
            <div class="nodo-nombre central-nombre">{{ grupoSeleccionado.nombre }}</div>
            <div class="nodo-relacion">Grupo Étnico</div>
            <div class="nodo-edad">{{ lenguasActuales.length }} lenguas</div>
            <div class="nodo-ocupacion">Lenguas maternas habladas</div>
          </div>
        </div>
      </div>

      <!-- Conexión vertical -->
      <div class="conexion-vertical"></div>

      <!-- Nivel 2: Lenguas Maternas -->
      <div class="nivel lenguas">
        <div
          v-for="lengua in lenguasActuales"
          :key="lengua.id"
          class="nodo-familiar lengua"
        >
          <div class="nodo-avatar" style="background-color: #28a745;">
            🗣️
          </div>
          <div class="nodo-info">
            <div class="nodo-nombre">{{ lengua.nombre }}</div>
            <div class="nodo-relacion">Lengua Materna</div>
            <div class="nodo-edad">{{ lengua.cantidad_hablantes }} hablantes</div>
            <div class="nodo-ocupacion">Idioma nativo</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Leyenda -->
    <div class="leyenda">
      <h4>Leyenda</h4>
      <div class="leyenda-items">
        <div class="leyenda-item">
          <div class="leyenda-color" style="background-color: #007bff;"></div>
          <span>🌍 Grupo Étnico</span>
        </div>
        <div class="leyenda-item">
          <div class="leyenda-color" style="background-color: #28a745;"></div>
          <span>🗣️ Lengua Materna</span>
        </div>
      </div>
      <p class="leyenda-nota">💡 Selecciona un grupo étnico para ver sus lenguas maternas</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ArbolFamiliar',
  props: {
    gruposEtnicos: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      grupoSeleccionadoId: '',
      grupoSeleccionado: null,
      lenguasActuales: [],
      cargando: false
    }
  },
  computed: {
    todosLosGrupos() {
      return this.gruposEtnicos
    }
  },
  methods: {
    async cargarArbol() {
      if (!this.grupoSeleccionadoId) {
        this.grupoSeleccionado = null
        this.lenguasActuales = []
        return
      }

      this.cargando = true

      try {
        // Buscar el grupo étnico seleccionado
        this.grupoSeleccionado = this.gruposEtnicos.find(g => g.id == this.grupoSeleccionadoId)

        // Cargar lenguas maternas desde API
        const response = await poblacionService.getLenguasPorGrupoEtnico(this.grupoSeleccionadoId)
        this.lenguasActuales = response.data
      } catch (error) {
        console.error('Error al cargar lenguas maternas:', error)
        this.lenguasActuales = []
      } finally {
        this.cargando = false
      }
    }
  }
}
</script>

<style scoped>
.arbol-familiar {
  padding: 1.5rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.arbol-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.arbol-header h2 {
  margin: 0;
  color: #333;
}

.persona-selector {
  padding: 0.5rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 0.9rem;
  min-width: 250px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-selection {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
  font-size: 1.1rem;
}

.arbol-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 600px;
}

.nivel {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin: 1rem 0;
  flex-wrap: wrap;
}

.padres {
  margin-top: 2rem;
}

.central {
  margin: 2rem 0;
}

.descendientes {
  margin-bottom: 2rem;
}

.hermanos {
  position: absolute;
  right: 2rem;
  flex-direction: column;
  gap: 1rem;
}

.conexion-vertical {
  width: 2px;
  height: 40px;
  background: #007bff;
  position: relative;
}

.conexion-vertical::before {
  content: '';
  position: absolute;
  top: -5px;
  left: -5px;
  width: 12px;
  height: 12px;
  background: #007bff;
  border-radius: 50%;
}

.nodo-familiar {
  background: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  min-width: 180px;
  text-align: center;
}

.nodo-familiar:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  border-color: #007bff;
}

.central-nodo {
  border-color: #007bff;
  background: #f8f9ff;
}

.nodo-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1rem;
  margin: 0 auto 0.75rem;
}

.central-avatar {
  width: 60px;
  height: 60px;
  font-size: 1.2rem;
}

.nodo-info {
  text-align: center;
}

.nodo-nombre {
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
  color: #333;
  word-break: break-word;
}

.central-nombre {
  font-size: 1rem;
  font-weight: 700;
}

.nodo-relacion {
  font-size: 0.75rem;
  color: #666;
  margin-bottom: 0.25rem;
  font-style: italic;
}

.nodo-edad {
  font-size: 0.8rem;
  color: #888;
  margin-bottom: 0.25rem;
}

.nodo-ocupacion {
  font-size: 0.75rem;
  color: #999;
  font-style: italic;
}

.leyenda {
  margin-top: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.leyenda h4 {
  margin: 0 0 1rem 0;
  color: #495057;
}

.leyenda-items {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.leyenda-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #666;
}

.leyenda-color {
  width: 16px;
  height: 16px;
  border-radius: 50%;
}

.leyenda-nota {
  font-size: 0.8rem;
  color: #888;
  font-style: italic;
  margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .arbol-header {
    flex-direction: column;
    align-items: stretch;
  }

  .persona-selector {
    min-width: auto;
  }

  .nivel {
    gap: 1rem;
  }

  .hermanos {
    position: static;
    flex-direction: row;
    justify-content: center;
    margin-top: 1rem;
  }

  .nodo-familiar {
    min-width: 150px;
    padding: 0.75rem;
  }

  .nodo-avatar {
    width: 40px;
    height: 40px;
    font-size: 0.9rem;
  }

  .central-avatar {
    width: 50px;
    height: 50px;
    font-size: 1rem;
  }

  .leyenda-items {
    justify-content: center;
  }
}
</style>