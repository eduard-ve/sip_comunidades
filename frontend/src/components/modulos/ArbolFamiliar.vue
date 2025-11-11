<template>
  <div class="arbol-familiar">
    <div class="arbol-header">
      <h2>🌳 Árbol Familiar</h2>
      <select v-model="personaSeleccionadaId" @change="cargarArbol" class="persona-selector">
        <option value="">Selecciona una persona</option>
        <option
          v-for="persona in todasLasPersonas"
          :key="persona.id"
          :value="persona.value"
        >
          {{ persona.label }}
        </option>
      </select>
    </div>

    <div v-if="cargando" class="loading">
      <div class="spinner"></div>
      <p>Cargando árbol familiar...</p>
    </div>

    <div v-else-if="!personaSeleccionadaId" class="no-selection">
      <p>👆 Selecciona una persona para ver su árbol familiar</p>
    </div>

    <div v-else class="arbol-container">
      <!-- Nivel 1: Padres -->
      <div class="nivel padres">
        <div
          v-for="familiar in relacionesFiltradas.padres"
          :key="familiar.id"
          class="nodo-familiar padre"
          @click="cambiarPersonaCentral(familiar)"
        >
          <div class="nodo-avatar" :style="{ backgroundColor: getColorGenero(familiar.genero) }">
            {{ getIniciales(familiar.nombre_completo) }}
          </div>
          <div class="nodo-info">
            <div class="nodo-nombre">{{ familiar.nombre_completo }}</div>
            <div class="nodo-relacion">Padre/Madre</div>
            <div class="nodo-edad">{{ familiar.edad }} años</div>
            <div class="nodo-ocupacion">{{ familiar.ocupacion || 'Sin ocupación' }}</div>
          </div>
        </div>
      </div>

      <!-- Conexión vertical -->
      <div class="conexion-vertical"></div>

      <!-- Nivel 2: Persona central -->
      <div class="nivel central">
        <div class="nodo-familiar central-nodo">
          <div class="nodo-avatar central-avatar" :style="{ backgroundColor: getColorGenero(personaCentral.genero) }">
            {{ getIniciales(personaCentral.nombre_completo) }}
          </div>
          <div class="nodo-info">
            <div class="nodo-nombre central-nombre">{{ personaCentral.nombre_completo }}</div>
            <div class="nodo-relacion">Persona Central</div>
            <div class="nodo-edad">{{ personaCentral.edad }} años</div>
            <div class="nodo-ocupacion">{{ personaCentral.ocupacion || 'Sin ocupación' }}</div>
          </div>
        </div>
      </div>

      <!-- Conexión vertical -->
      <div class="conexion-vertical"></div>

      <!-- Nivel 3: Pareja e hijos -->
      <div class="nivel descendientes">
        <!-- Pareja -->
        <div
          v-for="familiar in relacionesFiltradas.pareja"
          :key="familiar.id"
          class="nodo-familiar pareja"
          @click="cambiarPersonaCentral(familiar)"
        >
          <div class="nodo-avatar" :style="{ backgroundColor: getColorGenero(familiar.genero) }">
            {{ getIniciales(familiar.nombre_completo) }}
          </div>
          <div class="nodo-info">
            <div class="nodo-nombre">{{ familiar.nombre_completo }}</div>
            <div class="nodo-relacion">Pareja</div>
            <div class="nodo-edad">{{ familiar.edad }} años</div>
            <div class="nodo-ocupacion">{{ familiar.ocupacion || 'Sin ocupación' }}</div>
          </div>
        </div>

        <!-- Hijos -->
        <div
          v-for="familiar in relacionesFiltradas.hijos"
          :key="familiar.id"
          class="nodo-familiar hijo"
          @click="cambiarPersonaCentral(familiar)"
        >
          <div class="nodo-avatar" :style="{ backgroundColor: getColorGenero(familiar.genero) }">
            {{ getIniciales(familiar.nombre_completo) }}
          </div>
          <div class="nodo-info">
            <div class="nodo-nombre">{{ familiar.nombre_completo }}</div>
            <div class="nodo-relacion">Hijo/a</div>
            <div class="nodo-edad">{{ familiar.edad }} años</div>
            <div class="nodo-ocupacion">{{ familiar.ocupacion || 'Sin ocupación' }}</div>
          </div>
        </div>
      </div>

      <!-- Nivel 4: Hermanos (lateral) -->
      <div class="nivel hermanos">
        <div
          v-for="familiar in relacionesFiltradas.hermanos"
          :key="familiar.id"
          class="nodo-familiar hermano"
          @click="cambiarPersonaCentral(familiar)"
        >
          <div class="nodo-avatar" :style="{ backgroundColor: getColorGenero(familiar.genero) }">
            {{ getIniciales(familiar.nombre_completo) }}
          </div>
          <div class="nodo-info">
            <div class="nodo-nombre">{{ familiar.nombre_completo }}</div>
            <div class="nodo-relacion">Hermano/a</div>
            <div class="nodo-edad">{{ familiar.edad }} años</div>
            <div class="nodo-ocupacion">{{ familiar.ocupacion || 'Sin ocupación' }}</div>
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
          <span>Hombres</span>
        </div>
        <div class="leyenda-item">
          <div class="leyenda-color" style="background-color: #e83e8c;"></div>
          <span>Mujeres</span>
        </div>
        <div class="leyenda-item">
          <div class="leyenda-color" style="background-color: #6c757d;"></div>
          <span>Otro</span>
        </div>
      </div>
      <p class="leyenda-nota">💡 Haz clic en cualquier persona para centrar el árbol en ella</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ArbolFamiliar',
  props: {
    personas: {
      type: Array,
      default: () => []
    },
    relacionesFamiliares: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      personaSeleccionadaId: '',
      personaCentral: null,
      relacionesActuales: [],
      cargando: false
    }
  },
  computed: {
    todasLasPersonas() {
      return this.personas.map(persona => ({
        value: persona.id,
        label: `${persona.nombre_completo} (${this.calcularEdad(persona.fecha_nacimiento)} años)`
      }))
    },
    relacionesFiltradas() {
      if (!this.relacionesActuales.length) {
        return {
          padres: [],
          pareja: [],
          hijos: [],
          hermanos: []
        }
      }

      const padres = []
      const pareja = []
      const hijos = []
      const hermanos = []

      this.relacionesActuales.forEach(relacion => {
        const relacionLower = relacion.relacion.toLowerCase()

        if (relacionLower.includes('padre') || relacionLower.includes('madre')) {
          padres.push(relacion)
        } else if (relacionLower.includes('pareja') || relacionLower.includes('esposo') || relacionLower.includes('esposa')) {
          pareja.push(relacion)
        } else if (relacionLower.includes('hijo') || relacionLower.includes('hija')) {
          hijos.push(relacion)
        } else if (relacionLower.includes('hermano') || relacionLower.includes('hermana')) {
          hermanos.push(relacion)
        }
      })

      return {
        padres,
        pareja,
        hijos,
        hermanos
      }
    }
  },
  methods: {
    async cargarArbol() {
      if (!this.personaSeleccionadaId) {
        this.personaCentral = null
        this.relacionesActuales = []
        return
      }

      this.cargando = true

      try {
        // Buscar la persona central
        this.personaCentral = this.personas.find(p => p.id == this.personaSeleccionadaId)
        if (this.personaCentral) {
          this.personaCentral.edad = this.calcularEdad(this.personaCentral.fecha_nacimiento)
          this.personaCentral.ocupacion = this.personaCentral.ocupacion?.nombre || null
        }

        // Cargar relaciones familiares desde API
        const response = await fetch(`/api/poblacion/estadisticas/personas/${this.personaSeleccionadaId}/relaciones-familiares/`)
        if (response.ok) {
          this.relacionesActuales = await response.json()
        } else {
          console.error('Error al cargar relaciones familiares')
          this.relacionesActuales = []
        }
      } catch (error) {
        console.error('Error:', error)
        this.relacionesActuales = []
      } finally {
        this.cargando = false
      }
    },

    cambiarPersonaCentral(familiar) {
      this.personaSeleccionadaId = familiar.id
      this.cargarArbol()
    },

    getIniciales(nombreCompleto) {
      if (!nombreCompleto) return '??'
      const partes = nombreCompleto.split(' ')
      const iniciales = partes.map(parte => parte.charAt(0).toUpperCase()).slice(0, 2)
      return iniciales.join('')
    },

    getColorGenero(genero) {
      const colores = {
        'M': '#007bff', // Azul para hombres
        'F': '#e83e8c', // Rosa para mujeres
        'O': '#6c757d'  // Gris para otro
      }
      return colores[genero] || '#6c757d'
    },

    calcularEdad(fechaNacimiento) {
      if (!fechaNacimiento) return 'N/A'
      const hoy = new Date()
      const nacimiento = new Date(fechaNacimiento)
      let edad = hoy.getFullYear() - nacimiento.getFullYear()
      const mes = hoy.getMonth() - nacimiento.getMonth()
      if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
        edad--
      }
      return edad
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