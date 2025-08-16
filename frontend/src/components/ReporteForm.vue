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
              <!-- Título -->
              <div class="col-md-6">
                <label class="form-label fw-bold">Título</label>
                <input v-model="form.titulo" type="text" class="form-control" required />
              </div>

              <!-- Módulo -->
              <div class="col-md-6">
                <label class="form-label fw-bold">Módulo</label>
                <select v-model="form.modulo" class="form-select" required>
                  <option value="">Seleccione...</option>
                  <option value="Salud">Salud</option>
                  <option value="Educación">Educación</option>
                  <option value="Social">Social</option>
                </select>
              </div>

              <!-- Fecha -->
              <div class="col-md-6">
                <label class="form-label fw-bold">Fecha</label>
                <input v-model="form.fecha" type="date" class="form-control" required />
              </div>

              <!-- Configuración automática -->
              <div class="col-md-6">
                <label class="form-label fw-bold">Configuración automática</label>
                <select v-model="form.auto" class="form-select">
                  <option value="">Ninguna</option>
                  <option value="diario">Diario</option>
                  <option value="semanal">Semanal</option>
                  <option value="mensual">Mensual</option>
                </select>
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
  titulo: "",
  modulo: "",
  fecha: "",
  descripcion: "",
  auto: ""
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
  if (!form.titulo || !form.modulo || !form.fecha) {
    alert("Por favor complete los campos obligatorios.")
    return
  }

  loading.value = true
  setTimeout(() => {
    emit("save", { ...form })
    loading.value = false
  }, 800) // Simulación de petición async
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
