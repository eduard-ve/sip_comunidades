<template>
  <div class="card dashboard-card shadow-sm border-0 h-100 p-3">
    <div class="d-flex align-items-center">
      <i :class="icon" class="fs-1 me-3" :style="{ color: colorIcon }"></i>
      <div>
        <h6 class="text-muted mb-0">{{ title }}</h6>
        <h4 class="fw-bold mb-0">{{ value }}</h4>
        <small :class="change > 0 ? 'text-success fw-semibold' : 'text-danger fw-semibold'">
          {{ change > 0 ? '+' : '' }}{{ change }}%
        </small>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
  change: Number,
  icon: String,
  colorIcon: { type: String, default: '#0d6efd' }
})
</script>

<style scoped>
.dashboard-card {
  border-radius: 12px;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s;
}
.dashboard-card:hover {
  transform: translateY(-4px);
  box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1);
}
</style>
