<template>
  <BaseModule
    title="Auditoría"
    :breadcrumbs="[
      { label: 'Inicio', to: '/' },
      { label: 'Auditoría' }
    ]"
    :table="{ columns, rows }"
    search-placeholder="Buscar evento…"
    @rowClick="verDetalle"
    @export="exportarAuditoria"
  >
    <!-- Filtros -->
    <template #table-filters>
      <div class="d-flex flex-wrap gap-2">
        <!-- Filtro por módulo -->
        <select v-model="filtros.modulo" class="form-select form-select-sm">
          <option value="">Todos los módulos</option>
          <option v-for="m in modulos" :key="m" :value="m">{{ m }}</option>
        </select>

        <!-- Filtro por usuario -->
        <select v-model="filtros.usuario" class="form-select form-select-sm">
          <option value="">Todos los usuarios</option>
          <option v-for="u in usuarios" :key="u" :value="u">{{ u }}</option>
        </select>

        <!-- Filtro por fecha -->
        <input
          type="date"
          v-model="filtros.fecha"
          class="form-control form-control-sm"
        />
      </div>
    </template>
  </BaseModule>
</template>

<script setup>
import { ref, computed } from "vue"
import BaseModule from "../components/BaseModule.vue"
import { useRouter } from "vue-router"

const router = useRouter()

// Definición de columnas de la tabla
const columns = [
  { key: "id", label: "ID" },
  { key: "modulo", label: "Módulo" },
  { key: "usuario", label: "Usuario" },
  { key: "accion", label: "Acción" },
  { key: "fecha", label: "Fecha" }
]

// Datos mock (aquí luego se conectaría a la API)
const eventos = ref([
  { id: 1, modulo: "Usuarios", usuario: "Admin", accion: "Creó usuario Juan", fecha: "2025-08-01" },
  { id: 2, modulo: "Roles", usuario: "María", accion: "Actualizó permisos", fecha: "2025-08-10" },
  { id: 3, modulo: "Reportes", usuario: "Pedro", accion: "Descargó informe PDF", fecha: "2025-08-12" }
])

// Filtros
const filtros = ref({ modulo: "", usuario: "", fecha: "" })

const modulos = ["Usuarios", "Roles", "Reportes"]
const usuarios = ["Admin", "María", "Pedro"]

// Filtrado dinámico
const rows = computed(() => {
  return eventos.value.filter(e => {
    return (
      (!filtros.value.modulo || e.modulo === filtros.value.modulo) &&
      (!filtros.value.usuario || e.usuario === filtros.value.usuario) &&
      (!filtros.value.fecha || e.fecha === filtros.value.fecha)
    )
  })
})

// Navegar a detalle
function verDetalle(evento) {
  router.push({ name: "auditoria-detalle", params: { id: evento.id } })
}

// Exportar auditoría
function exportarAuditoria() {
  alert("Exportando auditoría en Excel/PDF...")
}
</script>
