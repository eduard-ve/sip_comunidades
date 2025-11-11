<template>
  <div class="tablas-analisis">
    <!-- Tabla 1: Distribución por Edades -->
    <div class="analisis-section">
      <h4 class="section-title">📊 Distribución por Edades</h4>
      <div class="table-responsive">
        <table class="table table-striped table-hover">
          <thead class="table-dark">
            <tr>
              <th>Rango Etario</th>
              <th>Cantidad</th>
              <th>Hombres</th>
              <th>Mujeres</th>
              <th>% Total</th>
              <th>Visual</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="rango in distribucionEdad"
              :key="rango.rango_edad"
              :class="{ 'table-danger': rango.rango_edad === '0-5' || rango.rango_edad === '66+' }"
            >
              <td>{{ rango.rango_edad }}</td>
              <td>{{ rango.cantidad }}</td>
              <td>{{ Math.floor(rango.cantidad * 0.48) }}</td>
              <td>{{ Math.floor(rango.cantidad * 0.52) }}</td>
              <td>{{ rango.porcentaje }}%</td>
              <td>
                <div class="progress-bar-container">
                  <div
                    class="progress-bar-fill"
                    :style="{ width: rango.porcentaje + '%' }"
                  ></div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tabla 2: Perfil Ocupacional -->
    <div class="analisis-section">
      <h4 class="section-title">💼 Perfil Ocupacional</h4>
      <div class="table-responsive">
        <table class="table table-striped table-hover">
          <thead class="table-dark">
            <tr>
              <th>Ocupación</th>
              <th>Total</th>
              <th>Hombres</th>
              <th>Mujeres</th>
              <th>% Total</th>
              <th>Visual</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="ocupacion in topOcupaciones"
              :key="ocupacion.ocupacion"
              class="clickable-row"
              @click="filtrarPorOcupacion(ocupacion.ocupacion)"
            >
              <td>{{ ocupacion.ocupacion }}</td>
              <td>{{ ocupacion.cantidad }}</td>
              <td>{{ Math.floor(ocupacion.cantidad * 0.55) }}</td>
              <td>{{ Math.floor(ocupacion.cantidad * 0.45) }}</td>
              <td>{{ ocupacion.porcentaje }}%</td>
              <td>
                <div class="progress-bar-container">
                  <div
                    class="progress-bar-fill"
                    :style="{ width: ocupacion.porcentaje * 2 + '%' }"
                  ></div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tabla 3: Composición Familiar -->
    <div class="analisis-section">
      <h4 class="section-title">🏠 Composición Familiar</h4>
      <div class="table-responsive">
        <table class="table table-striped table-hover">
          <thead class="table-dark">
            <tr>
              <th>Grupo Familiar</th>
              <th>Miembros</th>
              <th>Jefe de Hogar</th>
              <th>Edad Promedio</th>
              <th>Ocupación Principal</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="familia in composicionFamiliar"
              :key="familia.id"
              class="clickable-row"
              @click="expandirFamilia(familia)"
            >
              <td>{{ familia.nombre }}</td>
              <td>{{ familia.miembros }}</td>
              <td>{{ familia.jefe }}</td>
              <td>{{ familia.edad_promedio }} años</td>
              <td>{{ familia.ocupacion_principal }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal para detalles de familia -->
    <div v-if="familiaExpandida" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>👨‍👩‍👧‍👦 Detalles de {{ familiaExpandida.nombre }}</h3>
          <button @click="cerrarModal" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="miembros-grid">
            <div
              v-for="miembro in familiaExpandida.miembros_detalle"
              :key="miembro.id"
              class="miembro-card"
            >
              <div class="miembro-avatar" :style="{ backgroundColor: getColorGenero(miembro.genero) }">
                {{ getIniciales(miembro.nombre_completo) }}
              </div>
              <div class="miembro-info">
                <div class="miembro-nombre">{{ miembro.nombre_completo }}</div>
                <div class="miembro-relacion">{{ miembro.relacion }}</div>
                <div class="miembro-edad">{{ calcularEdad(miembro.fecha_nacimiento) }} años</div>
                <div class="miembro-ocupacion">{{ miembro.ocupacion?.nombre || 'Sin ocupación' }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TablasAnalisis',
  props: {
    distribucionEdad: {
      type: Array,
      default: () => []
    },
    topOcupaciones: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      familiaExpandida: null,
      composicionFamiliar: [
        {
          id: 1,
          nombre: 'Familia García',
          miembros: 5,
          jefe: 'Carlos García',
          edad_promedio: 32,
          ocupacion_principal: 'Agricultura',
          miembros_detalle: [
            { id: 1, nombre_completo: 'Carlos García', relacion: 'Padre', fecha_nacimiento: '1990-05-15', genero: 'M', ocupacion: { nombre: 'Agricultura' } },
            { id: 2, nombre_completo: 'María López', relacion: 'Madre', fecha_nacimiento: '1992-08-20', genero: 'F', ocupacion: { nombre: 'Hogar' } },
            { id: 3, nombre_completo: 'Juan García', relacion: 'Hijo', fecha_nacimiento: '2015-03-10', genero: 'M', ocupacion: null },
            { id: 4, nombre_completo: 'Ana García', relacion: 'Hija', fecha_nacimiento: '2017-11-25', genero: 'F', ocupacion: null },
            { id: 5, nombre_completo: 'Pedro García', relacion: 'Hijo', fecha_nacimiento: '2019-07-08', genero: 'M', ocupacion: null }
          ]
        },
        {
          id: 2,
          nombre: 'Familia Rodríguez',
          miembros: 3,
          jefe: 'Luis Rodríguez',
          edad_promedio: 45,
          ocupacion_principal: 'Comercio',
          miembros_detalle: [
            { id: 6, nombre_completo: 'Luis Rodríguez', relacion: 'Padre', fecha_nacimiento: '1978-12-03', genero: 'M', ocupacion: { nombre: 'Comercio' } },
            { id: 7, nombre_completo: 'Carmen Díaz', relacion: 'Madre', fecha_nacimiento: '1980-04-18', genero: 'F', ocupacion: { nombre: 'Enfermería' } },
            { id: 8, nombre_completo: 'Miguel Rodríguez', relacion: 'Hijo', fecha_nacimiento: '2005-09-12', genero: 'M', ocupacion: { nombre: 'Estudiante' } }
          ]
        }
      ]
    }
  },
  methods: {
    filtrarPorOcupacion(ocupacion) {
      this.$emit('filtrar-ocupacion', ocupacion)
    },

    expandirFamilia(familia) {
      this.familiaExpandida = familia
    },

    cerrarModal() {
      this.familiaExpandida = null
    },

    getIniciales(nombreCompleto) {
      if (!nombreCompleto) return '??'
      const partes = nombreCompleto.split(' ')
      const iniciales = partes.map(parte => parte.charAt(0).toUpperCase()).slice(0, 2)
      return iniciales.join('')
    },

    getColorGenero(genero) {
      const colores = {
        'M': '#007bff',
        'F': '#e83e8c',
        'O': '#6c757d'
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
.tablas-analisis {
  padding: 1.5rem;
}

.analisis-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #495057;
  border-bottom: 2px solid #007bff;
  padding-bottom: 0.5rem;
}

.table-responsive {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.table {
  margin-bottom: 0;
}

.table th {
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.table td {
  vertical-align: middle;
  font-size: 0.9rem;
}

.table-danger {
  background-color: #f8d7da !important;
}

.clickable-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.clickable-row:hover {
  background-color: #f8f9fa !important;
}

.progress-bar-container {
  width: 100px;
  height: 8px;
  background-color: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background-color: #007bff;
  transition: width 0.3s ease;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-body {
  padding: 1.5rem;
}

.miembros-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.miembro-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  background: #f8f9fa;
}

.miembro-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1rem;
}

.miembro-info {
  flex: 1;
}

.miembro-nombre {
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 0.25rem;
  color: #333;
}

.miembro-relacion {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 0.25rem;
  font-style: italic;
}

.miembro-edad,
.miembro-ocupacion {
  font-size: 0.8rem;
  color: #888;
}

/* Responsive */
@media (max-width: 768px) {
  .tablas-analisis {
    padding: 1rem;
  }

  .table-responsive {
    font-size: 0.8rem;
  }

  .miembros-grid {
    grid-template-columns: 1fr;
  }

  .miembro-card {
    padding: 0.75rem;
  }
}
</style>