<template>
  <div class="modal fade show d-block" tabindex="-1">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content shadow-lg border-0">
        <!-- Header -->
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-file-earmark-text me-2"></i>
            {{ reporte ? "Editar reporte" : "Nuevo reporte" }}
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <!-- Body -->
        <div class="modal-body">
          <form @submit.prevent="guardar">
            <div class="row g-3">
              <!-- Tipo de reporte -->
              <div class="col-md-6">
                <label class="form-label fw-bold">Tipo de reporte</label>
                <select v-model="form.tipo_reporte" class="form-select" required>
                  <option value="">Seleccione...</option>
                  <option value="reporte_salud">Reporte de Salud</option>
                  <option value="reporte_social">Reporte Social</option>
                  <option value="reporte_encuestas">Reporte de Encuestas</option>
                </select>
              </div>

              <!-- Fecha del reporte -->
              <div class="col-md-6">
                <label class="form-label fw-bold">Fecha del reporte</label>
                <input v-model="form.fecha_reporte" type="date" class="form-control" required />
              </div>

              <!-- Persona (ID) -->
              <div class="col-md-6">
                <label class="form-label fw-bold">ID de Persona</label>
                <input v-model="form.persona" type="number" class="form-control" required min="1" />
              </div>

              <!-- Descripción -->
              <div class="col-12">
                <label class="form-label fw-bold">Descripción</label>
                <textarea v-model="form.descripcion" class="form-control" rows="3"></textarea>
              </div>
            </div>
          </form>
        </div>

        <!-- Footer -->
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="$emit('close')">
            <i class="bi bi-x-circle me-1"></i> Cancelar
          </button>
          <button class="btn btn-primary" :disabled="loading" @click="guardar">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            <i class="bi bi-save me-1"></i> Guardar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch, ref } from "vue"

const props = defineProps({
  reporte: { type: Object, default: null }
})
const emit = defineEmits(["close", "save"])

const loading = ref(false)

const form = reactive({
  persona: 1, // ID de persona por defecto
  tipo_reporte: "",
  datos_agregados: {},
  fecha_reporte: "",
  generado_por: "Usuario Frontend",
  descripcion: ""
})

// Rellenar datos si es edición
watch(
  () => props.reporte,
  (val) => {
    if (val) Object.assign(form, val)
  },
  { immediate: true }
)

async function guardar() {
  if (!form.tipo_reporte || !form.fecha_reporte || !form.persona) {
    alert("Por favor complete los campos obligatorios.")
    return
  }

  loading.value = true
  try {
    // Preparar datos para el backend
    const reporteData = {
      persona: form.persona,
      tipo_reporte: form.tipo_reporte,
      datos_agregados: form.datos_agregados || {},
      fecha_reporte: form.fecha_reporte,
      generado_por: form.generado_por
    }

    emit("save", reporteData)
  } catch (error) {
    console.error('Error al guardar:', error)
    alert("Error al guardar el reporte")
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal {
  background: rgba(0, 0, 0, 0.5);
}
.modal-title {
  font-weight: bold;
}
</style>
