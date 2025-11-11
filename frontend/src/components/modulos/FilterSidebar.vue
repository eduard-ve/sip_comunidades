<template>
  <div class="filter-sidebar">
    <h3 class="filter-title">🔍 Filtros de Búsqueda</h3>

    <!-- Filtro Rango de Edad -->
    <div class="filter-group">
      <label class="filter-label">Edad</label>
      <div class="age-range">
        <input
          type="number"
          v-model="filtros.edad_min"
          placeholder="Mín"
          min="0"
          max="120"
          class="age-input"
          @input="emitirFiltros"
        />
        <span class="age-separator">-</span>
        <input
          type="number"
          v-model="filtros.edad_max"
          placeholder="Máx"
          min="0"
          max="120"
          class="age-input"
          @input="emitirFiltros"
        />
      </div>
      <div class="age-display">
        Edad: {{ filtros.edad_min || 0 }} - {{ filtros.edad_max || 100 }} años
      </div>
    </div>

    <!-- Filtro Género -->
    <div class="filter-group">
      <label class="filter-label">Género</label>
      <div class="checkbox-group">
        <label v-for="genero in opcionesGenero" :key="genero.value" class="checkbox-label">
          <input
            type="checkbox"
            :value="genero.value"
            v-model="filtros.genero"
            @change="emitirFiltros"
          />
          {{ genero.label }}
        </label>
      </div>
    </div>

    <!-- Filtro Ocupación -->
    <div class="filter-group">
      <label class="filter-label">Ocupación</label>
      <select v-model="filtros.ocupacion_id" @change="emitirFiltros" class="filter-select">
        <option value="">Todas las ocupaciones</option>
        <option
          v-for="ocupacion in ocupaciones"
          :key="ocupacion.id"
          :value="ocupacion.id"
        >
          {{ ocupacion.nombre }}
        </option>
      </select>
    </div>

    <!-- Filtro Nivel Educativo -->
    <div class="filter-group">
      <label class="filter-label">Nivel Educativo</label>
      <select v-model="filtros.nivel_educativo_id" @change="emitirFiltros" class="filter-select">
        <option value="">Todos los niveles</option>
        <option
          v-for="nivel in nivelesEducativos"
          :key="nivel.id"
          :value="nivel.id"
        >
          {{ nivel.nombre }}
        </option>
      </select>
    </div>

    <!-- Filtro Estado Civil -->
    <div class="filter-group">
      <label class="filter-label">Estado Civil</label>
      <div class="checkbox-group">
        <label v-for="estado in estadosCiviles" :key="estado.id" class="checkbox-label">
          <input
            type="checkbox"
            :value="estado.id"
            v-model="filtros.estado_civil_ids"
            @change="emitirFiltros"
          />
          {{ estado.nombre }}
        </label>
      </div>
    </div>

    <!-- Filtro Lengua Materna -->
    <div class="filter-group">
      <label class="filter-label">Lengua Materna</label>
      <select v-model="filtros.lengua_id" @change="emitirFiltros" class="filter-select">
        <option value="">Todas las lenguas</option>
        <option
          v-for="lengua in lenguas"
          :key="lengua.id"
          :value="lengua.id"
        >
          {{ lengua.nombre }}
        </option>
      </select>
    </div>

    <!-- Botón Limpiar Filtros -->
    <button @click="limpiarFiltros" class="clear-filters-btn">
      🗑️ Limpiar Filtros
    </button>
  </div>
</template>

<script>
export default {
  name: 'FilterSidebar',
  props: {
    ocupaciones: {
      type: Array,
      default: () => []
    },
    nivelesEducativos: {
      type: Array,
      default: () => []
    },
    estadosCiviles: {
      type: Array,
      default: () => []
    },
    lenguas: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      filtros: {
        edad_min: null,
        edad_max: null,
        genero: [],
        ocupacion_id: '',
        nivel_educativo_id: '',
        estado_civil_ids: [],
        lengua_id: ''
      },
      opcionesGenero: [
        { value: 'M', label: 'Masculino' },
        { value: 'F', label: 'Femenino' },
        { value: 'O', label: 'Otro' }
      ]
    }
  },
  methods: {
    emitirFiltros() {
      // Debounce para evitar llamadas excesivas
      clearTimeout(this.debounceTimer)
      this.debounceTimer = setTimeout(() => {
        this.$emit('filtro-cambio', { ...this.filtros })
      }, 300)
    },
    limpiarFiltros() {
      this.filtros = {
        edad_min: null,
        edad_max: null,
        genero: [],
        ocupacion_id: '',
        nivel_educativo_id: '',
        estado_civil_ids: [],
        lengua_id: ''
      }
      this.$emit('filtros-limpios')
    }
  }
}
</script>

<style scoped>
.filter-sidebar {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-right: 1px solid #e9ecef;
  height: 100%;
  overflow-y: auto;
  width: 280px;
}

.filter-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #495057;
  border-bottom: 2px solid #007bff;
  padding-bottom: 0.5rem;
}

.filter-group {
  margin-bottom: 1.5rem;
}

.filter-label {
  display: block;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #495057;
  font-size: 0.9rem;
}

.age-range {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.age-input {
  width: 60px;
  padding: 0.375rem 0.5rem;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  font-size: 0.875rem;
}

.age-separator {
  color: #6c757d;
  font-weight: 500;
}

.age-display {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #6c757d;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #495057;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  margin: 0;
  width: 16px;
  height: 16px;
}

.filter-select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  background-color: white;
}

.clear-filters-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 0.25rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 1rem;
}

.clear-filters-btn:hover {
  background-color: #c82333;
}

/* Responsive */
@media (max-width: 768px) {
  .filter-sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #e9ecef;
    max-height: 300px;
  }

  .age-range {
    flex-wrap: wrap;
  }

  .age-input {
    width: 50px;
  }
}
</style>