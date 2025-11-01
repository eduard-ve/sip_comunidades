import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import { createPinia } from 'pinia'
import { useAuth } from './stores/auth.js'

// Estilos globales
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import './assets/css/main.scss'

// Importar JavaScript de Bootstrap para funcionalidad completa
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

const app = createApp(App)
const pinia = createPinia()

app.use(router)
app.use(pinia)

// Inicializar autenticación al cargar la aplicación
const { initAuth } = useAuth()
initAuth()

app.mount('#app')
