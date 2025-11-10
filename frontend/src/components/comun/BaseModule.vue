<template>
  <div class="container-fluid py-4">
    <!-- Header -->
    <div class="d-flex flex-wrap align-items-center justify-content-between mb-3 gap-2">
      <div>
        <nav v-if="breadcrumbs && breadcrumbs.length" aria-label="breadcrumb">
          <ol class="breadcrumb mb-1">
            <li
              v-for="(bc, i) in breadcrumbs"
              :key="i"
              class="breadcrumb-item"
              :class="{ active: i === breadcrumbs.length - 1 }"
              aria-current="page"
            >
              <template v-if="bc.to && i !== breadcrumbs.length - 1">
                <router-link :to="bc.to">{{ bc.label }}</router-link>
              </template>
              <template v-else>{{ bc.label }}</template>
            </li>
          </ol>
        </nav>
        <h2 class="fw-bold mb-0">{{ title }}</h2>
      </div>

      <!-- Acciones -->
      <div class="d-flex align-items-center gap-2">
        <slot name="actions">
          <button
            v-if="showCreate"
            class="btn btn-primary btn-sm nuevo-programa-btn"
            style="background-color: #198754 !important; border-color: #198754 !important; color: white !important;"
            @click="$emit('create')"
          >
            <i class="bi bi-plus-lg me-1"></i> Nuevo Programa
          </button>

          <button v-if="showExport" class="btn btn-outline-secondary btn-sm" @click="$emit('export')">
            <i class="bi bi-download me-1"></i> Exportar
          </button>
        </slot>
      </div>
    </div>

    <!-- KPIs -->
    <div v-if="kpis && kpis.length" class="row g-3 mb-3">
      <div class="col-12 col-sm-6 col-lg-3" v-for="(k, idx) in kpis" :key="idx">
        <KpiCard
          :title="k.title"
          :value="k.value"
          :change="k.change"
          :icon="k.icon"
          :colorIcon="k.colorIcon || '#0d6efd'"
          :colorBorder="k.colorBorder || '#eaeef5'"
        />
      </div>
    </div>

    <!-- Extra contenido encima de charts -->
    <slot name="extra"></slot>

    <!-- Charts -->
    <div class="row g-3">
      <div class="col-12 col-lg-6">
        <slot name="left">
          <ChartPanel
            v-if="charts?.left?.data"
            :chart-id="charts.left.id || 'leftChart'"
            :type="charts.left.type || 'bar'"
            :data="charts.left.data"
            :options="charts.left.options || {}"
          >
            <template #title>
              {{ charts.left.title || "Gráfico izquierdo" }}
            </template>
          </ChartPanel>
        </slot>
      </div>

      <div class="col-12 col-lg-6">
        <slot name="right">
          <ChartPanel
            v-if="charts?.right?.data"
            :chart-id="charts.right.id || 'rightChart'"
            :type="charts.right.type || 'pie'"
            :data="charts.right.data"
            :options="charts.right.options || {}"
          >
            <template #title>
              {{ charts.right.title || "Gráfico derecho" }}
            </template>
          </ChartPanel>
        </slot>
      </div>
    </div>

    <!-- Tabla -->
    <div
      v-if="table && (safeColumns.length || rowsArray.length || forceTable)"
      class="card border-0 shadow-sm mt-4"
    >
      <div class="card-body">
        <!-- Barra de búsqueda -->
        <div
          v-if="showSearch && safeColumns.length"
          class="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-3"
        >
          <div class="input-group input-group-sm" style="max-width: 340px;">
            <span class="input-group-text"><i class="bi bi-search"></i></span>
            <input v-model="query" type="text" class="form-control" :placeholder="searchPlaceholder" />
          </div>
          <slot name="table-filters"></slot>
        </div>

        <!-- Tabla SIEMPRE visible si hay columnas o forceTable -->
        <div v-if="safeColumns.length || forceTable" class="table-responsive">
          <table class="table table-sm align-middle">
            <thead>
              <tr>
                <th v-for="(col, cIdx) in safeColumns" :key="cIdx" :class="col.class">
                  {{ col.label || col.key }}
                </th>
              </tr>
            </thead>

            <!-- Filas con datos -->
            <tbody v-if="filteredRows.length">
              <tr
                v-for="(row, rIdx) in filteredRows"
                :key="rIdx"
                class="table-row"
                @click="$emit('rowClick', row)"
                style="cursor:pointer"
              >
                <td v-for="(col, cIdx) in safeColumns" :key="cIdx">
                  <slot name="table-cell" :column="col" :row="row">
                    {{ displayCell(row[col.key]) }}
                  </slot>
                </td>
              </tr>
            </tbody>

            <!-- Fila vacía cuando no hay datos -->
            <tbody v-else>
              <tr>
                <td :colspan="Math.max(safeColumns.length, 1)" class="text-center text-muted py-3">
                  {{ emptyMessage }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Si no hay columnas y no quieres ver tabla, muestra mensaje genérico -->
        <div v-else-if="showEmptyMessage" class="text-center text-muted py-3">
          {{ emptyMessage }}
        </div>

        <slot name="table-footer"></slot>
      </div>
    </div>

    <!-- Contenido adicional -->
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue"
import KpiCard from "../tarjetas/KpiCard.vue"
import ChartPanel from "../graficas/ChartPanel.vue"

interface Breadcrumb { label: string; to?: string }
interface Kpi {
  title: string
  value: string | number
  change?: string
  icon?: string
  colorIcon?: string
  colorBorder?: string
}
interface ChartConfig { id?: string; type?: string; data: any; options?: any; title?: string }
interface Column { key: string; label?: string; class?: string }
interface TableConfig { columns?: Column[]; rows?: Record<string, any>[] | any } // 'any' para permitir Ref

const props = withDefaults(defineProps<{
  title?: string
  breadcrumbs?: Breadcrumb[]
  kpis?: Kpi[]
  charts?: { left?: ChartConfig; right?: ChartConfig }
  table?: TableConfig
  searchPlaceholder?: string
  showCreate?: boolean
  showExport?: boolean
  showSearch?: boolean
  showEmptyMessage?: boolean
  forceTable?: boolean
  emptyMessage?: string
}>(), {
  title: "Módulo",
  searchPlaceholder: "Buscar...",
  showCreate: false,
  showExport: false,
  showSearch: true,
  showEmptyMessage: true,
  forceTable: false,
  emptyMessage: "Sin datos para mostrar",
  table: () => ({ columns: [], rows: [] })
})

defineEmits<{
  (e: "create"): void
  (e: "export"): void
  (e: "rowClick", row: Record<string, any>): void
}>()

const query = ref("")

/** Normaliza columnas seguras */
const safeColumns = computed<Column[]>(() => {
  if (Array.isArray(props.table?.columns) && props.table!.columns!.length) {
    return props.table!.columns as Column[]
  }
  // si no hay columnas, intenta inferir desde la primera fila
  const first = rowsArray.value[0]
  if (!first) return []
  return Object.keys(first).map(k => ({ key: k, label: k }))
})

/** Normaliza rows: admite array directo o ref([]) */
const rowsArray = computed<Record<string, any>[]>(() => {
  const r: any = props.table?.rows
  if (Array.isArray(r)) return r
  if (r && Array.isArray(r.value)) return r.value
  return []
})

/** Filtrado */
const filteredRows = computed<Record<string, any>[]>(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return rowsArray.value
  return rowsArray.value.filter(row =>
    safeColumns.value.some(col =>
      String(row[col.key] ?? "").toLowerCase().includes(q)
    )
  )
})

function displayCell(value: unknown): string {
  if (value === null || value === undefined) return "—"
  if (typeof value === "boolean") return value ? "Sí" : "No"
  return String(value)
}
</script>

<style scoped>
.table-row:hover { background-color: #f8f9fa; }
</style>
