<template>
  <div class="table-responsive">
    <table class="table table-striped table-hover align-middle">
      <thead class="table-primary">
        <tr>
          <th v-for="header in headers" :key="header">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, rowIndex) in items" :key="rowIndex">
          <td v-for="header in headers" :key="header">{{ item[header] }}</td>
        </tr>
        <tr v-if="items.length === 0">
          <td :colspan="headers.length" class="text-center text-muted py-3">
            No hay datos para mostrar
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  headers: {
    type: Array,
    required: true
  },
  items: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.table {
  font-size: 0.9rem;
}
</style>
