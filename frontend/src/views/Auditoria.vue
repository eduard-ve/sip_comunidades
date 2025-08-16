<template>
  <div class="container-fluid py-4">
    <!-- Título y exportación -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-bold">Auditoría</h2>
      <div class="d-flex gap-2">
        <button class="btn btn-success btn-sm" @click="exportExcel">
          <i class="bi bi-file-earmark-excel"></i> Exportar Excel
        </button>
        <button class="btn btn-danger btn-sm" @click="exportPdf">
          <i class="bi bi-file-earmark-pdf"></i> Exportar PDF
        </button>
      </div>
    </div>

    <!-- Componente de tabla -->
    <AuditTable :events="events" @view-details="showDetails" />

    <!-- Modal detalle -->
    <div v-if="selectedEvent" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Detalle del evento</h5>
            <button type="button" class="btn-close" @click="selectedEvent = null"></button>
          </div>
          <div class="modal-body">
            <p><strong>Módulo:</strong> {{ selectedEvent.module }}</p>
            <p><strong>Usuario:</strong> {{ selectedEvent.user }}</p>
            <p><strong>Acción:</strong> {{ selectedEvent.action }}</p>
            <p><strong>Fecha:</strong> {{ selectedEvent.date }}</p>

            <h6 class="fw-bold mt-3">Cambios</h6>
            <ul>
              <li v-for="(value, field) in selectedEvent.changes" :key="field">
                <strong>{{ field }}:</strong> {{ value.old }} → {{ value.new }}
              </li>
            </ul>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="selectedEvent = null">Cerrar</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="selectedEvent" class="modal-backdrop fade show"></div>
  </div>
</template>

<script setup>
import { ref, } from "vue"
import AuditTable from "../components/AuditTable.vue"

const events = ref([
  {
    id: 1,
    module: "usuarios",
    user: "admin",
    action: "Creación de usuario",
    date: "2025-08-15",
    changes: { nombre: { old: "-", new: "Juan" }, rol: { old: "-", new: "Editor" } }
  },
  {
    id: 2,
    module: "reportes",
    user: "soporte",
    action: "Eliminación de reporte",
    date: "2025-08-14",
    changes: { reporte: { old: "Reporte A", new: "-" } }
  },
  {
    id: 3,
    module: "encuestas",
    user: "usuario1",
    action: "Modificación de encuesta",
    date: "2025-08-13",
    changes: { titulo: { old: "Encuesta 2024", new: "Encuesta 2025" } }
  }
])

const selectedEvent = ref(null)

function exportExcel() {
  alert("Exportando a Excel...")
}

function exportPdf() {
  alert("Exportando a PDF...")
}

function showDetails(event) {
  selectedEvent.value = event
}
</script>
