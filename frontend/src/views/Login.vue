<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card p-4" style="width: 300px;">
      <h4 class="mb-3 text-center">Iniciar Sesión</h4>
      <input v-model="username" type="text" class="form-control mb-2" placeholder="Usuario">
      <input v-model="password" type="password" class="form-control mb-3" placeholder="Contraseña">
      <button class="btn btn-primary w-100" @click="login">Entrar</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref } from 'vue';
const router = useRouter();
const username = ref('');
const password = ref('');

function login() {
  // Simulación de login
  if (username.value && password.value) {
    router.push('/dashboard');
  }
}
</script>
