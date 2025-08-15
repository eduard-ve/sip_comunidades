import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'

// Estilos globales
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import './assets/css/main.scss'

createApp(App)
  .use(router)
  .mount('#app')
