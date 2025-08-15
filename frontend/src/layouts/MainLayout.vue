<template>
  <div>
    <Navbar />
    <div class="d-flex">
      <Sidebar />
      <main class="flex-fill p-3">
        <router-view /> <!-- Aquí se renderiza el contenido de la vista -->
      </main>
    </div>
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
import Sidebar from '../components/Sidebar.vue'
</script>
