<template>
  <div class="personas-cards">
    <div v-if="cargando" class="loading">
      <div class="spinner"></div>
      <p>Cargando personas...</p>
    </div>

    <div v-else-if="personas.length === 0" class="no-data">
      <p>📭 No se encontraron personas con los filtros aplicados</p>
    </div>

    <div v-else class="cards-grid">
      <div
        v-for="persona in personas"
        :key="persona.id"
        class="persona-card"
        @click="abrirModalDetalle(persona)"
      >
        <!-- Avatar con iniciales -->
        <div class="card-avatar" :style="{ backgroundColor: getColorAvatar(persona.nombre_completo) }">
          {{ getIniciales(persona.nombre_completo) }}
        </div>

        <!-- Información principal -->
        <div class="card-content">
          <h3 class="card-nombre">{{ persona.nombre_completo }}</h3>
          <p class="card-edad">{{ calcularEdad(persona.fecha_nacimiento) }} años</p>
          <p class="card-ocupacion">{{ persona.ocupacion?.nombre || 'Sin ocupación' }}</p>

          <!-- Estado civil con icono -->
          <div class="card-estado-civil">
            <span class="estado-icon">{{ getIconoEstadoCivil(persona.estado_civil?.nombre) }}</span>
            <span class="estado-texto">{{ persona.estado_civil?.nombre || 'No especificado' }}</span>
          </div>

          <!-- Género con icono -->
          <div class="card-genero">
            <span class="genero-icon">{{ getIconoGenero(persona.genero) }}</span>
            <span class="genero-texto">{{ getTextoGenero(persona.genero) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de detalle mejorado -->
    <div v-if="modalVisible" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <!-- Header con avatar -->
        <div class="modal-header">
          <div class="header-info">
            <div class="header-avatar" :style="{ backgroundColor: getColorAvatar(personaSeleccionada?.nombre_completo) }">
              {{ getIniciales(personaSeleccionada?.nombre_completo) }}
            </div>
            <div class="header-details">
              <h2>{{ personaSeleccionada?.nombre_completo }}</h2>
              <div class="header-meta">
                <span class="meta-item">{{ calcularEdad(personaSeleccionada?.fecha_nacimiento) }} años</span>
                <span class="meta-item">{{ getTextoGenero(personaSeleccionada?.genero) }}</span>
                <span class="meta-item">{{ personaSeleccionada?.numero_identificacion }}</span>
              </div>
            </div>
          </div>
          <button @click="cerrarModal" class="close-btn">&times;</button>
        </div>

        <!-- Tabs de navegación -->
        <div class="modal-tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="tabActiva = tab.id"
            :class="['tab-btn', { active: tabActiva === tab.id }]"
          >
            {{ tab.icon }} {{ tab.nombre }}
          </button>
        </div>

        <div class="modal-body">
          <!-- Tab Información Personal -->
          <div v-if="tabActiva === 'personal'" class="tab-content">
            <div class="info-cards">
              <div class="info-card">
                <h4>📋 Identificación</h4>
                <div class="card-content">
                  <div class="info-row">
                    <span class="label">Tipo ID:</span>
                    <span class="value">{{ personaSeleccionada?.tipo_identificacion?.nombre || 'N/A' }}</span>
                  </div>
                  <div class="info-row">
                    <span class="label">Número:</span>
                    <span class="value">{{ personaSeleccionada?.numero_identificacion }}</span>
                  </div>
                  <div class="info-row">
                    <span class="label">Fecha Nacimiento:</span>
                    <span class="value">{{ formatFecha(personaSeleccionada?.fecha_nacimiento) }}</span>
                  </div>
                </div>
              </div>

              <div class="info-card">
                <h4>👤 Datos Personales</h4>
                <div class="card-content">
                  <div class="info-row">
                    <span class="label">Nombre Completo:</span>
                    <span class="value">{{ personaSeleccionada?.nombre_completo }}</span>
                  </div>
                  <div class="info-row">
                    <span class="label">Género:</span>
                    <span class="value">{{ getTextoGenero(personaSeleccionada?.genero) }}</span>
                  </div>
                  <div class="info-row">
                    <span class="label">Edad:</span>
                    <span class="value">{{ calcularEdad(personaSeleccionada?.fecha_nacimiento) }} años</span>
                  </div>
                  <div class="info-row">
                    <span class="label">Dirección:</span>
                    <span class="value">{{ personaSeleccionada?.direccion || 'No especificada' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Tab Información Socioeconómica -->
          <div v-if="tabActiva === 'socioeconomica'" class="tab-content">
            <div class="info-cards">
              <div class="info-card">
                <h4>💼 Situación Laboral</h4>
                <div class="card-content">
                  <div class="info-row">
                    <span class="label">Ocupación:</span>
                    <span class="value">{{ personaSeleccionada?.ocupacion?.nombre || 'No especificada' }}</span>
                  </div>
                  <div class="info-row">
                    <span class="label">Estado Civil:</span>
                    <span class="value">{{ personaSeleccionada?.estado_civil?.nombre || 'No especificado' }}</span>
                  </div>
                </div>
              </div>

              <div class="info-card">
                <h4>🎓 Nivel Educativo</h4>
                <div class="card-content">
                  <div class="info-row">
                    <span class="label">Nivel:</span>
                    <span class="value">{{ personaSeleccionada?.nivel_educativo?.nombre || 'No especificado' }}</span>
                  </div>
                  <div class="info-row">
                    <span class="label">Grupo Familiar:</span>
                    <span class="value">{{ personaSeleccionada?.grupo_familiar?.nombre || 'No especificado' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Tab Información Cultural -->
          <div v-if="tabActiva === 'cultural'" class="tab-content">
            <div class="info-cards">
              <div class="info-card">
                <h4>🌍 Origen Cultural</h4>
                <div class="card-content">
                  <div class="info-row">
                    <span class="label">Lengua Materna:</span>
                    <span class="value">{{ personaSeleccionada?.lengua_materna?.nombre || 'No especificada' }}</span>
                  </div>
                  <div class="info-row">
                    <span class="label">Tradiciones:</span>
                    <span class="value">{{ personaSeleccionada?.tradiciones || 'No especificadas' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Tab Relaciones Familiares -->
          <div v-if="tabActiva === 'familiares'" class="tab-content">
            <div v-if="relacionesFamiliares.length === 0" class="no-relations">
              <p>🔍 Cargando relaciones familiares...</p>
            </div>
            <div v-else class="relaciones-grid">
              <div
                v-for="relacion in relacionesFamiliares"
                :key="relacion.id"
                class="relacion-card"
                @click="verDetalleFamiliar(relacion)"
              >
                <div class="relacion-avatar" :style="{ backgroundColor: getColorGenero(relacion.genero) }">
                  {{ getIniciales(relacion.nombre_completo) }}
                </div>
                <div class="relacion-info">
                  <div class="relacion-nombre">{{ relacion.nombre_completo }}</div>
                  <div class="relacion-tipo">{{ relacion.relacion }}</div>
                  <div class="relacion-edad">{{ relacion.edad }} años</div>
                  <div class="relacion-ocupacion">{{ relacion.ocupacion || 'Sin ocupación' }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <div class="footer-right">
            <button @click="verArbolFamiliar" class="btn-info">🌳 Árbol Familiar</button>
            <button @click="editarPersona" class="btn-warning">✏️ Editar</button>
            <button @click="eliminarPersona" class="btn-danger">🗑️ Eliminar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PersonasCards',
  props: {
    personas: {
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
      modalVisible: false,
      personaSeleccionada: null,
      relacionesFamiliares: [],
      tabActiva: 'personal',
      tabs: [
        { id: 'personal', nombre: 'Personal', icon: '👤' },
        { id: 'socioeconomica', nombre: 'Socioeconómica', icon: '💼' },
        { id: 'cultural', nombre: 'Cultural', icon: '🌍' },
        { id: 'familiares', nombre: 'Familiares', icon: '👨‍👩‍👧‍👦' }
      ]
    }
  },
  methods: {
    getIniciales(nombreCompleto) {
      if (!nombreCompleto) return '??'
      const partes = nombreCompleto.split(' ')
      const iniciales = partes.map(parte => parte.charAt(0).toUpperCase()).slice(0, 2)
      return iniciales.join('')
    },

    getColorAvatar(nombreCompleto) {
      const colores = [
        '#007bff', '#28a745', '#dc3545', '#ffc107', '#17a2b8',
        '#6f42c1', '#e83e8c', '#fd7e14', '#20c997', '#6c757d'
      ]
      const index = nombreCompleto ? nombreCompleto.length % colores.length : 0
      return colores[index]
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
    },

    getIconoEstadoCivil(estadoCivil) {
      const iconos = {
        'Soltero': '🕺',
        'Casado': '💍',
        'Divorciado': '💔',
        'Viudo': '🕊️',
        'Unión Libre': '❤️'
      }
      return iconos[estadoCivil] || '❓'
    },

    getIconoGenero(genero) {
      const iconos = {
        'M': '👨',
        'F': '👩',
        'O': '🧑'
      }
      return iconos[genero] || '❓'
    },

    getTextoGenero(genero) {
      const textos = {
        'M': 'Masculino',
        'F': 'Femenino',
        'O': 'Otro'
      }
      return textos[genero] || 'No especificado'
    },

    formatFecha(fecha) {
      if (!fecha) return 'No especificada'
      return new Date(fecha).toLocaleDateString('es-ES')
    },

    async abrirModalDetalle(persona) {
      this.personaSeleccionada = persona
      this.tabActiva = 'personal'

      // Cargar relaciones familiares
      try {
        const response = await fetch(`/api/poblacion/estadisticas/personas/${persona.id}/relaciones-familiares/`)
        if (response.ok) {
          this.relacionesFamiliares = await response.json()
        } else {
          this.relacionesFamiliares = []
        }
      } catch (error) {
        console.error('Error cargando relaciones familiares:', error)
        this.relacionesFamiliares = []
      }

      this.modalVisible = true
    },

    cerrarModal() {
      this.modalVisible = false
      this.personaSeleccionada = null
      this.relacionesFamiliares = []
      this.tabActiva = 'personal'
    },

    verArbolFamiliar() {
      this.$emit('ver-arbol-familiar', this.personaSeleccionada)
      this.cerrarModal()
    },

    editarPersona() {
      this.$emit('editar-persona', this.personaSeleccionada)
      this.cerrarModal()
    },

    eliminarPersona() {
      if (confirm(`¿Seguro que deseas eliminar a ${this.personaSeleccionada.nombre_completo}?`)) {
        this.$emit('eliminar-persona', this.personaSeleccionada)
        this.cerrarModal()
      }
    },

    verDetalleFamiliar(familiar) {
      // Cambiar a vista de árbol familiar con el familiar seleccionado
      this.$emit('ver-arbol-familiar', { ...this.personaSeleccionada, cambiarA: familiar.id })
      this.cerrarModal()
    },

    imprimirDatos() {
      // Funcionalidad de impresión
      window.print()
    },

    exportarIndividual() {
      // Exportar datos individuales a PDF (se implementará en tarea 12)
      console.log('Exportar individual:', this.personaSeleccionada)
    }
  }
}
</script>

<style scoped>
.personas-cards {
  padding: 1rem;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: #6c757d;
  font-size: 1.1rem;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.persona-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.persona-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  border-color: #007bff;
}

.card-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
  margin: 0 auto 1rem;
}

.card-content {
  text-align: center;
}

.card-nombre {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
}

.card-edad {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.card-ocupacion {
  font-size: 0.85rem;
  color: #888;
  margin-bottom: 0.75rem;
  font-style: italic;
}

.card-estado-civil,
.card-genero {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.estado-icon,
.genero-icon {
  font-size: 1rem;
}

/* Modal Styles Mejorado */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
  backdrop-filter: blur(2px);
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 95%;
  max-width: 900px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.modal-header {
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  color: white;
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.header-details h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.header-meta {
  display: flex;
  gap: 1rem;
  margin-top: 0.25rem;
  font-size: 0.9rem;
  opacity: 0.9;
}

.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: white;
  padding: 0.5rem;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.modal-tabs {
  display: flex;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.tab-btn {
  flex: 1;
  padding: 1rem;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  color: #6c757d;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.tab-btn:hover {
  background: #e9ecef;
  color: #495057;
}

.tab-btn.active {
  background: white;
  color: #007bff;
  border-bottom: 3px solid #007bff;
  font-weight: 600;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 0;
}

.tab-content {
  padding: 1.5rem;
}

.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.info-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  border-left: 4px solid #007bff;
}

.info-card h4 {
  margin: 0 0 1rem 0;
  color: #495057;
  font-size: 1.1rem;
  font-weight: 600;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e9ecef;
}

.info-row:last-child {
  border-bottom: none;
}

.label {
  font-weight: 500;
  color: #6c757d;
  font-size: 0.9rem;
}

.value {
  font-weight: 600;
  color: #495057;
  text-align: right;
  flex: 1;
  margin-left: 1rem;
}

.relaciones-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.relacion-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.relacion-card:hover {
  background: white;
  border-color: #007bff;
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.1);
}

.relacion-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1rem;
  color: white;
}

.relacion-info {
  flex: 1;
}

.relacion-nombre {
  font-weight: 600;
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
  color: #333;
}

.relacion-tipo {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 0.25rem;
  font-style: italic;
}

.relacion-edad,
.relacion-ocupacion {
  font-size: 0.8rem;
  color: #888;
}

.no-relations {
  text-align: center;
  padding: 2rem;
  color: #6c757d;
}

.modal-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-top: 1px solid #e9ecef;
  background: #f8f9fa;
}

.footer-left,
.footer-right {
  display: flex;
  gap: 0.5rem;
}

.btn-primary,
.btn-secondary,
.btn-info,
.btn-warning,
.btn-danger {
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-info {
  background: #17a2b8;
  color: white;
}

.btn-warning {
  background: #ffc107;
  color: #212529;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
  transform: translateY(-1px);
}

.btn-secondary:hover {
  background: #545b62;
  transform: translateY(-1px);
}

.btn-info:hover {
  background: #138496;
  transform: translateY(-1px);
}

.btn-warning:hover {
  background: #e0a800;
  transform: translateY(-1px);
}

.btn-danger:hover {
  background: #c82333;
  transform: translateY(-1px);
}

/* Responsive */
@media (max-width: 768px) {
  .cards-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 0.75rem;
  }

  .persona-card {
    padding: 1rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .modal-content {
    width: 95%;
    margin: 1rem;
  }

  .modal-footer {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }
}
</style>